#!/usr/bin/env python3
"""Move a Studio21 section with children and a link in the real standalone runtime.

Controlled fixture changes ONLY the ccm-data JSON, not the Studio21 JS/CSS.
Checks native keyboard move, persisted geometry, node/asset/link identities,
native Undo/Redo, and a fresh download. This is a release regression, not
proof about unrelated touch, screen readers or arbitrary imported files.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'examples/collaborative-communication-medium'
MOVE=SOURCE/'meta-editor-lab/metaeditor-native-move.js'
MODEL=re.compile(r'(<script id="ccm-data" type="application/json">)(.*?)(</script>)', re.S)
SEC='regression-section'
CHILD='regression-card'
IMAGE='regression-image'
LINK='regression-link'
PNG='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO5N1f0AAAAASUVORK5CYII='


def fixture_html(original: str) -> tuple[str,dict]:
    match=MODEL.search(original)
    assert match, 'Studio21 ccm-data not found'
    doc=json.loads(match.group(2))
    scene=doc['scenes'][0]
    present={item['id'] for item in scene['elements']}
    assert len(present)==len(scene['elements'])
    assert {SEC,CHILD,IMAGE}.isdisjoint(present)
    endpoint = 'd1-c' if 'd1-c' in present else next(item['id'] for item in scene['elements'] if item['type']=='card')
    scene['elements'].extend([
        {'id':SEC,'type':'section','x':450,'y':300,'w':340,'h':245,
         'text':'Layout regression','fontSize':18,'color':'#183146',
         'fill':'#f1f6f6','align':'left'},
        {'id':CHILD,'type':'card','x':490,'y':345,'w':140,'h':65,
         'containerId':SEC,'text':'Child with relation','fontSize':20,
         'color':'#183146','fill':'#e7f5f0','align':'center'},
        {'id':IMAGE,'type':'image','x':490,'y':435,'w':110,'h':70,
         'containerId':SEC,'text':'Raster child','src':PNG,'fontSize':18}
    ])
    scene['links'].append({'id':LINK,'from':CHILD,'to':endpoint,
                           'label':'regression edge','width':3,'color':'#087b70',
                           'fromAnchor':'right','toAnchor':'left','arrow':True})
    data=json.dumps(doc,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    output=original[:match.start(2)]+data+original[match.end(2):]
    return output,doc


def download_model(page):
    with page.expect_download(timeout=20000) as event:
        page.locator('#saveBtn').evaluate('(button)=>button.click()')
    exported=Path(event.value.path()).read_text(encoding='utf-8')
    match=MODEL.search(exported)
    assert match, 'Saved work lacks ccm-data'
    return json.loads(match.group(2))


def elements(model):
    scene=model['scenes'][0]
    return {n['id']:n for n in scene['elements']}, {l['id']:l for l in scene['links']}


def observe(browser, name, width, source, move_js):
    page=browser.new_page(viewport={'width':width,'height':844},accept_downloads=True)
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.route('**/*',lambda r:r.abort())
    page.route('https://studio21.invalid/standalone',lambda r:r.fulfill(
        status=200,headers={'content-type':'text/html; charset=utf-8'},body=source))
    try:
        page.goto('https://studio21.invalid/standalone',wait_until='domcontentloaded')
        page.wait_for_function("""() => (
          document.querySelector('#canvas .node[data-id="regression-section"]') &&
          document.querySelector('#canvas .node[data-id="regression-card"]') &&
          document.querySelector('#canvas .node[data-id="regression-image"]') &&
          document.querySelectorAll('#canvas .edge-visible').length>=2
        )""")
        page.add_script_tag(content=move_js)
        initial=download_model(page)
        first,links_before=elements(initial)
        assert first[CHILD]['containerId']==SEC and first[IMAGE]['containerId']==SEC
        assert links_before[LINK]['from']==CHILD and links_before[LINK]['to'] in first
        assert links_before[LINK]['to'] not in {SEC,CHILD,IMAGE}
        initial_route=page.locator('#canvas .edge-visible').last.get_attribute('d')
        res=page.evaluate("""() => MetaEditorNativeMove.create({carrier:'scene',document})
          .execute({nodeId:'regression-section',direction:'right'})""")
        assert res['ok'],(name,width,'native move refused',res)
        after=download_model(page)
        next_nodes,next_links=elements(after)
        assert next_nodes[SEC]['x']==first[SEC]['x']+5,(name,width,'section did not move')
        # Children must travel WITH their native layout section.
        assert next_nodes[CHILD]['x']==first[CHILD]['x']+5,(name,width,'child separated from section')
        assert next_nodes[IMAGE]['x']==first[IMAGE]['x']+5,(name,width,'image separated from section')
        assert next_nodes[CHILD]['containerId']==SEC and next_nodes[IMAGE]['containerId']==SEC
        assert next_nodes[IMAGE]['src']==PNG,(name,width,'raster changed on move')
        assert next_links[LINK]==links_before[LINK],(name,width,'edge identity/anchors mutated')
        route_after=page.locator('#canvas .edge-visible').last.get_attribute('d')
        assert route_after!=initial_route,(name,width,'linked route did not follow moving child')

        page.locator('#undoBtn').evaluate('(button)=>button.click()')
        undone=download_model(page)
        restored,restored_links=elements(undone)
        for key in (SEC,CHILD,IMAGE):
            assert restored[key]==first[key],(name,width,'Undo did not restore',key)
        assert restored_links[LINK]==links_before[LINK],(name,width,'Undo link drift')
        assert page.locator('#canvas .edge-visible').last.get_attribute('d')==initial_route

        page.locator('#redoBtn').evaluate('(button)=>button.click()')
        redone=download_model(page)
        repeated,repeated_links=elements(redone)
        for key in (SEC,CHILD,IMAGE):
            assert repeated[key]==next_nodes[key],(name,width,'Redo changed geometry',key)
        assert repeated_links[LINK]==next_links[LINK],(name,width,'Redo link drift')
        assert not errors,(name,width,'page errors',errors)
        print('PASS',name,width,'section+child+image+link geometry; native Undo/Redo')
    finally:
        page.close()


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--channel',default=None)
    p.add_argument('--chromium',default=None)
    p.add_argument('--candidate-root',type=Path,default=None,
                   help='Use a prebuilt candidate Studio21 source tree, if supplied')
    args=p.parse_args()
    files=args.candidate_root or SOURCE
    move_js=MOVE.read_text(encoding='utf-8')
    with sync_playwright() as play:
        config={'headless':True,'args':['--no-sandbox']}
        if args.channel:config['channel']=args.channel
        if args.chromium:config['executable_path']=args.chromium
        browser=play.chromium.launch(**config)
        try:
            for name in ('MetaCanvas_Studio21_Consulenza_IT.html','MetaCanvas_Studio21_Consulenza_EN.html'):
                source,doc=fixture_html((files/name).read_text(encoding='utf-8'))
                for width in (1440,390):
                    observe(browser,name,width,source,move_js)
        finally:
            browser.close()


if __name__=='__main__':
    main()
