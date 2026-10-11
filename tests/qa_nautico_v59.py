"""K-UX-AI v5.9: source-bound browser verification of guided motion and card hierarchy.

Run from repository root with Python Playwright and Chromium installed:
  python tests/qa_nautico_v59.py
This uses page.set_content; it is not Edge physical-device testing or a site deploy.
"""
from __future__ import annotations
import asyncio
import hashlib
import json
import os
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[1]
FILE=ROOT/'labs/nautico-ui-v4/21-griglia-perceptual-continuity-v59.html'
RECEIPT=ROOT/'labs/nautico-ui-v4/EVIDENCE_GUIDED_CONTINUITY_V59_20261011.json'
EXPECTED='463d9d436ab982f4ab68ec0cd2b8770813d0346ecd26bf90b9335f0e0b57ed3a'
CHECKS=[]
ERRS=[]

def check(name,pred):
    if not pred:raise AssertionError('FAILED: '+name)
    CHECKS.append(name)

async def exercise(page, width, height, reduced):
    label=f'{width}x{height}/'+('reduce' if reduced else 'normal')
    check(label+' version', await page.evaluate('KUXAIDemo.version')=='lab-2026-10-11-r5.9')
    check(label+' starts at home', await page.evaluate('KUXAIDemo.perception().screen')=='home')
    check(label+' home tiles intact', await page.locator('#intentGrid .intent-tile').count()==10)
    check(label+' first entrance ready', await page.locator('#startRecommended').is_visible())
    if not reduced:
        check(label+' home has a scene entrance', 'kuxSceneArrival' in await page.locator('.home-screen').evaluate('(el)=>getComputedStyle(el).animationName'))
    # Guided home interaction (all three steps) and close/recovery.
    await page.locator('#homeTourButton').click()
    check(label+' home tour open', await page.locator('#homeTourDialog').evaluate('(el)=>el.open'))
    check(label+' guided focus aperture', not await page.locator('#kuxTourSpotlight').evaluate('(el)=>el.hidden'))
    check(label+' home first step', '1 / 3' in await page.locator('#homeTourStep').inner_text())
    await page.locator('#homeTourNext').click()
    check(label+' home second step', '2 / 3' in await page.locator('#homeTourStep').inner_text())
    await page.locator('#homeTourNext').click()
    check(label+' home third step', '3 / 3' in await page.locator('#homeTourStep').inner_text())
    await page.locator('#homeTourClose').click()
    check(label+' home tour closes', not await page.locator('#homeTourDialog').evaluate('(el)=>el.open'))
    # The work scene with at least five real UI cards.
    for item in ['fare','controllare','organizzare','presentare']:
        await page.locator(f'#intentGrid .intent-tile[data-intent="{item}"] .tile-open').click()
    await page.locator('#startRecommended').click()
    await page.wait_for_timeout(920 if not reduced else 120)
    check(label+' reaches work', await page.evaluate('KUXAIDemo.perception().screen')=='work')
    check(label+' five cards', await page.locator('.module:visible').count()>=5)
    check(label+' all titles present', await page.locator('.module:visible .module-title').count()>=5)
    check(label+' section/action hierarchy', await page.locator('.module:visible .module-section').count()>=5 and await page.locator('.module:visible .module-action').count()>=5)
    data=await page.evaluate('''() => {
       const cards=[...document.querySelectorAll('.module:not([hidden])')];
       const chosen=cards.find(x=>x.querySelector('.module-action')?.textContent.trim()==='Controllare');
       const cmp=chosen?getComputedStyle(chosen.querySelector('.module-title')):null;
       const tiny=chosen?getComputedStyle(chosen.querySelector('.module-action')):null;
       const sub=chosen?getComputedStyle(chosen.querySelector('.module-subtitle')):null;
       return {count:cards.length,title:chosen?.querySelector('.module-title')?.textContent,subtitle:chosen?.querySelector('.module-subtitle')?.textContent,
       section:chosen?.querySelector('.module-section')?.textContent,source:chosen?.querySelector('.module-info')?.title,
       titleSize:parseFloat(cmp?.fontSize),actionSize:parseFloat(tiny?.fontSize),subSize:parseFloat(sub?.fontSize),
       headW:chosen?.querySelector('.module-head')?.getBoundingClientRect().width,cardW:chosen?.getBoundingClientRect().width,
       titleW:chosen?.querySelector('.module-title')?.getBoundingClientRect().width};
    }''')
    check(label+' correct title is situated', data.get('title')=='Riscontri e criteri')
    check(label+' source stays qualified', 'KN/CASE-001' in (data.get('source') or ''))
    check(label+' title dominates meta', data.get('titleSize',0)>data.get('actionSize',999))
    check(label+' subtitle between title and action', data.get('actionSize',999)<data.get('subSize',0)<data.get('titleSize',0))
    check(label+' heading remains within card', (data.get('headW') or 0)<=(data.get('cardW') or 0)+1)
    check(label+' title stays in heading', (data.get('titleW') or 0)<=data.get('headW',0))
    # Source-backed checkbox control uses normal-size check and first-line baseline.
    align=await page.evaluate('''() => {
        const card=[...document.querySelectorAll('.module')].find(m=>m.querySelector('.module-action')?.textContent.trim()==='Controllare');
        const label=card?.querySelector('label.selectable-row'), input=label?.querySelector('input[type=checkbox]'),span=label?.querySelector('span');
        const a=input?.getBoundingClientRect(),b=span?.getBoundingClientRect();
        return {has:!!input&&!!span,layout:label&&getComputedStyle(label).display,inputW:a?.width,inputH:a?.height,delta:a&&b?Math.abs((a.top+2)-b.top):100};
    }''')
    check(label+' checkbox row is grid', align['has'] and align['layout']=='grid')
    check(label+' checkbox compact size', 14<=align['inputW']<=18 and 14<=align['inputH']<=18)
    check(label+' checkbox tracks first line', align['delta']<=8)
    # Tools open-state animates the arrow without changing action.
    await page.locator('#btnWorkMenu').click()
    check(label+' tools opened', not await page.locator('#workMega').evaluate('(el)=>el.hidden'))
    check(label+' tools semantic expansion', await page.locator('#btnWorkMenu').get_attribute('aria-expanded')=='true')
    if not reduced:
        duration=await page.locator('#btnWorkMenu').evaluate('(el)=>getComputedStyle(el).transitionDuration')
        check(label+' tools has transition', duration not in ('0s','0s, 0s'))
    await page.locator('#btnWorkMenu').click()
    check(label+' tools closes', await page.locator('#workMega').evaluate('(el)=>el.hidden'))
    # Divider icon is centered in each real boundary; disabled ones stay disabled.
    grip=await page.evaluate('''() => {
       const d=[...document.querySelectorAll('#kuxFocalDivider,.kux-grid-divider')].filter(x=>!x.hidden&&getComputedStyle(x).display!=='none');
       return {length:d.length,centered:d.every(x=>getComputedStyle(x).display==='grid'&&getComputedStyle(x).placeItems==='center'),
         patterns:d.map(x=>getComputedStyle(x,x.id==='kuxFocalDivider'?'::before':'::after').content)};
    }''')
    check(label+' divider geometry controls', (grip['length']>=1 and grip['centered']) if width>920 else (grip['length']==0 or grip['centered']))
    check(label+' divider dots', all('⋮' in x for x in grip['patterns']))
    # On real Canvas the tour moves through seven steps. Check motion and recovery.
    await page.locator('#btnWorkMenu').click()
    await page.locator('#btnHelpMobile').click()
    check(label+' Canvas tour open', await page.locator('#homeTourDialog').evaluate('(el)=>el.open'))
    check(label+' seven-step Canvas tour', '1 / 7' in await page.locator('#homeTourStep').inner_text())
    if not reduced:
        await page.wait_for_timeout(560)
        first=await page.locator('.kux-tour-ring').evaluate('(el)=>el.getBoundingClientRect().left')
        await page.locator('#homeTourNext').click()
        await page.wait_for_function("document.querySelector('.kux-tour-ring').getAnimations().length>0",timeout=1200)
        await page.wait_for_timeout(180)
        middle=await page.locator('.kux-tour-ring').evaluate('(el)=>el.getBoundingClientRect().left')
        await page.wait_for_timeout(520)
        final=await page.locator('.kux-tour-ring').evaluate('(el)=>el.getBoundingClientRect().left')
        check(label+' spotlight relocates', abs(first-final)>=3)
        check(label+' spotlight interpolates', min(first,final)-8<=middle<=max(first,final)+8 and abs(middle-first)>0.2 and abs(middle-final)>0.2)
    else:
        t=await page.locator('.kux-tour-ring').evaluate('(el)=>getComputedStyle(el).transitionDuration')
        check(label+' reduced motion has no spotlight transition', all(float(x.strip().replace('s',''))==0 for x in t.split(',')))
        await page.locator('#homeTourNext').click()
    check(label+' Canvas tour advances', '2 / 7' in await page.locator('#homeTourStep').inner_text())
    for n in range(3,8):
        await page.locator('#homeTourNext').click()
        check(label+f' Canvas tour step {n}', f'{n} / 7' in await page.locator('#homeTourStep').inner_text())
    await page.locator('#homeTourNext').click()
    check(label+' Canvas tour complete', not await page.locator('#homeTourDialog').evaluate('(el)=>el.open'))
    await page.wait_for_timeout(60)  # dialog close event restores spotlight/focus asynchronously
    check(label+' Canvas tour spotlight cleared', await page.locator('#kuxTourSpotlight').evaluate('(el)=>el.hidden'))
    check(label+' context unchanged by tour', await page.evaluate('KUXAIDemo.perception().view.context')=='poppa')
    # Input and state survive layout recomposition.
    await page.locator('#btnWorkMenu').click()
    await page.locator('#layoutTwo').click()
    check(label+' user layout still works', await page.evaluate('KUXAIDemo.perception().layout')=='split')
    await page.locator('#btnHome').click()
    check(label+' return home', await page.evaluate('KUXAIDemo.perception().screen')=='home')
    await page.locator('#startRecommended').click()
    check(label+' chosen layout survives Home', await page.evaluate('KUXAIDemo.perception().layout')=='split')
    doc_width=await page.evaluate('document.documentElement.scrollWidth')
    check(label+' no page-width overflow', doc_width<=width+4)

