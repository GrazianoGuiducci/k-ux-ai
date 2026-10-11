# K-UX-AI v5.9 — continuità percettiva del tour, gerarchia e controllo del campo

11 ottobre 2026 · owner di questo risultato: `GrazianoGuiducci/k-ux-ai`, branch candidato `work/ux-ai-ui-library-20261008`.

## Fonte che ha formato il movimento

L'operatore ha osservato la candidata v5.8 in Edge e ha segnalato due gruppi di differenze. La guida del tour attraversava posizioni distanti a scatti, perdendo l'orientamento. Le intestazioni delle schede e alcuni dettagli del Canvas mostravano dimensioni e posizioni non abbastanza coerenti: priorità fra **Sezione, Azione, Titolo, sottotitolo, informazioni aggiuntive**, apertura/chiusura dei modi della sidebar, menu Strumenti, passaggio Home/Plancia, tre pallini dei divisori e checkbox rispetto al testo. La richiesta è una costruzione originale del medium K-UX-AI, non una modifica diretta del runtime Nautico o del sito.

K-UX-AI detiene il medium riusabile fra kernel; questa Griglia esercita una possibile grammatica di interazione con fonti sintetiche Nautico. Il dominio Nautico e il site host restano proprietari di dati reali, esecuzione, account e integrazione.

## Risultato nel codice

- **Tour come transizione riconoscibile**: target e descrizione restano collegati mentre la cornice di focus, le quattro regioni di attenuazione e il dialogo raggiungono progressivamente la posizione finale. CSS usa una durata situata di 520 ms e un'interpolazione orientata al punto d'arrivo; il contenuto del passo ha una breve entrata di 240 ms. Quando il target è fuori viewport, lo scorrimento verso di esso è graduale. Con `prefers-reduced-motion: reduce` il significato resta, la disposizione finale è immediata e non dipende dall'animazione per avanzare.
- **Intestazione leggibile senza nuova fonte di dominio**: il visuale distingue la sezione di contesto (`context.name`), l'azione scelta (`intent.verb`), il titolo concreto della funzione di questa demo, il sottotitolo collegato all'oggetto e la fonte illustrativa. La scala visiva lascia predominare il titolo, comprime i metadati e mostra le informazioni aggiuntive nella scheda focalizzata/espansa. I nomi dei titoli sono *proiezioni sintetiche* del laboratorio: il futuro ricevente owner-native potrà fornirne il significato, non è stato creato un nuovo catalogo Nautico autorevole.
- **Tempo dei cambiamenti circoscritti**: animazione discreta al passaggio Home/Plancia; entrata della barra Attività con direzione percepibile; transizioni di stato per pulsanti Strumenti e controlli, mantenendo gli effetti governati dalle funzioni esistenti. L'animazione non cambia da sé la selezione né conferma un'azione esterna.
- **Pulizia visiva**: la gerarchia della testata usa pochi livelli di scala; i metadati perdono enfasi rispetto al focus. La guida non sostituisce l'etichetta o il significato dei comandi.
- **Dettagli geometrici**: i puntini sui divisori fra colonne sono centrati; la riga `selectable-row` allinea una checkbox nativa alla prima riga della relativa voce, lasciando più righe leggibili e cliccabili.

L'HTML v5.8 resta byte-identico; non sono stati sostituiti il contratto pubblico `createMedium`, la macchina di stato della barra Attività, il controller del Kernel Nautico, la chat reale, la distribuzione o la semantica dei permessi.

## Identità e verifica

- Baseline: `20-griglia-rail-home-v58.html`, SHA-256 `799727c0283c61829796f20d1c4b45e652c3b2dd8d6056fe5577b0460ee3d9ad`.
- Candidata: [21-griglia-perceptual-continuity-v59.html](21-griglia-perceptual-continuity-v59.html), SHA-256 `463d9d436ab982f4ab68ec0cd2b8770813d0346ecd26bf90b9335f0e0b57ed3a`.
- Builder deterministico: `python tools/build_nautico_v59.py --check` verifica che la derivazione da v5.8 coincida byte per byte. Non aggiorna la baseline.
- [Nuove verifiche](EVIDENCE_GUIDED_CONTINUITY_V59_20261011.json): **139/139** Chromium Playwright; tour Home e Canvas, movimento realmente interpolato, riduzione del movimento, intestazione, checkbox, divisori, menu Strumenti, layout e continuità dei contesti.
- [Regressione v5.8](EVIDENCE_RAIL_HOME_V59_20261011.json): **159/159** controlli rieseguiti sull'HTML v5.9; stati Attività, Home, keyboard e lettura.
- [Compatibilità operativa precedente](EVIDENCE_COMPATIBILITY_V59_20261011.json): **126/126** controlli correlati al percorso Canvas, fullscreen, contesto e azioni.
- I tre script embedded superano `node --check`; zero errori JavaScript di pagina osservati nelle prove. Le **424 verifiche sono correlate sullo stesso sorgente**, non 424 esperimenti indipendenti.

**Limiti:** i test usano Chromium e `page.set_content` sul documento standalone esatto. Non provano l'Edge fisico dell'operatore, input touch reale, lettori di schermo, trasporto o autorizzazioni del Kernel Nautico, modello AI, server MAIOS o pubblicazione. La comprensione del passaggio percettivo rimane da osservare nell'uso umano.

## Apprendimento e rientro

Il meccanismo di costruzione riusabile torna a **Code Medium Construction**: quando una guida cambia target, far seguire allo stesso referente percettivo e alla descrizione un tragitto temporale interpolato, senza produrre una diversa verità del focus; sotto riduzione del movimento, il risultato finale mantiene identità e recuperabilità. La gerarchia della testata va costruita da una relazione semantica esplicita, non dalla successione casuale degli elementi visuali. **Interaction Quality** in Design già possiede orientamento, accessibilità e movimento come relazione generale: non duplicarne il metodo. **Editoriali** contribuisce alla leggibilità, senza acquisire i fatti Nautico.

**Stop della candidata**: codice, builder, prova e stato di rientro riproducibili nel branch K-UX-AI. Nessun merge del medium su `main`, release, modifica dei repository Nautico/`maios_it`, installazione di agenti o pubblicazione.
