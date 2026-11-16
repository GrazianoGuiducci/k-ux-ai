# MetaCanvas — convergenza tra editor di pagina e studio di diagrammi
Data: 16 novembre 2026 · Stato: **metodo candidato esercitato in prototipo locale, non versione integrata/distribuita**.

## Fonte e oggetti distinti
L'operatore seleziona l'evoluzione dell'editor di pagine MAIOS usato con Codex mediante composizione con MetaCanvas Studio 20/21. Vuole poter modificare il testo al volo, duplicare qualunque elemento utile, spostare la copia dove serve, aggiungere diagrammi e immagini anche **nel paragrafo o in alto a destra**, e ridurre i passaggi necessari senza irrigidire il layout. La competenza deve imparare dall'esercizio e rendere il metodo riusabile.

- **Fonte pagina:** file HTML privato di conversazione `MAIOS_Consulenza_MetaCanvas_IT_R2(1).html`, con il proprio editor DOM (4 sezioni, ricerca, modifica testi, inserimento, spostamento, colori, dimensioni, pannello mobile, recovery, anteprima, export). Contenuti e copia della pagina appartengono al progetto MAIOS.it, non vanno trasferiti nel prodotto generico.
- **Fonte studio:** K-UX-AI / Collaborative Communication Medium, MetaCanvas Studio 20 e Studio 21 IT/EN; scene/nodi/frecce, Undo, Presenta, templates, round-trip AI selettivo e copia pubblica sono capacità verificate nei rispettivi artefatti. Il modello `ccm.document.v1` non coincide con il DOM di una pagina web.
- **Owner:** K-UX-AI/CCM conserva la logica generale del medium ed eventualmente il suo codice comune; D-ND Design conserva la relazione di disposizione e riduzione del carico percettivo; maios_it conserva contenuto/stile del sito; Codex è un ricevente possibile, non automaticamente attivato. KA/FDLA/Meta_Skill partecipano al metodo, non sostituiscono gli owner.

## Primo esercizio realmente prodotto
In ChatGPT è stato generato un **prototipo HTML R3 locale** derivato dall'allegato, non caricato nella repository e non distribuito sul sito. Mantiene la pagina e l'editor preesistenti. Aggiunge:
1. `Diagramma` con modello locale versionato in `data-mc-model`, rendering SVG, template processo/triangolo/confronto/vuoto, nodi aggiungibili/duplicabili/editabili/trascinabili, collegamenti e forme; dati e rendering restano nello stesso HTML.
2. `Immagine` con slot contestuale, alt text, prompt costruibile/copiabile per ChatGPT/Codex, upload PNG/JPEG/WebP con limite di 2 MB incorporato come data URL. **Nessuna chiamata automatica a un modello o generazione immagine nel browser**.
3. Posizioni dentro o all'inizio del paragrafo, in alto a sinistra/destra, flusso, centro e piena larghezza; layout responsive e griglie 1/2/3 colonne per blocchi aggiunti.
4. `Duplica nel punto…`: scelta della sorgente e clic sull'elemento destinatario, un solo checkpoint Undo. Duplica e rimappa gli ID HTML/ARIA locali per evitare collisioni; le relazioni SVG restano nel modello del singolo diagramma.
5. Riutilizzo dello **storico unico** e dell'export/recovery della pagina, senza introdurre un secondo controller del documento.

## Evidenza e apprendimento del metodo
Prove eseguite con Node `--check` dei due script e Chromium headless sul documento montato in contenuto HTML:
- inserimento diagramma, +nodo (3→4), testo del nodo, duplica, Undo della copia, immagine/prompt, preview ed export senza pageerror nel percorso osservato;
- inserimento nel paragrafo, Undo/Redo, `Duplica nel punto…` tra sezioni, griglia 2 colonne, upload PNG, esportazione, riapertura e recupero dei due diagrammi e dell'immagine incorporata;
- viewport 390 px: larghezza documento 390, nessun overflow iniziale rilevato.
Una prima verifica ha individuato un **errore di integrazione**, non del diagramma: l'intercettore dei click dell'editor originario bloccava i pulsanti del nuovo dialog fuori dal suo subtree. Estendere l'eccezione a `#mc-visual-dialog` ha restituito l'azione. Una seconda verifica ha trovato che un nuovo controllo era stato definito nello script senza inserire il relativo elemento DOM: il bootstrap si arrestava con `Cannot set properties of null`. È stata riparata la composizione del carrier ed è stato riesercitato il flusso. **Le correzioni sono conoscenza della competenza di costruzione**, non solo bugfix.

### Saper fare riusabile
Il problema non è sommare le toolbar. Per la pagina reale, **l'ancora è il punto della frase o del blocco nel quale l'operatore vuole trasformare la comunicazione**. L'inserimento di un oggetto rende immediatamente possibile la sua modifica; il duplicato può essere indirizzato con un gesto verso un referente visibile; la geometria non deve sostituire identità e testo; il modello dei diagrammi resta distinto dal DOM nel quale si incarna. La progressiva esposizione dei comandi riduce il costo del passaggio `comprendo la pagina → intervengo nel punto → guardo l'effetto → salvo`.

### Limite e seguito
Il prototipo R3 **non** importa la totalità del motore Studio 20/21 (template, presentazione a schede, confronto selettivo AI, formato `ccm.document.v1`) dentro l'editor di pagina. È un primo **ponte operativo**; una fusione canonica richiede una regola di proiezione fra documento a scene e pagina HTML, gestione delle classi/strutture native, privacy del copy/export, test file:// Windows, tastiera/touch/accessibilità, e verifica in Codex dell'HTML risultante. La copia esportata è un artefatto di lavoro, non un deployment del sito.

La prossima iterazione dovrebbe usare un documento neutro e uno reale, selezionando quali funzioni del canvas continuano come strumenti context-aware e quali restano specifiche delle presentazioni. In particolare, studiare riuso dei template e vero editor di layout a griglia senza danneggiare i CSS esistenti; preservare conversioni e roundtrip espliciti anziché mescolare due stati canonici incompatibili. La sorgente del prototipo è disponibile solo come artefatto di conversazione `MAIOS_Consulenza_MetaCanvas_R3_Prototipo_IT.html`, da trasferire con consenso/mezzo di Codex, non tramite questo documento.
