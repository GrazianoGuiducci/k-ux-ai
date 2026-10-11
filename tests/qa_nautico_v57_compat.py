"""Scoped browser proof for K-UX-AI v5.7: Home, Canvas tour, contextual actions and Activity rail."""
from __future__ import annotations
import asyncio, json, hashlib, os
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parent.parent
FILE=ROOT/'labs/nautico-ui-v4/19-griglia-rail-free-v57.html'
EXPECTED='e733a306b85f2ac3abefe20fa6801aa73b2b178e7c108b40d05bb07c5021db2d'
CHECKS=[]

def check(tag,ok):
 if not ok:raise AssertionError(tag)
 CHECKS.append(tag)

async def prop(page,key):return await page.evaluate(f'KUXAIDemo.{key}')

async def run():
 raw=FILE.read_bytes()
 check('SHA256 candidate',hashlib.sha256(raw).hexdigest()==EXPECTED)
 async with async_playwright() as pw:
  chromium=os.environ.get('KUX_CHROMIUM') or ('/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None)
  browser=await pw.chromium.launch(headless=True,executable_path=chromium,args=['--no-sandbox'])
  for width,height,motion in [(1715,905,'no-preference'),(1280,830,'reduce'),(390,844,'reduce')]:
   ctxt=await browser.new_context(viewport={'width':width,'height':height},reduced_motion=motion)
   page=await ctxt.new_page();page.set_default_timeout(6000);errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   tag=f'{width}x{height}/{motion}'
   await page.set_content(raw.decode('utf-8'),wait_until='domcontentloaded');await page.wait_for_timeout(70)
   check(tag+' version',await prop(page,'version')=='lab-2026-10-11-r5.7')
   check(tag+' home',await page.evaluate('KUXAIDemo.perception().screen')=='home')
   for css in ['.top-center','.demo-tag']:
    check(tag+' home hidden '+css,await page.locator(css).first.evaluate('(x)=>getComputedStyle(x).display')=='none')
   check(tag+' home chooser',await page.locator('#homeContextOptions button').count()==5)
   check(tag+' home tile count',await page.locator('#intentGrid .intent-tile').count()==10)
   check(tag+' home primary',await page.locator('#startRecommended').is_visible())
   check(tag+' home assistant one',await page.locator('.kux-surface-root>.kux-surface-avatar').is_visible())
   await page.locator('#homeTourButton').click()
   check(tag+' home tour',await page.evaluate('KUXAIDemo.tour().kind')=='home')
   await page.locator('#homeTourClose').click()
   check(tag+' home tour close',not await page.evaluate('KUXAIDemo.tour().open'))
   await page.locator('#homeContextOptions [data-context="cantiere"]').click()
   await page.locator('#startRecommended').click();await page.wait_for_timeout(120)
   check(tag+' work',await page.evaluate('KUXAIDemo.perception().screen')=='work')
   check(tag+' context',await page.evaluate('KUXAIDemo.perception().view.context')=='cantiere')
   check(tag+' rail complete',await page.evaluate('KUXAIDemo.activityRail().visibleIntents.length')==10)
   check(tag+' no extra floating assistant',not await page.locator('#assistantOrb').is_visible())
   check(tag+' only one panel',len(await page.evaluate('KUXAIDemo.perception().panels.filter(p=>p.visibleInField)'))==1)
   check(tag+' orphan divider hidden',await page.locator('#kuxFocalDivider').evaluate('(x)=>x.hidden'))
   if width>760:
    check(tag+' rail available',await page.locator('#railVisibility').is_visible())
    await page.locator('#railVisibility').click()
    check(tag+' rail collapsed',await page.evaluate('KUXAIDemo.activityRail().mode')=='hidden')
    check(tag+' rail inert',await page.locator('.intent-dock').evaluate('(x)=>x.inert'))
    check(tag+' rail edge',await page.locator('#activitiesEdge').is_visible())
    # Chat remains at the bottom-left outside the rail when the rail is hidden.
    check(tag+' chat without rail',await page.locator('.kux-surface-root>.kux-surface-avatar').count()==1)
    await page.locator('#activitiesEdge').hover()
    await page.wait_for_timeout(55)
    check(tag+' rail hover preview',await page.evaluate('KUXAIDemo.activityRail().mode')=='peek')
    check(tag+' rail preview visible',await page.locator('.intent-dock').evaluate('(x)=>!x.inert&&getComputedStyle(x).visibility!=="hidden"'))
    await page.locator('#activitiesEdge').click()
    check(tag+' rail pinned',await page.evaluate('KUXAIDemo.activityRail().mode')=='icons')
    check(tag+' rail accessible',not await page.locator('.intent-dock').evaluate('(x)=>x.inert'))
    # Work tour: the same spotlight/guide, seven distinct steps.
    await page.locator('#btnHelp').click()
   else:
    await page.locator('#btnWorkMenu').click()
    await page.locator('#btnHelpMobile').click()
   await page.wait_for_timeout(120)
   check(tag+' work tour open',await page.evaluate('KUXAIDemo.tour().open&&KUXAIDemo.tour().kind==="work"'))
   check(tag+' work tour spotlight',await page.locator('#kuxTourSpotlight').evaluate('(x)=>!x.hidden'))
   for index in range(7):
    check(tag+f' work tour {index+1}',await page.evaluate(f'KUXAIDemo.tour().index==={index}'))
    await page.locator('#homeTourNext').click()
   check(tag+' work tour closed',not await page.evaluate('KUXAIDemo.tour().open'))
   if width>760:
    check(tag+' focus restored',await page.evaluate('document.activeElement?.id')=='btnHelp')
   # Opening a second panel should expose a real divider on wide desktop only.
   await page.locator('#btnQuickAdd').click()
   await page.locator('#picker .picker-item').filter(has_text='Esplorare').first.click()
   await page.wait_for_timeout(180)
   check(tag+' second panel exists',len(await page.evaluate('KUXAIDemo.perception().panels.filter(p=>p.visibleInField)'))>=2)
   check(tag+' no page errors',not errors)
   if width>=1280:
    # Maximize from the command: activity rail remains next to the content.
    card=page.locator('.module[data-focused="true"]')
    await card.locator('[data-module-op="max"]').click()
    await page.wait_for_timeout(180 if motion=='reduce' else 850)
    geometry=await page.evaluate('''()=>{const m=document.querySelector('.module[data-placement="full"]').getBoundingClientRect();const a=document.querySelector('.intent-dock').getBoundingClientRect();return{mx:m.x,mr:m.right,ax:a.x,ar:a.right,full:document.body.dataset.fullscreenPanel==='true',railInert:document.querySelector('.intent-dock').inert,div:document.querySelector('#kuxFocalDivider').hidden}}''')
    check(tag+' maximized',geometry['full'])
    check(tag+' side-by-side full',abs(geometry['mx']-geometry['ar'])<4)
    check(tag+' rail usable full',not geometry['railInert'])
    check(tag+' divider hidden full',geometry['div'])
    await page.locator('#railVisibility').click()
    await page.wait_for_timeout(120)
    check(tag+' edge in full',await page.locator('#activitiesEdge').is_visible())
    await page.locator('#activitiesEdge').click()
    check(tag+' show rail in full',await page.evaluate('KUXAIDemo.activityRail().mode')=='icons')
    await page.locator('.module[data-placement="full"] [data-module-op="max"]').click()
    await page.wait_for_timeout(130)
    check(tag+' restore from full',await page.evaluate('!KUXAIDemo.perception().panels.some(p=>p.maximized)'))
   check(tag+' end errors',not errors)
   await ctxt.close()
  # Exact context switching through Esplora ↗: previous panel identity must not be reassigned.
  ctx=await browser.new_context(viewport={'width':1440,'height':900},reduced_motion='reduce')
  page=await ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  await page.set_content(raw.decode('utf-8'),wait_until='domcontentloaded')
  await page.locator('#startRecommended').click()
  await page.locator('#btnQuickAdd').click()
  await page.locator('#picker .picker-item').filter(has_text='Esplorare').first.click()
  await page.wait_for_timeout(60)
  target=page.locator('.module[data-focused="true"] [data-action="change-context"][data-target="cantiere"]').first
  # Scope can be focused or other panel; locate one visible source tile.
  if not await target.count():target=page.locator('.module[data-intent="esplorare"] [data-action="change-context"][data-target="cantiere"]').first
  await target.click();await page.wait_for_timeout(90)
  check('context button changes field',await page.evaluate('KUXAIDemo.perception().view.context')=='cantiere')
  check('context button opens same intent',await page.evaluate('KUXAIDemo.perception().panels.some(p=>p.context==="cantiere"&&p.intent==="esplorare"&&p.visibleInField)'))
  check('context button retains original source panel',await page.evaluate('KUXAIDemo.perception().panels.some(p=>p.context==="poppa"&&p.intent==="esplorare")'))
  check('context button no JS error',not errors)
  await ctx.close();await browser.close()
 receipt={'schema':'kux.v57.receipt.v1','source_sha256':EXPECTED,'test':'qa_nautico_v57.py','passed':len(CHECKS),'total':len(CHECKS),'correlated':True,'checks':CHECKS,'page_errors_observed':0,'browser':'Chromium via Playwright page.set_content','viewports':['1715x905 normal','1280x830 reduce','390x844 reduce','1440x900 reduce: context'], 'not_proven':['user installed Edge','file URL behavior','real source or Nautico bridge','provider and account authorization','real touchscreen or screen-reader audit','MAIOS site and publication']}
 dst=ROOT/'labs/nautico-ui-v4/EVIDENCE_COMPATIBILITY_V57_20261011.json';dst.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n')
 print('PASS',len(CHECKS),'page errors',0)
if __name__=='__main__':asyncio.run(run())
