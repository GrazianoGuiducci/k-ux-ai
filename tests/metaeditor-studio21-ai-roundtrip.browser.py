#!/usr/bin/env python3
"""Real Studio21 data handback: public AI export -> edited JSON -> selective merge -> Undo/Redo.

Private local content must survive an AI return that excludes it. This uses
synthetic data only, no AI provider and no remote execution. Browser controller
owns merge/history; the test does not modify ccm.document.v1 directly in-app.
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PRIV_PATH = Path(__file__).with_name("metaeditor-studio21-privacy.browser.py")
spec = importlib.util.spec_from_file_location("studio21_privacy_test", PRIV_PATH)
assert spec and spec.loader
priv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(priv)

NEW_ID = "ai-roundtrip-new-card"
NEW_LINK = "ai-roundtrip-new-link"
SUFFIX = " [AI return]"


def scene_items(model):
    scene = model["scenes"][0]
    return {node["id"]: node for node in scene["elements"]}, {edge["id"]: edge for edge in scene["links"]}


def run(browser, name, width, html: str):
    page = browser.new_page(viewport={"width": width, "height": 844}, accept_downloads=True)
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.route("**/*", lambda route: route.abort())
    page.route("https://studio21.invalid/standalone", lambda route: route.fulfill(
        status=200, headers={"content-type": "text/html; charset=utf-8"}, body=html
    ))
    try:
        page.goto("https://studio21.invalid/standalone", wait_until="domcontentloaded")
        page.locator("#saveBtn").wait_for(state="attached")
        before = priv.parse_html(priv.downloaded(page, "#saveBtn"))
        before_nodes, before_links = scene_items(before)
        assert priv.NOTE_ID in before_nodes and priv.LINK_ID in before_links

        page.locator("#exportData").evaluate("(button) => button.click()")
        page.locator("#aiShareDialog").wait_for(state="visible")
        assert not page.locator("#aiSharePrivate").is_checked()
        outgoing = json.loads(priv.downloaded(page, "#aiShareConfirm"))
        out_nodes, out_links = scene_items(outgoing)
        assert priv.NOTE_ID not in out_nodes and priv.LINK_ID not in out_links
        public_candidates = [n for n in outgoing["scenes"][0]["elements"]
                             if n["type"] in ("text", "card") and isinstance(n.get("text"), str)]
        assert public_candidates, (name, width, "no public text target")
        target = public_candidates[0]
        target_id = target["id"]
        old_text = target["text"]
        target["text"] = old_text + SUFFIX
        outgoing["scenes"][0]["elements"].append({
            "id": NEW_ID, "type": "card", "x": 650, "y": 490, "w": 180, "h": 90,
            "text": "Added via AI data handback", "fontSize": 20,
            "color": "#183146", "fill": "#e7f5f0"
        })
        outgoing["scenes"][0]["links"].append({
            "id": NEW_LINK, "from": target_id, "to": NEW_ID,
            "label": "new public relation", "width": 2, "color": "#087b70"
        })

        payload = json.dumps(outgoing, ensure_ascii=False).encode("utf-8")
        page.locator("#importDataFile").set_input_files({
            "name": "ai-return-synthetic.json", "mimeType": "application/json", "buffer": payload
        })
        page.wait_for_function("document.querySelector('#aiReviewDialog').open", timeout=12000)
        assert page.locator('#aiReviewList input[type="checkbox"]:checked').count() >= 1
        page.locator("#aiReviewMerge").evaluate("(button) => button.click()")
        page.wait_for_function("!document.querySelector('#aiReviewDialog').open")

        merged = priv.parse_html(priv.downloaded(page, "#saveBtn"))
        merged_nodes, merged_links = scene_items(merged)
        assert merged_nodes[target_id]["text"] == old_text + SUFFIX
        assert merged_nodes[NEW_ID]["text"] == "Added via AI data handback"
        assert NEW_LINK in merged_links and merged_links[NEW_LINK]["to"] == NEW_ID
        assert merged_nodes[priv.NOTE_ID] == before_nodes[priv.NOTE_ID]
        assert merged_links[priv.LINK_ID] == before_links[priv.LINK_ID]
        assert merged_links[priv.ORPHAN_ID] == before_links[priv.ORPHAN_ID]

        page.locator("#undoBtn").evaluate("(button) => button.click()")
        undone_nodes, undone_links = scene_items(priv.parse_html(priv.downloaded(page, "#saveBtn")))
        assert undone_nodes[target_id] == before_nodes[target_id]
        assert NEW_ID not in undone_nodes and NEW_LINK not in undone_links
        assert undone_nodes[priv.NOTE_ID] == before_nodes[priv.NOTE_ID]
        assert undone_links[priv.LINK_ID] == before_links[priv.LINK_ID]

        page.locator("#redoBtn").evaluate("(button) => button.click()")
        redone_nodes, redone_links = scene_items(priv.parse_html(priv.downloaded(page, "#saveBtn")))
        assert redone_nodes[target_id] == merged_nodes[target_id]
        assert redone_nodes[NEW_ID] == merged_nodes[NEW_ID]
        assert redone_links[NEW_LINK] == merged_links[NEW_LINK]
        assert redone_nodes[priv.NOTE_ID] == before_nodes[priv.NOTE_ID]
        assert redone_links[priv.LINK_ID] == before_links[priv.LINK_ID]
        assert not errors, (name, width, "browser errors", errors)
        print("PASS", name, width, "public AI JSON -> selective merge, private preserved, Undo/Redo")
    finally:
        page.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", default=None)
    parser.add_argument("--chromium", default=None)
    parser.add_argument("--source-root", type=Path, required=True)
    args = parser.parse_args()
    options = {"headless": True, "args": ["--no-sandbox"]}
    if args.channel:
        options["channel"] = args.channel
    if args.chromium:
        options["executable_path"] = args.chromium
    with sync_playwright() as play:
        browser = play.chromium.launch(**options)
        try:
            for name in ("MetaCanvas_Studio21_Consulenza_IT.html", "MetaCanvas_Studio21_Consulenza_EN.html"):
                html, model = priv.fixture((args.source_root / name).read_text(encoding="utf-8"))
                for width in (1440, 390):
                    run(browser, name, width, html)
        finally:
            browser.close()


if __name__ == "__main__":
    main()
