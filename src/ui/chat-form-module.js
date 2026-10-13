/* K-UX-AI Chat/Form module: bounded human interaction, no built-in provider.
 * The host supplies the action receiver. Internal responsive is frame-relative.
 */
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const div=(cls,tag='div')=>{const n=document.createElement(tag);n.className=cls;return n};
export function createChatFormModule({
  id, onAsk=()=>({accepted:false}), onSubmit=()=>({accepted:false}),
  storage=null, compactWidth=685,
  initialMessage='Modulo dimostrativo. Nessun assistente AI è collegato.',
}={}) {
  if(!/^[a-z][a-z0-9-]{2,63}$/.test(id))throw new TypeError('Stable module identity required');
  let persistentStore=storage;
  if(persistentStore===undefined){try{persistentStore=window.localStorage}catch{persistentStore=null}}
  const prefix=`kux:module:${id}:v1`;
  const root=div('kux-chat-form');root.dataset.compact='false';root.dataset.pane='chat';
  const tabbar=div('kux-chat-tabs');tabbar.setAttribute('role','tablist');tabbar.setAttribute('aria-label','Aree del modulo');
  const tabChat=div('','button');tabChat.type='button';tabChat.textContent='Chat';tabChat.setAttribute('role','tab');tabChat.dataset.pane='chat';
  const tabForm=div('','button');tabForm.type='button';tabForm.textContent='Modulo';tabForm.setAttribute('role','tab');tabForm.dataset.pane='form';
  tabbar.append(tabChat,tabForm);
  const regions=div('kux-chat-regions');
  const chat=div('kux-chat-pane','section');chat.setAttribute('aria-label','Conversazione');
  const messages=div('kux-chat-messages');messages.setAttribute('role','log');messages.setAttribute('aria-live','polite');
  const quick=div('kux-chat-quick');
  const inputRow=div('kux-chat-inputrow');
  const ask=div('','textarea');ask.placeholder='Scrivi una domanda…';ask.rows=2;ask.setAttribute('aria-label','Messaggio chat');
  const askButton=div('','button');askButton.type='button';askButton.textContent='Invia';
  inputRow.append(ask,askButton);chat.append(messages,quick,inputRow);
  const handle=div('kux-chat-splitter');handle.tabIndex=0;
  handle.setAttribute('role','separator');handle.setAttribute('aria-label','Regola spazio chat e modulo');
  handle.setAttribute('aria-orientation','vertical');handle.setAttribute('aria-valuemin','28');handle.setAttribute('aria-valuemax','65');
  const formPane=div('kux-form-pane','section');formPane.setAttribute('aria-label','Modulo contestuale');
  const form=div('kux-form','form');form.noValidate=true;
  const formHead=div('kux-form-heading');
  const formTitle=div('','strong');formTitle.textContent='Modulo di contributo';
  const formSubtitle=div('','small');formSubtitle.textContent='Prepara una traccia o una domanda per il controller ospitante.';
  formHead.append(formTitle,formSubtitle);
  const kindRow=div('kux-form-kinds');
  const kindContribution=div('','button');kindContribution.type='button';kindContribution.textContent='Contributo';
  const kindQuestion=div('','button');kindQuestion.type='button';kindQuestion.textContent='Domanda';
  kindContribution.dataset.kind='contribution';kindQuestion.dataset.kind='question';kindRow.append(kindContribution,kindQuestion);
  const makeField=(caption,tag='input')=>{
    const label=document.createElement('label');label.className='kux-field';
    const text=div('','span');text.textContent=caption;
    const field=div('',tag);if(tag==='input')field.type='text';
    field.setAttribute('aria-label',caption);label.append(text,field);return {label,field};
  };
  const {label:topicLabel,field:topic}=makeField('Oggetto');
  const {label:noteLabel,field:note}=makeField('Traccia, richiesta o osservazione','textarea');note.rows=7;
  const {label:sourceLabel,field:source}=makeField('Fonte o riferimento (facoltativo)');
  const tools=div('kux-form-tools');
  const preview=div('','button');preview.type='button';preview.textContent='Anteprima';
  const reset=div('','button');reset.type='button';reset.textContent='Pulisci';
  const submit=div('','button');submit.type='submit';submit.textContent='Consegna al controller';
  tools.append(preview,reset,submit);
  const previewOutput=div('kux-form-preview');previewOutput.hidden=true;previewOutput.setAttribute('aria-label','Anteprima del contributo');
  const status=div('kux-form-status');status.setAttribute('role','status');
  const footer=div('kux-form-boundary');footer.textContent='Il modulo non invia automaticamente dati o email. L’host determina l’effetto.';
  form.append(formHead,kindRow,topicLabel,noteLabel,sourceLabel,previewOutput,tools,status,footer);
  formPane.append(form);regions.append(chat,handle,formPane);root.append(tabbar,regions);
  let kind='contribution', pane='chat', compact=false, split=43, dragging=null, resize=null, busy=false;
  const MAX_TEXT=10000;
  let draft={};try{draft=JSON.parse(persistentStore?.getItem(prefix+':draft')||'{}')}catch{}
  topic.value=typeof draft.topic==='string'?draft.topic.slice(0,240):'';
  note.value=typeof draft.note==='string'?draft.note.slice(0,MAX_TEXT):'';
  source.value=typeof draft.source==='string'?draft.source.slice(0,400):'';
  kind=draft.kind==='question'?'question':'contribution';
  try{split=clamp(Number(persistentStore?.getItem(prefix+':split'))||43,28,65)}catch{}
  const setStatus=(message,error=false)=>{status.textContent=message;status.dataset.error=String(error)};
  const persist=()=>{try{persistentStore?.setItem(prefix+':draft',JSON.stringify(getDraft()))}catch{}};
  const getDraft=()=>({kind,topic:topic.value,note:note.value,source:source.value});
  const updateKinds=()=>{
    kindContribution.setAttribute('aria-pressed',String(kind==='contribution'));
    kindQuestion.setAttribute('aria-pressed',String(kind==='question'));
    formTitle.textContent=kind==='question'?'Modulo di domanda':'Modulo di contributo';
  };
  const setKind=value=>{if(!['contribution','question'].includes(value))return;kind=value;updateKinds();persist()};
  kindContribution.addEventListener('click',()=>setKind('contribution'));
  kindQuestion.addEventListener('click',()=>setKind('question'));
  for(const control of [topic,note,source])control.addEventListener('input',()=>{persist();if(!previewOutput.hidden)displayPreview()});
  const displayPreview=()=>{const d=getDraft();previewOutput.textContent=`${d.kind==='question'?'DOMANDA':'CONTRIBUTO'}\n${d.topic||'(senza oggetto)'}\n\n${d.note||'(nessuna traccia)'}\n\n${d.source?'Fonte: '+d.source:''}`;};
  preview.addEventListener('click',()=>{previewOutput.hidden=!previewOutput.hidden;if(!previewOutput.hidden)displayPreview()});
  let pendingResetUntil=0;
  reset.addEventListener('click',()=>{
    if(Date.now()>pendingResetUntil){pendingResetUntil=Date.now()+2600;setStatus('Premi ancora Pulisci per eliminare la bozza.');return;}
    pendingResetUntil=0;topic.value='';note.value='';source.value='';previewOutput.hidden=true;persist();setStatus('Bozza locale pulita.');
  });
  form.addEventListener('submit',async ev=>{
    ev.preventDefault();if(busy)return;
    const d=getDraft();if(!d.note.trim()){setStatus('Scrivi prima una traccia.',true);note.focus();return;}
    busy=true;submit.disabled=true;setStatus('Consegna al controller…');
    try{
      const outcome=await onSubmit({...d});
      if(outcome?.accepted===true){setStatus(outcome.message||'Controller ha accettato la richiesta.');}
      else setStatus(outcome?.message||'Nessun effetto confermato dal controller. La bozza resta disponibile.',true);
    }catch(e){setStatus('Richiesta non eseguita. La bozza resta disponibile.',true)}
    finally{busy=false;submit.disabled=false}
  });
  const appendMessage=(role,text)=>{
    const entry=div('kux-chat-msg');entry.dataset.role=role;
    const prefix=div('','strong');prefix.textContent=role==='operator'?'Operatore':role==='system'?'Sistema':'Assistente';
    const body=div('','p');body.textContent=String(text).slice(0,MAX_TEXT);
    entry.append(prefix,body);messages.append(entry);messages.scrollTop=messages.scrollHeight;
  };
  if(initialMessage)appendMessage('system',initialMessage);
  async function send(){
    const msg=ask.value.trim();if(!msg||busy)return;
    busy=true;askButton.disabled=true;appendMessage('operator',msg);ask.value='';
    try{
      const result=await onAsk(msg);
      if(result?.reply)appendMessage('assistant',result.reply);
      else if(result?.accepted!==true)appendMessage('system',result?.message||'Nessun assistente connesso: richiesta registrata solo dal ricevente locale.');
    }catch(e){appendMessage('system','Richiesta non eseguita. Nessuna risposta AI verificata.');}
    finally{busy=false;askButton.disabled=false}
  }
  askButton.addEventListener('click',send);ask.addEventListener('keydown',ev=>{if(ev.key==='Enter'&&!ev.shiftKey){ev.preventDefault();send();}});
  const setPane=(next)=>{if(!['chat','form'].includes(next))return;pane=next;root.dataset.pane=pane;
    for(const b of [tabChat,tabForm]){const sel=b.dataset.pane===pane;b.setAttribute('aria-selected',String(sel));b.tabIndex=sel?0:-1;}
  };
  tabChat.addEventListener('click',()=>setPane('chat'));tabForm.addEventListener('click',()=>setPane('form'));
  const refreshSize=()=>{
    // offsetWidth is layout width; transformed bounds shrink during avatar entry motion.
    const width=root.offsetWidth;
    compact=width<compactWidth;root.dataset.lastMeasuredWidth=String(width);root.dataset.compact=String(compact);root.style.setProperty('--kux-chat-split',`${split}%`);
    handle.setAttribute('aria-valuenow',String(Math.round(split)));
  };
  const setSplit=value=>{split=clamp(value,28,65);root.style.setProperty('--kux-chat-split',`${split}%`);
    handle.setAttribute('aria-valuenow',String(Math.round(split)));try{persistentStore?.setItem(prefix+':split',String(split))}catch{}};
  handle.addEventListener('pointerdown',ev=>{
    if(compact||ev.button!==0)return;
    dragging={id:ev.pointerId};handle.setPointerCapture(ev.pointerId);ev.preventDefault();
  });
  handle.addEventListener('pointermove',ev=>{
    if(!dragging||dragging.id!==ev.pointerId)return;
    const rect=regions.getBoundingClientRect();setSplit(100*(ev.clientX-rect.left)/Math.max(1,rect.width));
  });
  for(const type of ['pointerup','pointercancel'])handle.addEventListener(type,ev=>{
    if(dragging?.id!==ev.pointerId)return;dragging=null;
    if(handle.hasPointerCapture(ev.pointerId))handle.releasePointerCapture(ev.pointerId);
  });
  handle.addEventListener('keydown',ev=>{if(['ArrowLeft','ArrowRight'].includes(ev.key)){
    ev.preventDefault();setSplit(split+(ev.key==='ArrowLeft'?-5:5));}});
  const observer=typeof ResizeObserver==='function'?new ResizeObserver(refreshSize):null;
  observer?.observe(root);updateKinds();setPane('chat');refreshSize();
  return {
    element:root,
    getDraft, setPane, setKind, setSplit,appendMessage, refreshLayout:refreshSize,
    setActions(actions){quick.replaceChildren();for(const action of Array.isArray(actions)?actions.slice(0,5):[]){
      if(!action||typeof action.label!=='string'||typeof action.prompt!=='string')continue;
      const b=div('','button');b.type='button';b.textContent=action.label;
      b.addEventListener('click',()=>{ask.value=action.prompt;setPane('chat');ask.focus()});quick.append(b);
    }},
    snapshot:()=>({kind,pane,compact,split,draft:getDraft(),messageCount:messages.children.length}),
    destroy(){observer?.disconnect();root.remove();},
  };
}
