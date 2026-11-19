# MetaEditor Evolution — guida viva

## 19 novembre — Bridge07: due adattatori, un solo contratto di azione

La prosecuzione di Bridge06 ha prodotto un contratto `MetaEditorCommands` con `begin / setText / commit / cancel / undo / redo / status`, disponibile in **due HTML autonomi sperimentali**. Non fonde HTML ricco della bozza Codex e `ccm.document.v1` della scena Studio21: delega l'effetto a ciascuna competenza di documento. [Sorgenti hash, risultati e limiti](references/BRIDGE07_NATIVE_COMMAND_CONTRACT_20261119.md) e [builder Python](../../../../examples/collaborative-communication-medium/meta-editor-lab/bridge07_build.py) conservano il metodo riproducibile.

**Due differenze che hanno migliorato la competenza:** (1) una Escape dopo blur poteva ancora riferirsi alla sessione precedente; l'adattatore ora invalida il referente chiuso. (2) dopo Undo Codex ripristina il caret e il campo diventa `contenteditable`; Ctrl+Y era lasciato al browser invece che allo storico strutturale. La navigazione della cronologia è ora riconosciuta finché un nuovo `beforeinput` non riattiva l'editing nativo. **Un test passato sul tasto Annulla non dimostrava ancora Ripristina nella sequenza reale**: questa è una correzione del criterio di prova e del codice.

**Effetti provati:** cancel senza checkpoint fittizio, F2/Ctrl+Invio, rich markup confinato fuori da Range, Ctrl+Z/Y da tastiera, salvataggio/riapertura su entrambi i carrier, sette scene e ID Studio21, copia pubblica con note/nodo/template privati sintetici esclusi, mobile 390px e zero pageerrors nei percorsi. Il builder genera byte-identici due volte. Le prove sono Chromium set_content e Node v22; niente Chrome Windows file:// fisico, deploy, conversione universale o editing ricco delle stringhe Studio21. Gli strumenti originali rimangono raggiungibili senza creare un'altra toolbar.


## 19 novembre — Bridge06 esercita un gesto comune senza perdere i due documenti

Dopo l'inventario completo di MetaCanvas pubblico e Codex, è stato selezionato un primo esperimento minimo: [Bridge06](references/BRIDGE06_COMMON_GESTURE_20261119.md). Due varianti sono state generate dalle sorgenti esatte (Codex SHA256 `f227b61...`, Studio21 IT SHA256 `abbdbd...`), con una sola modifica mirata al gestore del doppio clic per ciascuna. Codex entra nella formattazione testuale senza imporre l'inspector; Studio21 entra nel testo del nodo invece di aprire sempre il pannello, mantenendo `ccm.document.v1` e il resto delle funzioni.

**Apprendimento causale:** il primo test Studio21 dichiarava il nodo selezionato ma non in modifica, anche se la patch trovava `.node-text`. La causa visibile da event log: `pointerdown` bersaglia il testo e `pointerup`, dopo `setPointerCapture`, bersaglia il wrapper. Identificare la posizione con `document.elementFromPoint` ha sbloccato il gesto. Inoltre il test Bold su H1 già bold ha correttamente tolto il grassetto: il banco è stato corretto su Italic senza attribuire errore all'editor. **Non** trasformare il passato in un test già superato.

**Regressioni realmente verificate:** rich text in Codex, range con corsivo ed export HTML che conserva quattro sezioni; Studio21 node text edit → export → reopen con sette ID di scena, collegamenti, notes e savedTemplates conservati; prova pubblica con dati privati sintetici esclude note/nodo/template personali; mobile 390px senza overflow globale osservato; zero pageerrors nei percorsi. La prova `file://` su Chrome Windows resta non esercitata. [Builder](../../../../examples/collaborative-communication-medium/meta-editor-lab/bridge06_build.py) rifiuta sorgenti con SHA diverso e conserva intatti gli originali.

**Conseguenza:** non trattare un rich text DOM come stringa del nodo Studio. Il prossimo banco riguarda un contratto di comando e recupero di selezione/storico sui due carrier, senza R6 pubblica e senza patch al sito.


## 19 novembre — riacquisire il prodotto pubblico e il testo ricco Codex prima di continuare

