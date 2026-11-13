# Collaborative Communication Medium — CURRENT

## 13 novembre — Studio 20 pubblico, continuità selettiva e consegna al sito

**Mandato:** rendere scaricabile per tutti l'artefatto finora locale e preparare il successivo ingresso MAIOS.it nella categoria **Risorse → Tool**, mantenendo l'incarnazione coerente con D-ND Design e K-UX-AI. Codex e il sito sono un effetto successivo, non attivati da questa pubblicazione.

**Risultante:** `examples/collaborative-communication-medium/AI_Collaboration_Studio.html` è stato aggiornato a **MetaCanvas Studio 20** sulla `main` pubblica (commit `0be329ae723110c62aa67d89756397683505319b`; 272.490 byte; SHA-256 `c8c1be74c7d9b91d99b0c7888c40cee387579ca26f3079d0fa44ea81f1817a19`). Readback GitHub byte-identico. Quattro scene neutre, HTML offline e MPL-2.0; nessuna pubblicazione MAIOS.it o nuova release npm. Le note precedenti su Studio 15 restano genealogia e non descrivono il runtime corrente.

**Capacità:** layout responsive e strumenti contestuali, esportazione AI con ambito selezionabile e dati privati esclusi per difetto; confronto prima dell'importazione; integrazione selettiva annullabile con preservazione degli appunti privati locali; recupero locale facoltativo, non sincronizzato; miniature con geometria più fedele. La competenza proprietaria mantiene il saper fare in [GUIDE](GUIDE.md#13-novembre-2026--studio-20-complessita-percettiva-minima-e-continuita-delloggetto); il mezzo tecnico e la documentazione in `examples/collaborative-communication-medium`.

**Prova e confini:** Node syntax verificato, esercizi Chromium locali riportati in `SOURCE_AND_SCOPE.md`, readback GitHub, nessuna libreria personale nel JSON iniziale. Da verificare `file://` su Chrome Windows, storage reale, touch, screen reader, comprensione di terzi. È collegato al Design Kernel come caso e metodo, non copiato in due runtime concorrenti. Il brief per Codex è `MAIOS_RESOURCE_TOOL_HANDOFF.md` nella cartella dell'artefatto.


