#!/usr/bin/env python3
"""MetaEditor native link and embedded-image work/export regression.

All fixtures are synthetic; source documents remain unchanged. Chromium
opens local file:// work files. Image data is generated here using stdlib PNG.
This does not certify arbitrary image imports, Windows or remote HTML.
"""
from __future__ import annotations

import argparse
import struct
import sys
import tempfile
import zlib
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_metaeditor_neutral_workpage import build, LAB, MODULES

CASES = [
    ROOT / "tests/fixtures/metaeditor/maios_topology_synthetic.html",
    LAB / "starter-templates/sources/articolo.html",
]


def png_chunk(tag, data):
    return struct.pack(">I", len(data)) + tag + data + struct.pack(
        ">I", zlib.crc32(tag + data) & 0xFFFFFFFF
    )


def sample_png():
    pixels = (b"\x00" + b"\x00\x9b\x78" * 2) * 2
    return (b"\x89PNG\r\n\x1a\n" +
            png_chunk(b"IHDR", struct.pack(">IIBBBBB", 2, 2, 8, 2, 0, 0, 0)) +
            png_chunk(b"IDAT", zlib.compress(pixels)) +
            png_chunk(b"IEND", b""))


def run(browser, root, original_path, width):
    original = original_path.read_text(encoding="utf-8")
    module_texts = [(LAB / name).read_text(encoding="utf-8") for name in MODULES]
    work = build(original, *module_texts)
    local = root / f"{original_path.stem}-{width}.html"
    local.write_text(work, encoding="utf-8")
    page = browser.new_page(viewport={"width": width, "height": 840}, accept_downloads=True)
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    try:
        page.goto(local.as_uri())
        page.wait_for_function("() => !!window.metaEditorPage")
        assert page.evaluate("() => window.metaEditorPage.cleanHtml()") == original

        # Never allow forbidden hrefs, even if clicked through the UI.
        group = page.locator("#me-neutral-link-group")
        group.evaluate("(element) => element.open = true")
        page.locator("#me-neutral-link-text").fill("Not allowed")
        initial_links = page.locator("main a").count()
        for forbidden in ("javascript:alert(1)", "data:text/html,hello", "file:///tmp/x", "//bad.example"):
            page.locator("#me-neutral-link-url").fill(forbidden)
            page.locator('[data-me-action="link"]').click()
            assert page.locator("main a").count() == initial_links
            assert page.evaluate("() => window.metaEditorPage.cleanHtml()") == original

        # A new author link is a locally owned paragraph. It must be placed
        # in the content column, with a safe href, never in the toolbar.
        page.locator("main h1").click()
        page.locator("#me-neutral-link-text").fill("Apri il progetto")
        page.locator("#me-neutral-link-url").fill("https://example.org/documentation")
        page.locator('[data-me-action="link"]').click()
        link = page.locator('main p[data-local-block] a')
        assert link.count() == 1
        assert link.get_attribute("href") == "https://example.org/documentation"
        assert link.inner_text() == "Apri il progetto"
        parent = page.locator('main p[data-local-block]')
        assert parent.count() == 1
        left = parent.bounding_box()["x"]
        hleft = page.locator("main h1").bounding_box()["x"]
        assert abs(left - hleft) <= 8, (original_path.stem, width, "link escaped flow column")
        assert page.evaluate("() => window.metaEditorPage.undo()")["changed"]
        assert page.locator('main p[data-local-block] a').count() == 0
        assert page.evaluate("() => window.metaEditorPage.redo()")["changed"]
        assert page.locator('main p[data-local-block] a').count() == 1

        # Existing simple authored links can be changed without affecting
        # their enclosing paragraph or its original siblings.
        author_link = page.locator('main a:not([href="https://example.org/documentation"])').first
        if author_link.count() > 0:
            before_text = author_link.inner_text()
            author_link.click()
            assert page.locator("#me-neutral-link-text").input_value() == before_text
            page.locator("#me-neutral-link-text").fill("Email di prova")
            page.locator("#me-neutral-link-url").fill("mailto:example@example.org")
            page.locator('[data-me-action="link"]').click()
            assert author_link.get_attribute("href") == "mailto:example@example.org"
            assert author_link.inner_text() == "Email di prova"
            assert page.evaluate("() => window.metaEditorPage.undo()")["changed"]
            # Undo replaces nodes, so locate again by preserved original text.
            assert page.locator("main a").filter(has_text=before_text).count() >= 1

        # Reject unsupported local media and missing alt text without
        # modifying the document or creating a history checkpoint.
        original_media_count = page.locator("main figure[data-local-block]").count()
        page.locator("#me-neutral-image-group").evaluate("(e)=>e.open=true")
        file_input = page.locator("#me-neutral-image-file")
        page.locator("#me-neutral-image-alt").fill("")
        file_input.set_input_files({
            "name": "photo.png", "mimeType": "image/png", "buffer": sample_png()
        })
        page.wait_for_timeout(150)
        assert page.locator("main figure[data-local-block]").count() == original_media_count
        page.locator("#me-neutral-image-alt").fill("Logo di prova")
        file_input.set_input_files({
            "name": "unsafe.svg", "mimeType": "image/svg+xml",
            "buffer": b'<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>'
        })
        page.wait_for_timeout(150)
        assert page.locator("main figure[data-local-block]").count() == original_media_count

        # Import a real tiny PNG, fully embedded (not blob/remote URL).
        page.locator("main h1").click()
        file_input.set_input_files({
            "name": "photo.png", "mimeType": "image/png", "buffer": sample_png()
        })
        figure = page.locator('main figure[data-local-block]')
        figure.wait_for(state="attached", timeout=10000)
        assert figure.count() == 1
        img = figure.locator("img")
        assert img.get_attribute("alt") == "Logo di prova"
        assert img.get_attribute("src").startswith("data:image/png;base64,")
        assert figure.locator("figcaption").inner_text() == "Logo di prova"
        assert abs(figure.bounding_box()["x"] - hleft) <= 8
        assert page.evaluate("() => window.metaEditorPage.status().dirty") is True

        clean = page.evaluate("() => window.metaEditorPage.cleanHtml()")
        working = page.evaluate("() => window.metaEditorPage.workHtml()")
        assert "data:image/png;base64," in clean and "Logo di prova" in clean
        assert "data-local-block" not in clean
        assert "data:image/png;base64," in working
        assert "data-local-block" in working
        assert page.evaluate("() => window.metaEditorPage.undo()")["changed"]
        assert page.locator("main figure[data-local-block]").count() == 0
        assert page.evaluate("() => window.metaEditorPage.redo()")["changed"]
        assert page.locator("main figure[data-local-block]").count() == 1

        # The real work file must reopen with the image and managed block
        # ownership still present; clean HTML must open without editor UI.
        work_path = root / f"saved-{original_path.stem}-{width}.html"
        work_path.write_text(working, encoding="utf-8")
        reopened = browser.new_page(viewport={"width":width,"height":840})
        try:
            reopened.goto(work_path.as_uri())
            reopened.wait_for_function("() => !!window.metaEditorPage")
            assert reopened.locator("main figure[data-local-block] img").count() == 1
            assert reopened.evaluate("() => window.metaEditorPage.cleanHtml()") == clean
            assert reopened.evaluate("() => window.metaEditorPage.status().dirty") is False
        finally:
            reopened.close()
        clean_path = root / f"clean-{original_path.stem}-{width}.html"
        clean_path.write_text(clean, encoding="utf-8")
        plain = browser.new_page(viewport={"width":width,"height":840})
        try:
            plain.goto(clean_path.as_uri())
            assert plain.locator("#me-neutral-toolbar").count() == 0
            assert plain.locator("main figure img").count() == 1
            assert plain.locator("main figure img").get_attribute("alt") == "Logo di prova"
        finally:
            plain.close()
        assert not errors, (original_path.stem,width,errors)
        print("PASS",original_path.name,width,"link/reject/undo, local PNG, save/reopen, clean")
    finally:
        page.close()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--channel",default=None)
    parser.add_argument("--chromium",default=None)
    args=parser.parse_args()
    config={"headless":True,"args":["--no-sandbox"]}
    if args.channel:config["channel"]=args.channel
    if args.chromium:config["executable_path"]=args.chromium
    with tempfile.TemporaryDirectory(prefix="metaeditor-media-") as temp:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(**config)
            try:
                for original in CASES:
                    for width in (1440,390):
                        run(browser,Path(temp),original,width)
            finally:
                browser.close()


if __name__=="__main__":
    main()
