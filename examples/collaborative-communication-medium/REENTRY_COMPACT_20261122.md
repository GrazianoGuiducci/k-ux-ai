# MetaCanvas + MetaEditor — checkpoint di rientro compatto · 22 novembre 2026

## 22 novembre — Inserimento nativo condiviso, provato su due portatori pagina

**Nuovo punto d'appoggio:** [`metaeditor-composition-commands.js`](meta-editor-lab/metaeditor-composition-commands.js), [contratto](meta-editor-lab/COMPOSITION_COMMANDS.md) e [6 test Node](../../tests/metaeditor-composition-commands.test.js) nel ramo candidato K-UX-AI. Aggiunge soltanto `execute('insert', …)`, mappando la richiesta sul comando nativo del carrier: pagina HTML `addBlock`, scena Studio21 `addNode`. Non tocca `MetaEditorCommands` Bridge07, storia, formati o UI dei prodotti. Test Chromium 1440/390 su vero Bridge11 e R3 MDN con inserimento e Undo: superati, senza pageerror; test browser ripetibile salvato nel workbench privato `maios_it/work/metaeditor-current/workbench/metaeditor/experiments/test_composition_native_bridge.py`.

**Errore e riparazione:** inserimento relativo non disponibile dopo un cambio di sezione deve ripristinare la selezione preesistente; ora controllato da test. Per le scene il contratto è provato solo con mock di pulsanti e conferma di codice Studio21, **non** test E2E del vero Studio21. **Gate B ancora parziale**, PR #2 draft, nessun deploy. Prossima unità utile: esercitare il modulo sulla scena reale, mantenendo distinto `ccm.document.v1` dall'HTML e senza aggiungere una seconda toolbar. Il rientro continua da questo risultato, senza riesaminare i precedenti Bridge.


## 22 novembre — Passo successivo esercitato: export browser riusabile

**Ora raggiungibile:** [`static-page-source-adapter.js`](meta-editor-lab/static-page-source-adapter.js) nel ramo K-UX-AI, test Node [`tests/metaeditor-static-page-source.test.js`](../../tests/metaeditor-static-page-source.test.js); il modulo sostituisce la parte di export della R3 MDN ma **non** i suoi gesture/editor. [Versione R3 con adapter](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/workbench/metaeditor/experiments/MetaEditor_MDN_R3_Shared_Source_Adapter_20261122.html) e builder vincolato conservati nel ramo privato del documento, blob output `2b2a6045fe2faf56f34b4730db6310c5ed11b65e`. I test locali Node e Chromium 1440/390 su MDN e fixture diverso, più uso integrato UI R3 con insert/Undo/export, sono passati nei percorsi; errore di attributo quotato non chiuso individuato e corretto.

**Competenza aggiornata:** K-UX-AI MetaEditor CURRENT e GUIDE; distinzione mantenuta fra il precedente patcher Python (trasformazione della sorgente già revisionata da un receiver) e il nuovo exporter browser (ripulisce DOM transitorio e confronta baseline immutabile). I limiti della prova sono in quelle sorgenti. `CURRENT.html` Bridge11, MetaCanvas pubblico e `maios_it/main` sono invariati. **Gate B parziale**: non dichiarare portabilità universale né release; il prossimo passo può esercitare l'editing/export su altre strutture supportate e la regressione completa prima di pubblicare. Il cambio istanza resta facoltativo.


**Scopo:** ridurre la lunghezza e il costo dei rientri in ChatGPT, conservando l'avanzamento reale senza ripetere l'intera conversazione. Questo è un cursore operativo, non autorità su release o prova esterna.

## Verifica successiva — R3 già persistita, lavoro continuabile nella stessa istanza

**Correzione alla comprensione del checkpoint precedente:** la frase sotto («non risulta un commit GitHub verificato di R3») descrive la verifica incompleta di quel momento, **non lo stato attuale**. Il 22 novembre alle 12:05–12:08 UTC la repository privata `GrazianoGuiducci/maios_it`, ramo `work/metaeditor-current`, aveva già acquisito HTML R3, sorgente MDN, CSS, generatore, test e spiegazione. La loro presenza e i blob sono stati riletti nel movimento successivo; non retrodatare questa verifica né interpretare l'assenza del rilievo come assenza dell'effetto.

**Identità comprovate:**
- [HTML MetaEditor MDN R3](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/workbench/metaeditor/experiments/MetaEditor_MDN_Independent_R3_20261122.html), Git blob `5b1dcb244dfcfc9d90f545174ce2a58ae5eb4734`, SHA-256 `8af2f8b18605f25f8a0e2da9e965c46364cb2756964699c52af7ef940cf75189`.
- [Builder R3](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/workbench/metaeditor/experiments/build_mdn_bridge_r3.py), Git blob `a6e16b7bcea6f01b397b87afbfa0f65bc737ada1`; [test R3](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/workbench/metaeditor/experiments/test_mdn_bridge_r3.py), blob `a7f47a2f62d883fe585da67b0c2b4c632a045b23`.
- [Sorgente MDN CC0](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/workbench/metaeditor/experiments/mdn_page_original.html), blob `0a2636f1c1bb30ffa6515141c831e348b9bd6150`, e CSS, blob `ff73dc352eb854b511a2caf2d2d016a3f5d2789a`.
- Builder rieseguito localmente con input R2 e MDN verificati: output SHA-256 identico all'HTML R3 archiviato. Test Chromium rieseguiti con successo a 1440×844 e 390×844 per no-op, undo, modifica ed export limitato a `main`, lavoro salvato e riaperto. I test non certificano compatibilità generalizzata o Windows file://.

