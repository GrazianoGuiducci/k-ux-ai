"""Build exact K-UX-AI v5.8 candidate from v5.7, preserving its recorded bytes.

The builder patches only the operator-requested Home copy and Activity rail
controls. `--check` compares the existing candidate without rewriting it.
"""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'labs/nautico-ui-v4/19-griglia-rail-free-v57.html'
OUT = ROOT / 'labs/nautico-ui-v4/20-griglia-rail-home-v58.html'
BASE_SHA = 'e733a306b85f2ac3abefe20fa6801aa73b2b178e7c108b40d05bb07c5021db2d'
OUTPUT_SHA = '799727c0283c61829796f20d1c4b45e652c3b2dd8d6056fe5577b0460ee3d9ad'

STYLE = '''
/* v5.8 — one compact Activity toolbar, same three operational states. */
body[data-kux-screen="work"] .intent-dock .kux-rail-head{
 position:sticky;top:0;z-index:7;display:flex;align-items:center;justify-content:center;
 gap:4px;flex:0 0 auto;min-height:34px;width:100%;min-width:0;
 padding:2px 0;background:var(--soft);
}
body[data-kux-screen="work"] .intent-dock .kux-rail-head #kuxRailToggle,
body[data-kux-screen="work"] .intent-dock .kux-rail-head #railVisibility{
 display:grid!important;place-items:center;flex:0 0 29px;
 width:29px!important;min-width:29px!important;height:29px!important;min-height:29px!important;
 margin:0!important;padding:0!important;border:1px solid var(--line);
 border-radius:8px;background:var(--surface);color:var(--ink);
 font-size:18px;line-height:1;
}
body[data-kux-screen="work"] .intent-dock .kux-rail-head .dock-caption{
 display:none!important;margin:0!important;white-space:nowrap!important;
 font-size:11px!important;line-height:1.1!important;letter-spacing:.07em!important;
}
body[data-kux-screen="work"][data-kux-rail-expanded="true"] .intent-dock .kux-rail-head{
 justify-content:flex-end;gap:7px;padding:2px 8px;
}
body[data-kux-screen="work"][data-kux-rail-expanded="true"] .intent-dock .kux-rail-head .dock-caption{
 display:block!important;margin-right:auto!important;
}
body[data-kux-screen="work"][data-kux-activities="peek"] .kux-rail-head #kuxRailToggle{display:none!important}
body[data-kux-screen="work"][data-kux-activities="hidden"] .kux-rail-head{display:none!important}
body[data-kux-screen="work"][data-kux-activities="previews"] .kux-rail-head #railVisibility{display:grid!important}
/* The Activity header is a control group, not a second scroller or a count panel. */
body[data-kux-screen="work"] .intent-dock .kux-rail-head+ .avatar-dock{min-height:0}
/* Home: the operator's current definition of Kernel UX-AI, across Web and apps. */
.kux-home-story #homeTitle{font-size:clamp(34px,3.4vw,60px);line-height:1.04;letter-spacing:-.045em;margin:8px 0 5px}
.kux-home-story .kux-home-thesis{font-size:clamp(18px,1.5vw,24px);font-weight:550;line-height:1.22;letter-spacing:-.023em;margin:0 0 13px}
.kux-home-story .intro-desc,.kux-home-story .kux-home-depth,.kux-home-story .kux-home-next{
 font-size:clamp(13px,.9vw,15px);line-height:1.38;margin-bottom:9px;
}
.kux-home-story .kux-home-demo-boundary{font-size:12px;line-height:1.35;color:var(--muted);margin:2px 0 0;}
body[data-kux-screen="home"] .home-screen[data-fit="true"] .kux-home-story #homeTitle{font-size:clamp(32px,3.2vw,52px)}
body[data-kux-screen="home"] .home-screen[data-fit="true"] .kux-home-story .intro-desc,
body[data-kux-screen="home"] .home-screen[data-fit="true"] .kux-home-story .kux-home-depth,
body[data-kux-screen="home"] .home-screen[data-fit="true"] .kux-home-story .kux-home-next{font-size:13px;line-height:1.33}
@media(max-width:780px){
 .kux-home-story #homeTitle{font-size:clamp(32px,5.1vw,46px)}
 .kux-home-story .kux-home-thesis{font-size:19px}
 .kux-home-story .intro-desc,.kux-home-story .kux-home-depth,.kux-home-story .kux-home-next{font-size:14px;line-height:1.42}
}
'''