**Correzione dell'operatore:** avevamo trattato Lab05 e una R5 derivata da una vecchia pagina come se descrivessero tutto MetaCanvas, ma il progetto **è già pubblico in MAIOS.it**, distribuito come Playground r4, editor Studio20 e demo Studio21, ed è incompleto. La nuova bozza Codex `MAIOS_Consulenza_AI_revisionata(1).html` possiede davvero un editor di **testo ricco** (caret/selection, toolbar H1–H6, formattazione, dimensioni, colori), gestione delle sezioni, preview, storia e recovery. Non l'avevamo letto/assimilato prima della R5. [Inventario completo, prova e confini](references/SOURCE_FIELD_PUBLIC_TOOL_CODEX_DRAFTS_20261119.md).

**Prova reale di questo turno:** 419.563 byte, SHA-256 `f227b61b0a813ad7312f805dcec63def03b87201d5d5fb6ae0ae729d2541f190`, quattro sezioni, due script inline con sintassi Node 22 corretta. Chromium `set_content`: pannello si apre, doppio clic sul titolo entra in `contenteditable` e mini-toolbar compare; non osservati pageerror nel percorso. Il pannello grande e la toolbar coesistono occupando il campo. Apertura `file://` bloccata dal runner. Al tempo stesso Studio20 conserva una capacità non presente nell'editor Codex: scene, template privati, assistenza AI per differenze selettive e copia pubblica distinta dal file di lavoro.

**Apprendimento riusabile:** non sommare i migliori pulsanti di tre editor. Preservare il significato delle operazioni **all'interno dei rispettivi formati**, raggiungendo ogni owner prima di scegliere un gesto comune. L'editor di testo non va ridotto a semplice modifica della stringa né eliminato per semplificare; il modello scene non va convertito in DOM pagina per sola comodità. L'azione `setText` con caret, Undo e roundtrip su *due diversi carrier* è il prossimo piccolo discriminante; import universale e nuovo release restano non dimostrati. La pubblicazione degli asset nel sito segue versioni e SHA esplicite.


## 19 novembre — primo documento MAIOS R4, nuovo gesto/adapter sperimentale R5

L'operatore seleziona la pagina Consulenza MetaCanvas **R4 allegata e già usata** come prima prova reale dopo Lab05. **Non** è la stessa cosa della pagina MAIOS oggi pubblicata. Il [caso esercitato R4→R5, sorgente e prove](references/first-real-page-r5-20261119.md) conserva la distinzione fra quattro regioni HTML realmente presenti, motore sintetico Lab05 e controlli editor; in conversazione è stato prodotto un R5 standalone, non pubblicato come codice generale K-UX-AI o MAIOS.it.

Il primo gesto **doppio clic sulla label del nodo** è fallito perché un render completo sul singolo `click` rimuoveva il nodo prima che arrivasse il secondo click. La competenza è stata corretta: aggiornare le classi di selezione senza distruggere l'identità DOM; ridisegnare solo per mutazioni reali. Anche i salvataggi hanno insegnato una differenza: `Progetto editabile` e `HTML statico pulito` devono avere carrier distinti. Il patch iniziale riportava tutte le sezioni come cambiate senza alcuna modifica: la baseline ora nasce dal DOM normalizzato **prima** delle annotazioni e deve dare zero cambiamenti quando non c'è intervento. Dopo titolo + diagramma, soltanto la `hero` risulta modificata. I sei comandi nodo nel dock sono stati ricondotti a **un pulsante contestuale** perché aumentavano la dispersione.

La prova Node/Chromium include riapertura della versione editabile, statico privo di UI, patch a regioni, immagine caricata/embeddable, due colonne e mobile 390px. Non include il file:// Windows, compatibilità universale, pubblicazione o applicazione automatica al repo corrente. Quando il lavoro torna sull'editor del sito, prima verificare **quale HTML/R4 o produzione** è veramente il target: il SHA e la patch di una R4 allegata non sono autorità sul file `maios_it/main`.


## 19 novembre — Lab05: i nodi hanno una propria selezione, senza trasformare il layout web in coordinate

