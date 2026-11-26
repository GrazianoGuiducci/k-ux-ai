#!/usr/bin/env python3
"""Build source-pinned Studio21 visual direct-action candidates (IT/EN).

Reuses Studio21's native selectedId/quick editor/direct text edit/inspector,
duplicate and history. It does not create another editing engine or alter
the published source. Input must be the independently verified Studio21
keyboard/private-safe candidate, assembled here from pinned originals.
"""
from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

from build_studio21_keyboard_section_move import build as build_keyboard, SOURCE_BLOBS
from build_studio21_public_projection import build as build_private_safe

EXAMPLES = Path(__file__).resolve().parents[1] / "examples" / "collaborative-communication-medium"
FILES = ("MetaCanvas_Studio21_Consulenza_IT.html", "MetaCanvas_Studio21_Consulenza_EN.html")

STYLE = r"""
/* R1: contextual actions for a selected visual object; purely runtime UI. */
#me-visual-actions[hidden]{display:none!important}
#me-visual-actions{
  position:fixed;z-index:2147482300;display:flex;align-items:center;
  gap:5px;flex-wrap:nowrap;max-width:calc(100vw - 18px);min-height:43px;
  padding:5px 7px;border:1px solid var(--line,#b9d0cc);
  border-radius:13px;background:var(--paper,#fff);color:var(--ink,#183146);
  box-shadow:0 9px 30px #071c2e38;box-sizing:border-box;
  font:600 12px/1.3 system-ui,sans-serif
}
#me-visual-actions button{
  border-radius:8px;padding:8px 9px;min-height:32px;
  font:inherit;white-space:nowrap;border:1px solid transparent;
  background:var(--ui-subtle,#eff8f6);color:inherit
}
#me-visual-actions button:hover{border-color:var(--accent,#087b70);background:#e3f6f0}
#me-visual-actions button:focus-visible{outline:3px solid #e3a04c;outline-offset:1px}
@media(max-width:520px){
  #me-visual-actions{gap:2px;padding:4px;border-radius:10px}
  #me-visual-actions button{font-size:11px;padding:7px 6px;min-height:30px}
}
"""

VISUAL_METHODS = r"""
// R1 direct editing: operate on the native Studio21 selected object, never
// on a parallel model. The toolbar is DOM-only and absent from exports.
function visualActionsHide(){
 const bar=document.getElementById('me-visual-actions');
 if(bar){bar.hidden=true;bar.removeAttribute('data-selected-id')}
}
function visualActionsEnsure(){
 let bar=document.getElementById('me-visual-actions');
 if(bar)return bar;
 bar=document.createElement('div');
 bar.id='me-visual-actions';bar.hidden=true;
 bar.setAttribute('role','toolbar');
 const en=(document.documentElement.lang||'it').toLowerCase().startsWith('en');
 bar.setAttribute('aria-label',en?'Selected object actions':'Azioni dell’oggetto selezionato');
 const actions=[
  ['text',en?'Edit text':'Modifica testo'],
  ['style',en?'Style':'Stile'],
  ['size',en?'Size / position':'Dimensioni'],
  ['copy',en?'Duplicate':'Duplica']
 ];
 for(const [action,label] of actions){
  const button=document.createElement('button');button.type='button';
  button.dataset.visualAction=action;button.textContent=label;
  button.addEventListener('pointerdown',event=>event.stopPropagation());
  button.addEventListener('click',event=>{
   event.stopPropagation();
   const id=bar.dataset.selectedId;
   if(!id||id!==selectedId||!current().elements.some(n=>n.id===id)){
    visualActionsHide();return;
   }
   visualActionsHide();
   if(action==='text'){startDirectEdit(id);return}
   if(action==='style'){openQuick('node',id);return}
   if(action==='size'){renderInspector();openPanel('properties');return}
   if(action==='copy'){duplicateNode()}
  });
  bar.append(button);
 }
 document.body.append(bar);
 return bar;
}
function visualActionsSync(){
 const existing=document.getElementById('me-visual-actions');
 if(presenting||publicMode||readingMode||editingId||
    !document.getElementById('quickEditor')?.hidden||
    !selectedId||!hasNode()){
  if(existing)visualActionsHide();
  return;
 }
 const target=document.querySelector('#canvas .node[data-id="'+CSS.escape(selectedId)+'"]');
 if(!target||!target.classList.contains('is-selected')){
  if(existing)visualActionsHide();return;
 }
 const rect=target.getBoundingClientRect();
 const canvas=document.getElementById('canvas')?.getBoundingClientRect();
 if(!canvas||rect.bottom<canvas.top||rect.top>canvas.bottom||
    rect.right<canvas.left||rect.left>canvas.right||
    rect.bottom<=0||rect.top>=window.innerHeight){
  if(existing)visualActionsHide();return;
 }
 const bar=visualActionsEnsure();
 bar.dataset.selectedId=selectedId;
 const text=bar.querySelector('[data-visual-action="text"]');
 text.hidden=selected()?.type==='image';
 bar.hidden=false;
 const width=Math.min(bar.offsetWidth,window.innerWidth-16);
 const height=bar.offsetHeight;
 const left=Math.max(8,Math.min(window.innerWidth-width-8,rect.left));
 const above=rect.top-height-9;
 const below=rect.bottom+9;
 const top=above>=8?above:Math.min(
    Math.max(8,below),Math.max(8,window.innerHeight-height-8));
 bar.style.left=Math.round(left)+'px';
 bar.style.top=Math.round(top)+'px';
}
window.addEventListener('scroll',visualActionsSync,true);
window.addEventListener('resize',visualActionsSync);
"""

