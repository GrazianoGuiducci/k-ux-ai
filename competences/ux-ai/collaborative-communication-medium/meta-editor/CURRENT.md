# MetaEditor Evolution — CURRENT

updated: 2026-11-20
status: bridge08_1_codex_selection_state_fixed_and_browser_exercised; no_site_deploy

## 20 novembre — Bridge08.1: evidenza umana della doppia selezione, correzione puntuale

L'operatore ha provato il vero `MetaEditor_Bridge08_Bozza_Codex_IT.html` in Chrome Windows e ha documentato con screenshot un titolo selezionato strutturalmente mentre è in modifica il testo di un altro riquadro. La [competenza ha isolato e corretto la mancata sincronizzazione](references/BRIDGE08_1_SELECTION_HANDOFF_20261120.md): il ramo diretto di `dblclick` nascondeva Struttura senza `syncTools(section)`. Bridge08.1 sincronizza il referente corrente, rimuove i contorni passati e conserva il cursore del campo rich text; la barra inferiore rende percepibile quale testo è attivo.

**Stato effetti:** `MetaEditor_Bridge08_1_Selezione_Coerente_IT.html` è un file di prova nella conversazione, ricostruibile con lo [script K-UX-AI SHA-guarded](../../../../examples/collaborative-communication-medium/meta-editor-lab/bridge08_1_selection_fix.py). Test Node e Chromium: prima/dopo, riapertura Struttura, nuovo referente, Esc, setText/commit, Undo/Redo, export/reopen con una sola UI e mobile 390 px. Nessuna modifica al prodotto pubblico, a MAIOS.it o al checkout Codex. **La prova Chrome Windows dell'esito corretto resta da fare**, distinta dalla prova umana del problema.

**Direzione aperta:** proseguire con inserimento e composizione degli elementi a livello pagina, preservando selezione e proprietà della scena. Non introdurre un nuovo pannello per compensare il passaggio di stato.


updated: 2026-11-19
status: bridge08_ux_layer_committed_two_adapters_browser_tested; no_public_release

## 19 novembre — Bridge08 rende raggiungibili capacità esistenti

L'operatore ha scelto di affinare le funzioni e l'intuitività, dopo il contratto di comando Bridge07. [Bridge08 / apprendimento owner-native](references/BRIDGE08_UX_ACTIONS_FOCUS_20261119.md) e i file `bridge08_ui.js`, `bridge08_ui.css`, `bridge08_build.py` nel laboratorio K-UX-AI sono stati committati. Due HTML sperimentali scaricabili in conversazione riusano i portatori esatti Bridge07 (Codex rich text e Studio21 `ccm.document.v1`), senza sostituire Studio pubblico, MAIOS.it o il checkout Codex.

**Verificato in Node/Chromium:** ricerca azioni e navigazione con Ctrl+Maiusc+P, F2 nativo, focus e formattazione progressiva, navigazione fra sezioni/schede e inserimento testo Studio, export e riapertura con una sola interfaccia, Studio public copy priva di elementi/script/style UX08, mobile 390px senza overflow orizzontale nel test e nessun pageerror nei percorsi. Il canvas Focus Studio nel test 1360 px cresce da circa 1019 a 1150 px. La prima doppia UI serializzata e la griglia Focus sbagliata sono state corrette; il metodo è in GUIDE.

**Resta aperto:** prova manuale file:// su Windows, accessibilità/touch, confronto sui gesti dopo uso reale, adattatore di regioni HTML su un secondo sito, e messa a regime nel prodotto pubblico. Il prossimo lavoro non è scelto da CURRENT; la competenza è disponibile quando serve.


updated: 2026-11-19
status: bridge07_native_shared_commands_exercised; builder_committed; public_product_unchanged

## 19 novembre — Bridge07: contratto di editing condiviso, esecuzione nativa