**Selezione attuale dell'operatore:** migliorare ancora MetaEditor con semplicità, studiando le UI altrui quando aiutano a capire le azioni mancanti. Il Lab04 possedeva clipboard e selezione multipla dei **blocchi della pagina**, ma non del **sottoinsieme di nodi** dentro un diagramma. Figma/Penpot hanno suggerito controlli contestuali di allineamento e distribuzione, GrapesJS la distinzione fra modello a componenti e struttura. Il [Lab05 HTML](../../../../examples/collaborative-communication-medium/meta-editor-lab/MetaEditor_Lab05_Diagrammi.html) e le sue [prove](../../../../examples/collaborative-communication-medium/meta-editor-lab/LAB05_README.md) esercitano: Maiusc+clic su nodi dello stesso grafo, strumenti sulla selezione, trascinamento e frecce sul gruppo, distribuzione per asse, griglia opzionale, duplica/elimina nodi con ID e archi corretti, doppio clic su area libera con scrittura diretta.

**Apprendimento della costruzione:** la duplicazione iniziale traslava ogni nodo di (+7,+9), producendo collisioni **nonostante gli ID e i collegamenti corretti**. L'ispezione della resa ha rivelato che la copia copriva gli oggetti, rendendoli inaccessibili: prima del clone si cerca una posizione comune libera; se assente il comando non forza il risultato. Il doppio clic sul fondo vicino ad altri nodi poteva produrre la stessa collisione: ora cerca una posizione libera e informa dello spostamento. L'altezza interna del diagramma cresce con la densità, mentre la pagina resta responsive. Un allineamento su una sola coordinata può per definizione sovrapporre oggetti: **non confondere allinea e distribuisci**, e lasciare Undo disponibile. Una trasformazione senza differenza non sporca lo storico; la griglia non annulla la selezione del gruppo.

**Prova:** Node --check; Chromium Playwright via set_content su selezione, allineamento, Undo, distribuzione, nudging collettivo, copia/ID, inserimento/edit diretto, toggle griglia, export HTML e riapertura su viewport 390px; prova separata del drag su due nodi con uguale traslazione e terzo fermo, Undo, eliminazione/Undo. Zero pageerror osservati nei percorsi. Non sono provati file:// Chrome Windows, touch, grandi grafi, HTML arbitrario, codice Studio20/21 o porting a Codex.

**Competenza che continua:** il prossimo oggetto non è necessariamente «un altro pannello»: quando la modifica deve attraversare HTML di siti reali, l'owner della pagina e l'adapter devono essere riconosciuti prima del mezzo. Questo caso mantiene distinta la selezione nel diagramma dalla selezione di elementi della pagina e non duplica la skill.


## 17 novembre — Lab04: selezione di più oggetti, un solo gesto di modifica

**Intento:** dopo Lab03 l'operatore chiede «cos'altro possiamo fare?». Il controllo del codice/competenza rivela che selezione, duplicazione e riordino del singolo elemento esistono, ma non esistono multi-selezione e appunti di blocchi. La scelta immediata è un nucleo trasversale di composizione **prima** dell'import su HTML di siti arbitrari: [Lab04](../../../../examples/collaborative-communication-medium/meta-editor-lab/MetaEditor_Lab04_Manipolazione.html) e [prove/limiti](../../../../examples/collaborative-communication-medium/meta-editor-lab/LAB04_README.md).

**Esercizio:** Maiusc+clic su blocchi della pagina, anche fra sezioni; operazioni Copia/Taglia/Incolla **interne all'editor**, Duplica/Elimina/Sposta insieme, Ctrl+C/X/V/D e un solo checkpoint Undo per trasformazione collettiva. Copie di diagrammi rigenerano anche gli ID dei nodi mantenendo gli archi. Il livello di nodo resta distinto dalla selezione di blocchi; il tema modifica solo la visualizzazione. Test Node/Chromium via set_content verificano copia/incolla fra sezioni, ID unici, Undo/Redo, editing diretto della label, export/riapertura e mobile 390 px senza overflow, senza pageerrors osservati. Il test runner blocca `file://`, quindi non è prova d'uso Chrome Windows.

