# CURRENT — K-UX-AI UI source cabinet, reusable Chat/Form and Nautico v4

## Ultima candidata 10 ottobre — K-UX-AI v5.1 Campo preparato

L'operatore, dopo quattro schermate Edge della v5.0, seleziona la Home come superficie per **preparare** il campo: cinque contesti visibili, multi-selezione di attività, Entrare nel canvas soltanto con selezione esplicita, tour opzionale. Gli avatar conservano peek pertinente; le card già aperte non mostrano un pulsante Anteprima duplicato. Dopo drag/avatar e reflow, i divisori non usati si sospendono e ritornano al bordo geometrico finale; le medie occupano righe/colonne compatibili con minimi di lettura.

[HTML v5.1](../../labs/nautico-ui-v4/12-griglia-campo-preparato.html), [contratto](../../labs/nautico-ui-v4/PREPARED_FIELD_20261010.md), [receipt](../../labs/nautico-ui-v4/EVIDENCE_PREPARED_FIELD_20261010.json). HTML Git blob `ac8de5bf2597759e9098c680d0295f730df26b51`, SHA256 `b5f11f4227a92e4f731d595c904ba93ec26e702036ac280319b12f6438f4d007`; tre suite Chromium correlate 103/103 + 26/26 + 23/23, 0 page errors osservati, provate via `page.set_content`. Builder, baseline immutata e test nel pacchetto consegnato all'operatore. Real Edge, gesture/device, storage intersessione, AI reale, filesystem e Nautico non provati. La Home usa `state.activeContext`, non introduce un owner di dominio; preparazione/entrata/autorizzazione restano distinti.

Questo modifica solo la candidata del branch di sviluppo, non `main`, Kernel Nautico o MAIOS. Prossimo: readback operatore in Edge; un altro movimento di integrazione si seleziona solo quando emergerà una differenza owner-native reale.


## Ultima candidata — v5.0 Campo coerente (9 ottobre 2026)

Dalle nuove schermate dell'operatore sulla v4.9: divisore a 2 card visibile ma inerte per override CSS 50/50; FLIP durante il drag produceva ritardo a 3 card; toolbar necessitava composizione funzionale; le tessere della Home devono scambiare i ruoli della posizione di drop anche fra tessere non principali e le 10 tessere devono entrare nel viewport desktop dove leggibile. [HTML v5.0](../../labs/nautico-ui-v4/11-griglia-campo-coerente.html), [causalità e metodo](../../labs/nautico-ui-v4/FOCAL_LAYOUT_V50_20261009.md), [ricevuta](../../labs/nautico-ui-v4/EVIDENCE_CAMPO_COHERENTE_20261009.json).

HTML blob esatto `a533b4e2751580c3fd0dae28c4025470a8011ff1`, SHA256 `baecb8930291f05aa07acf96888ec8147260183b8187e9f458a49b9e5343c56e`. 103/103 + 53/53 + 39/39 check Chromium correlati, 0 JS page errors osservati; `node --check` su 3 script. Test via `page.set_content`, non Edge locale. Pacchetto scaricabile con baseline v4.9, builder e test. Nessun nuovo controller sovrapposto e nessuna trasformazione owner-native del Nautico. Refactor modulare completo non selezionato in questo effetto.

**Rientro successivo:** osservazione Edge v5.0, poi solo differenze materiali. Nessun merge/release/deploy, provider, Section Kernel, filesystem esterno o autorità nuove.

## Risultante 9 ottobre — v4.9 Campo evolutivo

Dalle quattro osservazioni Edge sulla v4.8: la Home deve colmare i vuoti e consentire la promozione tramite drag di una tessera sopra un'altra; le finestre Libero non devono essere riordinate o ridimensionate senza gesto corrispondente; la sidebar deve preservare spazio agli avatar con Chat/Home sulla stessa riga; Contesto/Azione restano visibili; ogni confine reale di colonna deve avere una maniglia indipendente. [HTML v4.9](../../labs/nautico-ui-v4/10-griglia-campo-evolutivo.html), [decisioni](../../labs/nautico-ui-v4/FIELD_COMPOSITION_V49_20261009.md), [evidenza](../../labs/nautico-ui-v4/EVIDENCE_CAMPO_EVOLUTIVO_20261009.json).

