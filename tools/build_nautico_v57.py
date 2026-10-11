"""Build K-UX-AI v5.7 from the exact v5.6 standalone laboratory prototype.

    python tools/build_nautico_v57.py [--check]

Preserves the v5.6 baseline; output is another standalone candidate. No kernel
receiver, permissions, agent or site host is installed by this transformation.
"""
from __future__ import annotations
import argparse, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
BASE=ROOT/'labs/nautico-ui-v4/18-griglia-situated-v56.html'
OUT=ROOT/'labs/nautico-ui-v4/19-griglia-rail-free-v57.html'
BASE_SHA='8bb3939c44ab46bdfe7fff14beea8b63f8ad07afa723bd595e423022dcc3c617'
OUTPUT_SHA='e733a306b85f2ac3abefe20fa6801aa73b2b178e7c108b40d05bb07c5021db2d'

STYLE='''
/* v5.7 — legibility follows the receiving person's working surface. Titles unchanged. */
body{font-size:15px}
.module-content p,.module-content .data-row,.module-content label,.module-content .event-explain,
.kux-section-surface p,.kux-section-source p,.kux-section-discussion p{font-size:14px;line-height:1.5}
.module-content .source-note,.module-content .mini-caps,.module-content .status-chip,
.module-content .form-actions button,.module-content .small-button,.module-content .chip-button,
.module-foot,.module-foot button,.module-subtitle,.kux-section-tabs button,
.kux-section-source small,.kux-section-msg small,.module-content small{font-size:12px}
.dock-caption,.kux-dock-context,.kux-dock-count,.kux-avatar-detail small,.kux-avatar-detail em{font-size:11px!important}
.topbar button,.work-toolbar button,.kux-context-meta small,.kux-action-caption,
.kux-context-choice small,.focus-menu button,.kux-context-plan-count{font-size:13px}
.work-footer,.footer-identity,.footer-controls button{font-size:12px}
.kux-activity-edge{font-size:12px}
body[data-kux-screen="work"] .module .module-title{font-size:14px}
body[data-kux-screen="work"] .module .module-subtitle{font-size:12px!important}
.module-content textarea,.module-content input,.kux-section-editor,.kux-section-discussion textarea{font-size:14px}
body[data-kux-activities="previews"] #kuxRailToggle{position:sticky;top:0;z-index:4}
/* The sidebar has one visual state: hidden, icon rail, or expanded preview rail.
   Hover from the edge is only a transient icon-rail projection. */
body[data-kux-screen="work"][data-kux-activities="previews"] .intent-dock{
 position:relative!important;top:auto!important;bottom:auto!important;left:auto!important;
 width:var(--kux-avatar-rail,285px)!important;min-width:255px!important;
 max-width:395px!important;flex:0 0 var(--kux-avatar-rail,285px)!important;
 height:auto!important;visibility:visible!important;overflow-y:auto!important;}
body[data-kux-activities="previews"] .kux-activity-toggle,
body[data-kux-activities="peek"] .kux-rail-toggle,
body[data-kux-activities="previews"] .kux-activity-edge,
body[data-kux-activities="icons"] .kux-activity-edge{display:none!important}
body[data-kux-activities="peek"] .kux-activity-edge{display:block!important;left:0!important}
body[data-kux-activities="peek"] .kux-activity-toggle{display:grid!important}
body[data-kux-activities="peek"] .intent-dock{padding:9px 8px 12px!important}
body[data-kux-activities="peek"] .avatar-dock{overflow-y:visible}
body[data-kux-activities="previews"] .kux-rail-toggle{display:block!important}
body[data-kux-screen="work"][data-fullscreen-panel="true"][data-kux-activities="previews"] .intent-dock{
 position:fixed!important;top:0!important;left:0!important;height:100dvh!important;z-index:10003!important}
@media(max-width:760px){
 body[data-kux-activities="previews"] .intent-dock{display:none!important}
 .module-content p,.module-content .data-row,.module-content label{font-size:13px}
 .module-foot,.module-foot button{font-size:11px}
}
'''

OLD_RAIL='''let activitiesMode='pinned',activitiesPeekTimer=null;
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
activityEdge.addEventListener('pointerleave',()=>{if(activitiesMode!=='peek')return;activitiesPeekTimer=setTimeout(()=>{if(!activityRail.matches(':hover')&&!activityEdge.matches(':hover'))setActivitiesMode('hidden');},260);});'''