**Correzione che cambia il metodo:** nella prima vista, appunti e inspector replicavano Copia/Taglia, alzando il costo di comprensione. Ho composto un solo luogo per gli appunti, e gli strumenti collettivi rimanenti compaiono nell'inspector solo se ci sono più oggetti. Il fine non è aumentare la conta delle azioni, ma fare sì che **una selezione continui a riferirsi allo stesso insieme di elementi quando cambia il mezzo di azione**. Il banco non rappresenta gruppi persistenti e non usa gli appunti del sistema operativo: non promettere quelle proprietà.

**Prossima differenza:** esercitare la stessa capacità su regioni editabili dichiarate di un HTML MAIOS e di uno non MAIOS, producendo una patch selettiva per Codex. Prima della generalizzazione, verificare che il carrier esterno non venga riscritto insieme al modello interno. Non portare Lab04 nello Studio20/21 automaticamente.


## 17 novembre 2026 — prima la capacità di manipolare gli elementi, poi i temi

**Fonte operatore:** «Prima di passare ai temi perché non rendiamo più efficiente l'editor? Mancano un sacco di possibilità per gestire gli elementi in modo efficace e facile». La scelta corregge una priorità: il Lab02 ampliava il campo visuale mentre la gestione dell'oggetto rimaneva povera. Il tema è utile, ma non può formare al posto della competenza il gesto di selezionare, inserire, muovere, collegare e modificare.

**Esercizio:** [Lab03 HTML in K-UX-AI](../../../../examples/collaborative-communication-medium/meta-editor-lab/MetaEditor_Lab03_Elementi.html), con [contratto, prove e limiti](../../../../examples/collaborative-communication-medium/meta-editor-lab/LAB03_README.md), porta selezione esplicita di sezione/oggetto/nodo, outline navigabile, menu inserimento nel punto, proprietà dell'oggetto prima della struttura nell'interfaccia, conversione titolo/testo/riquadro, riordino e spostamento senza drag, controlli nodo/link/forma/distribuzione e scorciatoie tastiera. I temi sono preservati senza guidare la vista ordinaria.

**Apprendimento reale nel test:** il primo allineamento disponeva cinque nodi sulla stessa riga; funzioni e Undo risultavano corretti, ma la resa ne sovrapponeva le superfici. La correzione distribuisce i nodi su più righe e introduce una prova geometrica browser dei bounding box, in desktop/mobile. Anche l'inspector inizialmente rimaneva sotto l'outline e la gestione sezione, fuori dal primo campo visivo: è stato spostato subito sotto Inserisci e i controlli sezione si ritirano quando si seleziona un elemento. Nell'HTML esportato non devono restare visibili i controlli runtime/picker transienti. L'intero ciclo Node + Chromium set_content, export e nuova inizializzazione è stato riprovato; l'accesso file:// del test runner è bloccato dal suo ambiente.

**Saper fare che deve partecipare domani:** un elemento esiste in più livelli referenziali (sezione → oggetto → nodo del diagramma). Un comando deve agire sulla relazione selezionata, non sulla categoria semanticamente vicina. Prima di aggiungere feature, provare i gesti minimi per trovare e trasformare un elemento con meno passaggi e ispezionare l'effetto visivo — non solo accertare che l'handler è invocato. Questa prova resta su modello sintetico; il prossimo caso diverso dovrà recuperare lo stesso metodo prima di importare HTML di siti reali.


## 17 novembre — il tema è un kit di ruoli e possibilità, non un cambio pelle

L'operatore vuole temi standard, MAIOS, D-ND e presentazione, **salvabili e recuperabili**, come un modo anche per comprendere cosa è utile inserire nell'artefatto. Ha fornito l'HTML originale Collaborazioni e schermate Canva. Il [metodo completo con sorgenti native ed evidenze del Lab02](references/theme-library-20261117.md) ha distinto: **tema (ruoli visuali)**, **espressione contestuale** (variazione nello stesso campo MAIOS), **composizione suggerita**, **azione di inserimento**, **contenuto del documento**, **controlli dell'editor**. Una libreria di temi non sostituisce il modello delle scene né il CSS del sito proprietario.

