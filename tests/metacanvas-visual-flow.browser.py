#!/usr/bin/env python3
"""Exercise the same visual flow candidate and native document lifecycle."""
from __future__ import annotations
import argparse
import importlib.util
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from build_metacanvas_visual_flow import build

def load(name, filename):
    spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(filename))
    assert spec and spec.loader
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

visual=load("visual_r1","metacanvas-studio21-visual-actions.browser.py")
privacy=load("flow_privacy","metaeditor-studio21-privacy.browser.py")
rel=privacy.rel

def exercise(browser, path, width, screenshots):
    page=browser.new_page(viewport={"width":width,"height":850},accept_downloads=True)
    errors=[]
    page.on("pageerror",lambda e:errors.append(str(e)))
    page.on("dialog",lambda d:d.accept())
    html=path.read_text(encoding="utf-8")
    page.route("**/*",lambda route:route.abort())
    page.route("https://metacanvas.invalid/flow",lambda route:route.fulfill(status=200,content_type="text/html; charset=utf-8",body=html))
    try:
        page.goto("https://metacanvas.invalid/flow",wait_until="domcontentloaded")
        if page.locator("body").evaluate("(b)=>b.classList.contains('reading-mode')"):
            page.locator("#viewBtn").click()
        model=visual.model_from(html)
        nodes=[n for n in model["scenes"][0]["elements"] if n["type"]=="text"]
        a,b=nodes[0]["id"],nodes[1]["id"]
        # Native keyboard selection is an accessible real route even in a narrow canvas.
        target=page.locator(f'#canvas .node[data-id="{a}"]')
        target.focus()
        target.press("Enter")
        page.locator("#quickEditor").wait_for(state="visible")
        assert target.evaluate("(n)=>n.classList.contains('is-selected')")
        page.locator("#editOk").click()
        bar=page.locator("#me-visual-actions")
        bar.wait_for(state="visible")
        assert bar.get_attribute("data-selected-id")==a
        bar.locator('[data-visual-action="text"]').click()
        page.locator("#editOk").click()
        bar.wait_for(state="visible")
        assert bar.get_attribute("data-selected-id")==a
        bar.locator('[data-visual-action="size"]').click()
        page.locator("#propertyPanel.drawer-open").wait_for(state="visible")
        page.evaluate("window.dispatchEvent(new Event('resize'))")
        page.wait_for_timeout(300)
        assert bar.is_hidden()
        if screenshots:
            screenshots.mkdir(parents=True,exist_ok=True)
            page.screenshot(path=str(screenshots/f"{path.stem}-{width}-properties.png"))
        page.locator("#closeProperties").click()
        bar.wait_for(state="visible")
        other=page.locator(f'#canvas .node[data-id="{b}"]')
        other.focus()
        other.press("Enter")
        page.locator("#quickEditor").wait_for(state="visible")
        assert other.evaluate("(n)=>n.classList.contains('is-selected')")
        assert not target.evaluate("(n)=>n.classList.contains('is-selected')")
        page.locator("#editOk").click()
        # Reuse Flat and the existing native template engine.
        flat=page.locator("#flatLayoutBtn")
        if flat.get_attribute("aria-pressed")!="true":
            flat.click()
        assert page.locator("body").evaluate("(b)=>b.classList.contains('flat-layout')")
        page.locator("#me-template-entry").click()
        section=page.locator('#toolPanel [data-section="templates"]')
        assert section.evaluate("(e)=>e.open&&!e.hidden")
        before=len(visual.model_from(visual.download(page,"#saveBtn"))["scenes"])
        section.locator('#agentTemplateList [data-template-action="below"]').first.click()
        after=visual.model_from(visual.download(page,"#saveBtn"))
        assert len(after["scenes"])==before+1
        public=visual.download(page,"#publicBtn")
        assert 'id="me-visual-actions"' not in public
        assert not errors,(path.name,width,errors)
        print("PASS",path.name,width,"visual lifecycle, native template, export")
    finally:
        page.close()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--channel",default=None)
    p.add_argument("--output-root",type=Path,required=True)
    p.add_argument("--screenshots",type=Path)
    args=p.parse_args()
    paths=build(args.output_root)
    options={"headless":True,"args":["--no-sandbox"]}
    if args.channel:options["channel"]=args.channel
    with sync_playwright() as play:
        browser=play.chromium.launch(**options)
        try:
            for path in paths:
                for width in (1440,1024,390):
                    exercise(browser,path,width,args.screenshots)
                html=path.read_text(encoding="utf-8")
                private,model=privacy.fixture(html)
                move,_=rel.fixture_html(html)
                for width in (1440,390):
                    privacy.inspect(browser,path.name,width,private,model,False)
                    rel.observe(browser,path.name,width,move,rel.MOVE.read_text(encoding="utf-8"))
        finally:
            browser.close()

if __name__=="__main__":
    main()
