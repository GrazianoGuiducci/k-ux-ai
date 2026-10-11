"""Build K-UX-AI v5.6 from the exact v5.5 synthetic prototype.

Run: python tools/build_nautico_v56.py [--check]
The previous artifact is retained and never edited by this builder.
"""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / 'labs/nautico-ui-v4/17-griglia-situated-v55.html'
OUT = ROOT / 'labs/nautico-ui-v4/18-griglia-situated-v56.html'
BASE_SHA = 'd5a87e294d6fea395664d258d65c9a40f4c94d190bb807177146bd7301432d1c'

CSS = '''
/* v5.6 — home header is a simple entry, not a duplicate context/status surface. */
body[data-kux-screen="home"] .top-center,body[data-kux-screen="home"] .demo-tag{display:none!important}
body[data-kux-screen="home"] .topbar{justify-content:space-between}
/* The ten original intentions stay reachable within one vertically scrollable rail. */
body[data-kux-screen="work"] .intent-dock{transition:width .16s ease,flex-basis .16s ease}
.kux-activity-toggle{flex:0 0 auto;display:grid;place-items:center;min-height:26px;width:40px;border:1px solid var(--line);border-radius:7px;background:var(--surface);color:var(--ink);font-size:16px;padding:2px;margin-bottom:0}
.kux-dock-count{display:block;white-space:normal;max-width:75px;text-align:center;line-height:1.25;font-size:9px;font-weight:650;color:var(--muted);margin:0 auto 4px}
.kux-activity-edge{display:none;position:fixed;z-index:10008;left:0;top:33%;width:22px;min-height:111px;padding:9px 2px;background:#d6eee3;color:#143f38;border:1px solid #5da997;border-left:0;border-radius:0 12px 12px 0;box-shadow:2px 3px 12px #173b3944;writing-mode:vertical-rl;font-size:11px;font-weight:800;cursor:pointer}
body[data-kux-screen="work"][data-kux-activities="hidden"] .intent-dock{flex:0 0 0!important;width:0!important;min-width:0!important;max-width:0!important;padding:0!important;border:0!important;overflow:hidden!important;visibility:hidden}
body[data-kux-screen="work"][data-kux-activities="hidden"] .kux-activity-edge{display:block}
body[data-kux-screen="work"][data-kux-activities="peek"] .kux-activity-edge{display:block;left:86px}
body[data-kux-screen="work"][data-kux-activities="peek"] .intent-dock{position:fixed!important;z-index:10007!important;left:0!important;top:var(--kux-assistant-top,69px)!important;bottom:0!important;height:auto!important;visibility:visible!important;width:86px!important;min-width:86px!important;max-width:86px!important;flex:0 0 86px!important;box-shadow:6px 0 18px #14363836}
/* A full card uses the area next to the activity rail; the rail never overlays its text. */
body[data-kux-screen="work"][data-fullscreen-panel="true"] .intent-dock{position:fixed!important;z-index:10003!important;left:0!important;top:0!important;bottom:0!important;height:100dvh!important;visibility:visible}
body[data-kux-screen="work"][data-fullscreen-panel="true"][data-kux-activities="hidden"] .intent-dock{visibility:hidden!important}
body[data-kux-screen="work"][data-fullscreen-panel="true"][data-kux-activities="peek"] .intent-dock{top:0!important;height:100dvh!important}
body[data-kux-screen="work"][data-fullscreen-panel="true"] .workspace-stage .module[data-placement="full"]{left:var(--kux-full-rail,86px)!important;width:calc(100vw - var(--kux-full-rail,86px))!important;right:0!important;top:0!important;height:100dvh!important}
body[data-kux-screen="work"][data-kux-activities="hidden"] .workspace-stage .module[data-placement="full"],body[data-kux-screen="work"][data-kux-activities="peek"] .workspace-stage .module[data-placement="full"]{left:0!important;width:100vw!important}
body[data-kux-screen="work"] #assistantOrb{display:none!important}
body[data-kux-screen="work"][data-kux-activities="hidden"] .kux-surface-root>.kux-surface-avatar{left:28px!important;right:auto!important;bottom:18px!important}
@media(max-width:760px){body[data-kux-screen="work"] .kux-activity-edge{display:none!important}body[data-kux-screen="work"][data-fullscreen-panel="true"] .intent-dock{display:none!important}body[data-kux-screen="work"][data-fullscreen-panel="true"] .workspace-stage .module[data-placement="full"]{left:0!important;width:100vw!important}}
@media(prefers-reduced-motion:reduce){body[data-kux-screen="work"] .intent-dock{transition:none}}
'''