**Nuovo orientamento operativo:** possiamo **continuare in questa istanza** e trasferirci solo quando diventi realmente onerosa, senza una migrazione preventiva. La prossima differenza tecnica è delimitare/estrarre l'adattatore di pagina riutilizzabile dalla R3 privata, con fixture ed export verificabili, non recuperare nuovamente file che sono già raggiungibili. Gate B rimane **parziale**. Il prossimo ricevente prende questo checkpoint, [release gate](RELEASE_STABILIZATION_20261122.md), [handoff](WORK_HANDOFF_STABILIZATION_20261122.md) e [owner MetaEditor CURRENT](../../competences/ux-ai/collaborative-communication-medium/meta-editor/CURRENT.md), non tutta la conversazione. Per ogni avanzamento: output, prova, commit/readback e una sola differenza rilevante nella competenza; non generare copie narrative ridondanti.

## Risultato effettivo
- MetaCanvas generale, Playground r4 IT/EN e Studio21 IT/EN: cinque sorgenti K-UX-AI confrontate con copie della repository del sito `maios_it`, blob Git corrispondenti.
- [PR K-UX-AI #2](https://github.com/GrazianoGuiducci/k-ux-ai/pull/2) su `work/metacanvas-metaeditor-stabilization-20261122`: aperta **in bozza**, controlli di baseline/CI riusciti; non equivale a rilascio stabilizzato.
- MetaEditor Bridge11: versione di lavoro privata nel ramo `maios_it/work/metaeditor-current`; l'operatore riferisce «Nella versione 11 non vedo problemi». Non è un editor universale.
- Neutral Probe R2: file e generatore nella [cartella esperimenti privata](https://github.com/GrazianoGuiducci/maios_it/tree/work/metaeditor-current/workbench/metaeditor/experiments); esercitati editing, inserimento, spostamento, Undo, export lavoro e pagina pulita su desktop/mobile. Struttura ancora vicina a MAIOS.
- **R3 su pagina MDN indipendente:** in questa conversazione sono stati prodotti e provati artefatti locali (HTML di test e ZIP). Le prove riferite comprendono export no-op identico all'originale, modifiche circoscritte a `main`, Undo/Redo, salvataggio/riapertura e desktop/mobile; è emersa e stata corretta una perdita del riferimento alla sorgente originale dopo salvataggio. **Non risulta un commit GitHub verificato di R3**: non dichiararlo persistito in repository o rilasciato. Identità dell'ultima copia fornita in chat: `MetaEditor_Independent_R3.html`, SHA-256 riferito `8af2f8b18605f25f8a0e2da9e965c46364cb2756964699c52af7ef940cf75189`; pacchetto `MetaEditor_R3_Prova_Indipendente.zip` (verificare gli allegati esatti al rientro).
- Nessun nuovo deploy `maios_it/main`. La prova umana su Bridge11 non certifica gli altri carrier, accessibilità, sicurezza o uso Windows `file://` di R3.

## Blocco materiale, non narrativo
La R3 resta un esercizio documentale in chat: occorre renderla raggiungibile con sorgente/build/test riproducibili nell'owner corretto e chiarire quali invarianti del documento l'adattatore può garantire. Il Gate B di [RELEASE_STABILIZATION_20261122.md](RELEASE_STABILIZATION_20261122.md) è **parziale**, non chiuso. Poi i gate C–F (regressioni MetaCanvas, accessibilità/compatibilità, candidata e distribuzione) restano aperti.

## Prossimo movimento, nella stessa istanza o al rientro
1. Leggere soltanto questo checkpoint, la [guida di stabilizzazione](RELEASE_STABILIZATION_20261122.md), l'[handoff implementativo](WORK_HANDOFF_STABILIZATION_20261122.md) e [MetaEditor CURRENT](../../competences/ux-ai/collaborative-communication-medium/meta-editor/CURRENT.md); rivalidare PR e branch, senza rigiocare tutta la chat.
2. Recuperare gli artefatti R3 della conversazione o dal file Library **prima** di dichiararli disponibili; controllare SHA e ricostruibilità. Se non materializzabili, non inventare l'HTML: il codice/fixture va ricostruito dal builder verificato.
3. Chiudere soltanto il prossimo gate: consegna dell'adattatore e fixture neutri con test di regressione e prova di preservazione del documento; nel ricevente Codex usare il suo checkout nativo, non fingere di averlo modificato da ChatGPT.
4. Consegnare un risultato durevole per volta: codice + test + readback + limiti, poi un riepilogo breve. Non produrre molti allegati temporanei né aprire sottoprogetti mentre il gate corrente è ancora aperto.

## Regola di economia di contesto acquisita
L'operatore segnala blocchi ripetuti dell'istanza. Non attribuirne con certezza la causa a limiti non osservabili. In lavori lunghi: checkpoint essenziale owner-native, rientri selettivi, massima una risultante testabile per turno, tool calls raggruppate, nessun riversamento di interi file/log in risposta e passaggio tempestivo a nuova istanza. Conservare prove e stati nell'owner, non nella memoria verbosa della chat.

**Effetti non autorizzati o non eseguiti:** fusione PR, pubblicazione MetaCanvas/MetaEditor stabilizzati, push production, aggiornamento del sito live, esecuzione autonoma Codex.