I due HTML `MetaEditor_Bridge07_Bozza_Codex_IT.html` e `MetaEditor_Bridge07_Studio21_IT.html` sono artefatti **di conversazione** derivati dagli HTML Bridge06 già verificati, non nuovi file canonici distribuiti in MAIOS.it. Il [builder](../../../../examples/collaborative-communication-medium/meta-editor-lab/bridge07_build.py) è in K-UX-AI con readback identico. [Contratto/esperienza/prove](references/BRIDGE07_NATIVE_COMMAND_CONTRACT_20261119.md) distingue rich text del Codex editor dalla label stringa Studio21; in entrambi F2/Ctrl+Invio/Esc e Undo/Redo agiscono via metodi nativi.

**Risultati tecnici osservati:** testo parziale con markup esterno preservato; Esc recupera `innerHTML` e history originali; Ctrl+Z/Y funzionano dopo che Undo riporta il caret in `contenteditable`; scena Studio21 resta `ccm.document.v1` con sette scene e public copy che filtra note, nodi privati e template sintetici; export/riapertura dei due HTML conserva il Bridge07; mobile 390px senza overflow globale nel campione. I difetti di sessione stale dopo blur e redo perso col focus sono tornati alla GUIDE e al builder.

**Limiti:** non prova Chrome Windows file://, accessibilità completa, siti HTML arbitrari, editing rich text nelle label Studio o sostituzione di MetaCanvas Studio20/21 pubblico. Nessun deploy, nessuna modifica al checkout di Codex o alla pagina MAIOS. Prossimo discrimine: esperienza reale dell'operatore sul gesto e region adapter con patch selettiva su due pagine.


updated: 2026-11-19
status: bridge06_two_source_gesture_tested_in_Chromium; source_bound_builder_committed; no_public_release

## 19 novembre — primo ponte reale Codex / Studio21, senza unificazione dei modelli

I due esperimenti HTML `MetaEditor_Bridge06_Bozza_Codex_IT.html` e `MetaEditor_Bridge06_Studio21_Consulenza_IT.html` sono stati costruiti in conversazione (file scaricabili), non installati nel sito. Il [builder owner-native](../../../../examples/collaborative-communication-medium/meta-editor-lab/bridge06_build.py) ricrea le varianti da sorgenti originali con SHA verificati. La [prova completa](references/BRIDGE06_COMMON_GESTURE_20261119.md) registra modifica diretta del testo rich in Codex senza inspector forzato, modifica diretta della label in Studio21, export/riapertura separati e capacità privacy/template/link preservate. Le patch sono limitate a un gesto, non a un nuovo editor generale.

**Nuova differenza assimilata:** pointer capture dello Studio21 cambia l'evento target del secondo clic; il test iniziale falliva. `elementFromPoint` recupera il referente effettivo. Il test Bold su un H1 ha esercitato una disattivazione corretta, riformulata poi come selezione Italic. L'intervento non altera i sistemi di formattazione e dati rispettivi. Test Node/Chromium e viewport mobile sì; file:// Chrome Windows, accessibilità/touch e siti reali differenti non provati.

**Prossimo discriminante:** comando `setText`/commit/cancel/undo su due adapter con focus e caret coerente, preservando il DOM/markup Codex e il modello scene Studio. Ancora nessun cambio delle copie `maios_it` o dei prodotti pubblici.


updated: 2026-11-19
status: public_tool_and_codex_rich_editor_source_field_reconciled; no_new_product_release

## 19 novembre — nuova fonte Codex e MetaCanvas pubblico restituiti alla competenza

L'operatore ha corretto l'ambito: **MetaCanvas è già un tool pubblico MAIOS, incompleto**, e una sua bozza HTML attualmente usata con Codex offre editing di testo ricco e altre funzioni che i Lab/R5 non avevano conservato. Il [nuovo inventario owner-native](references/SOURCE_FIELD_PUBLIC_TOOL_CODEX_DRAFTS_20261119.md) distingue pagina pubblica, Playground IT/EN, Studio20 generale, Studio21 demo IT/EN, Codex page-editor, Lab01–05, vecchia R5 specifica e Siteman Studio. L'allegato Codex di 419.563 byte è stato letto e controllato con Node e Chromium su un percorso delimitato; non è stato importato nel prodotto, né sostituito. La difficoltà UX è coerente con la sovrapposizione effettivamente osservata fra toolbar testuale e inspector globale.

