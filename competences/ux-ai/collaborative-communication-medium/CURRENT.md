# Collaborative Communication Medium — CURRENT

**Data:** 2026-11-11 · Europe/Rome  
**Versione:** 0.1.0-candidate  
**Owner:** K-UX-AI / competences/ux-ai/collaborative-communication-medium  
**Stato iniziale (prima dell'esercizio locale):** SOURCE_COMPETENCE_FORMED / RUNTIME_NOT_YET_BUILT / GENERALIZATION_PENDING

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
