# K-UX-AI v4.7 · Sidebar e settore delle medie
9 ottobre 2026 · candidato nel branch di sviluppo K-UX-AI · prima sorgente Nautico sintetica

## Differenza osservata dall'operatore
La v4.6 comprim(eva) le icone nella barra ridotta, offriva sia mini anteprima flottante sia anteprime interne quando la barra era estesa, e presentava due zone medie nella mappa nonostante fossero un unico settore. Con molte attività la larghezza delle schede medie non veniva sempre governata dallo spazio realmente raggiungibile.

## Contratto v4.7 esercitato
- **Barra chiusa:** 86px fissi, solo icone con nome accessibile, distanziate; hover/focus permette quickpeek, niente resize della larghezza chiusa.
- **Barra aperta:** preview impilate con sorgente e contesto demo, scroll verticale, larghezza regolabile 255–395px da puntatore e tastiera; il mini-peek degli avatar viene disattivato. L'apertura/chiusura conserva i pannelli.
- **Mappa:** Grande + **Medie affiancate** come unico settore. Internamente il punto di rilascio superiore/inferiore continua a decidere l'ordine, non un'identità separata «piccola».
- **Settore medie:** divisione regolabile 27–60%, default nuovo 44% se la preferenza non esiste; affiancamento di due schede quando la larghezza reale del settore supera circa 680px, altrimenti stack scorrevole. Con quattro schede affiancabili, la griglia usa due righe che occupano il campo.
- **Ricomposizione, chat dimostrative e Section Workspace:** dati locali e owner rimangono distinti dal layout. Nessuna AI connessa o competenza automaticamente assimilata.

## Codice e riproducibilità
[HTML v4.7](08-griglia-campo-medie.html) · [JS sorgente](source-v47/composition.js) · [CSS sorgente](source-v47/composition.css) · [ricevuta](EVIDENCE_FIELD_20261009.json). I due moduli sostituiscono quelli v4.6 nel build autonomo. Il builder completo, la baseline esatta v4.6 e i test sono conservati anche nel pacchetto ZIP consegnato all'operatore; questa directory **non** pretende che i due moduli da soli generino il monolite precedente.

Non è stato creato un nuovo controller runtime. Rimane aperta la migrazione del legacy v4.x in veri moduli di prodotto quando il receiver Nautico e l'host saranno selezionati. Non copiare il codice Atlas per simulare una integrazione: si è usato solo il suo comportamento di sidebar come riferimento.

## Orizzonte successivo — risposte con artefatti
La fonte [OpenAI, «GPT-6 e Intelligent UI per tutti» (7 ottobre 2026)](https://openai.com/it-IT/index/gpt-6-for-everyone/) descrive risposte ChatGPT con testo, immagini, grafici, componenti e interazione anche in streaming. **Non dimostra** che quelle API, componenti o provider siano disponibili nel nostro ricevente.
Se in futuro la chat generale o una sezione genera un artefatto utile, distinguere fonte/intento, owner del significato, carrier generato, renderer, provider reale, interazione/effetto autorizzato, feedback e competenza da aggiornare. Archiviare solo quando utile la relazione riusabile e l'artefatto qualificato (identità, fonte, versione, stato, ragione, receipt), senza chiamare assimilazione la sola esistenza del file.
Owner già pertinenti: Code Medium Construction (costruzione), D-ND Design Kernel (forma/interazione), Editoriali (concetto e comunicazione), Meta_Skill/UX-AI (comprensione) e Kernel Nautico (dominio). Queste sono connessioni di competenze **possibili**, non nuovi controller o integrazioni installate.

## Prova ed effetti
97/97 layout + 51/51 interazione **correlati**, Playwright/Chromium, viewport da 390 a 2050px, reduced motion e normale, zero JS page error osservati. [Ricevuta esatta](EVIDENCE_FIELD_20261009.json), HTML SHA256 `2f134374521e886c0d5ea4102972006110b716797406f49691c2d0a23b5903c7`, Git blob `08834da1c5e3edb9f40a5cce6d1d4dfb8aaff4a3`.
Non provato: Edge dell'operatore, touch fisico, assistive technology complete, AI, filesystem condiviso o Nautico reale.
Nessuna modifica al main pubblico, Nautico, MAIOS, provider, release o deploy.
