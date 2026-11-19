#!/usr/bin/env python3
"""MetaEditor Bridge 07: source-bound native command adapters for Bridge06 carriers.
The original documents are never overwritten. Python 3.11 standard library only.
"""
from pathlib import Path
from hashlib import sha256
import argparse

CORE = r'''
/* Bridge07 common command contract (embedded, offline-safe). */
function createBridge07(native,kind,semantics) {
  const actions = ['begin','setText','commit','cancel','undo','redo'];
  for (const name of actions) if (typeof native[name] !== 'function') throw Error('Bridge07 missing '+name);
  const respond = (name,...args) => {
    try { const result = native[name](...args); return result && typeof result==='object' && 'ok' in result ? result : {ok:!!result,command:name}; }
    catch (error) { return {ok:false,command:name,error:String(error?.message||error)}; }
  };
  const api = Object.freeze({version:'0.7.0',carrier:kind,textSemantics:semantics,
    begin(target){return respond('begin',target)},
    setText(value){if(typeof value!=='string') return {ok:false,error:'Il testo deve essere una stringa.'};return respond('setText',value)},
    commit(){return respond('commit')}, cancel(){return respond('cancel')},
    undo(){return respond('undo')}, redo(){return respond('redo')},
    status(){return Object.freeze({carrier:kind,editing:!!native.isEditing(),target:native.target()})}
  });
  window.MetaEditorCommands = api;
  const isInput = node => !!node?.closest?.('input,textarea,select,[contenteditable="true"], [role="textbox"]');
  document.addEventListener('keydown', e => {
    if (e.defaultPrevented || e.altKey || e.isComposing) return;
    const edit = native.isEditing();
    let cmd = null;
    if (edit && e.key==='Escape') cmd='cancel';
    else if (edit && e.key==='Enter' && (e.ctrlKey || e.metaKey)) cmd='commit';
    else if (!edit && e.key==='F2' && !isInput(e.target)) cmd='begin';
    else if (!edit && (e.ctrlKey||e.metaKey) && (!isInput(e.target) || native.allowHistoryShortcut?.(e.target))) {
      const key=e.key.toLowerCase();
      if(key==='z')cmd=e.shiftKey?'redo':'undo';
      else if(key==='y')cmd='redo';
    }
    if (!cmd) return;
    // Non intercettare scorciatoie globali se nessun oggetto del documento è attivo.
    if (cmd!=='cancel' && cmd!=='commit' && !native.target()) return;
    const outcome=api[cmd]();
    if(outcome.ok){e.preventDefault();e.stopImmediatePropagation();}
  },true);
  return api;
}
'''

CODEX_ADAPTER = r'''
/* Bridge07 / native page adapter: rich HTML, selection ranges and original history. */
let b07RecentField=null, b07RecentIndex=-1, b07Session=null, b07HistoryNavigation=false;
main.addEventListener('beforeinput',()=>{b07HistoryNavigation=false;},true);
function b07MarkField(field){b07RecentField=field;b07RecentIndex=Array.from(main.querySelectorAll(selector)).indexOf(field);}
function b07FieldFrom(target){
  const raw=typeof target==='string' ? main.querySelector(target) : target;
  const candidate=raw instanceof Element ? raw : null;
  return candidate?.closest(selector) || candidate?.querySelector(selector) || null;
}
function b07Target(){
  if(b07RecentField && !b07RecentField.isConnected && b07RecentIndex>=0)
    b07RecentField=main.querySelectorAll(selector)[b07RecentIndex]||null;
  return [b07Session?.field,directField,miniField,b07RecentField]
    .find(n=>n?.isConnected && main.contains(n)) || null;
}
function b07Record(field){
  if(!field || !field.isConnected || b07Session?.field===field) return;
  b07Session={field,html:field.innerHTML,history:history.slice(),future:future.slice()};
}
main.addEventListener('pointerdown',event=>{
  const field=event.target.closest(selector); if(field) b07MarkField(field);
},true);
main.addEventListener('dblclick',event=>{
  const field=event.target.closest(selector);
  if(field){b07MarkField(field);b07Record(field);}
},true);
// Native blur commits the text session; do not leave a stale cancel target.
main.addEventListener('focusout',event=>{
  if(b07Session?.field===event.target && !event.target.isContentEditable) b07Session=null;
});
const b07Adapter={
  allowHistoryShortcut(target){return b07HistoryNavigation && main.contains(target)},
  target(){const f=b07Target();return f?{type:'page-text',tag:f.localName,section:sections().indexOf(f.closest('main > section'))}:null},
  isEditing(){return !!(b07Session?.field?.isConnected && b07Session.field.isContentEditable)},
  begin(target){
    const field=b07FieldFrom(target)||b07Target();if(!field)return false;
    b07HistoryNavigation=false;
    b07MarkField(field);b07Record(field);
    const hadRange=rangeIn(field);
    if(!field.isContentEditable){field.dispatchEvent(new MouseEvent('dblclick',{bubbles:true,cancelable:true}));}
    else {field.focus({preventScroll:true});openMini(field);}
    if(field.isContentEditable && !hadRange){
      const r=document.createRange();r.selectNodeContents(field);r.collapse(false);selectRange(r);openMini(field);
    }
    return field.isContentEditable;
  },
  setText(value){
    const field=b07Session?.field;if(!field?.isConnected||!field.isContentEditable)return false;
    const range=rangeIn(field);if(!range)return false;
    // Edit only the selected range; never replace formatted HTML outside it.
    remember();textCheckpoint=null;miniCommand=true;
    try{
      const selection=window.getSelection();selectRange(range);
      const inserted=document.execCommand('insertText',false,value);
      if(!inserted){
        range.deleteContents();const t=document.createTextNode(value);range.insertNode(t);
        range.setStartAfter(t);range.collapse(true);selectRange(range);
      }
    }finally{miniCommand=false;}
    openMini(field);showDirty();return true;
  },
  commit(){
    const field=b07Session?.field;
    if(!field?.isConnected)return false;
    b07Session=null;
    if(directField===field)stopDirectEdit();
    if(miniField===field)hideMini();
    field.blur();showDirty();return true;
  },
  cancel(){
    const tx=b07Session;if(!tx?.field?.isConnected)return false;
    const field=tx.field;b07Session=null;
    // Cancellation is not a new undo step; rollback the exact HTML & native history.
    field.innerHTML=tx.html;
    history.splice(0,history.length,...tx.history);
    future.splice(0,future.length,...tx.future);
    if(directField===field)stopDirectEdit();
    if(miniField===field)hideMini();
    field.blur();syncHistory();showDirty();return true;
  },
  undo(){if(b07Session?.field?.isContentEditable||!history.length)return false;b07Session=null;b07HistoryNavigation=true;restore(history,future);return true},
  redo(){if(b07Session?.field?.isContentEditable||!future.length)return false;b07Session=null;b07HistoryNavigation=true;restore(future,history);return true}
};
createBridge07(b07Adapter,'maios-page','HTML rich text: setText inserts/replaces selection, preserving other spans');
const b07MiniDone=mini.querySelector('[data-mini=close]');
if(b07MiniDone){b07MiniDone.title='Conferma ed esci · Ctrl+Invio (Esc annulla)';b07MiniDone.setAttribute('aria-keyshortcuts','Control+Enter');}
launcher.title=(launcher.title||'Modifica')+' · F2 sul testo selezionato';
'''

