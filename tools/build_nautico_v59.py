from pathlib import Path
import hashlib
import re

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT / 'labs/nautico-ui-v4/20-griglia-rail-home-v58.html'
OUT=ROOT / 'labs/nautico-ui-v4/21-griglia-perceptual-continuity-v59.html'
expected = '799727c0283c61829796f20d1c4b45e652c3b2dd8d6056fe5577b0460ee3d9ad'
raw = BASE.read_bytes()
assert hashlib.sha256(raw).hexdigest() == expected
html=raw.decode('utf-8')
replacements=[]

def swap(before, after):
    global html
    n=html.count(before)
    if n!=1: raise ValueError(f"patch target expected once, found {n}: {before[:90]}")
    replacements.append((before,after))
    html=html.replace(before,after,1)

swap('K-UX-AI v5.8: Home per i sistemi intelligenti e barra Attività compatta, con Canvas e tour contestuali. Demo sintetica Nautico.',
     'K-UX-AI v5.9: gerarchia delle schede, tour guidato continuo e microinterazioni. Demo sintetica Nautico.')
swap('<title>MAIOS · K-UX-AI — Griglia del fare v5.8 · Home e barra Attività</title>',
     '<title>MAIOS · K-UX-AI — Griglia del fare v5.9 · Continuità percettiva</title>')

# Keep domain meaning in existing receiver; create a visual hierarchy, not another domain controller.
before = '<div class="module-heading"><span class="module-ico" aria-hidden="true">${esc(readIntent(p.intent).icon)}</span><span><strong class="module-title"></strong><small class="module-subtitle"></small></span></div>'
after = '<div class="module-heading"><span class="module-ico" aria-hidden="true">${esc(readIntent(p.intent).icon)}</span><div class="module-heading-copy"><div class="module-heading-meta"><span class="module-section"></span><span class="module-action"></span></div><strong class="module-title"></strong><small class="module-subtitle"></small><small class="module-info"></small></div></div>'
swap(before,after)

before = "const intent=readIntent(p.intent);p.el.querySelector('.module-title').textContent=intent.verb;p.el.querySelector('.module-subtitle').textContent=ctxName(p.context);p.el.querySelector('.module-ico').textContent=intent.icon;"
after = '''const intent=readIntent(p.intent),ctxMeta=contexts[p.context]||contexts.poppa;
 const names={capire:'Questione presente',fare:'Porta un contributo',controllare:'Riscontri e criteri',esplorare:'Oggetti e relazioni',progettare:'Alternative e conseguenze',organizzare:'Relazioni di lavoro',comunicare:'Domande e contributi',presentare:'Percorso nel tempo',riprendere:'Punto di continuazione',sperimentare:'Nuove possibilità',monitorare:'Fonti in relazione',confrontare:'Confronto contestuale',chat:'Dialogo di lavoro'};
 const section=p.el.querySelector('.module-section'),action=p.el.querySelector('.module-action'),title=p.el.querySelector('.module-title'),subtitle=p.el.querySelector('.module-subtitle'),info=p.el.querySelector('.module-info');
 section.textContent=ctxMeta.name;section.title='Sezione · '+ctxMeta.name;
 action.textContent=intent.verb;action.title='Azione · '+intent.verb;
 title.textContent=names[p.intent]||intent.verb;title.title=title.textContent;
 subtitle.textContent=ctxMeta.subtitle;subtitle.title=ctxMeta.subtitle;
 info.textContent=ctxMeta.source.split(' · ')[0];info.title='Fonte dimostrativa · '+ctxMeta.source;
 p.el.querySelector('.module-ico').textContent=intent.icon;'''
swap(before,after)

before="target.scrollIntoView({block:'start',behavior:'instant'});"
after="target.scrollIntoView({block:'nearest',inline:'nearest',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});"
swap(before,after)
swap("version:'lab-2026-10-11-r5.8'","version:'lab-2026-10-11-r5.9'")

# The tour content is a separate surface from the spotlight's carrier; let it settle with a short cue.
before = "requestAnimationFrame(placeHomeTour);\n}\nfunction homeSlotOrder()"
after = """requestAnimationFrame(placeHomeTour);
 if(!matchMedia('(prefers-reduced-motion: reduce)').matches){
  const nodes=[$('homeTourText'),$('homeTourCausality')];
  for(const node of nodes){node.getAnimations().forEach(a=>a.cancel());node.animate([{opacity:.42,transform:'translateY(6px)'},{opacity:1,transform:'translateY(0)'}],{duration:240,easing:'cubic-bezier(.2,.72,.16,1)'});}
 }
}\nfunction homeSlotOrder()"""
swap(before,after)