NEW_RAIL='''// A single presentation state machine: hidden -> icons -> previews.
// Edge hover reveals only icons temporarily. Preview expansion requires a click.
let activitiesMode='icons',activitiesPeekTimer=null;
const railVisibility=document.createElement('button');railVisibility.id='railVisibility';railVisibility.type='button';railVisibility.className='kux-activity-toggle';railVisibility.title='Nascondi o fissa la barra Attività';railVisibility.setAttribute('aria-label','Nascondi barra delle attività');railVisibility.textContent='‹';
const activityCount=document.createElement('small');activityCount.id='activityCount';activityCount.className='kux-dock-count';activityCount.textContent='10 disponibili';
const activityEdge=document.createElement('button');activityEdge.type='button';activityEdge.id='activitiesEdge';activityEdge.className='kux-activity-edge';activityEdge.textContent='Attività';activityEdge.setAttribute('aria-label','Richiama la barra delle attività');activityEdge.setAttribute('aria-expanded','false');
const activityRail=document.querySelector('.intent-dock');activityRail.insertBefore(railVisibility,activityRail.querySelector('.dock-caption'));activityRail.insertBefore(activityCount,shell.dock);document.querySelector('#app').append(activityEdge);
function updateActivitiesRail(){
 const onCanvas=state.screen==='work'&&!matchMedia('(max-width:760px)').matches;
 const width=onCanvas&&(activitiesMode==='icons'||activitiesMode==='previews')?(sidebarCtrl?.width()||86):0;
 document.body.dataset.kuxActivities=activitiesMode;
 document.body.style.setProperty('--kux-full-rail',Math.round(width)+'px');
 activityRail.inert=activitiesMode==='hidden';activityRail.setAttribute('aria-hidden',activitiesMode==='hidden'?'true':'false');
 railVisibility.textContent=activitiesMode==='peek'?'↦':'‹';
 railVisibility.setAttribute('aria-label',activitiesMode==='peek'?'Fissa le icone delle attività':'Nascondi la barra delle attività');
 railVisibility.setAttribute('aria-expanded',String(activitiesMode!=='hidden'));
 activityEdge.setAttribute('aria-expanded',String(activitiesMode==='peek'));
 const shown=state.panels.filter(p=>p.context===state.activeContext&&!p.minimized).length;
 activityCount.textContent='10 accessi · '+shown+' nel campo';activityCount.title='10 attività disponibili; '+shown+' schede aperte in '+ctxName(state.activeContext);
}
function setActivitiesMode(next){
 if(!['hidden','peek','icons','previews'].includes(next)||activitiesMode===next)return;
 clearTimeout(activitiesPeekTimer);cancelDockPeekTimers?.();
 if(next==='hidden')closeQuickPeek?.();
 activitiesMode=next;updateActivitiesRail();
 if(state.screen==='work'){relocateAssistantAvatar();placePanels();syncAssistantDockBounds();}
}
railVisibility.addEventListener('click',()=>{
 if(activitiesMode==='peek'){setActivitiesMode('icons');railVisibility.focus({preventScroll:true});}
 else{setActivitiesMode('hidden');activityEdge.focus({preventScroll:true});}
});
activityEdge.addEventListener('click',()=>setActivitiesMode('icons'));
activityEdge.addEventListener('pointerenter',e=>{if(e.pointerType==='mouse'&&activitiesMode==='hidden')setActivitiesMode('peek');});
activityRail.addEventListener('pointerenter',()=>clearTimeout(activitiesPeekTimer));
function closeTransientActivities(){
 if(activitiesMode!=='peek')return;
 activitiesPeekTimer=setTimeout(()=>{
  if(activitiesMode==='peek'&&!activityRail.matches(':hover')&&!activityRail.contains(document.activeElement))setActivitiesMode('hidden');
 },260);
}
activityRail.addEventListener('pointerleave',closeTransientActivities);
activityEdge.addEventListener('pointerleave',closeTransientActivities);'''