STUDIO_ADAPTER = r'''
/* Bridge07 / native scene adapter: one node string in ccm.document.v1. */
let b07RecentNode=null;
$('#canvas').addEventListener('pointerdown',e=>{
  const node=e.target.closest('.node[data-id]');if(node)b07RecentNode=node.dataset.id;
},true);
const b07Adapter={
  target(){const id=editingId||selectedId||b07RecentNode;return id?{type:'scene-node',id,sceneId:current().id}:null},
  isEditing(){return !!editingId},
  begin(target){
    if(presenting||publicMode)return false;
    const id=typeof target==='string'?target:(target?.id||editingId||selectedId||b07RecentNode);
    const node=current().elements.find(n=>n.id===id && n.type!=='image');
    if(!node)return false;
    startDirectEdit(id);return editingId===id;
  },
  setText(value){
    if(!editingId)return false;
    const d=$('#canvas .node[data-id="'+CSS.escape(editingId)+'"] .node-text');if(!d)return false;
    d.textContent=value;d.focus({preventScroll:true});
    const range=document.createRange();range.selectNodeContents(d);range.collapse(false);
    const sel=window.getSelection();sel.removeAllRanges();sel.addRange(range);
    return true;
  },
  commit(){if(!editingId)return false;cancelDirectEdit(true);return true},
  cancel(){if(!editingId)return false;cancelDirectEdit(false);return true},
  undo(){if(editingId||!past.length)return false;undo();return true},
  redo(){if(editingId||!future.length)return false;redo();return true}
};
createBridge07(b07Adapter,'metacanvas-scene','Plain label string in ccm.document.v1; setText replaces selected node label');
const b07StudioOk=$('#editOk');
if(b07StudioOk){b07StudioOk.title='Conferma modifica · Ctrl+Invio (Esc annulla)';b07StudioOk.setAttribute('aria-keyshortcuts','Control+Enter');}
$('#canvas')?.setAttribute('aria-keyshortcuts','F2 Control+Enter Escape');
'''


def insert(source: str, payload: str, anchor: str, marker: str) -> str:
    if source.count(anchor)!=1: raise SystemExit(f'Uncertain source anchor {marker}: {source.count(anchor)} occurrences')
    return source.replace(anchor, CORE+'\n'+payload+'\n'+anchor)

def verify(path: Path, expected: str) -> str:
    raw=path.read_bytes()
    checksum=sha256(raw).hexdigest()
    if checksum!=expected:
        raise SystemExit(f'Source drift: {path.name} sha256={checksum}; expected {expected}')
    return raw.decode('utf-8')

def build(codex: Path,studio: Path,out: Path):
    c=verify(codex, '7f8f72f4ce98b5890f468058919dc01523395928b262a79c78166895684ad759')
    s=verify(studio, '6f39f3bbf2bc27bd6c16cda0cca375cf7bbb4e21960a84513966a04e45797a77')
    c=insert(c,CODEX_ADAPTER, "})();\n</script>\n\n\n</body></html>", 'codex')
    s=insert(s,STUDIO_ADAPTER, "initStudio12Controls();initResponsiveToolTemplate();render();initStudio20();", 'studio')
    out.mkdir(parents=True,exist_ok=True)
    for filename,body in [('MetaEditor_Bridge07_Bozza_Codex_IT.html',c),('MetaEditor_Bridge07_Studio21_IT.html',s)]:
        dest=out/filename
        dest.write_text(body,encoding='utf-8')
        print(str(dest),len(body))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codex',type=Path,required=True)
    parser.add_argument('--studio',type=Path,required=True)
    parser.add_argument('--out-dir',type=Path,required=True)
    arg=parser.parse_args()
    build(arg.codex,arg.studio,arg.out_dir)
