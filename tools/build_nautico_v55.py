"""Build K-UX-AI v5.5 from pinned v5.4.1 without rewriting the original.
Usage: python build_v55.py [--check]
"""
from pathlib import Path
import argparse, hashlib

HERE=Path(__file__).resolve().parent.parent
BASE=HERE/'labs/nautico-ui-v4/16-griglia-continuity-v541.html'
OUT=HERE/'labs/nautico-ui-v4/17-griglia-situated-v55.html'
PIN='7e8a35dc21bdc6940e1ad00db47fbe9327237a33c6aede5a71aaf03f7d8f9716'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def exact(a,b,label=''):
    global s
    n=s.count(a)
    if n!=1: raise RuntimeError(f'{label or a[:75]} expected once, found {n}')
    s=s.replace(a,b,1)

assert sha(BASE)==PIN, 'Source changed; do not apply to a different baseline.'
s=BASE.read_text('utf-8')

# Home: retain a compact first-viewport entrance while making the medium's scope legible.
exact('<title>MAIOS · K-UX-AI — Griglia del fare v5.4.1 · Continuità</title>', '<title>MAIOS · K-UX-AI — Griglia del fare v5.5 · Interazione situata</title>', 'document title')
exact('<meta name="description" content="K-UX-AI v5.4: Home preparativa, tour con spotlight contestuale e strumenti ordinati. Laboratorio locale sintetico.">',
      '<meta name="description" content="K-UX-AI v5.5: medium UI per kernel, tour situato, campo componibile e interazioni continue. Demo sintetica Nautico.">')
exact('<div><div class="eyebrow">PROTOTIPO 01 · LA GRIGLIA DEL FARE</div><h1 id="homeTitle">Un lavoro.<br><em>Molti modi di entrarci.</em></h1><p class="intro-desc">Il punto di ingresso non è una pagina da cercare. Scegli ciò che vuoi fare: il campo rende disponibili contesto, strumenti e possibilità di continuazione.</p></div>',
'''<div class="kux-home-story"><div class="eyebrow">K-UX-AI · IL DESIGN DELL’INTERAZIONE</div><h1 id="homeTitle">Un lavoro.<br><em>Molti modi di entrarci.</em></h1><h2 class="kux-home-thesis">UX-AI evolutiva e nuove possibilità</h2><p class="intro-desc">K-UX-AI sviluppa interfacce modulari per lavorare con kernel e sistemi agentici complessi, in ambito aziendale, professionale e di ricerca. Questa griglia è una delle forme possibili.</p><p class="kux-home-depth">Nel sistema integrato, contesto, eventi, competenze e risorse potranno orientare il campo, preservare continuità e sostenere le azioni. <strong>Qui sperimenti la UI con dati locali</strong>: adattamento cognitivo e agenti reali dipendono dal kernel ricevente.</p><p class="kux-home-next">Scegli un punto d’ingresso oppure esplora: una notifica qualificata potrà richiamare gli strumenti pertinenti quando il sistema sarà collegato. <a href="https://github.com/GrazianoGuiducci/k-ux-ai/blob/main/MANIFESTO.md" target="_blank" rel="noopener noreferrer" class="kux-home-learn">Approfondisci K-UX-AI ↗</a></p></div>''','home intro')
exact('Scegli un ambiente. Poi prepara le attività da ritrovare nel canvas.', 'Scegli un ambiente o argomento. Le attività si possono preparare qui oppure aggiungere dopo.', 'home setup intro')
exact('02 / ATTIVITÀ · SELEZIONA PER IL CANVAS, TRASCINA PER RIORDINARE','02 / PREPARA LE ATTIVITÀ · SCEGLI, TRASCINA O ENTRA PER ESPLORARE', 'home activity stripe')
exact('aria-label="Avatar delle attività"','aria-label="Accessi alle attività"')
exact('aria-label="Ridimensiona la barra degli avatar"','aria-label="Ridimensiona la barra delle attività"')
exact('Avatar, pannelli e chat possono condividere lo spazio senza modificare lo stato reale di alcuna imbarcazione.', 'Accessi alle attività, pannelli e chat possono condividere lo spazio senza modificare lo stato reale di alcuna imbarcazione.')
exact('LABORATORIO PRIVATO · 10.10.2026 · v5.1','LABORATORIO LOCALE · 11.10.2026 · v5.5')
exact('version:\'lab-2026-10-10-r5.4.1\',liveAI:false',"version:'lab-2026-10-11-r5.5',liveAI:false")

