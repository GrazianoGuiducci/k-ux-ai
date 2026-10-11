# K-UX-AI v5.5 — interazione situata del medium riusabile

11 ottobre 2026 · candidato nel solo branch `work/ux-ai-ui-library-20261008`.

## Fonte e distinzione

Le tre schermate dell'operatore sulla v5.4.1 mostrano divisore dopo Ricomponi spostato, chat dock sinistro che copre il contesto di lavoro, e modulo di contributo ancora rappresentato come forma obbligatoria. L'operatore richiede una Home più esplicativa, tre passaggi del tour riformulati, trascinamento card/chat con entrata e uscita da fullscreen, accessi Attività visibili e una chat localizzata per ogni scheda.

K-UX-AI resta **il medium neutrale** che può essere composto con kernel diversi; questa Griglia è soltanto una delle sue forme possibili. Kernel Nautico è il primo dominio ricevente, proprietario di oggetti, fonti, lifecycle e azioni. Il demo K-UX-AI usa dieci intenti sintetici: non sono le dieci entity public-target di Nautico. L'integrazione e la versione del sito sono movimenti distinti di Codex e del site owner.

## Risultato nell'HTML candidato

- **Home**: sintesi della ricerca in UX-AI evolutiva, impiego nei sistemi agentici in azienda/professioni/ricerca, profondità contestuale e link al Manifesto. Distingue la demo locale dalle possibili capacità future con kernel/provider veri. Conserva il campo in una prima schermata desktop, dove il frame lo consente.
- **Tour**: 1. contesto come luogo/argomento/situazione; 2. attività come accessi agli strumenti e alle azioni, preparabili anche dopo l'ingresso; 3. canvas come campo riconfigurabile in corso d'opera. Conserva ambito/quando/gesto/conseguenza e spotlight che non copre il target.
- **Ricomponi**: il divisore delle medie usa il settore reale della griglia, non la geometria provvisoria delle card durante la transizione. Dopo la ricomposizione viene riallineato quando il layout si assesta.
- **Drag e fullscreen**: intestazione della scheda o chat trascinata verso il bordo superiore → fullscreen con indizio di drop; trascinata verso il basso da fullscreen → ripristino. Il click non diventa drag senza soglia; reduced motion preserva l'effetto finale.
- **Chat dock sinistro**: misura dalla topbar, dalla fascia Attività e dallo spazio del canvas; non copre gli accessi e non forza una seconda sorgente di stato. In mobile il componente mantiene il proprio adattamento.
- **Modulo globale**: opzionale e reversibile, mantiene la bozza quando viene nascosto; lo schema attuale è sperimentale, non fissa la futura forma del contributo.
- **Dialogo scheda**: rende visibile la conversazione locale già esistente nelle Section Surface, distinta dalla chat generale; nessun nuovo AI provider o controller con permessi è stato installato. Gli accessi iconici si presentano come Attività, non come "avatar" nel significato per l'utente.

## Identità sorgente e riproducibilità

- Candidate: [17-griglia-situated-v55.html](17-griglia-situated-v55.html)
- SHA-256: `d5a87e294d6fea395664d258d65c9a40f4c94d190bb807177146bd7301432d1c`
- Git blob: `b84046ab5285823ba418d131bc36e56810cdc0fc`
- Baseline invariata: [v5.4.1](16-griglia-continuity-v541.html) SHA256 `7e8a35dc21bdc6940e1ad00db47fbe9327237a33c6aede5a71aaf03f7d8f9716`.
- Builder hash-guarded: `python tools/build_nautico_v55.py` produce il candidato dalla baseline; `--check` confronta i byte senza scrivere.
- QA situata: `python tests/qa_nautico_v55.py`, ricevuta [59/59](EVIDENCE_SITUATED_V55_20261011.json).
- QA di compatibilità: `python tests/qa_nautico_v55_compat.py`, ricevuta [97/97](EVIDENCE_COMPATIBILITY_V55_20261011.json).
- Chromium Playwright `page.set_content` su frame 1715/1300/768/390 nei test nuovi e 1440/390/768/1680 nella regressione, movimento normale/ridotto. Zero JS page errors osservati nei percorsi. Tre script embedded controllati con `node --check`.

Le suite sono correlate sullo stesso sorgente, non 156 dimostrazioni indipendenti. Non provano un Edge fisico, storage tra riavvii, screen reader, touch reale, Safari/Firefox, comprensione umana, né un sito o un modello AI integrato.

## Ritorno e stop

La competenza privata Code Medium Construction può apprendere dai gesti relativi al top-edge, dallo spazio riservato alla chat e dall'ancoraggio del divisore al contenitore reale; Interaction Quality del Design Kernel resta owner di interazione, comprensione e recovery. Nessun nuovo owner generico di permessi viene creato: Nautico/host governeranno azioni e dati effettivi.

La v5.5 e gli strumenti sono candidati del branch K-UX-AI. `main`, `createMedium()` pubblico, Kernel Nautico, maios.it, provider, account e pubblicazione restano invariati in questo movimento.
