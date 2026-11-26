#!/usr/bin/env python3
"""Mixed card composition: authored links/images and immutable protected islands.

Demonstrates bounded edits without treating a semantic section, CSS card, an
original media figure or an inert/read-only component as interchangeable.
Only synthetic fixture data; no production site updates or arbitrary HTML.
"""
from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_metaeditor_neutral_workpage import build, LAB, MODULES
from importlib.machinery import SourceFileLoader

MEDIA_TEST = SourceFileLoader(
    "metaeditor_media_test", str(ROOT / "tests/metaeditor-neutral-media-links.browser.py")
).load_module()
FIXTURE = ROOT / "tests/fixtures/metaeditor/mixed_protected_composition.html"


def choose_anchor(page, part: str):
    picker = page.locator("#me-neutral-anchor")
    choices = picker.locator("option").all_text_contents()
    hits = [i for i, label in enumerate(choices) if part in label]
    assert len(hits) == 1, (part, choices)
    picker.select_option(index=hits[0])


def original_islands(page):
    return page.evaluate("""() => ({
        locked: document.querySelector('#locked-card').outerHTML,
        widget: document.querySelector('#protected-widget').outerHTML,
        media: document.querySelector('#author-figure').outerHTML,
        inert: document.querySelector('#locked-card-d').outerHTML,
        href: document.querySelector('#original-link').getAttribute('href'),
        target: document.querySelector('#target-content').id,
        parentIds: ['locked-card','editable-card','editable-card-c','locked-card-d']
            .map(id => document.getElementById(id).parentElement.className)
    })""")