# Step messaging: operator's specific semantics, with present demo vs future kernel truth kept distinguishable.
start=s.index('const tourSteps=[')
end=s.index('];\nlet homeTourIndex=',start)+2
orig=s[start:end]
new='''const tourSteps=[
 {title:'Scegli il contesto',body:'Il contesto identifica un luogo, un argomento o la situazione in cui desideri lavorare. È il riferimento comune delle attività, delle fonti e del focus.',scope:'Gli ambienti della demo: Progetto/Poppa, Cantiere, Fornitori, A bordo e Assistenza.',when:'All’inizio, al ritorno sul lavoro o quando cambia l’oggetto da trattare.',action:'Scegli un ambiente. Potrai cambiare contesto dalla barra del campo e ritrovare quello che avevi preparato.',effect:'La Home e le schede proiettano il contesto scelto. La scelta non altera documenti, fonti o permessi Nautico.',target:()=>$('homeContextOptions')},
 {title:'Prepara le attività',body:'Le attività sono ingressi a strumenti e azioni del contesto. Le puoi preparare nella griglia oppure aggiungere quando sei già nel canvas.',scope:'Le dieci modalità dimostrative, le schede già aperte e la loro disposizione locale.',when:'Quando vuoi affiancare prospettive o dare priorità a un lavoro; puoi anche entrare e scoprire dopo.',action:'Seleziona le tessere da ritrovare; trascina per scambiare i posti. Nel canvas usa +Attività, focus e Ricomponi.',effect:'La griglia prepara la vista del lavoro, non crea automaticamente nuove fonti o approvazioni.',target:()=>shell.grid.querySelector('.intent-tile[data-selected="true"]')||shell.grid.querySelector('.intent-tile')},
 {title:'Entra nel campo operativo',body:'La preparazione compone il canvas. Anche la selezione iniziale è sufficiente per entrare e cominciare a esplorare: potrai cambiare tutto in seguito.',scope:'Il contesto, le attività preparate e le bozze già presenti in questa demo.',when:'Quando vuoi osservare, comprendere, conversare o intervenire nella situazione.',action:'Premi “Entra nel campo”. Sposta le schede, aggiungi attività e apri l’assistente globale o il dialogo della singola scheda.',effect:'Le schede diventano accessibili nel canvas. L’assistente di questa demo mostra letture locali; un agente realmente competente richiederà il kernel e i servizi collegati.',target:()=>$('homeSelectionStatus').closest('.home-setup-footer')}
];'''
exact(orig,new,'tour steps')

# Explain local dialogues and keep the generic medium independent of the Nautico demonstrator.
exact('Chat sezione ↗','Dialogo scheda ↗','section dialogue label')
exact('notice(\'Conversazione della scheda · contesto \'+ctxName(p.context)+\' · nessun provider AI\')', "notice('Dialogo locale della scheda · '+readIntent(p.intent).verb+' / '+ctxName(p.context)+' · nessun modello AI collegato')",'dialogue notice')
exact('Conversazione contestuale · senza AI collegata','Dialogo della singola scheda · demo locale')
exact('Lettura dimostrativa della fonte: ${escapeHTML(context.source)}. Le eventuali proposte sono candidate, non competenze assimilate.', 'La conversazione resta legata a questa attività e alla fonte ${escapeHTML(context.source)}. Può diventare il punto di accesso a competenze locali quando esiste un controller reale. Le proposte qui non sono assimilate.')
exact('Il prototipo esplora anche la possibile evoluzione della UI quando il sistema riceve una nuova capacità; non dimostra apprendimento autonomo.', 'Questo medium può essere adottato da altri kernel. La demo mostra strumenti locali; chat connessa, adattamento semantico e permessi reali dipendono dal ricevente. In ogni scheda trovi anche un dialogo locale dimostrativo.')