HTML exact blob `bd85631db3bfe8e25333f1dcf684db2989a4d22a`, SHA256 `8448c1eb8bd2a76237ebb66763535b40e0fe223baa65521e8013f1de3d978d8e`; test in Chromium headless 53/53 e 39/39 più 2 smoke normale-motion, tutti correlati, zero JS error nei percorsi. Mappa Home senza lacune, 1+2 maniglie Adatta quando medie affiancate, 1/2 maniglie in 2/3 colonne quando fisicamente valide, doppia conferma avatar, Libero dimensioni restaurate. La sorgente è una trasformazione controllata dell'HTML v4.8, non un refactor completo del monolite. Il pacchetto operatore contiene il builder e i test; l'evidenza non rivendica storage, Edge reale, AI, Nautico live, touch/AT.

**Prossimo:** esercizio Edge; nessun altro layout, merge o integrazione Nautico/MAIOS selezionata per inerzia.


## Nuova candidata — v4.8 Contesto → Azione e divider stabile (9 ottobre 2026)

Da tre schermate Edge e osservazione operatore: [v4.8](../../labs/nautico-ui-v4/09-griglia-contesto-focus.html) corregge touch/drag del divisore e l'auto pairing oscillante delle medie, il ridimensionamento quando l'assistente riduce lo stage, l'hover di un avatar già attivo, la ripetizione del click, i due scroller della sidebar e la scarsa visibilità del contesto. La sorgente sposta l'unico selettore reale prima dell'azione corrente e non altera la semantica del Nautico o i suoi dati. [Ragioni e confini](../../labs/nautico-ui-v4/CONTEXT_FOCUS_20261009.md).

Prove locali nuove 100/100, più suite v4.7 rieseguite sul file corrente 97/97 e 51/51, correlate; no JS page errors nei percorsi Chromium. [EVIDENCE](../../labs/nautico-ui-v4/EVIDENCE_CONTEXT_FOCUS_20261009.json). HTML blob `d4534238ee0ae8c587132a0736e0bfb99a335951`. Builder, baseline e screenshot/test nel pacchetto scaricabile. La v4.7 resta invariata.

**Prossimo movimento:** osservazione Edge del comportamento reale; soltanto dopo un nuovo caso owner-native Nautico o un'integrazione assistente/AI selezionati. Nessun merge, release, deploy, modifica a Kernel Nautico, aggiornamento di provider o competenza assimilata rivendicata.

## Ultimo candidato — K-UX-AI v4.7 (9 ottobre 2026)

Da osservazione Edge dell'operatore: la barra di avatar chiusa e' ora un campo stabile di icone a 86px; le anteprime complete vivono nella barra aperta 255–395px e il quickpeek dell'avatar e' attivo solo a barra chiusa. [Nuovo HTML](../../labs/nautico-ui-v4/08-griglia-campo-medie.html), [contratto](../../labs/nautico-ui-v4/FIELD_AND_RESPONSE_MEDIUM_20261009.md), [evidenza](../../labs/nautico-ui-v4/EVIDENCE_FIELD_20261009.json).

La mappa espone «Grande» e un unico «Medie affiancate». L'ordine delle medie dipende dal drop; la geometria dipende dalla larghezza effettiva e dal divisore 27–60%. Un settore troppo stretto usa stack, non card affiancate illeggibili. Blob HTML `08834da1c5e3edb9f40a5cce6d1d4dfb8aaff4a3`, SHA256 `2f134374521e886c0d5ea4102972006110b716797406f49691c2d0a23b5903c7`. Browser proof 97+51 correlati, zero JS page errors nelle prove.

L'oriente futuro delle risposte aumentate con artefatti e memoria riusabile e' conservato nel contratto e restituito a Code Medium Construction come metodo candidate; l'annuncio OpenAI su Intelligent UI non implica API/provider installati. Non aprire in automatico una integrazione Nautico, una release, un deploy o un provider AI: servono receiver, source/effect boundary e la prossima selezione materiale.

## Ultima candidata 9 ottobre — v4.6 Convergenza

