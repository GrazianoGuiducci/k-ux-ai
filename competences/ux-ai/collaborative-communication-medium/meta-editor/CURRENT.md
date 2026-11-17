# MetaEditor Evolution — CURRENT

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
