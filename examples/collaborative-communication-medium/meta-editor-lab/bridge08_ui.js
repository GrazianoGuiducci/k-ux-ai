
(() => {
'use strict';
function init(){
const carrier='__CARRIER__';
// Exported work HTML can contain a serialized UI shell. Remove it BEFORE recreation;
// public copies must lose the shell even when the authoring runtime is present.
document.querySelectorAll('#me08-launcher,#me08-dialog,#me08-toast').forEach(node=>node.remove());
// A public Studio copy remains read-only and receives no authoring UI.
if(carrier==='studio'){
  try { const d=JSON.parse(document.querySelector('#ccm-data')?.textContent||'{}');if(d?.ui?.publicCopy)return; } catch {}
}
// Rebuilt exactly once per load; the prior serialized shell was removed above.
const $=(q)=>document.querySelector(q);
const api=()=>window.MetaEditorCommands;
const make=(tag,props={})=>Object.assign(document.createElement(tag),props);
const shell=make('div',{id:'me08-launcher'});
const openBtn=make('button',{className:'primary',textContent:'⌕ Azioni'});
openBtn.title='Trova comandi e naviga · Ctrl+Maiusc+P';
const context=make('span',{id:'me08-context',textContent:'Nessuna selezione'});
const editBtn=make('button',{textContent:'Modifica'});
editBtn.title='Modifica testo selezionato · F2';
const focusBtn=make('button',{textContent:'Focus'});
focusBtn.title='Mostra o nascondi la modalità di concentrazione';
shell.append(openBtn,context,editBtn,focusBtn);
const dlg=make('dialog',{id:'me08-dialog'});
dlg.setAttribute('aria-label','Cerca azioni di MetaEditor');
dlg.innerHTML=`<div id="me08-window"><div id="me08-searchrow"><span aria-hidden="true">⌕</span><input id="me08-search" aria-label="Cerca azioni o sezioni" type="search" placeholder="Cerca un'azione, una sezione, una scheda…" autocomplete="off"><button id="me08-close" type="button" aria-label="Chiudi ricerca">Esc</button></div><div id="me08-results" role="group" aria-label="Risultati"></div><div id="me08-foot">↑ ↓ per scegliere · Invio per eseguire · Esc per uscire · F2 per modificare</div></div>`;
const input=dlg.querySelector('#me08-search'),list=dlg.querySelector('#me08-results');
const toast=make('div',{id:'me08-toast',hidden:true});toast.setAttribute('role','status');
document.body.append(shell,dlg,toast);
let lastFocus=null,rows=[],active=0,toastTimer=null,focus=false;
const safeText=t=>(t||'').replace(/\s+/g,' ').trim().slice(0,72);
const hasSelected=()=>!!api()?.status()?.target;
const nativeClick=id=>{const el=typeof id==='string'?$(id):id;if(!el||el.disabled)return false;el.click();return true;};
function notify(msg){toast.textContent=msg;toast.hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>{toast.hidden=true},1900)}
function nativePanel(id){const el=$(id);if(!el)return false; nativeClick(el);return true}
function pageSections(){return [...document.querySelectorAll('#main-content > section')];}
function pageSectionLabel(section,i){return safeText(section.querySelector('h1,h2,h3,h4')?.textContent)||`Sezione ${i+1}`;}
function gotoSection(section,i){if(!section)return false;section.scrollIntoView({behavior:'smooth',block:'start'});const picker=$('#local-section');if(picker){picker.value=String(i);picker.dispatchEvent(new Event('change',{bubbles:true}));}return true;}
function nativePagePanel(tab){const panel=$('#local-tools');if(!panel)return false;if(panel.hidden)nativeClick('#local-tools-open');if(tab)nativeClick('#local-tab-'+tab);return true;}
function studioScenes(){return [...document.querySelectorAll('#slideList .slide-chip')].map((el,i)=>({el,i,label:safeText(el.querySelector('.label')?.textContent)||'Scheda '+(i+1)}));}
function studioSceneClick(el){return nativeClick(el?.querySelector('button.sel'))}
function cmd(label,group,run,description='',enabled=true,keywords=''){return {label,group,run,description,enabled,keywords};}
function actions(){
 const editing=!!api()?.status()?.editing,selected=hasSelected();
 const general=[
 cmd('Modifica testo','Testo',()=>api()?.begin().ok,'F2',selected&&!editing,'edit titolo nodo'),
 cmd('Conferma modifica','Testo',()=>api()?.commit().ok,'Ctrl+Invio',editing),
 cmd('Annulla modifica in corso','Testo',()=>api()?.cancel().ok,'Esc',editing),
 cmd('Annulla ultima azione','Cronologia',()=>nativeClick(carrier==='studio'?'#undoBtn':'[data-local-action="undo"]'),'Ctrl+Z',true,'undo'),
 cmd('Ripristina azione','Cronologia',()=>nativeClick(carrier==='studio'?'#redoBtn':'[data-local-action="redo"]'),'Ctrl+Y',true,'redo'),
 cmd(focus?'Esci da Focus':'Modalità Focus','Vista',()=>toggleFocus(),'Più spazio al contenuto',true,'distraibilità')
 ];
 if(carrier==='codex'){
  general.push(
  cmd('Struttura e sezioni','Strumenti',()=>nativePagePanel('section'),'Organizza la pagina',true,'outline naviga'),
  cmd('Inserisci elemento','Composizione',()=>nativePagePanel('element'),'Paragrafo, titolo, elenco, riquadro',true,'blocchi aggiungi'),
  cmd('Dimensioni e disposizione','Strumenti',()=>nativePagePanel('size'),'Misure dell’elemento',true,'layout'),
  cmd('Colori della pagina','Strumenti',()=>nativePagePanel('color'),'Palette MAIOS',true),
  cmd('Anteprima desktop/mobile','Verifica',()=>nativeClick('#local-preview-open'),'Usa l’anteprima nativa',true),
  cmd('Esporta HTML','Documento',()=>nativeClick('#local-panel-save'),'Scarica la bozza editabile',true));
  pageSections().forEach((sec,i)=>general.push(cmd(`Vai a · ${pageSectionLabel(sec,i)}`,'Sezioni',()=>gotoSection(sec,i),`Sezione ${i+1}`,true,'vai naviga')));
 }else{
  general.push(
   cmd('Aggiungi testo','Elementi',()=>nativeClick('[data-add="text"]'),'Nuovo elemento testuale',true,'testo'),
   cmd('Aggiungi riquadro','Elementi',()=>nativeClick('[data-add="card"]'),'Inserisce un riquadro',true,'card'),
   cmd('Aggiungi collegamento','Elementi',()=>nativeClick('#addLink'),'Freccia fra due oggetti',true,'freccia'),
   cmd('Strumenti avanzati','Strumenti',()=>nativeClick('#toggleTools'),'Libreria, template, livelli',true,'proprietà'),
   cmd('Schede e miniature','Struttura',()=>nativeClick('#toggleSlideRail'),'Mostra/nasconde schede',true),
   cmd('Presenta','Vista',()=>nativeClick('#presentBtn'),'Modalità presentazione',true),
   cmd('Leggi','Vista',()=>nativeClick('#viewBtn'),'Vista di lettura',true),
   cmd('Layout Flat','Vista',()=>nativeClick('#flatLayoutBtn'),'Aumenta superficie del canvas',true),
   cmd('Apri guida','Aiuto',()=>nativeClick('#ccmGuideBtn'),'Guida MetaCanvas',true),
   cmd('Salva lavoro','Documento',()=>nativeClick('#saveBtn'),'Esporta documento editabile',true),
   cmd('Nuova scheda','Documento',()=>nativeClick('#addSlide'),'Aggiunge una scheda',true));
  studioScenes().forEach(({el,i,label})=>general.push(cmd(`Vai alla scheda ${i+1} · ${label}`,'Schede',()=>studioSceneClick(el),'Navigazione presentazione',true,'naviga slide')));
 }
 return general;
}
function toggleFocus(){focus=!focus;document.body.classList.toggle('me08-focus',focus);focusBtn.setAttribute('aria-pressed',String(focus));focusBtn.textContent=focus?'Esci Focus':'Focus';return true;}
function refreshContext(){const state=api()?.status();if(!state||!state.target){context.textContent='Seleziona un elemento';editBtn.disabled=true;editBtn.hidden=true;return;}
 const tgt=state.target, text=tgt.type==='scene-node'?`Nodo · ${tgt.id}`:`Testo · ${tgt.tag||''}`;
 context.textContent=state.editing?'Modifica in corso':text;
 editBtn.hidden=!!state.editing;editBtn.disabled=!!state.editing;
}
function searchable(){const needle=input.value.toLocaleLowerCase('it').trim();rows=actions().filter(a=>(a.label+' '+a.group+' '+a.description+' '+a.keywords).toLocaleLowerCase('it').includes(needle));active=0;draw();}
function draw(){list.replaceChildren();if(!rows.length){const no=make('div',{className:'me08-empty',textContent:'Nessuna azione trovata'});list.append(no);return}
 rows.slice(0,35).forEach((a,i)=>{
 const b=make('button',{className:'me08-row',type:'button'});b.disabled=!a.enabled;b.dataset.index=String(i);b.setAttribute('aria-selected',String(i===active));
 const name=make('span',{textContent:a.label});const hint=make('small',{textContent:a.group+(a.description?' · '+a.description:'')});b.append(name,hint);
 b.addEventListener('mouseenter',()=>{active=i;highlight()});b.addEventListener('click',()=>invoke(i));list.append(b);
 });
}
function highlight(){list.querySelectorAll('.me08-row').forEach((b,i)=>b.setAttribute('aria-selected',String(i===active)));const row=list.querySelectorAll('.me08-row')[active];row?.scrollIntoView({block:'nearest'});}
function invoke(i){const choice=rows[i];if(!choice?.enabled)return;close();try{const ok=choice.run();if(ok===false)notify('Azione non disponibile nel contesto attuale')}catch(error){notify('Operazione non eseguita: '+error.message)}setTimeout(refreshContext,70);}
function open(){if(dlg.open)return;lastFocus=document.activeElement;input.value='';dlg.showModal();searchable();input.focus();}
function close(){if(!dlg.open)return;dlg.close();if(lastFocus?.isConnected && lastFocus!==document.body)lastFocus.focus({preventScroll:true});else openBtn.focus();}
openBtn.addEventListener('click',open);
editBtn.addEventListener('click',()=>{const result=api()?.begin();if(!result?.ok)notify('Seleziona prima il testo da modificare');refreshContext()});
focusBtn.addEventListener('click',()=>toggleFocus());
$('#me08-close').addEventListener('click',close);
dlg.addEventListener('click',e=>{if(e.target===dlg)close()});
input.addEventListener('input',searchable);
input.addEventListener('keydown',e=>{
 if(e.key==='ArrowDown'){e.preventDefault();active=Math.min(rows.length-1,active+1);highlight()}
 if(e.key==='ArrowUp'){e.preventDefault();active=Math.max(0,active-1);highlight()}
 if(e.key==='Enter'){e.preventDefault();invoke(active)}
 if(e.key==='Escape'){e.preventDefault();close()}
});
document.addEventListener('keydown',e=>{
 if(dlg.open){if(e.key==='Escape'){e.preventDefault();close()}return}
 if((e.ctrlKey&&e.shiftKey&&e.key.toLowerCase()==='p') || (e.key==='/'&&!e.ctrlKey&&!e.altKey&&!e.metaKey&&!e.target.closest?.('input,textarea,select,[contenteditable="true"]'))){e.preventDefault();open();}
},true);
// An opt-in compact toolbar: no source buttons are deleted.
if(carrier==='codex'){const openNative=$('#local-tools-open');if(openNative)openNative.textContent='Struttura';}
if(carrier==='studio')document.body.classList.add('me08-studio-compact');
if(carrier==='codex'){
 const mini=$('#local-mini');
 if(mini){
  mini.classList.add('me08-short');
  const more=make('button',{className:'me08-more',type:'button',textContent:'Formato ▾'});
  more.setAttribute('aria-expanded','false');more.setAttribute('aria-label','Mostra altre opzioni di formattazione');
  more.addEventListener('pointerdown',e=>e.preventDefault());
  more.addEventListener('click',()=>{
    const expanded=mini.classList.toggle('me08-short')===false;
    more.textContent=expanded?'Riduci ▴':'Formato ▾';more.setAttribute('aria-expanded',String(expanded));
  });
  mini.insertBefore(more,mini.querySelector('[data-mini="undo"]'));
 }
}
// Only lightweight presentation state. No document data and no storage are modified.
document.addEventListener('pointerup',()=>requestAnimationFrame(refreshContext),true);
document.addEventListener('focusin',()=>requestAnimationFrame(refreshContext),true);
document.addEventListener('keyup',e=>{if(e.key==='F2'||e.key==='Escape'||e.key==='Enter')requestAnimationFrame(refreshContext)},true);
refreshContext();
window.MetaEditorUX08=Object.freeze({open,close,actions:()=>actions().map(a=>({label:a.label,group:a.group,enabled:a.enabled})),focus:toggleFocus});
}
// Wait until serialized runtime-only controls, if any, are fully parsed.
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
