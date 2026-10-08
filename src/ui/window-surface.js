/* K-UX-AI Window Surface — neutral UI carrier.
 * The source domain owns events, data, permission and effects. This component
 * owns only geometry, focus, attention presentation and perceptual continuity.
 * Independent original implementation inspired by source-backed THIA behaviors.
 */

const placements = new Set(['floating', 'dock-left', 'dock-right', 'full']);
const clamp = (n, lo, hi) => Math.max(lo, Math.min(hi, n));
const box = rect => ({ x: rect.left, y: rect.top, w: rect.width, h: rect.height });

export function createWindowSurface({
  id, title, subtitle = '', avatar = 'AI', host = document.body,
  content, storage = undefined, onLayoutChange = () => {},
  onPresenceChange = () => {}, initialWidth = 670, initialHeight = 535,
}) {
  if (!/^[a-z][a-z0-9-]{2,63}$/.test(id)) throw new TypeError('Stable lowercase window id required');
  if (!(content instanceof Node) || !(host instanceof Element)) throw new TypeError('Supply content Node and host Element');
  let persistentStore = storage;
  if (persistentStore === undefined) { try {persistentStore=window.localStorage;} catch {persistentStore=null;} }
  const key = `kux:window:${id}:geometry:v1`;
  const viewport = () => ({ width: window.innerWidth, height: window.innerHeight });
  const isCompactViewport = () => window.innerWidth < 720;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  let stored = null;
  try { stored = JSON.parse(persistentStore?.getItem(key) || 'null'); } catch {}
  const finite = (v, fallback) => Number.isFinite(v) ? v : fallback;
  const v = viewport();
  let geometry = {
    x: finite(stored?.geometry?.x, Math.max(12, v.width - initialWidth - 32)),
    y: finite(stored?.geometry?.y, Math.max(18, v.height - initialHeight - 36)),
    w: finite(stored?.geometry?.w, initialWidth),
    h: finite(stored?.geometry?.h, initialHeight),
  };
  let placement = placements.has(stored?.placement) ? stored.placement : 'floating';
  let open = false, closing = false, destroyed = false, animation = null, animationRun = 0;
  let activeDrag = null, activeResize = null, focusOrigin = null, cueKey = null;
  const seen = new Set();

  const root = document.createElement('div');
  root.className = 'kux-surface-root';
  root.dataset.surface = id;
  const avatarBtn = document.createElement('button');
  avatarBtn.type = 'button'; avatarBtn.className = 'kux-surface-avatar';
  avatarBtn.setAttribute('aria-label', `Apri ${title}`);
  avatarBtn.innerHTML = '<span class="kux-avatar-text"></span><span class="kux-avatar-dot" hidden></span>';
  avatarBtn.querySelector('.kux-avatar-text').textContent = avatar;
  const cue = document.createElement('div');
  cue.className = 'kux-surface-cue'; cue.hidden = true;
  const cueOpen = document.createElement('button'); cueOpen.type = 'button';
  cueOpen.className = 'kux-cue-message';
  const cueDismiss = document.createElement('button'); cueDismiss.type = 'button';
  cueDismiss.className = 'kux-cue-dismiss'; cueDismiss.textContent = '×';
  cueDismiss.setAttribute('aria-label', 'Nascondi avviso');
  cue.append(cueOpen, cueDismiss);

  const frame = document.createElement('section');
  frame.className = 'kux-surface-frame'; frame.hidden = true;
  frame.setAttribute('role', 'region');
  frame.setAttribute('aria-label', title);
  frame.dataset.mode = 'floating';
  const header = document.createElement('header'); header.className = 'kux-surface-header';
  const names = document.createElement('div'); names.className = 'kux-surface-heading';
  const hTitle = document.createElement('strong'); hTitle.textContent = title;
  const hSub = document.createElement('small'); hSub.textContent = subtitle;
  names.append(hTitle,hSub);
  const toolbar = document.createElement('div'); toolbar.className = 'kux-surface-toolbar';
  const buttons = {};
  for (const [action, glyph, tooltip] of [
    ['dock-left','◧','Aggancia a sinistra'], ['dock-right','◨','Aggancia a destra'],
    ['full','□','Pagina intera'], ['floating','▣','Ripristina finestra'],
    ['minimize','−','Riduci ad avatar'],
  ]) {
    const b = document.createElement('button');
    b.type = 'button'; b.textContent = glyph; b.title = tooltip;
    b.setAttribute('aria-label',tooltip); b.dataset.action = action;
    b.addEventListener('click',()=> action==='minimize'?minimize():setPlacement(action));
    buttons[action]=b; toolbar.append(b);
  }
  header.append(names,toolbar);
  const body = document.createElement('div'); body.className = 'kux-surface-body'; body.append(content);
  const resizeGrip = document.createElement('button'); resizeGrip.className = 'kux-surface-resize';
  resizeGrip.type = 'button'; resizeGrip.setAttribute('aria-label','Ridimensiona finestra');
  resizeGrip.title = 'Trascina per ridimensionare';
  frame.append(header,body,resizeGrip);
  root.append(avatarBtn,cue,frame); host.append(root);

  const save = () => { try {persistentStore?.setItem(key,JSON.stringify({ geometry, placement }));} catch {} };
  const normalizeGeometry = () => {
    const {width,height}=viewport();
    geometry.w=clamp(geometry.w,Math.min(300,width),Math.max(300,width-16));
    geometry.h=clamp(geometry.h,Math.min(230,height),Math.max(230,height-16));
    geometry.x=clamp(geometry.x,0,Math.max(0,width-geometry.w));
    geometry.y=clamp(geometry.y,0,Math.max(0,height-geometry.h));
  };
  function applyGeometry() {
    normalizeGeometry();
    frame.style.left = `${geometry.x}px`; frame.style.top = `${geometry.y}px`;
    frame.style.width = `${geometry.w}px`;frame.style.height = `${geometry.h}px`;
  }
  function actualPlacement(){ return isCompactViewport()?'full':placement; }
  function layout() {
    const effective = actualPlacement();
    frame.dataset.mode=effective;
    frame.classList.toggle('kux-floating',effective==='floating');
    if(effective==='floating') applyGeometry();
    else {frame.style.left='';frame.style.top='';frame.style.width='';frame.style.height='';}
    resizeGrip.hidden=effective!=='floating';
    buttons.floating.hidden=effective==='floating'||isCompactViewport();
    buttons.full.hidden=effective==='full';
    buttons['dock-left'].hidden=isCompactViewport()||effective==='dock-left';
    buttons['dock-right'].hidden=isCompactViewport()||effective==='dock-right';
    onLayoutChange({id,mode:effective,preferred:placement,open});
  }
  function cancelMotion(){animationRun++; if(animation){animation.cancel();animation=null;}}
  function geometryMotion(from,to){
    if(!frame.animate||reduced.matches)return Promise.resolve();
    const sx=clamp(from.w/Math.max(1,to.w),.055,3);
    const sy=clamp(from.h/Math.max(1,to.h),.055,3);
    const dx=from.x-to.x,dy=from.y-to.y;
    const effect=frame.animate([
      {transform:`translate(${dx}px,${dy}px) scale(${sx},${sy})`,opacity:.18,offset:0},
      {transform:'translate(0px,0px) scale(1,1)',opacity:1,offset:1},
    ],{duration:390,easing:'cubic-bezier(.18,.76,.18,1)',fill:'none'});
    animation=effect; const token=++animationRun;
    return effect.finished.catch(()=>{}).then(()=>{if(token===animationRun)animation=null;});
  }
  function avatarToWindow(entering=true){
    if(!frame.animate||reduced.matches)return Promise.resolve();
    const a=box(avatarBtn.getBoundingClientRect());
    const f=box(frame.getBoundingClientRect());
    const start={x:a.x,y:a.y,w:a.w,h:a.h};
    const end={x:f.x,y:f.y,w:f.w,h:f.h};
    const sx=clamp(start.w/Math.max(1,end.w),.04,.95);
    const sy=clamp(start.h/Math.max(1,end.h),.04,.95);
    const keys=[
      {transform:`translate(${start.x-end.x}px,${start.y-end.y}px) scale(${sx},${sy})`,opacity:.20},
      {transform:'translate(0px,0px) scale(1,1)',opacity:1},
    ];
    const effect=frame.animate(entering?keys:keys.reverse(),{duration:440,easing:'cubic-bezier(.18,.76,.18,1)',fill:'forwards'});
    animation=effect; const token=++animationRun;
    return effect.finished.catch(()=>{}).then(()=>{if(token===animationRun){animation=null;effect.cancel();}});
  }
  function dismissCue(){cue.hidden=true;avatarBtn.querySelector('.kux-avatar-dot').hidden=true;cueKey=null;}
  async function show(trigger=avatarBtn){
    if(destroyed||(open&&!closing))return;
    cancelMotion();closing=false;open=true;focusOrigin=trigger;
    dismissCue(); frame.hidden=false;layout();
    onPresenceChange({id,open:true,mode:actualPlacement()});
    await avatarToWindow(true);
    if(open)toolbar.querySelector('button:not([hidden])')?.focus({preventScroll:true});
  }
  async function minimize(){
    if(destroyed||!open||closing)return;
    closing=true;cancelMotion();
    const closingMotion=avatarToWindow(false);
    const token=animationRun;
    await closingMotion;
    if(destroyed||!open||!closing||token!==animationRun)return;
    frame.hidden=true;open=false;closing=false;
    onPresenceChange({id,open:false,mode:actualPlacement()});
    (focusOrigin?.isConnected?focusOrigin:avatarBtn).focus({preventScroll:true});
  }
  function setPlacement(next){
    if(destroyed||!placements.has(next))return;
    // A layout control may itself disappear after being used (full/dock).
    // Transfer focus to a still-visible control before the document body steals it.
    const focusedBefore=document.activeElement;
    const focusWasInside=frame.contains(focusedBefore);
    cancelMotion();const before=frame.hidden?null:box(frame.getBoundingClientRect());
    placement=next;layout();save();
    if(focusWasInside && (focusedBefore.hidden || !frame.contains(document.activeElement))){
      toolbar.querySelector('button:not([hidden])')?.focus({preventScroll:true});
    }
    if(open&&before){const after=box(frame.getBoundingClientRect());geometryMotion(before,after);}
  }
  function updateCue(event) {
    if(!event||typeof event.id!=='string'||!event.id.trim()||typeof event.text!=='string') throw new TypeError('Attributed event identity and text required');
    if(seen.has(event.id))return false;
    seen.add(event.id);
    if(seen.size>150)seen.delete(seen.values().next().value);
    if(!open){cueKey=event.id;cueOpen.textContent=event.text.slice(0,240);cue.hidden=false;avatarBtn.querySelector('.kux-avatar-dot').hidden=false;}
    return true;
  }
  // Pointer-owned movement has no easing. Geometry is only persisted after release.
  header.addEventListener('pointerdown',ev=>{
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
  };
  header.addEventListener('pointerup',finishDrag);header.addEventListener('pointercancel',finishDrag);
  resizeGrip.addEventListener('pointerdown',ev=>{
    if(ev.button!==0||actualPlacement()!=='floating')return;
    cancelMotion();activeResize={id:ev.pointerId,x:ev.clientX,y:ev.clientY,w:geometry.w,h:geometry.h};
    resizeGrip.setPointerCapture(ev.pointerId);ev.preventDefault();
  });
  resizeGrip.addEventListener('pointermove',ev=>{
    if(!activeResize||activeResize.id!==ev.pointerId)return;
    geometry.w=clamp(activeResize.w+ev.clientX-activeResize.x,300,window.innerWidth-geometry.x);
    geometry.h=clamp(activeResize.h+ev.clientY-activeResize.y,240,window.innerHeight-geometry.y);
    applyGeometry();
  });
  resizeGrip.addEventListener('keydown',ev=>{
    if(actualPlacement()!=='floating')return;
    const step=ev.shiftKey?24:8;
    if(ev.key==='ArrowRight')geometry.w+=step;
    else if(ev.key==='ArrowLeft')geometry.w-=step;
    else if(ev.key==='ArrowDown')geometry.h+=step;
    else if(ev.key==='ArrowUp')geometry.h-=step;
    else return;
    ev.preventDefault();applyGeometry();save();
  });
  const finishResize=ev=>{
    if(!activeResize||activeResize.id!==ev.pointerId)return;
    activeResize=null;if(resizeGrip.hasPointerCapture(ev.pointerId))resizeGrip.releasePointerCapture(ev.pointerId);
    save();onLayoutChange({id,mode:actualPlacement(),preferred:placement,open});
  };
  resizeGrip.addEventListener('pointerup',finishResize);resizeGrip.addEventListener('pointercancel',finishResize);
  avatarBtn.addEventListener('click',()=>show(avatarBtn));cueOpen.addEventListener('click',()=>show(cueOpen));
  cueDismiss.addEventListener('click',dismissCue);
  const onKeys=ev=>{
    if(!open||!frame.contains(document.activeElement))return;
    if(ev.key==='Escape'){ev.preventDefault();if(actualPlacement()==='full'&&!isCompactViewport())setPlacement('floating');else minimize();}
  };
  frame.addEventListener('keydown',onKeys);
  const onWindowResize=()=>{if(!destroyed){layout();}};
  window.addEventListener('resize',onWindowResize);
  save();layout();
  return {
    element:frame, contentElement:body, avatar:avatarBtn,
    open:show, minimize, setPlacement, notify:updateCue, dismissCue,
    snapshot:()=>({id,open,preferred:placement,mode:actualPlacement(),geometry:{...geometry},notificationId:cueKey}),
    destroy(){if(destroyed)return;destroyed=true;cancelMotion();window.removeEventListener('resize',onWindowResize);root.remove();},
  };
}