Dal feedback dell'operatore: sidebar da Nautico con avatar e anteprime, area principale/complementari ridimensionabile, chat globale e dialoghi locali, contributi candidati non assimilati, Presentare FORM/BUILD/LIVE/RETURN, etichetta Media affiancata. [Bundle HTML](../../labs/nautico-ui-v4/07-griglia-convergenza.html), [fonte/contratto](../../labs/nautico-ui-v4/CONVERGENCE_20261009.md), [receipt](../../labs/nautico-ui-v4/EVIDENCE_CONVERGENCE_20261009.json), due [moduli sorgente](../../labs/nautico-ui-v4/source-v46/); builder e script nel pacchetto ZIP dell'interazione.

HTML blob `39cdf482ec810437b79aa16d6e39a6653c1f8f87`; due suite Chromium correlate 64/64 + 30/30, zero page errors osservati con `page.set_content`. Non dimostra AI reale, SK, assimilazione, filesystem Codex o Nautico live. Nessun merge/release/deploy. Prossimo: prova Edge dell'operatore o nuovo movimento owner-native distinto.


## Ultima risultante — Griglia v4.5 Campo focale (9 ottobre 2026)

Nuova osservazione diretta: nella v4.4 l'operatore ha chiesto **anteprima diretta sull'hover** dell'avatar anziché mini-icona, click sempre nel posto principale spostando il precedente in seconda posizione, drag che riorganizza il campo, audit delle icone, una scheda dominante e altre impilate in una colonna, con opzione due-affiancate solo con spazio sufficiente. La [v4.5](../../labs/nautico-ui-v4/06-griglia-campo-focale.html) implementa questa relazione e conserva `main` e le v4.0–v4.4 storiche invariate.

[Contratto e osservazioni](../../labs/nautico-ui-v4/FOCAL_FIELD_20261009.md), [ricevuta bounded](../../labs/nautico-ui-v4/EVIDENCE_FOCAL_FIELD_20261009.json). Blob del sorgente HTML candidato `15b66abd4793de9dff2f9a33efb914ec20c696c5`, SHA-256 `e8dd429f61a2814aa529dd0b908b105290b72afe3af2cca480347283cd2275ae`.

Scissione operativa: `state.focused` identifica il principale, `state.slotOrder` conserva l'ordine della colonna complementare; anteprima/hover non muta dominio né focus, click è promozione esplicita anche con pin, drag in campo riordina, Libero resta manuale. Il contenitore secondario diventa una vera scroll region invece di celle grandi vuote; DOM order e visual order restano coerenti dopo spostamento. Desktop con frame >=2050 px può usare due piccole affiancate. Barra avatar 62–150 px ridimensionabile. Su mobile il contenuto e il piede della card rimangono **dentro** il riquadro e scorrono in normale flusso: un controesempio iniziale ha richiesto di riapplicare `data-placement=tiled` dopo `moduleStyles` e correggere flex/height del contenitore.

L'ultimo `KUXAIDemo.perception().view` descrive composizione, impilamento o coppie, ampiezza degli avatar e anteprima in corso; è soltanto un readback locale. Le fonti e gli effetti Nautico appartengono ancora ai rispettivi owner; Section Workspace e assistente locale rimangono simulazioni. Nessun nuovo kernel, controller o provider è stato installato.

**Proof**: 74+32+17 controlli Playwright/Chromium correlati sul file HTML esatto (totale 123), 0 page errors nei percorsi. Test ripetuti anche dalla copia distribuita nel pacchetto. Non provati: Edge sul PC dell'operatore, touchscreen, AT completa, comprensione umana, trasporto AI, dati enterprise. Nessuna release/merge/deploy, `src/medium.js`, Kernel Nautico o Site MAIOS modificati.

**Prossimo momento:** osservare v4.5 su Edge; cambiare layout solo per un controesempio materiale. L'integrazione con uno stato autentico Nautico resta un distinto movimento quando il ricevente e la sorgente siano disponibili.


## Resultant privato 9 ottobre 2026 — Griglia v4.4, slot + sezione

Da screenshot dell'operatore v4.3: focus semantico bloccato non impediva sovrapposizione delle card libere, drag da griglia sganciava il campo, mini anteprima aveva comportamento di movimento/resize incongruente. La nuova [v4.4](../../labs/nautico-ui-v4/05-griglia-ecosistemi-smart-slots.html) introduce una composizione dei ruoli Grande/Media/Piccola/Full indipendente dallo stato di dominio, mappa facoltativa negli avatar, collocazione in griglia per trascinamento, lettura preview mobile e ridimensionabile, focus non rubato e 750 ms sui passaggi strutturali con reduced-motion equivalente.