# Form control: one explicitly reversible choice; no second controller or premature form contract.
exact("const root=div('kux-chat-form');root.dataset.compact='false';root.dataset.pane='chat';", "const root=div('kux-chat-form');root.dataset.compact='false';root.dataset.pane='chat';root.dataset.formOpen='false';", 'form root')
exact("tabForm.textContent='Modulo';", "tabForm.textContent='Apri modulo';", 'form tab default')
exact("let kind='contribution', pane='chat', compact=false, split=43, dragging=null, resize=null, busy=false;", "let kind='contribution', pane='chat', formOpen=false, compact=false, split=43, dragging=null, resize=null, busy=false;",'form state')
exact("  const setPane=(next)=>{if(!['chat','form'].includes(next))return;pane=next;root.dataset.pane=pane;\n    for(const b of [tabChat,tabForm]){const sel=b.dataset.pane===pane;b.setAttribute('aria-selected',String(sel));b.tabIndex=sel?0:-1;}\n  };", '''  const setPane=(next)=>{if(!['chat','form'].includes(next))return;
    formOpen=next==='form';pane=next;root.dataset.formOpen=String(formOpen);root.dataset.pane=pane;
    tabForm.textContent=formOpen?'Chiudi modulo':'Apri modulo';
    tabForm.setAttribute('aria-label',formOpen?'Chiudi il modulo sperimentale e torna alla chat':'Apri il modulo sperimentale a fianco della chat, se lo spazio lo consente');
    for(const b of [tabChat,tabForm]){const sel=b.dataset.pane===pane;b.setAttribute('aria-selected',String(sel));b.tabIndex=sel?0:-1;}
  };''','module setPane')
exact("  tabChat.addEventListener('click',()=>setPane('chat'));tabForm.addEventListener('click',()=>setPane('form'));", "  tabChat.addEventListener('click',()=>setPane('chat'));tabForm.addEventListener('click',()=>setPane(formOpen?'chat':'form'));",'module tab callbacks')
exact("    snapshot:()=>({kind,pane,compact,split,draft:getDraft(),messageCount:messages.children.length}),", "    snapshot:()=>({kind,pane,formOpen,compact,split,draft:getDraft(),messageCount:messages.children.length}),",'module snapshot')
exact("  const formSubtitle=div('','small');formSubtitle.textContent='Prepara una traccia o una domanda per il controller ospitante.';", "  const formSubtitle=div('','small');formSubtitle.textContent='Strumento di prova: struttura e funzioni potranno cambiare con il kernel ricevente.';",'module nonfinal note')

