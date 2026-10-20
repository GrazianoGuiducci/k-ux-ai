"""Compose a public hosting-kernel profile with the unchanged GPT Griglia engine."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / 'examples/griglia/index.html'
REFERENCE_SHA256 = '1879dbe0d2ccba4c7db4701fe067c05ad1d20761aa2a6cf053f90b478118430b'


def replace_one(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f'GPT source anchor changed: {old[:80]}')
    return text.replace(old, new, 1)


def replace_pattern(text: str, pattern: str, replacement: str) -> str:
    updated, count = re.subn(pattern, lambda _: replacement, text, flags=re.S)
    if count != 1:
        raise ValueError(f'GPT source structure changed: {pattern[:80]}')
    return updated


def script_data(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')


def compose_tour(text: str, name: str, steps: list[dict]) -> str:
    """Keep the reference's tour anchors while composing its public guidance."""
    pattern = rf'const {name}=\[(.*?)\n\];'
    match = re.search(pattern, text, flags=re.S)
    if not match:
        raise ValueError(f'Missing guided tour: {name}')
    targets = [line.rsplit(',target:', 1)[1].rstrip(',').removesuffix('}')
               for line in match.group(1).splitlines() if ',target:' in line]
    if len(targets) != len(steps):
        raise ValueError(f'Guided-tour targets changed: {name}')
    composed = [script_data(step)[:-1] + ',target:' + target + '}'
                for step, target in zip(steps, targets)]
    return replace_pattern(text, pattern, f'const {name}=[\n' + ',\n'.join(composed) + '\n];')


def public_tours(profile: dict) -> tuple[list[dict], list[dict]]:
    """Stable tour fields select the public UI language without changing targets."""
    data = json.loads((ROOT / 'src/ui/locales/public-tours.json').read_text(encoding='utf-8'))
    selected = data[profile['locale']]
    selected['home'][0]['scope'] = selected['home'][0]['scope'].format(
        contexts=', '.join(context['name'] for context in profile['contexts'].values()))
    return selected['home'], selected['work']