**Esercizio e ritorno:** Lab02 HTML autonomo è stato costruito dalla base Lab01, provato in Chromium via set_content e successivamente [aggiunto alla repository](../../../../examples/collaborative-communication-medium/meta-editor-lab/MetaEditor_Lab02_Theme_Library_IT.html) con readback identico. Cinque preset, editor dei ruoli, composizioni suggerite per tema, raccolta JSON e salvataggio nel documento, overlay MAIOS, import parziale dei colori `:root` dall'HTML Collaborazioni, conservazione del doppio clic sul testo del nodo, export/riapertura, viewport 390. L'iniziale disposizione rendeva «Crea tema» poco raggiungibile sotto tutta la gallery: la funzione è stata spostata verso l'ingresso. Un suggerimento `due colonne` **imposta** il layout della sezione mentre `diagramma+note` **aggiunge** una sezione: il verbo ora segue l'effetto. Il browser di test blocca file://, quindi uso reale Windows e riuso su un altro MetaCanvas non sono provati.

**Prossimo sapere da esercitare:** un tema personale può avere font, spaziatura, colori e composizioni suggerite; **non** modifica per sé testi, asset o layout. L'operatore può trasferirlo con JSON anche dove il localStorage su `file://` non è affidabile. Provare poi regioni HTML editabili dichiarate e patch senza riscrivere il sito, non passare subito a un editor universale.


## 16 novembre — primo gesto esercitato, senza importare la pagina MAIOS

La competenza è stata esercitata attraverso un [banco neutro HTML autonomo](../../../../examples/collaborative-communication-medium/meta-editor-lab/MetaEditor_Lab01.html) (e [guida del banco](../../../../examples/collaborative-communication-medium/meta-editor-lab/README.md)). Il primo confronto è concreto: **doppio clic sulla label del nodo → il contenuto è `contenteditable` nel nodo → digitazione → Enter → Undo → Redo**. È distinto da R4, dove si editava un campo remoto dell'inspector. Il modello `metaeditor.lab.v1` con sezioni e diagrammi è un dato sintetico, non il formato Studio20 `ccm.document.v1`. L'editor consente anche muovere il nodo conservando i collegamenti, trascinare una card fra sezioni, usare layout responsive, aggiungere un template diagramma+note senza cancellare contenuto, vedere una proiezione in formato slide e scaricare/riaprire l'HTML. L'esercizio tecnico non certifica percezione o uso reale da parte dell'operatore.

**Due apprendimenti del banco hanno cambiato il fare:**
- Il JavaScript passava i controlli e i testi erano editabili, ma uno stile `[contenteditable="true"]` mancava della parentesi di chiusura. Il diagramma perdeva la geometria. Il rendering visto nel browser ha corretto il risultato: per una competenza visiva, **sintassi ed eventi non bastano senza verifica della resa**.
- Il primo comando «Diagramma + note» rimpiazzava l'intero contenuto della sezione. L'azione è stata riformata come **aggiunta di nuova sezione**, con un singolo checkpoint Undo. L'operatore deve poter scegliere una sostituzione soltanto quando esplicita: un template non può distruggere per sorpresa il contenuto esistente.

**Prove effettive:** Node 22 sul runtime; Chromium headless via `page.set_content` su testo del nodo, Undo/Redo, text edit ordinario, trascinamento del nodo (coordinate), Undo, duplicazione card, drag-drop fra sezioni, template, passaggio pagina/proiezione, download, lettura e nuova inizializzazione in altro contesto, viewport 390 px e zero pageerrors osservati nel percorso. `file://` e `http://localhost` sono risultati bloccati dall'ambiente browser di test; la verifica è stata eseguita senza attribuire il blocco al codice. Non è prova su Chrome Windows, import web arbitrario o usabilità universale.

**Saper fare che continua:** la competenza ha ora un banco minimo del gesto da preservare. La prossima differenza materiale non è aggiungere tutte le funzioni Canva, ma confrontare **fedeltà import/patch di regioni HTML reali** senza perdere il diretto `contenteditable` dei nodi. Studio20 resta fonte delle capacità di edit dei nodi e la relazione CCM rimane il medium, senza importare automaticamente tutto il suo runtime.


