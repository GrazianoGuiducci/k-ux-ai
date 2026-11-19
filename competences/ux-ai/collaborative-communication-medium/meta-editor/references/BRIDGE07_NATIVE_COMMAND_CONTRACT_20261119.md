# MetaEditor Bridge 07 — comando comune, portatori distinti

**Data:** 19 novembre 2026 · **Owner:** K-UX-AI / CCM / MetaEditor Evolution  
**Stato:** **due HTML sperimentali verificati in Chromium**, builder riproducibile pubblicato nella repository; **non** release Studio 20/21, non deploy MAIOS.it o esecuzione del checkout Codex.

## Perché questo movimento
Dopo [Bridge06](BRIDGE06_COMMON_GESTURE_20261119.md), l'operatore seleziona di proseguire verso un **contratto di comando** per i due gesti già verificati. Non creare un terzo stato di documento o una nuova toolbar: l'azione comune viene interpretata dall'owner nativo dei dati. Le fonti sono esattamente le due **copie Bridge06**, già derivate da sorgenti Codex e Studio21 con SHA verificati.

La prima capacità è:
- **F2** sull'elemento selezionato → `begin`;
- **Ctrl+Invio** → `commit`; **Esc** → `cancel` per l'editazione in corso;
- **Ctrl+Z** → `undo`; **Ctrl+Y** / **Ctrl+Maiusc+Z** → `redo` quando non si sta digitando in un campo;
- il doppio clic già esistente resta operativo;
- comandi disponibili anche su `window.MetaEditorCommands`: `status / begin / setText / commit / cancel / undo / redo`, con esito `{ok:boolean,...}`, versione 0.7.0, carrier e semantica dichiarata.

**`setText` NON significa la stessa mutazione nei due portatori.** Nel Codex HTML è una sostituzione/inserimento della sola selezione rich text, con markup vicino preservato; in Studio21 è una sostituzione della **stringa** nella label del nodo. La firma è condivisa, il significato e il modello restano distinti. Il progetto non migra `ccm.document.v1` in HTML pagina, né conferisce HTML ricco alle label Studio.

## Fonti ed effetti
- Input Codex: `MetaEditor_Bridge06_Bozza_Codex_IT.html`, SHA256 **`7f8f72f4ce98b5890f468058919dc01523395928b262a79c78166895684ad759`**. Output Bridge07: `MetaEditor_Bridge07_Bozza_Codex_IT.html`, SHA256 **`1ab5e4589953302ddd16b7b98dcd9c3017b7b61db63908a5dc43d93bc24b77f8`**.
- Input Studio: `MetaEditor_Bridge06_Studio21_Consulenza_IT.html`, SHA256 **`6f39f3bbf2bc27bd6c16cda0cca375cf7bbb4e21960a84513966a04e45797a77`**. Output Bridge07: `MetaEditor_Bridge07_Studio21_IT.html`, SHA256 **`e709d738531fa1023c404e4bbc8fc3326d3fc6033ca38ee7d391e07867da3a89`**.
- Il [builder Python 3.11 stdlib](../../../../examples/collaborative-communication-medium/meta-editor-lab/bridge07_build.py) accetta soltanto input con hash esatti, produce **due** HTML offline e non modifica gli originali. La catena completa resta `bridge06_build.py` → `bridge07_build.py`. Il sorgente builder è stato riletto dal repository con contenuto identico.
- Output HTML sperimentali e pacchetto con prove sono artefatti della **conversazione**, non copie distribuite da `maios_it`. Nessun file di bozza Codex è stato inserito in K-UX-AI.

## Saper fare ed errori che hanno cambiato il metodo
1. **La cancellazione è rollback, non solo chiusura della toolbar.** Codex conserva l'`innerHTML` del campo e lo stato della propria history all'ingresso della modifica: Esc ripristina esattamente entrambi. Studio usa `cancelDirectEdit(false)`, il percorso nativo del modello. Una successiva Escape dopo `blur` non deve annullare una modifica già implicitamente conclusa: la sessione viene invalidata.
2. **Una cronologia ripristinata può spostare il focus.** Nel primo test, dopo Ctrl+Z la funzione Codex `restoreText` riportava il caret in `contenteditable`; Ctrl+Y finiva quindi nella storia del browser invece che nella `future` strutturale. È stato introdotto un breve stato di navigazione del documento: il successivo Ctrl+Y raggiunge il redo nativo anche se il focus è nel campo, ma un nuovo `beforeinput` restituisce la gestione all'editing testuale. È la nuova differenza del movimento, non un difetto già risolto dal Bridge06.
3. **Selezione ricca e stringa non sono equivalenti.** Il comando della pagina non azzera `innerHTML` o paragrafi interi: opera nel `Range` ed esegue `insertText` attraverso le capacità browser già usate da Codex (con fallback DOM). Vanno preservate selezione, markup esterno, storia e caret; l'uso di `execCommand` rimane una scelta legacy dell'editor, non un'API raccomandata per nuovi prodotti.
4. **Non aggiungere la settima toolbar.** Sono state aggiunte scorciatoie e informazioni accessibili nei tooltip dei controlli già esistenti. L'editor avanzato rimane su richiesta. Test di compatibilità visuale senza introdurre un altro pannello.

## Prove osservate e limiti
Node v22 `--check` su entrambi gli script della bozza Codex e sui due script eseguibili Studio21. Chromium headless Playwright tramite `page.set_content`:
- Codex H1 → doppio clic/F2, testo digitato → Esc con HTML identico al pre-edit e nessun Undo superfluo; secondo intervento → Ctrl+Invio → Ctrl+Z e Ctrl+Y; API `setText` sostituisce una parte della stringa mentre restano i tag `<b>` e `<em>` sui segmenti non selezionati. File HTML esportato e riaperto conserva i controlli e il comando Bridge07.
- Studio21: nodo selezionato → F2 → `setText` → Esc, poi nuova modifica → Ctrl+Invio; file `Salva lavoro` contiene `ccm.document.v1` con **sette scene**, label aggiornata, e si riapre con il comando Bridge07.
- Copia pubblica su **dati sintetici**: nota privata, nodo `private:true` e raccolta di template personali restano esclusi dal file pubblico; sette scene conservate.
- Responsive 390px: nessun overflow orizzontale globale nei documenti di prova; nessun `pageerror` nei percorsi; esecuzione ripetuta del builder produce byte identici.

**Non verificati:** apertura reale `file://` nel Chrome Windows dell'operatore; browser diversi, touch, screen reader, formattazione complessa in tutte le regioni del sito, selezioni simultanee e adattamento a HTML arbitrari. La prova di questo contratto **non** garantisce round-trip fedele su pagine nuove o fusione completa Studio20/Lab05.

## Prossima discriminazione
Due esigenze possibili, senza imporre una soluzione:
1. **Aderenza al gesto umano** in Chrome Windows: test F2/CTRL+ENTER/ESC su testo con markup misto e nodo dentro presentazione, distinguendo problemi di interazione da stato e layout.
2. **Adattatore di regione reale**: editare una porzione dichiarata dell'HTML attuale MAIOS e una seconda pagina differente, generando diff selettivo, senza cancellare nota, template o sorgente esterna.

L'apprendimento deve continuare in [SKILL](../SKILL.md), [GUIDE](../GUIDE.md) e [CURRENT](../CURRENT.md); nessuna nuova R8 o pubblicazione nasce automaticamente dal solo completamento della prova.
