#!/usr/bin/env python3
"""Recover the shared visual editing flow on the five integrity candidates.

Use the existing R1 native action adapters, Flat layout, search, panels and
template engine. Do not add another document, selection or history owner.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import tempfile
from pathlib import Path

from build_metacanvas_integrity_candidates import build as build_integrity, EXAMPLES, MODEL
from build_studio21_visual_actions import STYLE, PATCHES, FIRST_USE_SOURCE, FIRST_USE_IT, FIRST_USE_EN
from build_studio21_keyboard_section_move import blob_sha

CSS = r"""
/* A hidden rail must not leave an empty grid column at medium widths. */
body.hide-slide-rail:not(.guided-playground):not(.presenting):not(.reading-mode) .editor-shell {
  display:grid!important;grid-template-columns:minmax(0,1fr)!important;
}
/* Flat is the existing focus surface: preserve the user's guide outside it. */
body.flat-layout:not(.reading-mode):not(.public-copy) #publicFirstUse:not(:has(#guideOptions)) {display:none!important}
/* The guided tutorial already has its own compact focus and progression. */
body.guided-playground #me-template-entry {display:none!important}
/* Preserve usable width when a side inspector and the slide rail compete. */
@media(min-width:1001px) and (max-width:1280px) {
 body.panel-open:not(.guided-playground):not(.reading-mode):not(.presenting):is([data-dock="left"],[data-dock="right"]):has(#propertyPanel.drawer-open) .editor-shell {
   grid-template-columns:minmax(0,1fr)!important;
 }
 body.panel-open:not(.guided-playground):not(.reading-mode):not(.presenting):is([data-dock="left"],[data-dock="right"]):has(#propertyPanel.drawer-open) .slide-rail {
   position:relative!important;top:auto!important;width:100%!important;min-width:0!important;max-width:none!important;max-height:108px!important;overflow:auto!important;padding:5px 8px!important;
 }
 body.panel-open:not(.guided-playground):not(.reading-mode):not(.presenting):is([data-dock="left"],[data-dock="right"]):has(#propertyPanel.drawer-open) .slide-rail-list {
   display:flex;flex-direction:row;gap:6px;overflow-x:auto;
 }
 body.panel-open:not(.guided-playground):not(.reading-mode):not(.presenting):is([data-dock="left"],[data-dock="right"]):has(#propertyPanel.drawer-open) .slide-rail-chip {min-width:125px!important}
 body.panel-open:not(.guided-playground):not(.reading-mode):not(.presenting):has(#propertyPanel.drawer-open) .slide-rail .mini {display:none}
}
/* Flat's padding shorthand must not allow the inspector to cover the canvas. */
@media(min-width:1001px) {
 body.flat-layout[data-dock="right"].panel-open:has(#propertyPanel.drawer-open) .work {padding-right:calc(var(--property-panel-width,360px) + 16px)!important}
 body.flat-layout[data-dock="left"].panel-open:has(#propertyPanel.drawer-open) .work {padding-left:calc(var(--property-panel-width,360px) + 16px)!important}
}
/* The guided viewport is its own layout, never a two-column standard editor.
   Opening a side inspector must not silently cover the subject. */
@media(min-width:1001px) {
 body.guided-playground[data-dock="right"].panel-open:has(#propertyPanel.drawer-open) .work {padding-right:calc(var(--property-panel-width,360px) + 16px)!important}
 body.guided-playground[data-dock="left"].panel-open:has(#propertyPanel.drawer-open) .work {padding-left:calc(var(--property-panel-width,360px) + 16px)!important}
}
body.guided-playground:not(.reading-mode):not(.presenting) .work .editor-shell {
 display:block!important;grid-template-columns:none!important;
}
/* On touch-size screens keep the editor and its native confirmation in
   separate viewport bands. The mini-editor remains scrollable. */
@media(max-width:700px) {
 body[data-theme]:has(#quickEditor:not([hidden])) #quickEditor {
  top:6px!important;left:6px!important;right:auto!important;bottom:auto!important;
  width:calc(100vw - 12px)!important;max-width:calc(100vw - 12px)!important;
  height:auto!important;min-height:0!important;max-height:calc(100dvh - 76px)!important;
  resize:none!important;overflow:auto;
 }
 body:not(.presenting):not(.public-copy):has(#quickEditor:not([hidden])) #editActionBar {
  position:fixed!important;bottom:8px!important;top:auto!important;left:50%!important;right:auto!important;
  transform:translateX(-50%)!important;z-index:185!important;margin:0!important;
  max-width:calc(100vw - 12px)!important;justify-self:auto!important;
 }
}
/* Fit first on phones in Flat; native zoom remains the intentional pan route. */
@media(max-width:510px) {
 body.flat-layout:not(.reading-mode):not(.presenting) #canvasViewport .canvas-wrap {min-width:0!important}
}
body.public-copy #me-template-entry,body.presenting #me-template-entry {display:none!important}
"""

def once(source, before, after):
    if source.count(before) != 1:
        raise ValueError("Visual flow source drift: " + before[:100])
    return source.replace(before, after, 1)

def patch(original):
    en = '<html lang="en">' in original
    html = original.replace("</style>", STYLE + CSS + "\n</style>", 1)
    if FIRST_USE_SOURCE in html:
        html = once(html, FIRST_USE_SOURCE, FIRST_USE_EN if en else FIRST_USE_IT)
    for before, after in PATCHES:
        html = once(html, before, after)
    # Synchronize against native interaction state, not a second controller.
    html = once(html, "if(presenting||publicMode||readingMode||editingId||",
                "if(presenting||publicMode||readingMode||editingId||document.body.classList.contains('panel-open')||")
    html = once(html, "window.addEventListener('scroll',visualActionsSync,true);\nwindow.addEventListener('resize',visualActionsSync);",
                """let visualFrame=0;
function visualActionsSchedule(){
 if(visualFrame)return;
 visualFrame=requestAnimationFrame(()=>{visualFrame=0;visualActionsSync()});
}
window.addEventListener('scroll',visualActionsSchedule,true);
window.addEventListener('resize',visualActionsSchedule);""")
    # The edit lifecycle reaches this native function even when there is no commit.
    html = once(html, "$('#editOk').disabled=!editing}",
                "$('#editOk').disabled=!editing;visualActionsSchedule()}")
    html = once(html, "syncEditBar();requestAnimationFrame(updateFloatGrip);",
                "syncEditBar();scheduleFlatFit();requestAnimationFrame(updateFloatGrip);")
    html = once(html, "if(e.key==='Enter'){e.preventDefault();openQuick('node',n.id)}",
                "if(e.key==='Enter'){e.preventDefault();if(editingId)cancelDirectEdit(true);selectNode(n.id,false);openQuick('node',n.id)}")
    # Keep the native inspector connected to the actual selected object.
    html = once(html, "renderLayers();visualActionsSync(); // La selezione",
                "renderLayers();if($('#propertyPanel').classList.contains('drawer-open'))renderInspector();visualActionsSync(); // La selezione")
    html = once(html, "updateLinkPositions();renderLayers();visualActionsHide();}",
                "updateLinkPositions();renderLayers();if($('#propertyPanel').classList.contains('drawer-open'))renderInspector();visualActionsHide();}")
    # Return focus to the object after closing its inspector, including in the
    # guided surface where the general Tools button is intentionally hidden.
    html = once(html, "const target=which==='properties'&&selectedId?",
                "const target=(which==='properties'||(!which&&property.contains(focusBefore)))&&selectedId&&!readingMode?")
    # Restore the same selected object after a no-op or close; native history is untouched.
    html = once(html, "if(commitText&&value!==n.text)commit(()=>n.text=value);else{d.textContent=n.text;}",
                "if(commitText&&value!==n.text)commit(()=>n.text=value);else{d.textContent=n.text;}visualActionsSchedule();")
    label = "Templates" if en else "Template"
    html = once(html, '<button id="toggleTools" class="gear"',
                '<button id="me-template-entry" type="button" aria-controls="toolPanel">' + label + '</button><button id="toggleTools" class="gear"')
    # One direct route to the existing template section and one keyboard route to
    # the existing search. No duplicate palette or template engine.
    html = once(html, "$('#toggleSlideRail').onclick=()=>toggleSlideRail();",
                """$('#toggleSlideRail').onclick=()=>toggleSlideRail();
function visualOpenTools(templates){
 if(publicMode||presenting||document.body.classList.contains('guided-playground'))return;
 if(editingId)cancelDirectEdit(true);
 flushQuick();closeQuick();
 if(templates&&readingMode)changeView(false);
 openPanel('tools',templates?null:'#toolSearch');
 if(!templates)return;
 const filter=$('#toolSearch');
 if(filter.value){filter.value='';filter.dispatchEvent(new Event('input',{bubbles:true}));}
 const section=$('#toolPanel [data-section="templates"]');
 section.hidden=false;section.open=true;
 requestAnimationFrame(()=>{section.querySelector('summary')?.focus({preventScroll:true});section.scrollIntoView({block:'start',behavior:'instant'})});
}
$('#me-template-entry').onclick=()=>visualOpenTools(true);
document.addEventListener('keydown',e=>{
 if(e.defaultPrevented||e.isComposing||publicMode||presenting||document.body.classList.contains('guided-playground')||editingId||!$('#quickEditor').hidden||e.target.closest('input,textarea,select,[contenteditable="true"]'))return;
 if((e.ctrlKey||e.metaKey)&&e.shiftKey&&e.key.toLowerCase()==='p'){e.preventDefault();visualOpenTools(false)}
});""")
    before, after = MODEL.search(original), MODEL.search(html)
    if not before or not after or before.group(1)!=after.group(1):
        raise ValueError("Visual flow changed source document model")
    return html

def build(output_root, source_root=EXAMPLES):
    output_root=Path(output_root).resolve()
    if output_root==Path(source_root).resolve() or (output_root.exists() and any(output_root.iterdir())):
        raise ValueError("Refusing to overwrite existing source or candidate")
    with tempfile.TemporaryDirectory() as tmp:
        candidates=build_integrity(Path(tmp)/"integrity", source_root)
        receipt={}
        results={}
        for source in candidates:
            raw=source.read_bytes()
            new=patch(raw.decode("utf-8")).encode("utf-8")
            results[source.name]=new
            receipt[source.name]={"integrity_blob":blob_sha(raw),"candidate_blob":blob_sha(new),"candidate_sha256":hashlib.sha256(new).hexdigest(),"status":"unpublished-visual-flow"}
        output_root.mkdir(parents=True,exist_ok=True)
        for name, raw in results.items():
            (output_root/name).write_bytes(raw)
        (output_root/"visual-flow-receipt.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return [output_root/name for name in results]

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--output-root",type=Path,required=True)
    parser.add_argument("--source-root",type=Path,default=EXAMPLES)
    args=parser.parse_args()
    build(args.output_root,args.source_root)
