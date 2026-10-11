"""K-UX-AI v5.9: exact-source Chromium checks for compact Activity rail and Home copy.

Requires Python Playwright and Chromium. Does not prove Edge, live AI, an
integrated nautical host, or a server-side authorization model.
"""
from __future__ import annotations
import asyncio, json, hashlib, os
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[1]
HTML=ROOT/'labs/nautico-ui-v4/21-griglia-perceptual-continuity-v59.html'
EXPECTED='463d9d436ab982f4ab68ec0cd2b8770813d0346ecd26bf90b9335f0e0b57ed3a'
CHECKS=[]
ERRORS=[]
def check(label,condition):
    if not condition: raise AssertionError('FAIL '+label)
    CHECKS.append(label)
async def rail(page):
    return await page.evaluate('''() => {const root=document.querySelector('.intent-dock'),hd=root.querySelector('.kux-rail-head');return {
       mode:document.body.dataset.kuxActivities, expanded:document.body.dataset.kuxRailExpanded,
       title:hd?.querySelector('.dock-caption')?.textContent, allButtons:[...hd.querySelectorAll('button')].map(b=>b.id),
       visibleButtons:[...hd.querySelectorAll('button')].filter(b=>getComputedStyle(b).display!=='none').map(b=>b.id),
       headerHeight:hd?.getBoundingClientRect().height, railWidth:root.getBoundingClientRect().width,
       countPresent:!!document.querySelector('#activityCount'), inert:root.inert,
       detailShown:!!root.querySelector('.kux-avatar-detail')&&getComputedStyle(root.querySelector('.kux-avatar-detail')).display!=='none',
       icons:root.querySelectorAll('#avatarDock .avatar-entry').length, navHidden:root.hidden,
       edgeVisible:getComputedStyle(document.querySelector('#activitiesEdge')).display!=='none',
       ariaLabel:root.getAttribute('aria-label'), railControlsLabel:hd?.getAttribute('aria-label')
    };}''')

