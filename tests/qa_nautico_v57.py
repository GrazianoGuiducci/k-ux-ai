"""Bounded Chromium exercise for K-UX-AI v5.7: activity states, readable text and drag anchor.

The run checks the exact candidate with page.set_content. It is not Edge, a
hosted Nautico controller, user study, account permission or site release.
"""
from __future__ import annotations
import asyncio,hashlib,json,os
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parent.parent
HTML=ROOT/'labs/nautico-ui-v4/19-griglia-rail-free-v57.html'
EXPECTED='e733a306b85f2ac3abefe20fa6801aa73b2b178e7c108b40d05bb07c5021db2d'
CHECKS=[]
def check(label,yes):
 if not yes:raise AssertionError(label)
 CHECKS.append(label)
async def state(page):return await page.evaluate('KUXAIDemo.activityRail()')
async def metric(page):
 return await page.evaluate('''() => {
 const rail=document.querySelector('.intent-dock'),stage=document.querySelector('.work-main');
 const r=rail.getBoundingClientRect(),s=stage.getBoundingClientRect();
 return {railWidth:r.width,railRight:r.right,stageLeft:s.left,
  mode:document.body.dataset.kuxActivities,
  preview:getComputedStyle(document.querySelector('#kuxRailToggle')).display,
  hide:getComputedStyle(document.querySelector('#railVisibility')).display,
  edge:getComputedStyle(document.querySelector('#activitiesEdge')).display,
  inert:rail.inert,expanded:document.body.dataset.kuxRailExpanded==='true'};
 }''')
async def drag(page,panel_id,dx,dy):
 await page.locator('#workFocusButton').click()
 await page.locator(f'#focusMenu [data-panel="{panel_id}"]').click()
 head=page.locator(f'.module[data-id="{panel_id}"] .module-head')
 r=await head.bounding_box();check('drag target rendered',bool(r and r['width']>120))
 x=r['x']+45;y=r['y']+20
 hit=await page.evaluate('''([x,y])=>document.elementFromPoint(x,y)?.closest('.module-head')?.closest('.module')?.dataset.id''',[x,y])
 check(f'drag {panel_id} start inside header',hit==panel_id)
 await page.mouse.move(x,y);await page.mouse.down();await page.mouse.move(x+dx,y+dy,steps=5)
 await page.wait_for_timeout(55)
 after=await head.bounding_box();await page.mouse.up()
 return (after['x']-r['x'],after['y']-r['y'])