def compose_card_layout(text: str) -> str:
    text = replace_one(text,
        '<div class="tile-head"><span class="tile-icon" aria-hidden="true">${esc(intent.icon)}</span><span class="tile-sequence">${String(index+1).padStart(2,\'0\')} / 10</span></div><div class="tile-center"><h3>${esc(intent.verb)}</h3>',
        '<div class="tile-head"><div class="tile-heading"><span class="tile-icon" aria-hidden="true">${esc(intent.icon)}</span><h3>${esc(intent.verb)}</h3></div><span class="tile-sequence">${String(index+1).padStart(2,\'0\')} / 10</span></div><div class="tile-center">')
    text = replace_one(text, 'function moduleElement(p){', '''function preparePanelResize(p){
 const el=p.el;el.getAnimations().forEach(animation=>animation.cancel());
 const stage=shell.stage.getBoundingClientRect(),box=el.getBoundingClientRect();
 const scaleX=stage.width/shell.stage.clientWidth||1,scaleY=stage.height/shell.stage.clientHeight||1;
 Object.assign(p,screenRect({x:(box.left-stage.left)/scaleX,y:(box.top-stage.top)/scaleY,w:box.width/scaleX,h:box.height/scaleY}));
 p.userSized=true;
 return {scaleX,scaleY};
}
function moduleElement(p){''')
    text = replace_one(text,
        'const initial={x:e.clientX,y:e.clientY,w:p.w,h:p.h};',
        'const scale=preparePanelResize(p);\n   const initial={x:e.clientX,y:e.clientY,w:p.w,h:p.h,...scale};')
    text = replace_one(text,
        'const size=screenRect({...p,w:initial.w+ev.clientX-initial.x,h:initial.h+ev.clientY-initial.y});\n     p.w=size.w;p.h=size.h;moduleStyles(p,screenRect(p));',
        'const size=screenRect({...p,w:initial.w+(ev.clientX-initial.x)/initial.scaleX,h:initial.h+(ev.clientY-initial.y)/initial.scaleY});\n     Object.assign(p,size);moduleStyles(p,screenRect(p));')
    text = replace_one(text,
        'focusPanel(p,{force:true});p.dock=null;p.maximized=false;p.manualPosition=true;\n   const step=e.shiftKey?40:15;',
        'focusPanel(p,{force:true});p.dock=null;p.maximized=false;p.manualPosition=true;\n   preparePanelResize(p);\n   const step=e.shiftKey?40:15;')
    text = replace_one(text,
        "if(p.compact&&!p.maximized&&!p.dock&&state.layout==='free'){",
        "if(p.compact&&!p.userSized&&!p.maximized&&!p.dock&&state.layout==='free'){")
    text = replace_one(text,
        'p.compact=!p.compact; p.maximized=false; p.dock=null;',
        'p.compact=!p.compact; p.userSized=false; p.maximized=false; p.dock=null;')
    return replace_one(text, '</head>', '''<style id="kux-public-card-layout">
.intent-grid .intent-tile{container-type:inline-size;border-radius:10px!important;padding:10px!important;gap:6px!important;justify-content:flex-start}
.intent-grid .tile-head{align-items:center;gap:10px;flex:none}
.intent-grid .tile-heading{display:flex;align-items:center;gap:10px;min-width:0;flex:1}
.intent-grid .tile-heading .tile-icon{flex:none;font-size:23px;line-height:1}
.intent-grid.kux-home-packed>.intent-tile .tile-heading h3{margin:0!important;line-height:1.12;font-size:clamp(17px,1.45vw,25px);letter-spacing:-.035em;overflow-wrap:normal}
.intent-grid.kux-home-packed>.intent-tile[data-home-role='principal'] .tile-heading h3{font-size:clamp(25px,2.2vw,36px)}
.intent-grid .tile-sequence{flex:none;font-size:10px;letter-spacing:.07em}
.intent-grid .tile-center{padding:0!important;margin:0 0 auto}
.intent-grid .tile-desc{max-width:none;line-height:1.35}
.intent-grid .tile-foot{flex:none;gap:8px;margin-top:4px}
.intent-grid .tile-drag{font-size:9px;letter-spacing:.04em}
.intent-grid .intent-tile[data-selected=true]{box-shadow:inset 0 0 0 1px #13886d,0 0 0 1px #13886d20!important}
.intent-grid .intent-tile[data-selected=true]::after{display:none}
@container(max-width:260px){.tile-head .tile-sequence{display:none}.tile-heading{gap:7px!important}.tile-heading h3{font-size:17px!important}.tile-heading .tile-icon{font-size:20px!important}}
@media(min-width:781px){
 .intent-grid.kux-home-packed{grid-auto-rows:minmax(108px,auto)}
 .intent-grid.kux-home-packed>.intent-tile{min-height:108px}
 .intent-grid.kux-home-packed>.intent-tile[data-featured='true']{min-height:224px}
 body[data-kux-screen='home'] .home-screen[data-fit='false'] .intent-grid.kux-home-packed{grid-auto-rows:minmax(108px,auto)!important}
 body[data-kux-screen='home'] .home-screen[data-fit='false'] .intent-grid.kux-home-packed>.intent-tile{min-height:108px!important}
 body[data-kux-screen='home'] .home-screen[data-fit='false'] .intent-grid.kux-home-packed>.intent-tile[data-featured='true']{min-height:224px!important}
}
@media(min-width:1051px) and (min-height:680px){
 body[data-kux-screen='home'] .home-screen[data-fit='true'] .intent-grid{grid-template-rows:repeat(var(--kux-home-rows,3),minmax(108px,1fr));grid-auto-rows:minmax(108px,1fr)}
 body[data-kux-screen='home'] .home-screen[data-fit='true'] .intent-grid>.intent-tile{gap:6px}
}
</style></head>''')


