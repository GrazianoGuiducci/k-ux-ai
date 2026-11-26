#!/usr/bin/env python3
"""Chrome file:// regressions for bounded contentEditable paste and source fidelity.

This test exercises synthetic clipboard/drop events in Chromium, not every
OS/browser clipboard integration. It checks the actual DOM and both exports.
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

CASES = (
    ("essenziale.html", "main > section"),
    ("articolo.html", "main > article > section"),
)
TEMPLATE_ROOT = LAB / "starter-templates" / "sources"


def fixture(name: str):
    original = (TEMPLATE_ROOT / name).read_text(encoding="utf-8")
    adapter, editor = [(LAB / item).read_text(encoding="utf-8") for item in MODULES]
    return original, build(original, adapter, editor)


def run(browser, root: Path, name: str, width: int):
    source, work = fixture(name)
    file = root / f"{width}-{name}"
    file.write_text(work, encoding="utf-8")
    page = browser.new_page(viewport={"width":width,"height":840}, accept_downloads=True)
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    try:
        page.goto(file.as_uri())
        page.wait_for_function("() => !!window.metaEditorPage")
        assert page.evaluate("() => window.metaEditorPage.cleanHtml()") == source

        # Enter must not produce an invalid div / new heading inside author h1.
        page.evaluate("""() => {
            const h = document.querySelector('main h1');
            window.metaEditorPage.select(h);
            window.metaEditorPage.edit();
            const s = window.getSelection(), r = document.createRange();
            r.selectNodeContents(h);
            r.collapse(false);
            s.removeAllRanges(); s.addRange(r);
        }""")
        page.locator("main h1").press("Enter")
        assert page.locator("main h1 > div,main h1 > p,main h1 > br").count() == 0
        page.evaluate("() => window.metaEditorPage.edit()")
        assert page.evaluate("() => window.metaEditorPage.cleanHtml()") == source

        # Synthetic clipboard with HTML payload and safe text fallback: the
        # editor must consume ONLY text/plain and preserve section structure.
        result = page.evaluate("""() => {
            const p = document.querySelector('main p');
            window.metaEditorPage.select(p);
            window.metaEditorPage.edit();
            const selection = window.getSelection(), range = document.createRange();
            range.selectNodeContents(p);
            selection.removeAllRanges(); selection.addRange(range);
            const data = new DataTransfer();
            data.setData('text/plain', 'Una riga di testo\\nuna seconda riga');
            data.setData('text/html', '<img src=x onerror="window.__unsafe=1"><a href="javascript:alert(1)">unsafe</a>');
            window.__unsafe=0;
            const event = new ClipboardEvent('paste', {
                bubbles:true, cancelable:true, clipboardData:data
            });
            const accepted = p.dispatchEvent(event);
            return {prevented: !accepted && event.defaultPrevented,
                    actual:p.innerHTML, unsafe:window.__unsafe};
        }""")
        assert result["prevented"], (name,width,"paste did not stop native rich HTML",result)
        assert result["unsafe"] == 0
        assert page.locator("main img,main [onerror],main [onclick]").count() == 0
        assert page.locator("main p").first.text_content() == "Una riga di testo una seconda riga", (name,width,result)
        assert page.locator("main p").first.locator("div,br,img,script").count() == 0

        # Neither HTML-only clipboard nor drag/drop may inject content.
        rejected = page.evaluate("""() => {
            const p = document.querySelector('main p'), before = p.innerHTML;
            const html = new DataTransfer();
            html.setData('text/html', '<img src=x onerror="window.__unsafe=2">');
            const paste = new ClipboardEvent('paste',{
                bubbles:true,cancelable:true,clipboardData:html});
            p.dispatchEvent(paste);
            const drag = new DragEvent('drop',{bubbles:true,cancelable:true,
                dataTransfer:html});
            p.dispatchEvent(drag);
            const bypass = new InputEvent('beforeinput',{
                inputType:'insertFromPaste',bubbles:true,cancelable:true,
                data:'<img src=x>'});
            p.dispatchEvent(bypass);
            return {same:before===p.innerHTML, pastePrevented:paste.defaultPrevented,
                dropPrevented:drag.defaultPrevented, bypassPrevented:bypass.defaultPrevented};
        }""")
        assert all(rejected.values()), (name,width,rejected)

        page.evaluate("() => window.metaEditorPage.edit()")  # finish edit, one history checkpoint
        clean = page.evaluate("() => window.metaEditorPage.cleanHtml()")
        assert "Una riga di testo una seconda riga" in clean
        assert "javascript:alert(1)" not in clean
        assert "onerror=" not in clean
        assert "<img" not in clean
        work_saved = page.evaluate("() => window.metaEditorPage.workHtml()")
        assert "Una riga di testo una seconda riga" in work_saved
        assert page.evaluate("() => window.metaEditorPage.undo()")["changed"]
        assert page.evaluate("() => window.metaEditorPage.cleanHtml()") == source
        assert page.evaluate("() => window.metaEditorPage.redo()")["changed"]
        assert page.evaluate("() => window.metaEditorPage.cleanHtml()") == clean

        saved = root / f"saved-{width}-{name}"
        saved.write_text(work_saved, encoding="utf-8")
        new_page = browser.new_page(viewport={"width":width,"height":840})
        try:
            new_page.goto(saved.as_uri())
            new_page.wait_for_function("() => !!window.metaEditorPage")
            assert new_page.evaluate("() => window.metaEditorPage.cleanHtml()") == clean
        finally:
            new_page.close()
        assert not errors, (name,width,errors)
        print("PASS",name,width,"plain-text paste, HTML/drop rejected, heading protected, Undo/Redo/reopen")
    finally:
        page.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel",default=None)
    parser.add_argument("--chromium",default=None)
    args=parser.parse_args()
    options={"headless":True,"args":["--no-sandbox"]}
    if args.channel: options["channel"]=args.channel
    if args.chromium: options["executable_path"]=args.chromium
    with tempfile.TemporaryDirectory(prefix="metaeditor-paste-test-") as tmp:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(**options)
            try:
                for name,_ in CASES:
                    for width in (1440,390):
                        run(browser,Path(tmp),name,width)
            finally:
                browser.close()


if __name__ == "__main__":
    main()