WORK_TOUR = '''
const workTourSteps=[
 {title:'Contesto e lavoro',body:'Scegli il contesto e l’attività su cui operare. Il cambio di vista recupera le schede e le bozze dell’ambiente, lasciando intatti i dati del dominio.',scope:'Contesto selezionato, situazione e focus del campo.',when:'Quando cambi argomento o riprendi un lavoro.',action:'Apri il navigatore del contesto e scegli un ambiente. Il menu Azione porta a una scheda nel campo.',effect:'Cambia la proiezione di questo laboratorio, non una fonte o un permesso Nautico.',target:()=>document.querySelector('.kux-context-navigation')},
 {title:'Attività a disposizione',body:'Le icone laterali sono accessi alle attività: dieci voci di base, tutte raggiungibili scorrendo. Un’attività non visibile non è persa; +Attività permette di aggiungere altre forme.',scope:'Attività disponibili e schede già aperte nel contesto.',when:'Per aprire, ritrovare, minimizzare o esplorare altre funzioni.',action:'Seleziona un’icona oppure usa +Attività. Nascondi la barra dal suo pulsante e richiamala dal bordo.',effect:'Si modifica il campo visualizzato; i dati rimangono nel controller della demo.',target:()=>getComputedStyle(document.querySelector('.intent-dock')).display!=='none'&&document.body.dataset.kuxActivities!=='hidden'?document.querySelector('.intent-dock'):$('btnQuickAdd')},
 {title:'Scheda e comandi',body:'La scheda rende accessibile il lavoro nella situazione corrente. I comandi del titolo cambiano posizione o profondità, non l’autorità sull’oggetto.',scope:'Una scheda selezionata e il relativo contesto.',when:'Per leggere, spostare, affiancare o aprire a pagina intera.',action:'Usa i comandi in alto; trascina l’intestazione verso il bordo alto per espandere, dall’alto verso il basso per tornare.',effect:'La stessa scheda conserva identità e contributi attraverso il movimento.',target:()=>getFocused()?.el?.querySelector('.module-head')||shell.stage},
 {title:'Composizione della vista',body:'Ricomponi distribuisce il campo in modo adattivo. Puoi anche scegliere Libero o le colonne e regolare soltanto divisori fra regioni esistenti.',scope:'Layout, schede in vista, focus e rapporti fra le colonne.',when:'Quando cambiano le attività o vuoi leggere insieme più elementi.',action:'Apri Strumenti, scegli una disposizione o Ricomponi. Mantieni focus se vuoi proteggere la scheda principale.',effect:'Nessuna approvazione o modificazione delle fonti del kernel ricevente.',target:()=>$('btnWorkMenu')},
 {title:'Dialogo della scheda',body:'Ogni scheda può aprire il proprio dialogo locale. È diverso dalla chat globale: riguarda il suo oggetto, le tracce e le relazioni che la scheda rende disponibili.',scope:'Lavoro e messaggi della sezione attiva.',when:'Per approfondire una fonte o preparare un contributo situato.',action:'Usa Dialogo scheda nel piede della scheda, poi le voci Conversazione o Fonti.',effect:'La demo non chiama un LLM: conserva soltanto un’interazione locale attribuita.',target:()=>getFocused()?.el?.querySelector('.module-foot')||shell.stage},
 {title:'Assistente globale',body:'La chat generale conserva l’orientamento sull’insieme del campo. Può affiancarsi alle schede e mostrare un modulo facoltativo; in futuro il kernel ricevente fornirà competenze, dati e azioni reali.',scope:'Assistente comune e risorse del contesto.',when:'Per chiedere come proseguire o comporre un contributo.',action:'Apri l’icona assistente in basso a sinistra, poi scegli Chat o Modulo. Chiudi il modulo quando non serve.',effect:'Questo ricevente è locale, non dispone di un agente connesso né invia messaggi esterni.',target:()=>document.querySelector('.kux-rail-footer .kux-surface-avatar')||$('btnHelp')},
 {title:'Eventi e ritorno',body:'Le variazioni e le capacità in questo laboratorio sono simulate. I segnali possono modificare l’attenzione, ma devono restare collegati alla loro sorgente.',scope:'Registro, evento dimostrativo e continuità del lavoro.',when:'Quando una notifica merita esame o vuoi recuperare la storia locale.',action:'Prova Simula variazione o apri Registro. Torna alla Home per preparare un altro campo.',effect:'Le simulazioni non diventano accadimenti aziendali e nessuna azione esterna viene eseguita.',target:()=>getComputedStyle($('btnEvent')).display!=='none'&&$('btnEvent').getClientRects().length?$('btnEvent'):document.querySelector('.work-footer')}
];
let guidedTourKind='home';
function beginGuidedTour(kind){
 guidedTourKind=kind==='work'?'work':'home';homeTourOrigin=document.activeElement;
 if(homeTourDialog.open)homeTourDialog.close();
 homeTourDialog.show();showHomeTour(0);$('homeTourNext').focus({preventScroll:true});
}
'''