# Split top/dock layout: reserve an actual lane for quick activity access; do not cover the site header.
exact(" body[data-kux-screen=\"work\"][data-kux-assistant-mode=\"dock-left\"] .work-main{margin-left:min(42vw,680px)}", " body[data-kux-screen=\"work\"][data-kux-assistant-mode=\"dock-left\"] .work-main{margin-left:var(--kux-assistant-dock-width,min(36vw,640px))}", 'dock left work margin')
# Appended override after accumulated historical CSS, preserving the existing other modes.
css='''
/* v5.5 — readable generic entrance + reversible chat module + sourced edge gestures. */
.kux-home-story{min-width:0}
.kux-home-thesis{font-size:clamp(15px,1.3vw,20px);letter-spacing:-.015em;margin:-7px 0 7px;font-weight:700}
.kux-home-story .intro-desc{font-size:clamp(12px,.9vw,14px);line-height:1.42;margin:0 0 8px;max-width:86ch}
.kux-home-depth,.kux-home-next{font-size:clamp(11px,.8vw,12.5px);line-height:1.45;color:var(--muted);margin:0 0 7px;max-width:92ch}
.kux-home-depth strong{color:var(--ink);font-weight:700}
.kux-home-learn{display:inline-block;font-weight:750;text-underline-offset:3px;color:var(--ink);margin-left:4px}
.kux-chat-form .kux-chat-tabs{display:flex;justify-content:space-between;align-items:center;gap:7px;flex:0 0 auto}
.kux-chat-form .kux-chat-tabs button{min-width:0;flex:1;text-align:center}
.kux-chat-form[data-form-open="false"] .kux-chat-regions{display:flex;flex-direction:column}
.kux-chat-form[data-form-open="false"] .kux-chat-pane{flex:1 1 auto;border-right:0}
.kux-chat-form[data-form-open="false"] .kux-form-pane,.kux-chat-form[data-form-open="false"] .kux-chat-splitter{display:none!important}
.kux-chat-form[data-form-open="true"]:not([data-compact="true"]) .kux-chat-regions{display:grid;grid-template-columns:minmax(225px,var(--kux-chat-split)) 7px minmax(0,1fr)}
.kux-chat-form[data-compact="true"][data-form-open="true"] .kux-chat-tabs{display:flex}
body[data-kux-screen="work"] .kux-surface-frame[data-mode="dock-left"]{
 inset:auto!important;left:var(--kux-assistant-left,86px)!important;
 top:var(--kux-assistant-top,115px)!important;bottom:var(--kux-assistant-bottom,36px)!important;
 width:var(--kux-assistant-dock-width,min(36vw,640px))!important;height:auto!important;
 border-radius:8px 8px 0 0;box-shadow:8px 7px 25px #152f3033}
body[data-kux-screen="work"] .kux-surface-frame[data-mode="dock-left"] .kux-surface-header{min-height:55px}
body[data-kux-screen="work"] .intent-dock{position:relative;z-index:203}
body[data-kux-screen="work"] .kux-surface-frame[data-mode="dock-left"]{z-index:202}
.kux-surface-frame[data-drag-target="full"],.module[data-drag-target="full"]{outline:3px solid var(--mint-strong,#72ee80);outline-offset:-3px}
body[data-kux-full-target="true"]:after{content:"Rilascia in alto per aprire a pagina intera";position:fixed;z-index:10020;pointer-events:none;top:49px;left:50%;transform:translateX(-50%);border:2px solid #1e746c;border-radius:8px;padding:9px 16px;background:#d6ffe2;color:#14363a;font:750 13px/1.3 system-ui,sans-serif;box-shadow:0 6px 24px #12363739;white-space:nowrap}
.workspace-stage .module[data-placement="full"] .module-head{cursor:grab;touch-action:none}
@media(max-width:780px){
 .kux-home-story .intro-desc,.kux-home-depth,.kux-home-next{font-size:13px}
 body[data-kux-screen="work"] .kux-surface-frame[data-mode="dock-left"]{inset:0!important;width:100vw!important;height:100dvh!important;border-radius:0}
 body[data-kux-full-target="true"]:after{max-width:calc(100vw - 24px);white-space:normal;text-align:center;top:7px}
}
'''
exact('</style>\n</head>',''+css+'</style>\n</head>','v5.5 css insertion')

# Dock bounds are measured from actual host geometry so the left activity rail
# is always exposed. This is receiving composition, not the window's domain owner.
insert='''function syncAssistantDockBounds(){
 if(!sharedAssistantSurface||state.screen!=='work')return;
 const rail=document.querySelector('.intent-dock'),topbar=document.querySelector('.topbar'),footer=document.querySelector('.work-footer');
 const r=rail?.getBoundingClientRect();
 const railRight=r&&getComputedStyle(rail).display!=='none'?Math.round(r.right):0;
 const top=Math.round(topbar?.getBoundingClientRect().bottom||0);
 const foot=footer?.getBoundingClientRect();
 const bottom=Math.max(0,Math.round(window.innerHeight-(foot?.top||window.innerHeight)));
 const width=Math.max(285,Math.min(640,Math.round(window.innerWidth*.36),window.innerWidth-railRight-280));
 const values={'--kux-assistant-left':railRight+'px','--kux-assistant-top':top+'px','--kux-assistant-bottom':bottom+'px','--kux-assistant-dock-width':width+'px'};
 for(const [key,value] of Object.entries(values))if(document.body.style.getPropertyValue(key)!==value)document.body.style.setProperty(key,value);
}
'''
exact('function initSharedAssistant(){',insert+'function initSharedAssistant(){','assistant bounds function')
# Both callbacks carry the same UI state and must acquire the same host bounds.
old_cb="     document.body.dataset.kuxAssistantMode=readback.open?readback.mode:'closed';\n     sharedAssistantModule.refreshLayout();"
new_cb="     document.body.dataset.kuxAssistantMode=readback.open?readback.mode:'closed';\n     syncAssistantDockBounds();\n     sharedAssistantModule.refreshLayout();"
assert s.count(old_cb)==2, 'Unexpected assistant callback structure'
s=s.replace(old_cb,new_cb)
exact(" relocateAssistantAvatar();\n if(screen==='home'&&sharedAssistantSurface", " relocateAssistantAvatar();syncAssistantDockBounds();\n if(screen==='home'&&sharedAssistantSurface", 'assistant in activateScreen')
exact("window.addEventListener('resize',()=>{relocateResponsiveControls();clampPeekToViewport();if(state.screen==='work')placePanels();else packHomeTiles();});", "window.addEventListener('resize',()=>{relocateResponsiveControls();clampPeekToViewport();syncAssistantDockBounds();if(state.screen==='work')placePanels();else packHomeTiles();});",'assistant resize')

