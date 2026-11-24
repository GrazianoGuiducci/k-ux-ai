#!/usr/bin/env python3
"""Regression of exact composition references in nested card/grid layouts.

A semantic section can contain multiple independent text-flow parents.
This test proves safe refusal of ambiguous automatic destinations, explicit
before/after anchors, same-section reposition and cross-section transfer.
It runs on an entirely synthetic local HTML fixture, at desktop/mobile width.
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_metaeditor_neutral_workpage import build, LAB, MODULES

FIXTURE = ROOT / "tests/fixtures/metaeditor/nested_composition_grid.html"


def choose_anchor(page, label):
    picker = page.locator("#me-neutral-anchor")
    options = picker.locator("option").all_text_contents()
    matched = [i for i, item in enumerate(options) if label in item]
    assert len(matched) == 1, (label, options)
    picker.select_option(index=matched[0])
    assert label in picker.locator("option:checked").inner_text()


def run(browser, tmp, width):
    original = FIXTURE.read_text(encoding="utf-8")
    adapter, controller = [(LAB / name).read_text(encoding="utf-8") for name in MODULES]
    local = tmp / f"complex-{width}.html"
    local.write_text(build(original, adapter, controller), encoding="utf-8")
    page = browser.new_page(viewport={"width":width,"height":850}, accept_downloads=True)
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    try:
        page.goto(local.as_uri())
        page.wait_for_function("() => !!window.metaEditorPage")
        assert page.evaluate("() => window.metaEditorPage.cleanHtml()") == original
        assert page.locator("main .card").count() == 4
        assert page.locator("main .card[data-local-block]").count() == 0
        assert page.locator("#me-neutral-position-group").count() == 1
        assert page.locator("#me-neutral-position-group").is_visible()

        # The second section contains two independent card flows but no
        # labelled section heading. Automatic insertion must reject it, with
        # neither a changed export nor a history entry.
        page.locator("#me-neutral-section").select_option("1")
        before = page.evaluate("() => window.metaEditorPage.cleanHtml()")
        res = page.evaluate("() => window.metaEditorPage.insert('p')")
        assert res["ok"] is False, ("ambiguous destination not rejected", res)
        assert page.evaluate("() => window.metaEditorPage.cleanHtml()") == before
        assert page.evaluate("() => window.metaEditorPage.status().canUndo") is False

        # Explicit source/placement: insert BEFORE the title in card D.
        detail = page.locator("#me-neutral-position-group")
        detail.evaluate("(d) => d.open = true")
        choose_anchor(page, "Scheda D")
        page.locator("#me-neutral-placement").select_option("before")
        res = page.evaluate("() => window.metaEditorPage.insert('p')")
        assert res["changed"], res
        card_d = page.locator("main .card").nth(3)
        inserted = card_d.locator('p[data-local-block]')
        assert inserted.count() == 1, ("wrong card", width)
        assert inserted.evaluate("(n)=>n.nextElementSibling.tagName") == "H2"
        assert abs(inserted.bounding_box()["x"] - card_d.locator("h2").bounding_box()["x"]) <= 8
        assert page.locator("main .card").nth(2).locator('[data-local-block]').count() == 0

        # Index shifts due to insertion do NOT redirect the explicit
        # reference to another node: it remains the card-D heading.
        assert "Scheda D" in page.locator("#me-neutral-anchor option:checked").inner_text()

        # Choose a different card in the SAME section, transfer AFTER C.
        choose_anchor(page, "Scheda C")
        page.locator("#me-neutral-placement").select_option("after")
        moved = page.evaluate("() => window.metaEditorPage.move('transfer')")
        assert moved["changed"], moved
        card_c = page.locator("main .card").nth(2)
        assert card_c.locator('p[data-local-block]').count() == 1
        assert card_d.locator('p[data-local-block]').count() == 0
        assert card_c.locator("h2").evaluate("(n)=>n.nextElementSibling.matches('p[data-local-block]')")

        # Undo restores the exact prior card identity, redo goes back to C.
        assert page.evaluate("() => window.metaEditorPage.undo()")["changed"]
        assert card_d.locator('p[data-local-block]').count() == 1
        assert page.evaluate("() => window.metaEditorPage.redo()")["changed"]
        assert card_c.locator('p[data-local-block]').count() == 1

        # Transfer to the FIRST section's card B, never the top-level shell
        # or the wrong card, using the same destination controls.
        page.evaluate("""() => window.metaEditorPage.select(
            document.querySelectorAll('main .card')[2].querySelector('[data-local-block]'))""")
        page.locator("#me-neutral-section").select_option("0")
        choose_anchor(page, "Scheda B")
        page.locator("#me-neutral-placement").select_option("after")
        moved = page.evaluate("() => window.metaEditorPage.move('transfer')")
        assert moved["changed"], moved
        card_b = page.locator("main .card").nth(1)
        assert card_b.locator('p[data-local-block]').count() == 1
        assert card_b.locator("h2").evaluate("(n)=>n.nextElementSibling.matches('p[data-local-block]')")
        assert card_c.locator('p[data-local-block]').count() == 0
        assert page.locator("main .card").nth(0).locator('[data-local-block]').count() == 0

        # Clean HTML preserves original CSS/head/footer and card structure.
        clean = page.evaluate("() => window.metaEditorPage.cleanHtml()")
        work = page.evaluate("() => window.metaEditorPage.workHtml()")
        assert "<style>" in clean and "Griglia annidata" in clean
        assert "data-local-block" not in clean
        assert "data-local-block" in work
        assert "Nuovo paragrafo" in clean
        clean_path = tmp / f"complex-clean-{width}.html"
        clean_path.write_text(clean, encoding="utf-8")
        public = browser.new_page(viewport={"width":width,"height":850})
        try:
            public.goto(clean_path.as_uri())
            assert public.locator("#me-neutral-toolbar").count() == 0
            assert public.locator("main .card").count() == 4
            assert public.locator("main .card").nth(1).locator("p").count() == 2
        finally:
            public.close()

        # Full Undo removes only our inserted block and restores original
        # source bytes. No direct modification to the four author cards.
        for _ in range(8):
            if not page.evaluate("() => window.metaEditorPage.status().canUndo"):
                break
            assert page.evaluate("() => window.metaEditorPage.undo()")["changed"]
        assert page.evaluate("() => window.metaEditorPage.cleanHtml()") == original
        assert page.evaluate("() => window.metaEditorPage.status().dirty") is False
        assert not errors, errors
        print("PASS", width, "ambiguous refused, explicit card before/after, transfers, export, full Undo")
    finally:
        page.close()


def exercise_reveal(browser,tmp,width):
    # A long but synthetic page makes an offscreen target and available
    # scroll range explicit. No MAIOS content is used.
    original=FIXTURE.read_text(encoding="utf-8").replace(
        "</style>", "header{min-height:1100px} footer{min-height:1000px}</style>",1)
    adapter,controller=[(LAB/name).read_text(encoding="utf-8") for name in MODULES]
    local=tmp/f"reveal-{width}.html"
    local.write_text(build(original,adapter,controller),encoding="utf-8")
    page=browser.new_page(viewport={"width":width,"height":850},accept_downloads=True)
    errors=[]
    page.on("pageerror",lambda e:errors.append(str(e)))
    try:
        page.goto(local.as_uri())
        page.wait_for_function("() => !!window.metaEditorPage")
        page.locator("#me-neutral-section").select_option("1")
        page.locator("#me-neutral-position-group summary").click()
        choose_anchor(page,"Scheda D")
        page.locator("#me-neutral-placement").select_option("after")
        page.evaluate("window.scrollTo(0,0)")
        page.locator('[data-me-action="insert-p"]').click()
        selected=page.locator("main [data-local-selected][data-local-block]")
        assert selected.count()==1
        assert selected.locator("xpath=..").locator("h2").inner_text().startswith("Scheda D")
        geometry=page.evaluate("""() => {
          const r=document.querySelector('main [data-local-selected]').getBoundingClientRect();
          const p=document.querySelector('#me-neutral-toolbar').getBoundingClientRect();
          return {scrollY:scrollY,node:{top:r.top,bottom:r.bottom,left:r.left,right:r.right},
                  panel:{top:p.top,bottom:p.bottom,left:p.left,right:p.right},height:innerHeight};
        }""")
        print("PAGE REVEAL",width,geometry,flush=True)
        assert geometry['scrollY']>0,geometry
        def visible_selection():
            assert page.evaluate("""() => {
              const node=document.querySelector('main [data-local-selected][data-local-block]');
              const r=node.getBoundingClientRect(), p=document.querySelector('#me-neutral-toolbar').getBoundingClientRect();
              const overlap=r.left<p.right&&r.right>p.left&&r.top<p.bottom&&r.bottom>p.top;
              return r.top>=0&&r.bottom<=innerHeight&&!overlap;
            }"""), "selected block is obscured or outside viewport"
        # At 390 the fixed bottom toolbar must not obscure the insertion.
        # At desktop the right card overlaps the toolbar horizontally;
        # a sufficiently tall viewport band is required.
        visible_selection()
        page.locator("#me-neutral-section").select_option("0")
        choose_anchor(page,"Scheda A")
        page.locator("#me-neutral-placement").select_option("after")
        page.locator('[data-me-group="block"] summary').click()
        page.locator('[data-me-action="transfer"]').click()
        assert selected.locator("xpath=..").locator("h2").inner_text().startswith("Scheda A")
        visible_selection()
        assert page.evaluate("() => window.metaEditorPage.undo()")["changed"]
        assert page.evaluate("() => window.metaEditorPage.undo()")["changed"]
        assert page.evaluate("() => window.metaEditorPage.cleanHtml()")==original
        assert not errors,errors
        print("PASS",width,"real insert and transfer reveal selected DOM block; full Undo")
    finally:
        page.close()


def exercise_direct(browser,tmp,width):
    original=FIXTURE.read_text(encoding="utf-8").replace(
        "</style>","header{min-height:400px} footer{min-height:900px}</style>",1)
    adapter,controller=[(LAB/name).read_text(encoding="utf-8") for name in MODULES]
    local=tmp/f"direct-{width}.html"
    local.write_text(build(original,adapter,controller),encoding="utf-8")
    page=browser.new_page(viewport={"width":width,"height":850},accept_downloads=True)
    errors=[]
    page.on("pageerror",lambda e:errors.append(str(e)))
    try:
        page.goto(local.as_uri())
        page.wait_for_function("() => !!window.metaEditorPage")
        # Native panel is reduced, not replaced; the local gesture must work
        # without navigating dropdowns or an action menu.
        page.locator('#me-neutral-toggle').click()
        title=page.locator("main .card").first.locator("h2")
        title.evaluate("(n)=>n.scrollIntoView({block:'center',behavior:'instant'})")
        title.click()
        actions=page.locator('#me-neutral-context-actions')
        actions.wait_for(state='visible')
        assert title.get_attribute('data-local-selected')=='true'
        actions.locator('[data-me-context-action="insert-p"]').click()
        added=page.locator("main .card").first.locator('p[data-local-block]')
        assert added.count()==1
        assert title.evaluate("(n)=>n.nextElementSibling.matches('p[data-local-block]')")
        assert added.get_attribute('data-local-selected')=='true'
        actions.wait_for(state='visible')
        actions.locator('[data-me-context-action="edit"]').click()
        assert added.get_attribute('contenteditable')=='true'
        assert actions.is_hidden()
        added.fill('Testo creato direttamente nella scheda')
        added.press('Escape')
        assert added.inner_text()=='Testo creato direttamente nella scheda'
        assert added.get_attribute('contenteditable') is None
        clean=page.evaluate("() => window.metaEditorPage.cleanHtml()")
        work=page.evaluate("() => window.metaEditorPage.workHtml()")
        assert 'Testo creato direttamente nella scheda' in clean
        assert 'id="me-neutral-context-actions"' not in clean
        assert 'id="me-neutral-context-actions"' not in work
        saved=tmp/f"direct-reopen-{width}.html"
        saved.write_text(work,encoding="utf-8")
        reopened=browser.new_page(viewport={"width":width,"height":850})
        try:
            reopened.goto(saved.as_uri())
            reopened.wait_for_function("() => !!window.metaEditorPage")
            assert reopened.locator('#me-neutral-context-actions').count()==1
            assert reopened.locator("main .card").first.locator('p[data-local-block]').inner_text()=='Testo creato direttamente nella scheda'
        finally:
            reopened.close()
        assert page.evaluate("() => window.metaEditorPage.undo()")["changed"]
        assert page.evaluate("() => window.metaEditorPage.undo()")["changed"]
        assert page.evaluate("() => window.metaEditorPage.cleanHtml()")==original
        assert not errors,errors
        print("PASS",width,"contextual click insertion/edit, reopen with one UI, exact full Undo")
    finally:
        page.close()


def exercise_composition(browser,tmp,width):
    original=FIXTURE.read_text(encoding="utf-8")
    adapter,controller=[(LAB/name).read_text(encoding="utf-8") for name in MODULES]
    local=tmp/f"composition-{width}.html"
    local.write_text(build(original,adapter,controller),encoding="utf-8")
    page=browser.new_page(viewport={"width":width,"height":850},accept_downloads=True)
    errors=[]
    page.on("pageerror",lambda e:errors.append(str(e)))
    try:
        page.goto(local.as_uri())
        page.wait_for_function("() => !!window.metaEditorPage")
        page.locator("#me-neutral-section").select_option("0")
        page.locator("#me-neutral-sections summary").click()
        page.locator("#me-neutral-section-template").select_option("columns")
        page.locator('[data-me-action="section-add"]').click()
        section=page.locator('main > section[data-local-section="columns"]')
        assert section.count()==1
        assert page.locator("main > section").nth(1).get_attribute("data-local-section")=="columns"
        assert section.locator("h3").count()==2
        heading=section.locator("h2")
        assert heading.get_attribute("data-local-selected")=="true"
        page.locator("#me-neutral-appearance summary").click()
        field=page.locator("#me-neutral-font-size")
        field.fill("30")
        field.press("Tab")
        assert heading.evaluate("(n)=>n.style.fontSize")=="30px"
        page.locator("#me-neutral-align").select_option("center")
        assert heading.evaluate("(n)=>n.style.textAlign")=="center"
        assert page.evaluate("() => window.metaEditorPage.undo()")["changed"]
        assert heading.evaluate("(n)=>n.style.textAlign")==""
        assert page.evaluate("() => window.metaEditorPage.redo()")["changed"]
        assert heading.evaluate("(n)=>n.style.textAlign")=="center"
        # Section choice remains native; management applies only to generated sections.
        page.locator("#me-neutral-section").select_option("1")
        page.locator('[data-me-action="section-copy"]').click()
        assert section.count()==2
        assert section.nth(1).locator("h2").evaluate("(n)=>n.style.fontSize")=="30px"
        page.locator('[data-me-action="section-down"]').click()
        assert page.locator("main > section").last.get_attribute("data-local-section")=="columns"
        page.locator('[data-me-action="section-delete"]').click()
        assert section.count()==1
        clean=page.evaluate("() => window.metaEditorPage.cleanHtml()")
        work=page.evaluate("() => window.metaEditorPage.workHtml()")
        assert "data-local-section" not in clean
        assert "flex-wrap: wrap" in clean
        assert "data-local-section" in work
        # Verify actual responsive columns and styles on the clean page.
        path=tmp/f"composition-clean-{width}.html"
        path.write_text(clean,encoding="utf-8")
        public=browser.new_page(viewport={"width":width,"height":850})
        try:
            public.goto(path.as_uri())
            cells=public.locator("main > section").nth(1).locator("h3")
            a,b=cells.nth(0).bounding_box(),cells.nth(1).bounding_box()
            if width==390: assert b["y"]>a["y"],(a,b)
            else: assert b["x"]>a["x"],(a,b)
            assert public.locator("#me-neutral-toolbar").count()==0
        finally:
            public.close()
        for _ in range(12):
            if not page.evaluate("() => window.metaEditorPage.status().canUndo"):break
            assert page.evaluate("() => window.metaEditorPage.undo()")["changed"]
        assert page.evaluate("() => window.metaEditorPage.cleanHtml()")==original
        assert not errors,errors
        print("PASS",width,"responsive section composition, style, copy/move/delete, exact Undo")
    finally:
        page.close()


def exercise_reuse(browser,tmp,width):
    original=FIXTURE.read_text(encoding="utf-8")
    adapter,controller=[(LAB/name).read_text(encoding="utf-8") for name in MODULES]
    local=tmp/f"reuse-{width}.html"
    local.write_text(build(original,adapter,controller),encoding="utf-8")
    page=browser.new_page(viewport={"width":width,"height":850},accept_downloads=True)
    page.on('dialog',lambda d:d.accept())
    errors=[]
    page.on("pageerror",lambda e:errors.append(str(e)))
    try:
        page.goto(local.as_uri())
        page.wait_for_function("() => !!window.metaEditorPage")
        page.locator("#me-neutral-section").select_option("0")
        page.locator("#me-neutral-sections summary").click()
        page.locator("#me-neutral-section-template").select_option("columns")
        page.locator('[data-me-action="section-add"]').click()
        section=page.locator('main > section[data-local-section="columns"]')
        heading=section.locator('h2')
        assert heading.get_attribute('data-local-selected')=='true'
        page.locator('[data-me-action="edit"]').click()
        heading.fill('Modello di progetto')
        # Instrument only the actual main clone call while typing.
        page.evaluate("""() => {window.cloneCount=0;const original=Element.prototype.cloneNode;
            Element.prototype.cloneNode=function(...args){if(this.localName==='main')window.cloneCount++;return original.apply(this,args)}}""")
        heading.press('End')
        heading.press_sequentially(' riusabile',delay=0)
        assert page.evaluate("window.cloneCount")==0
        heading.press('Control+Enter')
        assert heading.get_attribute("contenteditable") is None
        assert heading.inner_text()=="Modello di progetto riusabile"
        assert page.evaluate("window.cloneCount")>0
        page.locator('#me-neutral-appearance summary').click()
        page.locator('#me-neutral-font-size').fill('28')
        page.locator('#me-neutral-font-size').press('Tab')
        with page.expect_download() as info:
            page.locator('[data-me-action="section-export"]').click()
        packfile=tmp/f"section-{width}.json"
        info.value.save_as(packfile)
        pack=json.loads(packfile.read_text(encoding="utf-8"))
        assert pack['schema']=='metaeditor.section.v1'
        assert pack['kind']=='columns'
        # Import into a distinct work document, not the source.
        target=browser.new_page(viewport={"width":width,"height":850})
        try:
            target.goto(local.as_uri())
            target.wait_for_function("() => !!window.metaEditorPage")
            target.locator('#me-neutral-section').select_option('1')
            target.locator('#me-neutral-sections summary').click()
            target.locator('#me-neutral-section-import').set_input_files(str(packfile))
            imported=target.locator('main > section[data-local-section="columns"]')
            imported.wait_for(state='attached')
            assert imported.locator('h2').inner_text()=="Modello di progetto riusabile"
            assert imported.locator('h2').evaluate("(n)=>n.style.fontSize")=="28px"
            assert imported.locator('h3').count()==2
            assert target.evaluate("() => window.metaEditorPage.undo()")["changed"]
            assert target.evaluate("() => window.metaEditorPage.cleanHtml()")==original
            # No imported HTML, arbitrary attributes or URL CSS.
            malformed=dict(pack)
            malformed['tree']=dict(pack['tree'],style={'background-image':'url(https://invalid.example/a)'})
            bad=tmp/f"bad-{width}.json"
            bad.write_text(json.dumps(malformed),encoding='utf-8')
            target.locator('#me-neutral-section-import').set_input_files(str(bad))
            target.wait_for_function("document.querySelector('#me-neutral-status').textContent.includes('rifiutato')")
            assert target.evaluate("() => window.metaEditorPage.cleanHtml()")==original
            assert target.evaluate("() => !window.metaEditorPage.status().canUndo")
        finally:
            target.close()
        assert not errors,errors
        print("PASS",width,"portable section JSON roundtrip, invalid style refused, zero whole-main clones during typing")
    finally:
        page.close()


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--channel", default=None)
    p.add_argument("--chromium", default=None)
    args=p.parse_args()
    launch={"headless":True,"args":["--no-sandbox"]}
    if args.channel: launch["channel"]=args.channel
    if args.chromium: launch["executable_path"]=args.chromium
    with tempfile.TemporaryDirectory(prefix="metaeditor-layout-") as tmp:
        with sync_playwright() as play:
            browser=play.chromium.launch(**launch)
            try:
                for width in (1440,390):
                    run(browser,Path(tmp),width)
                    exercise_reveal(browser,Path(tmp),width)
                    exercise_direct(browser,Path(tmp),width)
                    exercise_composition(browser,Path(tmp),width)
                    exercise_reuse(browser,Path(tmp),width)
            finally:
                browser.close()


if __name__=="__main__":
    main()
