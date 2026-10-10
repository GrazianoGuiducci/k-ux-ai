# K-UX-AI v5.4 — Tour focale, preparazione e strumenti

10 ottobre 2026 · risultato candidato nel solo branch di lavoro `work/ux-ai-ui-library-20261008` · dominio Nautico dimostrativo.

## Fonte e differenza materiale

Le due schermate fornite dall'operatore sulla v5.3 segnalano che il tour non evidenzia in modo sufficiente ciò che spiega, il pannello «Prepara il campo» è una giustapposizione di titolo, contesti e CTA distante, e toolbar/Strumenti sono poco coerenti nella gerarchia. La richiesta seleziona un lavoro di UX/medium, non installazione AI, adattamento del controller Nautico o rilascio pubblico.

## Composizione esercitata

- **Home «Prepara il campo»**: un unico contenitore con intestazione/quesito di contesto, i cinque ambienti e un footer con selezione corrente e **Entra nel campo**. Sono i controlli e lo stato per-contesto della v5.3, non copie.
- **Tour con spotlight**: regioni esterne al target velate; il target rimane visibile e distinguibile senza che il pannello guida vi si sovrapponga. Il testo dello step distingue ambito, quando è utile, **cosa l'operatore può fare** e conseguenza. Spiega selezione e drag delle tessere in Home e l'effetto di Entra; pulsanti Indietro/Avanti/chiudi, Escape e ritorno al chiamante. X con centratura corretta. Gli elementi della pagina fuori focus restano percepibili ma attenuati; il tour non dichiara lavoro realmente eseguito.
- **Barra del campo**: gruppi Vista, Composizione, Azione e Aiuto con gerarchia e spaziatura coerenti. `Strumenti` raggruppa Disposizione, Riorganizza e mantieni, Comprendi e intervieni; i gestori Ricomponi, Mantieni focus, +Attività, Libero/Auto/2/3/4, Perché qui e Informazioni sono gli stessi, senza doppia autorità.
- **Responsive**: menu Strumenti sotto il complesso della testata, dentro il viewport stretto; tour non copre il target su 390/768/1200/1680 e nello zoom CSS esercitato fino al 150%, mentre i limiti dell'ambiente di test non autorizzano una conformità generale. Reduced-motion resta equivalente sul piano dello stato.

## Sorgente e prova

[HTML autonomo](15-griglia-focus-tour-tools.html) · [ricevuta](EVIDENCE_FOCUS_TOUR_V54_20261010.json). Prodotto dalla baseline [v5.3](14-griglia-navigatore-contestuale.html) con `build_v54.py` hash-guarded incluso nel pacchetto ZIP consegnato all'operatore; il bundle HTML è autosufficiente, la base storica resta parzialmente monolitica e non rivendica un refactor integrale.

HTML esatto SHA-256 `1a9ef7846a18cff981af61f47cd8ff50cfee3c102fb146a69d44c56726395ff2`, Git blob `a431c48c310f904f954804a9e6504c986b602d84`, 349260 byte. Il builder è stato rieseguito nel turno di rientro e l'output corrisponde byte per byte al deliverable. `node --check` supera tre script.

Prove Chromium/Playwright su file esatto: 80/80 UI/tour/toolbar + 68/68 viewport/zoom + regressioni v5.3 9/9, 84/84, 33/33, 60/60 = **334/334 controlli correlati**, zero errori JavaScript osservati nei percorsi. I log/test nel pacchetto restano prove di questo candidato, non di Edge sul PC, touch, screen reader, utenti indipendenti, effettiva persistenza browser, Nautico live, assistente/Section Kernel, o rilascio. Pacchetto ZIP SHA-256 `7c184a5fb513306cf76714fec059c07895857e66579a65f01868851e04ab4820`.

La scelta di design mantiene il materiale: la UI spiega e compone il campo; `contesto rappresentato != dato-source mutato != effetto autorizzato`. L'apprendimento riusabile del tour con target visibile e del riuso dei gestori torna a Code Medium Construction e alla pertinente Interaction Quality già esistente, senza duplicare un nuovo owner. Nessun merge, deploy, release, cambiamento del `main` K-UX-AI o modifica a Kernel Nautico/MAIOS.

**Prossima osservazione:** Home a 1680 e 390, i tre passi del tour, popup Strumenti, test Edge con zoom e Home→campo senza perdita delle schede del contesto.