# Keep the form closed until explicitly requested even in wide window mode.
# When opening for contribution, setPane('form') reveals it; Chat hides it.

# Divider: aligning from animated child rectangles may target former positions.
# Anchor x to the actual grid track and settle after recompose/reflow.
exact("   const first=bounds[0];\n   const top=Math.min(...bounds.map(r=>r.top)),bottom=Math.max(...bounds.map(r=>r.bottom));", "   const available=Math.max(1,secondaryRail.clientWidth-10);\n   const col=limit(available*mediumSplit/100,Math.min(215,available/2),Math.max(available/2,available-215));\n   const top=Math.min(...bounds.map(r=>r.top)),bottom=Math.max(...bounds.map(r=>r.bottom));",'medium divider stable column')
exact("   mediumDivider.style.left=Math.round(first.right-stage.left+4)+'px';", "   mediumDivider.style.left=Math.round(rail.left-stage.left+col+5)+'px';",'medium divider x anchor')
exact(" placePanels();notice('Campo ricomposto: attività conservate, focus e bozze preservati.');", " placePanels();beginDividerSettle(true);notice('Campo ricomposto: attività conservate, focus e bozze preservati.');",'recompose settle')

# Slot drag: create fullscreen by dropping a *meaningful gesture* at top viewport;
# don't turn any header click into full or change domain state.
exact("  currentRole=roleFromPosition(ev.clientX,ev.clientY);\n  highlightSlotDrop(currentRole);", "  currentRole=ev.clientY<=Math.max(54,Math.min(94,window.innerHeight*.11))?'full':roleFromPosition(ev.clientX,ev.clientY);\n  document.body.dataset.kuxFullTarget=String(currentRole==='full');\n  p.el.dataset.dragTarget=currentRole==='full'?'full':'';\n  highlightSlotDrop(currentRole==='full'?null:currentRole);",'slot drag top target')
exact("  delete p.el.dataset.slotDragging;p.el.style.transform='';dragData=null;$('kuxSlotDrop').hidden=true;highlightSlotDrop(null);\n  if(ev.type==='pointerup'&&currentRole){p.lastSlotDragAt=performance.now();movePanelAtDrop(p,ev.clientX,ev.clientY);beginDividerSettle(true);notice(`${readIntent(p.intent).verb}: posizione aggiornata nel campo`);}\n  else placePanels();", "  delete p.el.dataset.slotDragging;delete p.el.dataset.dragTarget;delete document.body.dataset.kuxFullTarget;p.el.style.transform='';dragData=null;$('kuxSlotDrop').hidden=true;highlightSlotDrop(null);\n  if(ev.type==='pointerup'&&currentRole==='full'){\n   p.lastSlotDragAt=performance.now();const before=p.el.getBoundingClientRect();p.focusBeforeFull=state.focused;focusPanel(p,{force:true});p.maximized=true;p.compact=false;p.returnDock=p.dock;p.dock=null;\n   placePanels();beginDividerSettle(true);animateFrameChange(p,before);notice(readIntent(p.intent).verb+' a pagina intera. Trascina l’intestazione in basso per tornare al campo.');\n  }else if(ev.type==='pointerup'&&currentRole){p.lastSlotDragAt=performance.now();movePanelAtDrop(p,ev.clientX,ev.clientY);beginDividerSettle(true);notice(`${readIntent(p.intent).verb}: posizione aggiornata nel campo`);}\n  else placePanels();",'slot drag finalize')

