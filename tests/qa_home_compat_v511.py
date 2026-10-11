"""Bounded K-UX-AI v5.10.1 home-balance regression, Chromium/Playwright.
Uses exact candidate HTML and page.set_content; no real Nautico/site integration.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json, hashlib

root=Path(__file__).resolve().parent.parent
p=root/'labs/nautico-ui-v4/24-griglia-content-hierarchy-v511.html'
source=p.read_bytes(); sha=hashlib.sha256(source).hexdigest(); assert sha=='67e8a1104d2abd66b886fad5354753a4db8964321c93947937de15f1917f434a',sha
views=[(1715,842,'reduce'),(1715,913,'no-preference'),(1440,900,'reduce'),(1280,800,'reduce'),(1160,780,'reduce'),(1050,800,'reduce'),(390,844,'reduce')]
checks=[]; summaries=[]
def check(label, condition):
    checks.append({'name':label,'passed':bool(condition)})
    if not condition: raise AssertionError(label)
with sync_playwright() as playwright:
    b=playwright.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    for w,h,motion in views:
        c=b.new_context(viewport={'width':w,'height':h},reduced_motion=motion)
        page=c.new_page();errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
        page.set_content(source.decode('utf-8'),wait_until='domcontentloaded');page.wait_for_timeout(950 if motion=='no-preference' else 190)
        data=page.evaluate('''() => {
          const rect=s=>{const e=document.querySelector(s);const r=e?.getBoundingClientRect();return r?{width:r.width,top:r.top,height:r.height,bottom:r.bottom}:null};
          const grid=document.querySelector('#intentGrid');
          const ts=[...grid.querySelectorAll('.intent-tile')];
          return {
            story:rect('.kux-home-story'),panel:rect('.kux-home-setup'),intro:rect('.home-intro'),grid:rect('#intentGrid'),
            title:document.title, count:ts.length,
            buttons:ts.map(t=>{
              const tr=t.getBoundingClientRect(),b=t.querySelector('.tile-open').getBoundingClientRect();
              return {id:t.dataset.intent,visibleWithinCard:b.bottom<=tr.bottom+2,dist:b.bottom-tr.bottom};
            }),
            gridScrollHeight:grid.scrollHeight,gridClientHeight:grid.clientHeight,
            bodyScrollHeight:document.body.scrollHeight,scrollWidth:document.documentElement.scrollWidth,
            viewHeight:innerHeight,contexts:[...document.querySelectorAll('#homeContextOptions button')].length,
            fit:document.querySelector('.home-screen')?.dataset.fit
          };
        }''')
        prefix=f'{w}x{h}-{motion}'
        check(prefix+':no_js_errors',len(errors)==0)
        check(prefix+':ten_tiles',data['count']==10)
        check(prefix+':five_context_choices',data['contexts']==5)
        check(prefix+':no_horizontal_overflow',data['scrollWidth']<=w+1)
        check(prefix+':controls_inside_tile',all(x['visibleWithinCard'] for x in data['buttons']))
        if w>=1051:
            check(prefix+':copy_wider_than_setup',data['story']['width']>data['panel']['width']-1)
            check(prefix+':setup_minimum_width',data['panel']['width']>=510-1)
            check(prefix+':grid_scroll_or_fit',data['gridScrollHeight']>=data['gridClientHeight'])
            check(prefix+':bottom_within_viewport',data['grid']['bottom']<=h+1)
        if w==1050:
            check(prefix+':tablet_document_reflow',data['bodyScrollHeight']>h)
            check(prefix+':tablet_tiles_readable',all(x['visibleWithinCard'] for x in data['buttons']))
        if w==390:
            check(prefix+':mobile_document_scroll',data['bodyScrollHeight']>h)
            check(prefix+':mobile_tiles_readable',all(x['visibleWithinCard'] for x in data['buttons']))
        if w==1715 and h==842:
            check(prefix+':short_viewport_grid_scrolls',data['gridScrollHeight']>data['gridClientHeight']+20)
            page.screenshot(path=str(root/'labs/nautico-ui-v4/QA_v511_Home_1715x842.png'),animations='disabled')
        if w==1440:
            page.screenshot(path=str(root/'labs/nautico-ui-v4/QA_v511_Home_1440x900.png'),animations='disabled')
        if w==390:
            page.screenshot(path=str(root/'labs/nautico-ui-v4/QA_v511_Home_390x844.png'),animations='disabled')
        last=page.locator('#intentGrid .intent-tile').last
        before=last.locator('.tile-open').get_attribute('aria-pressed')
        last.locator('.tile-open').click()
        after=page.locator('#intentGrid .intent-tile').last.locator('.tile-open').get_attribute('aria-pressed')
        check(prefix+':last_card_action_reachable',after is not None and before!=after)
        summaries.append({'viewport':prefix,'left_width':round(data['story']['width']),'setup_width':round(data['panel']['width']),'intro_height':round(data['intro']['height']),'grid_scroll_height':data['gridScrollHeight'],'grid_client_height':data['gridClientHeight'],'page_scroll_height':data['bodyScrollHeight']})
        c.close()
    b.close()
report={'candidate':'v5.11, v5.10.1 Home compatibility','sha256':sha,'method':'Playwright Chromium page.set_content, headless, local synthetic demo','passed':sum(x['passed'] for x in checks),'total':len(checks),'all_passed':all(x['passed'] for x in checks),'checks':checks,'measurements':summaries,'unverified':['Edge physical browser','live Nautico kernel','site deployment','screen-reader accessibility','multi-session persistence']}
(root/'labs/nautico-ui-v4/EVIDENCE_HOME_COMPAT_V511_20261011.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n','utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('checks',)},indent=2,ensure_ascii=False))