ACTIVITY_RAIL = '''
let activitiesMode='pinned',activitiesPeekTimer=null;
const railVisibility=document.createElement('button');railVisibility.id='railVisibility';railVisibility.type='button';railVisibility.className='kux-activity-toggle';railVisibility.title='Nascondi o mostra le attività';railVisibility.setAttribute('aria-label','Nascondi barra delle attività');railVisibility.textContent='‹';
const activityCount=document.createElement('small');activityCount.id='activityCount';activityCount.className='kux-dock-count';activityCount.textContent='10 disponibili';
const activityEdge=document.createElement('button');activityEdge.type='button';activityEdge.id='activitiesEdge';activityEdge.className='kux-activity-edge';activityEdge.textContent='Attività';activityEdge.setAttribute('aria-label','Mostra le attività nascoste');activityEdge.setAttribute('aria-expanded','false');
const activityRail=document.querySelector('.intent-dock');activityRail.insertBefore(railVisibility,activityRail.querySelector('.dock-caption'));activityRail.insertBefore(activityCount,shell.dock);document.querySelector('#app').append(activityEdge);
function updateActivitiesRail(){
 const width=activitiesMode==='pinned'&&state.screen==='work'&&!matchMedia('(max-width:760px)').matches?(activityRail.getBoundingClientRect().width||86):0;
 document.body.dataset.kuxActivities=activitiesMode;
 document.body.style.setProperty('--kux-full-rail',Math.round(width)+'px');
 activityRail.inert=activitiesMode==='hidden';activityRail.setAttribute('aria-hidden',activitiesMode==='hidden'?'true':'false');
 railVisibility.setAttribute('aria-label','Nascondi barra delle attività');railVisibility.setAttribute('aria-expanded','true');
 activityEdge.setAttribute('aria-expanded',activitiesMode==='peek'?'true':'false');
 const shown=state.panels.filter(p=>p.context===state.activeContext&&!p.minimized).length;
 activityCount.textContent='10 accessi · '+shown+' nel campo';activityCount.title='10 attività disponibili; '+shown+' schede aperte in '+ctxName(state.activeContext);
}
function setActivitiesMode(next){
 clearTimeout(activitiesPeekTimer);activitiesMode=next;updateActivitiesRail();
 if(state.screen==='work'){relocateAssistantAvatar();placePanels();syncAssistantDockBounds();}
}
railVisibility.addEventListener('click',()=>{setActivitiesMode('hidden');activityEdge.focus({preventScroll:true});});
activityEdge.addEventListener('click',()=>setActivitiesMode('pinned'));
activityEdge.addEventListener('pointerenter',e=>{if(e.pointerType==='mouse'&&activitiesMode==='hidden')setActivitiesMode('peek');});
activityRail.addEventListener('pointerenter',()=>clearTimeout(activitiesPeekTimer));
activityRail.addEventListener('pointerleave',()=>{if(activitiesMode!=='peek')return;activitiesPeekTimer=setTimeout(()=>{if(!activityRail.matches(':hover')&&!activityEdge.matches(':hover')&&!activityRail.contains(document.activeElement))setActivitiesMode('hidden');},260);});
activityEdge.addEventListener('pointerleave',()=>{if(activitiesMode!=='peek')return;activitiesPeekTimer=setTimeout(()=>{if(!activityRail.matches(':hover')&&!activityEdge.matches(':hover'))setActivitiesMode('hidden');},260);});
'''