# Fullscreen drag down restores the prior field *without* turning every layout
# into floating. Existing explicit max button and Escape remain alternative paths.
function='''function startFullscreenDrag(e,p){
 if(e.button!==0||e.target.closest('button'))return;
 const head=e.currentTarget,initialY=e.clientY,pointer=e.pointerId;
 head.setPointerCapture(pointer);
 const cleanup=()=>{for(const ev of ['pointermove','pointerup','pointercancel'])head.removeEventListener(ev,ev==='pointermove'?move:end);if(head.hasPointerCapture(pointer))head.releasePointerCapture(pointer);};
 const move=ev=>{
  if(ev.pointerId!==pointer||ev.clientY-initialY<32)return;
  const before=p.el.getBoundingClientRect();cleanup();p.maximized=false;p.dock=p.returnDock||null;p.returnDock=null;
  p.lastSlotDragAt=performance.now();
  placePanels();beginDividerSettle(true);animateFrameChange(p,before);
  p.el.querySelector('.module-head')?.focus({preventScroll:true});notice('Scheda ripristinata nella disposizione del campo.');
 };
 const end=ev=>{if(ev.pointerId!==pointer)return;cleanup();};
 for(const [ev,fn] of [['pointermove',move],['pointerup',end],['pointercancel',end]])head.addEventListener(ev,fn);
}
'''
exact('function startSlotDrag(e,p){',function+'function startSlotDrag(e,p){','fullscreen drag helper')
exact("node.querySelector('.module-head').addEventListener('pointerdown',event=>{if(state.layout!=='free'&&!event.altKey)startSlotDrag(event,p);else startDrag(event,p)});", "node.querySelector('.module-head').addEventListener('pointerdown',event=>{if(p.maximized)startFullscreenDrag(event,p);else if(state.layout!=='free'&&!event.altKey)startSlotDrag(event,p);else startDrag(event,p)});",'card drag router')
exact(" el.querySelector('[data-module-op=\"max\"]').setAttribute('aria-label',p.maximized?'Ripristina finestra':'Apri a pagina intera');", "  el.querySelector('[data-module-op=\"max\"]').setAttribute('aria-label',p.maximized?'Ripristina finestra':'Apri a pagina intera');\n  el.querySelector('.module-head').title=p.maximized?'Trascina verso il basso per tornare alla disposizione precedente':'Trascina in alto per pagina intera, oppure usa i comandi';",'full drag hint')

# Free-mode drag can also snap to full-page; avoid accidental side dock at the top edge.
exact("  previewDock(side);start.edge=side;", "  const fullCandidate=ev.clientY<=Math.max(54,Math.min(94,window.innerHeight*.11));\n  start.fullCandidate=fullCandidate;document.body.dataset.kuxFullTarget=String(fullCandidate);p.el.dataset.dragTarget=fullCandidate?'full':'';\n  previewDock(fullCandidate?null:side);start.edge=fullCandidate?null:side;",'free drag top candidate')
exact("  previewDock(null);dragData=null;\n  if(ev.type==='pointerup'&&start?.edge){p.dock=start.edge;notice('Scheda agganciata lateralmente');}\n  Object.assign(p,screenRect(p));if(!p.dock)p.savedFreeRect={x:p.x,y:p.y,w:p.w,h:p.h};placePanels();", "  previewDock(null);dragData=null;delete document.body.dataset.kuxFullTarget;delete p.el.dataset.dragTarget;\n  if(ev.type==='pointerup'&&start?.fullCandidate){\n   p.savedFreeRect=screenRect(p);const before=p.el.getBoundingClientRect();p.focusBeforeFull=state.focused;p.maximized=true;p.compact=false;p.returnDock=p.dock;p.dock=null;\n   placePanels();beginDividerSettle(true);animateFrameChange(p,before);notice('Pagina intera. Trascina l’intestazione in basso per tornare al campo.');return;\n  }\n  if(ev.type==='pointerup'&&start?.edge){p.dock=start.edge;notice('Scheda agganciata lateralmente');}\n  Object.assign(p,screenRect(p));if(!p.dock)p.savedFreeRect={x:p.x,y:p.y,w:p.w,h:p.h};placePanels();",'free drag finalize')