def activity_visual_assets(profile: dict, profile_path: Path) -> dict[str, Path]:
    """Only domain-owned local images and explicit colours enter the derivative."""
    assets = {}
    for intent, visual in profile.get('activityVisuals', {}).items():
        if not re.fullmatch(r'[a-z][a-z0-9-]*', intent):
            raise ValueError('Invalid activity visual ID')
        if not re.fullmatch(r'#[0-9a-fA-F]{6}', visual.get('color', '')):
            raise ValueError(f'Invalid activity colour: {intent}')
        if visual.get('position', 'center') not in {'center', 'left', 'right', 'center top', 'center bottom'}:
            raise ValueError(f'Invalid image position: {intent}')
        image = visual.get('image')
        if image is None:
            continue
        if not re.fullmatch(r'assets/[a-zA-Z0-9_/-]+\.(webp|png|jpg|jpeg)', image) or '..' in image:
            raise ValueError(f'Activity images must be local assets: {intent}')
        source = (profile_path.parent / image).resolve()
        if not source.is_relative_to(profile_path.parent.resolve()) or not source.is_file():
            raise ValueError(f'Missing domain visual asset: {image}')
        assets[image] = source
    empty_image = profile.get('emptyCanvas', {}).get('image')
    if empty_image is not None:
        if not re.fullmatch(r'assets/[a-zA-Z0-9_/-]+\.(svg|webp|png|jpg|jpeg)', empty_image) or '..' in empty_image:
            raise ValueError('Empty canvas images must be local assets')
        source = (profile_path.parent / empty_image).resolve()
        if not source.is_relative_to(profile_path.parent.resolve()) or not source.is_file():
            raise ValueError(f'Missing domain visual asset: {empty_image}')
        assets[empty_image] = source
    return assets


