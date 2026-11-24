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
        is_guide=page.locator('#guideOptions').count()>0
        if is_guide:
            assert page.locator('body').evaluate("(b)=>b.classList.contains('guided-playground')")
            assert page.locator('#publicFirstUse').is_visible()
            assert page.locator('#me-template-entry').is_hidden()
        nodes=[n for n in model["scenes"][0]["elements"] if n["type"]=="text"]
        a,b=nodes[0]["id"],nodes[1]["id"]
        # Native keyboard selection is an accessible real route even in a narrow canvas.
        target=page.locator(f'#canvas .node[data-id="{a}"]')
        target.focus()
        target.press("Enter")
        page.locator("#quickEditor").wait_for(state="visible")
        assert target.evaluate("(n)=>n.classList.contains('is-selected')")
        if width<=700:
            quick_rect=page.locator('#quickEditor').bounding_box()
            confirm_rect=page.locator('#editOk').bounding_box()
            assert quick_rect and confirm_rect
            assert quick_rect['y']+quick_rect['height']<=confirm_rect['y'],(path.name,width,quick_rect,confirm_rect)
        page.locator("#editOk").click()
        bar=page.locator("#me-visual-actions")
        bar.wait_for(state="visible")
        assert bar.get_attribute("data-selected-id")==a
        bar.locator('[data-visual-action="text"]').click()
        page.locator("#editOk").click()
        bar.wait_for(state="visible")
        assert bar.get_attribute("data-selected-id")==a
        canvas=page.locator('#canvas')
        before_rect=canvas.bounding_box()
        bar.locator('[data-visual-action="size"]').click()
        page.locator("#propertyPanel.drawer-open").wait_for(state="visible")
        page.evaluate("window.dispatchEvent(new Event('resize'))")
        page.wait_for_timeout(300)
        assert bar.is_hidden()
        panel_rect=page.locator('#propertyPanel').bounding_box()
        after_rect=canvas.bounding_box()
        print('GEOMETRY',path.name,width,'before',before_rect,'after',after_rect,'panel',panel_rect,flush=True)
        if width>=1001 and is_guide:
            assert before_rect['width']>=width*0.48,(path.name,width,'guide canvas collapsed',before_rect)
            assert after_rect['x']+after_rect['width']<=panel_rect['x']+2,(path.name,width,'side inspector covers canvas',after_rect,panel_rect)
        # Actually modify a native property, not merely open its inspector.
        node=next(n for n in model['scenes'][0]['elements'] if n['id']==a)
        field=page.locator('#inspectorContent').get_by_label('Larghezza',exact=True)
        new_width=int(node['w'])-10 if node['w']>75 else int(node['w'])+5
        field.fill(str(new_width))
        field.press('Tab')
        changed=visual.model_from(visual.download(page,'#saveBtn'))
        assert next(n for n in changed['scenes'][0]['elements'] if n['id']==a)['w']==new_width
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
        # The Playground's tutorial deliberately hides Flat and full tools.
        # Enter the full editor via the native guide transition first.
        if is_guide:
            page.locator('#guideOptions summary').click()
            page.locator('#guideExplore').click()
            assert not page.locator('body').evaluate("(b)=>b.classList.contains('guided-playground')")
            assert page.locator('#publicFirstUse').is_visible()
        # Reuse Flat and the existing native template engine.
        flat=page.locator("#flatLayoutBtn")
        if flat.get_attribute("aria-pressed")!="true":
            flat.click()
        assert page.locator("body").evaluate("(b)=>b.classList.contains('flat-layout')")
        if is_guide:
            # Flat must not hide the route back to the tutorial.
            assert page.locator('#publicFirstUse').is_visible()
            page.locator('#guideOptions summary').click()
            page.locator('#guideExplore').click()
            assert page.locator('body').evaluate("(b)=>b.classList.contains('guided-playground')")
            assert page.locator('#publicFirstUse').is_visible()
            assert page.locator('#me-template-entry').is_hidden()
            page.locator('#guideOptions summary').click()
            page.locator('#guideExplore').click()
        page.locator("#me-template-entry").click()
        section=page.locator('#toolPanel [data-section="templates"]')
        assert section.evaluate("(e)=>e.open&&!e.hidden")
        before=len(visual.model_from(visual.download(page,"#saveBtn"))["scenes"])
        section.locator('#agentTemplateList [data-template-action="below"]').first.click()
        saved_html=visual.download(page,"#saveBtn")
        after=visual.model_from(saved_html)
        assert len(after["scenes"])==before+1
        # Real downloaded work reopened in a fresh document, preserving scenes.
        reopened=browser.new_page(viewport={"width":width,"height":850},accept_downloads=True)
        reopen_errors=[]
        reopened.on('pageerror',lambda e:reopen_errors.append(str(e)))
        reopened.route('**/*',lambda route:route.abort())
        reopened.route('https://metacanvas.invalid/reopen',lambda route:route.fulfill(status=200,content_type='text/html; charset=utf-8',body=saved_html))
        try:
            reopened.goto('https://metacanvas.invalid/reopen',wait_until='domcontentloaded')
            reopened.locator('#canvas .node').first.wait_for(state='attached')
            assert reopened.locator('#me-template-entry').count()==1
            assert reopened.locator('#me-visual-actions').count()<=1
            restored=visual.model_from(visual.download(reopened,'#saveBtn'))
            assert [s['id'] for s in restored['scenes']]==[s['id'] for s in after['scenes']]
            assert not reopen_errors,reopen_errors
        finally:
            reopened.close()
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
