from pathlib import Path
import subprocess, sys
_root = Path(__file__).resolve().parents[1]
_standalone = _root / 'examples/window-surface/standalone.html'
if not _standalone.exists(): subprocess.run([sys.executable, str(_root / 'tools/generate_window_surface_demo.py')], check=True)
from playwright.sync_api import sync_playwright
import json
html=open(str(Path(__file__).resolve().parents[1] / 'examples/window-surface/standalone.html')).read()
result=[];errors=[]
def check(name,val,detail=None): result.append({'check':name,'passed':bool(val),'detail':detail if not val else None})
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1500,'height':930},device_scale_factor=1)
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(html);page.wait_for_timeout(100)
 page.locator('[data-demo-open]').first.click();page.wait_for_timeout(550)
 frame=page.locator('.kux-surface-frame');head=page.locator('.kux-surface-header');grip=page.locator('.kux-surface-resize')
 before=page.evaluate('window.KUX_UI_LAB.surface.snapshot().geometry')
 h=head.bounding_box();page.mouse.move(h['x']+100,h['y']+30);page.mouse.down();page.mouse.move(h['x']+166,h['y']+78,steps=8);page.mouse.up();page.wait_for_timeout(100)
 after=page.evaluate('window.KUX_UI_LAB.surface.snapshot().geometry')
 check('drag changes free x and y',after['x']>before['x']+30 and after['y']>before['y']+25,[before,after])
 r=grip.bounding_box();page.mouse.move(r['x']+10,r['y']+10);page.mouse.down();page.mouse.move(r['x']-60,r['y']-52,steps=8);page.mouse.up();page.wait_for_timeout(100)
 resized=page.evaluate('window.KUX_UI_LAB.surface.snapshot().geometry')
 check('resize changes manual geometry',resized['w']<before['w'] and resized['h']<before['h'],[before,resized])
 grip.focus();page.keyboard.press('Shift+ArrowLeft')
 smaller=page.evaluate('window.KUX_UI_LAB.surface.snapshot().geometry.w')
 check('keyboard resize available',smaller<resized['w'],[resized['w'],smaller])
 page.get_by_role('button',name='Pagina intera').click();page.wait_for_timeout(450)
 check('enters full via toolbar',page.evaluate('window.KUX_UI_LAB.surface.snapshot().mode')=='full')
 page.get_by_role('button',name='Riduci ad avatar').focus();page.keyboard.press('Escape');page.wait_for_timeout(450)
 check('Escape from full returns to floating',page.evaluate('window.KUX_UI_LAB.surface.snapshot().mode')=='floating')
 returned=page.evaluate('window.KUX_UI_LAB.surface.snapshot().geometry')
 check('free geometry survives full transition',returned['w']==smaller and returned['x']==after['x'] and returned['y']==after['y'],[returned,smaller,after])
 # context available no actual provider; submitting unsent draft should not fabricate a remote receipt.
 page.get_by_role('button',name='Riduci ad avatar').click();page.wait_for_timeout(480)
 same=page.evaluate("window.KUX_UI_LAB.surface.notify({id:'kn:notice:x',text:'Prima volta'})")
 dupe=page.evaluate("window.KUX_UI_LAB.surface.notify({id:'kn:notice:x',text:'Seconda volta'})")
 check('notice deduplicated by source event ID',same is True and dupe is False)
 check('closed avatar has one cue',page.locator('.kux-surface-cue').is_visible() and 'Prima volta' in page.locator('.kux-cue-message').inner_text())
 page.locator('.kux-cue-dismiss').click()
 check('dismissed cue is hidden, avatar remains',page.locator('.kux-surface-cue').is_hidden() and page.locator('.kux-surface-avatar').is_visible())
 page.locator('.kux-surface-avatar').click();page.wait_for_timeout(500)
 # host action when ask: cannot call network; receipt must not say AI response.
 page.locator('.kux-chat-form').evaluate("e=>e.querySelector('.kux-chat-inputrow textarea').value='Testo di prova'")
 page.locator('.kux-chat-inputrow button').click();page.wait_for_timeout(100)
 log=page.locator('.kux-chat-messages').inner_text()
 check('assistant clearly unavailable',('Nessun assistente' in log or 'nessun' in log.lower()) and 'Testo di prova' in log,log[-450:])
 check('question does not mutate domain',page.evaluate('window.KUX_UI_LAB.medium.snapshot().revision')==0)
 # back to compact after viewport resize and restore manual geometry
 page.set_viewport_size({'width':390,'height':844});page.wait_for_timeout(190)
 check('compact viewport presentation forced, preference preserved',page.evaluate("window.KUX_UI_LAB.surface.snapshot().mode==='full' && window.KUX_UI_LAB.surface.snapshot().preferred==='floating'"))
 page.set_viewport_size({'width':1500,'height':930});page.wait_for_timeout(190)
 check('manual preference resumes on desktop',page.evaluate("window.KUX_UI_LAB.surface.snapshot().mode==='floating'"))
 check('no page errors',len(errors)==0,errors)
 b.close()
out={'passed':sum(x['passed'] for x in result),'total':len(result),'checks':result,'page_errors':errors}
print(json.dumps(out,indent=2,ensure_ascii=False))
open(str(Path(__file__).resolve().parents[1] / 'examples/window-surface/qa_extended.json'),'w').write(json.dumps(out,indent=2,ensure_ascii=False))
