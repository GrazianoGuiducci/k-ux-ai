"""Bounded 750ms opening-motion readback. Reduced motion remains immediate."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import hashlib, json
root=Path(__file__).resolve().parent.parent
path=root/'labs/nautico-ui-v4/25-griglia-rail-composer-v512.html'
data=path.read_bytes();sha=hashlib.sha256(data).hexdigest();assert sha=='1879dbe0d2ccba4c7db4701fe067c05ad1d20761aa2a6cf053f90b478118430b'
result=[]
def check(name,ok,extra=None):
    result.append({'name':name,'passed':bool(ok),'meta':extra})
    if not ok:raise AssertionError(f'{name} {extra}')
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 for motion in ['no-preference','reduce']:
  ctx=b.new_context(viewport={'width':1715,'height':913},reduced_motion=motion)
  page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(data.decode(),wait_until='domcontentloaded');page.locator('#startRecommended').click();page.wait_for_timeout(90)
  timing=lambda s:page.evaluate('''(s)=> [...document.querySelector(s).getAnimations()].map(a=>({name:a.animationName||a.id||'',duration:a.effect?.getTiming().duration,state:a.playState}))''',s)
  if motion=='no-preference':
   # Canvas direct and menu opening transitions.
   page.locator('#kuxContextTrigger').click();page.wait_for_timeout(70)
   durations=timing('#kuxContextChoices')
   check('context-menu-opening>=750',any(isinstance(x['duration'],(int,float)) and x['duration']>=750 for x in durations),durations)
   page.locator('#kuxContextTrigger').click();page.wait_for_timeout(50)
   page.locator('#btnWorkMenu').click();page.wait_for_timeout(70)
   durations=timing('#workMega')
   check('tools-opening>=750',any(isinstance(x['duration'],(int,float)) and x['duration']>=750 for x in durations),durations)
   page.locator('#btnWorkMenu').click();page.wait_for_timeout(50)
   page.locator('#btnQuickAdd').click();page.wait_for_timeout(70)
   durations=timing('#picker')
   check('picker-opening>=750',any(isinstance(x['duration'],(int,float)) and x['duration']>=750 for x in durations),durations)
   page.locator('#picker').evaluate('(e)=>e.close()');page.wait_for_timeout(80)
   page.locator('#railVisibility').click();page.locator('#activitiesEdge').click();page.wait_for_timeout(100)
   durations=timing('.intent-dock')
   check('activity-return>=750',any(x['name']=='kux-activity-return' and x['duration']>=750 for x in durations),durations)
   check('activity-shows-icons',page.locator('body').get_attribute('data-kux-activities')=='icons')
  else:
   page.locator('#railVisibility').click();page.locator('#activitiesEdge').click();page.wait_for_timeout(30)
   durations=timing('.intent-dock')
   check('reduce-motion-no-activity-reveal',not any(x['name']=='kux-activity-return' for x in durations),durations)
   check('reduce-motion-icons',page.locator('body').get_attribute('data-kux-activities')=='icons')
  check(f'{motion}:js-clean',len(errors)==0,errors)
  ctx.close()
 b.close()
report={'sha256':sha,'candidate':'v5.12 compatibility with v5.11','checks':result,'passed':len(result),'total':len(result),'method':'Chromium Playwright page.set_content; CSS/WAAPI opening durations measured on live DOM', 'notes':['750ms requirement applies to spatial/opening animation; immediate reduced-motion mode remains available','No physical Edge/browser assistive verification']}
(root/'labs/nautico-ui-v4/EVIDENCE_OPENING_MOTION_COMPAT_V512_20261011.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':len(result),'checks':[x['name'] for x in result]},indent=2))
