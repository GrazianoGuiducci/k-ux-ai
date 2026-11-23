#!/usr/bin/env python3
"""R1 Studio21 direct visual actions, not an isolated HTML toolbar.

Exercises the REAL native node selection, direct text edit, mini editor,
properties, duplicate/Undo/Redo, save/reopen and public export. The candidate
is derived from source-pinned original Studio21 IT/EN, with privacy fixes.
Runs Chrome desktop and narrow viewport; human usability remains separate.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
RELATED=Path(__file__).with_name("metaeditor-studio21-relations.browser.py")
spec=importlib.util.spec_from_file_location("studio21_visual_rel",RELATED)
assert spec and spec.loader
rel=importlib.util.module_from_spec(spec)
spec.loader.exec_module(rel)


def model_from(html: str) -> dict:
    m=rel.MODEL.search(html)
    assert m, "document model missing from exported work"
    return json.loads(m.group(2))


def download(page, selector: str) -> str:
    with page.expect_download(timeout=25000) as event:
        page.locator(selector).evaluate("(button)=>button.click()")
    return Path(event.value.path()).read_text(encoding="utf-8")


def select(page, node_id="d1-h"):
    # Studio21 intentionally treats two clicks within 570 ms as a
    # double-click opening its full editor. Each test selection is a fresh
    # SINGLE click, not an accidental double-click in a fast CI runner.
    page.wait_for_timeout(650)
    node=page.locator('#canvas .node[data-id="'+node_id+'"]')
    node.wait_for(state="visible",timeout=15000)
    node.click(position={"x":15,"y":15},force=True)
    bar=page.locator("#me-visual-actions")
    bar.wait_for(state="visible",timeout=8000)
    assert bar.get_attribute("data-selected-id")==node_id
    rect=bar.bounding_box()
    assert rect and rect["x"]>=0 and rect["y"]>=0,rect
    assert rect["x"]+rect["width"]<=page.viewport_size["width"]+1,rect
    return bar


def exercise(browser, name, width, html):
    page=browser.new_page(viewport={"width":width,"height":850},accept_downloads=True)
    errors=[]
    page.on("pageerror",lambda error:errors.append(str(error)))
    page.on("dialog",lambda d:d.accept())
    page.route("**/*",lambda route:route.abort())
    page.route("https://studio21.invalid/visual-r1",lambda route:route.fulfill(
        status=200,headers={"content-type":"text/html; charset=utf-8"},body=html))
    try:
        page.goto("https://studio21.invalid/visual-r1",wait_until="domcontentloaded")
        page.locator("#canvas .node[data-id='d1-h']").wait_for(state="visible",timeout=15000)
        assert page.locator("#me-visual-actions").count()==0 or page.locator("#me-visual-actions").is_hidden()
        bar=select(page)
        en=name.endswith("_EN.html")
        label=bar.locator('[data-visual-action="text"]').inner_text()
        assert label==("Edit text" if en else "Modifica testo"),label
        assert bar.locator("button").count()==4
        assert page.locator("#quickEditor").is_hidden(), "selection unexpectedly opened full editor"

        # Single selected object -> DIRECT editing in the canvas, not a
        # separate modal or disconnected dropdown.
        bar.locator('[data-visual-action="text"]').click()
        text=page.locator("#canvas .node[data-id='d1-h'] .node-text")
        assert text.get_attribute("contenteditable")=="true"
        assert bar.is_hidden()
        text.fill("Titolo verificato dal gesto diretto")
        # Let blur finalize native history instead of modifying JSON directly.
        page.locator("#docTitle").click()
        edited=model_from(download(page,"#saveBtn"))
        assert any(n["id"]=="d1-h" and n["text"]=="Titolo verificato dal gesto diretto"
                   for n in edited["scenes"][0]["elements"])

        # Undo the actual native edit, redo it, preserving the document model.
        page.locator("#undoBtn").evaluate("(b)=>b.click()")
        undone=model_from(download(page,"#saveBtn"))
        assert any(n["id"]=="d1-h" and n["text"]!="Titolo verificato dal gesto diretto"
                   for n in undone["scenes"][0]["elements"])
        page.locator("#redoBtn").evaluate("(b)=>b.click()")
        restored=model_from(download(page,"#saveBtn"))
        assert any(n["id"]=="d1-h" and n["text"]=="Titolo verificato dal gesto diretto"
                   for n in restored["scenes"][0]["elements"])

        # Native mini editor for styles is reachable by ONE selection and
        # ONE action, instead of opening multiple tools and property panels.
        bar=select(page)
        bar.locator('[data-visual-action="style"]').click()
        assert page.locator("#quickEditor").is_visible()
        assert bar.is_hidden()
        page.locator('#quickEditor [aria-label="Chiudi la modalità di modifica"]').click()
        bar=select(page)
        bar.locator('[data-visual-action="size"]').click()
        assert page.locator("#propertyPanel").evaluate(
            "(el)=>el.classList.contains('drawer-open')")
        assert bar.is_hidden()
        page.locator("#closeProperties").evaluate("(b)=>b.click()")

        # Duplication reuses native selectedId and state history. It must not
        # create a parallel hidden scene or lose the original object identity.
        bar=select(page)
        baseline=len(model_from(download(page,"#saveBtn"))["scenes"][0]["elements"])
        bar.locator('[data-visual-action="copy"]').click()
        duplicated=model_from(download(page,"#saveBtn"))
        elems=duplicated["scenes"][0]["elements"]
        assert len(elems)==baseline+1,(name,width,len(elems),baseline)
        assert sum(n["text"]=="Titolo verificato dal gesto diretto" for n in elems)>=2
        ids=[n["id"] for n in elems]
        assert len(ids)==len(set(ids))
        page.locator("#undoBtn").evaluate("(b)=>b.click()")
        assert len(model_from(download(page,"#saveBtn"))["scenes"][0]["elements"])==baseline
        page.locator("#redoBtn").evaluate("(b)=>b.click()")
        assert len(model_from(download(page,"#saveBtn"))["scenes"][0]["elements"])==baseline+1

        # Deselect through original canvas background (not only helper API).
        page.locator("#canvas").evaluate("""canvas => {
          canvas.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}))
        }""")
        assert page.locator("#me-visual-actions").is_hidden()
        # Public projection must exclude the runtime action bar itself.
        public=download(page,"#publicBtn")
        assert 'id="me-visual-actions"' not in public
        check=browser.new_page(viewport={"width":width,"height":850})
        check.route("**/*",lambda route:route.abort())
        check.route("https://studio21.invalid/public",lambda route:route.fulfill(
            status=200,headers={"content-type":"text/html"},body=public))
        try:
            check.goto("https://studio21.invalid/public",wait_until="domcontentloaded")
            assert check.locator("#me-visual-actions").count()==0
            assert check.locator("#canvas .node").count()>0 or check.locator("#readingView").count()>0
        finally:
            check.close()

        assert not errors,(name,width,"page errors",errors)
        print("PASS",name,width,"visual selection, native edit/style/size/duplicate, Undo/Redo, public export")
    finally:
        page.close()


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-root",type=Path,required=True)
    p.add_argument("--channel",default=None)
    p.add_argument("--chromium",default=None)
    args=p.parse_args()
    options={"headless":True,"args":["--no-sandbox"]}
    if args.channel:options["channel"]=args.channel
    if args.chromium:options["executable_path"]=args.chromium
    with sync_playwright() as pw:
        browser=pw.chromium.launch(**options)
        try:
            for name in ("MetaCanvas_Studio21_Consulenza_IT.html","MetaCanvas_Studio21_Consulenza_EN.html"):
                html=(args.source_root/name).read_text(encoding="utf-8")
                for width in (1440,390):
                    exercise(browser,name,width,html)
        finally:
            browser.close()


if __name__=="__main__":
    main()