async def main():
  raw=FILE.read_bytes(); check('exact HTML SHA256',hashlib.sha256(raw).hexdigest()==EXPECTED)
  async with async_playwright() as p:
    b=await p.chromium.launch(headless=True,executable_path=os.getenv('KUX_CHROMIUM','/usr/bin/chromium'),args=['--no-sandbox'])
    for width,height,reduced in [(1715,935,False),(1280,900,True),(390,844,True)]:
       ctx=await b.new_context(viewport={'width':width,'height':height},reduced_motion='reduce' if reduced else 'no-preference')
       page=await ctx.new_page();page.set_default_timeout(9000)
       errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
       await page.set_content(raw.decode('utf-8'),wait_until='domcontentloaded')
       await exercise(page,width,height,reduced)
       check(f'{width}x{height}: JS page errors',not errors)
       ERRS.extend(errors)
       await ctx.close()
    await b.close()
  receipt={
    'schema':'kux.nautico.lab.v59.source-bound-chromium.v0.1','date':'2026-10-11',
    'source':'labs/nautico-ui-v4/21-griglia-perceptual-continuity-v59.html','source_sha256':EXPECTED,
    'method':'Chromium Playwright page.set_content (synthetic local UI; not hosted/runtime/Edge physical)',
    'check_count':len(CHECKS),'passed':len(CHECKS),'page_errors':ERRS,
    'viewports':['1715x935 normal','1280x900 reduced','390x844 reduced'],
    'checks':CHECKS,
    'not_exercised':['Edge physical device','touch physical gesture','screen reader','production host','real AI','Nautico domain controller','site deploy','session-restart persistence'],
  }
  RECEIPT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  print('PASS',len(CHECKS),'checks; page errors',len(ERRS),'SHA256',EXPECTED)

if __name__=='__main__': asyncio.run(main())