La [Section Workspace dimostrativa](../../labs/nautico-ui-v4/SMART_GRID_SECTION_ECOSYSTEM_20261009.md) dimostra quadro, fonti, conversazione e collegamenti dentro una card senza montare automaticamente un Section Kernel o AI provider. Kernel Nautico conserva la propria semantica e topologia federata; il primo collegamento reale resta un **altro** movimento con fonte/revisione/owner/autorità. L'ipotesi SK è possibilità, non nuova architettura promossa.

[Evidence v4.4](../../labs/nautico-ui-v4/EVIDENCE_SMART_GRID_20261009.json): 23/23 + 26/26 + 10/10 assertions Chromium locali, correlate, 0 page errors osservati, identificati con blob `de2dc784d9a51f162cd13587c9ca0d461b396c47`. Test riproducibili consegnati in pacchetto separato. Nessun `main`/release/deploy/site/Kernel Nautico modificato.

**Prossimo rientro:** prima leggere questo CURRENT e osservare la v4.4 insieme all'operatore; una nuova differenza reale può richiedere un evento source-owned Nautico, non aggiungere altre card o una finta AI per inerzia.


## Rientro del 9 ottobre 2026 — Griglia del fare v4.3, focus dinamico

L'operatore ha osservato quattro schermate della v4.2 e ha distinto una nuova pressione: lo spazio e l'attenzione non si distribuiscono automaticamente allo stesso modo. Una sola attività occupa il campo; due lo condividono; dalla terza il focus può prevalere, senza escludere gli altri oggetti. Aggiungere o controllare una scheda non autorizza di per sé a perdere il focus principale. È pertanto pertinente la distinzione [anteprima/attività/focus/full e Ricomponi](../../labs/nautico-ui-v4/FOCUS_COMPOSITION_20261009.md), non un semplice cambio di proporzioni.

**Artefatto corrente:** [Griglia v4.3 Focus dinamico](../../labs/nautico-ui-v4/04-griglia-focus-dinamico.html), blob Git `75d065cb961d28b545c77f820d9328abeec7663e` e [receipt separato](../../labs/nautico-ui-v4/EVIDENCE_FOCUS_20261009.json). Il prototipo accetta selezioni e produce cambi di layout/attenzione locali; la sorgente di stato e gli eventi Nautico rimangono *sintetici*. Il focus bloccabile protegge le aperture successive; l'anteprima mostra fonte, dato ancora da qualificare, ultime tracce/segnali demo senza aprire/approvare; la pagina intera è temporanea; Ricomponi non elimina i pannelli e non resetta i dati. L'input di resize di chat e card free ha un'impugnatura visiva e un cursor uguali nel ricevente di laboratorio.

**Evidenza propria:** 160/160 + 66/66 controlli browser Playwright/Chromium headless su dati locali, zero page errors rilevati nelle suite, su viewport 375–1680, modalità normale e reduced-motion. Queste due prove sono correlate e non 226 validazioni indipendenti. Test eseguiti con `page.set_content` perché `file://` era bloccato nel receiver di prova. Prova di navigazione diretta in Edge, touch fisico, utenti reali e accessibilità completa non acquisita. Le ricevute storiche v4–v4.2 restano valide solo per le loro identità testate.

**Confini:** non cambia `main`, `src/medium.js`, Kernel Nautico, THIA/provider, pubblico MAIOS, release o deploy. Il prossimo effetto non è selezionato automaticamente: prima osservare il candidato con l'operatore, poi eventualmente usare un vero cambiamento source-owned del Kernel Nautico nel suo receiver. La forma del campo non è autorità sul lavoro o sul suo significato.


## Ultima risultante — Griglia v4.2 workspace adattivo (8 ottobre 2026)

Le schermate osservate dall'operatore hanno selezionato un problema concreto di composizione: tutte le card operative devono restare esplorabili, anche su telefono, senza che il layout diventi una quota di attività visibili. La candidata [Griglia v4.2](../../labs/nautico-ui-v4/03-griglia-responsive-workspace.html) separa il contenuto owner-native dalla sua occupazione spaziale; il [documento di decisione](../../labs/nautico-ui-v4/RESPONSIVE_DESIGN_20261008.md) conserva motivazioni, alternative e confini.