OLD_DRAG='''function startDrag(e,p){
 if(e.target.closest('button')||e.button!==0||shell.stage.clientWidth<700)return;
 const head=e.currentTarget,downX=e.clientX,downY=e.clientY,pointer=e.pointerId;
 let engaged=false,start=null;
 head.setPointerCapture(pointer);
 const move=ev=>{
  if(ev.pointerId!==pointer)return;
  if(!engaged){
   if(Math.hypot(ev.clientX-downX,ev.clientY-downY)<8)return;
   engaged=true;
   focusPanel(p,{force:true});
   const bounds=shell.stage.getBoundingClientRect();
   if(state.layout!=='free')switchToFreeFromCurrent();
   p.manualPosition=true;
   if(p.dock||p.maximized){
    const w=limit(bounds.width*.45,Math.min(250,bounds.width-12),Math.min(510,bounds.width-12));
    const h=limit(bounds.height*.7,Math.min(200,bounds.height-12),Math.min(450,bounds.height-12));
    Object.assign(p,screenRect({x:ev.clientX-bounds.left-Math.min(150,w*.3),y:ev.clientY-bounds.top-32,w,h}));p.dock=null;p.maximized=false;
   }
   p.el.getAnimations().forEach(animation=>animation.cancel());
   start={x:ev.clientX,y:ev.clientY,x0:p.x,y0:p.y};
   dragData={p};p.el.dataset.interacting='true';p.el.dataset.dragging='true';
  }
  if(!start)return;
  p.x=start.x0+ev.clientX-start.x;p.y=start.y0+ev.clientY-start.y;
  Object.assign(p,screenRect(p));moduleStyles(p,screenRect(p));
  const stage=shell.stage.getBoundingClientRect(),x=ev.clientX-stage.left;
  const side=x<52?'left':x>stage.width-52?'right':null;
  const fullCandidate=ev.clientY<=Math.max(54,Math.min(94,window.innerHeight*.11));
  start.fullCandidate=fullCandidate;document.body.dataset.kuxFullTarget=String(fullCandidate);p.el.dataset.dragTarget=fullCandidate?'full':'';
  previewDock(fullCandidate?null:side);start.edge=fullCandidate?null:side;
 };'''
NEW_DRAG='''function startDrag(e,p){
 if(e.target.closest('button')||e.button!==0||shell.stage.clientWidth<700)return;
 const head=e.currentTarget,downX=e.clientX,downY=e.clientY,pointer=e.pointerId;
 // Preserve the actual pointer-to-rendered-card offset, even after focus change,
 // CSS motion, a right-side placement or a switch from tiled to free.
 const firstVisual=p.el.getBoundingClientRect();
 const firstStage=shell.stage.getBoundingClientRect();
 const initialScaleX=shell.stage.clientWidth/Math.max(1,firstStage.width);
 const initialScaleY=shell.stage.clientHeight/Math.max(1,firstStage.height);
 let engaged=false,start=null;
 head.setPointerCapture(pointer);
 const move=ev=>{
  if(ev.pointerId!==pointer)return;
  if(!engaged){
   if(Math.hypot(ev.clientX-downX,ev.clientY-downY)<8)return;
   engaged=true;
   focusPanel(p,{force:true});
   if(state.layout!=='free')switchToFreeFromCurrent();
   p.el.getAnimations().forEach(animation=>animation.cancel());
   p.manualPosition=true;
   const detached=!!(p.dock||p.maximized);
   const bounds=shell.stage.getBoundingClientRect();
   const sx=shell.stage.clientWidth/Math.max(1,bounds.width),sy=shell.stage.clientHeight/Math.max(1,bounds.height);
   const original={x:(firstVisual.left-firstStage.left)*initialScaleX,
    y:(firstVisual.top-firstStage.top)*initialScaleY,
    w:firstVisual.width*initialScaleX,h:firstVisual.height*initialScaleY};
   const w=detached?limit(bounds.width*sx*.45,Math.min(250,shell.stage.clientWidth-12),Math.min(510,shell.stage.clientWidth-12)):original.w;
   const h=detached?limit(bounds.height*sy*.7,Math.min(200,shell.stage.clientHeight-12),Math.min(450,shell.stage.clientHeight-12)):original.h;
   const grabX=detached?Math.min(Math.max(28,(downX-firstVisual.left)*initialScaleX),w-28):(downX-firstVisual.left)*initialScaleX;
   const grabY=detached?32:(downY-firstVisual.top)*initialScaleY;
   p.dock=null;p.maximized=false;
   Object.assign(p,screenRect({x:original.x,y:original.y,w,h}));
   start={grabX,grabY};
   dragData={p};p.el.dataset.interacting='true';p.el.dataset.dragging='true';
  }
  if(!start)return;
  const stage=shell.stage.getBoundingClientRect();
  const sx=shell.stage.clientWidth/Math.max(1,stage.width),sy=shell.stage.clientHeight/Math.max(1,stage.height);
  const x=(ev.clientX-stage.left)*sx-start.grabX;
  const y=(ev.clientY-stage.top)*sy-start.grabY;
  Object.assign(p,screenRect({...p,x,y}));moduleStyles(p,screenRect(p));
  const edgeX=ev.clientX-stage.left;
  const side=edgeX<52?'left':edgeX>stage.width-52?'right':null;
  const fullCandidate=ev.clientY<=Math.max(54,Math.min(94,window.innerHeight*.11));
  start.fullCandidate=fullCandidate;document.body.dataset.kuxFullTarget=String(fullCandidate);p.el.dataset.dragTarget=fullCandidate?'full':'';
  previewDock(fullCandidate?null:side);start.edge=fullCandidate?null:side;
 };'''

