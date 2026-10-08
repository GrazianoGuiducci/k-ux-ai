import { createMedium } from '../../src/medium.js';
import { createWindowSurface } from '../../src/ui/window-surface.js';
import { createChatFormModule } from '../../src/ui/chat-form-module.js';

const status=document.getElementById('demo-status'),receipt=document.getElementById('demo-receipt');
const eventLog=document.getElementById('demo-events');
const work=document.getElementById('demo-work');
const sourceState={caseId:'kn:demo:stern-access',revision:0,original:'Accesso di poppa',status:'illustrative',events:[]};
let counter=0;
let medium;
const publish=(why)=>{
  const id=`kn:demo:event:${++counter}`;
  sourceState.events.push({id,why,revision:sourceState.revision});
  medium.receive({id,state:structuredClone(sourceState)});
  return id;
};
const module=createChatFormModule({
  id:'nautico-local-assistant',
  onAsk:async text=>{
    medium.dispatch({type:'demo.question',text});
    return {accepted:false,message:'Richiesta dimostrativa registrata: non esiste una risposta AI collegata.'};
  },
  onSubmit:async draft=>{
    const result=medium.dispatch({type:'demo.contribution',draft});
    return result;
  },
});
let surface;
const layout=({mode,open})=>{work.dataset.dock=open?mode:'floating';
  module.refreshLayout();};
surface=createWindowSurface({
  id:'nautico-local-assistant',title:'Assistente K-UX-AI',subtitle:'Chat e contributo · demo locale',
  avatar:'AI',content:module.element,initialWidth:850,initialHeight:590,onLayoutChange:layout,onPresenceChange:layout,
});
module.setActions([
  {label:'Cosa è disponibile?',prompt:'Quali funzioni sono effettivamente disponibili nella demo?'},
  {label:'Prepara un contributo',prompt:'Aiutami a descrivere un contributo al progetto.'},
]);
medium=createMedium({
  state:structuredClone(sourceState),
  render:state=>{
    status.textContent=`Caso ${state.caseId} · revisione ${state.revision}`;
    receipt.textContent=state.events.length?`Ultimo: ${state.events.at(-1).why}`:'Nessun evento nuovo';
    eventLog.textContent=`Eventi sorgente: ${state.events.map(e=>e.id).join(' · ')||'nessuno'}\nDisponibilità: ${state.status}; nessun effetto remoto.`;
  },
  onAction:action=>{
    if(action.type==='demo.question')return {accepted:true,message:'Domanda registrata solo localmente'};
    if(action.type==='demo.contribution'){
      if(!action.draft?.note?.trim())return {accepted:false,message:'Il contributo è vuoto'};
      sourceState.revision++;
      publish('Contributo dimostrativo, senza effetto sul prodotto');
      return {accepted:true,message:'Traccia registrata nella sessione dimostrativa, revisione '+sourceState.revision};
    }
    return {accepted:false,message:'Azione non disponibile'};
  },
});
for(const el of document.querySelectorAll('[data-demo-open]'))el.addEventListener('click',()=>surface.open(el));
for(const el of document.querySelectorAll('[data-demo-form]'))el.addEventListener('click',async()=>{module.setPane('form');await surface.open(el)});
document.getElementById('demo-open').addEventListener('click',()=>surface.open());
document.getElementById('demo-dock').addEventListener('click',async()=>{await surface.open();surface.setPlacement('dock-right')});
document.getElementById('demo-event').addEventListener('click',()=>{
  const id=publish('Evento sintetico che richiede un controllo');
  surface.notify({id,text:'Il caso dimostrativo ha una variazione da esaminare. Apri per consultare.'});
});
document.getElementById('demo-reset-ui').addEventListener('click',()=>surface.setPlacement('floating'));
// Inspection-only API. No real credentials or external effects.
window.KUX_UI_LAB=Object.freeze({surface,module,medium});
