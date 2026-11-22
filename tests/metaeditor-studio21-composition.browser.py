#!/usr/bin/env python3
"""Exercise native-backed insert and nudge commands in REAL Studio21 standalone HTML.

Source IT/EN, Chromium desktop/mobile, native scene insertion, nudge, refusal, Undo/Redo.
Requires playwright + installed Chromium. Does not exercise Windows file://.
No browser calls to remote services are allowed.
"""
from pathlib import Path
import argparse

from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
MODULE=ROOT/'examples/collaborative-communication-medium/meta-editor-lab/metaeditor-composition-commands.js'
MOVE_MODULE=ROOT/'examples/collaborative-communication-medium/meta-editor-lab/metaeditor-native-move.js'
STUDIO=ROOT/'examples/collaborative-communication-medium'


def inspect(page):
    return page.evaluate("""() => Array.from(
      document.querySelectorAll('#canvas .node[data-id]'),
      node => node.dataset.id
    )""")


def exercise(browser, html, module, move_module, name, width):
    page=browser.new_page(viewport={'width':width,'height':844},accept_downloads=True)
    errors=[]
    page.on('pageerror', lambda e: errors.append(str(e)))
    # Use a real HTTP origin for localStorage, with no actual outgoing requests.
    page.route('**/*', lambda r: r.abort())
    page.route('https://studio21.invalid/standalone', lambda r: r.fulfill(
        status=200,
        headers={'content-type':'text/html; charset=utf-8'},
        body=html,
    ))
    try:
        page.goto('https://studio21.invalid/standalone',wait_until='domcontentloaded',timeout=20000)
        page.wait_for_function("""() => (
          document.querySelector('#canvas') &&
          document.querySelectorAll('#canvas .node[data-id]').length > 0 &&
          document.querySelector('#undoBtn') &&
          document.querySelector('#redoBtn') &&
          document.querySelector('[data-add="text"]')
        )""",timeout=15000)
        before=inspect(page)
        assert len(before)==len(set(before)),f'{name} duplicate source node IDs'
        page.add_script_tag(content=module)
        result=page.evaluate("""() => {
          const c=MetaEditorCompositionCommands.create({carrier:'scene',document});
          const before=document.querySelectorAll('#canvas .node[data-id]').length;
          const invalidType=c.execute('insert',{type:'paragraph'});
          const invalidPosition=c.execute('insert',{type:'text',position:'before'});
          const afterInvalid=document.querySelectorAll('#canvas .node[data-id]').length;
          const inserted=c.execute('insert',{type:'text'});
          return {status:c.status(),invalidType,invalidPosition,afterInvalid,inserted,before};
        }""")
        assert result['status']['carrier']=='scene', (name,width,result)
        assert not result['invalidType']['ok'] and not result['invalidPosition']['ok']
        assert result['afterInvalid']==len(before), (name,width,'invalid command mutated scene',result)
        assert result['inserted']['ok'],(name,width,result)
        inserted=inspect(page)
        assert len(inserted)==len(before)+1,(name,width,'insert count',before,inserted)
        assert len(set(inserted))==len(inserted),(name,width,'duplicate new node id')
        assert set(before).issubset(set(inserted)),(name,width,'existing node lost')
        added=list(set(inserted)-set(before))
        assert len(added)==1,(name,width,'ambiguous inserted node',added)

        # Native Studio21 history owns the effect, not the shared adapter.
        page.locator('#undoBtn').evaluate('(el)=>el.click()')
        page.wait_for_function(
            'expected => document.querySelectorAll("#canvas .node[data-id]").length === expected',
            arg=len(before),timeout=5000)
        assert inspect(page)==before,(name,width,'Undo failed')
        page.locator('#redoBtn').evaluate('(el)=>el.click()')
        page.wait_for_function(
            'expected => document.querySelectorAll("#canvas .node[data-id]").length === expected',
            arg=len(inserted),timeout=5000)
        assert inspect(page)==inserted,(name,width,'Redo failed')

        # A second native insertion must not disturb existing node references.
        second=page.evaluate("""() =>
          MetaEditorCompositionCommands.create({carrier:'scene',document})
            .execute('insert',{type:'card'})
        """)
        assert second['ok'],(name,width,'card insertion',second)
        assert len(inspect(page))==len(before)+2,(name,width,'card count')

        # Exercise actual scene coordinates through the original native keyboard handler.
        page.add_script_tag(content=move_module)
        moved=page.evaluate("""(nodeId) => {
          const native=MetaEditorNativeMove.create({carrier:'scene',document});
          const byId=()=>[...document.querySelectorAll('#canvas .node[data-id]')]
            .find(el=>el.dataset.id===nodeId);
          const left=byId().style.left;
          const beforeIds=[...document.querySelectorAll('#canvas .node[data-id]')].map(n=>n.dataset.id);
          const missing=native.execute({nodeId:'nonexistent',direction:'right'});
          const wrong=native.execute({nodeId,direction:'__proto__'});
          const pageOnly=native.execute({nodeId,direction:'right',placement:'before'});
          const afterInvalid=byId().style.left;
          const move=native.execute({nodeId,direction:'right'});
          const next=byId().style.left;
          const afterIds=[...document.querySelectorAll('#canvas .node[data-id]')].map(n=>n.dataset.id);
          return {status:native.status(),missing,wrong,pageOnly,afterInvalid,left,move,next,beforeIds,afterIds};
        }""",added[0])
        assert moved['status']['operation']=='nudge-scene-node',(name,width,moved)
        assert not moved['missing']['ok'] and not moved['wrong']['ok'] and not moved['pageOnly']['ok']
        assert moved['afterInvalid']==moved['left'],(name,width,'invalid nudge changed geometry')
        assert moved['move']['ok'] and moved['next']!=moved['left'],(name,width,'native nudge',moved)
        assert moved['afterIds']==moved['beforeIds'],(name,width,'nudge changed node IDs')
        page.locator('#undoBtn').evaluate('(el)=>el.click()')
        undo_left=page.evaluate("""id => [...document.querySelectorAll('#canvas .node[data-id]')]
          .find(el=>el.dataset.id===id)?.style.left""",added[0])
        assert undo_left==moved['left'],(name,width,'nudge Undo')
        page.locator('#redoBtn').evaluate('(el)=>el.click()')
        redo_left=page.evaluate("""id => [...document.querySelectorAll('#canvas .node[data-id]')]
          .find(el=>el.dataset.id===id)?.style.left""",added[0])
        assert redo_left==moved['next'],(name,width,'nudge Redo')

        # Reading mode is not an editing destination even when a hidden canvas remains in DOM.
        page.locator('#viewBtn').evaluate('(el)=>el.click()')
        assert page.locator('body').evaluate('(el)=>el.classList.contains("reading-mode")'),(name,width,'reading mode not active')
        blocked=page.evaluate("""id => MetaEditorNativeMove.create({carrier:'scene',document})
          .execute({nodeId:id,direction:'right'})""",added[0])
        assert not blocked['ok'],(name,width,'movement allowed in reading mode')
        page.locator('#viewBtn').evaluate('(el)=>el.click()')
        assert not errors,(name,width,'page errors',errors)
        print('PASS',name,width,'native nodes inserted/undone/redone, unique IDs, no pageerrors')
    finally:
        page.close()


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--chromium',default=None,help='Chromium executable for local exercise')
    p.add_argument('--channel',default=None,help='Use browser channel, e.g. preinstalled Chrome in GitHub Actions')
    a=p.parse_args()
    module=MODULE.read_text(encoding='utf-8')
    move_module=MOVE_MODULE.read_text(encoding='utf-8')
    with sync_playwright() as playwright:
        launch={'headless':True,'args':['--no-sandbox']}
        if a.chromium:
            launch['executable_path']=a.chromium
        elif a.channel:
            launch['channel']=a.channel
        browser=playwright.chromium.launch(**launch)
        try:
            for name in ('MetaCanvas_Studio21_Consulenza_IT.html','MetaCanvas_Studio21_Consulenza_EN.html'):
                html=(STUDIO/name).read_text(encoding='utf-8')
                for width in (1440,390):
                    exercise(browser,html,module,move_module,name,width)
        finally:
            browser.close()


if __name__=='__main__':
    main()