PATCHES=[
 ('<title>MAIOS · K-UX-AI — Griglia del fare v5.6 · Canvas guidato</title>',
  '<title>MAIOS · K-UX-AI — Griglia del fare v5.7 · Leggibilità e attività</title>'),
 ("version:'lab-2026-10-11-r5.6'", "version:'lab-2026-10-11-r5.7'"),
 ('</head>', '<style id="kux-v57-clarity-and-activity-rail">'+STYLE+'</style>\n</head>'),
 ("button.textContent=expanded?'‹ Riduci':'›';button.setAttribute('aria-expanded',String(expanded));",
  "button.textContent=expanded?'‹ Icone':'Anteprime ›';button.setAttribute('aria-expanded',String(expanded));"),
 (OLD_RAIL,NEW_RAIL),
 ("onChanged:(expanded)=>{cancelDockPeekTimers();if(expanded&&$('kuxPeek').dataset.hover==='true')closeQuickPeek();}",
  "onChanged:(expanded)=>{activitiesMode=expanded?'previews':'icons';updateActivitiesRail();cancelDockPeekTimers();if(expanded&&$('kuxPeek').dataset.hover==='true')closeQuickPeek();}"),
 ("  }});\n}\n\nfunction orderByUse()", "  }});\n if(sidebarCtrl?.expanded()){activitiesMode='previews';updateActivitiesRail();}\n}\n\nfunction orderByUse()"),
 ("if(sidebarCtrl?.expanded()||matchMedia('(hover:none)').matches)return;",
  "if(sidebarCtrl?.expanded()||activitiesMode==='peek'||activitiesMode==='hidden'||matchMedia('(hover:none)').matches)return;"),
 ("const railRight=r&&getComputedStyle(rail).display!=='none'?Math.round(r.right):0;",
  "const railRight=(activitiesMode==='icons'||activitiesMode==='previews')&&r&&getComputedStyle(rail).display!=='none'?Math.round(r.right):0;"),
 (OLD_DRAG,NEW_DRAG),
]

def sha(raw):return hashlib.sha256(raw).hexdigest()
def generate():
 raw=BASE.read_bytes();assert sha(raw)==BASE_SHA,(sha(raw),BASE_SHA)
 text=raw.decode('utf-8')
 for i,(before,after) in enumerate(PATCHES,1):
  n=text.count(before)
  if n!=1:raise RuntimeError(f'Patch {i} expected once, found {n}: {before[:85]}')
  text=text.replace(before,after,1)
 output=text.encode('utf-8')
 if OUTPUT_SHA!='__PENDING__' and sha(output)!=OUTPUT_SHA:raise RuntimeError('v5.7 builder output mismatch')
 return output
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');a=parser.parse_args();raw=generate()
 if a.check:
  assert OUT.read_bytes()==raw,'Candidate differs'
 else:OUT.write_bytes(raw)
 print('v5.7',len(raw),'SHA256',sha(raw))
