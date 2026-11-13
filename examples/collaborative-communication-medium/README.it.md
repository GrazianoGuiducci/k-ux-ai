# AI Collaboration Studio — anteprima pubblica

**Uno strumento HTML autonomo per collaborare con l’AI e presentare le proprie idee.**

1. Apri `AI_Collaboration_Studio.html` in un browser aggiornato.
2. Seleziona una delle quattro schede dimostrative oppure una pagina vuota.
3. Modifica testi, forme, frecce e appunti; puoi passare da vista di lettura a presentazione.
4. Premi **Salva lavoro** e verifica il file HTML scaricato.
5. Per collaborare con un modello linguistico allega **il tuo file HTML** e chiedi: «Comprendi le schede e le relazioni, conserva i miei concetti, distingui fatti e proposte, restituisci l’HTML modificabile».
6. Per condividerlo con un pubblico, usa **Copia pubblica** dopo aver controllato i contenuti: rimuove appunti privati e libreria, ma il sorgente HTML resta ispezionabile.

Il documento contiene il modello strutturato in `<script id="ccm-data" type="application/json">` (schema `ccm.document.v1`). Le frecce fanno riferimento agli ID dei nodi. Il file non incorpora un LLM, non sincronizza dati e non richiede un server.

## MetaCanvas 0.1.1 — il ritorno dall’AI

La stessa sorgente può tornare da un LLM come **JSON modificato**, senza sostituire manualmente il codice dell'editor.

1. Apri **Strumenti → Salva ed esporta → Dati per AI** e scarica il JSON.
2. Allegalo al modello e chiedi di rispettare `ccm.document.v1`, gli ID delle schede e i riferimenti `from`/`to` delle frecce.
3. Ricevi un JSON corretto, oppure un **HTML MetaCanvas completo**; nell'editor già aperto seleziona **Importa JSON / HTML**.
4. Verifica titolo e numero di schede nel messaggio di conferma; dopo l'importazione puoi usare **Annulla** per ripristinare il documento precedente. Salva il nuovo lavoro in un HTML autonomo.

L'importazione legge **solo il modello JSON**: non importa JavaScript, CSS o altri elementi attivi dall'HTML ricevuto. Rifiuta schema incompatibile, ID duplicati, collegamenti verso elementi inesistenti e file troppo grandi. Non unisce automaticamente due lavori: **sostituisce il documento corrente dopo conferma**. Il contenuto prodotto dall'AI va comunque controllato; non rappresenta una convalida dei fatti.

## Licenza e proprietà

**Mozilla Public License 2.0 (MPL-2.0)**, *soltanto per i file di questo strumento*. Chiunque può usare, modificare, distribuire e commercializzare il software nel rispetto della licenza. Chi distribuisce modifiche ai file coperti deve rendere disponibile il relativo sorgente secondo la MPL. Il copyright sul codice originale resta a **Graziano Guiducci (2026)**; i nuovi autori conservano i diritti sulle proprie modifiche. Nomi commerciali, marchi e loghi non sono concessi dalla MPL.

[Leggi la licenza](LICENSE) · [Domande frequenti Mozilla](https://www.mozilla.org/en-US/MPL/2.0/FAQ/) · [Contratto del documento](DOCUMENT_CONTRACT.md).

Questa licenza **non modifica** quella del kernel K-UX-AI, delle competenze o degli altri esempi della repository.

## Stato e limiti

Anteprima pubblica autonoma, non un modulo installato nel runtime K-UX-AI né una demo online MAIOS.it. L’interfaccia è in italiano; la traduzione inglese completa non è ancora disponibile. Diagrams molto densi, stampa/PDF, accessibilità completa e browser fisici diversi richiedono ulteriori verifiche. Non inserire segreti o dati personali in file destinati a terzi.
