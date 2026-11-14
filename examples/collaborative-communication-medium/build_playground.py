"""Compose the bilingual removable guide using the existing Studio 21 editor."""

import argparse
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
BASE_BUDGET_BYTES = 500_000
SOURCE = "MetaCanvas_Studio21_Consulenza_{}.html"
OUTPUT = "MetaCanvas_Guida_Playground_{}.html"
COPY = {
    "IT": {
        "title": "MetaCanvas · Guida e playground",
        "intro": "Questa guida è modificabile. Inizia dalla scheda aperta o esplora liberamente.",
        "show": "Vai alla guida", "hint": "Mostra dove", "remove": "Rimuovi guida",
        "removed": "Guida rimossa. Puoi recuperarla con Annulla.",
        "confirm": "Rimuovere tutte le schede della guida? Le altre schede restano. Puoi usare Annulla.",
        "blank": "Canvas vuoto", "addBlank": "Aggiungi scheda vuota",
        "showEditor": "Passa a Componi per provare sul canvas.",
        "missing": "L’elemento è assente. Puoi continuare sulla scheda o annullare l’ultima modifica.",
        "example": "Prova un ritorno simulato", "proposal": "Esempio didattico · proposta",
        "addition": "Scegli casi comparabili", "relation": "prepara",
        "alreadyApplied": "La proposta è già nella scheda. Usa Annulla per riprovare.",
        "lessons": [
            ("edit", "Modifica questa guida", "Fai doppio clic sul riquadro evidenziato per riscriverlo. Con la tastiera selezionalo e premi Invio.", "Una richiesta da chiarire", "Decidere cosa provare"),
            ("move", "Sposta e annulla", "Sposta il primo riquadro: la freccia lo segue. Puoi anche selezionarlo e usare i tasti freccia. Usa Annulla per tornare indietro.", "Una prova su casi chiusi", "Una decisione da prendere"),
            ("share", "Passa una scheda e riprendi", "Apri Dati per AI e scegli Solo scheda corrente. Prova poi il ritorno simulato: confronta la proposta e scegli se integrarla.", "Richiesta di preventivo", "Prova su casi già chiusi"),
            ("save", "Salva e continua da qui", "Scarica il tuo HTML con Salva lavoro e riaprilo nel browser. Puoi rimuovere tutte le schede guida e continuare con il tuo documento.", "La tua revisione", "La prossima modifica"),
        ],
    },
    "EN": {
        "title": "MetaCanvas · Guide and playground",
        "intro": "This guide is editable. Start with the open slide or explore at your own pace.",
        "show": "Go to guide", "hint": "Show me where", "remove": "Remove guide",
        "removed": "Guide removed. Use Undo to restore it.",
        "confirm": "Remove all guide slides? Other slides are kept. You can undo this action.",
        "blank": "Blank canvas", "addBlank": "Add blank slide",
        "showEditor": "Switch to Compose to try this on the canvas.",
        "missing": "The element is missing. Keep working on the slide or undo your last edit.",
        "example": "Try a simulated return", "proposal": "Practice example · proposal",
        "addition": "Choose comparable cases", "relation": "prepares",
        "alreadyApplied": "The proposal is already in the slide. Use Undo to try again.",
        "lessons": [
            ("edit", "Edit this guide", "Double-click the highlighted card to rewrite it. With the keyboard, select it and press Enter.", "A request to clarify", "Decide what to try"),
            ("move", "Move and undo", "Move the first card and watch the arrow follow it. You can also select it and use the arrow keys. Use Undo to go back.", "A trial with closed cases", "A decision to make"),
            ("share", "Share one slide and resume", "Open Data for AI and choose Current slide only. Then try the simulated return, review the proposal and decide whether to integrate it.", "A quote request", "A trial with closed cases"),
            ("save", "Save and pick up here", "Use Save work to download your HTML and reopen it in a browser. You can remove the guide slides and keep working on your own document.", "Your revision", "Your next edit"),
        ],
    },
}