async def run():
    raw=HTML.read_bytes();digest=hashlib.sha256(raw).hexdigest()
    check('candidate exact sha256',digest==EXPECTED)
    browser_location=os.environ.get('KUX_CHROMIUM') or ('/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None)
    async with async_playwright() as p:
        browser=await p.chromium.launch(headless=True,executable_path=browser_location,args=['--no-sandbox'])
        cases=[(1715,930,'no-preference'),(1280,900,'reduce'),(768,900,'no-preference'),(390,844,'reduce')]
        for w,h,motion in cases:
            ctx=await browser.new_context(viewport={'width':w,'height':h},reduced_motion=motion)
            page=await ctx.new_page();page.set_default_timeout(8000)
            errors=[];page.on('pageerror',lambda x:errors.append(str(x)))
            key=f'{w}x{h}/{motion}'
            await page.set_content(raw.decode('utf-8'),wait_until='domcontentloaded')
            await page.wait_for_timeout(90)
            check(key+' home visible',await page.evaluate('KUXAIDemo.perception().screen')=='home')
            check(key+' version',await page.evaluate('KUXAIDemo.version')=='lab-2026-10-11-r5.9')
            check(key+' heading',await page.locator('#homeTitle').inner_text()=='Kernel UX-AI')
            check(key+' subheading',await page.locator('.kux-home-thesis').inner_text()=='per l’interazione in Sistemi Intelligenti.')
            story=await page.locator('.kux-home-story').inner_text()
            for part in ['Il progetto K-UX-AI fornisce', 'sistemi agentici complessi','impara e si adatta', 'mantiene la continuità operativa','Scegli il punto di ingresso', 'notifica pertinente', 'prototipo con dati dimostrativi']:
                check(key+' copy '+part,part in story)
            check(key+' manifesto',await page.locator('.kux-home-learn').get_attribute('href')=='https://github.com/GrazianoGuiducci/k-ux-ai/blob/main/MANIFESTO.md')
            check(key+' five contexts',await page.locator('#homeContextOptions button').count()==5)
            check(key+' ten home intents',await page.locator('#intentGrid .intent-tile').count()==10)
            check(key+' no horizontal document overflow',await page.evaluate('document.documentElement.scrollWidth <= window.innerWidth+3'))
            check(key+' enter enabled',await page.locator('#startRecommended').is_enabled())
            await page.locator('#startRecommended').click();await page.wait_for_timeout(130 if motion=='reduce' else 800)
            check(key+' canvas',await page.evaluate('KUXAIDemo.perception().screen')=='work')
            check(key+' ten rail intents',await page.evaluate('KUXAIDemo.activityRail().visibleIntents.length')==10)
            check(key+' no rail counter',await page.locator('#activityCount').count()==0)
            check(key+' only one rail head',await page.locator('.intent-dock .kux-rail-head').count()==1)
            check(key+' two head buttons',set((await rail(page))['allButtons'])=={'railVisibility','kuxRailToggle'})
            check(key+' no inherited context label in rail header',await page.locator('.kux-rail-head .kux-dock-context').count()==0)
            check(key+' header height compact',(await rail(page))['headerHeight']<=38)
            if w>760:
                info=await rail(page)
                check(key+' starts icons',info['mode']=='icons' and info['expanded']=='false')
                check(key+' two visible controls',info['visibleButtons']==['railVisibility','kuxRailToggle'])
                check(key+' icon header no redundant label',not await page.locator('.kux-rail-head .dock-caption').is_visible())
                check(key+' initial no details',not info['detailShown'])
                await page.locator('#kuxRailToggle').click();await page.wait_for_timeout(80)
                info=await rail(page)
                check(key+' click previews',info['mode']=='previews' and info['expanded']=='true')
                check(key+' previews has label',await page.locator('.kux-rail-head .dock-caption').is_visible())
                check(key+' previews has both buttons',info['visibleButtons']==['railVisibility','kuxRailToggle'])
                check(key+' previews show detail',info['detailShown'])
                check(key+' previews after-click not overlay',info['railWidth']>=250)
                await page.locator('#kuxRailToggle').click();await page.wait_for_timeout(80)
                info=await rail(page)
                check(key+' click back icons',info['mode']=='icons' and info['expanded']=='false')
                await page.locator('#kuxRailToggle').click();await page.wait_for_timeout(80)
                await page.locator('#railVisibility').click();await page.wait_for_timeout(100)
                info=await rail(page)
                check(key+' hide from previews collapses source',info['mode']=='hidden' and info['expanded']=='false' and info['inert'])
                check(key+' edge visible hidden',info['edgeVisible'])
                await page.locator('#activitiesEdge').hover();await page.wait_for_timeout(90)
                info=await rail(page)
                check(key+' hover reveals icons only',info['mode']=='peek' and info['expanded']=='false' and not info['detailShown'])
                check(key+' transient one control',info['visibleButtons']==['railVisibility'])
                await page.locator('#activitiesEdge').click();await page.wait_for_timeout(75)
                info=await rail(page)
                check(key+' edge click pins icons',info['mode']=='icons' and info['expanded']=='false')
                check(key+' two buttons return',info['visibleButtons']==['railVisibility','kuxRailToggle'])
                check(key+' controls respond to keyboard',await page.locator('#kuxRailToggle').is_enabled() and await page.locator('#railVisibility').is_enabled())
            else:
                check(key+' rail hidden on narrow',not await page.locator('.intent-dock').is_visible())
                check(key+' assistant still available',await page.evaluate('!!document.getElementById("assistantOrb")'))
            check(key+' no JS errors',not errors)
            ERRORS.extend(errors)
            await ctx.close()
        # Extra state continuity and keyboard. Pinned state must not require pointer hover.
        ctx=await browser.new_context(viewport={'width':1440,'height':900},reduced_motion='reduce')
        page=await ctx.new_page(); errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        await page.set_content(raw.decode('utf-8'),wait_until='domcontentloaded')
        await page.locator('#startRecommended').click()
        await page.locator('#kuxRailToggle').focus();await page.keyboard.press('Enter')
        check('keyboard opens previews',(await rail(page))['mode']=='previews')
        await page.keyboard.press('Enter')
        check('keyboard closes previews',(await rail(page))['mode']=='icons')
        await page.locator('#kuxRailToggle').click()
        await page.locator('#railVisibility').focus();await page.keyboard.press('Enter')
        check('keyboard hides whole rail',(await rail(page))['mode']=='hidden')
        await page.locator('#activitiesEdge').focus();await page.keyboard.press('Enter')
        check('keyboard restores icons',(await rail(page))['mode']=='icons')
        await page.locator('#kuxContextTrigger').click()
        await page.locator('#kuxContextChoices [data-work-context="cantiere"]').click()
        check('switch context retained',await page.evaluate('KUXAIDemo.perception().view.context')=='cantiere')
        check('header contextual aria', 'Cantiere' in (await rail(page))['ariaLabel'])
        await page.locator('#btnWorkMenu').click()
        await page.locator('#btnHelpMobile').click()
        check('canvas tour still available',await page.evaluate('KUXAIDemo.tour().open && KUXAIDemo.tour().kind==="work"'))
        await page.locator('#homeTourClose').click()
        check('tour close preserves canvas',await page.evaluate('!KUXAIDemo.tour().open && KUXAIDemo.perception().screen==="work"'))
        check('keyboard context errors',not errors);ERRORS.extend(errors)
        await ctx.close();await browser.close()
    receipt={'schema':'kux.ui-lab.v59.reexercise-v58-rail-home.receipt.v1','source_sha256':digest,'browser':'Chromium headless, Python Playwright, page.set_content','correlated':True,'passed':len(CHECKS),'total':len(CHECKS),'checks':CHECKS,'page_errors':ERRORS,'viewport_modes':['1715x930 normal','1280x900 reduced','768x900 normal','390x844 reduced','1440x900 keyboard/reduced'],'unverified':['installed Edge and file:// behavior','live Nautico controllers or assistant','user reading comprehension','screen reader and physical touch','public release or MAIOS site integration']}
    dest=ROOT/'labs/nautico-ui-v4/EVIDENCE_RAIL_HOME_V59_20261011.json';dest.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    print(f'PASS {len(CHECKS)}/{len(CHECKS)} Chromium checks, {len(ERRORS)} page errors; SHA256 {digest}')

if __name__=='__main__':asyncio.run(run())
