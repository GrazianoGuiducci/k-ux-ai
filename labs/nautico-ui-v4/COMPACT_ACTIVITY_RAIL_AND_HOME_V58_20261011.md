# K-UX-AI v5.8 — barra Attività essenziale e ingresso al Kernel UX-AI

11 ottobre 2026 · candidato nel solo ramo `work/ux-ai-ui-library-20261008`.

## Sorgente e scelta

L'operatore osserva in Edge la candidata v5.7 e chiede di usare meno altezza per i controlli della sidebar Attività, ridurre la visibilità di informazioni già palesi (`10 accessi · 4 nel campo`) e sostituire l'introduzione della Home con una spiegazione di **Kernel UX-AI per l'interazione in Sistemi Intelligenti**.

K-UX-AI rimane il medium neutrale per le interfacce di kernel distinti: la Griglia è il prototipo sintetico che esercita alcune sue funzioni. Il Kernel Nautico possiede il primo dominio di applicazione. Un controllo grafico non autorizza nuove operazioni o dati del dominio.

## Intervento concreto

- I due pulsanti `#railVisibility` e `#kuxRailToggle` entrano in **una sola riga compatta** `.kux-rail-head`, affiancati in vista icone; quando la barra è espansa, anche la scritta `ATTIVITÀ` occupa la stessa riga. Le due azioni rimangono semanticamente distinte: nascondere la barra e cambiare proiezione icone/anteprime. Etichette accessibili e titoli restano presenti.
- Il nodo e il testo di `#activityCount` sono ritirati: non occupano spazio verticale. Il campo già mostra le schede attive e il footer ne porta il conteggio; la barra mantiene il nome del contesto nell'etichetta accessibile.
- Il piccolo sottotitolo di contesto sotto `ATTIVITÀ`, aggiunto ad ogni rendering, non viene più duplicato; la fonte del contesto resta il selettore nella toolbar superiore.
- Dal meccanismo della v5.7 si conservano **nascosta → icone temporanee al bordo → icone fissate → anteprime espanse**. Passare a nascosta/icone compatte riconcilia anche la geometria della sidebar prima di esporre il nuovo stato; il richiamo dal bordo non apre automaticamente le anteprime. La modalità expand continua a conservare larghezza regolabile.
- La Home porta il titolo `Kernel UX-AI`, il sottotitolo `per l’interazione in Sistemi Intelligenti.` e le tre relazioni testuali fornite dall'operatore: ambiti di gestione dei sistemi agentici; composizione contestuale con apprendimento, memoria, continuità, assistenza e risorse; ingresso e risposta situata agli eventi. Mantiene il link al Manifesto. Una breve nota distingue la demo locale dalle capacità integrate: il codice corrente non riceve un modello AI vero né possiede account o autorizzazioni Nautico.

L'ottimizzazione ha riutilizzato `mountSidebar` e `setActivitiesMode` senza creare un secondo controller dell'espansione. Il cambio non trasferisce prove dalla candidata v5.7.

## Identità del nuovo oggetto e prova

- Base invariata: [v5.7](19-griglia-rail-free-v57.html), SHA-256 `e733a306b85f2ac3abefe20fa6801aa73b2b178e7c108b40d05bb07c5021db2d`.
- Candidate: [v5.8](20-griglia-rail-home-v58.html), SHA-256 **`799727c0283c61829796f20d1c4b45e652c3b2dd8d6056fe5577b0460ee3d9ad`**. Git blob da qualificare nella destinazione del commit.
- Builder deterministico `tools/build_nautico_v58.py` con baseline/risultante SHA-guarded; `--check` verifica i byte già generati.
- Nuove verifiche `tests/qa_nautico_v58.py`: [receipt 159/159](EVIDENCE_RAIL_HOME_V58_20261011.json), quattro viewport e un controllo aggiuntivo di tastiera/contesto.
- Compatibilità di comportamenti v5.7 riesercitata sul **nuovo file esatto** con `tests/qa_nautico_v58_compat.py`: [receipt 126/126](EVIDENCE_COMPATIBILITY_V58_20261011.json), Home/Canvas tour, contestualizzazione, due schede, fullscreen, anteprime al bordo e assenza di sovrapposizioni osservate nei percorsi.
- Due suite correlate, non 285 prove indipendenti; zero JavaScript `pageerror` negli esercizi. Esecuzione Chromium Playwright usando `page.set_content` sui byte del candidato, non Edge installato, sito o trasporto AI reale.

## Confini e seguito

La sintesi generale della Home descrive la direzione e il sistema integrato. Il prototipo non esercita apprendimento autonomo, memoria oltre allo stato locale o capacità di agire su sistemi aziendali. La nota qualificante resta visibile.

Un futuro aggiornamento Nautico/sito ha già i propri owner e preparazioni Codex: il presente cambiamento è del medium K-UX-AI, non del bridge nautico o della distribuzione MAIOS. Non sono stati eseguiti merge, release, deploy, modifiche di account, nuovi servizi o contatti esterni.

**Prossima osservazione:** l'operatore può aprire la v5.8 in Edge per verificare leggibilità del testo introduttivo e uso dei due controlli su sidebar compatta, espansa e richiamo al bordo. In presenza di nuove differenze il receiver corregge il primo owner responsabile; se sufficienti, la UI può fermarsi come candidata di sviluppo.