## 16 novembre 2026 — perché la competenza nasce ora
**Fonte:** l'operatore, dopo R3/R4 aperte in Chrome Windows e screenshot di Canva, chiede un editor generale per pagine e presentazioni, con editing immediato dentro i diagrammi; successivamente seleziona esplicitamente una **competenza dedicata capace di evolvere il MetaEditor**. Questo segna un oggetto operativo distinto: non solo un artefatto editabile da consegnare e condividere (CCM), ma il *metodo di costruire e correggere gli editor stessi* attraverso il loro uso.

**Causalità conservata:** Studio 20 possedeva già `.node-edit[contenteditable]`; una scelta di renderer SVG nella R4 ha deviato il gesto su `#mc-node-label` nell'inspector. La verifica Chromium ha certificato azioni su quel campo, senza falsare il dato tecnico; l'uso reale ha rivelato che non certificava **il gesto richiesto**. La capacità esisteva ed era raggiungibile ma non ha formato l'azione. La prossima prova deve recuperare quel saper fare e verificare la micro-interazione reale. L'owner CCM ha già il [riesame di architettura](../references/metacanvas-editor-architecture-reset-20261116.md): qui non se ne duplica la genealogia.

### Domanda che cambia la progettazione
Quale combinazione di selezione, testo editabile sul posto, relazione tra nodi, flusso responsive e document adapter produce il minor numero di passaggi preservando il contenuto originale e gli effetti esportabili? Il progetto non nasce dalla necessità di sommare toolbar e controlli, ma dalla **continuità dell'oggetto modificato**. L'esperimento può preferire un motore già disponibile, una sua parte, un'integrazione di libreria o una costruzione minima; la scelta deve dipendere dalle differenze verificate.

### Banco discriminante inaugurale
1. Su HTML sintetico, fare doppio clic sulla **scritta** del nodo del diagramma, ottenere focus nello stesso nodo, cambiare il testo, completare la modifica, e annullarla con Undo. La freccia resta agganciata quando il nodo si sposta.
2. Duplicare una card e ricollocarla in una sezione a due colonne; la resa mobile conserva l'ordine logico.
3. Esportare e riaprire il documento, con ID e contenuti stabili, senza toolbar duplicate e senza perdere dati. Mostrare la differenza prima di applicarla a un altro file.
4. Ripetere il test su un documento non MAIOS; import/export arbitrary HTML è **ipotesi**, non promessa.
5. Valutare come proiezione distinta una scheda di presentazione; nessuna uguaglianza automatica fra layout CSS di pagina e coordinate di scena.

### Fonti di capacità da confrontare
- [Studio 20](../../../../examples/collaborative-communication-medium/AI_Collaboration_Studio.html): nodo editabile direttamente, scene, links, undo, selezione e round-trip AI.
- [Siteman Studio](https://github.com/GrazianoGuiducci/d-nd_com/blob/main/components/admin/SitemanStudio.tsx): contentEditable nell'editor redazionale e passaggio visuale/sorgente, non importatore arbitrario di siti.
- [GrapesJS core](https://grapesjs.com/docs/), [Puck](https://puckeditor.com/docs), [Tiptap](https://tiptap.dev/docs/editor/), [Excalidraw](https://github.com/excalidraw/excalidraw), [tldraw](https://tldraw.dev/): strumenti/referenti con ambiti e licenze differenti, da rivalidare nella forma scelta.
- [D-ND Design](https://github.com/GrazianoGuiducci/d-nd-ux-ai-seed): Interaction Quality e Perceptual Composition.

### Come questa guida impara
Registrare una differenza solo quando cambia un gesto o il prossimo metodo. Per ogni episodio utile conservare: **fonte e intento → implementazione/competenza realmente selezionata → prova eseguita → differenza vista → ragione fondata o ipotesi → cambiamento della capacità → prova successiva discriminante**. Non costruire report ripetitivi. L'operatore può cambiare priorità nell'uso e il nucleo deve seguire la trasformazione, non un backlog chiuso per inerzia.

**Stato di formazione:** metodo scritto nell'owner K-UX-AI; una prova futura non identica dovrà mostrare che la nuova competenza viene esercitata e corretta senza doverla reinsegnare.
