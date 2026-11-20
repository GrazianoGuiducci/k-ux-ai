# Bridge 08.1 — selezione coerente fra struttura e testo

**Data:** 20 novembre 2026  
**Owner:** K-UX-AI / CCM / MetaEditor Evolution  
**Fonte decisiva:** screenshot reale dell'operatore su Chrome Windows, con la pagina `MetaEditor_Bridge08_Bozza_Codex_IT.html`: un elemento del titolo ha il contorno viola di selezione strutturale, mentre è attiva la modifica ricca di un testo diverso nel riquadro destro. L'operatore segnala che la doppia selezione può creare problemi.  
**Stato:** correzione *sperimentale sulla sola bozza Codex Bridge 08*, esercitata in Node/Chromium; non è applicata al MetaCanvas pubblico, a Studio21, al repository MAIOS.it o al checkout Codex.

## Comprensione causale (non riscrivere il passato)

Il Bridge08 aveva aggiunto una UI contestuale al vero editor Codex senza cambiare i dati del sito. Nel ramo `main.addEventListener('dblclick')` il documento nascondeva `#local-tools` impostando direttamente `tools.hidden=true`, ma **non richiamava `syncTools(section)`**. Perciò gli attributi `data-local-picked` e `data-local-selected` rimanevano nel DOM e il browser continuava a disegnare il contorno della selezione strutturale, anche mentre un altro campo `contenteditable` e la mini-toolbar rich text erano attivi. Il problema è una **mancata transizione di stato**, non la necessità di aggiungere un altro pannello.

Non confondere **selezione dell'oggetto per layout/proprietà** con **selezione di caratteri/parole dentro il testo**. Quest'ultima deve continuare a funzionare durante l'editing rich text. Una selezione multipla esplicita nei diagrammi rimane un'altra operazione e non va soppressa da questa regola.

## Correzione esercitata
Nel ramo diretto del doppio clic, quando il pannello viene nascosto, aggiornare prima il referente `picked` e poi richiamare `syncTools(section)` **mentre `tools.hidden` è true**. La funzione esistente pulisce i vecchi attributi di outline e aggiorna la sezione senza distruggere il `Range` o spostare il caret. Riaprendo la struttura si ritrova così l'elemento che l'operatore sta effettivamente modificando.

Il livello UX08 mostrava soltanto «Modifica in corso», che non permetteva di capire il referente. Ora mostra `Testo · …` con una breve parte del testo realmente attivo; il testo completo è nel tooltip. L'interazione rimane nel contesto esistente: nessun nuovo toolbar, API documento, preferenza o formato.

Lo [script di riproduzione K-UX-AI](../../../../examples/collaborative-communication-medium/meta-editor-lab/bridge08_1_selection_fix.py) controlla SHA-256 e ancore della versione Bridge08 originale; non sovrascrive input o HTML canonico. La versione corretta è stata generata e distribuita nella conversazione come `MetaEditor_Bridge08_1_Selezione_Coerente_IT.html`.

- Input HTML SHA-256: `be278d0ddaaf5430c8168d78c18600968453fe242339b4c74272af8caf5f880f`
- Output HTML SHA-256: `9dbbf5b5337aa94a8252e9624fab2c75a2ded7dd555db5d9b675501d73fe8e0c`

## Prove e osservazioni

**Reproduzione controllata del difetto precedente:** Chromium, aprire Struttura, selezionare titolo, generare il doppio clic su testo diverso. Il vecchio handler lasciava `data-local-picked` e la sezione marcata quando `tools.hidden` era true, contemporaneamente a `data-local-editing` e mini-toolbar. Lo screenshot Windows dell'operatore dimostra il sintomo nell'uso effettivo; il test Chromium ne individua il meccanismo specifico.

**Dopo la correzione:** Node `--check` su tutti gli script inline; Playwright Chromium su transizione titolo→testo destro: zero elementi `[data-local-picked]`, zero sezioni `[data-local-selected]`, mini-toolbar aperta e campo rich text attivo; reopening Struttura seleziona il nuovo testo; nuovo doppio clic sul titolo cambia correttamente referente; Esc annulla. Il contesto UI mostra il testo in modifica. Un test distinto ha esercitato `setText`, commit, Ctrl+Z/Y, export HTML, riapertura con una sola UI, nessun outline persistito e viewport 390 px senza overflow globale nel campione; zero pageerrors osservati nei percorsi. File Bridge08 originale verificato byte-identico dopo i test.

**Limiti:** la nuova versione non è ancora stata provata dall'operatore su Chrome Windows; il runner Chromium usa `page.set_content`, non navigazione reale `file://`. Non abbiamo verificato ogni percorso di trascinamento/resizing, tutte le combinazioni editor legacy, touch o accessibilità assistiva, né applicato il fix a pagine HTML esterne o a Studio21. Il file di test esportato con testo sintetico non va applicato a MAIOS.it.

## Metodo che deve continuare

Quando un'interfaccia mostra due elementi apparentemente attivi, ricostruire la **macchina di stati della selezione e il referente dell'effetto** prima di aggiungere controlli o togliere outline per via CSS. Ogni transizione verso l'editing del testo deve aggiornare lo stato strutturale, mentre la selezione del Range rimane propria del rich text. Validare la sequenza completa: elemento A selezionato → testo B editabile → richiama Struttura → B è il referente → export/riapertura senza UI doppia e senza marcatori rimasti.

**Prossima distinzione:** migliorare poi l'inserimento di elementi nel punto, le azioni contestuali e il passaggio da pagina a scena **sulla base del gesto umano osservato**, senza perdere il modello `ccm.document.v1` del prodotto pubblico. La correzione non autorizza un nuovo rilascio o una modifica di MAIOS.it.
