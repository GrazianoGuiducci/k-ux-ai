#!/usr/bin/env python3
"""Test the beginner entry point in real Chrome, including file:// navigation.

Tests all four starter choices, their independent original baselines,
editing, insertion, save/reopen, clean export and the ability to undo back to
exact original source. Only synthetic originals are packaged.
"""
from __future__ import annotations

import argparse
import sys
import tempfile
import zipfile
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_metaeditor_starter_pack import TEMPLATES, ROOT as STARTERS, pack

EXPECTED = {"Articolo", "Da_zero", "Essenziale", "Progetto"}


def exercise(browser, root: Path, width: int) -> None:
    context = browser.new_context(viewport={"width":width, "height":850}, accept_downloads=True)
    chooser = context.new_page()
    page_errors = []
    chooser.on("pageerror", lambda e: page_errors.append(str(e)))
    try:
        chooser.goto((root / "Apri_MetaEditor.html").as_uri())
        assert chooser.locator("h1").inner_text() == "Da dove vuoi iniziare?"
        links = chooser.locator('a[href^="Modelli/"]')
        assert links.count() == 4, ("chooser must have 4 visible starter choices", links.count())
        assert chooser.locator("input,select").count() == 0
        assert chooser.locator('script').count() == 0, "chooser should not execute launcher code"
        assert chooser.locator(".card").count() == 4
        seen = set()
        for item in range(links.count()):
            href = links.nth(item).get_attribute("href")
            name = Path(href).stem
            assert name in EXPECTED and name not in seen
            seen.add(name)
            assert (root / href).is_file(), (width,href,"broken local link")
            before = (root / href).read_bytes()
            with context.expect_page() as popup:
                links.nth(item).click()
            page = popup.value
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            try:
                page.wait_for_function("() => !!window.metaEditorPage")
                assert page.url.startswith("file://"), page.url
                assert page.locator("#me-neutral-toolbar").count() == 1
                assert page.locator("#me-neutral-context").is_visible()
                raw = (STARTERS / "sources" / TEMPLATES[name]).read_text(encoding="utf-8")
                no_op = page.evaluate("() => window.metaEditorPage.cleanHtml()")
                assert no_op == raw, (name,width,"chooser changed original source before editing")
                heading = page.locator("main h1")
                assert heading.count() == 1, (name,width,"missing editable title")
                heading.click()
                page.locator('[data-me-action="edit"]').click()
                heading.fill("Titolo scelto da un modello")
                page.locator('[data-me-action="edit"]').click()
                assert "Titolo scelto da un modello" in page.evaluate("() => window.metaEditorPage.cleanHtml()")
                page.locator('#me-neutral-section').select_option('0')
                page.locator('[data-me-action="insert-p"]').click()
                added = page.locator("main [data-local-block]")
                assert added.count() == 1
                x0 = heading.bounding_box()["x"]
                x1 = added.bounding_box()["x"]
                assert abs(x0 - x1) <= 8, (name,width,"inserted block escaped text column",x0,x1)
                # Test the ACTUAL browser download actions, not only the
                # JavaScript serialization helpers. The downloaded work copy
                # is what a person will reopen on Windows.
                with page.expect_download() as event:
                    page.locator('[data-me-action="work"]').click()
                download_work = event.value
                assert download_work.suggested_filename == "MetaEditor_Lavoro_Modificabile.html"
                work = Path(download_work.path()).read_text(encoding="utf-8")
                with page.expect_download() as event:
                    page.locator('[data-me-action="clean"]').click()
                download_clean = event.value
                assert download_clean.suggested_filename == "MetaEditor_Pagina_Pulita.html"
                clean = Path(download_clean.path()).read_text(encoding="utf-8")
                assert work == page.evaluate("() => window.metaEditorPage.workHtml()")
                assert clean == page.evaluate("() => window.metaEditorPage.cleanHtml()")
                assert "Nuovo paragrafo" in clean
                assert "data-local-block" not in clean
                assert "me-neutral-toolbar" not in clean
                assert "data-local-block" in work
                assert "me-neutral-original-source" in work
                assert (root / href).read_bytes() == before, (name,width,"template file was mutated")

                # The saved work file must reopen from disk, with editing and
                # clean-export fidelity intact; no network or server.
                saved = root / ("Riaperto_" + name + "_" + str(width) + ".html")
                saved.write_text(work, encoding="utf-8")
                reopened = context.new_page()
                try:
                    reopened.goto(saved.as_uri())
                    reopened.wait_for_function("() => !!window.metaEditorPage")
                    assert reopened.locator("#me-neutral-toolbar").count() == 1
                    assert reopened.evaluate("() => window.metaEditorPage.cleanHtml()") == clean
                    assert reopened.locator("main [data-local-block]").count() == 1
                finally:
                    reopened.close()
                for _ in range(4):
                    if not page.evaluate("() => window.metaEditorPage.status().canUndo"):
                        break
                    page.evaluate("() => window.metaEditorPage.undo()")
                assert page.evaluate("() => window.metaEditorPage.cleanHtml()") == raw, (
                    name,width,"full undo changed original document"
                )
                assert not errors, (name,width,errors)
                print("PASS",width,name,"file:// chooser->work, insert, reopen, Undo, original unchanged")
            finally:
                page.close()
        assert seen == EXPECTED
        assert not page_errors, page_errors
    finally:
        context.close()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--channel",default=None)
    p.add_argument("--chromium",default=None)
    args = p.parse_args()
    opts={"headless":True,"args":["--no-sandbox"]}
    if args.channel: opts["channel"]=args.channel
    if args.chromium: opts["executable_path"]=args.chromium
    with tempfile.TemporaryDirectory(prefix="metaeditor-chooser-test-") as folder:
        root = Path(folder)
        archive_path = root / "MetaEditor_Scegli_Modello.zip"
        pack(archive_path)
        with zipfile.ZipFile(archive_path) as archive:
            names = set(archive.namelist())
            expected = {"Apri_MetaEditor.html","LEGGIMI.txt"} | {
                "Modelli/" + name + ".html" for name in EXPECTED
            }
            assert names == expected, names
            archive.extractall(root / "opened")
        with sync_playwright() as play:
            browser = play.chromium.launch(**opts)
            try:
                for width in (1440,390):
                    exercise(browser, root / "opened", width)
            finally:
                browser.close()


if __name__ == "__main__":
    main()