PATCHES = (
    (
        "function selectNode(id,show=true){",
        VISUAL_METHODS + "\nfunction selectNode(id,show=true){",
    ),
    (
        " renderLayers(); // La selezione non apre automaticamente l’editor generale.",
        " renderLayers();visualActionsSync(); // La selezione non apre automaticamente l’editor generale.",
    ),
    (
        " updateLinkPositions();renderLayers();}",
        " updateLinkPositions();renderLayers();visualActionsHide();}",
    ),
    (
        "if(editingId)cancelDirectEdit();closeQuick();selectedId=n.id;selectedLinkId=null;",
        "if(editingId)cancelDirectEdit();closeQuick();visualActionsHide();selectedId=n.id;selectedLinkId=null;",
    ),
    (
        "function openQuick(kind,id,anchor){closeQuick();",
        "function openQuick(kind,id,anchor){closeQuick();visualActionsHide();",
    ),
    (
        "editingId=id;syncEditBar();d.contentEditable='true';",
        "editingId=id;visualActionsHide();syncEditBar();d.contentEditable='true';",
    ),
    (
        "function renderCanvas(){drawCanvas($('#canvas'),current(),(presenting||publicMode)?'present':'edit');requestAnimationFrame(markTextOverflow)}",
        "function renderCanvas(){drawCanvas($('#canvas'),current(),(presenting||publicMode)?'present':'edit');requestAnimationFrame(()=>{markTextOverflow();visualActionsSync()})}",
    ),
    (
        "mount.onpointerdown=e=>{if(e.target===mount||e.target===nodes){selectedId=null;",
        "mount.onpointerdown=e=>{if(e.target===mount||e.target===nodes){visualActionsHide();selectedId=null;",
    ),
    (
        "let doc=document.documentElement.cloneNode(true);const grip=",
        "let doc=document.documentElement.cloneNode(true);doc.querySelector('#me-visual-actions')?.remove();const grip=",
    ),
)


FIRST_USE_SOURCE = (
    ' Nella colonna Schede scegli <b>Demo MAIOS</b> per presentarla o '
    '<b>Canvas vuoto</b> per iniziare. Usa Salva lavoro per scaricare il tuo HTML.'
)
FIRST_USE_IT = (
    ' Scegli <b>Demo MAIOS</b> o <b>Canvas vuoto</b> nelle Schede. '
    '<b>Clicca un oggetto</b> per modificare testo, stile e dimensioni direttamente '
    'nel canvas. Usa Salva lavoro per conservarlo.'
)
FIRST_USE_EN = (
    ' Choose <b>MAIOS Demo</b> or <b>Blank Canvas</b> in Slides. '
    '<b>Click an object</b> to edit text, style and size directly '
    'on the canvas. Use Save Work to keep a copy.'
)


def patch_source(original: str) -> str:
    if original.count("</style>") < 1:
        raise ValueError("Studio21 style element missing")
    result=original.replace("</style>",STYLE+"\n</style>",1)
    if result.count(FIRST_USE_SOURCE)!=1:
        raise ValueError("Studio21 first-use entry drift")
    en='<html lang="en">' in original
    result=result.replace(FIRST_USE_SOURCE,FIRST_USE_EN if en else FIRST_USE_IT,1)
    for before, after in PATCHES:
        if result.count(before)!=1:
            raise ValueError("Studio21 source drift at "+before[:75])
        result=result.replace(before,after,1)
    if result.count("function visualActionsSync()")!=1:
        raise AssertionError("Visual actions injected more than once")
    return result


def build(output_dir: Path, source_root: Path = EXAMPLES) -> list[Path]:
    output_dir=Path(output_dir).resolve()
    source_root=Path(source_root).resolve()
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValueError("Refusing to overwrite an existing nonempty candidate directory")
    with tempfile.TemporaryDirectory(prefix="studio21-visual-r1-") as tmp:
        root=Path(tmp)
        keyboard=root/"keyboard";safe=root/"safe"
        build_keyboard(source_root,keyboard)
        build_private_safe(keyboard,safe)
        patched={name:patch_source((safe/name).read_text(encoding="utf-8")) for name in FILES}
        output_dir.mkdir(parents=True,exist_ok=True)
        for name,html in patched.items():
            (output_dir/name).write_text(html,encoding="utf-8")
    return [output_dir/name for name in FILES]


def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument("--output-dir",type=Path,required=True)
    p.add_argument("--source-root",type=Path,default=EXAMPLES)
    args=p.parse_args()
    for file in build(args.output_dir,args.source_root):
        print("VISUAL-R1",file)


if __name__=="__main__":
    main()
