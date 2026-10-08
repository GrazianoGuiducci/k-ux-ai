# K-UX-AI — riuso delle interfacce esistenti, dalla sorgente al comportamento

**8 ottobre 2026 · analisi e prototipo locale v3 · non integrato nel sito**

## Selezione dell'operatore

- Il campo centrale deve occupare il massimo spazio utile. L'intestazione lunga, le liste di comandi, lo storico e le spiegazioni non devono restare su righe separate quando non sono materialmente pertinenti.
- La scheda operativa può apparire come avatar, card rapida, finestra mobile/ridimensionabile, dock laterale o pagina intera. Il cambiamento di forma non modifica l'oggetto, il contributo o la fonte.
- Esistono repertori maturi di chat, dashboard, editor e form con assistente. Va recuperata l'**unità completa** (stato, responsive, focus, split, eventi, backend boundary), non copiata la sola pelle.
- Apertura e chiusura devono indicare origine/destinazione attraverso un movimento continuo. Tendine e domande guidate trasferiscono focus/viewport solo quando cambia la prossima decisione leggibile.
- Il sapere deve tornare a UX-AI/Design e diventare parte della demo Nautico **dopo** osservazione e scelta dell'operatore, non tramite deploy anticipato.

## Fonti effettivamente lette nel repository Design/Agentic UX Seed

Repository `GrazianoGuiducci/d-nd-ux-ai-seed@972349d5c38a851f40ff6d8c87f541cd0da70f9e`, package `0.2.1`, componenti React/TSX.

