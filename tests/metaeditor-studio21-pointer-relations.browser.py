#!/usr/bin/env python3
"""Exercise actual pointer dragging of composed Studio21 sections on original and candidate HTML.

Unlike the keyboard regression, this sends browser mouse/pointer events through
the native controller and compares the downloaded ccm.document.v1 work model.
It does not claim touch-screen, Windows file:// or arbitrary-import coverage.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
REL_PATH = Path(__file__).with_name("metaeditor-studio21-relations.browser.py")
spec = importlib.util.spec_from_file_location("studio21_relations", REL_PATH)
assert spec and spec.loader
rel = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rel)

THIRD = "regression-card-two"
INSIDE_LINK = "regression-inner-link"


def fixture_html(original: str) -> str:
    html, model = rel.fixture_html(original)
    scene = model["scenes"][0]
    scene["elements"].append({
        "id": THIRD, "type": "card", "x": 680, "y": 345,
        "w": 75, "h": 65, "containerId": rel.SEC,
        "text": "Second card", "fontSize": 17,
        "color": "#183146", "fill": "#e7f5f0", "align": "center"
    })
    scene["links"].append({
        "id": INSIDE_LINK, "from": THIRD, "to": rel.IMAGE,
        "label": "internal relation", "width": 2,
        "color": "#087b70", "fromAnchor": "bottom",
        "toAnchor": "top", "arrow": True
    })
    match = rel.MODEL.search(html)
    assert match
    encoded = json.dumps(model, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    return html[:match.start(2)] + encoded + html[match.end(2):]


def geometry(model):
    return rel.elements(model)


def observe(browser, name: str, width: int, html: str):
    page = browser.new_page(viewport={"width": width, "height": 844}, accept_downloads=True)
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.route("**/*", lambda route: route.abort())
    page.route("https://studio21.invalid/standalone", lambda route: route.fulfill(
        status=200, headers={"content-type": "text/html; charset=utf-8"}, body=html
    ))
    try:
        page.goto("https://studio21.invalid/standalone", wait_until="domcontentloaded")
        section = page.locator(f'#canvas .node[data-id="{rel.SEC}"]')
        section.wait_for(state="visible", timeout=15000)
        for key in (rel.CHILD, rel.IMAGE, THIRD):
            page.locator(f'#canvas .node[data-id="{key}"]').wait_for(state="attached")
        initial = rel.download_model(page)
        before, links_before = geometry(initial)
        assert all(before[key]["containerId"] == rel.SEC for key in (rel.CHILD, rel.IMAGE, THIRD))
        assert links_before[rel.LINK]["from"] == rel.CHILD
        assert links_before[INSIDE_LINK]["from"] == THIRD
        routes_before = page.locator("#canvas .edge-visible").evaluate_all(
            "(nodes) => nodes.map(n => n.getAttribute('d'))"
        )

        section.scroll_into_view_if_needed()
        box = section.bounding_box()
        assert box and box["width"] > 0 and box["height"] > 0, (name, width, "no section box")
        # Sample a genuinely reachable part of the section: child/link overlays
        # can be above its rectangle, especially in the narrow viewport.
        hit = page.evaluate("""(id) => {
            const section = document.querySelector('#canvas .node[data-id="' + id + '"]');
            const r = section.getBoundingClientRect();
            const misses = [];
            for (const fy of [.12, .28, .48, .72, .9]) {
                for (const fx of [.42, .17, .8, .6, .05, .95]) {
                    const x = r.x + r.width * fx, y = r.y + r.height * fy;
                    if (x < 1 || y < 1 || x >= innerWidth - 1 || y >= innerHeight - 1) continue;
                    const element = document.elementFromPoint(x, y);
                    const node = element?.closest('.node')?.dataset.id || null;
                    if (node === id) return {ok: true, x, y, node, tag:element.tagName};
                    misses.push({fx, fy, node, tag:element?.tagName || null});
                }
            }
            return {ok: false, rect:{x:r.x,y:r.y,w:r.width,h:r.height}, misses};
        }""", rel.SEC)
        assert hit["ok"], (name, width, "section has no reachable pointer target", hit)
        start_x, start_y = hit["x"], hit["y"]
        page.evaluate("""() => {
            window.__dragProbe = [];
            for (const type of ['pointerdown','pointermove','pointerup']) {
                document.addEventListener(type, e => {
                    if(window.__dragProbe.length < 60) {
                        window.__dragProbe.push({type, node:e.target.closest('.node')?.dataset.id || null,
                           buttons:e.buttons, x:e.clientX, y:e.clientY});
                    }
                }, true);
            }
        }""")
        page.mouse.move(start_x, start_y)
        page.mouse.down()
        page.mouse.move(start_x + 36, start_y + 22, steps=14)
        page.mouse.up()

        after = rel.download_model(page)
        moved, links_after = geometry(after)
        dx = moved[rel.SEC]["x"] - before[rel.SEC]["x"]
        dy = moved[rel.SEC]["y"] - before[rel.SEC]["y"]
        assert (dx or dy), (name, width, "pointer drag did not move section", hit, page.evaluate("window.__dragProbe"))
        for key in (rel.CHILD, rel.IMAGE, THIRD):
            assert moved[key]["x"] - before[key]["x"] == dx, (name, width, key, "x displacement")
            assert moved[key]["y"] - before[key]["y"] == dy, (name, width, key, "y displacement")
            assert moved[key]["containerId"] == rel.SEC, (name, width, key, "lost container")
        assert moved[rel.IMAGE]["src"] == rel.PNG
        assert moved["d1-c"] == before["d1-c"], (name, width, "unrelated node moved")
        assert links_after == links_before, (name, width, "link identity/anchors changed")
        routes_after = page.locator("#canvas .edge-visible").evaluate_all(
            "(nodes) => nodes.map(n => n.getAttribute('d'))"
        )
        assert routes_after != routes_before, (name, width, "rendered link paths did not change")

        page.locator("#undoBtn").evaluate("(button) => button.click()")
        undone, undone_links = geometry(rel.download_model(page))
        for key in (rel.SEC, rel.CHILD, rel.IMAGE, THIRD):
            assert undone[key] == before[key], (name, width, key, "Undo drift")
        assert undone_links == links_before, (name, width, "Undo link drift")
        page.locator("#redoBtn").evaluate("(button) => button.click()")
        redone, redone_links = geometry(rel.download_model(page))
        for key in (rel.SEC, rel.CHILD, rel.IMAGE, THIRD):
            assert redone[key] == moved[key], (name, width, key, "Redo drift")
        assert redone_links == links_before, (name, width, "Redo link drift")
        assert not errors, (name, width, "page errors", errors)
        print("PASS", name, width, "pointer section+3 children+2 links; work export; Undo/Redo")
    finally:
        page.close()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--channel", default=None)
    p.add_argument("--chromium", default=None)
    p.add_argument("--candidate-root", type=Path, default=None)
    args = p.parse_args()
    source_root = args.candidate_root or (ROOT / "examples/collaborative-communication-medium")
    options = {"headless": True, "args": ["--no-sandbox"]}
    if args.channel:
        options["channel"] = args.channel
    if args.chromium:
        options["executable_path"] = args.chromium
    with sync_playwright() as play:
        browser = play.chromium.launch(**options)
        try:
            for name in ("MetaCanvas_Studio21_Consulenza_IT.html", "MetaCanvas_Studio21_Consulenza_EN.html"):
                html = fixture_html((source_root / name).read_text(encoding="utf-8"))
                for width in (1440, 390):
                    observe(browser, name, width, html)
        finally:
            browser.close()


if __name__ == "__main__":
    main()
