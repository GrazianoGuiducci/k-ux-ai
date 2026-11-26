#!/usr/bin/env python3
"""Boundary regression for public HTML, default AI data and personal templates.

Synthetic private link has PUBLIC endpoints: endpoint-only filtering must not
mistake it for shareable content. Baseline mode characterizes the known source;
candidate mode requires private link exclusion. An invalid remote image import
must be rejected in both. No user data or remote service is used.
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
MODULE = Path(__file__).with_name("metaeditor-studio21-relations.browser.py")
spec = importlib.util.spec_from_file_location("studio21_privacy_fixture", MODULE)
assert spec and spec.loader
rel = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rel)

NOTE_ID = "privacy-test-private-note"
LINK_ID = "privacy-test-link-between-public-nodes"
ORPHAN_ID = "privacy-test-link-to-private-note"
NOTE_MARKER = "SYNTHETIC_PRIVATE_NOTE_20261122"
LINK_MARKER = "SYNTHETIC_PRIVATE_EDGE_20261122"


def fixture(original: str):
    match = rel.MODEL.search(original)
    assert match
    model = json.loads(match.group(2))
    scene = model["scenes"][0]
    public_nodes = [n for n in scene["elements"] if n["type"] not in ("note",)]
    assert len(public_nodes) >= 2
    scene["notes"] = NOTE_MARKER
    scene["elements"].append({
        "id": NOTE_ID, "type": "note", "private": True,
        "x": 800, "y": 510, "w": 150, "h": 65,
        "text": NOTE_MARKER, "fontSize": 17
    })
    scene["links"].extend([
        {"id": LINK_ID, "private": True, "from": public_nodes[0]["id"],
         "to": public_nodes[1]["id"], "label": LINK_MARKER,
         "width": 2, "color": "#087b70"},
        {"id": ORPHAN_ID, "from": NOTE_ID, "to": public_nodes[0]["id"],
         "label": "private endpoint", "width": 2, "color": "#087b70"}
    ])
    encoded = json.dumps(model, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    return original[:match.start(2)] + encoded + original[match.end(2):], model


def downloaded(page, selector):
    with page.expect_download(timeout=25000) as event:
        page.locator(selector).evaluate("(button) => button.click()")
    return Path(event.value.path()).read_text(encoding="utf-8")


def parse_html(html):
    match = rel.MODEL.search(html)
    assert match, "missing ccm-data in downloaded HTML"
    return json.loads(match.group(2))


def examine(model, expect_leak: bool, kind: str):
    scene = model["scenes"][0]
    elements = {n["id"]: n for n in scene["elements"]}
    links = {l["id"]: l for l in scene["links"]}
    assert scene.get("notes", "") == "", (kind, "private notes survived")
    assert NOTE_ID not in elements, (kind, "private node survived")
    assert ORPHAN_ID not in links, (kind, "link to private node survived")
    assert (LINK_ID in links) == expect_leak, (kind, "private edge filtering differs", list(links))
    assert model.get("library", []) == [], (kind, "library not cleared")
    assert model.get("savedTemplates", []) == [], (kind, "personal templates not cleared")


def inspect(browser, name, width, html: str, model: dict, expect_leak: bool):
    page = browser.new_page(viewport={"width": width, "height": 844}, accept_downloads=True)
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on("dialog", lambda dialog: dialog.accept("Synthetic regression template") if dialog.type == "prompt" else dialog.accept())
    page.route("**/*", lambda route: route.abort())
    page.route("https://studio21.invalid/standalone", lambda route: route.fulfill(
        status=200, headers={"content-type": "text/html; charset=utf-8"}, body=html
    ))
    try:
        page.goto("https://studio21.invalid/standalone", wait_until="domcontentloaded")
        page.locator("#saveBtn").wait_for(state="attached", timeout=15000)
        work = parse_html(downloaded(page, "#saveBtn"))
        work_scene = work["scenes"][0]
        # The loader may migrate scene.notes into a private note element.
        assert (work_scene.get("notes") == NOTE_MARKER or any(
            n.get("text") == NOTE_MARKER and n.get("private") is True
            for n in work_scene["elements"]
        )), "private work note was not preserved"
        assert any(n["id"] == NOTE_ID for n in work_scene["elements"])
        assert any(l["id"] == LINK_ID and l.get("private") is True for l in work_scene["links"])

        public_html = downloaded(page, "#publicBtn")
        public = parse_html(public_html)
        examine(public, expect_leak, "public HTML")
        assert public.get("ui", {}).get("publicCopy") is True
        assert (LINK_MARKER in public_html) == expect_leak
        assert NOTE_MARKER not in public_html

        page.locator("#exportData").evaluate("(button) => button.click()")
        page.locator("#aiShareDialog").wait_for(state="visible")
        assert not page.locator("#aiSharePrivate").is_checked()
        ai = json.loads(downloaded(page, "#aiShareConfirm"))
        examine(ai, expect_leak, "AI JSON")

        page.locator("#saveSceneTemplate").evaluate("(button) => button.click()")
        pack = json.loads(downloaded(page, "#exportTemplates"))
        assert pack["schema"] == "metacanvas.templates.v1"
        assert len(pack["templates"]) >= 1
        template = pack["templates"][-1]["scene"]
        assert template["notes"] == ""
        assert NOTE_ID not in {n["id"] for n in template["elements"]}
        assert ORPHAN_ID not in {l["id"] for l in template["links"]}
        assert (LINK_ID in {l["id"] for l in template["links"]}) == expect_leak

        invalid = copy.deepcopy(model)
        invalid["scenes"][0]["elements"].append({
            "id": "privacy-remote-image", "type": "image",
            "x": 100, "y": 100, "w": 130, "h": 80,
            "src": "https://invalid.example/private.png", "text": "remote"
        })
        payload = json.dumps(invalid).encode("utf-8")
        page.locator("#importDataFile").set_input_files({
            "name": "invalid-remote-image.json", "mimeType": "application/json", "buffer": payload
        })
        page.wait_for_function("document.querySelector('#toast').textContent.includes('Immagine')", timeout=10000)
        assert not page.locator("#aiReviewDialog").evaluate("(d) => d.open")
        assert not errors, (name, width, "browser errors", errors)
        print("PASS", name, width, "privacy projection", "baseline-leak" if expect_leak else "private-excluded",
              "work/public/AI/template and remote-image rejection")
    finally:
        page.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", default=None)
    parser.add_argument("--chromium", default=None)
    parser.add_argument("--source-root", type=Path, default=ROOT / "examples/collaborative-communication-medium")
    parser.add_argument("--expect-private-link-leak", action="store_true",
                        help="Characterize the original unpatched source only")
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
                html, model = fixture((args.source_root / name).read_text(encoding="utf-8"))
                for width in (1440, 390):
                    inspect(browser, name, width, html, model, args.expect_private_link_leak)
        finally:
            browser.close()


if __name__ == "__main__":
    main()