La modalità Adatta (iniziale) usa una griglia a 1–3 colonne secondo il *frame* disponibile, con righe aggiuntive e scorrimento dell'intero canvas. Le scelte 2/3/4 sono composizioni, non limiti al numero di card. La modalità Libero resta distinta per geometria manuale. Sul mobile si elimina il dock di avatar laterali, si mantengono card in colonna scorrevole e si collocano assistente, focus e menu Strumenti nella barra superiore. Il menu ha un contesto di profondità proprio e non può essere coperto dal progressivo z-index delle card. Le azioni dimostrative del footer passano al menu su schermi piccoli, senza duplicare il controller.

La [ricevuta separata](../../labs/nautico-ui-v4/EVIDENCE_RESPONSIVE_20261008.json) registra 121/121 + 19/19 controlli locali correlati sul file HTML v4.2 esatto, senza errori di pagina nei percorsi osservati. La v4 e la v4.1 con i loro controlli restano genealogia; la nuova prova non trasferisce automaticamente completezza o conformità di accessibilità. Il browser di prova non consentiva l'apertura `file://`, quindi i percorsi sono stati esercitati con `page.set_content`. Nessun kernel Nautico reale, hosting, provider AI, THIA o Site MAIOS è stato connesso; nessun merge/release/deploy selezionato.

**Prossimo confine:** osservazione dell'operatore della v4.2 e/o esercizio di una vera modifica owner-native del Nautico nel receiver separato. Non convertire automaticamente questo miglioramento percettivo in un'integrazione live né avviare un altro layout per inerzia.


## Ultima differenza — candidato v4.1 motion parity (8 ottobre 2026)

La Griglia v4 e [la sua ricevuta correlata da 93 controlli](../../labs/nautico-ui-v4/EVIDENCE.json) restano identità storiche conservate. Il [nuovo HTML v4.1](../../labs/nautico-ui-v4/02-griglia-chat-window-surface-motion-parity.html) usa la modifica minima applicata anche a [`createWindowSurface`](../../src/ui/window-surface.js): `minimize()` legge il token dell'animazione dopo `avatarToWindow(false)`, non prima. L'assenza di animazione deve concludere la chiusura con focus, stato e avvisi corretti.

La [ricevuta della prova di rientro](../../labs/nautico-ui-v4/EVIDENCE_MOTION_PARITY_20261008.json) registra 11/13 controesempi sulla v4 originale in reduced-motion, 13/13 sul candidato in reduced-motion e 13/13 con motion normale (suite locale di smoke mirata). Non sono 26 convalide indipendenti né una riesecuzione dei 93 controlli originari. La v4.1 resta **candidate/synthetic**: nessun merge, release, hosting MAIOS, stato reale Nautico o modello AI connesso.

Il prossimo esperimento utile non e' un'ulteriore ottimizzazione grafica automatica: e' un evento / cambiamento owner-native reale in Kernel Nautico, osservato dal medium con identita', revisione e doppio readback, senza trasferire proprieta' del dominio a K-UX-AI. L'ingresso di costruzione cognitiva corrente e' il Code Medium Construction 0.4.0 privato in `tm7/gpt/ux-ai-code-competence`, distinto dal candidato pubblico.


**8 October 2026 · private branch candidate · public product version remains `0.1.0-alpha.1`**

```text
owner: GrazianoGuiducci/k-ux-ai
branch: work/ux-ai-ui-library-20261008
starting_main: 68cb9c82631aae2d1d5ad4fa22cd255d67e5f57b
semantic_owner: Meta_Skill / ux-ai-kernel-design
design_owner: D-ND Design Kernel / Agentic UX Seed
first_domain: Kernel Nautico
receiving_site: MAIOS (separately owned, not modified)
status: CANDIDATE_SOURCE_CABINET + REUSABLE_CHATFORM + INTEGRATED_GRIGLIA_V4_SYNTHETIC
effect: no release, merge, installation or public site update
```

## Selected current movement — Griglia del fare v4

