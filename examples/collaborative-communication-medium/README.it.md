# AI Collaboration Studio — anteprima pubblica

## Download attuale — MetaCanvas Studio 20 (13 novembre 2026)

**[Scarica l'editor autonomo](AI_Collaboration_Studio.html)** · [Visualizza il file su GitHub](https://github.com/GrazianoGuiducci/k-ux-ai/blob/main/examples/collaborative-communication-medium/AI_Collaboration_Studio.html) · 272.490 byte · SHA-256 `c8c1be74c7d9b91d99b0c7888c40cee387579ca26f3079d0fa44ea81f1817a19`.

MetaCanvas è uno **strumento HTML autonomo** per costruire e modificare diagrammi, schede, presentazioni e idee condivise con persone o sistemi AI. Contiene quattro esempi neutri e non richiede installazione, server o servizio AI incorporato. Apri l'HTML in un browser moderno, lavora nel documento e usa **Salva lavoro** per scaricare una nuova copia; non sovrascrive automaticamente il file originale.

**Novità Studio 20:** superfici Standard/Flat più compatte e responsive; editor e strumenti spostabili; riordino delle schede; frecce con etichette; template salvabili e inserimento annullabile. **Dati per AI** permette di scegliere documento o singola scheda, con appunti privati e raccolte personali esclusi per impostazione predefinita. **Importa JSON / HTML** mostra le schede nuove, cambiate e mancanti prima di integrare selettivamente (con Annulla) oppure sostituire l'intero documento dopo conferma; l'integrazione selettiva conserva le note private locali. **Recupero locale** è una funzione facoltativa, inizialmente disattivata: non è sincronizzazione né backup nel cloud. Le miniature rappresentano meglio i percorsi delle frecce.

**Da sapere:** verifica i testi e gli asset prima di condividere. Il filtro non può riconoscere automaticamente informazioni riservate scritte nel testo comune. L'importazione legge soltanto il modello dati, non esegue codice ricevuto e rifiuta immagini remote; non equivale a una certificazione di sicurezza. Il recupero è stato provato con archiviazione simulata, non è garantito su tutte le aperture `file://`.

Le sezioni **storiche** sottostanti descrivono le prime versioni e non sostituiscono il funzionamento attuale di Studio 20.

[Contratto del documento](DOCUMENT_CONTRACT.md) · [Consegna alla futura pagina MAIOS.it](MAIOS_RESOURCE_TOOL_HANDOFF.md).


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

## Studio 14 — Presenta, Flat, Strumenti e modifica

Questa versione incorpora quattro correzioni richieste dall'operatore:

1. **Presenta**: ripristinato il canvas visibile in modalità a schermo intero; il problema derivava dalla griglia editor con sidebar nascosta che azzerava la colonna del canvas.
2. **Strumenti**: ridimensionamento dei pannelli anche con il loro contenuto scorrevole; nella posizione Finestra mobile l'angolo in basso a destra modifica larghezza e altezza. Restano i comandi +/- e i dock laterali/superiore/inferiore.
3. **Flat**: un pulsante in testata (e in Strumenti) cambia modalità di lavoro, allarga l'area di lettura e riduce cornici e margini. Su schermi ampi la lettura può usare due colonne; il canvas grafico conserva le coordinate.
4. **Modifica**: quando un testo o il mini editor è attivo appare un menu compatto **OK · Indietro · Avanti**. OK conferma ed esce; Indietro e Avanti gestiscono i passi della cronologia. ESC continua a chiudere la modifica.

**Uso:** apri l'HTML, usa **Flat** per passare al layout più ampio, **Presenta** per verificare le schede, **Strumenti** per ridimensionare il pannello; fai doppio clic su un testo per il mini editor. I controlli e le preferenze permangono nel file HTML salvato. Non è previsto un server o un LLM incorporato.

## Studio 15 — Template personali, posizionamento e Annulla

In **Strumenti → Template agentici**, ogni modello ha tre comandi:
- **Sostituisci** rimpiazza la scheda attiva, dopo conferma; l’originale si recupera con **↶ Annulla**.
- **↑ Sopra** aggiunge una scheda immediatamente prima della corrente.
- **↓ Sotto** aggiunge una scheda immediatamente dopo la corrente.

Il percorso completo da cinque schede usa gli stessi tre comandi e costituisce un’unica azione annullabile. La sezione include **Annulla** e **Ripristina**.

**I miei template:** dopo aver personalizzato una scheda seleziona **☆ Salva questa scheda come template**, assegnale un nome e riutilizzala con gli stessi tre comandi. I template personali vengono inclusi nel file di lavoro quando premi **Salva lavoro**. Per portarli in un altro progetto usa **↓ Esporta raccolta JSON** e, nell’altro documento MetaCanvas, **↑ Importa raccolta JSON**. L'importazione aggiunge i template, non sostituisce le schede e può essere annullata.

I template salvati escludono appunti del relatore ed elementi marcati come privati; **controlla comunque il testo dei riquadri e gli approfondimenti** prima di condividere una raccolta. La **Copia pubblica** non contiene i template personali né le rappresentazioni HTML generate della loro lista.

[Formato della raccolta](TEMPLATE_COLLECTION.md) · [Contratto del documento](DOCUMENT_CONTRACT.md).

## Licenza e proprietà

**Mozilla Public License 2.0 (MPL-2.0)**, *soltanto per i file di questo strumento*. Chiunque può usare, modificare, distribuire e commercializzare il software nel rispetto della licenza. Chi distribuisce modifiche ai file coperti deve rendere disponibile il relativo sorgente secondo la MPL. Il copyright sul codice originale resta a **Graziano Guiducci (2026)**; i nuovi autori conservano i diritti sulle proprie modifiche. Nomi commerciali, marchi e loghi non sono concessi dalla MPL.

[Leggi la licenza](LICENSE) · [Domande frequenti Mozilla](https://www.mozilla.org/en-US/MPL/2.0/FAQ/) · [Contratto del documento](DOCUMENT_CONTRACT.md).

Questa licenza **non modifica** quella del kernel K-UX-AI, delle competenze o degli altri esempi della repository.

## Stato e limiti

Anteprima pubblica autonoma, non un modulo installato nel runtime K-UX-AI né una demo online MAIOS.it. L’interfaccia è in italiano; la traduzione inglese completa non è ancora disponibile. Diagrams molto densi, stampa/PDF, accessibilità completa e browser fisici diversi richiedono ulteriori verifiche. Non inserire segreti o dati personali in file destinati a terzi.
