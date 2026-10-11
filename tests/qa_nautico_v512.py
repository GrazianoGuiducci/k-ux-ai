"""K-UX-AI v5.12: real browser rail-pinning and one-line chat composer regressions.

Synthetic browser-local laboratory only; host permissions, live AI and Nautico
controller are not exercised.
"""
from __future__ import annotations
import json,hashlib
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent.parent
FILE=ROOT/'labs/nautico-ui-v4/25-griglia-rail-composer-v512.html'
EXPECTED='1879dbe0d2ccba4c7db4701fe067c05ad1d20761aa2a6cf053f90b478118430b'
data=FILE.read_bytes();digest=hashlib.sha256(data).hexdigest()
if EXPECTED!='1879dbe0d2ccba4c7db4701fe067c05ad1d20761aa2a6cf053f90b478118430b': assert digest==EXPECTED, digest
checks=[]; samples=[]
def check(name,condition,detail=None):
    checks.append({'name':name,'passed':bool(condition)})
    if not condition: raise AssertionError(f'{name}: {detail}')

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    for width,height,motion in [(1715,913,'no-preference'),(1366,768,'no-preference'),(1715,913,'reduce'),(390,844,'reduce')]:
        ctx=browser.new_context(viewport={'width':width,'height':height},reduced_motion=motion)
        page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content(data.decode('utf-8'),wait_until='domcontentloaded')
        page.wait_for_timeout(65 if motion=='reduce' else 850)
        label=f'{width}x{height}-{motion}'
        check(label+':version',page.evaluate('window.KUXAIDemo.version')=='lab-2026-10-11-r5.12')
        check(label+':home-activities',page.locator('#intentGrid .intent-tile').count()==10)
        page.locator('#startRecommended').click()
        page.wait_for_timeout(75 if motion=='reduce' else 790)
        check(label+':canvas',page.locator('body').get_attribute('data-kux-screen')=='work')
        if width>=1024:
            # Start from a known state; moving onto the label displays a transient icon rail.
            page.locator('#railVisibility').click()
            check(label+':hidden',page.locator('body').get_attribute('data-kux-activities')=='hidden')
            edge=page.locator('#activitiesEdge');edge.hover()
            page.wait_for_timeout(110 if motion=='no-preference' else 30)
            check(label+':peek',page.locator('body').get_attribute('data-kux-activities')=='peek')
            check(label+':peek-icons-visible',page.locator('.intent-dock .avatar-button').count()==10)
            page.evaluate('''() => {const rail=document.querySelector('.intent-dock');window.__pinCarrier=rail.querySelector('.avatar-button');window.__pinAnim=rail.getAnimations().find(a=>a.id==='kux-activity-return');window.__pinAnimTime=window.__pinAnim?.currentTime??null;}''')
            if motion=='no-preference':
                check(label+':hover-animation-present',page.evaluate('!!window.__pinAnim'))
                check(label+':hover-animation-860',page.evaluate('window.__pinAnim.effect.getTiming().duration===860'))
            else:
                check(label+':reduce-no-hover-motion',page.evaluate('!window.__pinAnim'))
            edge.click()
            check(label+':pins-icons',page.locator('body').get_attribute('data-kux-activities')=='icons')
            check(label+':focus-restored',page.evaluate("document.activeElement?.id==='railVisibility'"))
            check(label+':same-icon-DOM',page.evaluate("document.querySelector('.intent-dock .avatar-button')===window.__pinCarrier"))
            check(label+':no-second-reveal',page.evaluate('''() => {
              const a=document.querySelector('.intent-dock').getAnimations().find(a=>a.id==='kux-activity-return');
              return (window.__pinAnim===undefined||window.__pinAnim===null)?!a:a===window.__pinAnim&&a.currentTime>=window.__pinAnimTime;
            }'''))
            check(label+':edge-disappears',not edge.is_visible())
            if motion=='no-preference':
                page.wait_for_timeout(120)
                check(label+':hover-motion-continues',page.evaluate("window.__pinAnim.currentTime>window.__pinAnimTime"))
            # Pinned state must behave exactly like an intentional icon rail.
            toggle=page.locator('#kuxRailToggle')
            toggle.click()
            check(label+':can-expand-previews',page.locator('body').get_attribute('data-kux-activities')=='previews')
            toggle.click()
            check(label+':can-collapse-previews',page.locator('body').get_attribute('data-kux-activities')=='icons')
            samples.append({'viewport':label,'pin_carrier_kept':True})
        if width!=1366:
            avatar=page.locator('.kux-rail-footer .kux-surface-avatar').first if width>760 else page.locator('.mobile-assistant-slot .kux-surface-avatar').first
            if not avatar.count() or not avatar.is_visible():
                avatar=page.locator('.kux-surface-avatar').first
            avatar.click()
            page.wait_for_timeout(80 if motion=='reduce' else 820)
            entry=page.locator('.kux-chat-inputrow textarea')
            check(label+':chat-visible',entry.is_visible())
            initial=entry.evaluate('''e=>({rows:e.rows,value:e.value,placeholder:e.placeholder,rect:e.getBoundingClientRect().height})''')
            check(label+':one-row-empty',initial['rows']==1 and initial['value']=='' and initial['placeholder']=='',initial)
            check(label+':one-row-height',40<=initial['rect']<=52,initial)
            gap=page.evaluate('''() => {const q=document.querySelector('.kux-chat-quick'),i=document.querySelector('.kux-chat-inputrow');return i.getBoundingClientRect().top-q.getBoundingClientRect().bottom;}''')
            check(label+':starter-separation',gap>=(12 if width<=470 else 17),gap)
            check(label+':send-control-reachable',page.locator('.kux-chat-inputrow button').is_visible())
            check(label+':no-chat-horizontal-overflow',page.evaluate('''()=>{const row=document.querySelector('.kux-chat-inputrow');return row.scrollWidth<=row.clientWidth+2;}'''))
            entry.fill('Primo messaggio\nSeconda riga\nTerza riga')
            grown=entry.evaluate('(e)=>e.getBoundingClientRect().height')
            check(label+':multiline-autogrow',grown>initial['rect']+14,{'before':initial['rect'],'after':grown})
            page.locator('.kux-chat-inputrow button').click()
            page.wait_for_timeout(180)
            after=entry.evaluate('''e=>({value:e.value,height:e.getBoundingClientRect().height})''')
            check(label+':resets-after-send',after['value']=='' and after['height']<=initial['rect']+2,after)
            check(label+':local-message-readback',page.locator('.kux-chat-msg[data-role="operator"]').count()>=1)
            samples.append({'viewport':label,'composer_at_rest':initial,'grown':grown,'gap':gap})
        check(label+':no-page-errors',not errors,errors)
        ctx.close()
    browser.close()

report={'candidate':'v5.12','sha256':digest,'method':'Chromium Playwright page.set_content on pinned candidate','passed':len(checks),'total':len(checks),'all_passed':all(x['passed'] for x in checks),'checks':checks,'samples':samples,'scope':['Single-line empty composer, growing/shrinking textarea, send and starter spacing','Hover-to-pinned rail continuity with identical carrier and animation identity','Reduced-motion remains instantaneous','No real Nautico or AI provider, no physical Edge']}
out=ROOT/'labs/nautico-ui-v4/EVIDENCE_PEEK_PIN_CHAT_V512_20261011.json'
out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('checks','samples')},indent=2,ensure_ascii=False))