**Data:** 2026-11-11 · Europe/Rome  
**Versione:** 0.1.0-candidate  
**Owner:** K-UX-AI / competences/ux-ai/collaborative-communication-medium  
**Stato iniziale (prima dell'esercizio locale):** SOURCE_COMPETENCE_FORMED / RUNTIME_NOT_YET_BUILT / GENERALIZATION_PENDING

## 13 novembre — Studio 15: operazioni template reversibili e raccolta personale portabile

**Mandato dell'operatore:** i template inseriti devono poter essere annullati, una scheda personalizzata deve diventare template riutilizzabile, e la scelta di posizionamento deve essere esplicita: **Sostituisci, Aggiungi sopra, Aggiungi sotto**.

**Risultante esercitata:** i cinque template incorporati e quelli personali mostrano tre comandi; ogni inserimento, anche quello del percorso completo, forma un solo checkpoint. La sostituzione chiede conferma. La scheda modificata si salva come template personale dentro il documento di lavoro; la raccolta è esportabile/importabile via JSON `metacanvas.templates.v1` in altri file, con controllo di schema/identità/collegamenti. La copia pubblica rimuove il dato `savedTemplates` **e la lista già renderizzata nel DOM**, perché ripulire soltanto lo script JSON avrebbe lasciato testo personale nel sorgente HTML condiviso. Note ed elementi esplicitamente privati sono esclusi anche dalla raccolta esportata. L'editor resta MPL-2.0 nella propria directory.

**Prova:** Node `--check` sugli script; 31 controlli Chromium/Playwright in un editor e in un secondo editor, salvataggio/riapertura, undo/redo e copia pubblica; test ulteriore su note marcate e rifiuto di immagini esterne. Non attestati touch fisico, interoperabilità universale, sicurezza completa. [GUIDE](GUIDE.md#13-novembre-2026--studio-15-il-template-come-modello-personale-e-azione-reversibile) e [formato](../../../../examples/collaborative-communication-medium/TEMPLATE_COLLECTION.md).

## 13 novembre — MetaCanvas Studio 14: correzioni UX richieste, sorgente pubblico e privato

**Mandato:** verificare e correggere quattro differenze in Studio 13: resize Strumenti in finestra mobile, Presenta vuota, area orizzontale non sfruttata, uscita dalla modifica macchinosa. Studio 14 ripristina geometria del canvas in Presenta, bordi di trascinamento mobili e persistenti nelle copie esportate, opzione Flat con lettura a due colonne su desktop e menu OK/Indietro/Avanti in modifica senza checkpoint ridondanti. Il prodotto conserva MPL 2.0 solo nella propria directory e i quattro esempi neutri.

**Prove locali:** Chromium/Playwright su Presenta di 4 scene, 390px mobile, Flat e standard, drag dei pannelli float/right/top/bottom, quick edit + undo/redo, download/riapertura HTML con controlli e stato conservati; export pubblico senza i marker di contenuto privato di prova; Node `--check`. Non sono provati touch fisici o PDF finale. [Guida causale](GUIDE.md#13-novembre-2026--studio-14-presenta-spazio-e-gesto-di-modifica).

**Owner:** K-UX-AI tool e Code Medium Construction / tm7 privata. Codex/TM9 mantiene separatamente pagina MAIOS.it e PR #33, non modificata da questa revisione.

## 13 novembre — MetaCanvas 0.1.1: ritorno di JSON/HTML dell’AI nel documento

**Nuova possibilità esercitata:** oltre a consegnare HTML/JSON a un modello, l'operatore può reimportare il risultato in un editor già aperto. Il tool importa solo il JSON `ccm.document.v1` e non esegue script/CSS di HTML ricevuti; controlla integrità referenziale, chiede conferma, permette Undo e mantiene l'avviso MPL. Non è un merge di versioni né una sincronizzazione in background. È ancora un HTML autonomo.

**Verifiche locali:** JSON→HTML, HTML→modello, annulla/ripristina, file incompatibile, link a referente assente, rifiuto conferma, copia pubblica senza marker di note private/libreria, 390px, zero eccezioni osservate; script validati con `node --check`. Identità di rilascio del tool: preview MetaCanvas 0.1.1, senza nuova release generale K-UX-AI. Prova reale file:// e browser diversi non ancora attestata. [Metodo e causalità](GUIDE.md#13-novembre-2026--metacanvas-dal-passaggio-al-ritorno-strutturato).

## 13 novembre — prima sorgente pubblica dello strumento e licenza MPL-2.0

**Mandato esplicito dell'operatore:** pubblicare l'HTML e la documentazione sul prodotto pubblico K-UX-AI e nella lane privata del produttore, mentre Codex si occupa autonomamente della pagina su MAIOS.it. Licenza selezionata successivamente: tutti possono usare, modificare e commercializzare il tool; il copyright sul codice originale rimane al titolare.

**Risultante di pubblicazione:** `examples/collaborative-communication-medium/AI_Collaboration_Studio.html`, con quattro scene generiche e nessuna dipendenza esterna, accompagnato da README IT/EN, `DOCUMENT_CONTRACT.md`, `SOURCE_AND_SCOPE.md`, `NOTICE.md` e dal testo ufficiale `LICENSE` MPL 2.0. L'HTML include l'avviso SPDX/copyright nell'head e la guida espone il regime d'uso; il normale salvataggio conserva l'avviso. Questa concessione è **circoscritta** ai file della directory, non alle competenze, altri esempi, runtime o loghi. Il copyright sul lavoro originale resta a Graziano Guiducci; gli altri autori non cedono automaticamente i diritti sui propri contributi. MPL significa software open source con copyleft per file, non divieto di rivendita.

**Prove prima della pubblicazione:** controllo sintattico degli script incorporati; Chromium su quattro scene e guida; modifica del titolo, scaricamento e lettura del JSON con avvisi di licenza preservati; viewport 390 px senza overflow orizzontale; zero errori pagina osservati. Non sono stati verificati file:// nel browser dell'operatore, sicurezza completa, tutti i gesture/touch, PDF finale o comprensione di terzi. Nessuna pubblicazione su MAIOS.it né modifica al runtime.

**Separazione owner:** K-UX-AI possiede l'esempio/tool pubblico; la sorgente privata dei processi e degli apprendimenti resta nella lane tm7 e non viene automaticamente esposta; Codex opera sulla PR del sito. Non attribuire al pubblico capacità o disponibilità online non provate.

## 13 novembre — proposta di distribuzione pubblica del medium e perimetro licenza

**Mandato:** rendere il tool comprensibile immediatamente fuori da MAIOS, con esempi generici e una pagina «Strumenti AI» distinta dalle Meta-skill. L'operatore seleziona la direzione di tenere il controllo commerciale dei prodotti UX-AI escludendoli dal modello permissivo MIT, pur consentendo l'uso; il contratto preciso va ancora determinato.

**Prodotto candidato locale (non pubblicato):** editor HTML neutro `AI_Collaboration_Studio_Preview.html` (188.547 byte; SHA-256 `a95652dace40bcb5db6b594e8e23d2984378bed968a9aeae084e7f5ec46301c6`) con quattro casi e un primo ingresso; pagine statiche IT `strumenti/index.html` e EN `tools/index.html` (editor UI ancora IT); README, manifesto file SHA, brief su licenza e checklist. ZIP `AI_Collaboration_Studio_Public_Preview_Package.zip` SHA-256 `0321de2935b60f6dbc92a4381da9d0c6111b51a4cd5e451b6b52cc2e189a78ea`. Artefatti della chat, non sorgente aggiunta alla repository K-UX-AI, non sito live. [Guida](GUIDE.md#13-novembre-2026--ingresso-pubblico-neutro-contenuto-distribuibile-e-prodotto-controllato) conserva metodo, prove e confini.

**Prova locale:** HTML con 4 scene, guida e banner; test Chromium di modifica titolo → download → rientro e viewport 390px; ZIP e manifest byte-verificati, zero JS error nei percorsi osservati. Nessun test `file://` sul browser dell'operatore, né sicurezza completa o PDF finale.

**Condizione materiale non risolta:** l'HTML esportato comprende il codice dell'editor. Qualsiasi concessione commerciale deve proteggere la portabilità del documento dell'utente con un permesso esplicito per la redistribuzione delle proprie presentazioni, pur separando la rivendita/white-label del tool. La licenza attuale del repo pubblico non è esplicitata da un `LICENSE`; nessuna licenza è stata modificata, nessun nuovo termine è entrato in vigore.

**Stato:** PUBLIC_ENTRY_PREVIEW_LOCAL / LICENSE_DIRECTION_IDENTIFIED_NOT_GRANTED / GITHUB_SOURCE_AND_RUNTIME_UNCHANGED / WEBSITE_TOOLS_PAGE_NOT_DEPLOYED / IP_AND_RELEASE_GATE_OPEN.


## 12 novembre — Studio 12, rail delle schede e catalogo responsive

**Mandato:** proseguire il miglioramento UX dopo Studio 11, aggiungendo i comportamenti utili senza appesantire il medium.

**Artefatti autonomi nel ricevente ChatGPT:** `MAIOS_CCM_Studio12_Editor_Guida.html` (185.345 byte, SHA-256 `e0f9ae538cf3808f1d59fae06a49b3a3f917fe06d2cd9bd024d677c2fb0f954d`), `MAIOS_CCM_Studio12_Presentazione_Preconfigurata.html` (199.880 byte, SHA-256 `c7f11faf37ea9827899c76a11c5b7adbc981b5ecbce62d4fe24372a0343e09c2`), ZIP (107.278 byte) con i due HTML. Colonna sinistra elenco/miniature, selezione e riordino ancora attraverso i comandi preesistenti, bordo di resize; pannello strumenti a destra ridimensionabile con sette gruppi richiudibili, ricerca, catalogo in 2/3/4 colonne secondo larghezza, docking esistente. Stato UI incorporato nell'HTML e riutilizzabile.

**Prova:** entrambe le copie in Chromium/Playwright `set_content`, senza errori JS nei percorsi di test: toggle/lista/miniature, allargamento con pulsanti, drag left rail e tool rail, aperture top/bottom/right, ricerca e sezioni, save/reopen con preferenze, modalità Presenta, mobile 390 px senza lettura compressa. In corso d'opera corretto `<details>` che attribuiva modifiche non richieste all'apertura, gesto resize durante transition e adattamento viewport che clobberava width desktop. [GUIDE](GUIDE.md#12-novembre-2026--studio-12--due-superfici-laterali-con-geometria-propria) conserva causalità e metodo.

**Stato:** LOCAL_STUDIO12_CREATED / SIDE_RAIL_AND_TOOL_LAYOUT_TESTED / HTML_ROUNDTRIP_OBSERVED / MOBILE_READABLE_IN_HEADLESS_BROWSER / UX_OPERATOR_REVIEW_OPEN / KUX_PUBLIC_RUNTIME_UNCHANGED / DIRECT_FILE_OPEN_AND_TOUCH_UNVERIFIED.


## 12 novembre — Studio 09, guida e prova di preconfigurazione da fonte reale

**Mandato:** spiegare in una breve guida incorporata che l'HTML è un mezzo di interazione con LLM e con interlocutori umani; provare la capacità della stessa AI di ricevere il file e trasformarlo in una presentazione organizzata secondo le competenze, senza impedire che l'operatore la corregga.

**Esercizio locale:** letti Studio 08 HTML/JSON e fonti owner-native MPK, Meta_Skill e K-UX-AI. Creati (1) editor HTML con `? Guida`, tre passaggi e richiesta copiabile; (2) un nuovo documento HTML di sette schede con note private, fonti `sourceRefs`, nodi/relazioni e catalogo preesistente modificabili; (3) JSON strutturato e ZIP. La guida non pretende un LLM già collegato nel file. La presentazione è una proposta interpretativa, non la prova che le capacità di tutti gli agenti rappresentati siano installate.

**File:** editor `MAIOS_CCM_Studio09_Editor_Guida.html`, 151.399 byte; presentazione `MAIOS_CCM_Studio09_Presentazione_Preconfigurata.html`, 165.934 byte, SHA-256 `61b7a327bf9e220f6556ea345c18a3e757dfb3872628ab4bbf84bd34ca7d5caf`; JSON 28.977 byte; ZIP byte-verificato. File locali della conversazione, non artefatti inclusi nel repository o installati nel runtime.

**Prova:** 8 scenari principali Chromium/Playwright, ciascuno con assert su UI, documento e/o roundtrip, zero JS page errors; sette schede controllate senza troncamenti, note private invisibili in Presenta e assenti dalla copia pubblica, 390px in vista Leggi. [GUIDE](GUIDE.md#12-novembre-2026--studio-09--il-file-modificabile-è-una-fonte-di-lavoro-per-lllm) conserva metodo e differenze.

**Stato:** LOCAL_STUDIO09_GUIDED_EDITOR_AND_CONFIGURED_STORY_BUILT / JSON_READ_TO_HTML_AUTHORING_EXERCISED / HTML_EXPORT_REOPEN_VERIFIED / PROVIDER_CONNECTION_NOT_PRESENT / OPERATOR_USAGE_AND_NEXT_CASE_OPEN / KUX_PUBLIC_RUNTIME_UNCHANGED.


## 12 novembre — Studio 08, libreria di template agentici

**Mandato:** creare template per comunicare possibili organizzazioni della logica di sistemi agentici, a partire dal medium già esercitato. Nessuna architettura universale imposta.

**Artefatti locali verificati:** editor Studio 08 con cinque template non distruttivi (145.276 byte); HTML già composto con cinque schede (153.266 byte); JSON corrispondente (18.802 byte); ZIP completo (90.915 byte). I temi sono: intento/competenza, reciprocità umano–AI, cooperazione fra agenti, proposta/decisione/effetto, continuità dopo evento. Schede con nodi/relazioni modificabili, sorgente `templateSource.kind=illustrative`, nuovi ID quando inserite. [Guida](GUIDE.md#12-novembre-2026--studio-08--template-agentici-come-ipotesi-modificabili) conserva le ragioni e i confini dei modelli.

**Esercizio:** JavaScript valido; inserzione delle cinque schede singole e dell'intero set, salvataggio e riapertura, scena connessa da referenti esistenti, copia pubblica e tema scuro, presentazione, ZIP integro. Le 16 frecce iniziali dei cinque modelli non attraversano l'interno dei riquadri nelle posizioni verificate. La prima verifica visiva ha portato a fissare gli ancoraggi iniziali dei template orizzontali e verticali. Il file HTML locale è un esempio esercitato, non una capability installata nel runtime pubblico.

**Stato:** LOCAL_STUDIO08_TEMPLATE_LIBRARY_BUILT / FIVE_EDITABLE_EXAMPLES_AND_JSON_PRODUCED / SAVE_REOPEN_BROWSER_CHECKED / OPERATOR_FEEDBACK_OPEN / PUBLIC_RUNTIME_UNCHANGED / CROSS_CASE_ASSIMILATION_UNKNOWN.

## 12 novembre — Studio 07, aggiramento e quattro ingressi per lato

**Mandato:** rafforzare l'aggiramento quando i riquadri si toccano o si sovrappongono; punte di freccia solo inizio, solo fine, entrambe o nessuna; ganci/punte visibili davanti alle schede; quattro ingressi standard per lato e distribuzione quando più frecce convergono.

**Artefatto locale prodotto:** `MAIOS_Comunicazione_Collaborativa_Studio07.html`, 135.511 byte, SHA-256 `d56564923d767f09119e75984ec54a885a64f5ad2aaac6eeae2da8a7b591a7c8`, ZIP di 39.948 byte con HTML identico. Unico file offline con schema `ccm.document.v1`. [Guida](GUIDE.md#12-novembre-2026--studio-07-il-gancio-è-un-oggetto-percettivo-non-un-nuovo-referente) esplicita meccanismi e limiti.

**Esercizio:** sette situazioni geometriche × due relazioni, senza attraversamento degli interni o collisione con riquadri dei badge nei casi campionati; quattro ingressi distinti sullo stesso lato (20/40/60/80%); quattro modalità di punta SVG; click sul gancio, scelta della porta, export/reopen e punte bidirezionali attraverso mini editor; copia pubblica priva del testo di appunto privato; ZIP verificato; prova iniziale con 24 collegamenti/12 nodi senza JS error. Test Chromium Playwright su HTML caricato nel harness, non uso umano di `file://`.

**Stato:** STUDIO07_HTML_LOCAL_BUILT / CONTACT_BYPASS_AND_PORTS_CHECKED / BIDIRECTIONAL_HEADS_AND_REOPEN_CHECKED / PUBLIC_COPY_PRIVACY_CHECKED / USER_REVIEW_PENDING / KUX_PUBLIC_RUNTIME_UNCHANGED / CROSS_CASE_ASSIMILATION_UNKNOWN.

## 12 novembre — Studio 06, frecce semantiche e percorso adattivo

**Fonte:** screenshot reale dell'operatore su Studio 05 in Chrome locale e correzione «La logica delle frecce va rafforzata». Il problema riscontrato riguarda riquadri sfalsati, curvatura, ancore ed etichette non sempre leggibili.

**Risultante locale:** `MAIOS_Comunicazione_Collaborativa_Studio06.html`, 126.062 byte, SHA-256 `602d1358382f93faf89a95c2747dbb71e8b0fe817c0d582eab582ae306bb5567`, più ZIP alternativo byte-identico e screenshot di verifica. Partendo da Studio 05, conserva `ccm.document.v1` e le funzioni di lavoro ed esportazione. Auto-routing confronta lati, ostacoli, percorso, etichette e spazio; badge etichette indipendenti, trascinabili e a capo; centro freccia per modificare curva mantenendo i nodi collegati; modalità auto/dritto/angoli/curva e ripristino automatico. Screenshot di partenza resta prova dell'uso dell'operatore della versione precedente, non prova del nuovo risultato.

**Prova:** JavaScript sintatticamente valido, sei configurazioni geometriche su dodici frecce senza attraversamento delle forme e senza badge sopra le forme nei casi esercitati, drag/reopen di percorso e label, selettore/ripristino, Grafite e privacy export, scena sintetica 40 relazioni renderizzata senza errore. [Guida](GUIDE.md#12-novembre-2026--studio-06-relazione-percorso-ed-etichetta-non-coincidono) aggiornata con meccanismo e limiti.

**Stato:** LOCAL_STUDIO06_BUILT / AUTO_ROUTING_AND_LABEL_UX_BROWSER_CHECKED / SAVE_REOPEN_CONFIRMED_IN_HARNESS / PUBLIC_RUNTIME_UNCHANGED / OPERATOR_REVIEW_PENDING / FILE_URL_AND_TOUCH_NOT_VERIFIED / CROSS_CASE_ASSIMILATION_UNKNOWN.


## 12 novembre — Studio 05: intervento UX sull'HTML locale

**File consegnabile:** `MAIOS_Comunicazione_Collaborativa_Studio05.html`, 114.556 byte, SHA-256 `5e496e0031de67670fdedc308781847c3a8503b90890b369f805be405e4082c4`; ZIP di ripiego locale con HTML identico. Il download nell'interfaccia dell'operatore non è verificato. Non installato in runtime K-UX-AI.

**Differenze implementate:** pannelli che non occludono il canvas sul desktop; vista di lettura lineare e modificabile su mobile senza duplicare il modello; canvas con zoom/scroll disponibile; mini editor ridotti grazie a proprietà secondarie collassabili; segnalazione dell'overflow di testo e nota iniziale più leggibile; stato «download richiesto» anziché falsa conferma; copia pubblica di sola lettura senza note in JSON **né** nella proiezione DOM; pannello mobile esplicito; rispetto del focus/inert quando chiuso.

**Prova:** 35/35 test principali + 10/10 regressioni mirate Playwright/Chromium `set_content`, incluse frecce, quattro temi, stampa preparata, HTML scaricato e ricaricato, privacy pubblica e mobile. Errori iniziali corretti e riesercitati. Source HTML autonomo e ZIP creati nel container; nessun deploy, release, merge, test file://, dispositivo fisico o PDF effettivo. [Guida](GUIDE.md#12-novembre-2026--studio-05-lo-spazio-di-lavoro-non-è-lo-schermo-del-pannello) custodisce il metodo e la distinzione sulle proiezioni private.

**Stato:** LOCAL_STUDIO05_BUILT / 45_OF_45_BROWSER_CHECKS_PASS / PUBLIC_DOM_PRIVACY_REGRESSION_FIXED / USER_DOWNLOAD_AND_UX_TRIAL_PENDING / KUX_PUBLIC_RUNTIME_UNCHANGED / CROSS_CASE_ASSIMILATION_UNKNOWN.

## 11 novembre — Studio 04: UI coerente e mini editor riposizionabili

**Artefatto locale:** `MAIOS_Comunicazione_Collaborativa_Studio04.html`, 101.419 byte, SHA-256 `579c7f2ee7891b34eb60b7ef3e749ebe8cd373a71d3b76acbda70014f3c25a32`. Tema diffuso nell'area esterna, toolbar, controlli, pannelli, dialoghi e mini editor per tutti e quattro i preset. Mini editor spostabile dalla testata, ridimensionabile dall'angolo, con geometria salvata nel file, riuso e comando «↩ Vicino». Il pulsante Copia pubblica continua a eliminare note e libreria; ciò non cifra il file né verifica i contenuti condivisi.

**Esercizio:** nuova suite browser Chromium `set_content` su palette, spostamento, resize, riuso, reset, save/reopen e privato/pubblico; 16/16 test di regressione Studio 03 verdi; zero errori JS osservati. Apertura diretta `file://` bloccata dal runner, controllo sul desktop/touch dell'operatore non eseguito. [Guida](GUIDE.md#11-novembre-2026--studio-04-mini-editor-mobili-e-tema-sullintero-ambiente) aggiornata con metodo e confini della prova.

**Stato:** LOCAL_STUDIO04_BUILT / CROSS_THEME_UI_VERIFIED / MINI_EDITOR_DRAG_RESIZE_VERIFIED / HTML_ROUNDTRIP_VERIFIED / REGRESSION_16_OF_16 / PUBLIC_RUNTIME_UNCHANGED / USER_BROWSER_EXERCISE_OPEN.

## 11 novembre — Studio 03, HTML avanzato locale e apprendimento

**Risultante:** `MAIOS_Comunicazione_Collaborativa_Studio03.html` costruito come file autonomo di 92.537 byte (SHA-256 `f00442c79ada3433a05f417c046af5d0f4fbfbdc81bed15298037416f869ebd6`). Estende Studio 02 con snap magnetico e guide, frecce su punti medi dei lati e maniglia centrale, mini editor vicino a riquadro/freccia/scheda, strumenti solo su comando (dock destra, sinistra, sopra, sotto, flottante), note mobili private, forme circle/oval/pill, collasso con segnaposto numerato, approfondimento live e pagina separata nel PDF, layout nelle sezioni, esportazione di una copia pubblica che pulisce **sia il JSON sia il DOM proiettato**.

**Esercizio locale:** 16/16 controlli funzionali + 6/6 approfondimenti Playwright/Chromium via `set_content`. Risultati verificati: selezione non apre automaticamente inspector; doppio clic apre mini editor; triplo clic attraversa i livelli; magnetismo osservato; freccia agganciata a metà lato e spostabile dal centro; note escluse in Presenta e nell'HTML pubblico; approfondimento produce foglio aggiuntivo nella preparazione della stampa; export HTML e riapertura preservano forma, testo e note; interfaccia e mini editor raggiungibili a 390 px. Zero errori JavaScript pagina osservati nel test principale. **Non verificati** apertura diretta `file://`, touch su dispositivi fisici, PDF finale e comprensione reale dell'interlocutore.

La [guida](GUIDE.md#11-novembre-2026--studio-03-mini-editor-magnetismo-e-continuità-tra-dom-e-documento) conserva i meccanismi. Il sorgente del prototipo è un artefatto della chat, non un file del repository pubblico. Nessun aggiornamento di `src/`, demo, release o sito derivato da questo commit.

**Stato:** STUDIO03_LOCAL_HTML_BUILT / CHROMIUM_TESTS_22_OF_22 / PRIVATE_PUBLIC_EXPORT_SEPARATED / COMPETENCE_SOURCE_LEARNING_RETURNED / RUNTIME_NOT_INTEGRATED / USER_BROWSER_TRIAL_PENDING / CROSS_CASE_ASSIMILATION_UNKNOWN.

## 11 novembre — Studio 02, secondo esercizio locale

L'operatore ha scelto come risultante una pagina che rimanga visivamente il lavoro stesso, con editor contestuali richiamati su clic e strumenti dalla rotellina a destra; triplo clic per il livello sottostante quando vi è sovrapposizione, oppure per le proprietà visive, più alternativa esplicita dall'elenco Livelli. Ha chiesto frecce con estremi trascinabili, proprietà specifiche, quattro temi, preset e layout/sezioni drag-and-drop, mantenendo l'HTML entro circa 2 MB.

**Artefatto locale esercitato:** `MAIOS_Comunicazione_Collaborativa_Studio02.html`, SHA-256 `1023ca424ead3b10d49541d895ee2ba6af006e32ba27aa8781cf914970fa085c`, 66.438 byte. Modello `ccm.document.v1` compatibile con il precedente; nuova superficie HTML/CSS/JS autonoma. 11/11 scenari Playwright + prove specifiche su trascinamento di sezione con contenuto, immagine importata/compressa e riaperta, fogli di stampa preparati. La [guida](GUIDE.md#11-novembre-2026--studio-02-superficie-libera-strumenti-situati-e-diagrammi-manipolabili) conserva differenze e meccanismi.

**Correzioni riusabili nello stesso movimento:** mantenere il DOM del referente attraverso il triplo clic; evitare duplicazione degli handler su canvas persistente; renderizzare sopra ai nodi gli handle della freccia solo quando selezionata; verificare gli stili SVG computed e non solo i loro attributi. Le sezioni trasportano i membri tramite `containerId`; le estremità non collegate della freccia restano punti liberi reali. Il sapere di progetto rimane in questa competenza; i metodi generali di Interaction Quality e Code Medium Construction restano owner complementari senza copia obbligatoria.

**Stato:** LOCAL_STUDIO02_BUILT / BROWSER_EXERCISE_11_OF_11 / HTML_EXPORT_REOPEN_OBSERVED / PUBLIC_KERNEL_RUNTIME_UNCHANGED / OPERATOR_TRIAL_AWAITED / DIRECT_FILE_URL_AND_TOUCH_NOT_VERIFIED / CROSS_CONTEXT_ASSIMILATION_UNKNOWN.


## 11 novembre — esercizio locale del medium neutro

È stato costruito e verificato nel ricevente ChatGPT un HTML autonomo, con modello dati incorporato, tre schede iniziali, editing strutturale/testuale, collegamenti etichettati, drag/resize, libreria, immagini, note, presentazione, export HTML/JSON, copia pubblica e preparazione dei fogli per la stampa. La prova Playwright ha coperto andata/ritorno dell'HTML e alcuni gesti reali sul DOM. File locale: `MAIOS_Comunicazione_Collaborativa_Prototipo.html`; SHA-256 `f7d7761ef5876c85a47309b882b593c1a91c7cc4c37c1893d20e8c4df49b59c7`, 42.639 byte. **Non è un file pubblicato o installato in questo repository.**

Correzione riusabile: il rerender su un `pointerup` privo di movimento sopprimeva il successivo doppio clic sul medesimo elemento; ora il nodo rimane e la maniglia viene aggiunta senza ricrearlo, mentre le trasformazioni effettive vengono salvate e renderizzate. [La guida](GUIDE.md#11-novembre-2026--primo-esercizio-del-medium-html-neutro) conserva ragione e metodo.

**Stato:** SOURCE_COMPETENCE_FORMED / LOCAL_BROWSER_EXERCISE_OBSERVED / EXPORTED_HTML_REHYDRATION_TESTED / PUBLIC_RUNTIME_NOT_CHANGED / CROSS_DEVICE_AND_FILE_OPEN_NOT_VERIFIED / LATER_ASSIMILATION_UNKNOWN.

## Determinazione dell'operatore

L'esperienza con un HTML modificabile usato per la presentazione MAIOS × Schnell apre uno strumento per builder AI, aziende e operatori che devono comunicare oggetti di lavoro e prodotti fra persone e AI. La persona modifica il documento, lo salva, lo presenta o lo trasferisce; l'AI può comprenderne la struttura e contribuire alla formazione dei contenuti. Il nucleo deve generalizzarsi oltre le presentazioni: content web, progettazione, gestione di sistemi complessi e altri casi che emergano.

**Prima origine tecnica:** file allegato alla conversazione del 2026-11-11 `MAIOS_Schnell_Presentazione_modificata(1).html`, contenente un HTML completo con introduzione e cinque schede, campi `contenteditable`, appunti, vista Presenta, stampa e download HTML. Resta un artefatto privato dell'operatore; qui sono conservati metodo e osservazioni, non testo e note aziendali.

## Formazione eseguita nella sorgente

- [SKILL](SKILL.md): competenza specializzata, proprietaria del metodo degli artefatti comunicativi condivisi.
- [GUIDE](GUIDE.md): meccanismi del primo caso, distinzione fra fonte/forma/relazioni, architettura candidata, condizioni per esercitare.
- Raccordi d'ingresso con K-UX-AI e adapter LLM.

Il caso indica un uso pratico riferito dall'operatore, non l'esistenza di un editor universale integrato in K-UX-AI. Le capacità future non si considerano esercitate per il solo fatto che la competenza le descrive.

## Primo seguito materiale

Costruire e testare un HTML neutro autosufficiente a partire dal meccanismo esistente, preservando semplicità, modifica, salvataggio, riapertura e presentazione; introdurre editing di struttura e relazione in modo incrementale. Usare il medesimo artefatto per passaggi AI/umano con identità della revisione, prima di scegliere connettori o hosting.

**Confini:** nessuna modifica al file Schnell, al prodotto JS, al sito, alla release, a credenziali, controller, mailbox o automazioni. Repository source ≠ editor installato ≠ esercizio sul nuovo prototipo ≠ assimilazione in altri host.
