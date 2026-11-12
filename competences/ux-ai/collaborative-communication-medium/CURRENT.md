# Collaborative Communication Medium — CURRENT

**Data:** 2026-11-11 · Europe/Rome  
**Versione:** 0.1.0-candidate  
**Owner:** K-UX-AI / competences/ux-ai/collaborative-communication-medium  
**Stato iniziale (prima dell'esercizio locale):** SOURCE_COMPETENCE_FORMED / RUNTIME_NOT_YET_BUILT / GENERALIZATION_PENDING

## 12 novembre — Studio 07, aggiramento e quattro ingressi per lato

**Mandato:** rafforzare l'aggiramento quando i riquadri si toccano o si sovrappongono; punte di freccia solo inizio, solo fine, entrambe o nessuna; ganci/punte visibili davanti alle schede; quattro ingressi standard per lato e distribuzione quando più frecce convergono.

**Artefatto locale prodotto:** `MAIOS_Comunicazione_Collaborativa_Studio07.html`, 135.511 byte, SHA-256 `d56564923d767f09119e75984ec54a885a64f5ad2aaac6eeae2da8a7b591a7c8`, ZIP di 39.948 byte con HTML identico. Unico file offline con schema `ccm.document.v1`. [Guida](GUIDE.md#12-novembre-2026--studio-07-il-gancio-è-un-oggetto-percettivo-non-un-nuovo-referente) esplicita meccanismi e limiti.

**Esercizio:** sette situazioni geometriche × due relazioni, senza attraversamento degli interni o collisione con riquadri dei badge nei casi campionati; quattro ingressi distinti sullo stesso lato (20/40/60/80%); quattro modalità di punta SVG; click sul gancio, scelta della porta, export/reopen e punte bidirezionali attraverso mini editor; copia pubblica priva del testo di appunto privato; ZIP verificato; prova iniziale con 24 collegamenti/12 nodi senza JS error. Test Chromium Playwright su HTML caricato nel harness, non uso umano di `file://`.

**Stato:** STUDIO07_HTML_LOCAL_BUILT / CONTACT_BYPASS_AND_PORTS_CHECKED / BIDIRECTIONAL_HEADS_AND_REOPEN_CHECKED / PUBLIC_COPY_PRIVACY_CHECKED / USER_REVIEW_PENDING / KUX_PUBLIC_RUNTIME_UNCHANGED / CROSS_CASE_ASSIMILATION_UNKNOWN.

## 12 novembre — Studio 06, frecce semantiche e percorso adattivo

**Fonte:** screenshot reale dell'operatore su Studio 05 in Chrome locale e correzione «La logica delle frecce va rafforzata». Il problema riscontrato riguarda riquadri sfalsati, curvatura, ancore ed etichette non sempre leggibili.

**Risultante locale:** `MAIOS_Comunicazione_Collaborativa_Studio06.html`, 126.062 byte, SHA-256 `602d1358382f93faf89a95c2747dbb71e8b0fe817c0d582eab582ae306bb5567`, più ZIP alternativo byte-identico e screenshot di verifica. Partendo da Studio 05, conserva `ccm.document.v1` e le funzioni di lavoro ed esportazione. Auto-routing confronta lati, ostacoli, percorso, etichette e spazio; badge etichette indipendenti, trascinabili e a capo; centro freccia per modificare curva mantenendo i nodi collegati; modalità auto/dritto/angoli/curva e ripristino automatico. Screenshot di partenza resta prova dell'uso dell'operatore della versione precedente, non prova del nuovo risultato.

**Prova:** JavaScript sintatticamente valido, sei configurazioni geometriche su dodici frecce senza attraversamento delle forme e senza badge sopra le forme nei casi esercitati, drag/reopen di percorso e label, selettore/ripristino, Grafite e privacy export, scena sintetica 40 relazioni renderizzata senza errore. [Guida](GUIDE.md#12-novembre-2026--studio-06-relazione-percorso-ed-etichetta-non-coincidono) aggiornata con meccanismo e limiti.

**Stato:** LOCAL_STUDIO06_BUILT / AUTO_ROUTING_AND_LABEL_UX_BROWSER_CHECKED / SAVE_REOPEN_CONFIRMED_IN_HARNESS / PUBLIC_RUNTIME_UNCHANGED / OPERATOR_REVIEW_PENDING / FILE_URL_AND_TOUCH_NOT_VERIFIED / CROSS_CASE_ASSIMILATION_UNKNOWN.


## 12 novembre — Studio 05: intervento UX sull'HTML locale

**File consegnabile:** `MAIOS_Comunicazione_Collaborativa_Studio05.html`, 114.556 byte, SHA-256 `5e496e0031de67670fdedc308781847c3a8503b90890b369f805be405e4082c4`; ZIP di ripiego locale con HTML identico. Il download nell'interfaccia dell'operatore non è verificato. Non installato in runtime K-UX-AI.

**Differenze implementate:** pannelli che non occludono il canvas sul desktop; vista di lettura lineare e modificabile su mobile senza duplicare il modello; canvas con zoom/scroll disponibile; mini editor ridotti grazie a proprietà secondarie collassabili; segnalazione dell'overflow di testo e nota iniziale più leggibile; stato «download richiesto» anziché falsa conferma; copia pubblica di sola lettura senza note in JSON **né** nella proiezione DOM; pannello mobile esplicito; rispetto del focus/inert quando chiuso.

**Prova:** 35/35 test principali + 10/10 regressioni mirate Playwright/Chromium `set_content`, incluse frecce, quattro temi, stampa preparata, HTML scaricato e ricaricato, privacy pubblica e mobile. Errori iniziali corretti e riesercitati. Source HTML autonomo e ZIP creati nel container; nessun deploy, release, merge, test file://, dispositivo fisico o PDF effettivo. [Guida](GUIDE.md#12-novembre-2026--studio-05-lo-spazio-di-lavoro-non-è-lo-schermo-del-pannello) custodisce il metodo e la distinzione sulle proiezioni private.

**Stato:** LOCAL_STUDIO05_BUILT / 45_OF_45_BROWSER_CHECKS_PASS / PUBLIC_DOM_PRIVACY_REGRESSION_FIXED / USER_DOWNLOAD_AND_UX_TRIAL_PENDING / KUX_PUBLIC_RUNTIME_UNCHANGED / CROSS_CASE_ASSIMILATION_UNKNOWN.

## 11 novembre — Studio 04: UI coerente e mini editor riposizionabili

**Artefatto locale:** `MAIOS_Comunicazione_Collaborativa_Studio04.html`, 101.419 byte, SHA-256 `579c7f2ee7891b34eb60b7ef3e749ebe8cd373a71d3b76acbda70014f3c25a32`. Tema diffuso nell'area esterna, toolbar, controlli, pannelli, dialoghi e mini editor per tutti e quattro i preset. Mini editor spostabile dalla testata, ridimensionabile dall'angolo, con geometria salvata nel file, riuso e comando «↩ Vicino». Il pulsante Copia pubblica continua a eliminare note e libreria; ciò non cifra il file né verifica i contenuti condivisi.

**Esercizio:** nuova suite browser Chromium `set_content` su palette, spostamento, resize, riuso, reset, save/reopen e privato/pubblico; 16/16 test di regressione Studio 03 verdi; zero errori JS osservati. Apertura diretta `file://` bloccata dal runner, controllo sul desktop/touch dell'operatore non eseguito. [Guida](GUIDE.md#11-novembre-2026--studio-04-mini-editor-mobili-e-tema-sullintero-ambiente) aggiornata con metodo e confini della prova.

**Stato:** LOCAL_STUDIO04_BUILT / CROSS_THEME_UI_VERIFIED / MINI_EDITOR_DRAG_RESIZE_VERIFIED / HTML_ROUNDTRIP_VERIFIED / REGRESSION_16_OF_16 / PUBLIC_RUNTIME_UNCHANGED / USER_BROWSER_EXERCISE_OPEN.

## 11 novembre — Studio 03, HTML avanzato locale e apprendimento

**Risultante:** `MAIOS_Comunicazione_Collaborativa_Studio03.html` costruito come file autonomo di 92.537 byte (SHA-256 `f00442c79ada3433a05f417c046af5d0f4fbfbdc81bed15298037416f869ebd6`). Estende Studio 02 con snap magnetico e guide, frecce su punti medi dei lati e maniglia centrale, mini editor vicino a riquadro/freccia/scheda, strumenti solo su comando (dock destra, sinistra, sopra, sotto, flottante), note mobili private, forme circle/oval/pill, collasso con segnaposto numerato, approfondimento live e pagina separata nel PDF, layout nelle sezioni, esportazione di una copia pubblica che pulisce **sia il JSON sia il DOM proiettato**.

**Esercizio locale:** 16/16 controlli funzionali + 6/6 approfondimenti Playwright/Chromium via `set_content`. Risultati verificati: selezione non apre automaticamente inspector; doppio clic apre mini editor; triplo clic attraversa i livelli; magnetismo osservato; freccia agganciata a metà lato e spostabile dal centro; note escluse in Presenta e nell'HTML pubblico; approfondimento produce foglio aggiuntivo nella preparazione della stampa; export HTML e riapertura preservano forma, testo e note; interfaccia e mini editor raggiungibili a 390 px. Zero errori JavaScript pagina osservati nel test principale. **Non verificati** apertura diretta `file://`, touch su dispositivi fisici, PDF finale e comprensione reale dell'interlocutore.

La [guida](GUIDE.md#11-novembre-2026--studio-03-mini-editor-magnetismo-e-continuità-tra-dom-e-documento) conserva i meccanismi. Il sorgente del prototipo è un artefatto della chat, non un file del repository pubblico. Nessun aggiornamento di `src/`, demo, release o sito derivato da questo commit.

**Stato:** STUDIO03_LOCAL_HTML_BUILT / CHROMIUM_TESTS_22_OF_22 / PRIVATE_PUBLIC_EXPORT_SEPARATED / COMPETENCE_SOURCE_LEARNING_RETURNED / RUNTIME_NOT_INTEGRATED / USER_BROWSER_TRIAL_PENDING / CROSS_CASE_ASSIMILATION_UNKNOWN.

## 11 novembre — Studio 02, secondo esercizio locale

L'operatore ha scelto come risultante una pagina che rimanga visivamente il lavoro stesso, con editor contestuali richiamati su clic e strumenti dalla rotellina a destra; triplo clic per il livello sottostante quando vi è sovrapposizione, oppure per le proprietà visive, più alternativa esplicita dall'elenco Livelli. Ha chiesto frecce con estremi trascinabili, proprietà specifiche, quattro temi, preset e layout/sezioni drag-and-drop, mantenendo l'HTML entro circa 2 MB.

**Artefatto locale esercitato:** `MAIOS_Comunicazione_Collaborativa_Studio02.html`, SHA-256 `1023ca424ead3b10d49541d895ee2ba6af006e32ba27aa8781cf914970fa085c`, 66.438 byte. Modello `ccm.document.v1` compatibile con il precedente; nuova superficie HTML/CSS/JS autonoma. 11/11 scenari Playwright + prove specifiche su trascinamento di sezione con contenuto, immagine importata/compressa e riaperta, fogli di stampa preparati. La [guida](GUIDE.md#11-novembre-2026--studio-02-superficie-libera-strumenti-situati-e-diagrammi-manipolabili) conserva differenze e meccanismi.

**Correzioni riusabili nello stesso movimento:** mantenere il DOM del referente attraverso il triplo clic; evitare duplicazione degli handler su canvas persistente; renderizzare sopra ai nodi gli handle della freccia solo quando selezionata; verificare gli stili SVG computed e non solo i loro attributi. Le sezioni trasportano i membri tramite `containerId`; le estremità non collegate della freccia restano punti liberi reali. Il sapere di progetto rimane in questa competenza; i metodi generali di Interaction Quality e Code Medium Construction restano owner complementari senza copia obbligatoria.

**Stato:** LOCAL_STUDIO02_BUILT / BROWSER_EXERCISE_11_OF_11 / HTML_EXPORT_REOPEN_OBSERVED / PUBLIC_KERNEL_RUNTIME_UNCHANGED / OPERATOR_TRIAL_AWAITED / DIRECT_FILE_URL_AND_TOUCH_NOT_VERIFIED / CROSS_CONTEXT_ASSIMILATION_UNKNOWN.


## 11 novembre — esercizio locale del medium neutro

È stato costruito e verificato nel ricevente ChatGPT un HTML autonomo, con modello dati incorporato, tre schede iniziali, editing strutturale/testuale, collegamenti etichettati, drag/resize, libreria, immagini, note, presentazione, export HTML/JSON, copia pubblica e preparazione dei fogli per la stampa. La prova Playwright ha coperto andata/ritorno dell'HTML e alcuni gesti reali sul DOM. File locale: `MAIOS_Comunicazione_Collaborativa_Prototipo.html`; SHA-256 `f7d7761ef5876c85a47309b882b593c1a91c7cc4c37c1893d20e8c4df49b59c7`, 42.639 byte. **Non è un file pubblicato o installato in questo repository.**

Correzione riusabile: il rerender su un `pointerup` privo di movimento sopprimeva il successivo doppio clic sul medesimo elemento; ora il nodo rimane e la maniglia viene aggiunta senza ricrearlo, mentre le trasformazioni effettive vengono salvate e renderizzate. [La guida](GUIDE.md#11-novembre-2026--primo-esercizio-del-medium-html-neutro) conserva ragione e metodo.

**Stato:** SOURCE_COMPETENCE_FORMED / LOCAL_BROWSER_EXERCISE_OBSERVED / EXPORTED_HTML_REHYDRATION_TESTED / PUBLIC_RUNTIME_NOT_CHANGED / CROSS_DEVICE_AND_FILE_OPEN_NOT_VERIFIED / LATER_ASSIMILATION_UNKNOWN.

## Determinazione dell'operatore

L'esperienza con un HTML modificabile usato per la presentazione MAIOS × Schnell apre uno strumento per builder AI, aziende e operatori che devono comunicare oggetti di lavoro e prodotti fra persone e AI. La persona modifica il documento, lo salva, lo presenta o lo trasferisce; l'AI può comprenderne la struttura e contribuire alla formazione dei contenuti. Il nucleo deve generalizzarsi oltre le presentazioni: content web, progettazione, gestione di sistemi complessi e altri casi che emergano.

**Prima origine tecnica:** file allegato alla conversazione del 2026-11-11 `MAIOS_Schnell_Presentazione_modificata(1).html`, contenente un HTML completo con introduzione e cinque schede, campi `contenteditable`, appunti, vista Presenta, stampa e download HTML. Resta un artefatto privato dell'operatore; qui sono conservati metodo e osservazioni, non testo e note aziendali.

## Formazione eseguita nella sorgente

- [SKILL](SKILL.md): competenza specializzata, proprietaria del metodo degli artefatti comunicativi condivisi.
- [GUIDE](GUIDE.md): meccanismi del primo caso, distinzione fra fonte/forma/relazioni, architettura candidata, condizioni per esercitare.
- Raccordi d'ingresso con K-UX-AI e adapter LLM.

Il caso indica un uso pratico riferito dall'operatore, non l'esistenza di un editor universale integrato in K-UX-AI. Le capacità future non si considerano esercitate per il solo fatto che la competenza le descrive.

## Primo seguito materiale

Costruire e testare un HTML neutro autosufficiente a partire dal meccanismo esistente, preservando semplicità, modifica, salvataggio, riapertura e presentazione; introdurre editing di struttura e relazione in modo incrementale. Usare il medesimo artefatto per passaggi AI/umano con identità della revisione, prima di scegliere connettori o hosting.

**Confini:** nessuna modifica al file Schnell, al prodotto JS, al sito, alla release, a credenziali, controller, mailbox o automazioni. Repository source ≠ editor installato ≠ esercizio sul nuovo prototipo ≠ assimilazione in altri host.
