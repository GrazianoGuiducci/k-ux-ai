import asyncio,hashlib,json,tempfile
from pathlib import Path
from playwright.async_api import async_playwright
BASE=Path(__file__).resolve().parent.parent
SOURCE=BASE/'labs/nautico-ui-v4/17-griglia-situated-v55.html'
IMAGE_DIR=Path(tempfile.mkdtemp(prefix='kux-v55-qa-'))
CHECKS=[]
ERRORS=[]
def check(label,passed):
    if not passed: raise AssertionError(label)
    CHECKS.append(label)
async def inspect(page):
    return await page.evaluate('''()=>({
      mode:document.body.dataset.kuxAssistantMode,
      form:window.KUXAIDemo?.assistantModule()?.formOpen,
      layout:window.KUXAIDemo?.perception().layout,
      stage:document.querySelector('#workspaceStage').getBoundingClientRect().toJSON(),
      rail:document.querySelector('.intent-dock').getBoundingClientRect().toJSON(),
      secondary:document.querySelector('.kux-secondary-rail')?.getBoundingClientRect().toJSON(),
      frame:document.querySelector('.kux-surface-frame')?.getBoundingClientRect().toJSON(),
      main:document.querySelector('.work-main').getBoundingClientRect().toJSON(),
      topbar:document.querySelector('.topbar').getBoundingClientRect().toJSON(),
      divider:{medium:document.querySelector('#kuxMediumDivider').getBoundingClientRect().toJSON(),hidden:document.querySelector('#kuxMediumDivider').hidden,suspended:document.querySelector('#kuxMediumDivider').dataset.suspended||null},
      view:window.KUXAIDemo?.perception().view,
      panels:window.KUXAIDemo?.perception().panels.filter(p=>p.visibleInField).map(p=>({id:p.id,intent:p.intent,maximized:p.maximized}))
    })''')
async def drag(page,locator,dx,dy,steps=10):
    r=await locator.bounding_box()
    if not r:raise RuntimeError('Drag target not visible')
    x=r['x']+min(60,r['width']*.3); y=r['y']+r['height']*.5
    await page.mouse.move(x,y);await page.mouse.down();await page.mouse.move(x+dx,y+dy,steps=steps);await page.mouse.up()

async def prepare(page,mode='cantiere',activities=['fare','controllare','progettare','organizzare']):
    await page.locator(f'#homeContextOptions [data-context="{mode}"]').click()
    for intent in activities:
        selector=page.locator(f'#intentGrid [data-intent="{intent}"] .tile-open')
        if 'Seleziona' in await selector.inner_text() and 'Selezionata' not in await selector.inner_text(): await selector.click()
    await page.locator('#startRecommended').click()
    await page.wait_for_timeout(180)

