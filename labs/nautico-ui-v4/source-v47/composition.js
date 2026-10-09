/* K-UX-AI v4.7 — one source-owned compositional receiver; no provider/AI installed. */
(()=>{'use strict';
 const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
 const escapeHTML=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 function safeStore(key,write){try{return write?localStorage.setItem(key,write):localStorage.getItem(key)}catch{return null}}
 function mountSidebar({aside,dock,grip,render,reflow,getSummary,onChanged=()=>{}}){
  const button=document.createElement('button');button.type='button';button.id='kuxRailToggle';button.className='kux-rail-toggle';
  button.setAttribute('aria-controls','avatarDock');aside.insertBefore(button,aside.firstChild);
  let expanded=safeStore('kux:v46:sidebar')==='expanded';
  const collapsedWidth=86; // stable icon affordance: not a resizable miniature preview
  let expandedWidth=clamp(Number(safeStore('kux:v47:expandedWidth'))||285,255,395);
  let current=expanded?expandedWidth:collapsedWidth;
  function apply(){current=expanded?expandedWidth:collapsedWidth;document.body.dataset.kuxRailExpanded=String(expanded);
   document.documentElement.style.setProperty('--kux-avatar-rail',current+'px');
   button.textContent=expanded?'‹ Riduci':'›';button.setAttribute('aria-expanded',String(expanded));
   button.setAttribute('aria-label',expanded?'Riduci la sidebar alle icone':'Espandi la sidebar con le anteprime');
   button.title=button.getAttribute('aria-label');
   grip.hidden=!expanded;
   grip.setAttribute('aria-valuemin','255');grip.setAttribute('aria-valuemax','395');
   grip.setAttribute('aria-valuenow',String(current));grip.setAttribute('aria-valuetext',current+' pixel');
   safeStore('kux:v46:sidebar',expanded?'expanded':'collapsed');
   if(expanded)safeStore('kux:v47:expandedWidth',String(expandedWidth));
  }
  button.addEventListener('click',()=>{expanded=!expanded;onChanged(expanded);apply();render();reflow();button.focus({preventScroll:true});});
  const setWidth=n=>{if(!expanded)return;expandedWidth=clamp(Math.round(n),255,395);apply();reflow();};
  grip.addEventListener('pointerdown',event=>{if(event.button!==0||!expanded)return;event.preventDefault();const start=event.clientX,w=current,id=event.pointerId;grip.setPointerCapture(id);
   const move=e=>{if(e.pointerId===id)setWidth(w+e.clientX-start)};
   const finish=e=>{if(e.pointerId!==id)return;grip.removeEventListener('pointermove',move);grip.removeEventListener('pointerup',finish);grip.removeEventListener('pointercancel',finish);if(grip.hasPointerCapture(id))grip.releasePointerCapture(id)};
   grip.addEventListener('pointermove',move);grip.addEventListener('pointerup',finish);grip.addEventListener('pointercancel',finish);
  });
  grip.addEventListener('keydown',e=>{if(!expanded||!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;e.preventDefault();setWidth(e.key==='Home'?255:e.key==='End'?395:current+(e.key==='ArrowRight'?(e.shiftKey?20:10):-(e.shiftKey?20:10)))});
  apply();
  return {expanded:()=>expanded,width:()=>current,decorate:(entry,intent,context,alert)=>{
    const data=getSummary(intent,context);
    const info=document.createElement('span');info.className='kux-avatar-detail';info.setAttribute('aria-hidden','true');
    const heading=document.createElement('strong');heading.textContent=intent.verb;
    const name=document.createElement('small');name.textContent=data.context+' · '+data.subtitle;
    const secondary=document.createElement('em');secondary.textContent=alert?'Segnale demo da esaminare':data.unknown;
    info.append(heading,name,secondary);entry.querySelector('.avatar-button')?.append(info);
  }};
 }
 function mountDivider({stage,reflow}){
  const grip=document.createElement('button');grip.type='button';grip.id='kuxFocalDivider';grip.className='kux-focal-divider';
  grip.setAttribute('role','separator');grip.setAttribute('aria-label','Regola il rapporto fra scheda principale e complementari');grip.setAttribute('aria-orientation','vertical');
  grip.setAttribute('aria-valuemin','27');grip.setAttribute('aria-valuemax','60');stage.append(grip);
  let value=clamp(Number(safeStore('kux:v46:secondaryPct'))||44,27,60);
  function update(p){value=clamp(Math.round(p),27,60);stage.style.setProperty('--kux-secondary-ratio',value+'%');grip.setAttribute('aria-valuenow',String(value));grip.setAttribute('aria-valuetext',value+'% dello spazio operativo per attività complementari');safeStore('kux:v46:secondaryPct',String(value))}
  update(value);
  grip.addEventListener('pointerdown',e=>{if(e.button!==0)return;e.preventDefault();const id=e.pointerId;grip.setPointerCapture(id);grip.dataset.dragging='true';
   const move=ev=>{if(ev.pointerId!==id)return;const box=stage.getBoundingClientRect();update(100*(box.right-ev.clientX)/Math.max(1,box.width));};
   const done=ev=>{if(ev.pointerId!==id)return;grip.removeEventListener('pointermove',move);grip.removeEventListener('pointerup',done);grip.removeEventListener('pointercancel',done);grip.dataset.dragging='false';if(grip.hasPointerCapture(id))grip.releasePointerCapture(id);reflow();};
   grip.addEventListener('pointermove',move);grip.addEventListener('pointerup',done);grip.addEventListener('pointercancel',done);
  });
  grip.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;e.preventDefault();update(e.key==='Home'?27:e.key==='End'?60:value+(e.key==='ArrowLeft'?(e.shiftKey?5:2):-(e.shiftKey?5:2)));reflow();});
  const sync=(show)=>{grip.hidden=!show};sync(false);
  return {sync,value:()=>value};
 }
 function createDiscussions(){
  const entries=new Map(),proposals=[];
  const get=id=>{if(!entries.has(id))entries.set(id,[]);return entries.get(id)};
  const getMessages=id=>[...get(id)];
  function post(id,text,context){
   const t=String(text||'').trim().slice(0,3000);if(!t)return null;
   const messages=get(id),source=String(context.source||'Demo local').slice(0,200);
   const stem=id.replace(/[^A-Za-z0-9]/g,'').slice(0,10);
   const user={id:stem+'-U'+(messages.length+1),role:'operator',text:t,owner:id,context:context.name,source:'Operatore locale',kind:'local-entry'};
   // Derived source facts: deliberately not an AI-generated response.
   const lookup=t.toLowerCase();
   const info=lookup.includes('font')?`Fonte illustrativa: ${source}. Non è un documento di cantiere.`:
    lookup.includes('competenz')?`Questa superficie può ricevere competenze pertinenti, ma nessun Section Kernel o AI è collegato. Qualificare con il relativo owner.`:
    lookup.includes('pass')||lookup.includes('continu')?`Continuazione illustrativa per ${context.name}: ${context.next}`:
    `Dal contesto ${context.name}: ${context.goal} Punto da qualificare: ${context.unknown}`;
   const result={id:stem+'-S'+(messages.length+2),role:'source-readback',text:info,owner:id,context:context.name,source,kind:'deterministic-fixture',eligibleForProposal:false};
   messages.push(user,result);return {user,result};
  }
  function propose(id){const arr=get(id),last=[...arr].reverse().find(m=>m.role==='source-readback');if(!last)return null;
   const existing=proposals.find(p=>p.owner===id&&p.origin===last.id);if(existing)return existing;
   const p={id:'PROP-'+String(proposals.length+1).padStart(3,'0'),owner:id,origin:last.id,source:last.source,context:last.context,status:'candidate_not_assimilated',assertion:last.text};
   proposals.push(p);return p;
  }
  function renderHTML(id,context,draft=''){
    const msgs=getMessages(id);
    return `<div class="kux-section-discussion"><div class="kux-section-source"><strong>Conversazione contestuale · senza AI collegata</strong><p>Lettura dimostrativa della fonte: ${escapeHTML(context.source)}. Le eventuali proposte sono candidate, non competenze assimilate.</p></div>
    <div class="kux-section-messages" role="log" aria-label="Conversazione locale della sezione">${msgs.map(m=>`<article class="kux-section-msg" data-role="${m.role}"><strong>${m.role==='operator'?'Operatore':'Lettura dal caso demo · non AI'}</strong><p>${escapeHTML(m.text)}</p><small>${escapeHTML(m.source)} · ${escapeHTML(m.context)}</small></article>`).join('')||'<p>Nessun contributo ancora registrato.</p>'}</div>
    <label for="section-text-${escapeHTML(id)}">Domanda o contributo della sezione</label><textarea id="section-text-${escapeHTML(id)}" class="kux-section-editor" placeholder="Scrivi un messaggio contestuale...">${escapeHTML(draft)}</textarea>
    <div class="kux-section-actions"><button type="button" data-section="ask">Registra e leggi il caso</button><button type="button" data-section="candidate" ${msgs.some(m=>m.role==='source-readback')?'':'disabled'}>Prepara candidato di competenza</button><button type="button" data-section="export">Esporta contributi</button></div>
    <div class="kux-candidate-indicator">Candidate della sessione: ${proposals.filter(p=>p.owner===id).length}. Nessuna assimilazione automatica · controller AI assente · owner da qualificare.</div></div>`;
  }
  function exportPacket(id){return {schema:'kux.section.learning-candidates.v0.1',kind:'local-demo-export',owner:id,createdAt:new Date().toISOString(),messages:getMessages(id),candidates:proposals.filter(p=>p.owner===id),authority:'none',assimilated:false}}
  return {getMessages,post,propose,renderHTML,exportPacket,proposals:()=>proposals.map(p=>({...p})),summary:()=>({sessions:entries.size,proposals:proposals.length,assimilated:0})};
 }
 window.KUX_V46=Object.freeze({mountSidebar,mountDivider,createDiscussions,escapeHTML});
})();

