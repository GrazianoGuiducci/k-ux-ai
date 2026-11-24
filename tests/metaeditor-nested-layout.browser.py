#!/usr/bin/env python3
"""Regression of exact composition references in nested card/grid layouts.

A semantic section can contain multiple independent text-flow parents.
This test proves safe refusal of ambiguous automatic destinations, explicit
before/after anchors, same-section reposition and cross-section transfer.
It runs on an entirely synthetic local HTML fixture, at desktop/mobile width.
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
            finally:
                browser.close()


if __name__=="__main__":
    main()