[Griglia v4 con Window Surface/ChatForm realmente riutilizzati](../../labs/nautico-ui-v4/01-griglia-chat-window-surface.html) è il primo esercizio integrato nello **stesso browser**: le altre card Nautico rimangono quelle del laboratorio v3, mentre l'assistente usa una sola istanza dei componenti pubblici di K-UX-AI. La [ricevuta](../../labs/nautico-ui-v4/EVIDENCE.json) distingue 28/28 controlli base, 28/28 integrativi e 23/23 + 14/14 sul componente riutilizzabile, tutte suite **correlate**.

Tre differenze hanno già modificato l'implementazione:
- il primo click sull'avatar del workspace deve attraversare la politica host di docking per liberare il canvas, non aprire arbitrariamente in sovrapposizione;
- quando un cambio di forma nasconde il pulsante attivo (full/dock), il **focus deve passare a un comando visibile**; altrimenti anche Escape può perdere efficacia;
- un evento simulato ma ancora aperto deve poter tornare come avviso attribuito all'avatar chiuso dopo il rientro nella Home, senza doppie notifiche.

**Confine:** nessuna chat AI effettivamente collegata, nessuna integrazione con lo stato live Nautico, nessun Site MAIOS, nessuna approvazione aziendale o distribuzione. L'HTML v4 è un probe sinteticamente integrato, non il prodotto pubblicato. La v3 resta conservata e il codice di base `src/medium.js` non è cambiato.

## Begin here

1. Read the [K-UX-AI Kernel](../../KERNEL.md) and the published [medium contract](../../docs/interface.md).
2. Read [the module catalog](../../ui-library/catalog.v0.1.json): **20 exact source references across five owners, nine behavior families**.
3. Read [the complete surface composition contract](OPERATING_CONTRACT.md), then the [source-by-source adoption map](SOURCE_ADOPTION_20261008.md).
4. Apri prima [Griglia v4](../../labs/nautico-ui-v4/01-griglia-chat-window-surface.html) e la sua [ricevuta](../../labs/nautico-ui-v4/EVIDENCE.json). Per genealogia, conserva poi [Griglia del fare v3](../../labs/nautico-ui-v3/01-griglia-del-fare.html) and [Campo a quattro fonti v3](../../labs/nautico-ui-v3/02-campo-quattro-fonti.html) as standalone **synthetic probes**. Read their [receipt](../../labs/nautico-ui-v3/EVIDENCE.json) before making claims about what is tested.
5. Only when a real Nautico/coder integration is selected, resolve the **current** owner-native state and source SHA again. These commits are readback coordinates, not permanent freshness claims.

## First native K-UX-AI Chat/Form module — 8 October 2026

The source cabinet now includes a **bounded executable native implementation**, not just upstream references:

- [`createWindowSurface`](../../src/ui/window-surface.js) + [CSS](../../src/ui/window-surface.css) — stable window identity, avatar, attributed cue, directional open/close, free position/resize, edge docking, full-page, keyboard resize, restoration and reduced-motion support.
- [`createChatFormModule`](../../src/ui/chat-form-module.js) + [CSS](../../src/ui/chat-form-module.css) — Chat/Form in one frame, responsive based on **layout width, not animated bounding box**, splitter, mobile tabs, drafts preserved when the window transforms, host-controlled submissions.
- [Example using actual `createMedium`](../../examples/window-surface/index.html) and [example contract/readme](../../examples/window-surface/README.md). Demonstration state and event IDs are **synthetic**; no AI backend or real Nautico state is connected.
- [Bounded QA receipt](../../examples/window-surface/evidence.json): 23/23 primary + 14/14 additional browser assertions on related flows, zero page errors observed. The tests were run on a self-contained inline composition of the same JS/CSS modules via Chromium `set_content` because the current browser runtime blocked file:// and localhost navigation. The repository's modular HTTP-served build was not independently browser-tested.

Useful learning: during an avatar-origin animation, `getBoundingClientRect().width` shrinks because CSS transform changes visual geometry; internal module responsiveness must measure layout width (`offsetWidth`) instead. A denied browser storage must not disable the module. Free dragging must keep resize handles reachable within the viewport.

**Not yet complete:** full THIA/DOMUS parity, agent/provider transport, manager privileges, actual Nautico owner event stream, general multiwindow orchestration, first-drag expansion/undock-from-full behavior, fully audited accessibility or real Site integration.