# Window Surface drag: wait for actual movement, allow top-drop full and full→down
# restoring the saved floating geometry. No silent placement change on click.
old='''  header.addEventListener('pointerdown',ev=>{
    if(ev.button!==0||isCompactViewport()||ev.target.closest('button'))return;
    cancelMotion();
    const current=box(frame.getBoundingClientRect());
    if(placement!=='floating'){
      geometry.x=clamp(ev.clientX-geometry.w*.25,0,Math.max(0,window.innerWidth-geometry.w));
      geometry.y=clamp(ev.clientY-27,0,Math.max(0,window.innerHeight-geometry.h));
      placement='floating';layout();
    }
    activeDrag={id:ev.pointerId,originX:ev.clientX,originY:ev.clientY,x:geometry.x,y:geometry.y};
    header.setPointerCapture(ev.pointerId);
    ev.preventDefault();
  });
  header.addEventListener('pointermove',ev=>{
    if(!activeDrag||activeDrag.id!==ev.pointerId)return;
    geometry.x=clamp(activeDrag.x+ev.clientX-activeDrag.originX,0,Math.max(0,window.innerWidth-geometry.w));
    geometry.y=clamp(activeDrag.y+ev.clientY-activeDrag.originY,0,Math.max(0,window.innerHeight-geometry.h));
    applyGeometry();
  });
  const finishDrag=ev=>{
    if(!activeDrag||activeDrag.id!==ev.pointerId)return;
    activeDrag=null;if(header.hasPointerCapture(ev.pointerId))header.releasePointerCapture(ev.pointerId);
    if(ev.type==='pointerup'&&ev.clientX<64)setPlacement('dock-left');
    else if(ev.type==='pointerup'&&ev.clientX>innerWidth-64)setPlacement('dock-right');
    else {save();onLayoutChange({id,mode:actualPlacement(),preferred:placement,open});}
  };'''
new='''  const topDropLimit=()=>Math.max(54,Math.min(94,window.innerHeight*.11));
  header.addEventListener('pointerdown',ev=>{
    if(ev.button!==0||isCompactViewport()||ev.target.closest('button'))return;
    activeDrag={id:ev.pointerId,originX:ev.clientX,originY:ev.clientY,x:geometry.x,y:geometry.y,
      begun:false,fromFull:actualPlacement()==='full',topCandidate:false};
    header.setPointerCapture(ev.pointerId);ev.preventDefault();
  });
  header.addEventListener('pointermove',ev=>{
    if(!activeDrag||activeDrag.id!==ev.pointerId)return;
    const d=activeDrag;
    if(!d.begun){
      if(Math.hypot(ev.clientX-d.originX,ev.clientY-d.originY)<12)return;
      if(d.fromFull&&ev.clientY-d.originY<32)return;
      d.begun=true;cancelMotion();
      if(placement!=='floating'){
        geometry.x=clamp(ev.clientX-geometry.w*.28,0,Math.max(0,window.innerWidth-geometry.w));
        geometry.y=clamp(ev.clientY-29,0,Math.max(0,window.innerHeight-geometry.h));
        placement='floating';layout();
      }
      d.x=geometry.x;d.y=geometry.y;d.originX=ev.clientX;d.originY=ev.clientY;
    }
    geometry.x=clamp(d.x+ev.clientX-d.originX,0,Math.max(0,window.innerWidth-geometry.w));
    geometry.y=clamp(d.y+ev.clientY-d.originY,0,Math.max(0,window.innerHeight-geometry.h));
    applyGeometry();
    d.topCandidate=ev.clientY<=topDropLimit();
    document.body.dataset.kuxFullTarget=String(d.topCandidate);
    frame.dataset.dragTarget=d.topCandidate?'full':'';
  });
  const finishDrag=ev=>{
    if(!activeDrag||activeDrag.id!==ev.pointerId)return;
    const d=activeDrag;activeDrag=null;
    delete document.body.dataset.kuxFullTarget;delete frame.dataset.dragTarget;
    if(header.hasPointerCapture(ev.pointerId))header.releasePointerCapture(ev.pointerId);
    if(!d.begun)return;
    if(ev.type==='pointerup'&&d.topCandidate)setPlacement('full');
    else if(ev.type==='pointerup'&&ev.clientX<Math.max(64,Number.parseFloat(document.body.style.getPropertyValue('--kux-assistant-left'))||0)+36)setPlacement('dock-left');
    else if(ev.type==='pointerup'&&ev.clientX>innerWidth-64)setPlacement('dock-right');
    else {save();onLayoutChange({id,mode:actualPlacement(),preferred:placement,open});}
  };'''