**Regola operativa ora raggiungibile:** il prossimo sviluppo deve preservare contemporaneamente formattazione/selection/caret Codex, schema/note/template/pubblico/AI merge Studio20, gestione dei diagrammi Lab05 e origine/revisioni/patch del sito, senza fare coincidere i tre modelli di stato. La R5 della vecchia R4 è evidenza separata, non sorgente canonica. La ricognizione non prova l'HTML distribuito effettivamente servito dal server, browser Windows fisico o compatibilità universale.

**Effetti:** aggiornati metodo e routing della competenza; nessun commit sul runtime pubblico, nessun merge, nessun asset sostituito e nessun sito pubblicato.


updated: 2026-11-19
status: first_R4_MAIOS_page_adapter_R5_conversation_artifact_tested; no_site_or_studio_deploy

## 19 novembre — prima prova su pagina R4 MAIOS, R5 locale

Dopo Lab05 l'operatore ha scelto «l'ultima pagina di MAIOS MetaCanvas già usata». È stata riaperta l'esatta `MAIOS_Consulenza_MetaCanvas_R4_Editor_Contestuale_IT.html`, diversa dall'attuale sorgente produttiva MAIOS. La [prova R4→R5](references/first-real-page-r5-20261119.md) ha prodotto un HTML sperimentale consegnato nella conversazione: un solo dock, modifica diretta, inserimenti dentro le quattro regioni, diagramma con testo dei nodi editabile in loco e azioni collettive contestuali. Possiede esportazione di progetto riapribile, HTML statico e patch JSON **a livello di regione** vincolata alla R4 originaria.

**Prova:** Chromium/Node con patch vuota su documento invariato, una sola regione hero modificata dopo due interventi, file progetto riaperto con una UI, clean export senza editor, immagine e colonne salvate, viewport 390 senza overflow globale, nessun pageerror nei percorsi esercitati. Sono stati corretti re-render su click che impediva il doppio clic reale, serializzazione errata del progetto, false differenze causate da attributi editor e sovraccarico della toolbar. Il browser amministrato blocca `file://`; non attribuire l'uso Windows reale o un sito modificato.

**Confini:** codice R5 della pagina non aggiunto a questa repository, Studio20/21 e Lab05 restano distinti, MAIOS.it non modificato, Codex non attivato. Resta aperto un secondo sito diverso e la ricognizione della pagina produttiva corrente **prima** di autorizzare l'applicazione di eventuali patch.


updated: 2026-11-19
status: Lab05_spatial_nodes_committed_and_chromium_exercised; Chrome_Windows_human_unobserved

## 19 novembre — Lab05 disponibile, strumenti spaziali dei diagrammi

L'operatore ha chiesto di migliorare l'editor generale con gesti più efficaci, aiutandosi con le UI di strumenti esistenti. La nuova risultante [Lab05 HTML](../../../../examples/collaborative-communication-medium/meta-editor-lab/MetaEditor_Lab05_Diagrammi.html) mantiene Lab04 e aggiunge gestione di **più nodi dello stesso diagramma**: Maiusc+clic, allineamento/distribuzione, spostamento collettivo, duplicazione con ricostruzione dei link, griglia, inserimento tramite doppio clic direttamente nell'area e modifica del testo immediata. [Il README](../../../../examples/collaborative-communication-medium/meta-editor-lab/LAB05_README.md) registra fonte, prove e limiti. Sono state corrette due collisioni effettive (copie e nuovo nodo in uno spazio occupato), crescita del canvas e la creazione di un Undo fittizio per allineamenti senza variazione.

**Prova:** Node v22 + Chromium headless Playwright `set_content`: gesti di selezione, gruppo, drag, Undo, copia, relazione di link, riapertura HTML e mobile 390px senza overflow nel caso; nessun pageerror osservato. La repository ha il codice di laboratorio, non un rilascio Studio20/21 o un editor universale installato. La pagina MAIOS.it, D-ND.com e il codice Codex rimangono invariati.

**Prossimo discrimine**: utilizzo umano su Chrome Windows e, quando selezionato, un primo adapter su regioni HTML dichiarate e patch sicura, verificata su una seconda pagina diversa; questo Lab05 non ha esercitato quell'adapter.