def patch(text:str,old:str,new:str,tag:str)->str:
    count=text.count(old)
    if count!=1:raise RuntimeError(f'{tag}: expected 1 occurrence, found {count}')
    return text.replace(old,new,1)


def build()->str:
    raw=BASE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=BASE_SHA:raise RuntimeError('v5.5 source identity changed')
    s=raw.decode('utf-8')
    s=patch(s,'<title>MAIOS · K-UX-AI — Griglia del fare v5.5 · Interazione situata</title>','<title>MAIOS · K-UX-AI — Griglia del fare v5.6 · Canvas guidato</title>','title')
    s=patch(s,'K-UX-AI v5.5: medium UI per kernel, tour situato, campo componibile e interazioni continue. Demo sintetica Nautico.','K-UX-AI v5.6: medium UI per kernel, canvas guidato, attività contestuali e interazioni continue. Demo sintetica Nautico.','description')
    s=patch(s,'</style>\n</head>','\n'+CSS+'\n</style>\n</head>','css')
    s=patch(s,'<div class="eyebrow">LABORATORIO LOCALE · 11.10.2026 · v5.5</div>','<div class="eyebrow">LABORATORIO LOCALE · 11.10.2026 · v5.6</div>','info')
    # The same tour component serves two contexts without inventing a duplicate controller.
    s=patch(s,'const tourSteps=[','const tourSteps=[','toursteps') if False else s
    anchor='let homeTourIndex=0,homeTourOrigin=null,homeTourHighlighted=null;'
    s=patch(s,anchor,WORK_TOUR+'\n'+anchor,'work-tour')
    s=patch(s,"if(!homeTourDialog.open||state.screen!=='home')return;","if(!homeTourDialog.open||state.screen!==(guidedTourKind==='work'?'work':'home'))return;",'tour-state')
    s=patch(s,"const target=tourSteps[homeTourIndex].target();if(!target)return;","const steps=guidedTourKind==='work'?workTourSteps:tourSteps;const target=steps[homeTourIndex].target();if(!target)return;",'tour-target')
    s=patch(s,"homeTourIndex=Math.max(0,Math.min(tourSteps.length-1,index));const item=tourSteps[homeTourIndex];","const steps=guidedTourKind==='work'?workTourSteps:tourSteps;homeTourIndex=Math.max(0,Math.min(steps.length-1,index));const item=steps[homeTourIndex];",'tour-show')
    s=patch(s,"$('homeTourStep').textContent=`PASSO ${homeTourIndex+1} / ${tourSteps.length}`;","$('homeTourStep').textContent=`${guidedTourKind==='work'?'CANVAS':'HOME'} · PASSO ${homeTourIndex+1} / ${steps.length}`;",'tour-progress')
    s=patch(s,"$('homeTourBack').disabled=homeTourIndex===0;$('homeTourNext').textContent=homeTourIndex===tourSteps.length-1?'Concludi':'Avanti ↗';","$('homeTourBack').disabled=homeTourIndex===0;$('homeTourNext').textContent=homeTourIndex===steps.length-1?'Concludi':'Avanti ↗';",'tour-next')
    s=patch(s,"$('homeTourButton').addEventListener('click',()=>{homeTourOrigin=document.activeElement;homeTourDialog.show();showHomeTour(0);$('homeTourNext').focus({preventScroll:true});});","$('homeTourButton').addEventListener('click',()=>beginGuidedTour('home'));",'tour-home-handler')
    s=patch(s,"if(homeTourIndex===tourSteps.length-1)$('homeTourDialog').close();","if(homeTourIndex===(guidedTourKind==='work'?workTourSteps:tourSteps).length-1)$('homeTourDialog').close();",'tour-end')
    s=patch(s,"$('btnHelp').addEventListener('click',()=>$('infoDialog').showModal());","$('btnHelp').addEventListener('click',()=>state.screen==='work'?beginGuidedTour('work'):$('infoDialog').showModal());",'tour-toolbar')
    s=patch(s,"$('btnHelpMobile').addEventListener('click',()=>$('infoDialog').showModal());","$('btnHelpMobile').addEventListener('click',()=>beginGuidedTour('work'));",'tour-menu')
    s=patch(s,"$('btnHelp').setAttribute('aria-label','Informazioni sul prototipo');","$('btnHelp').setAttribute('aria-label','Informazioni sul prototipo');",'noop') if False else s
    # All ten primary activity entrances, not the first seven plus a contextual extra.
    s=patch(s,"for(const intent of [...intents.slice(0,7),additional[0]]){","for(const intent of intents){",'all-ten-intents')
    s=patch(s,"shell.dock.replaceChildren();\n for(const intent of intents){","shell.dock.replaceChildren();\n updateActivitiesRail();\n for(const intent of intents){",'activity-count')
    # Real context navigation: clicking Esplora changes the workspace projection, not the identity of an existing panel.
    s=patch(s,"if(act==='change-context'){p.context=button.dataset.target;focusPanel(p);renderModule(p);notice('Stesso ingresso, nuovo contesto: '+ctxName(p.context));return;}","if(act==='change-context'){const target=button.dataset.target;if(!Object.hasOwn(contexts,target))return;switchWorkspaceContext(target);const next=openPanel('esplorare',target,{forceFocus:true});if(next)focusPanel(next,{force:true});notice('Esplora '+ctxName(target)+' · contesto e attività allineati; nessun effetto Nautico.');return;}",'explore-action')
    # Activity rail pinned alongside fullscreen; independent of the floating global chat avatar.
    s=patch(s,"function relocateAssistantAvatar(){\n if(!sharedAssistantSurface)return;\n const full=state.panels.some(p=>p.maximized&&!p.minimized);","function relocateAssistantAvatar(){\n if(!sharedAssistantSurface)return;",'remove-unused-full')
    s=patch(s,"const destination=(state.screen==='work'&&!full)\n  ? (mobile?$('mobileAssistantSlot'):railFooter)\n  : (mobile?$('mobileAssistantSlot'):document.querySelector('.kux-surface-root'));","const destination=(state.screen==='work')\n  ? (mobile?$('mobileAssistantSlot'):(activitiesMode==='hidden'?document.querySelector('.kux-surface-root'):railFooter))\n  : document.querySelector('.kux-surface-root');",'chat-one-locus')
    s=patch(s,"for(const el of [document.querySelector('.topbar'),document.querySelector('.intent-dock'),document.querySelector('.work-toolbar'),document.querySelector('.work-footer'),$('openTabs')])if(el)el.inert=!!full;","for(const el of [document.querySelector('.topbar'),document.querySelector('.work-toolbar'),document.querySelector('.work-footer'),$('openTabs')])if(el)el.inert=!!full;",'rail-access-during-full')
    s=patch(s,"document.body.dataset.fullscreenPanel=String(!!full);\n  relocateAssistantAvatar();","document.body.dataset.fullscreenPanel=String(!!full);\n  updateActivitiesRail();relocateAssistantAvatar();",'rail-full-sync')
    s=patch(s,"el.setAttribute('role',p.maximized?'dialog':'region');\n if(p.maximized)el.setAttribute('aria-modal','true');else el.removeAttribute('aria-modal');","el.setAttribute('role','region');\n el.removeAttribute('aria-modal'); // The adjacent Activity rail remains operable in full view.",'full-aria')
    s=patch(s,"  if(p.maximized&&e.key==='Tab'){\n   const els=[...p.el.querySelectorAll('button,input,select,textarea,a[href],[tabindex]:not([tabindex=\"-1\"])')].filter(x=>!x.hidden&&!x.closest('[hidden]')&&!x.disabled&&x.getClientRects().length);\n   if(els.length){const first=els[0],last=els[els.length-1];if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}}\n  }","  // Full view keeps the Activity rail reachable via normal keyboard navigation.",'full-no-trap')
    # Hidden dividers never persist after a single-card transition / fullscreen.
    s=patch(s,"const visible=state.panels.filter(p=>!p.minimized&&p.context===state.activeContext);\n const lead=getFocused();\n const ordered=slotVisibleOrder();","const visible=state.panels.filter(p=>!p.minimized&&p.context===state.activeContext);\n const lead=getFocused();\n const ordered=slotVisibleOrder();",'noop2') if False else s
    s=patch(s,"dividerCtrl?.sync(secondary.length>0&&w>=760);","dividerCtrl?.sync(visible.length>1&&secondary.length>0&&w>=760&&!visible.some(p=>p.maximized));",'orphan-divider')
    s=patch(s,"const active=state.layout==='auto'&&secondaryRail&&!secondaryRail.hidden&&secondaryRail.dataset.fast==='true'&&secondaryRail.children.length>=2&&!shell.stage.dataset.railCompact?.includes('true');","const active=state.layout==='auto'&&secondaryRail&&!secondaryRail.hidden&&secondaryRail.dataset.fast==='true'&&secondaryRail.children.length>=2&&state.panels.some(p=>p.context===state.activeContext&&!p.minimized&&!p.maximized)&&!state.panels.some(p=>p.context===state.activeContext&&p.maximized)&&!shell.stage.dataset.railCompact?.includes('true');",'medium-divider-full')
    s=patch(s,"if(state.layout==='auto'){dividerCtrl?.align();alignMediumDivider();}","if(state.layout==='auto'){dividerCtrl?.sync(state.panels.filter(p=>p.context===state.activeContext&&!p.minimized).length>1&&!state.panels.some(p=>p.context===state.activeContext&&p.maximized));dividerCtrl?.align();alignMediumDivider();}",'restored-dividers')
    # Additional affordance is separate from sidebar's expand-rail control.
    s=patch(s,"const railAside=document.querySelector('.intent-dock');railAside.insertBefore(railFooter,$('dockAll'));railFooter.append($('dockAll'));","const railAside=document.querySelector('.intent-dock');railAside.insertBefore(railFooter,$('dockAll'));railFooter.append($('dockAll'));\n"+ACTIVITY_RAIL,'activity-control')
    s=patch(s,"state.screen=screen;shell.home.hidden=screen!=='home';shell.work.hidden=screen!=='work';document.body.dataset.kuxScreen=screen;","state.screen=screen;shell.home.hidden=screen!=='home';shell.work.hidden=screen!=='work';document.body.dataset.kuxScreen=screen;\n updateActivitiesRail();$('btnHelp').setAttribute('aria-label',screen==='work'?'Avvia il tour del Canvas':'Informazioni sul prototipo');",'screen-controls')
    s=patch(s,"version:'lab-2026-10-11-r5.5',liveAI:false","version:'lab-2026-10-11-r5.6',liveAI:false",'diagnostic-version')
    # expose read-only rail and tour info for independent browser checks
    s=patch(s,"version:'lab-2026-10-11-r5.6',liveAI:false","activityRail:()=>({mode:activitiesMode,visibleIntents:[...shell.dock.querySelectorAll('.avatar-entry')].map(e=>e.dataset.intent),edgeVisible:!activityEdge.hidden&&getComputedStyle(activityEdge).display!=='none'}),tour:()=>({kind:guidedTourKind,index:homeTourIndex,open:homeTourDialog.open}),version:'lab-2026-10-11-r5.6',liveAI:false",'debug-readback')
    return s


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');a=parser.parse_args()
    txt=build();data=txt.encode('utf-8')
    if a.check:
        if not OUT.exists() or OUT.read_bytes()!=data:raise SystemExit('DRIFT: v5.6 HTML not byte-identical')
    else:OUT.write_bytes(data)
    print('OK', 'check' if a.check else 'build',OUT.name,len(data),'sha256',hashlib.sha256(data).hexdigest())

if __name__=='__main__':main()