def json_script(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")


def scene_for(lesson, relation):
    cue, title, instructions, first, second = lesson
    return {
        "id": f"playground-{cue}", "title": title, "guideCue": cue,
        "notes": "", "background": "#fffdf5",
        "elements": [
            {"id": "title", "type": "text", "x": 65, "y": 55, "w": 1070, "h": 96,
             "fontSize": 44, "color": "#183146", "text": title},
            {"id": "instructions", "type": "text", "x": 65, "y": 165, "w": 1070, "h": 140,
             "fontSize": 32, "color": "#183146", "text": instructions},
            {"id": "practice", "type": "card", "x": 65, "y": 344, "w": 320, "h": 142,
             "fontSize": 30, "fill": "#e7f5f0", "color": "#183146", "text": first},
            {"id": "outcome", "type": "card", "x": 815, "y": 344, "w": 320, "h": 142,
             "fontSize": 30, "fill": "#edf1f9", "color": "#183146", "text": second},
        ],
        "links": [{"id": "relationship", "from": "practice", "to": "outcome",
                   "fromAnchor": "right", "toAnchor": "left", "label": relation,
                   "width": 3, "color": "#087b70", "arrow": True, "heads": "end"}],
    }


def replace_once(html, pattern, value):
    html, count = re.subn(pattern, lambda _: value, html, count=1)
    if count != 1:
        raise ValueError(f"Studio 21 marker missing: {pattern}")
    return html


def build(locale):
    copy = COPY[locale]
    html = (ROOT / SOURCE.format(locale)).read_text(encoding="utf-8")
    html = replace_once(html, r"<title>[^<]+</title>", f'<title>{copy["title"]}</title>')
    marker = r'(<script id="ccm-data" type="application/json">)([^\n]*)(</script>)'
    state = json.loads(re.search(marker, html)[2])
    scenes = [scene_for(lesson, copy["relation"]) for lesson in copy["lessons"]]
    state.update(id="metacanvas-playground", title=copy["title"],
                 scenes=scenes, activeSceneId=scenes[0]["id"])
    state["ui"].pop("viewMode", None)
    html = replace_once(html, marker, '<script id="ccm-data" type="application/json">'
                        + json_script(state) + '</script>')
    html = replace_once(html, r'<script id="ccm-consulting-demo"[^>]*>[^\n]*</script>\n', "")
    html = replace_once(html, r'<section class="public-first-use" id="publicFirstUse".*?</section>',
                        f'''<section class="public-first-use" id="publicFirstUse" aria-label="{copy["title"]}" hidden>
<p style="margin:0">{copy["intro"]}</p>
<div class="public-first-actions" style="flex-wrap:wrap">
<button id="guideHint" type="button">{copy["hint"]}</button>
<button id="guideExample" type="button" hidden>{copy["example"]}</button>
<button id="guideRemove" type="button">{copy["remove"]}</button>
</div></section>''')
    for button in ("demoRail", "demoTools"):
        html = replace_once(html, rf'<button type="button" id="{button}"[^>]*>[^<]*</button>',
                            f'<button type="button" id="{button}">{copy["show"]}</button>')
    for button in ("blankRail", "blankTools"):
        html = replace_once(html, rf'<button type="button" id="{button}"[^>]*>[^<]*</button>',
                            f'<button type="button" id="{button}">{copy["addBlank"]}</button>')
    html = replace_once(html,
                        r'// Studio 21: canonical demo[^\n]*\n[\s\S]*?(?=\$\(\x27#addSlide\x27\))',
                        (ROOT / "playground-interaction.js").read_text(encoding="utf-8")
                        .replace("/* PLAYGROUND_COPY */ null", json_script({
                            key: value for key, value in copy.items() if key != "lessons"
                        })) + "\n")
    html = replace_once(html,
                        r"\(function\(\)\{\n const box=document.getElementById\('publicFirstUse'\);[\s\S]*?\}\)\(\);", "")
    html = html.replace("updateHistory();updateView();syncEditBar();scheduleFlatFit();",
                        "updateHistory();updateView();syncEditBar();renderPlayground();scheduleFlatFit();", 1)
    html = html.replace("copy.id=uid('sc');", "copy.id=uid('sc');delete copy.guideCue;", 1)
    html = html.replace("sc.id=uid('sc');sc.notes='';",
                        "sc.id=uid('sc');sc.notes='';delete sc.guideCue;", 1)
    html = html.replace("doc.querySelector('#ccm-data').textContent=safeData(copyData);",
                        """doc.querySelector('#ccm-data').textContent=safeData(copyData);
 doc.querySelector('#publicFirstUse').hidden=true;
 doc.querySelector('[data-guide-highlight]')?.removeAttribute('data-guide-highlight');""", 1)
    html = replace_once(html, r"</style>\n</head>", """[data-guide-highlight]{outline:3px solid #087b70;outline-offset:4px}
@media(forced-colors:active){[data-guide-highlight]{outline-color:Highlight}}
</style>
</head>""")
    if len(html.encode("utf-8")) > BASE_BUDGET_BYTES:
        raise ValueError(f"{locale} playground exceeds {BASE_BUDGET_BYTES:,} bytes")
    return html


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    for locale in COPY:
        content = build(locale).encode("utf-8")
        target = args.output / OUTPUT.format(locale)
        target.write_bytes(content)
        print(f"{target} · {len(content):,} bytes")


if __name__ == "__main__":
    main()