updated: 2026-11-17
status: Lab04_multi_selection_committed_and_browser_exercised; human_file_url_usability_unobserved

## 17 novembre — Lab04 gesti multipli, prima della compatibilità con siti veri

Il [Lab04 HTML autonomo](../../../../examples/collaborative-communication-medium/meta-editor-lab/MetaEditor_Lab04_Manipolazione.html) è presente in K-UX-AI con [test, limiti e contratto](../../../../examples/collaborative-communication-medium/meta-editor-lab/LAB04_README.md). Il nuovo saper fare è composizione collettiva di blocchi della pagina: Maiusc+clic, copia/taglia/incolla interno all'editor, duplica/elimina/sposta insieme, shortcut e un Undo per azione. Conserva diagrammi, nodi, collegamenti e temi. Non supporta ancora grouping persistente o clipboard OS. Node/Chromium set_content: selezione, duplicazione, undo/redo, trasferimento fra sezioni, testo in nodo, roundtrip HTML, 390 px; nessun pageerror nei percorsi. È stato tolto il doppio luogo di Copia/Taglia e reso esplicito che gli appunti sono locali.

**Confini:** il file è un esempio prodotto/testato, non una release Studio20/21, né un adapter per pagine reali, né un deploy MAIOS/D-ND. La qualità dell'uso in Chrome Windows resta da osservare. Prossimo discriminante: regione HTML dichiarata, patch e secondo sito differente, conservando la competenza di selezione multipla.


updated: 2026-11-17
status: Lab03_object_first_editor_committed_and_browser_exercised; end_user_usability_unobserved

## 17 novembre 2026 — Lab03: competenza esercitata sulla manipolazione degli elementi

**Nuova priorità operatoria:** i temi sono subordinati alla capacità di usare davvero l'editor. [Lab03 · Gestione elementi](../../../../examples/collaborative-communication-medium/meta-editor-lab/MetaEditor_Lab03_Elementi.html) è presente in K-UX-AI come esempio HTML autonomo con [README e limiti](../../../../examples/collaborative-communication-medium/meta-editor-lab/LAB03_README.md), distinto dalle release Studio20/21 e dai siti.

**Effetti esercitati:** selezione esplicita di sezioni, gestione della struttura, proprietà di oggetto collocate in alto, inserimento contestuale, conversione titolo/testo/card, riordino e spostamento con o senza drag, nodi/collegamenti/forme, layout responsive e temi conservati. Node syntax + Chromium set_content hanno coperto editing diretto, Undo/Redo, duplicazioni, trasporto fra sezioni, relazione node-link e rimozione link, cinque nodi distribuiti senza sovrapposizione dei loro rettangoli, tema, HTML export e riapertura, viewport 390 px senza overflow globale e nessun pageerror osservato. File HTML riletto da GitHub identico ai byte condivisi della versione validata. I limiti del runner bloccano file://: nessuna prova reale Chrome Windows né valutazione d'uso dell'operatore.

**Apprendimento:** la sequenza originale di prova non guardava la densità dei nodi; una schermata ha reso evidente la collisione dei rettangoli. La nuova prova controlla anche geometria e non solo modello. La posizione dell'inspector rispetto all'outline cambia il costo del gesto: l'oggetto selezionato governa i controlli visibili, la sezione resta raggiungibile senza occupare lo spazio principale. Le ragioni e il metodo vivono in [GUIDE](GUIDE.md), la separazione degli owner in [SKILL](SKILL.md). Non è un adattatore universalmente affidabile per le pagine HTML.


updated: 2026-11-17
status: Lab02_theme_library_committed_and_locally_exercised; no_Studio_port_or_site_deploy

## 17 novembre — libreria temi e recupero di capacità dalle sorgenti

**Richiesta attuale:** temi recuperabili standard/MAIOS/D-ND/presentazione, da usare anche per rendere percepibili le possibili composizioni, mantenendo semplice il MetaEditor e connessa la competenza al lavoro. [Sorgenti, metodo, prova e limiti](references/theme-library-20261117.md) ora possiedono la risultante.

