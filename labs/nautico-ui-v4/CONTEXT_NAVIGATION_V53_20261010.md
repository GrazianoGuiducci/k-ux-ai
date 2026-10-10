# K-UX-AI v5.3 — Navigatore contestuale e continuità del campo
10 ottobre 2026. Owner `GrazianoGuiducci/k-ux-ai`; branch `work/ux-ai-ui-library-20261008`. Laboratorio con fonti dimostrative Nautico, **non** sistema aziendale operativo.

## Differenza dell'operatore
Nella v5.2 l'etichetta Contesto poteva mostrare «A bordo» mentre il canvas conteneva schede Fornitori o Assistenza. Il selettore riscriveva il contesto della scheda principale anziché proiettare l'ambiente scelto. Il menu Azione sembrava governare il campo e la tessera principale nella Home non era necessariamente già preparata per il canvas.

## Nuovo comportamento
- La **tessera principale della Home è sempre una delle attività selezionate** nel piano del contesto, dopo drag, cambio ambiente e recupero best-effort del piano. Selezione e ingresso nel lavoro restano effetti distinti.
- Il **navigatore contestuale** sostituisce visivamente il precedente `contextSelect` (conservato come mirror tecnico, non secondo owner). Presenta cinque ambienti, caso relativo e conteggio delle attività preparate o aperte; offre menu operabile con puntatore e tastiera, Escape e rientro del focus.
- Il contesto selezionato governa schede, avatar, focus e disposizione proiettati nel canvas. Il codice non modifica `p.context` di un pannello appartenente ad altro ambiente. Schede non appartenenti al contesto corrente sono conservate ma nascoste/inerti.
- Il menu **Azione nel contesto** modifica il focus fra attività visibili di quell'ambiente. Disposizione e blocco del focus sono recuperati per contesto; entrare in un campo già avviato non importa il layout di un altro ambiente.
- Il readback locale distingue `visibleInField` e `panel retained`; non trasforma una scheda salvata in una scheda visibile né attribuisce capacità Nautico a una proiezione di UI.

## Implementazione
[HTML standalone 14](14-griglia-navigatore-contestuale.html) derivato dalla [baseline v5.2](13-griglia-contesti-tour.html) con patch sorgente e builder che verifica l'hash della baseline. Builder, baseline, sei script di prova, screenshot e ricevuta tecnica sono nel pacchetto ZIP consegnato all'operatore. Il codice resta un laboratorio HTML ancora parzialmente monolitico: non affermare un refactor completo, un nuovo controller di dominio o un nuovo provider AI.

L'attuale UI opera con scenari dimostrativi; nessuna fonte Nautico vera, sincronizzazione filesystem PC/Codex, Section Kernel installato, modello/LLM collegato, autorizzazione o effetto esterno è stata acquisita. **Contesto rappresentato ≠ fonte mutata ≠ effetto autorizzato.**

## Evidenza e limiti
[Receipt](EVIDENCE_CONTEXT_NAV_V53_20261010.json). HTML SHA256 `bba2db6f1c395733b429b73db9606a5bbbe8aa5daaa17d06452ef6f7ae9b8ffd`; Git blob `55812cc3033f80d7a9357c85f5de68200eaff7e4`; 335858 byte.

Sei suite Playwright/Chromium `page.set_content`, **42/42 + 84/84 + 60/60 + 12/12 + 33/33 + 9/9 = 240/240 controlli correlati**. Nessun JS page error osservato. Coperti desktop/mobile, contesti multipli e bozze, focus/assetti separati, assistant docked, popup tastiera e zoom CSS fino 200%, re-entry Home. Il riavvio usa archivio `localStorage` simulato, non è prova Edge `file://` reale, continuità persistente su PC o capacità AI. Non testati touch/AT fisici né utenti indipendenti.

## Rientro
Primo esercizio in Edge: preparare Fornitori e A bordo in modo diverso, entrare in Fornitori, scrivere una bozza, cambiare ad A bordo, poi tornare a Fornitori e verificare sorgente, avatar, schede, bozza e layout. Ricaricare separatamente per testare persistenza reale. Le fonti e il kernel Nautico rimangono owner-native e non sono modificati da questa correzione. Nessun merge, deploy o rilascio.
