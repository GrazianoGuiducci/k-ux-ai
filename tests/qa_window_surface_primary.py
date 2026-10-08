from pathlib import Path
import subprocess, sys
_root = Path(__file__).resolve().parents[1]
_standalone = _root / 'examples/window-surface/standalone.html'
if not _standalone.exists(): subprocess.run([sys.executable, str(_root / 'tools/generate_window_surface_demo.py')], check=True)
from playwright.sync_api import sync_playwright
import json, traceback
base='http://127.0.0.1:8899/examples/window-surface/index.html'
checks=[]; bugs=[]
def check(name,ok,details=''):
    checks.append((name,bool(ok),str(details)[:260]))
    if not ok: bugs.append((name,details))
with sync_playwright() as p:
  b=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=b.new_page(viewport={'width':1440,'height':900},device_scale_factor=1)
  errors=[]
  page.on('pageerror',lambda e: errors.append(str(e)))
  page.set_content(open(str(Path(__file__).resolve().parents[1] / 'examples/window-surface/standalone.html')).read(),wait_until='domcontentloaded')
  page.wait_for_timeout(200)
  check('module loads',page.evaluate("!!window.KUX_UI_LAB && !!window.KUX_UI_LAB.surface && !!window.KUX_UI_LAB.module"),errors)
  check('initially closed',page.locator('.kux-surface-frame').is_hidden())
  page.locator('[data-demo-open]').first.click()
  page.wait_for_timeout(650)
  check('opens from intent card',page.locator('.kux-surface-frame').is_visible() and page.evaluate("window.KUX_UI_LAB.surface.snapshot().open"))
  page.locator('.kux-form-pane input[aria-label="Oggetto"]').fill('Poppa')
  page.locator('.kux-form-pane textarea[aria-label="Traccia, richiesta o osservazione"]').fill('La bozza non deve scomparire con il layout.')
  page.get_by_role('button',name='Pagina intera').click();page.wait_for_timeout(650)
  bbox=page.locator('.kux-surface-frame').bounding_box()
  check('full fills viewport',bbox['width']>1436 and bbox['height']>895,bbox)
  check('full keeps form draft',page.locator('textarea[aria-label="Traccia, richiesta o osservazione"]').input_value().startswith('La bozza'))
  page.get_by_role('button',name='Ripristina finestra').click();page.wait_for_timeout(500)
  check('returns to floating',page.evaluate("window.KUX_UI_LAB.surface.snapshot().mode === 'floating'"))
  page.get_by_role('button',name='Aggancia a destra').click();page.wait_for_timeout(520)
  check('dock-right active',page.evaluate("window.KUX_UI_LAB.surface.snapshot().mode === 'dock-right'"))
  check('workspace makes room',page.locator('.demo-work').get_attribute('data-dock')=='dock-right')
  check('internal compact due frame width',page.locator('.kux-chat-form').get_attribute('data-compact')=='true')
  page.locator('.kux-chat-tabs button',has_text='Modulo').click();page.wait_for_timeout(100)
  check('compact switches to form',page.locator('.kux-chat-form').get_attribute('data-pane')=='form' and page.locator('.kux-form-pane').is_visible())
  page.get_by_role('button',name='Riduci ad avatar').click();page.wait_for_timeout(520)
  check('minimizes with no state loss',page.locator('.kux-surface-frame').is_hidden() and page.locator('.kux-surface-avatar').is_visible())
  page.get_by_role('button',name='Simula evento').click();page.wait_for_timeout(80)
  check('real local event alerts while closed',page.locator('.kux-surface-cue').is_visible())
  page.locator('.kux-surface-avatar').click();page.wait_for_timeout(550)
  check('restores form draft',page.locator('textarea[aria-label="Traccia, richiesta o osservazione"]').input_value().startswith('La bozza'))
  check('source event recorded via medium',page.evaluate("window.KUX_UI_LAB.medium.snapshot().events.length === 1"))
  page.get_by_role('button',name='Consegna al controller').click();page.wait_for_timeout(150)
  check('submit increments revision',page.evaluate("window.KUX_UI_LAB.medium.snapshot().revision === 1"))
  check('draft remains after submit',page.locator('textarea[aria-label="Traccia, richiesta o osservazione"]').input_value().startswith('La bozza'))
  # screenshot
  page.screenshot(path=str(Path(__file__).resolve().parents[1] / 'examples/window-surface/desktop.png'),full_page=True)
  check('desktop no JS errors',not errors,errors)
  # touch mobile separately
  m=b.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
  errs=[];m.on('pageerror',lambda e: errs.append(str(e)))
  m.set_content(open(str(Path(__file__).resolve().parents[1] / 'examples/window-surface/standalone.html')).read(),wait_until='domcontentloaded');m.wait_for_timeout(220)
  m.locator('[data-demo-open]').first.click();m.wait_for_timeout(620)
  rect=m.locator('.kux-surface-frame').bounding_box()
  check('mobile full',rect['width']>388 and rect['height']>830,rect)
  check('mobile compact internal',m.locator('.kux-chat-form').get_attribute('data-compact')=='true')
  m.locator('.kux-chat-tabs button',has_text='Modulo').click()
  check('mobile form tab visible',m.locator('.kux-form-pane').is_visible() and m.locator('.kux-chat-pane').is_hidden())
  m.screenshot(path=str(Path(__file__).resolve().parents[1] / 'examples/window-surface/mobile.png'),full_page=True)
  check('mobile no horiz overflow',m.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
  check('mobile no page errors',not errs,errs)
  # reduce motion
  r=b.new_page(viewport={'width':1024,'height':768},reduced_motion='reduce')
  r.set_content(open(str(Path(__file__).resolve().parents[1] / 'examples/window-surface/standalone.html')).read());r.locator('[data-demo-open]').first.click();r.wait_for_timeout(60)
  check('reduced motion opens quickly',r.locator('.kux-surface-frame').is_visible())
  b.close()
print(json.dumps({'passed':sum(t[1] for t in checks),'total':len(checks),'checks':checks,'bugs':bugs},indent=2,ensure_ascii=False))
