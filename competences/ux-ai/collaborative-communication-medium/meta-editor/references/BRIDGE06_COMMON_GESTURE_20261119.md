# Bridge 06 — un gesto comune senza fondere i documenti
Data: 19 novembre 2026 · Owner: K-UX-AI / CCM / MetaEditor Evolution
Stato: due prototipi HTML **sperimentali**, costruiti in conversazione e provati in Chromium. Non distribuiti in K-UX-AI come nuove edizioni del prodotto, né in MAIOS.it.

## Perché esiste
Dopo la riconciliazione fra [MetaCanvas pubblico e bozza Codex](SOURCE_FIELD_PUBLIC_TOOL_CODEX_DRAFTS_20261119.md), l'operatore seleziona di proseguire. La scelta non è una R6 che importa tre motori in uno: è il primo *gesto comune* esercitato su **due sorgenti reali** che conservano differenti modelli, UI e contratti.

| Carrier | Sorgente esatta | Prova del gesto |
|---|---|---|
| Bozza Codex Consulenza AI | `MAIOS_Consulenza_AI_revisionata(1).html`, SHA256 `f227b61b0a813ad7312f805dcec63def03b87201d5d5fb6ae0ae729d2541f190`, 419.563 B, caricata in conversazione | Doppio clic H1 → `contenteditable` e toolbar rich text visibile **senza apertura forzata del grande inspector**; pannello riapribile su scelta |
| Studio21 Consulenza IT (K-UX-AI) | `examples/collaborative-communication-medium/MetaCanvas_Studio21_Consulenza_IT.html`, SHA256 `abbdbd9e749453434fddb140505c0586ce594990739742c8106f37ab542165df`, 293.797 B | Secondo clic sulla **scritta di un nodo** → editor testuale in situ, mentre clic sul resto del nodo conserva mini editor avanzato |

## Intervento tecnico riproducibile
La patch di ciascuna sorgente è delimitata a un solo gestore:
- Nel `main.addEventListener('dblclick')` della bozza Codex, quando il referente è un campo di testo e non siamo nel toggle `editing` globale, nascondere `#local-tools` senza chiamare `setTools(false)` (che chiuderebbe il direct edit), mantenere `picked` e `#local-mini`. Non toccare `Range`, `selectionchange`, `execCommand`, cronologia o exporter dell'owner.
- Nel `clickNode()` di Studio21, il secondo clic su testo invoca `startDirectEdit(n.id)` e non `laterQuick('node',n.id)`. L'evento `pointerup` è *retargeted al wrapper* per pointer capture; `e.target.closest('.node-text')` da solo falliva silenziosamente. Si usa `document.elementFromPoint(e.clientX,e.clientY)?.closest('.node-text')` per ricostruire il bersaglio visivo, senza interrompere il gesto. L'inspector continua per i clic sul bordo e per gli altri percorsi.

Il tool `bridge06_build.py` nella directory di laboratorio accetta i due file originali, valida entrambi gli SHA e produce copie di lavoro: non modifica i sorgenti né copia il contenuto della bozza Codex nel repository.

## Prove osservate
Node 22 `--check` su entrambi gli script inline dell'HTML Codex e sui due script eseguibili Studio21.

Chromium headless `page.set_content`: doppio clic H1 → mini attiva, inspector chiuso; selezione di 9 caratteri di un titolo → corsivo applicato → esportazione HTML con `<i>` e quattro sezioni originali ancora presenti; doppio clic nodo `d1-a` → editing `contenteditable`, cambio `Contesto` in `Contesto condiviso` → salvataggio HTML → nuova apertura recupera testo. Sette ID di scena, link, note e `savedTemplates` conservati senza alterazioni; `ccm.document.v1` rimane invariato. Nel **test privato sintetico**, Copia pubblica ha rimosso nota riservata, nodo marcato `private:true` e template personali; gli output HTML dati dal test non sono una copia del sorgente produttivo. Zero `pageerror` nei flussi. A viewport 390 px entrambe le UI restano senza overflow globale e la mini del testo Codex è visibile.

**Regressione nella formazione del test:** la prima versione su Studio21 passava sintassi e selezionava il nodo ma NON entrava nel testo. L'ispezione degli eventi ha mostrato `pointerdown` su `.node-text` e `pointerup` sul contenitore per pointer capture. L'uso del bersaglio sotto puntatore ha corretto la prova: non basta avere una funzione editor già disponibile. Nel test Codex, applicare il comando Bold ad H1 già bold lo *disattivava* (corretto per l'editor): il test è stato riformulato usando Italic. Non riscrivere quei test come successi precedenti.

## Distinzioni ancora vive
- Il testo Codex è HTML rich text con focus e caret: il testo di un nodo Studio21 è una **stringa nel modello**. Non affermare che lo Studio supporti markup rich-text nel nodo; questa funzione richiederebbe evoluzione di schema e prova.
- Il corpo pagina responsive e la scena 16:9 restano due adapter/documenti; non sostituire `ccm.document.v1` con il DOM pagina e non serializzare gli strumenti due volte.
- Codex HTML esportato porta con sé il suo editor, mentre lo Studio21 mantiene lavoro e copia pubblica separati; non applicare la bozza Codex al sito live senza confronto con l'owner.
- Apertura `file://` in Chrome Windows dell'operatore, touch, accessibilità completa, import universale e recezione di terzi **non attestati**. Il test Chromium non autorizza release, deploy o intervento nel checkout di Codex.

## Prossima azione discriminante
Progettare un piccolo **contratto di comando** (`referente`, `setText`, `commit`, `cancel`, `undo`) che chiama le operazioni native degli adapter, con roundtrip caret/markup Codex e ID/link/privacy Studio21. Prima di migrare rich-text in uno schema dei diagrammi, verificare un documento di prova che contenga **formattazione mista** e selezioni ricche: la stessa parola non implica lo stesso tipo di valore. Qualità dell'interazione e mantenimento del significato precedono il numero di pulsanti.

Le capacità acquisite sono esercitate nei prototipi ed entrano ora nella competenza; non sono automaticamente esercitate nel prodotto pubblico.