css=r'''
<style id="kux-v59-guided-continuity">
/* Shared interaction timing, with actual state changes as the source of truth. */
:root{--kux-motion-quick:200ms;--kux-motion-gesture:320ms;--kux-motion-orientation:520ms;--kux-motion-ease:cubic-bezier(.18,.72,.17,1)}
html{scroll-behavior:smooth}
body[data-kux-screen='home'] .home-screen:not([hidden]),
body[data-kux-screen='work'] .work-screen:not([hidden]){animation:kuxSceneArrival 230ms var(--kux-motion-ease) both}
@keyframes kuxSceneArrival{from{opacity:.2;transform:translateY(5px)}to{opacity:1;transform:translateY(0)}}
body[data-kux-screen='work'] .intent-dock{
 transition:width var(--kux-motion-gesture) var(--kux-motion-ease),min-width var(--kux-motion-gesture) var(--kux-motion-ease),max-width var(--kux-motion-gesture) var(--kux-motion-ease),opacity var(--kux-motion-gesture) var(--kux-motion-ease),box-shadow var(--kux-motion-gesture) var(--kux-motion-ease)}
body[data-kux-screen='work'][data-kux-activities='previews'] .intent-dock .avatar-dock,
body[data-kux-screen='work'][data-kux-activities='peek'] .intent-dock .avatar-dock{
 animation:kuxRailEntrance 290ms var(--kux-motion-ease) both}
@keyframes kuxRailEntrance{from{opacity:.6;transform:translateX(-9px)}to{opacity:1;transform:translateX(0)}}
body[data-kux-screen='work'] .kux-rail-head button,
body[data-kux-screen='work'] .module-tools button,
body[data-kux-screen='work'] #btnWorkMenu,
body[data-kux-screen='work'] #btnWorkMenu>span[aria-hidden='true']{
 transition:transform var(--kux-motion-quick) var(--kux-motion-ease),background-color var(--kux-motion-quick) var(--kux-motion-ease),border-color var(--kux-motion-quick) var(--kux-motion-ease),box-shadow var(--kux-motion-quick) var(--kux-motion-ease)}
body[data-kux-screen='work'] #btnWorkMenu[aria-expanded='true']{background:#d7efe4;border-color:#318b7e;box-shadow:0 2px 10px #174e4622}
body[data-kux-screen='work'] #btnWorkMenu>span[aria-hidden='true']{display:inline-block;transform-origin:center}
body[data-kux-screen='work'] #btnWorkMenu[aria-expanded='true']>span[aria-hidden='true']{transform:rotate(180deg)}
body[data-kux-screen='work'] #workMega:not([hidden]){animation:kuxToolsArrive 240ms var(--kux-motion-ease) both;transform-origin:top right}
@keyframes kuxToolsArrive{from{opacity:.5;transform:translateY(-8px) scale(.985)}to{opacity:1;transform:translateY(0) scale(1)}}

/* Spotlight and guidance carry the eye from one location to the next. */
.kux-tour-ring,.kux-tour-shade,#homeTourDialog.kux-home-tour[open]{
 transition:left var(--kux-motion-orientation) var(--kux-motion-ease),top var(--kux-motion-orientation) var(--kux-motion-ease),width var(--kux-motion-orientation) var(--kux-motion-ease),height var(--kux-motion-orientation) var(--kux-motion-ease),max-height var(--kux-motion-orientation) var(--kux-motion-ease)}
#homeTourDialog.kux-home-tour[open]{transform:none;will-change:left,top}
.kux-tour-ring{will-change:left,top,width,height}

/* Card reading hierarchy: section > action > title > subtitle > extra information.
   The latter stays in the focused card, not repeated across a dense overview. */
body[data-kux-screen='work'] .module-head{display:grid;grid-template-columns:minmax(0,1fr) auto;grid-template-rows:auto auto;align-content:start;gap:3px 7px;min-height:78px;padding:8px 10px 9px;align-items:start}
body[data-kux-screen='work'] .module-heading{display:contents}
body[data-kux-screen='work'] .module-ico{grid-column:1;grid-row:1;width:31px;height:31px;font-size:17px;border-radius:9px}
body[data-kux-screen='work'] .module-tools{grid-column:2;grid-row:1;justify-self:end;gap:3px}
body[data-kux-screen='work'] .module-tools button{height:27px;width:27px;min-width:27px;font-size:15px}
body[data-kux-screen='work'] .module-heading-copy{grid-column:1/-1;grid-row:2;display:grid;gap:2px;min-width:0}
body[data-kux-screen='work'] .module-heading-meta{display:flex;flex-wrap:nowrap;align-items:center;gap:7px;min-width:0}
body[data-kux-screen='work'] .module-section,
body[data-kux-screen='work'] .module-action{max-width:50%;min-width:0;font-size:10px;line-height:1.25;letter-spacing:.055em;font-weight:750;text-transform:uppercase;color:#496b6b;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}
body[data-kux-screen='work'] .module-action{color:#17433f;max-width:40%}
body[data-kux-screen='work'] .module-action::before{content:'·';padding-right:7px;color:#7ca69e}
body[data-kux-screen='work'] .module .module-title{display:block;max-width:none;font-size:16px;line-height:1.18;font-weight:770;letter-spacing:-.02em;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
body[data-kux-screen='work'] .module .module-subtitle{display:block;font-size:12px!important;line-height:1.35;color:#4b686a;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
body[data-kux-screen='work'] .module .module-info{display:none;font-size:11px;line-height:1.24;color:#617b7b;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
body[data-kux-screen='work'] .module[data-focused='true'] .module-info,
body[data-kux-screen='work'] .module[data-placement='full'] .module-info{display:block}

/* A smaller consistent type scale, with legibility and focus hierarchy intact. */
body[data-kux-screen='work'] .module-content h3{font-size:18px;line-height:1.2}
body[data-kux-screen='work'] .module-content p,
body[data-kux-screen='work'] .module-content .data-row,
body[data-kux-screen='work'] .module-content label,
body[data-kux-screen='work'] .source-tile strong,
body[data-kux-screen='work'] .message{font-size:13px;line-height:1.48}
body[data-kux-screen='work'] .module-foot,
body[data-kux-screen='work'] .module-foot button,
body[data-kux-screen='work'] .mini-caps,
body[data-kux-screen='work'] .source-note{font-size:11px}

/* Center the same three-dot affordance in every actual resize control. */
#kuxFocalDivider,.kux-grid-divider{display:grid;place-items:center;font-size:0!important;line-height:0;padding:0!important}
#kuxFocalDivider::before,.kux-grid-divider::after{display:block;line-height:1;transform:translateY(-1px)}
#kuxFocalDivider::before{content:'⋮';font-size:21px;color:#205f59}
.kux-grid-divider::after{content:'⋮';font-size:18px;color:#236c5c}

/* Align the checkbox to the first text line, rather than the whole row. */
body[data-kux-screen='work'] .module-content label.selectable-row{display:grid!important;grid-template-columns:18px minmax(0,1fr);align-items:start;gap:10px;margin:7px 0;padding:11px 12px}
body[data-kux-screen='work'] .module-content label.selectable-row>input[type='checkbox']{box-sizing:border-box;display:block;justify-self:center;align-self:start;width:16px!important;height:16px!important;min-width:16px!important;min-height:16px!important;margin:2px 0 0!important;padding:0!important;flex:none}
body[data-kux-screen='work'] .module-content label.selectable-row>span{display:block;color:var(--ink);font-size:13px;line-height:1.43;font-weight:620}

@media(max-width:760px){
 body[data-kux-screen='work'] .module-head{min-height:78px;padding:8px 9px}
 body[data-kux-screen='work'] .module .module-title{font-size:15px}
 body[data-kux-screen='work'] .module .module-info{display:none!important}
}
@media(prefers-reduced-motion:reduce){
 html{scroll-behavior:auto}
 body[data-kux-screen='home'] .home-screen:not([hidden]),
 body[data-kux-screen='work'] .work-screen:not([hidden]),
 body[data-kux-screen='work'] #workMega:not([hidden]),
 body[data-kux-screen='work'] .avatar-dock{animation:none!important}
 .kux-tour-ring,.kux-tour-shade,#homeTourDialog.kux-home-tour[open],
 body[data-kux-screen='work'] .intent-dock,
 body[data-kux-screen='work'] .kux-rail-head button,
 body[data-kux-screen='work'] .module-tools button,
 body[data-kux-screen='work'] #btnWorkMenu,
 body[data-kux-screen='work'] #btnWorkMenu>span[aria-hidden='true']{transition:none!important;animation:none!important}
}
</style>
'''
swap('</head>', css+'</head>')
import argparse
parser=argparse.ArgumentParser(description='Build source-pinned K-UX-AI v5.9 from exact v5.8')
parser.add_argument('--check',action='store_true',help='Check candidate bytes without writing')
args=parser.parse_args()
result=html.encode('utf-8')
expected_output='463d9d436ab982f4ab68ec0cd2b8770813d0346ecd26bf90b9335f0e0b57ed3a'
if hashlib.sha256(result).hexdigest()!=expected_output:
    raise RuntimeError('Candidate differs from the exact verified v5.9 source')
if args.check:
    if not OUT.exists() or OUT.read_bytes()!=result:
        raise SystemExit('Candidate missing or differs from reproducible build')
    print(f'OK: {OUT.name} ({len(result)} bytes; {expected_output})')
else:
    OUT.write_bytes(result)
    print(f'Wrote {OUT.name} ({len(result)} bytes; {expected_output})')
