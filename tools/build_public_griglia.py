"""Compose a public hosting-kernel profile with the unchanged GPT Griglia engine."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
import re

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


def build(profile_path: Path, output: Path) -> dict:
    source = REFERENCE.read_bytes()
    if hashlib.sha256(source).hexdigest() != REFERENCE_SHA256:
        raise ValueError('The selected GPT reference changed; assimilate it before rebuilding.')
    profile_bytes = profile_path.read_bytes()
    profile = json.loads(profile_bytes)
    if profile.get('schema') != 'kux.hosting-kernel-profile.v1':
        raise ValueError('Unknown hosting-kernel profile')
    if set(profile['contexts']) != {'poppa', 'cantiere', 'fornitori', 'bordo', 'assistenza'}:
        raise ValueError('This GPT incarnation requires its five context carriers')
    for context in profile['contexts'].values():
        for field in ['name', 'subtitle', 'goal', 'source', 'items', 'unknown', 'next']:
            if field not in context:
                raise ValueError(f'Missing carrier field: {field}')
    runtime = (ROOT / 'src/ui/public-griglia.js').read_text(encoding='utf-8')
    text = source.decode('utf-8')
    prelude = '<script>window.__UXAI_CONFIG__=' + script_data({'skin': 'atlas', 'start': 'home', 'profile': profile}) + ';\n' + runtime + '\n</script>'
    text = replace_one(text, "window.__UXAI_CONFIG__ = {skin:'atlas',start:'home'};", "// Hosting-kernel configuration is provided by the public source profile.")
    text = replace_one(text, '<body data-skin="atlas" data-start="home">', '<body data-skin="atlas" data-start="home" data-kux-product="' + html.escape(profile['id'], quote=True) + '">' + prelude)
    text = replace_pattern(text, r'const contexts=\{.*?\n\};?\s*const scenarios=', 'const contexts=' + script_data(profile['contexts']) + ';\nconst scenarios=')
    text = replace_pattern(text, r'const scenarios=\[.*?\n\];', 'const scenarios=' + script_data(profile['events']) + ';')
    story = profile['home']
    intro = '<div class="kux-home-story"><div class="eyebrow">' + html.escape(story['eyebrow']) + '</div><h1 id="homeTitle">' + html.escape(story['title']) + '</h1><h2 class="kux-home-thesis">' + html.escape(story['subtitle']) + '</h2>'
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
    text = replace_one(text, anchor, integration + anchor)
    text = text.replace("provider:'none',authority:'local-demo-only'", "provider:'maios-public-assistant',authority:'public-presentation-only'")
    text = text.replace('Superficie composta K-UX-AI / Nautico sintetico. Non è un SK installato: nessuna AI, sincronizzazione tra kernel, autorizzazione o apprendimento autonomo viene esercitata.', 'Le schede usano le fonti del kernel presentato. I casi sono illustrativi; contributi e proposte restano locali finché vengono trasferiti al ricevente pertinente. Le domande inviate a MAIOS AI sono distinte da quelle bozze.')
    text = text.replace('Collegare le fonti effettive richiede un owner e un ricevente autorizzati.', 'Il lavoro in azienda collega documenti, persone e strumenti del suo contesto.')
    text = text.replace('Competenze e permessi effettivi di un SK: non risolti.', 'Le azioni aziendali appartengono all’ambiente che adotta il kernel.')
    text = text.replace("submit.textContent='Consegna al controller';", "submit.textContent='Conserva contributo';")
    text = text.replace("setStatus('Consegna al controller…');", "setStatus('Conservo il contributo…');")
    text = text.replace('Il modulo non invia automaticamente dati o email. L’host determina l’effetto.', 'Il contributo resta in questo spazio. La domanda si invia nella chat.')
    text = replace_one(text, '</head>', '<style>body[data-kux-product="k-ux-ai"] .kux-present-object{clip-path:none;border-radius:14px;width:55%;height:48%;background:linear-gradient(90deg,#c7ecec 36%,#fffaf0 36%);box-shadow:0 0 0 1px #527675} .kux-public-source a{color:inherit}.kux-ai-note{font-size:.82rem;line-height:1.45;color:#496667}.kux-source-diagram{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}.kux-source-diagram>span{padding:18px 10px;border:1px solid #a9c7bc;border-radius:10px;background:#edf4e8;text-align:center}.kux-ai-error{color:#7b4a21}</style></head>')
    output.mkdir(parents=True, exist_ok=True)
    (output / 'index.html').write_text(text, encoding='utf-8', newline='\n')
    manifest = {'schema': 'kux.public-griglia-build.v1', 'profile_id': profile['id'], 'semantic_owner': profile['semanticOwner'], 'reference_sha256': REFERENCE_SHA256, 'profile_sha256': hashlib.sha256(profile_bytes).hexdigest(), 'runtime_sha256': hashlib.sha256(runtime.encode()).hexdigest(), 'html_sha256': hashlib.sha256(text.encode()).hexdigest(), 'means': {'ui': 'GPT Griglia v5.12 derived public incarnation', 'dialogs': 'explicit MAIOS public assistant requests when host configured', 'company_integrations': False}}
    (output / 'BUILD.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.profile, args.output), ensure_ascii=False))
