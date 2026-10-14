/* Public hosting-kernel adaptation of the selected GPT Griglia.
 * Geometry, focus, rail, drafts and gestures remain in that source engine.
 * A hosting kernel owns its profile and any actual domain effects. */
(() => {
  'use strict';
  const profile = () => window.__UXAI_CONFIG__.profile;
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const row = (name, value, tone = '') => `<div class="data-row"><strong>${esc(name)}</strong><span class="status-chip ${esc(tone)}">${esc(value)}</span></div>`;
  const threads = new Map();
  const thread = id => { if (!threads.has(id)) threads.set(id, []); return threads.get(id); };
  let core, session = '', target = '', sharedSequence = 0, completedRequests = 0;
  const uuid = () => globalThis.crypto?.randomUUID?.() || `public-${Date.now()}-${++sharedSequence}`;
  const transportSession = uuid();
  const notify = id => document.dispatchEvent(new CustomEvent('kux:public-dialogue', {detail: {id}}));
  function focusActions(actions) {
    const p=profile();
    return (actions||[]).filter(a=>a?.kind==='focus_section'&&typeof a.target==='string').map(a=>{
      const key=a.target.slice(1), target=Object.hasOwn(p.actionAliases||{},key)?p.actionAliases[key]:key;
      return a.target.startsWith('#')&&Object.hasOwn(p.targets,target)?{target,label:String(a.label||'Apri la vista').slice(0,80)}:null;
    }).filter(Boolean);
  }
  const actionButtons = actions => focusActions(actions).map(a=>`<button type="button" class="small-button" data-kux-ai-target="${esc(a.target)}">${esc(a.label)} ↗</button>`).join('');

  function publicContext(context, intent) {
    const p = profile(), c = p.contexts[context] || p.contexts.poppa;
    const marker = Object.entries(p.targets).find(([, v]) => v.context === context && v.intent === intent)?.[0] || '';
    return {path: p.pagePath, hash: marker ? '#' + marker : '#kernel-guide', title: p.home.title,
      surface: p.id, expression: 'product', h1: p.home.title, headings: [c.name, c.subtitle],
      active_label: c.name + ' · ' + intent, active_marker: marker,
      visible_text: [c.goal, 'Fonte pubblica: ' + c.source, 'Punto aperto: ' + c.unknown, 'Seguito: ' + c.next].join('\n')};
  }

  async function ask(text, context, intent, owner) {
    const messages = thread(owner), message = String(text || '').trim().slice(0, 6000);
    if (!message) return {accepted: false, message: 'Scrivi una domanda prima di inviarla.'};
    const history = messages.filter(x => ['user','assistant'].includes(x.role) && !['pending','unavailable'].includes(x.kind)).slice(-12).map(x => ({role:x.role,content:x.text}));
    if(history.at(-1)?.role==='user' && history.at(-1).content===message)history.pop();
    const requestId = uuid();
    const response = await fetch('/api/setup/v1/assistant/site-turn', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({
      schema:'maios.public-assistant-request.v1',request_id:requestId,session_id:transportSession,
      locale:profile().locale || 'it',message,history,context:publicContext(context,intent),
      allowed_action_kinds:['focus_section'],processing_consent:{external_processing:true,disclosure_id:'maios-ai-processing-footer-v1'}
    })});
    let body; try { body = await response.json(); } catch { throw new Error('Il collegamento MAIOS AI non è disponibile in questo ambiente.'); }
    if (!response.ok || typeof body.message !== 'string' || !body.message.trim())
      throw new Error(response.status === 429 ? 'L’assistente è occupato. Puoi riprovare fra poco.' : 'Il collegamento MAIOS AI non è disponibile in questo ambiente. La bozza resta nella scheda.');
    completedRequests++;
    return {accepted:true,message:body.message,requestId,proposedActions:Array.isArray(body.proposed_actions)?body.proposed_actions:[]};
  }

  function createDiscussions() {
    const entries = new Map(), proposals = [];
    const get = id => { if(!entries.has(id))entries.set(id,[]);return entries.get(id); };
    function post(id,text,context) {
      const clean=String(text||'').trim().slice(0,3000);if(!clean)return null;
      const c=get(id), user={id:uuid(),role:'operator',text:clean,owner:id,context:context.name,source:'Contributo della persona',kind:'explicit-question'};
      const pending={id:uuid(),role:'pending',text:'MAIOS AI sta leggendo la domanda e il contesto di questa scheda.',owner:id,context:context.name,source:context.source,kind:'pending'};
      c.push(user,pending);
      const panel=core?.state.panels.find(x=>x.id===id);
      const contextId=panel?.context || Object.keys(profile().contexts).find(k=>profile().contexts[k].name===context.name) || 'poppa';
      const owner='section-'+id, h=thread(owner);h.push({role:'user',text:clean});
      ask(clean,contextId,panel?.intent||'capire',owner).then(result=>{
        Object.assign(pending,{role:'assistant',text:result.message,kind:'maios-response',eligibleForProposal:true,proposedActions:result.proposedActions,requestId:result.requestId});
        h.push({role:'assistant',text:result.message});notify(id);
      }).catch(error=>{Object.assign(pending,{role:'unavailable',text:error.message,kind:'unavailable',eligibleForProposal:false});notify(id);});
      return {user,result:pending};
    }
    function propose(id) {
      const last=[...get(id)].reverse().find(m=>m.eligibleForProposal);if(!last)return null;
      const existing=proposals.find(x=>x.origin===last.id);if(existing)return existing;
      const proposal={id:uuid(),owner:id,origin:last.id,source:last.source,context:last.context,status:'proposed_not_applied',assertion:last.text};
      proposals.push(proposal);return proposal;
    }
    function renderHTML(id,context,draft='') {
      const messages=get(id);
      return `<div class="kux-section-discussion"><div class="kux-section-source"><strong>Dialogo di questa scheda</strong><p>Domanda e risposta restano collegate a ${esc(context.name)}. Una proposta può continuare nel kernel che lavora sul caso.</p></div><div class="kux-section-messages" role="log" aria-label="Dialogo della scheda">${messages.map(m=>`<article class="kux-section-msg" data-role="${esc(m.role)}"><strong>${m.role==='operator'?'Contributo':m.role==='pending'?'In elaborazione':m.role==='unavailable'?'Collegamento':'MAIOS AI'}</strong><p>${esc(m.text)}</p><small>${esc(m.context)}</small>${actionButtons(m.proposedActions)}</article>`).join('')||'<p>Si può chiedere come usare il kernel in questo punto del lavoro.</p>'}</div><label for="section-text-${esc(id)}">Domanda per questa scheda</label><textarea id="section-text-${esc(id)}" class="kux-section-editor" placeholder="Scrivi una domanda…">${esc(draft)}</textarea><p class="kux-ai-note" data-disclosure-id="maios-ai-processing-footer-v1">Con Invia, la domanda raggiunge MAIOS AI insieme al contesto pubblico della scheda. Le bozze nelle altre schede restano locali. Il servizio AI elabora i messaggi inviati; usa esempi senza dati riservati.</p><div class="kux-section-actions"><button type="button" data-section="ask">Invia domanda ↗</button><button type="button" data-section="candidate">Conserva proposta</button><button type="button" data-section="export">Esporta dialogo e proposte</button></div><div class="kux-section-proposal-status" role="status">Proposte conservate: ${proposals.filter(p=>p.owner===id).length}. Il trasferimento al kernel di lavoro è esplicito.</div></div>`;
    }
    return {getMessages:id=>[...get(id)],post,propose,renderHTML,
      exportPacket:id=>({schema:'kux.section.learning-candidates.v0.1',kind:'public-dialogue-export',owner:id,createdAt:new Date().toISOString(),messages:[...get(id)],candidates:proposals.filter(p=>p.owner===id),authority:'proposal_only',assimilated:false}),
      proposals:()=>proposals.map(p=>({...p})),summary:()=>({sessions:entries.size,proposals:proposals.length,assimilated:0})};
  }

  function source(c) {
    return `<details class="kux-public-source"><summary>Metodo e documentazione</summary><p>${esc(c.method)}</p><ul>${profile().documents.map(d=>`<li><a href="${esc(d.href)}" target="_blank" rel="noopener">${esc(d.label)}</a></li>`).join('')}</ul></details>`;
  }

  function renderActivity(p,c,state) {
    const id=p.id, pr=profile(); c={...pr.defaults,...c}; let body;
    const possibilities=c.possibilities || pr.possibilities;
    const link=(intent,label)=>`<button class="small-button" data-intent-link="${intent}">${esc(label)} ↗</button>`;
    switch(p.intent) {
      case 'capire': body=`<div class="mini-caps">${esc(c.kind)}</div><h3>${esc(c.subtitle)}</h3><p>${esc(c.goal)}</p><div class="model-path"><b>${esc(pr.actors[0])}</b><span>→</span><b>${esc(pr.actors[1])}</b><span>→</span><b>${esc(pr.actors[2])}</b></div>${row('Oggetto presente',c.object,'ok')}${row('Punto da comprendere',c.unknown,'warn')}${row('Continuazione',c.next)}<div class="form-actions">${link('esplorare','Esplora le relazioni')}${link('presentare','Vedi il funzionamento')}</div>`;break;
      case 'fare': body=`<div class="mini-caps">CONTRIBUTO AL LAVORO</div><h3>${esc(c.contributionTitle)}</h3><p>${esc(c.goal)}</p><label for="note-${id}">Che cosa cambia o merita di essere conservato?</label><textarea id="note-${id}" class="note-editor" placeholder="Annota un'esigenza, un riscontro o una proposta…"></textarea><div class="form-actions"><button class="primary" data-action="save-note">Conserva nella sessione ↗</button>${link('organizzare','Organizza il seguito')}</div><p class="kux-ai-note">Questa annotazione resta nella sessione del browser. Il dialogo della scheda permette di chiedere come farla continuare.</p><div class="mini-caps">CONTRIBUTI DEL CONTESTO</div>${state.notes.filter(n=>n.context===p.context).slice(0,3).map(n=>row(n.id,n.text)).join('')||'<p>Ancora nessun contributo.</p>'}`;break;
      case 'controllare': {const e=state.events.find(x=>x.context===p.context&&x.status==='pending');body=`<div class="mini-caps">RISCONTRI DEL CASO ILLUSTRATIVO</div><h3>${esc(c.checkTitle)}</h3><p>${esc(c.checkMeaning)}</p>${c.items.map((x,i)=>`<label class="selectable-row"><input type="checkbox" data-action="check-item" data-check-key="${esc(p.context)}:${i}" ${state.checks[p.context+':'+i]?'checked':''}><span>${esc(x)}</span></label>`).join('')}${row('Punto aperto',c.unknown,'warn')}${e?`<div class="event-explain"><strong>${esc(e.title)}</strong><p>${esc(e.description)}</p><button data-action="resolve-event" data-event-id="${esc(e.id)}">Conserva come esaminato</button></div>`:''}<div class="form-actions">${link('confrontare','Confronta due contributi')}</div>`;break;}
      case 'esplorare': body=`<div class="mini-caps">OGGETTI E RELAZIONI</div><h3>${esc(pr.exploreTitle)}</h3><div class="kux-source-diagram">${pr.actors.map(x=>`<span>${esc(x)}</span>`).join('')}</div><p>${esc(pr.exploreMeaning)}</p><div class="source-grid">${Object.entries(pr.contexts).map(([key,x])=>`<div class="source-tile"><span class="mini-caps">${esc(x.kind)}</span><strong>${esc(x.name)}</strong><small>${esc(x.subtitle)}</small><button data-action="change-context" data-target="${key}">Esplora ↗</button></div>`).join('')}</div>`;break;
      case 'progettare': body=`<div class="mini-caps">POSSIBILITÀ DA ESPLORARE</div><h3>${esc(c.designTitle)}</h3><p>${esc(c.goal)}</p>${possibilities.map((x,i)=>`<label class="selectable-row"><input type="radio" name="proposal-${id}" data-action="choose-option" data-value="${i?'B':'A'}" ${state.selections[p.context]===(i?'B':'A')?'checked':''}><span><strong>${esc(x.title)}</strong><p>${esc(x.detail)}</p></span></label>`).join('')}${row('Esplorazione corrente',state.selections[p.context]||'Da scegliere')}${link('controllare','Esamina le conseguenze')}`;break;
      case 'organizzare': body=`<div class="mini-caps">COMPOSIZIONE DEL SEGUITO</div><h3>${esc(c.organizeTitle)}</h3><p>${esc(c.next)}</p>${(p.localItemOrder||c.items.map((_,i)=>i)).map((item,i)=>`<div class="data-row"><strong>${i+1}. ${esc(c.items[item])}</strong><button data-action="promote-item" data-index="${i}" ${i===0?'disabled':''}>↑</button></div>`).join('')}<p class="kux-ai-note">Il riordino organizza questa vista locale del lavoro.</p>${link('comunicare','Prepara un contributo')}`;break;
      case 'comunicare':body=`<div class="mini-caps">CONTRIBUTO PER CHI CONTINUA</div><h3>${esc(c.communicateTitle)}</h3><p>${esc(c.communicationMeaning)}</p><label for="request-${id}">Che cosa deve sapere chi riprende questo punto?</label><textarea id="request-${id}" class="request-editor" placeholder="Situazione, oggetto, riscontro e domanda…"></textarea><div class="form-actions"><button data-action="save-request" class="primary">Conserva bozza ↗</button></div><p class="kux-ai-note">La bozza rimane locale. Le domande per MAIOS AI si inviano nel dialogo della scheda.</p>`;break;
      case 'presentare':body=`<div class="mini-caps">${esc(pr.name)} · PRESENTAZIONE E GUIDA</div><h3>${esc(pr.presentationTitle)}</h3><div class="kux-present-field" data-phase="${state.stageStep}">${pr.id==='k-ux-ai'?"<div class=\"kux-source-diagram\" role=\"group\" aria-label=\"Dal lavoro al mezzo, dal riscontro al metodo\"><span>Lavoro presente</span><span>Interfaccia</span><span>Riscontro</span></div>":"<div class=\"kux-present-object\" aria-label=\"Rappresentazione dell'oggetto di lavoro\"></div>"}</div><div class="kux-present-phases">${pr.phases.map((x,i)=>`<button data-action="presentation-step" data-step="${i}" ${i===state.stageStep?'aria-current="step"':''}>${esc(x.title)}</button>`).join('')}</div><div class="kux-present-explain">${esc(pr.phases[state.stageStep]?.text||pr.phases[0].text)}</div><p>${esc(pr.presentationMeaning)}</p><div class="form-actions"><button data-action="next-presentation" class="primary">Continua →</button>${link('capire',pr.presentationCaseLabel||'Apri il caso')}${pr.presentationHref?`<a href="${esc(pr.presentationHref)}" target="_blank" rel="noopener">Presentazione tridimensionale ↗</a>`:''}</div>`;break;
      case 'riprendere':body=`<div class="mini-caps">CONTINUITÀ DEL LAVORO LOCALE</div><h3>Ritrova il punto da cui continuare.</h3><p>${esc(c.reentryMeaning)}</p>${row('Contributi della sessione',String(state.notes.length),'ok')}${row('Eventi illustrativi esaminati',String(state.events.filter(x=>x.status==='examined').length))}${row('Viste del lavoro',String(state.panels.filter(x=>!x.minimized).length))}<ul class="events-list">${state.notes.slice(0,4).map(x=>`<li><b>${esc(x.text)}</b><small>${esc(pr.contexts[x.context]?.name||x.context)}</small></li>`).join('')||'<li>Il primo contributo può essere un’esigenza, una fonte o un riscontro.</li>'}</ul>${link('fare','Continua il contributo')}`;break;
      case 'sperimentare':body=`<div class="mini-caps">SCENARI ILLUSTRATIVI</div><h3>${esc(c.experimentTitle)}</h3><p>${esc(c.experimentMeaning)}</p>${possibilities.map((x,i)=>row('Possibilità '+(i?'B':'A'),x.title)).join('')}${row('Relazione da comprendere',c.unknown,'warn')}<label for="projection-${id}">Quanto dettaglio esplorare?</label><input id="projection-${id}" type="range" min="0" max="100" value="50"><button data-action="projection" class="primary">Esplora lo scenario</button><p class="projection-result" id="projection-result-${id}">La vista è una proiezione del caso.</p>`;break;
      case 'monitorare':{const e=state.events.find(x=>x.context===p.context&&x.status==='pending');body=`<div class="mini-caps">MONITORAGGIO · CASO ILLUSTRATIVO</div><h3>${esc(c.monitorTitle)}</h3><p>${esc(c.monitorMeaning)}</p>${row('Fonte',c.source)}${row('Situazione',e?e.title:'Nessuna nuova variazione',e?'warn':'ok')}${row('Punto aperto',c.unknown,'warn')}<p>${esc(c.monitorHorizon)}</p><div class="form-actions">${link('controllare','Esamina il riscontro')}${link('esplorare','Raggiungi le relazioni')}</div>`;break;}
      case 'confrontare':body=`<div class="mini-caps">CONFRONTO DI CONTRIBUTI</div><h3>${esc(c.compareTitle)}</h3><p>Il confronto locale rende visibili parole condivise e differenze. Il dialogo della scheda permette di discuterne il significato.</p><label for="srcA-${id}">Contributo A</label><textarea id="srcA-${id}" class="compare-a">${esc(c.compareTexts[0])}</textarea><label for="srcB-${id}">Contributo B</label><textarea id="srcB-${id}" class="compare-b">${esc(c.compareTexts[1])}</textarea><button class="primary" data-action="compare-text">Confronta termini ↗</button><div class="compare-output" role="status">Il confronto partirà dai testi presenti.</div>`;break;
      case 'chat':{const msgs=thread('chat-'+id);body=`<div class="mini-caps">DIALOGO CON ${esc(pr.name)}</div><h3>${esc(c.aiTitle)}</h3><p>${esc(c.aiMeaning)}</p><div class="chat-log" role="log">${msgs.map(m=>`<div class="message ${esc(m.role)}">${esc(m.text)}${actionButtons(m.proposedActions)}</div>`).join('')||'<p>La domanda porta il contesto pubblico di questa scheda.</p>'}</div><div class="quick-prompts"><button data-action="quick-chat" data-message="${esc(c.aiPrompt)}">${esc(c.aiPrompt)}</button></div><div class="chat-compose"><input class="chat-editor" aria-label="Domanda per MAIOS AI" placeholder="Scrivi una domanda…"><button data-action="send-chat">Invia ↗</button></div><p class="kux-ai-note" data-disclosure-id="maios-ai-processing-footer-v1">La domanda inviata raggiunge MAIOS AI. Le bozze nelle altre schede restano locali. Il servizio AI elabora i messaggi inviati; usa esempi senza dati riservati.</p>`;break;}
      default:return null;
    }
    return body+source(c);
  }

  async function sendChat(p,message) {
    const clean=String(message||'').trim();if(!clean)return;
    const owner='chat-'+p.id, messages=thread(owner);messages.push({role:'user',text:clean});
    const pending={role:'assistant',kind:'pending',text:'MAIOS AI sta leggendo la domanda e il contesto.'};messages.push(pending);
    const input=p.el.querySelector('.chat-editor');if(input)input.value='';core.renderModule(p);
    try{const answer=await ask(clean,p.context,p.intent,owner);pending.text=answer.message;pending.kind='maios-response';pending.proposedActions=answer.proposedActions;}catch(error){pending.text=error.message;pending.kind='unavailable';}
    if(core.state.panels.includes(p))core.renderModule(p);
  }
  async function askShared(action) {const owner='shared-'+action.context;const messages=thread(owner);messages.push({role:'user',text:action.text});const result=await ask(action.text,action.context,core.getFocused()?.intent||'capire',owner);messages.push({role:'assistant',text:result.message});return {...result,reply:result.message};}

  function focusedTarget() {
    const assistant=core?.getAssistant?.(),requested=profile().targets[target];
    if(core?.state.screen==='work'&&assistant?.open&&assistant.visible&&(requested?.intent==='chat'||(!requested&&assistant.focused))) {
      if(requested?.intent==='chat'&&requested.context===core.state.activeContext)return target;
      return Object.entries(profile().targets).find(([,x])=>x.context===core.state.activeContext&&x.intent==='chat')?.[0]||'';
    }
    const p=core?.getFocused();if(!p)return '';
    if(core.state.screen!=='work'||p.minimized||p.context!==core.state.activeContext||!p.el?.isConnected)return '';
    if(p.el.hidden||!p.el.getClientRects().length)return '';
    const style=getComputedStyle(p.el);if(style.display==='none'||style.visibility==='hidden')return '';
    if(requested?.context===p.context&&requested?.intent===p.intent)return target;
    return Object.entries(profile().targets).find(([,x])=>x.context===p.context&&x.intent===p.intent)?.[0]||'';
  }
  function report(requestId='',ok=true) {
    if(!session||parent===window)return;
    parent.postMessage({schema:profile().bridge+'-state.v2',session,requestId,ready:true,target:focusedTarget(),ok},location.origin);
  }
  function install(api) {
    core=api;
    document.addEventListener('click',event=>{
      if(event.target.closest?.('.module'))target='';
      const button=event.target.closest?.('[data-kux-ai-target]');if(!button)return;
      const key=button.dataset.kuxAiTarget;if(!Object.hasOwn(profile().targets,key))return;
      const route=profile().targets[key];target=key;
      core.switchWorkspaceContext(route.context);core.activateScreen('work');core.openPanel(route.intent,route.context,{forceFocus:true});
    });
    document.addEventListener('kux:public-dialogue',event=>{
      const p=core.state.panels.find(x=>x.id===event.detail.id);if(!p?.sectionOpen)return;
      const input=p.el.querySelector('.kux-section-editor'), focused=document.activeElement===input;
      const selection=focused?{start:input.selectionStart,end:input.selectionEnd,direction:input.selectionDirection,scroll:input.scrollTop}:null;
      if(input)p.sectionDraft=input.value;
      core.renderSection(p);
      if(focused){const next=p.el.querySelector('.kux-section-editor');next?.focus({preventScroll:true});next?.setSelectionRange(selection.start,selection.end,selection.direction);if(next)next.scrollTop=selection.scroll;}
    });
    addEventListener('message',event=>{
      if(event.source!==parent||event.origin!==location.origin)return;
      const data=event.data, bridge=profile().bridge;
      if(data?.schema===bridge+'-hello.v2'&&typeof data.session==='string'&&data.session.length<=100){session=data.session;report();return;}
      if(data?.schema!==bridge+'-command.v2'||data.session!==session||typeof data.requestId!=='string')return;
      const route=Object.hasOwn(profile().targets,data.target)?profile().targets[data.target]:null;
      if(!route){report(data.requestId,false);return;}
      target=data.target;core.switchWorkspaceContext(route.context);core.activateScreen('work');core.openPanel(route.intent,route.context,{forceFocus:true});
      requestAnimationFrame(()=>requestAnimationFrame(()=>report(data.requestId,focusedTarget()===data.target)));
    });
    if(parent!==window)parent.postMessage({schema:profile().bridge+'-available.v2'},location.origin);
    let pending=false;
    const scheduleReport=()=>{if(pending)return;pending=true;requestAnimationFrame(()=>{pending=false;report();});};
    document.addEventListener('focusin',scheduleReport);
    new MutationObserver(scheduleReport).observe(document.body,{childList:true,subtree:true,attributes:true,attributeFilter:['class','hidden','data-focused']});
    window.KUXPublicSurface=Object.freeze({snapshot:()=>({product:profile().id,source:profile().semanticOwner,context:core.state.activeContext,intent:core.getFocused()?.intent||'',target:focusedTarget(),completedAssistantRequests:completedRequests,companyIntegrations:false})});
  }

  function promoteItem(p,index) {
    const items=profile().contexts[p.context].items;
    if(!Number.isInteger(index)||index<1||index>=items.length)return;
    const order=p.localItemOrder||items.map((_,i)=>i);
    [order[index-1],order[index]]=[order[index],order[index-1]];p.localItemOrder=order;
    core.renderModule(p);
    p.el?.querySelector(`[data-action="promote-item"][data-index="${index-1}"]`)?.focus({preventScroll:true});
  }
  function chatMarkdown() {
    const p=core.getFocused(),owner=p?.sectionOpen&&p.sectionTab==='dialogo'?'section-'+p.id:p?.intent==='chat'?'chat-'+p.id:'shared-'+core.state.activeContext;
    return ['# Dialogo · '+profile().name,'','Contesto: '+(profile().contexts[p?.context||core.state.activeContext]?.name||''),'',...thread(owner).map(m=>`**${m.role==='user'?'Persona':'MAIOS AI'}**: ${m.text}`),''].join('\n');
  }
  window.KUXHostedGriglia=Object.freeze({createDiscussions,renderActivity,sendChat,askShared,install,promoteItem,chatMarkdown});
})();