exact(old,new,'chat surface directional drag')

# The visual dock and actual-geometry policy share the same mobile breakpoint.
exact("  const isCompactViewport = () => window.innerWidth < 720;", "  const isCompactViewport = () => window.innerWidth < 781;", 'mobile assistant break')
# The form is a reversible option, not a tab system claiming both visible regions are exclusive.
exact("const tabbar=div('kux-chat-tabs');tabbar.setAttribute('role','tablist');tabbar.setAttribute('aria-label','Aree del modulo');", "const tabbar=div('kux-chat-tabs');tabbar.setAttribute('role','group');tabbar.setAttribute('aria-label','Chat globale e modulo facoltativo');", 'form group')
exact("tabChat.setAttribute('role','tab');tabChat.dataset.pane='chat';", "tabChat.dataset.pane='chat';", 'chat semantic button')
exact("tabForm.setAttribute('role','tab');tabForm.dataset.pane='form';", "tabForm.dataset.pane='form';", 'form semantic button')
exact("    for(const b of [tabChat,tabForm]){const sel=b.dataset.pane===pane;b.setAttribute('aria-selected',String(sel));b.tabIndex=sel?0:-1;}", "    tabChat.setAttribute('aria-pressed',String(!formOpen));tabForm.setAttribute('aria-pressed',String(formOpen));", 'reversible form accessibility')
exact('.kux-chat-form .kux-chat-tabs button{min-width:0;flex:1;text-align:center}', '.kux-chat-form .kux-chat-tabs button{min-width:0;flex:1;text-align:center}\n.kux-chat-form .kux-chat-tabs [aria-pressed="true"]{background:#173d43;color:#fff;border-color:#173d43}'.replace('\\n','\n'), 'form pressed style')
# User-facing vocabulary follows the activity/access function, not the implementation class.
exact("rail.setAttribute('aria-label','Avatar disponibili per '+ctxName(state.activeContext))", "rail.setAttribute('aria-label','Attività disponibili per '+ctxName(state.activeContext))",'rail label')
exact("notice('Premi ancora l’avatar '+intent.verb+' per chiudere la scheda; scade tra pochi secondi.');", "notice('Premi ancora l’icona '+intent.verb+' per chiudere la scheda; scade tra pochi secondi.');",'access close note')
exact("aria-label=\"Riduci ad avatar\"", "aria-label=\"Riduci a icona attività\"", 'reduce icon')
# Keep the original module's inherited size measurements and responsive UI.
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check',action='store_true',help='Verify exact generated candidate bytes without writing')
args=parser.parse_args()
if args.check:
    if not OUT.exists() or OUT.read_bytes()!=s.encode('utf-8'):
        raise SystemExit('FAIL: regenerate the v5.5 candidate; generated bytes differ')
    print('Verified byte-identical',OUT,'sha256',sha(OUT))
else:
    OUT.write_text(s,encoding='utf-8')
    print('candidate',OUT,'bytes',len(OUT.read_bytes()),'sha256',sha(OUT))