OLD_HOME = '''<div class="kux-home-story"><div class="eyebrow">K-UX-AI · IL DESIGN DELL’INTERAZIONE</div><h1 id="homeTitle">Un lavoro.<br><em>Molti modi di entrarci.</em></h1><h2 class="kux-home-thesis">UX-AI evolutiva e nuove possibilità</h2><p class="intro-desc">K-UX-AI sviluppa interfacce modulari per lavorare con kernel e sistemi agentici complessi, in ambito aziendale, professionale e di ricerca. Questa griglia è una delle forme possibili.</p><p class="kux-home-depth">Nel sistema integrato, contesto, eventi, competenze e risorse potranno orientare il campo, preservare continuità e sostenere le azioni. <strong>Qui sperimenti la UI con dati locali</strong>: adattamento cognitivo e agenti reali dipendono dal kernel ricevente.</p><p class="kux-home-next">Scegli un punto d’ingresso oppure esplora: una notifica qualificata potrà richiamare gli strumenti pertinenti quando il sistema sarà collegato. <a href="https://github.com/GrazianoGuiducci/k-ux-ai/blob/main/MANIFESTO.md" target="_blank" rel="noopener noreferrer" class="kux-home-learn">Approfondisci K-UX-AI ↗</a></p></div>'''
NEW_HOME = '''<div class="kux-home-story"><div class="eyebrow">K-UX-AI · IL DESIGN DELL’INTERAZIONE</div><h1 id="homeTitle">Kernel UX-AI</h1><h2 class="kux-home-thesis">per l’interazione in Sistemi Intelligenti.</h2><p class="intro-desc">Il progetto K-UX-AI fornisce un’interfaccia per gestire sistemi agentici complessi nei diversi ambiti lavorativi e di ricerca.</p><p class="kux-home-depth">Il sistema è modulare per contesto e azioni negli eventi: impara e si adatta, segue il contesto che evolve, ricorda le cose utili, mantiene la continuità operativa, assiste nel lavoro e rende disponibili gli strumenti e le risorse adatte. <a href="https://github.com/GrazianoGuiducci/k-ux-ai/blob/main/MANIFESTO.md" target="_blank" rel="noopener noreferrer" class="kux-home-learn">Approfondisci K-UX-AI ↗</a></p><p class="kux-home-next">Scegli il punto di ingresso e ciò che vuoi fare: il campo rende disponibili contesto, strumenti e possibilità di continuazione. Rispondendo a una notifica pertinente, il campo potrà configurarsi con gli strumenti adatti a comprendere e agire.</p><p class="kux-home-demo-boundary">Questa Griglia è un prototipo con dati dimostrativi. Apprendimento operativo, memoria e azioni reali dipendono dai kernel e dai servizi collegati.</p></div>'''