async def main():
    source=SOURCE.read_text('utf-8')
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
        for width,height,reduced in [(1715,895,'no-preference'),(1300,900,'reduce'),(768,850,'no-preference'),(390,844,'reduce')]:
            ctx=await b.new_context(viewport={'width':width,'height':height},reduced_motion=reduced)
            pg=await ctx.new_page();pg.set_default_timeout(7000);errors=[];pg.on('pageerror',lambda e:errors.append(str(e)))
            await pg.set_content(source,wait_until='domcontentloaded');await pg.wait_for_timeout(70)
            label=f'{width}/{reduced}'
            check(label+':boot',await pg.evaluate('window.KUXAIDemo?.version')=='lab-2026-10-11-r5.5')
            check(label+':scope',await pg.locator('.kux-home-thesis').inner_text()=='UX-AI evolutiva e nuove possibilità')
            check(label+':link',await pg.locator('.kux-home-learn').get_attribute('href')=='https://github.com/GrazianoGuiducci/k-ux-ai/blob/main/MANIFESTO.md')
            await pg.locator('#homeTourButton').click()
            for i,t in enumerate(['Scegli il contesto','Prepara le attività','Entra nel campo operativo']):
                check(label+f':tour{i+1}',t==await pg.locator('#homeTourTitle').inner_text())
                if i<2:await pg.locator('#homeTourNext').click()
            await pg.locator('#homeTourNext').click()
            check(label+':tour-closed',not await pg.locator('#homeTourDialog').evaluate('(x)=>x.open'))
            await prepare(pg)
            check(label+':work',await pg.evaluate('window.KUXAIDemo.perception().screen')=='work')
            check(label+':5cards',len((await inspect(pg))['panels'])==5)
            if await pg.locator('#btnRecompose').is_visible(): await pg.locator('#btnRecompose').click()
            else:
                await pg.locator('#btnWorkMenu').click()
                await pg.locator('#menuRecompose').click()
            await pg.wait_for_timeout(930)
            a=await inspect(pg)
            if width>=1150 and a['divider']['medium']['width']:
                # check actual divider geometry
                check(label+':medium-inside-secondary',a['secondary']['x']-4<=a['divider']['medium']['x']<=a['secondary']['right']+6)
            check(label+':no-page-errors',not errors)
            if width==1715:
                await pg.screenshot(path=str(IMAGE_DIR/'v55-desktop.png'))
                # Global assistant: open then dock left while keeping the access rail visible.
                await pg.locator('.kux-surface-avatar').click();await pg.wait_for_timeout(180)
                check(label+':assistant-open',await pg.evaluate('window.KUXAIDemo.assistantSurface().open'))
                check(label+':form-hidden-default',await pg.evaluate('window.KUXAIDemo.assistantModule().formOpen')==False)
                await pg.locator('.kux-chat-tabs button').filter(has_text='Apri modulo').click()
                check(label+':form-open',await pg.evaluate('window.KUXAIDemo.assistantModule().formOpen'))
                await pg.locator('.kux-field textarea').fill('Bozza locale temporanea')
                await pg.locator('.kux-chat-tabs button').filter(has_text='Chiudi modulo').click()
                check(label+':form-closed',await pg.evaluate('window.KUXAIDemo.assistantModule().formOpen')==False)
                await pg.locator('.kux-chat-tabs button').filter(has_text='Apri modulo').click()
                check(label+':form-draft-retained',(await pg.locator('.kux-field textarea').input_value())=='Bozza locale temporanea')
                await pg.locator('.kux-chat-tabs button').filter(has_text='Chiudi modulo').click()
                await pg.locator('.kux-surface-toolbar button[title="Aggancia a sinistra"]').click();await pg.wait_for_timeout(700)
                geom=await inspect(pg)
                check(label+':dock-left',geom['mode']=='dock-left')
                check(label+':rail-exposed',geom['frame']['x']>=geom['rail']['x']+geom['rail']['width']-3)
                check(label+':chat-below-topbar',geom['frame']['y']>=geom['topbar']['y']+geom['topbar']['height']-3)
                check(label+':main-clear',geom['main']['x']>=geom['frame']['x']+geom['frame']['width']-4)
                await pg.screenshot(path=str(IMAGE_DIR/'v55-chat-dock-left.png'))
                # Back to floating. Then drag chat to top / full and back down.
                await pg.locator('.kux-surface-toolbar button[title="Ripristina finestra"]').click()
                await pg.wait_for_timeout(180)
                check(label+':floating',await pg.evaluate('window.KUXAIDemo.assistantSurface().mode')=='floating')
                chatHead=pg.locator('.kux-surface-header .kux-surface-heading')
                r=await chatHead.bounding_box();x=r['x']+90;y=r['y']+16
                await pg.mouse.move(x,y);await pg.mouse.down();await pg.mouse.move(x+35,50,steps=12);await pg.mouse.up();await pg.wait_for_timeout(140)
                check(label+':chat-drag-full',await pg.evaluate('window.KUXAIDemo.assistantSurface().mode')=='full')
                r=await chatHead.bounding_box();x=r['x']+90;y=r['y']+16
                await pg.mouse.move(x,y);await pg.mouse.down();await pg.mouse.move(x+25,y+85,steps=12);await pg.mouse.up();await pg.wait_for_timeout(110)
                check(label+':chat-drag-down-restores',await pg.evaluate('window.KUXAIDemo.assistantSurface().mode')=='floating')
                await pg.screenshot(path=str(IMAGE_DIR/'v55-chat-floating.png'))
                await pg.locator('.kux-surface-toolbar button[title="Riduci ad avatar"]').click();await pg.wait_for_timeout(200)
                # Single-card dialog is linked to that card, not cloned global assistant.
                card=pg.locator('.module[data-id]').filter(has=pg.locator('.module-title',has_text='Fare')).first
                await card.locator('[data-module-op="dialogue"]').click()
                check(label+':card-dialogue',await card.locator('.kux-section-surface').is_visible())
                check(label+':local-label','Dialogo della singola scheda' in await card.locator('.kux-section-surface').inner_text())
                await card.locator('.kux-section-editor').fill('Contesto locale della scheda')
                await card.locator('[data-section="ask"]').click()
                check(label+':local-response','Lettura dal caso demo' in await card.locator('.kux-section-messages').inner_text())
                # Slot drag into top-page full, then downward to restore chosen layout.
                await card.locator('[data-section="close"]').click()
                cardhead=card.locator('.module-head .module-heading')
                r=await cardhead.bounding_box();x=r['x']+40;y=r['y']+16
                await pg.mouse.move(x,y);await pg.mouse.down();await pg.mouse.move(x,52,steps=12);await pg.mouse.up();await pg.wait_for_timeout(900)
                check(label+':card-drag-full',any(p['intent']=='fare' and p['maximized'] for p in (await inspect(pg))['panels']))
                r=await cardhead.bounding_box();x=r['x']+38;y=r['y']+16
                await pg.mouse.move(x,y);await pg.mouse.down();await pg.mouse.move(x+18,y+105,steps=12);await pg.mouse.up();await pg.wait_for_timeout(150)
                # No debug snapshot needed once confirmed
                check(label+':card-drag-down-restores',not any(p['intent']=='fare' and p['maximized'] for p in (await inspect(pg))['panels']))
                check(label+':layout-stable',await pg.evaluate('window.KUXAIDemo.perception().layout')=='auto')
                await pg.screenshot(path=str(IMAGE_DIR/'v55-after-drag.png'))
            ERRORS.extend(f'{label}: {e}' for e in errors)
            await ctx.close()
        await b.close()
    result={'version':'5.5','passed':len(CHECKS),'checks':CHECKS,'page_errors':ERRORS,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest()}
    (BASE/'labs/nautico-ui-v4/EVIDENCE_SITUATED_V55_20261011.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
    print('PASS',len(CHECKS),'ERRORS',ERRORS)
if __name__=='__main__':asyncio.run(main())
