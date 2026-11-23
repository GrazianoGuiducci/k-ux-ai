# MetaEditor Evolution — CURRENT

## 23 novembre — Correzione autoriale: RC1 tecnicamente valida ma non sufficientemente utilizzabile

**Feedback d'uso reale:** l'operatore constata «È ancora abbastanza poco utilizzabile. Non credo, non vedo tanti sviluppi da dove eravamo partiti». **Questo supera la decisione precedente di trattare il sottoinsieme neutro come MetaEditor 1.0 pronto al collaudo di accettazione.** Non è un errore che si risolve aumentando il numero di test; l'oggetto valutato non corrispondeva alla direzione del prodotto. L'operatore non deve ripetere il medesimo collaudo per dimostrarlo.

**Sorgenti riaperte e confrontate:** [SKILL.md](SKILL.md) definisce già correttamente una capacità di **modifica diretta, composizione di oggetti, testo, diagrammi, sezioni e documenti** per pagine e presentazioni; il routing ha mancato tale conoscenza. [Bridge11 / CURRENT.html](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/workbench/metaeditor/CURRENT.html) (blob `9f4f843124f8619eee02ece40a7efc1470881b07`) possiede mini editor, ricerca e focus, sezioni/elementi, colori/dimensioni, maniglie e anteprima desktop/mobile. [MetaCanvas Studio20](https://github.com/GrazianoGuiducci/k-ux-ai/blob/main/examples/collaborative-communication-medium/AI_Collaboration_Studio.html) (blob `d057d68c60061dd9e8f5c2d704cfff2016ea19b1`) possiede composizione spaziale, template Sostituisci/Sopra/Sotto, oggetti/livelli, editing e presentazione. Il [neutro](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/examples/collaborative-communication-medium/meta-editor-lab/neutral-static-page-editor.js) è una toolbar fissa e un set ridotto di editing DOM. Il [riesame di prodotto](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/examples/collaborative-communication-medium/meta-editor-lab/PRODUCT_REALIGNMENT_20261123.md) rende il confronto e le tre risultanti R1/R2/R3 disponibili.

**Stato corretto delle prove:** gli artifact RC1, gli SHA e i 5 job verdi restano eventi verificati e riutilizzabili per integrità, portabilità e reversibilità **del laboratorio HTML neutro**. **Nessuna v1 di prodotto approvata e nessun gate d'uso chiuso.** Il vecchio `METAEDITOR_1_0_RELEASE_CONTRACT.md` resta storico ma è superato come criterio di riuscita del prodotto. PR #2 draft, site main invariato.

**Prossimo movimento competente:** **R1: ritornare alla superficie di editing visuale effettivamente posseduta** (Bridge11/Studio20), agire direttamente sull'oggetto, con focus e controlli contestuali, non ricostruire per la quinta volta una toolbar ridotta. R2: composizione di elementi, layout e template del carrier appropriato. R3: anteprima, salvataggio e rientro con prove di export già utili. Il modello documento pagina e quello scena non si fondono per semantica. Nuove operazioni si formano dall'esperienza d'uso, non da un contratto prematuro che esclude le facoltà originali. Metodologia rettificata in [GUIDE.md](GUIDE.md). Il test umano resta d'uso, non QA tecnica.

## 23 novembre — Consegna effettiva delle due RC e arresto dello sviluppo per inerzia

**Azione concreta:** il pacchetto MetaEditor `1.0.0-rc.1` è stato scaricato dall'[artifact 14816910606](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45169380830), estratto dal wrapper CI e verificato in questo host, SHA-256 `867c271915221bcc3a1d2f3d9164798c0448258768ed96f91b9d5293ab29dfaf`, **9 checksum file corretti**. È disponibile per un **unico collaudo d'uso umano**, ma questa disponibilità non chiude il gate.

**Linea distinta MetaCanvas Studio21:** da due sorgenti IT/EN source-pinned il [builder release](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/tools/build_metacanvas_studio21_release_pack.py) forma un ZIP di privacy+movimento con manifest, licenza e NOTICE. [CI 45171725612](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45171725612) **5/5 verde**; artefatto `metacanvas-studio21-privacy-rc1` ID `14816672688`, ZIP SHA-256 `830c5b40894164b993ae66d027338e97a5067da3e736ca738f97a62c5e88c4e0`, 5 file verificati dopo estrazione. Pubblicazione IT/EN da parte dell'owner sito e readback **non esercitati**. La correzione della prima prova del pacchetto ha riguardato un assert di conteggio: nella sorgente esisteva già un filtro `private`; il test ora verifica i quattro nuovi filtri *in differenza*, preservando la prova precedente.

**Orientamento:** niente nuovi prototipi o miglioramenti indeterminati. I due artefatti sono raggiungibili e verificati. Procedere soltanto ai loro gate rimasti, riconoscendo competenza, oggetto, owner e autorità distinti.

## 23 novembre — MetaEditor 1.0 RC completo: fermata l'espansione di scope

L'[owner del contratto 1.0](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/examples/collaborative-communication-medium/meta-editor-lab/METAEDITOR_1_0_RELEASE_CONTRACT.md) determina **otto percorsi di uso da quattro modelli HTML statici** e separa fuori scope CMS/editor universale, scene MetaCanvas e publish. Il builder genera `1.0.0-rc.1` riproducibile con manifest SHA-256, launcher, quattro workpage, guida, licenza MPL-2.0, NOTICE e crediti. [CI 45169380830](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45169380830) **5/5 verde**, incluso Chrome Windows `file://`, Linux, Studio21 e sito MAIOS verificato read-only; artefatto `metaeditor-1-0-rc1` ID `14816910606`. **Resta un solo collaudo umano d'uso integrato e una decisione distinta di rilascio; PR #2 draft, nessun sito modificato.** Le nuove capacità fuori dagli otto percorsi appartengono al backlog, non riaprono la 1.0. MetaCanvas ha un gate privacy/publish separato.

## 23 novembre — MetaEditor 1.0 determinato: fermare l'espansione, chiudere i gate

**Nuova determinazione dell'operatore:** i test umani saranno **d'uso**, e il progetto deve assumere una forma finita. Il contratto di prodotto è [METAEDITOR_1_0_RELEASE_CONTRACT.md](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/examples/collaborative-communication-medium/meta-editor-lab/METAEDITOR_1_0_RELEASE_CONTRACT.md): editor locale di pagine HTML statiche **da quattro template**, con otto percorsi chiusi; esclusi CMS universale, arbitrario import HTML, editing di scene MetaCanvas e pubblicazione automatica. Le altre possibilità sono backlog, non nuovi gate. MetaCanvas pubblico resta prodotto distinto; sua patch privacy Studio21 candidata ma non distribuita.

**Effetti reali:** [builder starter](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/tools/build_metaeditor_starter_pack.py) ora produce unico `MetaEditor_1.0.0-rc.1.zip` con manifest verificabile `VERSIONE_E_FILE.json`; test di build riproducibile e hash. Il workflow ha un job separato **Chrome Windows** e un solo artefatto RC invece di molte anteprime. [CI 45168573050](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45168573050): **5/5 job verdi**, incluso Windows `file://` con quattro template, editing/salvataggio, paste e composizione protetta; gli altri job verificano Studio21, MAIOS live, Linux e contratti. Artefatto `metaeditor-1-0-rc1` ID `14815467429`. **Non** equivale a prova umana o rilascio.

**Prossima transizione:** non aggiungere funzioni salvo bug che impediscano uno degli otto percorsi; revisionare pacchetto e condizioni di release, poi una sola prova d'uso integrata con l'operatore, prima di eventuale decisione di pubblicazione. PR #2 rimane draft; `maios_it/main` non modificato. Metodo in [GUIDE](GUIDE.md).

## 23 novembre — Composizioni miste con isole autoriali protette

**Stato nel ramo [PR #2](https://github.com/GrazianoGuiducci/k-ux-ai/pull/2):** la [candidata neutra](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/examples/collaborative-communication-medium/meta-editor-lab/neutral-static-page-editor.js) esclude da selezione e posizionamento le isole `contenteditable="false"` e `inert`, impedisce ai movimenti rapidi di scavalcare nodi originali e mantiene come opzione la destinazione esplicita prima/dopo. L'[adapter sorgente](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/examples/collaborative-communication-medium/meta-editor-lab/static-page-source-adapter.js) conserva il `contenteditable=false` autoriale nei file lavoro e pulito, rifiutando invece editabilità autoriale attiva.

**Identità work/history:** `data-local-block-id` stabile e distinto per ogni blocco creato o duplicato, compresa migrazione delle copie lavoro precedenti che hanno `data-local-block` ma non un ID. Lo scambio di due paragrafi con markup identico è ora rilevabile da history; clean HTML rimuove i metadati. Un click sulla caption di una figura aggiunta seleziona l'intera figura; doppio clic permette editing del testo.

**Verifica:** [CI 45153539786](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45153539786) quattro job verdi: [test mixed protected](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/tests/metaeditor-mixed-protected.browser.py) a 1440/390 Chrome Linux `file://` esercita card con immagini e link originali, readonly e inert, inserimento/media/trasferimento, originale invariato, esportazione e reopen, Undo totale; restano verdi Studio21, altri test neutri e la pagina MAIOS source-identical. Il successivo [run 45153723331](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45153723331) ha quattro job verdi e verifica anche che due copie della stessa immagine abbiano identificativi di blocco diversi, con Undo coerente.

**Confini:** niente merge o produzione; prova umana Windows differita come richiesto, release Gate B ancora parziale. Il metodo è in [GUIDE](GUIDE.md).

## 23 novembre — Posizionamento preciso nei layout annidati, CI verde

**Nuovo portatore candidato:** [neutral-static-page-editor.js](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/examples/collaborative-communication-medium/meta-editor-lab/neutral-static-page-editor.js) distingue la `section` dal gruppo di testo effettivo e permette di scegliere un riferimento prima/dopo tramite `Posizionamento preciso`. La scelta rimane nascosta sotto un `details` finché serve; viene conservata per identità del nodo, non per indice che può spostarsi. I flussi multipli senza referente autoriale o selezione sicura vengono rifiutati, senza cambiare documento o history. Inserimento, link, immagine e trasferimento usano il medesimo posizionamento; una scheda della stessa sezione può essere nuova destinazione esplicita.

**Evidenza:** [CI 45149431000](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45149431000) quattro job verdi, incluso [test nested grid](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/tests/metaeditor-nested-layout.browser.py) su fixture sintetica con quattro schede, viewport 1440/390 e URL `file://`: rifiuto dell'ambiguo, prima/dopo sul card corretto, stesso/altra sezione, Undo/Redo, clean HTML e pieno ritorno ai byte originali. Regressioni su Studio21, altri HTML statici e pagina MAIOS reale source-identical rimangono verdi. Non certifica HTML/CSS arbitrario, Chrome Windows fisico, accessibilità completa o release.

**Stato e direzione:** [PR #2](https://github.com/GrazianoGuiducci/k-ux-ai/pull/2) draft; `maios_it/main` e pubblicazione invariati. L'operatore ha differito i test manuali fino a un prodotto più completo. Resta da valutare il campo di possibilità di layout/template realmente supportati e la futura verifica umana del flusso, senza indurre a nuovi micro-test. Il metodo è in [GUIDE](GUIDE.md).

## 23 novembre — Link e immagini incorporati: candidato HTML neutro

**Nuove capacità nel ramo [PR #2](https://github.com/GrazianoGuiducci/k-ux-ai/pull/2):** creazione di link come blocchi HTML e aggiornamento di link semplici esistenti, con schema sicuro e ancore locali esistenti; importazione di PNG/JPEG/WebP/GIF locali verificati, con firma/decodifica/limite 1,5 MiB, incorporati come data URI, alt e didascalia. SVG, indirizzi immagine remoti e URL di collegamento pericolosi non sono accettati. Figura e link usano selezione, storia, spostamento, salvataggio e export del documento; la descrizione accessibile resta distinta dalla didascalia editata.

**Esercizio:** [CI 45135851508](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45135851508) con test [`media-links.browser.py`](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/tests/metaeditor-neutral-media-links.browser.py) su file locali Linux Chrome, 2 topologie × 2 viewport, includendo URL negati, SVG negato, PNG valido, modifica alt, trasferimento, storico a tre passi, salvataggio/reopen ed export pulito. L'arresto della prima CI dopo l'estensione dell'alt derivava da **assert obsoleti sul test**, non da un'immagine sparita: corretto conservando l'ordine causale delle modifiche. Altri job di regressione indipendenti invariati.

**Confini ancora aperti:** editing media più ricco, gestione del peso e delle dimensioni delle pagine, layout complessi, accessibilità, Windows fisico e prodotto pubblicabile; il collaudo dell'operatore rimane differito come richiesto. PR draft, nessun deploy. Il criterio e le distinzioni sono nella [GUIDE](GUIDE.md).

## 23 novembre — Incolla e salvataggio propri, CI verde, prova umana differita

**Stato della candidata:** il [controller statico neutro](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/examples/collaborative-communication-medium/meta-editor-lab/neutral-static-page-editor.js) gestisce `paste` come testo semplice soltanto, rifiuta il contenuto HTML/drop nel blocco e protegge la struttura di titoli/paragrafi da Enter nativo. `Ctrl+S` richiede il download del **file di lavoro modificabile**, non Save Page di Chrome; stato modifiche calcolato sulla differenza dalla copia aperta, con ritorno a pulito dopo Undo completo, tentativo `beforeunload` su modifiche pendenti. Non si dichiara il download salvato senza ricevuta del browser/disco.

**Evidenza:** [CI 45133248996](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45133248996) quattro job verdi, inclusi [test paste/drop `file://`](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/tests/metaeditor-neutral-paste.browser.py) sintetici, [download reali e Ctrl+S su tutti e quattro i modelli](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/tests/metaeditor-starter-chooser.browser.py), ricostruzione work/reopen/export/undo, Studio21 IT/EN e documento MAIOS live source-identical. Questo prova il percorso Chromium Linux, non l'integrazione nativa clipboard/Windows.

**Direzione selezionata:** l'utente rimanda i test umani fino a quando il prodotto avrà maturità sufficiente; quindi non chiedere un nuovo collaudo a ogni versione. Proseguire con audit funzionali e regressioni per i blocchi ancora aperti (materiali multimediali, riferimenti, accessibilità, affidabilità di export e UX), lasciando priorità al comportamento reale del documento e alla coerenza con le competenze esistenti. Gate B ancora parziale, PR #2 draft, nessun deployment.

## 23 novembre — Primo avvio con scelta del modello (candidato esercitato)

**Differenza risolta nel candidato:** l'operatore osserva che partire direttamente da una pagina vuota o da un solo file dimostrativo è difficile per chi prende confidenza con MetaEditor. La nuova [schermata di selezione](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/examples/collaborative-communication-medium/meta-editor-lab/starter-templates/Apri_MetaEditor.html) offre pagina essenziale, progetto/servizio, articolo e pagina minima. [Builder e contratto](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/examples/collaborative-communication-medium/meta-editor-lab/starter-templates/README.md) realizzano un ZIP offline con quattro copie lavoro autonome: scegliere non sostituisce un'altra sessione né cambia l'originale. Distinta da template JSON delle scene MetaCanvas.

**Evidenza:** [Actions 45124239776](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45124239776) quattro job verdi; [test browser](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/tests/metaeditor-starter-chooser.browser.py) ha esercitato tutti i quattro percorsi con `file://`, editor, modifica, inserimento, riapertura, Undo esatto e modello immutabile a 1440/390. Artifatto ZIP `metaeditor-template-starter-pack` ID `14795300603`. Scaricato, estratto e ispezionato; visualizzazione della galleria senza errori. Non è attestata ancora la comprensione reale in Chrome Windows, né la pubblicazione.

**Prossimo passo:** valutazione dell'operatore sulla prima scelta e sulle prime modifiche; poi eventuale rifinitura delle card e dell'onboarding. PR #2 draft, Gate B parziale, produzione invariata. Nuovo metodo e differenze nella [GUIDE](GUIDE.md).

## 22 novembre — UI neutra contestuale verificata, prova Windows v3 ancora aperta

**Capacità candidata:** in [neutral-static-page-editor.js](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/examples/collaborative-communication-medium/meta-editor-lab/neutral-static-page-editor.js) il pannello ora è compatto e riducibile, con selezione e inserimento in evidenza; modifica solo con selezione, formato solo durante edit, gruppo di gestione solo sui blocchi aggiunti. Messaggio di contesto dinamico, `Termina modifica` esplicito e tasto Escape coerente con la history. `workHtml` e `cleanHtml` rimangono distinti.

**Test:** [Actions 45066893656](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45066893656) quattro job verdi `verify`, `studio21-browser`, `neutral-static-browser`, `neutral-live-site-browser`. [Test UI](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/tests/metaeditor-neutral-static-page.browser.py) copre visibilità contestuale, focus/edit, termina/Escape e collasso senza drift, oltre a inserimento, gerarchia, Undo/Redo, reopen e pagina MAIOS source-identical su Linux Chrome. Visualizzazione locale in Chromium `set_content` controllata, non Windows file://.

**Pendenza:** [artefatto v3](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45066893656) `metaeditor-neutral-windows-preview`, ID `14771900985`, con HTML sintetico autonomo; prodotto anche un archivio v3 a root piatta per prova utente. L'operatore non ha ancora confermato v2/v3: Gate B resta **parziale**, PR #2 draft, produzione invariata. Da approfondire accessibilità, incolla da clipboard, ergonomia su vere pagine e portabilità Windows. Il metodo di disclosure contestuale è nella [GUIDE](GUIDE.md).

## 22 novembre — Feedback Windows: layout fuori colonna corretto nel candidato

**Osservato direttamente:** nel file HTML locale di prova Windows il pannello MetaEditor si carica, ma due titoli aggiunti compaiono sul margine sinistro fuori dalla colonna dell'autore. Non è una conferma dell'intero gate `file://`: è una prova parziale che ha rivelato un difetto concreto. Analisi del codice: inserimento/trasferimento diretto con `section.append(node)`, mentre testo e stili sono contenuti in flussi interni. La verifica precedente controllava solo appartenenza alla sezione.

**Correzione e prova:** [controller](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/examples/collaborative-communication-medium/meta-editor-lab/neutral-static-page-editor.js) modificato per collocare rispetto a un elemento testuale selezionato o a titolo/ancora autoriale della sezione, e per rifiutare destinazioni non riconosciute. Livello dei nuovi titoli relativo al titolo della sezione. [Test regressivo](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/tests/metaeditor-neutral-static-page.browser.py) ora confronta parent e coordinate dei titoli e dei trasferimenti, oltre a storia/esportazione. [CI 45059052731](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45059052731) quattro job verdi su sorgenti supportati; artefatto aggiornato per Windows v2 generato da [Actions 45059052731](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45059052731).

**Ancora da provare dall'operatore:** aprire il nuovo HTML locale v2 (il precedente non si aggiorna automaticamente), aggiungere due titoli nella prima sezione, verificarne l'allineamento e lo storico. Restano UX della toolbar, formattazione, accessibilità, sicurezza paste/HTML e Gate B–F. PR #2 draft; nessun deploy.

## 22 novembre — Gate B: pagina MAIOS identica al sorgente esercitata; parità Bridge11 circoscritta

**Prova live indipendente:** [CI GitHub 45045287380](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45045287380), **4 job verdi**: `verify`, `studio21-browser`, `neutral-static-browser` e `neutral-live-site-browser`. Il job live ha scaricato `https://maios.it/consulting-ai.html`, verificato prima il Git blob `0fda8ce0d9c1da544999d39fe5d9c05f54bc771d` identico a `maios_it/consulting-ai.html`, quindi usato il vero sorgente nel test neutro a 1440/390 Chrome Linux, senza modificare produzione. Il workflow privato su `push` mantiene la propria identità e non può essere valutato dall'endpoint usato per soli run PR; non confondere `[]` con un fallimento.

**Nuova capacità:** il [controller neutro](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/examples/collaborative-communication-medium/meta-editor-lab/neutral-static-page-editor.js) ha picker nativo degli elementi (per selezione e orientamento senza mouse), scroll al bersaglio, e azioni duplicate/delete per **blocchi aggiunti**, con Undo/Redo; non modifica per inerzia sezioni originali né duplica un nodo con ID. [Comparazione Bridge11](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/examples/collaborative-communication-medium/meta-editor-lab/BRIDGE11_COMPARISON_20261122.md) documenta anche assenze: ricerca, rich text esteso, dimensioni/colori/preview, manipolazione delle sezioni originali; nessuna parità dichiarata senza prova.

**Articolo di lavoro e gate umano:** CI ha allegato `metaeditor-neutral-windows-preview` (artifact ID `14762989805`), fixture **sintetica** e [protocollo di accettazione Windows](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/examples/collaborative-communication-medium/meta-editor-lab/WINDOWS_ACCEPTANCE_20261122.md). Disponibile per verifica dell'operatore, non ancora esercitato su Windows `file://`. Rimangono da verificare caret/focus, accessibilità, paste e HTML non fiduciato, integrazione necessaria dei gesti Bridge11, packaging e approvazione release. PR #2 resta draft; cinque asset MetaCanvas pubblici e `maios_it/main` invariati. L'apprendimento operativo dettagliato è nella [GUIDE](GUIDE.md).

## 22 novembre — Candidato neutro HTML statico: gate B avanzato, non chiuso

**Nuova candidata nel ramo [PR #2](https://github.com/GrazianoGuiducci/k-ux-ai/pull/2):** [controller static-page](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/examples/collaborative-communication-medium/meta-editor-lab/neutral-static-page-editor.js), [builder di copia lavoro](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/tools/build_metaeditor_neutral_workpage.py) e [guida precisa](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/examples/collaborative-communication-medium/meta-editor-lab/NEUTRAL_WORKPAGE.md). Sorgente HTML autore immutabile; copia lavoro conserva identità dei blocchi aggiunti anche su Undo e dopo riapertura; export pulito preserva il resto del file, rimuove marcatori e torna byte-identico su no-op/Undo completo. Non riusa o pubblica contenuti di pagine MAIOS in bozza.

**Prova:** [CI 45043342858](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45043342858) tre job verdi, inclusi quattro scenari browser (Chrome Linux, 1440/390 × due strutture): fixture sintetica simil-MAIOS e MDN originale CC0 non-MAIOS. Editing, bold nativo, inserimento, spostamento tra sezioni, Undo/Redo, salvataggio e riapertura, export con head/footer intatti, annullamento completo. La prima rappresentazione di history che scartava `data-local-block` è stata corretta; test di marcatori ristretto a `main` invece che al testo JS dell'intero file.

**Owner/site e pendenza:** il ramo privato `maios_it/work/metaeditor-current` contiene ora un workflow di test in sola lettura per `consulting-ai.html` vero (Git blob `0fda8ce...`), con K-UX-AI candidato pin, ma **nessuna ricevuta CI privata disponibile** da questo receiver. Nessun deploy, nessuna mutazione a `maios_it/main`; originali pubblici MetaCanvas intatti. Restano prova reale MAIOS, più gesti Bridge11 da integrare o delimitare, sicurezza HTML, touch, accessibilità, Chrome Windows file://, Gates B–F e release IT/EN. Leggere la [GUIDE](GUIDE.md) per la differenza tra stato di lavoro, prova ed export.

## 22 novembre — Proiezioni private e ritorno AI: candidato verificato, pubblico invariato

**Difetto originale documentato:** un link marcato `private:true` fra nodi pubblici restava nella copia HTML pubblica, nell'AI JSON senza appunti e nei template, benché `publicSceneForComparison` lo escludesse già. [Test caratterizzazione](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/tests/metaeditor-studio21-privacy.browser.py) sul runtime vero IT/EN. Non confondere con un link pendente a nodo privato, già filtrato.

**Correzione candidata, non release:** [builder proiezioni](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/tools/build_studio21_public_projection.py) applicato al candidato Arrow in directory temporanea, con quattro esclusioni esplicite `l.private!==true`; HTML distribuiti e sito invariati. [CI 45040754731](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45040754731) entrambi i job riusciti: dati lavoro preservati, HTML pubblico/AI/template senza link privato, immagini remote respinte in import, [handback JSON selettivo](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/tests/metaeditor-studio21-ai-roundtrip.browser.py) con modifiche pubbliche integrate, note/link locali protetti, Undo/Redo, precedenti prove di movimento mantenute. Prove Chrome Linux IT/EN 1440/390 su fixture sintetica.

**Prossimo discriminante:** privacy di testi e dettagli non marcati, import/template avversi più ampi, touch/annidamento, accessibilità e Chrome Windows file://. PR #2 draft, nessun merge, nessun deploy né attestazione di sicurezza universale; l'owner [GUIDE](GUIDE.md) conserva la distinzione proiezione / legame privato / rappresentazione delle note.

## 22 novembre — Drag di sezione composto: regressione pointer verde

**Prova nuova e separata da Arrow:** sul ramo [PR #2](https://github.com/GrazianoGuiducci/k-ux-ai/pull/2) il [test reale pointer](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/tests/metaeditor-studio21-pointer-relations.browser.py) trascina una sezione con tre figli (due card e una immagine) e due link (interno/esterno). Verifica il bersaglio reale prima del gesto e poi salva ed esamina il modello, preservando coordinate relative, `containerId`, immagine, ID/endpoint dei link, geometria del percorso, Undo/Redo.

**Esito:** [CI 45040063638](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45040063638), job `verify` e `studio21-browser` riusciti. Otto esercizi di drag: Studio21 originale/candidato × IT/EN × 1440/390. Il precedente [run 45039940356](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45039940356) falliva su un gesto simulato non qualificato, senza dimostrare un bug del controller. La correzione del test non altera la sorgente pubblica. Il metodo di hit-target e la distinzione delle prove sono nella [GUIDE](GUIDE.md).

**Confine:** sezione con figli diretti e due link testata in Chromium Linux con mouse; touch, annidamento, import/export/AI avversi, privacy, accessibilità, Chrome Windows e release restano aperti. La correzione Arrow resta candidata, PR #2 draft; nessun merge/deploy e nessuna prova di universalità.

## 22 novembre — Relazioni di scena: difetto dimostrato, correzione candidata verificata

**Evento:** il test del nudge di un nodo isolato in Studio21 era verde, ma non copriva un contenitore e i suoi figli. Su un modello di prova iniettato nel vero Studio21 originale, con `section`, card figlia, immagine figlia e link, [Actions 45037096198](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45037096198) fallisce perché la tastiera muove solo la sezione. Il movimento pointer aveva già la propagazione ai figli: il divario è **tra due gesti nativi**, non fra due formati.

**Risultante:** [generatore candidato IT/EN](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/tools/build_studio21_keyboard_section_move.py) source-pinned modifica un solo gestore Arrow nel runtime Studio21; figli traslati nello stesso `commit` del contenitore, no-op senza checkpoint. [Regressione complessa](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/tests/metaeditor-studio21-relations.browser.py) verifica la serializzazione effettiva, immagine e link senza alterazioni di identità/estremi, percorso geometrico aggiornato e Undo/Redo. [CI 45037298632](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45037298632) ha entrambi i job verdi IT/EN a 1440/390, comprese le precedenti prove di inserimento/nudge.

**Distinzioni:** modello fixture di test ≠ contenuto autore; build candidata in directory temporanea ≠ file pubblico rilasciato; controllo strutturale sul documento esportato ≠ mera osservazione del DOM. La PR #2 rimane draft, `maios_it/main` e i 5 download pubblici intatti. Da provare separatamente: trascinamento complesso, touch, più contenitori annidati, import/AI roundtrip, privacy, accessibilità e Chrome Windows `file://`. Il Gate B/C migliora ma non è globalmente chiuso.


## 22 novembre — Spostamento nativo distinto: pagina e scena

**Risultante esercitata:** nel ramo K-UX-AI della [PR #2](https://github.com/GrazianoGuiducci/k-ux-ai/pull/2) è stato aggiunto [`metaeditor-native-move.js`](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/examples/collaborative-communication-medium/meta-editor-lab/metaeditor-native-move.js), con [contratto e limiti](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/examples/collaborative-communication-medium/meta-editor-lab/MOVE_COMMANDS.md). Non sostituisce un controller: nella pagina delega il riordino del blocco aggiunto al `transfer` di Bridge11; nella scena emette un solo nudge nativo di 5 unità, tramite keydown del nodo renderizzato, con `commit` e history proprie di Studio21. L'omonimia di `move` non implica equivalenza fra riferimenti strutturali HTML e geometria `ccm.document.v1`.

**Correzione dal secondo portatore:** il controllo di destinazione inizialmente cercava solo `main > section`, producendo un falso errore nella R3 MDN organizzata in `main > article`; ora usa l'insieme delle regioni già supportate dall'adattatore. I movimenti nulli e gli ancoraggi non validi vengono rifiutati; se lo spostamento è impossibile non viene inventato un effetto né un nuovo storico. Studio21 vieta il nudge nella modalità lettura/presentazione.

**Prove:** Playwright locale su Bridge11 e R3 a 1440/390 con before, end, attraversamento di sezioni Bridge11, Undo/Redo e no-op; test privato riproducibile nel workbench `maios_it`. [Actions 45035705911](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45035705911) ha esercitato Studio21 reale IT/EN a 1440/390, movimento, ID conservati, Undo/Redo e read mode; sei test Node passati, [Actions 45035753475](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45035753475). **Gate B ancora parziale:** spostamenti complessi di contenitori/collegamenti, distribuzione, ergonomia e altri gate sono distinti. Nessun deploy.


## 22 novembre — Studio21 IT/EN reale: inserimento e history esercitati in CI

**Differenza di prova:** il contratto `MetaEditorCompositionCommands.execute('insert')`, che prima aveva solo un mock per il modello di scena, è stato esercitato sui veri HTML pubblici Studio21 IT/EN attraverso [Playwright browser test](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/tests/metaeditor-studio21-composition.browser.py) nel ramo candidato K-UX-AI. Il test carica gli HTML standalone originali in Chrome Linux, con origine HTTP locale simulata e richieste di rete bloccate; misura i nodi `#canvas .node[data-id]`, la nascita di un solo ID nuovo, la conservazione degli esistenti e `#undoBtn/#redoBtn` nativi. Dopo il Redo inserisce anche un `card`. Le richieste con tipo pagina e `position` pagina sono rifiutate senza effetti.

**Evidenza:** [GitHub Actions run 45030544046](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45030544046), jobs `verify` e `studio21-browser` completati con `success`, 1440×844 e 390×844 su versioni IT/EN, nessun pageerror nel percorso. Il primo run 45030431494 falliva **prima** dell'esercizio per installazione Chromium nel runner; è stato corretto il mezzo di prova usando Chrome presente nell'immagine Actions. Non attribuire il fallimento iniziale al prodotto.

**Effetto e confini:** il contratto comune ha adesso evidenza browser sui due carrier di pagina (Bridge11 e R3 MDN) **e** sul vero carrier di scena Studio21. Non ne consegue ancora rilascio: spostamento/diagrammi/template, usabilità, file:// Chrome Windows, accessibilità e tutti i gate rimanenti sono separati. Nessun download pubblico o documento di cliente modificato.


## 22 novembre — Composizione: un comando di inserimento, due motori nativi

**Risultante concreta:** dopo l'export browser R3, il ramo candidato K-UX-AI contiene [`metaeditor-composition-commands.js`](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/examples/collaborative-communication-medium/meta-editor-lab/metaeditor-composition-commands.js), con [contratto e limiti](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/examples/collaborative-communication-medium/meta-editor-lab/COMPOSITION_COMMANDS.md). L'azione `insert` è una richiesta condivisa; su pagina usa il controller `addBlock`, su Studio il nativo `addNode`/`commit`. Non inventa un documento comune, history o toolbar. I tipi e la posizione supportati sono specifici del carrier: pagina `paragraph/heading/list/callout` (end/before/after dove consentito); scena `text/card/tag/section/circle/oval/pill/note` senza semantica della posizione pagina. `move` non è ancora estratto.

**Prove distinte:** 6 test Node del contratto e GitHub Actions della PR #2 verdi sul commit dei test; Chromium 1440/390 su vero Bridge11 e R3 MDN con inserimento/Undo e nessun pageerror nel percorso. Il carrier di scena è stato letto nella sorgente Studio21 e verificato finora contro pulsanti nativi **simulati**, non con un browser test dello Studio21 completo. Il test browser riproducibile è nel workbench privato `maios_it/work/metaeditor-current/workbench/metaeditor/experiments/test_composition_native_bridge.py`.

**Correzione emersa:** quando un target esplicito cambia sezione ma il punto `before/after` non è valido, il comando deve ripristinare la selezione originale. Test di regressione aggiunto. Il controller nativo mantiene il solo Undo del documento. **Gate B ancora parziale, PR in bozza, prodotto e sito pubblici invariati.**


## 22 novembre — Sorgente immutabile: esportazione browser estratta dalla R3

**Nuova risultante esercitata:** la logica di confronto/esportazione della R3 non è più soltanto dentro il file MDN. Un [adattatore JavaScript condiviso](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/examples/collaborative-communication-medium/meta-editor-lab/static-page-source-adapter.js) risiede nel ramo candidato K-UX-AI e offre `MetaEditorStaticPageAdapter.create({sourceHtml, regionElement, runtimeRootAttributes})` con `exportHtml()` e scansione conservativa di un unico `main`. Distingue testo in commenti/script/attributi, rifiuta `main` ambigui, markup attivo nella regione, attributi riservati e variazioni non autorizzate della radice; rimuove marcatori dell'editor solo dalla copia. Con no-op restituisce il testo sorgente esatto; con modifica sostituisce solo il contenuto della regione. È una **capacità di export dal browser**, non un importatore e non un editor completo.

**Evidenza:** Node --check e tre test del riconoscimento nel runner Node, prove Chromium su documento MDN e fixture differente a 1440×844 e 390×844; integrazione nel vero HTML R3 con UI Codex, inserimento, Undo e export, zero pageerror nei casi. L'[HTML integrato](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/workbench/metaeditor/experiments/MetaEditor_MDN_R3_Shared_Source_Adapter_20261122.html) è stato committato nel workbench privato con Git blob `2b2a6045fe2faf56f34b4730db6310c5ed11b65e` corrispondente al file localmente esercitato; builder SHA-guarded conservato accanto. `CURRENT.html` Bridge11 e il prodotto MetaCanvas pubblicato non sono stati modificati.

**Distinzione di competenze:** `tools/metaeditor_region_patch.py` nel ramo candidato possedeva già la sostituzione delimitata della sorgente nel ricevente Python. Non duplicarne l'autorità: la variante JS applica il contratto **nel browser**, confrontando il DOM pulito con una baseline immutabile. Entrambe sono primitive limitate a pagine statiche riconosciute, non sostituti dei gesture/editor di pagina o di `ccm.document.v1`. **Gate B ancora parziale**: restano un adapter pagina coerente sul secondo documento, suite di comportamento più ampia e verifica umana. Nessun deploy o release.


## 22 novembre — Portabilità R3 su HTML esterno: sorgente immutabile ed export fedele

**Evento verificato:** dopo il banco neutro R2 è stata selezionata una seconda topologia HTML: la pagina `mdn/learning-area/html/introduction-to-html/document_and_website_structure/index.html`, sorgente CC0-1.0 del repository MDN, con `main > article`, sottosezioni, `aside` laterale, header/nav/form e stylesheet esterno. Il file originale è stato confrontato con il Git blob MDN `0a2636f1c1bb30ffa6515141c831e348b9bd6150`; la pagina sperimentale R3 e il suo builder/test sono conservati nel [workbench privato](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/workbench/metaeditor/experiments/README.md).

**Risultante:** MetaEditor R3 SHA-256 `8af2f8b18605f25f8a0e2da9e965c46364cb2756964699c52af7ef940cf75189`, Git blob `5b1dcb244dfcfc9d90f545174ce2a58ae5eb4734`. L'esercizio via Chromium `set_content` a 1440×844 e 390×844 dimostra selezione articolo, inserimento, Undo/Redo, export statico *byte-identico all'HTML di partenza quando non ci sono modifiche*, export modificato confinato a `main`, salvataggio e riapertura del lavoro con un unico editor e seconda esportazione corrispondente. Nessun `pageerror` nei percorsi.

**Difetto corretto nel test:** dopo la riapertura l'export di una versione precedente prendeva come baseline il DOM di lavoro già modificato, rischiando di restituire l'originale e perdere gli interventi. La baseline ora proviene dalla **sorgente originale immutabile incorporata** nel portatore. La differenza causale cambia il metodo della competenza, non solo un pulsante.

**Confini:** builder ancora source-pinned al caso MDN e derivato dal portatore Bridge11 privato; CSS originale resta come asset separato e i font esterni non sono offline. HTML arbitrario/CMS/React e script non fidati non sono supportati; nemmeno file:// Windows, touch, accessibilità generale o il rilascio pubblico sono provati. Gate B progredisce ma **non è chiuso**. La PR #2 resta in bozza.


## 22 novembre — Stabilizzazione selezionata e prima prova di portabilità R2

**Fonte dell'operatore:** «Finiamo di fare tutto quello che serve fare per fare bene, l'obiettivo finale è pubblicare tutto e stabilizzare il progetto metaeditor e metacanvas». Questo cambia il bersaglio dalla prosecuzione di prototipi sequenziali a un **prodotto verificabile e distribuibile** senza perdere identità, contenuto o capacità dei carrier distinti.

**Riconciliazione delle sorgenti:** i cinque file pubblici MetaCanvas (editor generale, Playground IT/EN, Studio21 IT/EN) sono già distribuiti su MAIOS.it e i loro blob Git coincidono con le fonti K-UX-AI. L'editor generale canonico corrisponde alla copia site `editor-generale-aaa6702-it.bin` (Git blob `d057d68c60061dd9e8f5c2d704cfff2016ea19b1`), **non** alla precedente copia `studio-20-it.bin`; la distinzione viene corretta nei documenti di una [PR candidata K-UX-AI #2](https://github.com/GrazianoGuiducci/k-ux-ai/pull/2), non ancora fusa. Il workflow di preflight ha terminato con successo una prima esecuzione; non prova un rilascio nuovo né tutte le funzioni.

**Primo esperimento neutro:** il portatore privato Bridge11 è stato trasposto su un documento sintetico non MAIOS, salvato come [MetaEditor Neutral Probe R2](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/workbench/metaeditor/experiments/MetaEditor_Neutral_Probe_R2_20261122.html), SHA-256 `dab81b7ee10e003c2027eb0972ad0fc701dd90759c5a1979ffb5936a60fdeea4`, blob Git `cc27f5660e9cc687364a3a786a13cc273dd1423b`. Il [builder SHA-guarded](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/workbench/metaeditor/experiments/build_neutral_probe.py) riproduce lo stesso output dal Bridge11 esatto. Chromium desktop/mobile ha esercitato testo diretto, inserimento, movimento, Undo, salvataggio/riapertura e una pagina pulita senza runtime editor; zero pageerror nei casi. Inizialmente l'export rompeva su una nav MAIOS inesistente e poi il link del download veniva intercettato dal controller: entrambi corretti nel R2, senza cancellare la protezione.

**Limite proprietario:** neutralità di **un fixture** ≠ compatibilità con siti arbitrari: permane l'assunzione `main > section > .site-shell` e residui del carrier Codex. La variante è privata e non sostituisce `CURRENT.html` Bridge11 Consulenza o Studio21/ccm.document.v1. Prossimi discriminanti effettivi: neutralizzazione degli adapter e prova su un secondo DOM reale non-MAIOS con patch/export fedele; poi regressioni dei diagrammi, import AI e privacy, UX/accessibilità, versione IT/EN e release pubblica separata. [Gate e criteri](https://github.com/GrazianoGuiducci/k-ux-ai/blob/work/metacanvas-metaeditor-stabilization-20261122/examples/collaborative-communication-medium/RELEASE_STABILIZATION_20261122.md). Nessun push al sito né release nuova.


## 22 novembre — Bridge11: nessun problema segnalato nell'uso

**Fonte diretta dell'operatore:** «Nella versione 11 non vedo problemi». È un riscontro favorevole sull'uso della versione 11, non una nuova prova automatica di tutti i gesti e neppure una certificazione indistinta dell'adattamento Collaborazioni su HTML aggiornato.

**Conseguenza:** non inventare un difetto o riaprire un ciclo di riparazione per inerzia. La diversa versione `maios_it/main:collaborazioni.html`, aggiornata dopo la bozza di lavoro del 21 novembre, è drift del **contenuto della pagina**, non prova di difetto dell'editor Bridge11. Per evolvere il mezzo, cercare la prossima capacità realmente utile (per esempio immagini, diagrammi o composizioni riutilizzabili) dopo aver verificato quali funzioni Studio21 e altri adattatori già possiedono. Conservare inalterato Bridge11 nel workbench privato.


## 21 novembre — Bridge11 esercitato come adattamento documentale Collaborazioni

**Fonte dell'operatore:** rivedere la pagina Collaborazioni usando MetaCanvas/MetaEditor prima del passaggio a Codex, partendo dalla versione più aggiornata del repository e confrontandola, se possibile, con il sito pubblico. La forma desiderata nasce da una nuova direzione di collaborazione: «Cerco collaborazioni», ricerca fuori dal Lab, sguardo esterno sul team e trasformazione dell'esperienza in capacità.

**Sorgenti e owner:** la bozza canonica della pagina HTML è `GrazianoGuiducci/maios_it/main:collaborazioni.html` (blob `cbce790d2a713b2b3ef1b96c2c10bd1eeb01e39c`); il Bridge11 preesistente su `work/metaeditor-current/workbench/metaeditor/CURRENT.html` è portatore **Consulenza**, non Collaborazioni. La pagina pubblica `https://maios.it/collaborazioni.html` non è stata raggiungibile dagli strumenti nel turno, quindi uguaglianza fra live e main non verificata.

**Risultante nel documento owner:** nuovo [adattamento Bridge11 per Collaborazioni](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/workbench/metaeditor/collaborazioni/Collab_MetaEditor_Bridge11_20261121.html), [HTML pulito candidato](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/workbench/metaeditor/collaborazioni/CANDIDATE_SITE.html) e [handoff](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/workbench/metaeditor/collaborazioni/README.md). Il documento completo preserva le quattro sezioni originarie, aggiunge una sezione ricerca/team, aggiorna la hero e il contributo reciproco nell'accordo. I CSS `site.css` e `consulting-ai.css` sono incorporati dalla sorgente repository corrente; il supporto Bridge11 resta intatto. Il README workbench rende il portatore distinto raggiungibile senza sovrascrivere il CURRENT Consulenza.

**Prova effettiva:** file creati sul ramo non di produzione, readback Git blob; parsabilità sintattica dei tre script dell'editor verificata nel ricevente JS; controlli testuali su singolo main, singola shell editor, unicità titolo e nuova sezione. **Non** eseguite prove Chromium visuali, test Windows umano, export interattivo, confronto dei byte serviti dalla VPS, applicazione della patch a main o pubblicazione. La futura revisione umana del file può mutare la sorgente che Codex dovrà applicare. La trasformazione qui è riuso situato di competenza già esistente, non una nuova generalizzazione garantita dell'editor per qualunque sito.


updated: 2026-11-21
status: bridge11_private_workbench_source_verified; no_site_deploy

## 21 novembre — Bridge11 disponibile nel workbench privato dell'owner documento

**Risultato effettivamente consegnato:** `GrazianoGuiducci/maios_it` (privata), ramo `work/metaeditor-current`, [ingresso operativo](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/workbench/metaeditor/README.md), [`workbench/metaeditor/CURRENT.html`](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/workbench/metaeditor/CURRENT.html) = Bridge11. Conservate anche le versioni HTML integrali Bridge09, Bridge10 e Bridge11 in `workbench/metaeditor/versions/`. Le tre copie sono state create da artefatti della conversazione e verificate con i blob Git degli originali; Bridge11 SHA-256 `c0c1078db990cb658261bcc09b83cf5be92d88d825f9fa9a94a4c486d76aeecd`, blob `9f4f843124f8619eee02ece40a7efc1470881b07`. Il workbench contiene un protocollo di aggiornamento del file stabile e delle versioni.

**Confini:** nessuna modifica alla pagina `maios_it/main` o deploy del sito; GitHub privato richiede l'accesso autorizzato, e un download modificato dal browser non è ancora committato. K-UX-AI rimane owner della competenza di editing, `maios_it` owner del documento e del relativo artefatto, Codex/ChatGPT riceventi potenziali. Codice riusabile Bridge09–11 non è ancora estratto dal documento per il prodotto MetaCanvas generalizzato. Il riferimento ora è **recuperabile in repo**, non più soltanto nei file della conversazione.

## 20 novembre — Bridge11: posizionamento preciso degli elementi aggiunti

**Selezione:** l'operatore chiede di continuare dal Bridge10. Il codice possiede già drag intra-gruppo e trasferimento intersezione al fondo; la differenza da sviluppare è scegliere il **punto esatto della destinazione**, preservando gli elementi nativi e il responsive.

**Artefatto corrente della conversazione:** `MetaEditor_Bridge11_Posizionamento_Preciso_IT.html` SHA-256 `c0c1078db990cb658261bcc09b83cf5be92d88d825f9fa9a94a4c486d76aeecd`; input byte-identico Bridge10 SHA-256 `38612d819682af89172003399fe96eed7fc5494476a3015eecc3d2dbd08857ce`. Il comando nativo `transfer` ora sposta un blocco `data-local-block` nello stesso o in un altro contesto, con scelta di riferimento e prima/dopo/fine. Le ancore di riferimento sono blocchi aggiunti o testo in flusso della hero; i componenti nativi in griglia non sono candidati arbitrari. Anteprima e target highlight restano transitori e fuori dall'export. Gli spostamenti nulli non registrano undo né marcano sporco tramite il listener generale.

**Prove reali di laboratorio:** Node --check su 3 script; Chromium set_content desktop 1680×900 e mobile 390×844: 4 sezioni originarie; titolo nativo non trasferibile; spostamento tra sezioni; riordino locale; Undo/Redo a un checkpoint; no-op e successivo Undo che torna al movimento reale; inserimento prima dell'H1 hero con ID e layout conservati; export HTML e riapertura con un'unica UI, nessun marcatore target e nessun pageerror nei percorsi provati. La verifica dell'operatore su Chrome Windows della nuova variante, altri siti, touch e Studio21 resta da compiere. **Nessun deploy e nessuna mutazione di Codex o MAIOS.it.** [GUIDE](GUIDE.md) e [SKILL](SKILL.md) custodiscono la funzione.

## 20 novembre — Bridge10: inserimento contestuale nel referente

**Selezione presente:** dopo la conferma Bridge09, l'operatore domanda ulteriori migliorie. È stata esercitata una direzione già aperta, **comporre la pagina nel punto scelto** riutilizzando l'inserimento nativo della bozza Codex.

**Artefatto:** `MetaEditor_Bridge10_Inserimento_Contestuale_IT.html`, unico HTML offline di conversazione, SHA-256 `38612d819682af89172003399fe96eed7fc5494476a3015eecc3d2dbd08857ce`, derivato dall'esatto Bridge09 SHA `e58ef0f889508e59027b908188a03ba153e7182081767479697feb93611ab2a3`. Pulsante `+` di inserimento prima/dopo per paragrafo, sottotitolo, elenco e riquadro, ancora nativa `insertionAnchor` e `addBlock`; in spazi stretti la stessa UI va accanto al selettore elementi. Il file precedente resta byte-identico e il sito non cambia.

**Esercizio tecnico:** Node `--check` dei tre script, Chromium desktop 1680×900 e mobile 390×844: scelta, menu, inserimento, Undo/Redo, export work HTML senza shell me10 serializzata e riapertura con una sola UI, zero pageerrors. Test separato su inserimento `before` accanto a H1 e chiusura Esc. La prima prova ha trovato un click soppresso dal controller `blockPageAction` quando il nuovo pulsante viveva fuori da `#local-editor`; corretto portandolo nel perimetro editoriale. La seconda ha scoperto che il pannello copriva il pulsante su 390px; corretto mediante fallback inline nella picker-row. **Prova umana Chrome Windows di Bridge10 ancora aperta**. Non estendere queste prove al MetaCanvas pubblico o a Studio21.

**Continuità:** il prossimo gesto reale dell'operatore può valutare se il `+` è percettibile e il menu consente di lavorare con meno passaggi. Conservare [GUIDE](GUIDE.md) e [SKILL](SKILL.md) come owner di metodo; la creazione in conversazione non è di per sé release o installazione di un nuovo editor.

## 20 novembre — Bridge09: navigazione e focus della selezione

**Sorgente:** conferma dell'operatore nel Chrome Windows reale che Bridge08.1 ora funziona, seguita dalla richiesta di scorrere automaticamente verso gli oggetti scelti e di introdurre altre facilitazioni. Lo screenshot mostra la sezione 2 scelta nel pannello mentre parte del suo contenuto resta sul bordo inferiore dello schermo.

**Nuovo artefatto sperimentale:** `MetaEditor_Bridge09_Focus_Contestuale_IT.html`, derivato dall'esatto Bridge08.1 (input SHA-256 `9dbbf5b5337aa94a8252e9624fab2c75a2ded7dd555db5d9b675501d73fe8e0c`; output SHA-256 `e58ef0f889508e59027b908188a03ba153e7182081767479697feb93611ab2a3`). Introduce `revealSelection` per le scelte esplicite da sezioni, blocchi, ricerca e palette; pulsante ◎ per riportare in vista l'elemento selezionato; allineamento con il viewport e la barra inferiore; nessuno scroll in seguito a normali eventi di editing.

**Esercizio osservato:** Node --check sui tre script; Chromium `set_content` desktop 1680×900 e mobile 390×844: scelte, ricentratura, singola selezione, edit rich-text e export/riapertura senza raddoppio della UI o marcatori nel documento, zero pageerrors. Ricerca elementi e palette sono state esercitate in una prova separata. La nuova versione non è ancora stata provata dall'operatore in Chrome Windows; file:// è bloccato nel runner. Nessun deploy del prodotto pubblico, modifica a MAIOS.it o Codex. [GUIDE](GUIDE.md) conserva il metodo.

## 20 novembre — Bridge08.1: evidenza umana della doppia selezione, correzione puntuale

L'operatore ha provato il vero `MetaEditor_Bridge08_Bozza_Codex_IT.html` in Chrome Windows e ha documentato con screenshot un titolo selezionato strutturalmente mentre è in modifica il testo di un altro riquadro. La [competenza ha isolato e corretto la mancata sincronizzazione](references/BRIDGE08_1_SELECTION_HANDOFF_20261120.md): il ramo diretto di `dblclick` nascondeva Struttura senza `syncTools(section)`. Bridge08.1 sincronizza il referente corrente, rimuove i contorni passati e conserva il cursore del campo rich text; la barra inferiore rende percepibile quale testo è attivo.

**Stato effetti:** `MetaEditor_Bridge08_1_Selezione_Coerente_IT.html` è un file di prova nella conversazione, ricostruibile con lo [script K-UX-AI SHA-guarded](../../../../examples/collaborative-communication-medium/meta-editor-lab/bridge08_1_selection_fix.py). Test Node e Chromium: prima/dopo, riapertura Struttura, nuovo referente, Esc, setText/commit, Undo/Redo, export/reopen con una sola UI e mobile 390 px. Nessuna modifica al prodotto pubblico, a MAIOS.it o al checkout Codex. **La prova Chrome Windows dell'esito corretto resta da fare**, distinta dalla prova umana del problema.

**Direzione aperta:** proseguire con inserimento e composizione degli elementi a livello pagina, preservando selezione e proprietà della scena. Non introdurre un nuovo pannello per compensare il passaggio di stato.


updated: 2026-11-19
status: bridge08_ux_layer_committed_two_adapters_browser_tested; no_public_release

## 19 novembre — Bridge08 rende raggiungibili capacità esistenti

L'operatore ha scelto di affinare le funzioni e l'intuitività, dopo il contratto di comando Bridge07. [Bridge08 / apprendimento owner-native](references/BRIDGE08_UX_ACTIONS_FOCUS_20261119.md) e i file `bridge08_ui.js`, `bridge08_ui.css`, `bridge08_build.py` nel laboratorio K-UX-AI sono stati committati. Due HTML sperimentali scaricabili in conversazione riusano i portatori esatti Bridge07 (Codex rich text e Studio21 `ccm.document.v1`), senza sostituire Studio pubblico, MAIOS.it o il checkout Codex.

**Verificato in Node/Chromium:** ricerca azioni e navigazione con Ctrl+Maiusc+P, F2 nativo, focus e formattazione progressiva, navigazione fra sezioni/schede e inserimento testo Studio, export e riapertura con una sola interfaccia, Studio public copy priva di elementi/script/style UX08, mobile 390px senza overflow orizzontale nel test e nessun pageerror nei percorsi. Il canvas Focus Studio nel test 1360 px cresce da circa 1019 a 1150 px. La prima doppia UI serializzata e la griglia Focus sbagliata sono state corrette; il metodo è in GUIDE.

**Resta aperto:** prova manuale file:// su Windows, accessibilità/touch, confronto sui gesti dopo uso reale, adattatore di regioni HTML su un secondo sito, e messa a regime nel prodotto pubblico. Il prossimo lavoro non è scelto da CURRENT; la competenza è disponibile quando serve.


updated: 2026-11-19
status: bridge07_native_shared_commands_exercised; builder_committed; public_product_unchanged

## 19 novembre — Bridge07: contratto di editing condiviso, esecuzione nativa

I due HTML `MetaEditor_Bridge07_Bozza_Codex_IT.html` e `MetaEditor_Bridge07_Studio21_IT.html` sono artefatti **di conversazione** derivati dagli HTML Bridge06 già verificati, non nuovi file canonici distribuiti in MAIOS.it. Il [builder](../../../../examples/collaborative-communication-medium/meta-editor-lab/bridge07_build.py) è in K-UX-AI con readback identico. [Contratto/esperienza/prove](references/BRIDGE07_NATIVE_COMMAND_CONTRACT_20261119.md) distingue rich text del Codex editor dalla label stringa Studio21; in entrambi F2/Ctrl+Invio/Esc e Undo/Redo agiscono via metodi nativi.

**Risultati tecnici osservati:** testo parziale con markup esterno preservato; Esc recupera `innerHTML` e history originali; Ctrl+Z/Y funzionano dopo che Undo riporta il caret in `contenteditable`; scena Studio21 resta `ccm.document.v1` con sette scene e public copy che filtra note, nodi privati e template sintetici; export/riapertura dei due HTML conserva il Bridge07; mobile 390px senza overflow globale nel campione. I difetti di sessione stale dopo blur e redo perso col focus sono tornati alla GUIDE e al builder.

**Limiti:** non prova Chrome Windows file://, accessibilità completa, siti HTML arbitrari, editing rich text nelle label Studio o sostituzione di MetaCanvas Studio20/21 pubblico. Nessun deploy, nessuna modifica al checkout di Codex o alla pagina MAIOS. Prossimo discrimine: esperienza reale dell'operatore sul gesto e region adapter con patch selettiva su due pagine.


updated: 2026-11-19
status: bridge06_two_source_gesture_tested_in_Chromium; source_bound_builder_committed; no_public_release

## 19 novembre — primo ponte reale Codex / Studio21, senza unificazione dei modelli

I due esperimenti HTML `MetaEditor_Bridge06_Bozza_Codex_IT.html` e `MetaEditor_Bridge06_Studio21_Consulenza_IT.html` sono stati costruiti in conversazione (file scaricabili), non installati nel sito. Il [builder owner-native](../../../../examples/collaborative-communication-medium/meta-editor-lab/bridge06_build.py) ricrea le varianti da sorgenti originali con SHA verificati. La [prova completa](references/BRIDGE06_COMMON_GESTURE_20261119.md) registra modifica diretta del testo rich in Codex senza inspector forzato, modifica diretta della label in Studio21, export/riapertura separati e capacità privacy/template/link preservate. Le patch sono limitate a un gesto, non a un nuovo editor generale.

**Nuova differenza assimilata:** pointer capture dello Studio21 cambia l'evento target del secondo clic; il test iniziale falliva. `elementFromPoint` recupera il referente effettivo. Il test Bold su un H1 ha esercitato una disattivazione corretta, riformulata poi come selezione Italic. L'intervento non altera i sistemi di formattazione e dati rispettivi. Test Node/Chromium e viewport mobile sì; file:// Chrome Windows, accessibilità/touch e siti reali differenti non provati.

**Prossimo discriminante:** comando `setText`/commit/cancel/undo su due adapter con focus e caret coerente, preservando il DOM/markup Codex e il modello scene Studio. Ancora nessun cambio delle copie `maios_it` o dei prodotti pubblici.


updated: 2026-11-19
status: public_tool_and_codex_rich_editor_source_field_reconciled; no_new_product_release

## 19 novembre — nuova fonte Codex e MetaCanvas pubblico restituiti alla competenza

L'operatore ha corretto l'ambito: **MetaCanvas è già un tool pubblico MAIOS, incompleto**, e una sua bozza HTML attualmente usata con Codex offre editing di testo ricco e altre funzioni che i Lab/R5 non avevano conservato. Il [nuovo inventario owner-native](references/SOURCE_FIELD_PUBLIC_TOOL_CODEX_DRAFTS_20261119.md) distingue pagina pubblica, Playground IT/EN, Studio20 generale, Studio21 demo IT/EN, Codex page-editor, Lab01–05, vecchia R5 specifica e Siteman Studio. L'allegato Codex di 419.563 byte è stato letto e controllato con Node e Chromium su un percorso delimitato; non è stato importato nel prodotto, né sostituito. La difficoltà UX è coerente con la sovrapposizione effettivamente osservata fra toolbar testuale e inspector globale.

**Regola operativa ora raggiungibile:** il prossimo sviluppo deve preservare contemporaneamente formattazione/selection/caret Codex, schema/note/template/pubblico/AI merge Studio20, gestione dei diagrammi Lab05 e origine/revisioni/patch del sito, senza fare coincidere i tre modelli di stato. La R5 della vecchia R4 è evidenza separata, non sorgente canonica. La ricognizione non prova l'HTML distribuito effettivamente servito dal server, browser Windows fisico o compatibilità universale.

**Effetti:** aggiornati metodo e routing della competenza; nessun commit sul runtime pubblico, nessun merge, nessun asset sostituito e nessun sito pubblicato.


updated: 2026-11-19
status: first_R4_MAIOS_page_adapter_R5_conversation_artifact_tested; no_site_or_studio_deploy

## 19 novembre — prima prova su pagina R4 MAIOS, R5 locale

Dopo Lab05 l'operatore ha scelto «l'ultima pagina di MAIOS MetaCanvas già usata». È stata riaperta l'esatta `MAIOS_Consulenza_MetaCanvas_R4_Editor_Contestuale_IT.html`, diversa dall'attuale sorgente produttiva MAIOS. La [prova R4→R5](references/first-real-page-r5-20261119.md) ha prodotto un HTML sperimentale consegnato nella conversazione: un solo dock, modifica diretta, inserimenti dentro le quattro regioni, diagramma con testo dei nodi editabile in loco e azioni collettive contestuali. Possiede esportazione di progetto riapribile, HTML statico e patch JSON **a livello di regione** vincolata alla R4 originaria.

**Prova:** Chromium/Node con patch vuota su documento invariato, una sola regione hero modificata dopo due interventi, file progetto riaperto con una UI, clean export senza editor, immagine e colonne salvate, viewport 390 senza overflow globale, nessun pageerror nei percorsi esercitati. Sono stati corretti re-render su click che impediva il doppio clic reale, serializzazione errata del progetto, false differenze causate da attributi editor e sovraccarico della toolbar. Il browser amministrato blocca `file://`; non attribuire l'uso Windows reale o un sito modificato.

**Confini:** codice R5 della pagina non aggiunto a questa repository, Studio20/21 e Lab05 restano distinti, MAIOS.it non modificato, Codex non attivato. Resta aperto un secondo sito diverso e la ricognizione della pagina produttiva corrente **prima** di autorizzare l'applicazione di eventuali patch.


updated: 2026-11-19
status: Lab05_spatial_nodes_committed_and_chromium_exercised; Chrome_Windows_human_unobserved

## 19 novembre — Lab05 disponibile, strumenti spaziali dei diagrammi

L'operatore ha chiesto di migliorare l'editor generale con gesti più efficaci, aiutandosi con le UI di strumenti esistenti. La nuova risultante [Lab05 HTML](../../../../examples/collaborative-communication-medium/meta-editor-lab/MetaEditor_Lab05_Diagrammi.html) mantiene Lab04 e aggiunge gestione di **più nodi dello stesso diagramma**: Maiusc+clic, allineamento/distribuzione, spostamento collettivo, duplicazione con ricostruzione dei link, griglia, inserimento tramite doppio clic direttamente nell'area e modifica del testo immediata. [Il README](../../../../examples/collaborative-communication-medium/meta-editor-lab/LAB05_README.md) registra fonte, prove e limiti. Sono state corrette due collisioni effettive (copie e nuovo nodo in uno spazio occupato), crescita del canvas e la creazione di un Undo fittizio per allineamenti senza variazione.

**Prova:** Node v22 + Chromium headless Playwright `set_content`: gesti di selezione, gruppo, drag, Undo, copia, relazione di link, riapertura HTML e mobile 390px senza overflow nel caso; nessun pageerror osservato. La repository ha il codice di laboratorio, non un rilascio Studio20/21 o un editor universale installato. La pagina MAIOS.it, D-ND.com e il codice Codex rimangono invariati.

**Prossimo discrimine**: utilizzo umano su Chrome Windows e, quando selezionato, un primo adapter su regioni HTML dichiarate e patch sicura, verificata su una seconda pagina diversa; questo Lab05 non ha esercitato quell'adapter.


updated: 2026-11-17
status: Lab04_multi_selection_committed_and_browser_exercised; human_file_url_usability_unobserved

## 17 novembre — Lab04 gesti multipli, prima della compatibilità con siti veri

Il [Lab04 HTML autonomo](../../../../examples/collaborative-communication-medium/meta-editor-lab/MetaEditor_Lab04_Manipolazione.html) è presente in K-UX-AI con [test, limiti e contratto](../../../../examples/collaborative-communication-medium/meta-editor-lab/LAB04_README.md). Il nuovo saper fare è composizione collettiva di blocchi della pagina: Maiusc+clic, copia/taglia/incolla interno all'editor, duplica/elimina/sposta insieme, shortcut e un Undo per azione. Conserva diagrammi, nodi, collegamenti e temi. Non supporta ancora grouping persistente o clipboard OS. Node/Chromium set_content: selezione, duplicazione, undo/redo, trasferimento fra sezioni, testo in nodo, roundtrip HTML, 390 px; nessun pageerror nei percorsi. È stato tolto il doppio luogo di Copia/Taglia e reso esplicito che gli appunti sono locali.

**Confini:** il file è un esempio prodotto/testato, non una release Studio20/21, né un adapter per pagine reali, né un deploy MAIOS/D-ND. La qualità dell'uso in Chrome Windows resta da osservare. Prossimo discriminante: regione HTML dichiarata, patch e secondo sito differente, conservando la competenza di selezione multipla.


updated: 2026-11-17
status: Lab03_object_first_editor_committed_and_browser_exercised; end_user_usability_unobserved

## 17 novembre 2026 — Lab03: competenza esercitata sulla manipolazione degli elementi

**Nuova priorità operatoria:** i temi sono subordinati alla capacità di usare davvero l'editor. [Lab03 · Gestione elementi](../../../../examples/collaborative-communication-medium/meta-editor-lab/MetaEditor_Lab03_Elementi.html) è presente in K-UX-AI come esempio HTML autonomo con [README e limiti](../../../../examples/collaborative-communication-medium/meta-editor-lab/LAB03_README.md), distinto dalle release Studio20/21 e dai siti.

**Effetti esercitati:** selezione esplicita di sezioni, gestione della struttura, proprietà di oggetto collocate in alto, inserimento contestuale, conversione titolo/testo/card, riordino e spostamento con o senza drag, nodi/collegamenti/forme, layout responsive e temi conservati. Node syntax + Chromium set_content hanno coperto editing diretto, Undo/Redo, duplicazioni, trasporto fra sezioni, relazione node-link e rimozione link, cinque nodi distribuiti senza sovrapposizione dei loro rettangoli, tema, HTML export e riapertura, viewport 390 px senza overflow globale e nessun pageerror osservato. File HTML riletto da GitHub identico ai byte condivisi della versione validata. I limiti del runner bloccano file://: nessuna prova reale Chrome Windows né valutazione d'uso dell'operatore.

**Apprendimento:** la sequenza originale di prova non guardava la densità dei nodi; una schermata ha reso evidente la collisione dei rettangoli. La nuova prova controlla anche geometria e non solo modello. La posizione dell'inspector rispetto all'outline cambia il costo del gesto: l'oggetto selezionato governa i controlli visibili, la sezione resta raggiungibile senza occupare lo spazio principale. Le ragioni e il metodo vivono in [GUIDE](GUIDE.md), la separazione degli owner in [SKILL](SKILL.md). Non è un adattatore universalmente affidabile per le pagine HTML.


updated: 2026-11-17
status: Lab02_theme_library_committed_and_locally_exercised; no_Studio_port_or_site_deploy

## 17 novembre — libreria temi e recupero di capacità dalle sorgenti

**Richiesta attuale:** temi recuperabili standard/MAIOS/D-ND/presentazione, da usare anche per rendere percepibili le possibili composizioni, mantenendo semplice il MetaEditor e connessa la competenza al lavoro. [Sorgenti, metodo, prova e limiti](references/theme-library-20261117.md) ora possiedono la risultante.

**Artefatto in K-UX-AI:** [Lab 02 — Themes](../../../../examples/collaborative-communication-medium/meta-editor-lab/MetaEditor_Lab02_Theme_Library_IT.html) pubblicato come **esempio autonomo**, readback GitHub byte-identico all'HTML del laboratorio. Non è il runtime di Studio20/21 e non modifica alcun sito.\n\n**Artefatto creato in conversazione:** `MetaEditor_Lab02_Theme_Library_IT.html` (successore del Lab01, ancora non presente nella repository come HTML). Esercitati: selezione fra 5 profili, overlay di espressioni MAIOS, modifica/creazione di tema personale con composizioni suggerite configurabili, salvataggio nel documento e in localStorage dove consentito, export/import JSON, lettura selettiva di CSS da HTML Collaborazioni, testo del diagramma ancora editabile in situ, Undo, export HTML e riapertura. Node/Chromium `set_content`, viewport 390 e screenshot MAIOS/D-ND verificati; apertura `file://` bloccata dal runner. La copia locale dell'HTML e la guida restano raggiungibili in conversazione; l'HTML di esempio è ora raggiungibile anche tramite GitHub al percorso indicato. Questo non certifica adozione in altri riceventi.

**Prossimo discriminante:** esercitare un import dichiarativo e non distruttivo di regioni HTML (minimo due siti), collegare tema e patch come stati distinti, poi considerare il trasporto del motore ai vari MetaCanvas. Codex non è stato attivato e nessun sito o release è stato modificato.


updated: 2026-11-16
owner: GrazianoGuiducci/k-ux-ai / collaborative-communication-medium / meta-editor
status: competence_formed; neutral_lab01_node_edit_browser_exercised; end_user_usability_unobserved
runtime_owner: examples/collaborative-communication-medium/ (future candidate)
distribution: no release; no MAIOS.it deployment

## Presente selezionato
L'operatore chiede una competenza dedicata che evolva il MetaEditor. La forma pertinente è una specializzazione **interna a CCM/K-UX-AI** sul metodo di progettare e verificare editor generalizzabili. L'architettura da discriminare conserva differenze fra pagina web, presentazione, diagramma, contenuto originale e strumenti di modifica; non prosegue automaticamente R4.

## Prima risultante tecnica — Lab 01

Il [prototipo neutro](../../../../examples/collaborative-communication-medium/meta-editor-lab/MetaEditor_Lab01.html) è ora in K-UX-AI con [documentazione della prova](../../../../examples/collaborative-communication-medium/meta-editor-lab/README.md). Node + Chromium tramite set_content hanno verificato `contenteditable` direttamente nella label, Enter, Undo/Redo, trascinamento del nodo con link, card fra sezioni, sezione template non distruttiva, salvataggio/riapertura HTML e viewport 390 px. Sono stati corretti due difetti trovati in corso d'opera: parentesi CSS mancante che alterava la geometria e template che sostituiva indebitamente una sezione. La [GUIDE](GUIDE.md) custodisce il saper fare emergente.

**Limiti:** pagina/proiezione slide sono due viste del documento sintetico `metaeditor.lab.v1`; non integrazione con Studio20 `ccm.document.v1`. Il banco non importa HTML arbitrario né è stato esercitato su Chrome Windows reale; la qualità percepita dal ricevente resta da osservare. Fonte pubblica non equivale a runtime installato in Codex o MAIOS.it.

## Primo banco / stato degli effetti
Il primo esercizio deve testare **doppio clic sulla label di un nodo e digitazione in situ**, una card duplicabile su layout responsive e round-trip del documento con un solo storico. Soluzioni esterne restano candidate, non importate. La copia del sito MAIOS non è il banco neutro. Un documento o un test creato in una conversazione non equivale a un file già residente in K-UX-AI; registrare qui il percorso reale se e quando trasferito.

## Limiti
Competenza scritta ≠ runtime integrato ≠ sito modificato ≠ funzionalità esercitata dall'operatore ≠ assimilazione futura. Esercizi precedenti R3/R4 conservano prove specifiche e difetti, ma non soddisfano la nuova prova. Codex non è automaticamente attivato.