CHANGES = [
 ('<meta name="description" content="K-UX-AI v5.6: medium UI per kernel, canvas guidato, attività contestuali e interazioni continue. Demo sintetica Nautico.">', '<meta name="description" content="K-UX-AI v5.8: Home per i sistemi intelligenti e barra Attività compatta, con Canvas e tour contestuali. Demo sintetica Nautico.">'),
 ('<title>MAIOS · K-UX-AI — Griglia del fare v5.7 · Leggibilità e attività</title>', '<title>MAIOS · K-UX-AI — Griglia del fare v5.8 · Home e barra Attività</title>'),
 ('<style id="kux-v57-clarity-and-activity-rail">', '<style id="kux-v57-clarity-and-activity-rail">'),
 (OLD_HOME, NEW_HOME),
 ("const activityCount=document.createElement('small');activityCount.id='activityCount';activityCount.className='kux-dock-count';activityCount.textContent='10 disponibili';\n", ''),
 ("activityRail.insertBefore(railVisibility,activityRail.querySelector('.dock-caption'));activityRail.insertBefore(activityCount,shell.dock);", "activityRail.insertBefore(railVisibility,activityRail.querySelector('.dock-caption'));"),
 ("const shown=state.panels.filter(p=>p.context===state.activeContext&&!p.minimized).length;\n activityCount.textContent='10 accessi · '+shown+' nel campo';activityCount.title='10 attività disponibili; '+shown+' schede aperte in '+ctxName(state.activeContext);", "activityRail.title='Attività disponibili per '+ctxName(state.activeContext);"),
 ("if(caption){caption.textContent='ATTIVITÀ';const sub=document.createElement('small');sub.className='kux-dock-context';sub.textContent=' · '+ctxName(state.activeContext);caption.append(sub);caption.title='Ambiente '+ctxName(state.activeContext);}", "if(caption){caption.textContent='ATTIVITÀ';caption.title='Attività per '+ctxName(state.activeContext);}"),
 ("button.textContent=expanded?'‹ Icone':'Anteprime ›';button.setAttribute('aria-expanded',String(expanded));", "button.textContent=expanded?'▦':'▤';button.setAttribute('aria-expanded',String(expanded));button.setAttribute('aria-pressed',String(expanded));"),
 ("button.addEventListener('click',()=>{expanded=!expanded;onChanged(expanded);apply();render();reflow();button.focus({preventScroll:true});});", "const setExpanded=(next,{focus=false}={})=>{if(expanded===next)return;expanded=next;apply();onChanged(expanded);render();reflow();if(focus)button.focus({preventScroll:true});};\n  button.addEventListener('click',()=>setExpanded(!expanded,{focus:true}));"),
 ("return {expanded:()=>expanded,width:()=>current,decorate:", "return {expanded:()=>expanded,width:()=>current,setExpanded,decorate:"),
 ("if(next==='hidden')closeQuickPeek?.();\n activitiesMode=next;updateActivitiesRail();", "if(next==='hidden')closeQuickPeek?.();\n if(['hidden','peek','icons'].includes(next)&&sidebarCtrl?.expanded())sidebarCtrl.setExpanded(false);\n activitiesMode=next;updateActivitiesRail();"),
 ("if(sidebarCtrl?.expanded()){activitiesMode='previews';updateActivitiesRail();}", "const head=document.createElement('div');head.className='kux-rail-head';head.setAttribute('role','group');head.setAttribute('aria-label','Controlli della barra Attività');\n activityRail.insertBefore(head,activityRail.firstChild);head.append(activityRail.querySelector('.dock-caption'),railVisibility,$('kuxRailToggle'));\n if(sidebarCtrl?.expanded()){activitiesMode='previews';updateActivitiesRail();}"),
 ("version:'lab-2026-10-11-r5.7',liveAI:false", "version:'lab-2026-10-11-r5.8',liveAI:false"),
]

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build() -> bytes:
    raw=BASE.read_bytes()
    if sha(raw)!=BASE_SHA:
        raise RuntimeError('v5.7 source changed; stop to reconcile its Git/receipt identity')
    content=raw.decode('utf-8')
    for before,after in CHANGES:
        if before==after: continue
        if content.count(before)!=1:
            raise RuntimeError(f'Expected one source anchor, found {content.count(before)}: {before[:90]!r}')
        content=content.replace(before,after,1)
    if '<style id="kux-v57-clarity-and-activity-rail">' not in content:
        raise RuntimeError('style anchor unavailable')
    content=content.replace('</head>','<style id="kux-v58-compact-rail-and-home">\n'+STYLE+'</style>\n</head>',1)
    data=content.encode('utf-8')
    if OUTPUT_SHA!='__PENDING__' and sha(data)!=OUTPUT_SHA:
        raise RuntimeError('candidate SHA changed: check source/build method')
    return data

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check',action='store_true')
    a=ap.parse_args()
    data=build()
    if a.check:
        if not OUT.exists() or OUT.read_bytes()!=data: raise SystemExit('CHECK FAILED: output bytes differ')
    else:
        OUT.write_bytes(data)
    print('PASS' if a.check else 'BUILT',OUT.name,len(data),sha(data))

if __name__=='__main__': main()