def build(profile_path: Path, output: Path, locale: str = 'en') -> dict:
    if locale not in {'en', 'it'}:
        raise ValueError('Unsupported public UI locale')
    if locale == 'it':
        profile_path = profile_path.with_name('PROFILE.it.json')
    source = REFERENCE.read_bytes()
    if hashlib.sha256(source).hexdigest() != REFERENCE_SHA256:
        raise ValueError('The selected GPT reference changed; assimilate it before rebuilding.')
    profile_bytes = profile_path.read_bytes()
    profile = json.loads(profile_bytes)
    visual_assets = activity_visual_assets(profile, profile_path)
    if profile.get('locale') != locale:
        raise ValueError('Profile and public UI locale differ')
    if profile.get('schema') != 'kux.hosting-kernel-profile.v1':
        raise ValueError('Unknown hosting-kernel profile')
    if set(profile['contexts']) != {'poppa', 'cantiere', 'fornitori', 'bordo', 'assistenza'}:
        raise ValueError('This GPT incarnation requires its five context carriers')
    for context in profile['contexts'].values():
        for field in ['name', 'subtitle', 'goal', 'source', 'items', 'unknown', 'next']:
            if field not in context:
                raise ValueError(f'Missing carrier field: {field}')
    runtime = (ROOT / 'src/ui/public-griglia.js').read_text(encoding='utf-8')
    has_visuals = profile.get('activityVisuals') or profile.get('emptyCanvas')
    visual_runtime = (ROOT / 'src/ui/activity-visuals.js').read_text(encoding='utf-8') if has_visuals else ''
    visual_css = (ROOT / 'src/ui/activity-visuals.css').read_text(encoding='utf-8') if has_visuals else ''
    text = source.decode('utf-8')
    text = compose_card_layout(text)
    home_tour, work_tour = public_tours(profile)
    text = compose_tour(text, 'tourSteps', home_tour)
    text = compose_tour(text, 'workTourSteps', work_tour)
    prelude = '<script>window.__UXAI_CONFIG__=' + script_data({'skin': 'atlas', 'start': 'home', 'profile': profile}) + ';\n' + runtime + '\n' + visual_runtime + '\n</script>'
    text = replace_one(text, "window.__UXAI_CONFIG__ = {skin:'atlas',start:'home'};", "// Hosting-kernel configuration is provided by the public source profile.")
    text = replace_one(text, '<body data-skin="atlas" data-start="home">', '<body data-skin="atlas" data-start="home" data-kux-product="' + html.escape(profile['id'], quote=True) + '">' + prelude)
    text = replace_pattern(text, r'const contexts=\{.*?\n\};?\s*const scenarios=', 'const contexts=' + script_data(profile['contexts']) + ';\nconst scenarios=')
    text = replace_pattern(text, r'const scenarios=\[.*?\n\];', 'const scenarios=' + script_data(profile['events']) + ';')
    text = replace_pattern(text, r'(<select id="contextSelect"[^>]*>).*?(</select>)',
                           '<select id="contextSelect" aria-label="' + ('Active context' if locale == 'en' else 'Contesto attivo') + '">' + ''.join('<option value="' + key + '">' + html.escape(value['name']) + '</option>' for key,value in profile['contexts'].items()) + '</select>')
    story = profile['home']
    eyebrow = '<div class="eyebrow">' + html.escape(story['eyebrow']) + '</div>' if story['eyebrow'] else ''
    intro = '<div class="kux-home-story">' + eyebrow + '<h1 id="homeTitle">' + html.escape(story['title']) + '</h1><h2 class="kux-home-thesis">' + html.escape(story['subtitle']) + '</h2>'
    intro += ''.join('<p class="' + cls + '">' + html.escape(story[key]) + '</p>' for cls, key in [('intro-desc', 'intro'), ('kux-home-depth', 'method'), ('kux-home-next', 'use'), ('kux-home-demo-boundary', 'scope')])
    intro += '</div>'
    text = replace_pattern(text, r'<div class="kux-home-story">[^\r\n]*</div>', intro)
    text = replace_pattern(text, r'<title>.*?</title>', '<title>' + html.escape(story['title']) + ' · MAIOS</title>')
    text = replace_pattern(text, r'<meta name="description" content="[^"]*">', '<meta name="description" content="' + html.escape(story['intro'], quote=True) + '">')
    info = '<dialog id="infoDialog" class="info-dialog"><div class="dialog-top"><div><div class="eyebrow">' + html.escape(profile['name']) + ' · PRESENTAZIONE E GUIDA</div><h3>Come usare questo spazio</h3></div><button type="button" id="closeInfo" aria-label="Chiudi">×</button></div>'
    info += '<p>' + html.escape(story['intro']) + '</p><p>Le schede hanno funzioni diverse: guida, contributo, confronto, monitoraggio, ripresa e dialogo. Si possono comporre intorno allo stesso lavoro conservando il focus e le bozze.</p>'
    info += '<p>' + html.escape(story['scope']) + '</p><div class="dialog-foot"><button id="resetSession" type="button">Riparti dalla Griglia</button><button type="button" id="okInfo">Torna al campo</button></div></dialog>'
    text = replace_pattern(text, r'<dialog id="infoDialog".*?</dialog>', info)
    text = replace_one(text, 'K-UX-AI <span class="brand-remainder">/ Kernel Nautico</span>', html.escape(profile['name']))
    text = text.replace('LABORATORIO · DATI DEMO', 'PRESENTAZIONE INTERATTIVA')
    text = replace_one(text, 'const dialogues=KUX_V46.createDiscussions();', 'const dialogues=window.KUXHostedGriglia.createDiscussions(KUX_V46.createDiscussions);')
    text = replace_one(text, "function panelContents(p){const c=contexts[p.context]||contexts.poppa,", "function panelContents(p){const hosted=window.KUXHostedGriglia.renderActivity(p,contexts[p.context]||contexts.poppa,state);if(hosted!==null)return hosted;const c=contexts[p.context]||contexts.poppa,")
    text = replace_one(text, "function sendChat(p,message){if(!message.trim())return;", "function sendChat(p,message){if(cfg.profile)return window.KUXHostedGriglia.sendChat(p,message);if(!message.trim())return;")
    text = replace_one(text, "function chatMarkdown(){return", "function chatMarkdown(){if(cfg.profile)return window.KUXHostedGriglia.chatMarkdown();return")
    text = replace_one(text, "if(act==='promote-item')return notice('L’ordine tecnico è di competenza del Kernel: questa scheda non cambia il piano di produzione.');", "if(act==='promote-item'){window.KUXHostedGriglia.promoteItem(p,Number(button.dataset.index));return;}")
    text = replace_one(text, "if(action.type==='demo.assistant.question'){", "if(action.type==='demo.assistant.question'){if(cfg.profile)return window.KUXHostedGriglia.askShared(action);")
    text = text.replace('Sono un assistente dimostrativo locale. Posso mostrare i campi e le attività della demo; non sono collegato a un modello AI.', 'Questo spazio presenta ' + profile['name'] + '. La guida usa le fonti del kernel; le domande inviate esplicitamente possono raggiungere MAIOS AI nel sito configurato.')
    text = text.replace('Assistente del laboratorio locale. La conversazione non usa un modello AI e nessun dato è inviato a un server.', 'Assistente di ' + profile['name'] + '. Con Invia, il testo della domanda raggiunge MAIOS AI; le bozze nelle altre schede restano locali.')
    text = text.replace("title:'Assistente K-UX-AI'", "title:" + script_data('Assistente di ' + profile['name']))
    text = text.replace("id:'nautico-griglia-shared-assistant-v4'", "id:" + script_data(profile['id'] + '-public-assistant-v1'))
    text = text.replace("id:'nautico-griglia-assistant-v4'", "id:" + script_data(profile['id'] + '-public-assistant-window-v1'))
    text = text.replace("subtitle:'Chat + modulo · ricevente locale'", "subtitle:" + script_data('Dialogo e contributi · ' + profile['name']))
    text = text.replace('Sessione locale azzerata. Non sono collegato a un modello AI.', 'Sessione locale azzerata. Puoi riprendere la guida o inviare una domanda a MAIOS AI.')
    text = text.replace('Solo dati dimostrativi. Configurare la vista non approva interventi sul Kernel Nautico.', 'Griglia illustrativa · contributi locali · domande inviate a MAIOS AI dove collegata.')
    text = text.replace('Contributo locale registrato nella scheda. Lettura della fonte demo, non risposta AI.', 'Domanda inviata a MAIOS AI con il contesto pubblico della scheda.')
    text = text.replace('nessun effetto Nautico.', 'configurazione locale del campo.')
    text = text.replace('nessuna azione esterna', 'nessuna azione aziendale')
    text = text.replace('non le fonti Nautico.', 'conservando le fonti del kernel ospitante.')
    text = text.replace('fonti o permessi Nautico.', 'fonti o permessi aziendali.')
    text = text.replace('Gli ambienti della demo: Progetto/Poppa, Cantiere, Fornitori, A bordo e Assistenza.', 'Gli ambienti della demo: ' + ', '.join(c['name'] for c in profile['contexts'].values()) + '.')
    text = text.replace('Dialogo locale della scheda · ', 'Dialogo della scheda · ')
    text = text.replace(' · nessun modello AI collegato', ' · domanda esplicita a MAIOS AI nel sito configurato')
    text = text.replace('Ogni scheda può aprire il proprio dialogo locale.', 'Ogni scheda può aprire un dialogo sul proprio contesto pubblico.')
    text = text.replace('La demo non chiama un LLM: conserva soltanto un’interazione locale attribuita.', 'Invia una domanda esplicita a MAIOS AI; conserva i contributi della scheda come proposte da trasferire.')
    text = replace_one(text, 'defaultHomeFeatured=state.homeFeatured;', "defaultHomeFeatured=cfg.profile.initialFeatured||state.homeFeatured;")
    text = replace_one(text, 'Array.isArray(raw.selected)?raw.selected:[]', 'Array.isArray(raw.selected)?raw.selected:(cfg.profile.initialActivities||[])')
    text = text.replace('(state.stageStep+1)%4', '(state.stageStep+1)%cfg.profile.phases.length')
    text = replace_one(text, 'capabilities:new Set(),drafts:', 'capabilities:new Set(cfg.profile.capabilities||[]),drafts:')
    text = replace_one(text, 'state.capabilities.clear();state.stageStep=0;', 'state.capabilities.clear();for(const capability of cfg.profile.capabilities||[])state.capabilities.add(capability);state.stageStep=0;')
    text = text.replace("'kux-intent-lab-preferences'", "'kux-public:' + cfg.profile.id + ':preferences'")
    text = text.replace("'kux:home-prepared-contexts:v1'", "'kux-public:' + cfg.profile.id + ':home-preparations:v1'")
    text = replace_one(text, "version:'lab-2026-10-11-r5.12',liveAI:false", "version:'public-griglia-v1',referenceLiveAI:false,assistantBinding:'maios-public-assistant'")
    anchor = '// Safe, read-only debug readback for the standalone demo (not an AI interface).'
    integration = '''window.KUXHostedGriglia.install({state,contexts,openPanel,activateScreen,switchWorkspaceContext,renderModule,renderSection,refreshModules,getFocused,updateHeader,getAssistant:()=>sharedAssistantSurface?{...sharedAssistantSurface.snapshot(),visible:!!sharedAssistantSurface.element.getClientRects().length,focused:sharedAssistantSurface.element.contains(document.activeElement)}:null});\n'''
    if visual_runtime:
        integration += 'window.KUXActivityVisuals.install({state});\n'
        text = replace_one(text, '</head>', '<style id="kux-activity-visuals">' + visual_css + '</style></head>')
    text = replace_one(text, anchor, integration + anchor)
    text = text.replace("provider:'none',authority:'local-demo-only'", "provider:'maios-public-assistant',authority:'public-presentation-only'")
    text = text.replace('Superficie composta K-UX-AI / Nautico sintetico. Non è un SK installato: nessuna AI, sincronizzazione tra kernel, autorizzazione o apprendimento autonomo viene esercitata.', 'Le schede usano le fonti del kernel presentato. I casi sono illustrativi; contributi e proposte restano locali finché vengono trasferiti al ricevente pertinente. Le domande inviate a MAIOS AI sono distinte da quelle bozze.')
    text = text.replace('Collegare le fonti effettive richiede un owner e un ricevente autorizzati.', 'Il lavoro in azienda collega documenti, persone e strumenti del suo contesto.')
    text = text.replace('Competenze e permessi effettivi di un SK: non risolti.', 'Le azioni aziendali appartengono all’ambiente che adotta il kernel.')
    text = text.replace("submit.textContent='Consegna al controller';", "submit.textContent='Conserva contributo';")
    text = text.replace("setStatus('Consegna al controller…');", "setStatus('Conservo il contributo…');")
    text = text.replace('Il modulo non invia automaticamente dati o email. L’host determina l’effetto.', 'Il contributo resta in questo spazio. La domanda si invia nella chat.')
    text = replace_one(text, '</head>', '<style>body[data-kux-product="k-ux-ai"] .kux-present-object{clip-path:none;border-radius:14px;width:55%;height:48%;background:linear-gradient(90deg,#c7ecec 36%,#fffaf0 36%);box-shadow:0 0 0 1px #527675} .kux-public-source a{color:inherit}.kux-ai-note{font-size:.82rem;line-height:1.45;color:#496667}.kux-source-diagram{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}.kux-source-diagram>span{padding:18px 10px;border:1px solid #a9c7bc;border-radius:10px;background:#edf4e8;text-align:center}.kux-ai-error{color:#7b4a21}</style></head>')
    if profile['id'] == 'kernel-nautico':
        # Hosting-domain presentation: leave the GPT reference and neutral receiver intact.
        text = replace_one(text, '</head>', '''<style id="kux-nautical-home-space">
body[data-kux-product="kernel-nautico"] .home-screen .home-intro .kux-home-story #homeTitle{font-size:clamp(28px,2.6vw,42px);line-height:1.08;margin:0 0 6px;letter-spacing:-.035em}
body[data-kux-product="kernel-nautico"] .kux-home-story .kux-home-thesis{font-size:clamp(17px,1.35vw,22px);line-height:1.25;margin:0 0 10px}
body[data-kux-product="kernel-nautico"] .home-screen .home-intro .kux-home-story .intro-desc,
body[data-kux-product="kernel-nautico"] .home-screen .home-intro .kux-home-story .kux-home-depth,
body[data-kux-product="kernel-nautico"] .home-screen .home-intro .kux-home-story .kux-home-next,
body[data-kux-product="kernel-nautico"] .home-screen .home-intro .kux-home-story .kux-home-demo-boundary{font-size:13px;line-height:1.35;margin:0 0 7px;max-width:none}
body[data-kux-product="kernel-nautico"] .home-screen .home-intro .kux-home-story p:last-child{margin-bottom:0}
body[data-kux-product="kernel-nautico"] .kux-home-setup{align-self:start}
@media(min-width:1051px){body[data-kux-product="kernel-nautico"] .home-intro{grid-template-columns:minmax(0,1.15fr) minmax(370px,.85fr)}}
@media(max-width:780px){body[data-kux-product="kernel-nautico"] .home-screen .home-intro .kux-home-story p[class]{font-size:14px;line-height:1.42}}
</style></head>''')
    if profile['id'] == 'k-ux-ai':
        # The neutral introduction uses its own language and leaves the domain derivative intact.
        text = replace_one(text, '</head>', """<style id="kux-neutral-home-space">
body[data-kux-product="k-ux-ai"] .home-screen .home-intro .kux-home-story #homeTitle{font-size:clamp(30px,2.8vw,44px);line-height:1.08;margin:0 0 6px;letter-spacing:-.035em}
body[data-kux-product="k-ux-ai"] .kux-home-story .kux-home-thesis{font-size:clamp(17px,1.4vw,23px);line-height:1.25;margin:0 0 10px}
body[data-kux-product="k-ux-ai"] .home-screen .home-intro .kux-home-story p[class]{font-size:15px!important;line-height:1.5!important;margin:0 0 6px;max-width:none}
body[data-kux-product="k-ux-ai"] .home-screen .home-intro .kux-home-story p:last-child{margin-bottom:0}
body[data-kux-product="k-ux-ai"] .kux-home-setup{align-self:start}
@media(min-width:1051px){body[data-kux-product="k-ux-ai"] .home-intro{grid-template-columns:minmax(0,1.15fr) minmax(370px,.85fr)}}
@media(max-width:780px){body[data-kux-product="k-ux-ai"] .home-screen .home-intro .kux-home-story p[class]{font-size:14px!important;line-height:1.42!important}}
</style></head>""")
    text = text.replace('Informazioni sul prototipo', 'Guida all’interfaccia')
    text = text.replace('STATO LOCALE · SORGENTI DEMO', 'SESSIONE LOCALE · CASO ILLUSTRATIVO')
    text = text.replace('CAPACITÀ NEL PROTOTIPO', 'COME USARE LA SCHEDA')
    text = text.replace('La correlazione è illustrativa: l’effetto resta nel controller del contesto.', 'Il caso è illustrativo; il contributo resta in questa sessione.')
    text = text.replace("guidedTourKind==='work'?'CANVAS':'HOME'", "guidedTourKind==='work'?'LAVORO IN CORSO':'PANORAMICA'")
    # User-facing names express what the person can do; source identifiers remain stable.
    text = text.replace('>Griglia<', '>Panoramica<')
    text = text.replace('Apri Griglia iniziale', 'Apri Panoramica')
    text = text.replace('Griglia iniziale', 'Panoramica')
    text = text.replace('Apri griglia iniziale', 'Apri panoramica')
    text = text.replace('Spostati fra Griglia e Campo', 'Spostati fra Panoramica e Lavoro in corso')
    text = text.replace('Torna alla griglia iniziale', 'Torna alla panoramica')
    text = text.replace('Apri Campo attivo', 'Apri Lavoro in corso')
    text = text.replace('Campo attivo', 'Lavoro in corso')
    text = text.replace('Entra nel campo', 'Apri il lavoro')
    text = text.replace('PREPARA IL CAMPO', 'PREPARA IL LAVORO')
    text = text.replace('Il tuo campo', 'Le attività preparate')
    text = text.replace('IL TUO CAMPO', 'ATTIVITÀ PREPARATE')
    text = text.replace('attività pronte per il canvas', 'attività pronte per il lavoro')
    text = text.replace('per il canvas', 'per il lavoro')
    text = text.replace('dalla griglia', 'dalla panoramica')
    text = text.replace('Campo preparato · ', 'Lavoro preparato · ')
    text = text.replace('Griglia illustrativa · ', 'Spazio di lavoro illustrativo · ')
    text = text.replace('Simula nuova capacità', 'Apri confronto')
    text = text.replace('Avvia il tour del Canvas', 'Avvia il tour del lavoro in corso')
    text = text.replace('Campo operativo', 'Spazio di lavoro')
    text = text.replace('FIELD / 01', 'SPAZIO DI LAVORO')
    text = text.replace('Il campo è pronto.', 'Lo spazio di lavoro è pronto.')
    text = text.replace('cambia l’intero campo e gli avatar', 'cambia argomento e attività')
    text = text.replace('cambia il canvas e gli avatar, senza cambiare la fonte di una scheda', 'cambia argomento e attività conservando le fonti delle schede')
    text = text.replace('Strumento di prova: struttura e funzioni potranno cambiare con il kernel ricevente.', 'Descrivi il tuo riscontro e conserva il contributo insieme al suo contesto.')
    text = text.replace('Nessun effetto confermato dal controller. La bozza resta disponibile.', 'Il contributo non è stato conservato. La bozza resta disponibile.')
    text = text.replace('trasferiti al ricevente pertinente', 'trasferiti al kernel che continua il lavoro')
    text = text.replace('Apri il modulo sperimentale a fianco della chat, se lo spazio lo consente', 'Apri il modulo per preparare un contributo')
    text = text.replace('Riparti dalla Griglia', 'Riparti dalla panoramica')
    text = text.replace('Torna al campo', 'Torna al lavoro')
    text = replace_one(text, '<html lang="it">', '<html lang="' + locale + '">')
    catalog_path = ROOT / 'src/ui/locales/public-workspace.json'
    if locale == 'en':
        localized = subprocess.run(['node', str(ROOT / 'tools/localize_public_griglia.mjs'),
                                    str(catalog_path)], input=text, capture_output=True,
                                   text=True, encoding='utf-8', check=True)
        text = localized.stdout
    locale_link = ('it/' if locale == 'en' else '../')
    locale_label = ('Italiano' if locale == 'en' else 'English')
    text = replace_one(text, '<body data-skin="atlas" data-start="home"',
                       '<body data-ui-locale="' + locale + '" data-skin="atlas" data-start="home"')
    # The native artifact has a relative alternative. A recognised same-origin
    # product page follows its companion so page and frame keep the same locale.
    language_control = '<a class="kux-locale-link" href="' + locale_link + '" hreflang="' + ('it' if locale == 'en' else 'en') + '" lang="' + ('it' if locale == 'en' else 'en') + '">' + locale_label + '</a>'
    text = replace_one(text, '<button class="toolbar-icon" id="btnHelp"', language_control + '<button class="toolbar-icon" id="btnHelp"')
    companion_page = ('/k-ux-ai-it.html' if locale == 'en' else '/k-ux-ai.html') if profile['id'] == 'k-ux-ai' else ('/kernel-nautico.html' if locale == 'en' else '/kernel-nautico-en.html')
    text = replace_one(text, '</body>', '<script>document.querySelector(".kux-locale-link").addEventListener("click",event=>{if(parent===window)return;try{if(parent.location.origin===location.origin&&' + script_data([profile['pagePath'], companion_page]) + '.includes(parent.location.pathname)){event.preventDefault();parent.location.href=' + script_data(companion_page + '#kernel-guide') + ';}}catch{}});</script></body>')
    output.mkdir(parents=True, exist_ok=True)
    for image, source_path in visual_assets.items():
        destination = output / image
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source_path.resolve() != destination.resolve():
            shutil.copyfile(source_path, destination)
    (output / 'index.html').write_text(text, encoding='utf-8', newline='\n')
    manifest = {'schema': 'kux.public-griglia-build.v1', 'profile_id': profile['id'], 'semantic_owner': profile['semanticOwner'], 'reference_sha256': REFERENCE_SHA256, 'profile_sha256': hashlib.sha256(profile_bytes).hexdigest(), 'runtime_sha256': hashlib.sha256(runtime.encode()).hexdigest(), 'html_sha256': hashlib.sha256(text.encode()).hexdigest(), 'means': {'ui': 'GPT Griglia v5.12 derived public incarnation', 'dialogs': 'explicit MAIOS public assistant requests when host configured', 'company_integrations': False}}
    manifest.update(locale=locale, default_locale='en', supported_locales=['en', 'it'],
                    locale_catalog_sha256=hashlib.sha256(catalog_path.read_bytes()).hexdigest(),
                    tour_catalog_sha256=hashlib.sha256((ROOT / 'src/ui/locales/public-tours.json').read_bytes()).hexdigest())
    if visual_runtime:
        manifest['activity_visuals'] = {
            'runtime_sha256': hashlib.sha256(visual_runtime.encode()).hexdigest(),
            'css_sha256': hashlib.sha256(visual_css.encode()).hexdigest(),
            'assets': {path: hashlib.sha256(source.read_bytes()).hexdigest() for path, source in visual_assets.items()}}
    (output / 'BUILD.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--locale', choices=('en', 'it'), default='en')
    args = parser.parse_args()
    print(json.dumps(build(args.profile, args.output, args.locale), ensure_ascii=False))