**Artefatto in K-UX-AI:** [Lab 02 — Themes](../../../../examples/collaborative-communication-medium/meta-editor-lab/MetaEditor_Lab02_Theme_Library_IT.html) pubblicato come **esempio autonomo**, readback GitHub byte-identico all'HTML del laboratorio. Non è il runtime di Studio20/21 e non modifica alcun sito.\n\n**Artefatto creato in conversazione:** `MetaEditor_Lab02_Theme_Library_IT.html` (successore del Lab01, ancora non presente nella repository come HTML). Esercitati: selezione fra 5 profili, overlay di espressioni MAIOS, modifica/creazione di tema personale con composizioni suggerite configurabili, salvataggio nel documento e in localStorage dove consentito, export/import JSON, lettura selettiva di CSS da HTML Collaborazioni, testo del diagramma ancora editabile in situ, Undo, export HTML e riapertura. Node/Chromium `set_content`, viewport 390 e screenshot MAIOS/D-ND verificati; apertura `file://` bloccata dal runner. La copia locale dell'HTML e la guida restano raggiungibili in conversazione; l'HTML di esempio è ora raggiungibile anche tramite GitHub al percorso indicato. Questo non certifica adozione in altri riceventi.

**Prossimo discriminante:** esercitare un import dichiarativo e non distruttivo di regioni HTML (minimo due siti), collegare tema e patch come stati distinti, poi considerare il trasporto del motore ai vari MetaCanvas. Codex non è stato attivato e nessun sito o release è stato modificato.


updated: 2026-11-16
owner: GrazianoGuiducci/k-ux-ai / collaborative-communication-medium / meta-editor
status: competence_formed; neutral_lab01_node_edit_browser_exercised; end_user_usability_unobserved
runtime_owner: examples/collaborative-communication-medium/ (future candidate)
distribution: no release; no MAIOS.it deployment

## Presente selezionato
L'operatore chiede una competenza dedicata che evolva il MetaEditor. La forma pertinente è una specializzazione **interna a CCM/K-UX-AI** sul metodo di progettare e verificare editor generalizzabili. L'architettura da discriminare conserva differenze fra pagina web, presentazione, diagramma, contenuto originale e strumenti di modifica; non prosegue automaticamente R4.

## Prima risultante tecnica — Lab 01

Il [prototipo neutro](../../../../examples/collaborative-communication-medium/meta-editor-lab/MetaEditor_Lab01.html) è ora in K-UX-AI con [documentazione della prova](../../../../examples/collaborative-communication-medium/meta-editor-lab/README.md). Node + Chromium tramite set_content hanno verificato `contenteditable` direttamente nella label, Enter, Undo/Redo, trascinamento del nodo con link, card fra sezioni, sezione template non distruttiva, salvataggio/riapertura HTML e viewport 390 px. Sono stati corretti due difetti trovati in corso d'opera: parentesi CSS mancante che alterava la geometria e template che sostituiva indebitamente una sezione. La [GUIDE](GUIDE.md) custodisce il saper fare emergente.

**Limiti:** pagina/proiezione slide sono due viste del documento sintetico `metaeditor.lab.v1`; non integrazione con Studio20 `ccm.document.v1`. Il banco non importa HTML arbitrario né è stato esercitato su Chrome Windows reale; la qualità percepita dal ricevente resta da osservare. Fonte pubblica non equivale a runtime installato in Codex o MAIOS.it.

## Primo banco / stato degli effetti
Il primo esercizio deve testare **doppio clic sulla label di un nodo e digitazione in situ**, una card duplicabile su layout responsive e round-trip del documento con un solo storico. Soluzioni esterne restano candidate, non importate. La copia del sito MAIOS non è il banco neutro. Un documento o un test creato in una conversazione non equivale a un file già residente in K-UX-AI; registrare qui il percorso reale se e quando trasferito.

## Limiti
Competenza scritta ≠ runtime integrato ≠ sito modificato ≠ funzionalità esercitata dall'operatore ≠ assimilazione futura. Esercizi precedenti R3/R4 conservano prove specifiche e difetti, ma non soddisfano la nuova prova. Codex non è automaticamente attivato.
