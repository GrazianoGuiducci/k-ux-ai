# Collaborative Communication Medium — CURRENT

**Data:** 2026-11-11 · Europe/Rome  
**Versione:** 0.1.0-candidate  
**Owner:** K-UX-AI / competences/ux-ai/collaborative-communication-medium  
**Stato iniziale (prima dell'esercizio locale):** SOURCE_COMPETENCE_FORMED / RUNTIME_NOT_YET_BUILT / GENERALIZATION_PENDING

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