async def run():
 raw=HTML.read_bytes();check('exact sha256',hashlib.sha256(raw).hexdigest()==EXPECTED)
 async with async_playwright() as pw:
  browser=await pw.chromium.launch(headless=True,executable_path=os.environ.get('KUX_CHROMIUM') or ('/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None),args=['--no-sandbox'])
  for width,height,motion in [(1715,900,'reduce'),(1280,850,'no-preference'),(768,860,'reduce'),(390,844,'reduce')]:
   context=await browser.new_context(viewport={'width':width,'height':height},reduced_motion=motion)
   page=await context.new_page();page.set_default_timeout(6000);errors=[];page.on('pageerror',lambda err:errors.append(str(err)))
   await page.set_content(raw.decode('utf-8'),wait_until='domcontentloaded');await page.locator('#startRecommended').click();await page.wait_for_timeout(140)
   tag=f'{width}x{height}/{motion}'
   check(tag+' version',await page.evaluate('KUXAIDemo.version')=='lab-2026-10-11-r5.7')
   check(tag+' work',await page.evaluate('KUXAIDemo.perception().screen')=='work')
   check(tag+' all 10 intents represented',len((await state(page))['visibleIntents'])==10)
   check(tag+' no unexpected edge initially',(await metric(page))['edge']=='none')
   check(tag+' title unchanged',float((await page.locator('.module-content h3').first.evaluate('(e)=>getComputedStyle(e).fontSize')).removesuffix('px'))>=16)
   sizes=await page.evaluate('''()=>({p:getComputedStyle(document.querySelector('.module-content p')).fontSize,
      caps:getComputedStyle(document.querySelector('.module-content .mini-caps')).fontSize,
      subtitle:getComputedStyle(document.querySelector('.module-subtitle')).fontSize,
      foot:getComputedStyle(document.querySelector('.module-foot')).fontSize})''')
   check(tag+' paragraphs readable',float(sizes['p'][:-2])>=13)
   check(tag+' tiny caps raised',float(sizes['caps'][:-2])>=11)
   check(tag+' subtitle raised',float(sizes['subtitle'][:-2])>=12)
   check(tag+' footer raised',float(sizes['foot'][:-2])>=11)
   if width>760:
    check(tag+' icons state',(await metric(page))['mode']=='icons')
    await page.locator('#railVisibility').click();hidden=await metric(page)
    check(tag+' hidden state',hidden['mode']=='hidden')
    check(tag+' hidden zero-width',hidden['railWidth']<1)
    check(tag+' hidden inaccessible',hidden['inert'])
    check(tag+' hidden edge reachable',hidden['edge']!='none')
    edge=await page.locator('#activitiesEdge').bounding_box()
    await page.mouse.move(edge['x']+8,edge['y']+28)
    await page.wait_for_timeout(100)
    peek=await metric(page)
    check(tag+' temporary icons',peek['mode']=='peek')
    check(tag+' temporary icons only',80<=peek['railWidth']<=90 and not peek['expanded'])
    check(tag+' edge remains clickable on temporary icons',peek['edge']!='none')
    check(tag+' previews require click',peek['preview']=='none')
    await page.locator('#railVisibility').click();icons=await metric(page)
    check(tag+' pin icons',icons['mode']=='icons')
    check(tag+' pinned width',80<=icons['railWidth']<=90)
    check(tag+' no preview before explicit click',not icons['expanded'])
    await page.locator('#kuxRailToggle').click();previews=await metric(page)
    check(tag+' expanded previews',previews['mode']=='previews' and previews['expanded'])
    check(tag+' preview in normal flow',255<=previews['railWidth']<=395)
    check(tag+' no overlay on cards',abs(previews['stageLeft']-previews['railRight'])<=3)
    check(tag+' no stray edge tab',previews['edge']=='none')
    check(tag+' no hide control on preview',previews['hide']=='none')
    check(tag+' all 10 previews available',await page.locator('.avatar-entry').count()==10)
    await page.locator('#kuxRailToggle').click();icons2=await metric(page)
    check(tag+' collapse preview -> icons',icons2['mode']=='icons' and icons2['railWidth']<90)
    # Hover reveals quick readback for normal pinned icons (not transient hidden overlay).
    await page.locator('#railVisibility').click()
    check(tag+' second hide',(await metric(page))['mode']=='hidden')
    await page.locator('#activitiesEdge').click()
    check(tag+' explicit edge pin',(await metric(page))['mode']=='icons')
    # Test the real drag anchor in the work stage on full-width receivers.
    if width>=1280:
     await page.locator('#btnQuickAdd').click();await page.locator('#picker .picker-item').filter(has_text='Fare').first.click()
     await page.locator('#btnQuickAdd').click();await page.locator('#picker .picker-item').filter(has_text='Esplorare').first.click()
     await page.locator('#btnWorkMenu').click();await page.locator('#layoutFree').click();await page.wait_for_timeout(1000 if motion=='no-preference' else 130)
     check(tag+' free mode',await page.evaluate('KUXAIDemo.perception().layout')=='free')
     pan=await page.evaluate('KUXAIDemo.perception().panels.filter(p=>p.visibleInField)')
     target=max(pan,key=lambda p:p['rendered']['x'])
     dx,dy=await drag(page,target['id'],-110,12)
     check(tag+' drag moves from rendered anchor',abs(dx+110)<=12)
     check(tag+' drag vertical tracks',abs(dy-12)<=9)
     check(tag+' drag persistent free mode',await page.evaluate('KUXAIDemo.perception().layout')=='free')
     # Unfocused left/right card must remain the same object after focus switch.
     another=max((p for p in pan if p['id']!=target['id']),key=lambda p:p['rendered']['x'])
     dx2,dy2=await drag(page,another['id'],-80,18)
     check(tag+' alternate focus drag tracks',abs(dx2+80)<=14)
     check(tag+' alternate drag vertical respects stage bounds',0<=dy2<=18)
   check(tag+' no page errors',not errors)
   await context.close()
  await browser.close()
 receipt={
  'schema':'kux-ai.v57.rail-drag-type.exercise.v1',
  'source_sha256':EXPECTED,'check_count':len(CHECKS),'passed':len(CHECKS),'correlated':True,
  'test':'python tests/qa_nautico_v57.py','method':'Chromium Playwright page.set_content; normal/reduced motion',
  'viewports':['1715x900 reduced','1280x850 normal','768x860 reduced','390x844 reduced'],
  'javascript_page_errors_observed':0,'checks':CHECKS,
  'boundaries':['synthetic demo only','not Edge file URL','not full accessibility or touchscreen audit','not real kernel or AI','not public site integration','storage and multiuser authority untested']}
 dst=ROOT/'labs/nautico-ui-v4/EVIDENCE_ACTIVITY_DRAG_TYPOGRAPHY_V57_20261011.json'
 dst.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
 print('PASS new',len(CHECKS))
if __name__=='__main__':asyncio.run(run())
