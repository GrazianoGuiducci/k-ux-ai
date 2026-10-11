"""Generate K-UX-AI v5.11 from exact v5.10.1 source; never edit predecessor.

Run: python tools/build_nautico_v511.py [--check]
"""
from pathlib import Path
import argparse, hashlib
BASE = Path(__file__).resolve().parent.parent
SOURCE = BASE/'labs/nautico-ui-v4/23-griglia-home-balance-v5101.html'
OUTPUT = BASE/'labs/nautico-ui-v4/24-griglia-content-hierarchy-v511.html'
CSS = BASE/'tools/kux_card_rail_v511.css'
BASE_SHA256 = 'e448bd07dc406a68932e90ff220acc7b509a287cd8b91e9742593794849d6004'
OUTPUT_SHA256 = '67e8a1104d2abd66b886fad5354753a4db8964321c93947937de15f1917f434a'

def digest(x:bytes)->str:return hashlib.sha256(x).hexdigest()

def replace_once(s,a,b):
    assert s.count(a)==1, (a[:90],s.count(a))
    return s.replace(a,b,1)

def generate()->bytes:
    raw=SOURCE.read_bytes()
    assert digest(raw)==BASE_SHA256, f'Base source drift: {digest(raw)}'
    s=raw.decode('utf-8')
    s=replace_once(s,'K-UX-AI v5.10.1: Home bilanciata, copy leggibile e attività senza clipping. Demo sintetica Nautico.',
    'K-UX-AI v5.11: gerarchia del contenuto nelle schede, stato Attività riconciliato e animazioni contestuali. Demo sintetica Nautico.')
    s=replace_once(s,'<title>MAIOS · K-UX-AI — Griglia del fare v5.10.1 · Home bilanciata</title>',
      '<title>MAIOS · K-UX-AI — Griglia del fare v5.11 · Gerarchia e continuità</title>')
    s=replace_once(s," return helper(c.source)+core;", " return core;")
    start=""" const capsule=document.createElement('div');capsule.className='kux-context-capsule';
 const context=contexts[p.context]||contexts.poppa;
 capsule.textContent='Azione nella scheda '+intent.verb+' · contesto '+context.name+' · fonte dimostrativa '+context.source+'. La correlazione è illustrativa: l’effetto resta nel controller del contesto.';
 body.prepend(capsule);body.querySelectorAll(editableDraft).forEach(field=>{const key=draftKey(p,field);if(Object.hasOwn(state.drafts,key))field.value=state.drafts[key];});body.scrollTop=scroll;renderSection(p);"""
    dest=""" // Semantic work heading first; qualified source is available as a single optional readback.
 const context=contexts[p.context]||contexts.poppa;
 const capsule=document.createElement('details');capsule.className='kux-context-capsule kux-provenance';
 const sourceSummary=document.createElement('summary');sourceSummary.className='source-note';
 const sourceDot=document.createElement('span');sourceDot.className='bullet-dot';sourceDot.setAttribute('aria-hidden','true');
 const sourceId=document.createElement('span');sourceId.className='kux-source-id';
 sourceId.textContent='DATI DIMOSTRATIVI · '+context.source;
 const sourceMore=document.createElement('span');sourceMore.className='kux-source-more';sourceMore.textContent='Fonte e limiti ▾';
 sourceSummary.append(sourceDot,sourceId,sourceMore);
 const sourceLimit=document.createElement('p');sourceLimit.className='kux-source-limit';
 sourceLimit.textContent='Azione nella scheda '+intent.verb+' · contesto '+context.name+' · fonte dimostrativa '+context.source+'. La correlazione è illustrativa: l’effetto resta nel controller del contesto.';
 capsule.append(sourceSummary,sourceLimit);
 const workTitle=body.querySelector(':scope > h3');
 let after=workTitle;
 if(after?.nextElementSibling?.matches('p'))after=after.nextElementSibling;
 if(after)after.after(capsule);else body.prepend(capsule);
 body.querySelectorAll(editableDraft).forEach(field=>{const key=draftKey(p,field);if(Object.hasOwn(state.drafts,key))field.value=state.drafts[key];});body.scrollTop=scroll;renderSection(p);"""
    s=replace_once(s,start,dest)
    s=replace_once(s," if(remove){p.el?.remove();state.panels=state.panels.filter(x=>x!==p);state.slotOrder=state.slotOrder.filter(id=>id!==p.id);}",
                     " if(pendingAvatarClose?.panel===p.id)clearPendingAvatarClose();\n if(remove){p.el?.remove();state.panels=state.panels.filter(x=>x!==p);state.slotOrder=state.slotOrder.filter(id=>id!==p.id);}")
    s=replace_once(s," if(state.layout!=='free')arrangeUnpinnedPanels();placePanels();beginDividerSettle(true);\n notice(remove?",
                     " if(state.layout!=='free')arrangeUnpinnedPanels();placePanels();beginDividerSettle(true);\n // A closed nonfocused card must also invalidate its Activity entry.\n renderDock();updateHeader();\n notice(remove?")
    s=replace_once(s,"function setActivitiesMode(next){", """function animateRailReturn(previous,next){
 if(state.screen!=='work'||matchMedia('(max-width:760px)').matches||matchMedia('(prefers-reduced-motion: reduce)').matches)return;
 if(next==='hidden'||!['hidden','peek','icons'].includes(previous))return;
 for(const a of activityRail.getAnimations()){if(a.id==='kux-activity-return')a.cancel();}
 const motion=activityRail.animate([
  {clipPath:'inset(0 100% 0 0)',opacity:.15,transform:'translateX(-24px)'},
  {clipPath:'inset(0 0% 0 0)',opacity:1,transform:'translateX(0px)'}
 ],{duration:860,easing:'cubic-bezier(.18,.72,.17,1)',fill:'none'});
 motion.id='kux-activity-return';
}
function setActivitiesMode(next){""")
    s=replace_once(s, " if(['hidden','peek','icons'].includes(next)&&sidebarCtrl?.expanded())sidebarCtrl.setExpanded(false);\n activitiesMode=next;updateActivitiesRail();",
      " const previousActivitiesMode=activitiesMode;\n if(['hidden','peek','icons'].includes(next)&&sidebarCtrl?.expanded())sidebarCtrl.setExpanded(false);\n activitiesMode=next;updateActivitiesRail();\n animateRailReturn(previousActivitiesMode,next);")
    s=replace_once(s,"],{duration:390,easing:'cubic-bezier(.18,.76,.18,1)',fill:'none'});",
        "],{duration:840,easing:'cubic-bezier(.18,.76,.18,1)',fill:'none'});")
    s=replace_once(s,"],{duration:240,easing:'cubic-bezier(.2,.72,.16,1)'});",
        "],{duration:780,easing:'cubic-bezier(.2,.72,.16,1)'});")
    s=replace_once(s,"{duration:440,easing:'cubic-bezier(.2,.78,.18,1)'});",
        "{duration:800,easing:'cubic-bezier(.2,.78,.18,1)'});")
    s=replace_once(s,'</head>',"<style id=\"kux-v511-content-rail\">\n"+CSS.read_text(encoding='utf-8')+"\n</style>\n</head>")
    return s.encode('utf-8')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ns=ap.parse_args();out=generate();sha=digest(out)
    if OUTPUT_SHA256!='__TO_FILL__': assert sha==OUTPUT_SHA256, f'Candidate changed {sha}'
    if ns.check:
        assert OUTPUT.read_bytes()==out,'Build not byte-identical'
        print(f'OK --check SHA-256 {sha}')
    else:
        OUTPUT.write_bytes(out)
        print(f'Built {OUTPUT} bytes={len(out)} SHA-256 {sha}')
if __name__=='__main__':main()