def run(browser, tmp: Path, width: int):
    original = FIXTURE.read_text(encoding="utf-8")
    modules = [(LAB / name).read_text(encoding="utf-8") for name in MODULES]
    workfile = tmp / f"mixed-{width}.html"
    workfile.write_text(build(original, *modules), encoding="utf-8")
    page = browser.new_page(viewport={"width":width,"height":850}, accept_downloads=True)
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    try:
        page.goto(workfile.as_uri())
        try:
            page.wait_for_function("() => !!window.metaEditorPage", timeout=6000)
        except Exception as exc:
            raise AssertionError({
                "startup":str(exc), "width":width, "pageerrors":errors,
                "scripts":page.locator("script").count(),
                "mount":page.evaluate("""() => ({
                    adapter:!!window.MetaEditorStaticPageAdapter,
                    controller:!!window.MetaEditorNeutralStaticPage,
                    mounted:!!window.metaEditorPage,
                    state:document.readyState,
                    hasMain:!!document.querySelector('main')
                })"""),
                "tail":page.content()[-600:]
            }) from exc
        assert page.evaluate("() => window.metaEditorPage.cleanHtml()") == original
        # Authored read-only islands are allowed, but imported active
        # contentEditable must still fail at the source adapter boundary.
        active_source = page.evaluate("""() => {
            const source = JSON.parse(document.querySelector(
                '#me-neutral-original-source').textContent).source;
            const active = source.replace('contenteditable="false"',
                                           'contenteditable="true"');
            try {
                window.MetaEditorStaticPageAdapter.create({
                    sourceHtml:active, regionElement:document.querySelector('main')
                });
                return 'unexpectedly-accepted';
            } catch (err) { return String(err.message); }
        }""")
        assert "editor-reserved attributes: contenteditable" in active_source, active_source
        baseline = original_islands(page)
        assert page.locator("main .card").count() == 4
        for selector in ("#locked-card h2", "#locked-asset-link",
                         "#protected-widget p", "#author-figure figcaption",
                         "#locked-card-d h2"):
            assert page.evaluate("""(selector) => window.metaEditorPage.select(
                document.querySelector(selector))""", selector) is False, (
                    width, "protected original was selectable", selector
                )
        assert page.evaluate("() => window.metaEditorPage.edit()")["ok"] is False
        assert page.evaluate("() => window.metaEditorPage.cleanHtml()") == original
        assert page.evaluate("() => window.metaEditorPage.status().canUndo") is False

        anchors = page.locator("#me-neutral-anchor option").all_text_contents()
        assert not any("protetto" in x.lower() or "widget" in x.lower() for x in anchors), anchors
        page.locator("#me-neutral-section").select_option("1")
        anchors = page.locator("#me-neutral-anchor option").all_text_contents()
        assert not any("inerte" in x.lower() for x in anchors), anchors

        # Choose the editable card B, not the protected card A. The first
        # added paragraph starts next to authored content, inside card B.
        page.locator("#editable-card h2").click()
        inserted = page.evaluate("() => window.metaEditorPage.insert('p')")
        assert inserted["changed"], inserted
        card_b = page.locator("#editable-card")
        blocks = card_b.locator("p[data-local-block]")
        assert blocks.count() == 1
        assert blocks.first.evaluate("(n) => n.previousElementSibling.tagName") == "H2"
        assert abs(blocks.first.bounding_box()["x"] - card_b.locator("h2").bounding_box()["x"]) <= 8

        # Up/down must not jump over authored text, original images,
        # link-bearing paragraphs or protected widgets. No history effect.
        before = page.evaluate("() => window.metaEditorPage.cleanHtml()")
        down = page.evaluate("() => window.metaEditorPage.move('down')")
        up = page.evaluate("() => window.metaEditorPage.move('up')")
        assert not down["changed"] and not up["changed"], (width, down, up)
        assert page.evaluate("() => window.metaEditorPage.cleanHtml()") == before

        # An explicit author-reference may reposition our block beyond a
        # protected widget, without moving/changing the widget itself.
        page.locator("#me-neutral-position-group").evaluate("(n)=>n.open=true")
        choose_anchor(page, "Testo finale")
        page.locator("#me-neutral-placement").select_option("after")
        moved = page.evaluate("() => window.metaEditorPage.move('transfer')")
        assert moved["changed"], moved
        assert card_b.locator("#target-content").evaluate(
            "(n) => n.nextElementSibling.matches('p[data-local-block]')")
        assert original_islands(page) == baseline

        # Add a second paragraph after the first, then reorder only the two
        # adjacent editor-owned blocks; original composition stays intact.
        added = card_b.locator("p[data-local-block]")
        added.click()
        page.locator("#me-neutral-anchor").select_option("")
        second = page.evaluate("() => window.metaEditorPage.insert('p')")
        assert second["changed"], second
        assert card_b.locator("p[data-local-block]").count() == 2
        ids_before = card_b.locator("p[data-local-block]").evaluate_all(
            "(nodes) => nodes.map(n=>n.getAttribute('data-local-block-id'))")
        assert len(set(ids_before)) == 2 and all(ids_before), ids_before
        up = page.evaluate("() => window.metaEditorPage.move('up')")
        assert up["changed"], (up, ids_before)
        ids_after = card_b.locator("p[data-local-block]").evaluate_all(
            "(nodes) => nodes.map(n=>n.getAttribute('data-local-block-id'))")
        assert ids_after == list(reversed(ids_before)), (ids_before,ids_after)
        assert card_b.locator("p[data-local-block]").count() == 2
        assert original_islands(page) == baseline

        # New links are independent owned paragraphs. The original link and
        # fragment destination are retained exactly.
        page.locator("#editable-card h2").click()
        page.locator("#me-neutral-link-group").evaluate("(n)=>n.open=true")
        page.locator("#me-neutral-link-text").fill("Link aggiunto")
        page.locator("#me-neutral-link-url").fill("https://example.org/new")
        created = page.evaluate("() => window.metaEditorPage.linkAction()")
        assert created["changed"], created
        assert card_b.locator('p[data-local-block] a[href="https://example.org/new"]').count() == 1

        # Insert PNG from an actual file input; the original protected and
        # linked image are never replaced, re-encoded or moved.
        page.locator("#editable-card h2").click()
        page.locator("#me-neutral-image-group").evaluate("(n)=>n.open=true")
        page.locator("#me-neutral-image-alt").fill("Grafico incorporato nel lavoro")
        file_input = page.locator("#me-neutral-image-file")
        file_input.set_input_files({
            "name":"diagram.png","mimeType":"image/png",
            "buffer": MEDIA_TEST.sample_png()
        })
        figure = card_b.locator("figure[data-local-block]")
        figure.wait_for(state="attached", timeout=10000)
        assert figure.locator("img").get_attribute("src").startswith("data:image/png;base64,")
        assert figure.locator("img").get_attribute("alt") == "Grafico incorporato nel lavoro"
        assert original_islands(page) == baseline

        # Transfer only the new figure to card C (another section). Existing
        # card media, linked fragments, relative orders remain unchanged.
        figure.click()
        assert figure.get_attribute("data-local-selected") == "true", (
            width,"figure caption click selected a child rather than the media component")
        page.locator("#me-neutral-section").select_option("1")
        choose_anchor(page, "Area compositiva C")
        page.locator("#me-neutral-placement").select_option("after")
        moved = page.evaluate("() => window.metaEditorPage.move('transfer')")
        assert moved["changed"], moved
        card_c = page.locator("#editable-card-c")
        assert card_c.locator("figure[data-local-block]").count() == 1
        assert card_b.locator("figure[data-local-block]").count() == 0
        assert original_islands(page) == baseline

        # Duplicating an owned image must not duplicate its private block ID.
        page.evaluate("""() => window.metaEditorPage.select(
            document.querySelector('#editable-card-c figure[data-local-block]'))""")
        copy = page.evaluate("() => window.metaEditorPage.changeAddedBlock('duplicate')")
        assert copy["changed"], copy
        media_ids = card_c.locator("figure[data-local-block]").evaluate_all(
            "(nodes) => nodes.map(n => n.getAttribute('data-local-block-id'))")
        assert len(media_ids) == 2 and len(set(media_ids)) == 2, (width,media_ids)
        assert original_islands(page) == baseline
        assert page.evaluate("() => window.metaEditorPage.undo()")["changed"]
        assert card_c.locator("figure[data-local-block]").count() == 1

        # The work and clean file each preserve every protected original;
        # added media remains embedded and original navigation still resolves.
        clean = page.evaluate("() => window.metaEditorPage.cleanHtml()")
        working = page.evaluate("() => window.metaEditorPage.workHtml()")
        assert "data-local-block" not in clean
        assert "data-local-block-id" not in clean
        assert "me-neutral-toolbar" not in clean
        assert "data-local-block-id" in working
        assert 'contenteditable="false"' in working
        assert 'contenteditable="false"' in clean
        assert "data:image/png;base64," in clean
        assert clean.count('href="#target-content"') == original.count('href="#target-content"')
        saved = tmp / f"mixed-saved-{width}.html"
        saved.write_text(working, encoding="utf-8")
        reopened = browser.new_page(viewport={"width":width,"height":850})
        try:
            reopened.goto(saved.as_uri())
            reopened.wait_for_function("() => !!window.metaEditorPage")
            assert reopened.evaluate("() => window.metaEditorPage.cleanHtml()") == clean
            assert reopened.locator("#editable-card-c figure[data-local-block]").count() == 1
            assert original_islands(reopened) == baseline
        finally:
            reopened.close()
        cleanfile = tmp / f"mixed-clean-{width}.html"
        cleanfile.write_text(clean, encoding="utf-8")
        exported = browser.new_page(viewport={"width":width,"height":850})
        try:
            exported.goto(cleanfile.as_uri())
            assert exported.locator("#me-neutral-toolbar").count() == 0
            assert exported.locator("#editable-card-c figure img").count() == 1
            assert original_islands(exported) == baseline
        finally:
            exported.close()

        # Undo all mutating steps, including mixed content and transfers.
        for _ in range(24):
            if not page.evaluate("() => window.metaEditorPage.status().canUndo"):
                break
            assert page.evaluate("() => window.metaEditorPage.undo()")["changed"]
        assert page.evaluate("() => window.metaEditorPage.cleanHtml()") == original
        assert page.evaluate("() => window.metaEditorPage.status().dirty") is False
        assert original_islands(page) == baseline
        assert not errors, (width,errors)
        print("PASS", width, "mixed protected originals/link/image, safe placement, history and exports")
    finally:
        page.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel",default=None)
    parser.add_argument("--chromium",default=None)
    args = parser.parse_args()
    options={"headless":True,"args":["--no-sandbox"]}
    if args.channel: options["channel"]=args.channel
    if args.chromium: options["executable_path"]=args.chromium
    with tempfile.TemporaryDirectory(prefix="metaeditor-mixed-") as folder:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(**options)
            try:
                for width in (1440,390):
                    run(browser,Path(folder),width)
            finally:
                browser.close()


if __name__=="__main__":
    main()