| Unità | Sorgente owner-native | Contratto necessario |
|---|---|---|
| Chat e modulo completo | [`src/ThiaChatSeed.tsx`](https://github.com/GrazianoGuiducci/d-nd-ux-ai-seed/blob/main/src/ThiaChatSeed.tsx), [`docs/THIA_CHAT_PORT_PARITY_CONTRACT.md`](https://github.com/GrazianoGuiducci/d-nd-ux-ai-seed/blob/main/docs/THIA_CHAT_PORT_PARITY_CONTRACT.md) | Avatar, motion inverso, primo drag che espande, resize, full-page + restore, reset con conferma, chat/form nello stesso frame, divider, tab mobile, persistenza con chiavi proprie, handoff `onFeedbackSubmit` del host |
| Chat cognitiva | [`src/AgenticChatSystem.tsx`](https://github.com/GrazianoGuiducci/d-nd-ux-ai-seed/blob/main/src/AgenticChatSystem.tsx), [`docs/AGENTIC_CHAT_SYSTEM.md`](https://github.com/GrazianoGuiducci/d-nd-ux-ai-seed/blob/main/docs/AGENTIC_CHAT_SYSTEM.md) | Adapter host per contesto, conoscenza, competenze, trasporto e ricevute; side effect separati da normale risposta |
| Split | [`src/ui/SplitPanel.tsx`](https://github.com/GrazianoGuiducci/d-nd-ux-ai-seed/blob/main/src/ui/SplitPanel.tsx) | Pointer capture, ratio e clamp persistiti, frecce tastiera, recupero del pannello collassato, mobile sopra/sotto per superfici di lavoro o tab per Chat/Modulo dove lo specifico contratto THIA lo richiede |
| Shell | [`src/Shell3Col.tsx`](https://github.com/GrazianoGuiducci/d-nd-ux-ai-seed/blob/main/src/Shell3Col.tsx), [`docs/SHELL3COL_WORKSPACE_SEED.md`](https://github.com/GrazianoGuiducci/d-nd-ux-ai-seed/blob/main/docs/SHELL3COL_WORKSPACE_SEED.md) | Il campo principale governa il viewport, gutter cliccabili, sidebars indipendenti, fallback mobile; **non imporre tre colonne a tutte le pagine** |
| Megamenu | [`src/MegaMenuSeed.tsx`](https://github.com/GrazianoGuiducci/d-nd-ux-ai-seed/blob/main/src/MegaMenuSeed.tsx) | Gruppi e identificativi stabili, selezione/focus, descrizioni, comportamento mobile, handoff ad assistant quando davvero pertinente |
| Tooltip contestuale | [`src/ui/HoverPopover.tsx`](https://github.com/GrazianoGuiducci/d-nd-ux-ai-seed/blob/main/src/ui/HoverPopover.tsx) | Portal anti-clipping, placement auto, hover intent, Escape, focus/tastiera, pointer interactivo |
| Form contestuale | [`design/references/context-aware-guided-form-composition.md`](https://github.com/GrazianoGuiducci/d-nd-ux-ai-seed/blob/main/design/references/context-aware-guided-form-composition.md) | Grafo di domande causali, stato accettato/ignoto/derivato, invalidazione dipendenze, divulgazione reversibile, viewport/focus coerenti, review distinta da submit/effetto |
| Principi d'integrazione | [`docs/INTEGRATION_CHECKLIST.md`](https://github.com/GrazianoGuiducci/d-nd-ux-ai-seed/blob/main/docs/INTEGRATION_CHECKLIST.md) | Viaggiano insieme componente, dipendenze, CSS, storage key, awareness, stati responsive, prove browser. **Non copiare soltanto il markup.** |

## Originali recuperati: repository e contratti, non soltanto screenshot

Ho letto direttamente i sorgenti **GitHub** dei tre owner originari accessibili. Questa verifica non dimostra che i file installati oggi sul server siano byte-identici ai repository osservati.

| Superficie d'origine | Sorgente verificata | Logica da recuperare |
| --- | --- | --- |
| THIA / Chatbot React | [`d-nd_com/components/Chatbot.tsx`](https://github.com/GrazianoGuiducci/d-nd_com/blob/8ad776c76f735fb36c87df2a6f73b082c2e4813d/components/Chatbot.tsx), blob `ab5533a85726cfbf8c4353a2cb7d4bff996fabe2` | Chat, intake, stato della conversazione, drag/resize/split, starter contestuali, provider/servizi host. Dipendenze e autorità restano nell'owner. |
| THIA / Intake Form | [`d-nd_com/components/CommunityIntakeForm.tsx`](https://github.com/GrazianoGuiducci/d-nd_com/blob/8ad776c76f735fb36c87df2a6f73b082c2e4813d/components/CommunityIntakeForm.tsx), blob `d6447df32a7cf4e23200e76dbb1c5510cc8f3c75` | Domanda/contributo, allegati/contatti, consenso, stato e invio posseduto dal sito. |
| Lab D-ND / THIA vanilla | [`lab-d-nd-site/assets/js/domus-widget.js`](https://github.com/GrazianoGuiducci/lab-d-nd-site/blob/bc92ae3f90786ceaaf84d6042aef0aec876a50cb/assets/js/domus-widget.js), blob `32fe6769a83996b3b3a7d70f68c566acdefea054` | Unità completa **senza React**: avatar, pannello mobile/resizable, piena pagina su viewport stretti, split e chiavi persistenti. Candidato tecnico importante se il Nautico resta vanilla JS. Non trasportare endpoint THIA né sessioni di admin. |
| SITEMAN OS / Studio | [`d-nd_com/components/admin/SitemanStudio.tsx`](https://github.com/GrazianoGuiducci/d-nd_com/blob/8ad776c76f735fb36c87df2a6f73b082c2e4813d/components/admin/SitemanStudio.tsx), blob `c0eb28d26c9a2f46d60da5f0c78f5cdb3863f7d2` | Chat/editor/metadata, rapporti di split, collapsing, resize del composer, preferenze indipendenti, selezione mobile; mantenere i callback del controller Siteman fuori da Nautico. |
| SITEMAN OS / Dashboard | [`d-nd_com/components/admin/SitemanDashboard.tsx`](https://github.com/GrazianoGuiducci/d-nd_com/blob/8ad776c76f735fb36c87df2a6f73b082c2e4813d/components/admin/SitemanDashboard.tsx), blob `0ca83c3a679ec353ca4d6c09b81aef54e19264f0` | Card statistiche, filtri, ricerca, selezione, apertura del dettaglio e azioni esplicitamente delegate. Riutilizzo del comportamento, non delle autorizzazioni editoriali. |
| MAIOS Client Setup | [`web/app.js`](https://github.com/GrazianoGuiducci/MAIOS_CLIENT_SETUP/blob/21303ec074bd7bf395f4150ebc11764e0c2d1931/web/app.js), blob `3162bbcc89ab405abf75fd8cff516ac1c65d5a90`; [`web/maios-assistant.js`](https://github.com/GrazianoGuiducci/MAIOS_CLIENT_SETUP/blob/21303ec074bd7bf395f4150ebc11764e0c2d1931/web/maios-assistant.js), blob `8f95b528630586faaaeea10d52fd25b1b87da599` | Disclosure condizionale con prerequisiti, slow scroll e focus; ingresso chat/form, split/resize, full page con ritorno, invalidazione delle domande dipendenti. Non trasferire logiche P1–P5 al Nautico per sola somiglianza. |

**Rendere portabile il componente non significa spostare intere pagine, dati privati, account, segreti e autorizzazioni.** Significa trasferire il contratto completo della UI con le sue dipendenze e i confini degli effetti; i dati e le azioni restano al controller del prodotto ospitante.


Il package dichiara **PolyForm-Noncommercial-1.0.0** in `package.json`: per un prodotto MAIOS commerciale occorre confermare la facoltà di riuso/licenza con il titolare della sorgente (l'operatore è proprietario del repository, ma la liceità per terzi non si deduce da questo test).

## Che cosa esercita il laboratorio v3

Questi due file mantengono l'HTML/JS autonomo di laboratorio. Sono un **adattamento comportamentale parziale**, non un'importazione completa del package React né un'implementazione paritaria del sistema cognitivo THIA.

| Comportamento | v3 | Consegna prodotto successiva |
|---|---|---|
| Canvas prioritario | Barra da una riga; menu secondario; footer ridotto; `openTabs` compatto; +104px canvas a 1600×900 | Verificare anche altezze basse, mobile landscape, 200% zoom e spazio occupato da host/chat |
| Card rapida ↔ finestra | Contrazione `compact` con sintesi del focus, espansione senza perdere bozza | Associare semantica entity/attività agli owner del Nautico, non a dati fittizi |
| Vero full-page | Finestra 100vw×100dvh, Escape, focus verso controllo valido, altre superfici rese inattive | Verificare scroll lock/portals e ruolo modale nel Site host reale |
| Chat con modulo interno | Form e conversazione affiancati, divider trascinabile con ratio, tab Chat/Modulo se pannello stretto, draft, anteprima, download, reset chat confermato | Adottare `AgenticChatSystem/ThiaChatSeed` come unità completa con hook `onFeedbackSubmit` e host adapters |
| Movimento direzionale | Open avatar→finestra, riduzione verso avatar, transizione full↔free; reduced motion | Completare esatto source parity: prima drag-espansione, frame intake, manager, resize grip, close-frame reale, ricevute degli effetti |
| Spiegazione locale | “Perché qui?” separa osservato/interpretato/ignoto nel demo | Collegarlo solo a sorgenti, competenze e conseguenze realmente raggiunte dal Kernel, con readback umano/AI |
| Megamenu | Contesto, disposizioni e strumenti raggiungibili senza rubare righe | Usare `MegaMenuSeed` nell'host quando il bundling React è scelto; preservare selezione e mobile nav |

**Limiti dichiarati:** nessuna chat AI reale, nessuna trasmissione, form solo locale, nessun dashboard o editor di produzione importato, nessuna prova di assimilazione cognitiva o efficacia aziendale. I risultati sono test Playwright del singolo laboratorio.

## Composizione fra libreria, K-UX-AI e Nautico

**Non fare** `modal = finestra grafica + copia di qualche input`.

Quando il port sarà selezionato, una possibile unità di integrazione è:

```text
Kernel Nautico
  source objects / case / event / revision / authority
        ↕ adapter di ricevente
K-UX-AI
  active entity + intent / capabilities + perceptual composition
        ↕ componente ospitato
Agentic UX Seed
  ThiaChatSeed / AgenticChatSystem / SplitPanel / MegaMenuSeed
        ↕ host boundary
Site MAIOS
  provider, source knowledge, chat persistence, submit controller,
  viewport, focus, routing, acknowledgement
```

Il Kernel e il Site attuale possono usare JavaScript vanilla: il package principale è React. **Serve una scelta esplicita di adapter/build o l'estrazione di un nucleo headless**, verificando parità del comportamento, prima di promettere import diretto dei TSX nel Nautico. Una nuova rappresentazione non deve creare un secondo proprietario dei casi e delle revisioni.

## Prove di accettazione nell'host reale

1. Il primo visitatore vede la presentazione e raggiunge gli strumenti senza navigazione annidata inutile; la UI conserva il prodotto pubblico effettivo.
2. La chat reale apre avatar → frame → full-page; può tornare verso la stessa origine e rispettare il reduced motion, senza falsi effetti.
3. Drag, resize e dock restano di controllo umano; nessun pulsante scorrevole sotto il pannello diventa inaccessibile.
4. Uno stesso modulo funziona nel frame largo con split, nel frame stretto con Chat/Form, in mobile a pagina piena. La bozza resta attraverso i cambi di forma.
5. In un form guidato le dipendenze si invalidano quando cambiano risposte precedenti. Scrolling e focus non spostano la persona durante una selezione ancora da confermare.
6. Tooltip, pulsazione e annunci compaiono solo per un evento qualificato e raggiungibile; la mancanza d'azione o il silenzio possono essere corretti.
7. Due card o quattro monitor condividono il canvas senza fingere sincronizzazione concorrente di dati non implementata.
8. K-UX-AI riceve solo il contesto autorizzato; le risposte e gli effetti del controller del Site mantengono ricevuta e autorità distinte.
9. Site usa il branch/prototipo selezionato soltanto dopo confronto umano e test su viewport reali; `main`, Site pubblico e Codex restano inalterati fino alla scelta.

## Rientro e owner

- **Design/Agentic UX Seed:** sorgente completa dei componenti e dei contratti di UI. Imparare da errori implementativi del medium soltanto con ritorni source-bound.
- **K-UX-AI:** forma la competenza di composizione situata e i contratti di adapter fra owner, medium e dispositivo. Non duplicare il codice React senza ragione.
- **Kernel Nautico:** campo di lavoro, fonti, dati, oggetti ed effetti.
- **Sito MAIOS/Codex:** pagina ospitante, chat reale, provider, build/deploy, integrazione e test. Nessun effetto è ancora autorizzato dal presente documento.

Questo documento è un **hand-off candidato**, non un packet esecutivo inviato a Codex.