"""Source-pinned Chromium checks for v5.11. Synthetic UI only; no external receivers."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import hashlib, json, time
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'labs/nautico-ui-v4/24-griglia-content-hierarchy-v511.html'
SHA256='67e8a1104d2abd66b886fad5354753a4db8964321c93947937de15f1917f434a'
html=PATH.read_bytes(); sha=hashlib.sha256(html).hexdigest(); assert sha==SHA256, sha
checks=[]; samples=[]
def check(key,okay):
    checks.append({'name':key,'passed':bool(okay)})
    if not okay:raise AssertionError(key)
views=[(1715,913,'no-preference'),(1366,768,'no-preference'),(768,900,'reduce'),(390,844,'reduce')]
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
    for w,h,motion in views:
        context=browser.new_context(viewport={'width':w,'height':h},reduced_motion=motion)
        page=context.new_page();errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
        page.set_content(html.decode('utf-8'),wait_until='domcontentloaded')
        page.wait_for_timeout(110 if motion=='reduce' else 950)
        prefix=f'{w}x{h}-{motion}'
        check(prefix+':home',page.evaluate('window.KUXAIDemo?.perception().screen')=='home')
        check(prefix+':home-ten',page.locator('#intentGrid .intent-tile').count()==10)
        check(prefix+':home-no-overflow',page.evaluate('document.documentElement.scrollWidth <= window.innerWidth+1'))
        for intent in ['fare','controllare','organizzare','esplorare']:
            page.locator(f'#intentGrid .intent-tile[data-intent="{intent}"] .tile-open').click()
        page.locator('#startRecommended').click()
        page.wait_for_timeout(110 if motion=='reduce' else 900)
        check(prefix+':canvas',page.evaluate('window.KUXAIDemo.perception().screen')=='work')
        check(prefix+':five-panels',page.locator('.workspace-stage .module:not([hidden])').count()==5)
        # Verify semantic reading structure and compact source provenance for each active panel.
        cards=page.evaluate('''() => [...document.querySelectorAll('.workspace-stage .module:not([hidden])')].map(m=>{
          const b=m.querySelector('.module-content');const first=[...b.children].slice(0,5);
          const caps=b.querySelector(':scope > .kux-context-capsule.kux-provenance');
          const h=m.querySelector('.module-head');const label=m.querySelector('.module-heading');
          return {hDisplay:getComputedStyle(h).display,hHeight:h.getBoundingClientRect().height,
            section:m.querySelector('.module-section').textContent,action:m.querySelector('.module-action').textContent,
            title:m.querySelector('.module-title').textContent,first:first.map(e=>e.tagName),
            introLabel:first[0]?.textContent,headline:first[1]?.textContent,
            sourceVisible:!!caps&&!caps.open,sourceSummary:caps?.querySelector('summary')?.textContent,
            sourceDetails:caps?.querySelector('.kux-source-limit')?.textContent,
            leadBeforeSource:first.indexOf(caps)>1,duplicateSourceCount:b.querySelectorAll(':scope > .kux-context-capsule.kux-provenance').length};
        })''')
        check(prefix+':headers-in-one-row',all(c['hDisplay']=='flex' and c['hHeight']<=80 for c in cards))
        check(prefix+':header-has-context-action',all(bool(c['section'] and c['action'] and c['title']) for c in cards))
        check(prefix+':body-starts-with-semantic-label',all(c['first'][0]=='DIV' and c['first'][1]=='H3' for c in cards))
        check(prefix+':provenance-follows-work',all(c['leadBeforeSource'] for c in cards))
        check(prefix+':single-provenance',all(c['duplicateSourceCount']==1 and c['sourceVisible'] for c in cards))
        check(prefix+':provenance-real-limit',all('controller del contesto' in c['sourceDetails'] and 'KN/' in c['sourceSummary'] for c in cards))
        if w>=1024:
            first=page.locator('.module:not([hidden]) .kux-provenance').first
            check(prefix+':disclosure-closed',first.get_attribute('open') is None)
            first.locator('summary').click()
            check(prefix+':disclosure-expand',first.get_attribute('open') is not None)
            first.locator('summary').click()
            check(prefix+':disclosure-collapse',first.get_attribute('open') is None)
            # Close a nonfocused card by two explicit sequential clicks on its Activity icon.
            focusBefore=page.evaluate('window.KUXAIDemo.perception().focus')
            selected=page.evaluate('''() => {const ps=window.KUXAIDemo.perception().panels.filter(p=>p.visibleInField);return ps.map(p=>({intent:p.intent,id:p.id}));}''')
            # Always choose a non-focused intent; its close must update the active toggle regardless of focus.
            target=next(x for x in selected if x['id']!=focusBefore and x['intent']!='capire')
            item=page.locator(f'.avatar-entry[data-intent="{target["intent"]}"] .avatar-button')
            check(prefix+':activity-open-before',item.get_attribute('data-active')=='true')
            item.click();check(prefix+':double-click-armed',item.get_attribute('data-confirm-close')=='true')
            item.click();page.wait_for_timeout(90)
            check(prefix+':activity-off-after',item.get_attribute('data-active')=='false')
            check(prefix+':activity-not-in-canvas',not any(x['intent']==target['intent'] and x['visibleInField'] for x in page.evaluate('window.KUXAIDemo.perception().panels')))
        if w==1715:
            page.locator('#railVisibility').click()
            check(prefix+':rail-hidden',page.locator('body').get_attribute('data-kux-activities')=='hidden')
            page.locator('#activitiesEdge').click()
            check(prefix+':rail-restored',page.locator('body').get_attribute('data-kux-activities')=='icons')
            animations=page.evaluate('''() => document.querySelector('.intent-dock').getAnimations().map(a=>({id:a.id,duration:a.effect?.getTiming().duration,phase:a.effect?.getComputedTiming().progress}))''')
            check(prefix+':rail-return-duration',any(a['id']=='kux-activity-return' and a['duration']>=750 for a in animations))
            samples.append({'viewport':prefix,'rail_animation':animations})
            page.screenshot(path=str(ROOT/'labs/nautico-ui-v4/QA_v511_canvas.png'),animations='disabled')
        check(prefix+':no-js-errors',len(errors)==0)
        if errors:samples.append({'viewport':prefix,'errors':errors})
        context.close()
    browser.close()
report={'candidate':'v5.11','source_sha256':sha,'method':'Playwright Chromium page.set_content; local synthetic Nautico UI','checks_passed':len(checks),'checks_total':len(checks),'all_passed':all(c['passed'] for c in checks),'checks':checks,'samples':samples,'viewports':[f'{w}x{h}-{m}' for w,h,m in views], 'limits':['Not Edge physical browser','Not real Nautico or MAIOS site','No server permissions/AI provider','Reduced-motion is an alternate final state, not a 750ms requirement','No full accessibility audit']}
(ROOT/'labs/nautico-ui-v4/EVIDENCE_CONTENT_RAIL_V511_20261011.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('checks','samples')},ensure_ascii=False,indent=2))