This new code does not bump the public alpha or replace the historical source cabinet. Continue owner-native work from this precise candidate and the original THIA parity sources rather than copying host API/credentials.

## What moved

The operator requested that the behavior of the Lab D-ND HTML/JavaScript assistant and adjacent original UI modules be made reachable within K-UX-AI, **before any new HTML generation or Codex site integration**. The need is to recover full behavior (drag, resize, inverse motion, two-pane modals, mobile, manager, guided forms, scroll/focus, state and effect boundaries), not to import its look.

Lab D-ND original source:

- `lab-d-nd-site@bc92ae3f90786ceaaf84d6042aef0aec876a50cb/assets/js/domus-widget.js` (JS, 6k+ lines, host-specific backend and admin logic).

Related original carriers:

- `d-nd_com@8ad776c76f735fb36c87df2a6f73b082c2e4813d`: THIA React, intake, SITEMAN Studio and Dashboard.
- `d-nd-ux-ai-seed@972349d5c38a851f40ff6d8c87f541cd0da70f9e`: THIA/AgenticChatSystem, Shell3Col, SplitPanel, MegaMenu, HoverPopover, primitives, source-parity and design contracts.
- `MAIOS_CLIENT_SETUP@21303ec074bd7bf395f4150ebc11764e0c2d1931`: context-aware guided form, chat/form pairing, animated focus/scroll and dependency invalidation.
- `kernel-nautico@82896de01829752614d04cfa6e3ffacbd9544a0a`: first domain object, actual public views and separate owner-native case state.

**No upstream runtime or full page was copied.** The branch contains two original self-contained v3 demo HTML files produced in this conversation and documents source references to the implementation owners. The Lab source's auth, provider, server API and storage must not become default K-UX-AI behavior.

## Sufficient observed distinctions

- A single entity can appear as **avatar, concise card, floating window, dock, split plane or full-page**, with its semantic/domain identity unchanged.
- The **canvas wins vertical space** over large titles, duplicated statuses and toolbars; secondary commands can remain available in a compact megamenu.
- Manual window geometry is distinct from system-generated arrangements and must be recoverable, including mobile → desktop restoration.
- A module may need an **internal responsive** mode according to its own width, not just the viewport width.
- A chat/form workspace can be side-by-side in a wide frame and one-pane-at-a-time on compact frames; retaining unsent drafts is necessary.
- Movement should communicate origin/destination and causal change, not simply delay the UI. Interruptions, ESC, focus and reduced-motion parity are part of the action contract.
- Tool-specific backend authority and the host's data/credentials do not become transferable when its visual component is reused.
- Notifications are owner-source events, not new UI renderings or arbitrary decorative pulses.

## Evidence and absence

The historical local laboratory run records **63/63 correlated Playwright assertions**, with zero JS page errors, on v3 standalone HTML with synthetic state. The files are now in the branch, but **that browser suite has not been rerun against the GitHub copy in this movement**.

The product's `createMedium()` code is unchanged. No chat transport, real THIA model, authenticated manager, enterprise/vessel data, domain effects, simultaneous writable nautical panes, independent human comprehension validation or deployed Site is produced by this cabinet.

The license declared by the upstream Agentic UX Seed package is **PolyForm-Noncommercial-1.0.0**. If the selected MAIOS product requires a different use, qualify the appropriate grant with the source owner. Mere common authorship or catalog entry is not a distribution right.

## Next material movement

From the user's review of v3 plus the source contracts, choose the smallest whole UI module that makes the Nautico work materially more understandable and operable. Adapt a **real source-owned event** through `createMedium()` into the selected module. Compare this with the historical synthetic example; test keyboard, touch, geometry, persistence, responsive, resize, host effects and actual operator comprehension.

Only after a selected candidate works in its host should Codex Site receive an integration packet. Do not publish/update MAIOS or mutate Kernel Nautico from this source cabinet by inertia.

## Status of adjacent owners

- Meta_Skill / UX-AI: kernel–human comprehensibility and code-medium competence, can receive later source-bound learning.
- Design/Agentic UX Seed: component and perceptual construction owner, not overwritten.
- Nautico: case, product, events and domain meaning owner.
- MAIOS Site/Codex: actual page host, agent providers and public integration authority.

Current result: **source availability and a candidate kernel-product cabinet**, not completion of the final UI.
