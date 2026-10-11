# K-UX-AI v5.12 — fissaggio coerente della barra e compositore chat essenziale

11 ottobre 2026 · candidata nel solo branch `work/ux-ai-ui-library-20261008`.

## Fonte e differenza attuale

L'operatore ha osservato nel proprio browser una discontinuità specifica della barra Attività: l'hover sulla linguetta espone temporaneamente le icone, ma facendo clic per **fissare la barra** quelle icone scompaiono e tornano visibili. Non richiede un nuovo tempo di hover; richiede che il gesto di fissaggio **continui la stessa apparizione** già in corso. Chiede inoltre per la chat un campo vuoto iniziale di **una sola riga**, capace di crescere mentre si scrive, e un intervallo più chiaro fra le domande starter e la zona di editing.

La sorgente dell'osservazione fotografica mostra ancora una versione locale v5.10.1. Il ricevente selezionato è tuttavia la **v5.11 corrente** nel repository, che conservava il medesimo difetto nella propria macchina della barra. Questa differenza è verificata nel codice e nel browser; non abbiamo chiamato bug un effetto soltanto supposto dalla foto.

## Causalità esercitata e trasformazione

1. `hidden → peek` avviava una animazione di rivelazione della stessa `.intent-dock` di **860 ms** con `clipPath` da interamente chiuso ad aperto. Nel vecchio `animateRailReturn`, `peek → icons` **annullava** la prima animazione e ne avviava una nuova dallo stesso primo frame coperto. Per questo, alla conferma con clic, le icone già viste sparivano e riapparivano. **v5.12 non riavvia l'animazione per `peek → icons`**: conserva il carrier DOM originale e il tempo già trascorso. Quando la barra viene richiamata direttamente da `hidden` a `icons` resta l'animazione a 860 ms. La modalità `prefers-reduced-motion` porta direttamente al medesimo stato finale.
2. Il clic sulla linguetta `#activitiesEdge` restituisce il focus al controllo ancora visibile `#railVisibility`, dopo la scomparsa della linguetta. Icone, attività attive, geometria del workspace e semantica `hidden/peek/icons/previews` restano proprietà dello stesso controller.
3. Il compositore del modulo chat globale viene inizializzato con `rows=1`, `value=''`, nessun placeholder visibile e nome accessibile. Riusa l'autosize già esistente, adeguandone il minimo a **46 px** per la chat; quando il testo va a capo aumenta l'altezza fino al limite esistente di 190 px. L'invio pulisce il valore e attiva il ricalcolo dell'altezza, ritornando alla riga iniziale. Il form di contributo contestuale non viene ridisegnato.
4. Fra la riga di domande suggerite `.kux-chat-quick` e `.kux-chat-inputrow` c'è una distanza controllata di **21 px desktop** e **13 px** nella geometria compatta. Il pulsante Invia conserva una colonna separata dal campo, fuori dalla maniglia di ridimensionamento della finestra.

**Distinzione riusabile:** `carriera già percepita != nuova apertura da zero`; fissare uno stato transitorio è una **continuità dello stesso evento percettivo**, non un nuovo evento di comparsa. `valore azzerato != dimensione di editing azzerata`: il campo deve riacquisire l'altezza semantica iniziale anche dopo un reset programmatico.

## Identità ed esercizio

- Base preservata: [`24-griglia-content-hierarchy-v511.html`](24-griglia-content-hierarchy-v511.html), SHA-256 `67e8a1104d2abd66b886fad5354753a4db8964321c93947937de15f1917f434a`.
- Nuovo HTML autosufficiente: [`25-griglia-rail-composer-v512.html`](25-griglia-rail-composer-v512.html), SHA-256 **`1879dbe0d2ccba4c7db4701fe067c05ad1d20761aa2a6cf053f90b478118430b`**.
- Builder source-bound [`tools/build_nautico_v512.py`](../../tools/build_nautico_v512.py) + CSS additivo [`tools/kux_rail_chat_v512.css`](../../tools/kux_rail_chat_v512.css). Il `--check` confronta byte per byte; quattro script JS superano `node --check`.
- Suite nuova [`tests/qa_nautico_v512.py`](../../tests/qa_nautico_v512.py), [ricevuta](EVIDENCE_PEEK_PIN_CHAT_V512_20261011.json): **80/80** controlli su quattro viewport/configurazioni. Identità dell'animazione e dell'elemento DOM prima/dopo clic, durata 860 ms, reduced motion, focus, riga chat vuota, autosize e reset, spazio starter, pulsante e assenza di overflow/pagina error.
- Suite v5.11 rieseguite sul nuovo SHA con test compatibili [`qa_compat_content_v512.py`](../../tests/qa_compat_content_v512.py), [`qa_compat_motion_v512.py`](../../tests/qa_compat_motion_v512.py), [`qa_compat_home_v512.py`](../../tests/qa_compat_home_v512.py). Ricevute: [65/65](EVIDENCE_CONTENT_RAIL_COMPAT_V512_20261011.json) contenuto, [9/9](EVIDENCE_OPENING_MOTION_COMPAT_V512_20261011.json) aperture e [67/67](EVIDENCE_HOME_COMPAT_V512_20261011.json) Home. Totale **221 controlli correlati**, non 221 esperimenti indipendenti.

Le prove avvengono tramite Chromium Playwright `page.set_content` sul file locale esatto: **non** dimostrano Edge fisico, comprensione umana, assistive technology reale, API/AI collegati, permissioning o funzionamento sul sito pubblico. La persistenza della vecchia chat e la proprietà delle azioni restano nel controller della demo; la modifica non genera alcun agente reale.

## Ritorno ed effetti

Code Medium Construction è l'owner privato del meccanismo riusabile di costruzione (sopravvivenza della percezione nel passaggio da stato transitorio a stabile e recupero della geometria textarea). Interaction Quality del Design Kernel conserva la funzione generale di continuità e accessibilità: non creiamo un duplicato.

Stop: nuova candidata sorgente/prove e relativo cursore nel branch K-UX-AI. Nessun aggiornamento di `main`, release, sito MAIOS, Kernel Nautico, credenziali, provider o permessi. Successivo readback utile: conferma su Edge dell'assenza di sparizione durante il clic e della comodità del compositore.
