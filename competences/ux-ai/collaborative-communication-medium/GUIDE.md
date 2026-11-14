# Collaborative Communication Medium — guida viva

## 14 novembre 2026 — la demo come guida modificabile

I casi riferiti di revisione web con Codex e costruzione di presentazioni
aziendali con GPT individuano la stessa relazione: una correzione
attuata sulla rappresentazione può proseguire nel lavoro di chi la
riceve. La [proposta per la nuova demo](METACANVAS_SELF_DEMO.md) lega
ogni capacità a un esito pratico, forma il caso da esercitare nell'editor
e distingue la condivisione di una scheda già supportata dall'estrazione
di un sottoinsieme di nodi da esplorare. Il seguito è comporre la demo
nativa IT/EN e la revisione modificabile della pagina MAIOS.it.

## 13 novembre 2026 — distribuzione localizzata e demo derivata da sorgente

**Differenza emersa:** dopo la prima demo inglese con selettore, l'operatore ha determinato la topologia di pubblicazione: una pagina italiana e una inglese di MAIOS.it, ognuna riferita a un HTML della propria lingua ospitato in K-UX-AI. Una possibilità tecnicamente presente (toggle EN/IT dentro il singolo file) **non equivale** al percorso scelto per i riceventi; il mezzo deve incarnare la relazione di distribuzione, non aggiungere opzioni visibili per inerzia.

**Metodo:** formare la demo in scene modificabili partendo da una sorgente autoriale corrente; conservare distinte fonte di pagina, traduzione, rappresentazione da presentare, documento dell'utente e sito futuro. Produrre due file HTML coerenti ma indipendenti, con collegamenti e contenuti linguistici propri; verificare non solo la lingua delle scene, ma anche l'involucro usato per comprenderle e modificarle (toolbar, guida, template). Conservare ID/link e reversibilità di Demo/Canvas vuoto. Il tool generale resta un'identità distinta, non eliminata dalla demo.

**Prova:** pubblicati entrambi in `examples/collaborative-communication-medium`; Node syntax, sette scene senza overflow dei contenuti, Open/Present, conferma della nuova demo, blank e save/reopen in Chromium, viewport 390 px senza overflow della pagina. Nessun test su touch fisico, Chrome Windows file://, storage reale o deployment del sito. I riferimenti per il sito stanno nel [handoff](../../../../examples/collaborative-communication-medium/MAIOS_RESOURCE_TOOL_HANDOFF.md); Codex non si attiva per la sola esistenza di una fonte.



## 13 novembre 2026 — Studio 20: complessità percettiva minima e continuità dell'oggetto

**Fonte del lavoro:** l'operatore ha richiesto di mantenere bassa la complessità visiva, far partecipare D-ND Design al flusso delle idee, controllare gli aspetti verificabili e continuare oltre il solo perfezionamento geometrico. Il medium è stato portato dalla versione Studio 19 a Studio 20 e poi pubblicato in K-UX-AI dopo il controllo del carrier reale.

**Meccanismo riusabile:** un artefatto insieme *documento, editor e mezzo di cooperazione* non conserva la continuità soltanto salvando `state`. Il passaggio effettivo è: **quale parte consegno → cosa cambia nel ricevente → quali differenze tornano → cosa mantengo privato/localmente → quale gesto integra la modifica**. L'interfaccia ordinaria resta semplice mentre l'utente accede a scelte contestuali di export, confronto e recupero. Non usare più pannelli permanenti per ogni nuova possibilità. Conservare identità scena/nodi/links e un solo storico; integrare selettivamente senza annullare gli appunti privati locali omessi dal trasferimento.

**Incarnazione verificata:** export documento/scheda, privacy opt-in, confronto strutturale nuove/modificate/mancanti, selezione/Undo, recupero locale disattivato per difetto (testato con storage simulato), miniature più fedeli, blocco di URL remoti nelle immagini importate. HTML autonomo `examples/collaborative-communication-medium/AI_Collaboration_Studio.html` su GitHub K-UX-AI main al commit `0be329ae723110c62aa67d89756397683505319b`, con readback byte-identico. Sintassi Node corretta, esercizi Chromium circoscritti; nessuna prova di storage reale file://, touch, totale sicurezza o apprendimento del destinatario.

**Relazione con Design:** Interaction Quality conserva adattamento a larghezza/altezza, focus, orientamento e recupero; Perceptual Composition conserva gerarchia e spazio percettivo. K-UX-AI/CCM mantiene documento, stato, schema, comportamento di scambio e artefatto. D-ND Design ha un riferimento owner-native a questo caso; non spostare il codice in Design per darne conto, né fare della UI attuale una grammatica obbligatoria.

**Prossima conseguenza distinta:** futura pagina MAIOS.it in Risorse → Tool, tramite Codex e il vero owner del sito, con contenuti orientati a chi incontra lo strumento per la prima volta, seguendo le regole già presenti del sito. Un link/brief non è un'attivazione Codex né un deploy. [Passaggio sito](../../../../examples/collaborative-communication-medium/MAIOS_RESOURCE_TOOL_HANDOFF.md).


**Owner:** K-UX-AI / collaborative-communication-medium.  
**Stato:** 0.1.0 candidate, 11 novembre 2026.  
**Ingresso:** [SKILL](SKILL.md) → [CURRENT](CURRENT.md) → la sorgente del lavoro e la differenza reale da costruire.

## 13 novembre 2026 — Studio 15: il template come modello personale e azione reversibile

**Fonte operativa:** l'operatore vede la gallery e domanda «se aggiungo un template posso annullare l'operazione?»; propone inoltre di salvare i template modificati per riutilizzarli e sostituire il generico «Inserisci» con tre relazioni esplicite alla scheda corrente: **Sostituisci, Sopra, Sotto**. È un cambiamento del mezzo di comprensione, non un'aggiunta cosmetica. «Inserire» lasciava al software la scelta del rapporto con il documento esistente.

**Saper fare corretto:** l'interazione di una raccolta di template deve conservare due cose: (1) **autorità dell'operatore sul punto d'inserimento**, rendendo esplicito se una composizione sostituisce, precede o segue; (2) **reversibilità dell'effetto**, con lo stesso storico che porta le modifiche al documento. Le azioni bulk (5 template) sono una sola intenzione e un solo checkpoint; l'operatore può annullarle in un gesto. La sostituzione è distruttiva solo nella vista corrente e richiede conferma; Undo recupera la scena precedente senza falsare la storia.

**Riutilizzo senza perdita di referente:** un template salvato non è la stessa scheda viva: è un modello che conserva contenuto/relazioni, ma la sua istanziazione deve ricevere nuovi ID per scena, elementi e link, compresi riferimenti `containerId`, evitando collisioni. I template personali vivono nel documento di lavoro e possono migrare con `metacanvas.templates.v1`; non richiedono server o persistenza automatica esterna. `Esporta raccolta`/ `Importa raccolta` portano materiale fra documenti ma non equivalgono a sincronizzazione.

**Privacy dal livello giusto:** poiché l'HTML è sia sorgente dati sia editor con DOM già renderizzato, una copia pubblica che cancellasse `savedTemplates[]` nel solo JSON lascerebbe i nomi personali nelle card già presenti nel DOM clonato. È stato necessario ripulire **anche** il DOM di `#savedTemplateList` e normalizzare il contatore. Il template estratto esclude note ed elementi `private:true`, ma non può dedurre segreti contenuti in testi non marcati: l'export espone questo limite e richiede revisione umana. L'importazione JSON con riferimenti invalidi o immagini remote viene rifiutata prima del commit.

**Prova locale:** test di inserimento sopra/sotto, sostituzione annullata/confermata, Undo/Redo, bulk 5 in un passo, template salvato, trasferimento ad altro file, preservazione di frecce, riapertura HTML, copia pubblica senza dati personali, stripping di note private, rifiuto `image.src` remoti e nessun pageerror osservato. La competenza futura deve ricordare che **l'HTML è insieme carrier dati e superficie interattiva clonabile**: il contratto di privacy attraversa entrambi.

## 13 novembre 2026 — Studio 14: Presenta, spazio e gesto di modifica

**Fonte:** l'operatore riporta quattro difetti/incomodità del medium: ridimensionamento del modale Strumenti, Presenta vuota, spazio orizzontale sprecato e difficoltà di uscire da modifica. Il gesto corretto nasce dal documento concreto, non dalla pretesa di imporre un nuovo workflow: recuperare canvas visibile, controllo percettivo dello spazio, e azioni temporali chiare mentre il testo viene cambiato.

**Meccanismo del difetto e risultante:** l'editor aveva una grid a due colonne e nascondeva la sidebar in `body.presenting`, ma non la geometria della grid; la colonna canvas collassava a 0 px. Modalità Presenta adesso cambia composizione della shell a blocco prima di ridimensionare il canvas. Il pannello Strumenti in modalità mobile era governato da CSS `!important` e un resize/grip dentro un contenuto scrollabile: ora i grip sono overlay fissi riposizionati sui bordi reali, e un angolo di presa modifica entrambe le dimensioni in modalità floating. L'export ricolloca i grip dentro il DOM prima dell'esecuzione del codice nel nuovo file: senza questo passaggio, il documento esportato poteva perdere le maniglie di resize.

**Nuova possibilità senza perdita del referente:** Flat allarga la superficie di lettura e riduce margini/cornici, passando a due colonne a desktop e a una su mobile. Lo stato è preferenza `state.ui.flatLayout`, non cambiamento dei concetti, frecce o coordinate. Quando si entra in modifica, un piccolo menu persistente OK/Indietro/Avanti rende visibile la possibilità di concludere o rivedere i passi; l'input quick editor evita checkpoint ripetuti quando un evento change non contiene nuova informazione. Si conserva un unico storico, non una seconda storia della UI.

**Prove e limiti:** prove Playwright reali sui quattro canvas in Presenta, dock laterale/top/bottom/floating, trascinamento a larghezza/altezza, cambi Flat/standard, mini editor/toolbar, Undo/Redo e salvataggio-riapertura. Copia pubblica con marcatori privati in note/libreria, assenti nel risultato; MPL preservata. Node `--check`, viewport 390px senza overflow. I test non attestano touch fisico o tutte le tecnologie assistive. Codex/TM9 mantiene la pagina MAIOS.it; questo movimento modifica soltanto il tool pubblico K-UX-AI e la sua fonte privata tm7.

## 13 novembre 2026 — MetaCanvas: dal passaggio al ritorno strutturato

**Evento:** nel primo tool pubblico l'operatore può esportare dati JSON per una AI, ma un LLM che restituisce quel JSON modificato non ha un gesto di rientro equivalente nel documento già aperto. Il mezzo unidirezionale rende difficile continuare l'oggetto senza rimaneggiare l'intero HTML. Il valore del medium non è semplicemente offrire un pulsante d'importazione: **stessa identità semantica attraverso rappresentazione umana, file, AI, file di ritorno e nuova rappresentazione umana**.

**Risultante in 0.1.1:** importazione di `ccm.document.v1` da JSON o HTML che contiene `#ccm-data`, leggendo solo dati, senza valutare HTML o script ricevuti. Prima del gesto verificare schema, ID e collegamenti, conservare l'attuale stato per Undo, mostrare titolo e numero di schede e chiedere conferma perché il documento viene sostituito, non fuso. Le chiavi UI sono preferenze; la versione pubblica di un documento importato può tornare in modalità editabile come copia di lavoro, senza inventare appunti privati rimossi. La UI e il copyright originario rimangono quelli dell'applicazione locale, non vengono sostituiti dal contenuto del file importato.

**Prova:** test Chromium locale su JSON→HTML, undo/redo, import HTML con script marcatore non eseguito, rifiuto di frecce con target assente, annullamento della conferma, rientro da copia pubblica, viewport mobile 390px e assenza di errori JavaScript nei percorsi; test di esportazione pubblica con indicatori privati in note e libreria, nessun indicatore nel documento prodotto. Node `--check` per gli script incorporati. Limite: non sono una certificazione di sicurezza su tutte le strutture ostili o sulla compatibilità reale con ogni browser. Non fare della validazione un contenuto o una verità semantica; essa controlla soltanto l'integrità minima del carrier.

**Ritorno di metodo:** quando si costruisce un mezzo di scambio con un altro ricevente, verificare che il **risultato ritorni in uno stato ancora modificabile dall'operatore**, distinguendo un documento restituito da un effetto esterno eseguito. La funzione appartiene alla competenza CCM e al Code Medium; la pagina del sito resta all'owner Codex/MAIOS.it.

## 13 novembre 2026 — ingresso pubblico neutro, contenuto distribuibile e prodotto controllato

**Sorgente e mandato:** dopo dodici iterazioni locali del medium HTML, l'operatore chiede come farlo usare immediatamente da chi non conosce MAIOS o le sue metalogiche, e propone una risorsa pubblica con controllo commerciale del prodotto UX-AI: apertura del sapere fondativo non implica pubblicazione dei tool sotto licenza MIT; tutti devono poter usare lo strumento, ma la sua rivendita/white-label come prodotto UX-AI richiederebbe una concessione distinta. La proposta di licenza è una **direzione autoriale da qualificare**, non un testo di concessione giuridicamente definito né pubblicazione già esercitata.

**Distinzione formativa:** un **metodo pubblico per l'AI** e un **artefatto utilizzabile da una persona** non devono presentare lo stesso testo di ingresso. Il primo richiede il modello dati, riferenti, identità, fonti e modo di continuare; il secondo comincia da cosa si può fare ora, un esempio, il gesto di modifica e l'output che può condividere. La specializzazione del kernel può rimanere esplicitamente attribuita in documentazione tecnica senza proiettare KA, FDLA, Meta_Skill, path e cronologia aziendale nelle schede illustrative. Qui la conoscenza del produttore ha formato il metodo, ma non deve essere prerequisito di accesso per il ricevente.

**Prima incarnazione locale, non pubblicazione:** il pacchetto `AI_Collaboration_Studio_Public_Preview_Package.zip` contiene editor neutro `AI_Collaboration_Studio_Preview.html`, due pagine indice IT/EN `strumenti/index.html` e `tools/index.html`, README, manifest con hash, bozza di decisione licenza e checklist. L'HTML di ~189 KB usa quattro scene sintetiche, «Presenta un'idea», «Spiega un processo», «Lavora con un assistente AI» e «Pagina vuota», guidate da una barra di primo uso e dal dialogo Guida. L'editor rimane in italiano: la pagina inglese è introduzione, non prova di traduzione UI. Nessuna risorsa Schnell e nessun contenuto aziendale. SHA-256 del preview HTML `a95652dace40bcb5db6b594e8e23d2984378bed968a9aeae084e7f5ec46301c6`; ZIP `0321de2935b60f6dbc92a4381da9d0c6111b51a4cd5e451b6b52cc2e189a78ea`. Gli artefatti rimangono locali alla chat: **non sono nel repository né su MAIOS.it**.

**Prove locali attribuite:** Chromium/Playwright `set_content`: quattro scene leggibili, banner di primo uso e guida richiamata, cambio della scheda, modifica del titolo, richiesta di download dell'HTML, recupero di un file concreto in harness, ricaricamento del modello JSON con titolo e scene conservati; viewport 390 px senza overflow orizzontale, zero errori pagina osservati nei percorsi. Manifest e ZIP corrispondono byte-per-byte ai file. La procedura non ha esercitato apertura reale `file://` nel browser dell'operatore, sicurezza completa contro input ostili, PDF stampato, sito live o accettazione della licenza.

**Confine giuridico e tecnico che incide sul modo di distribuire:** la repository K-UX-AI è pubblica ma non presenta un file `LICENSE` riconosciuto al momento della ricognizione; il `private:true` del package.json non è una licenza. MIT, AGPL e altre licenze OSI consentono forme di uso/vendita commerciale e non soddisfano una proibizione della rivendita. Un eventuale permesso d'uso gratuito con divieto di rivendita/white-label va definito come licenza commerciale/proprietaria source-available, non «open source». La direttiva UE 2009/24/CE tutela l'espressione del programma e non il concetto astratto di interazione; nome, grafica originale e codice hanno eventuali forme di tutela distinte, da accertare con competente consulenza legale.

**Il problema di licenza introdotto dal mezzo stesso:** quando un utente salva un documento, il singolo HTML incorpora **anche l'intero editor**. Un divieto generico di ridistribuzione del software potrebbe vietare involontariamente la condivisione delle presentazioni per le quali l'editor è stato costruito. La licenza dovrà distinguere esplicitamente: uso interno e creazione di documenti; concessione di distribuzione di copie documento che incorporano il runtime per la lettura/revisione; assenza di permesso automatico di vendere, ribattezzare o ospitare l'editor come prodotto indipendente. Il contenuto creato dall'utente e il mezzo che lo incorpora sono oggetti distinti anche quando i loro byte viaggiano insieme. Senza questa distinzione una protezione commerciale distruggerebbe la portabilità che costituisce il valore del medium.

**Composizione con owner esterni:** K-UX-AI possiede metodo, artefatto e release. La futura pagina `/strumenti/` e `/tools/` appartiene all'owner `maios_it`, che già espone Kernel, Meta-skill e Attività programmate in raccolte distinte. «Strumenti AI» diventerebbe una quarta raccolta, non una meta-skill rinominata; la sorgente del prodotto va esposta con ID/revisione verificabili e la pagina del sito riceve quell'oggetto. La pubblicazione del sito, le condizioni di licenza, la versione del prodotto, l'eventuale attivazione della sua API e la comprensione di un destinatario sono effetti separati. Il sapere utile per formare una nuova risorsa resta raccordato a Meta_Skill/form-public-metaskill-resources, senza duplicarne il metodo.

**Seguito selezionabile:** qualificare sorgenti/diritti dei componenti, definire la licenza proprietaria con eccezione per il documento esportato, verificare sicurezza e browser reali, tradurre interamente la UI se si promette inglese, assegnare versione e manifest immutabili. Solo dopo decisione sul perimetro fare owner-native release e proiezioni del sito. Non importare automaticamente nel runtime pubblico i prototipi creati nella chat e non rendere una bozza di licenza un permesso operativo.


## 12 novembre 2026 — Studio 12 — due superfici laterali con geometria propria

**Fonte:** dopo Studio 10 (editor contestuali chiudibili/espandibili) e Studio 11 (lista delle schede a sinistra e pannello proprietà ridimensionabile), l'operatore chiede di proseguire e includere ciò che aiuti concretamente. La direzione materiale è **rendere governabile la densità dell'ambiente**, non aumentare indiscriminatamente le funzioni: l'elenco delle schede deve poter restare visibile o sparire; il catalogo a destra deve poter aumentare di larghezza e sfruttare lo spazio aggiunto senza lasciare i suoi controlli stretti in una sola colonna.

**Risultante locale:** `MAIOS_CCM_Studio12_Editor_Guida.html` (185.345 byte, SHA-256 `e0f9ae538cf3808f1d59fae06a49b3a3f917fe06d2cd9bd024d677c2fb0f954d`) e `MAIOS_CCM_Studio12_Presentazione_Preconfigurata.html` (199.880 byte, SHA-256 `c7f11faf37ea9827899c76a11c5b7adbc981b5ecbce62d4fe24372a0343e09c2`). ZIP alternativo (107.278 byte) conserva entrambe le copie. Sono file HTML/JS/CSS autonomi nel ricevente ChatGPT, senza dipendenze esterne; non sono ancora runtime, release o demo pubblica K-UX-AI.

### Meccanismi riusabili appresi

1. **Navigazione a due rappresentazioni della stessa scheda.** La colonna sinistra offre Elenco e Miniature: le miniature sono SVG leggeri ricostruiti dal modello documentale `ccm.document.v1` (rettangoli, testi abbreviati e relazioni indicative), non immagini esportate né copie dello stato da aggiornare separatamente. Scelta, titoli e sequenza si riferiscono agli stessi ID delle schede; la colonna può essere nascosta e ripristinata. Le note del relatore non entrano nell'anteprima sintetica. Il rendering della miniatura è orientativo e non sostituisce la vista effettiva del canvas o la resa finale delle frecce.

2. **Composizione della larghezza.** La colonna sinistra è ridimensionabile trascinando il bordo; il pannello strumenti da destra ha pulsanti +/- e un bordo trascinabile. La larghezza diventa informazione UI conservata nel documento, ma non muta la geometria semantica degli oggetti. Il canvas può avere scroll/zoom quando entrambi i pannelli sono visibili e il residuo non basta, invece di ridurre arbitrariamente i caratteri.

3. **Responsive interno al pannello, non soltanto alla pagina.** Il pannello Strumenti usa query sul proprio contenitore: da due a tre o quattro colonne nel catalogo di elementi, e da una a più colonne per template e schede. Sette gruppi semantici sono richiudibili: schede, elementi, template, layout/temi, elementi salvati, livelli, salvataggio/esportazione. La ricerca filtra i gruppi senza cancellarne il contenuto. I comandi preesistenti restano gli stessi ID/effetti; il nuovo layout non crea nuove funzioni non verificate.

4. **Memoria dei pannelli distinta dal documento.** `state.ui.slideView`, `slideRailWidth`, `toolWidth`, `toolHeight` e `toolSections` sono preferenze dell'artefatto, trasferite nel file salvato con `state.ui`. La reidratazione riprende la geometria su desktop. Un difetto emerso nel test: chiamare la funzione di adattamento all'apertura in viewport molto stretto sovrascriveva la larghezza salvata con la misura minima momentanea (315 px). Correzione: l'adattamento alla viewport **proietta** una larghezza corrente senza riscrivere lo stato; solo un gesto di ridimensionamento o pulsante intenzionale aggiorna la preferenza. Un altro difetto: il `toggle` iniziale di `<details>` al caricamento marcava il documento «modificato» senza gesto umano. Correzione: segnare variazione soltanto quando il valore di apertura cambia rispetto allo stato persistito.

5. **Mobile leggibile e distinta dalla vista spaziale.** La prima prova CSS manteneva erroneamente `grid-template-columns:auto 1fr` fuori dall'override responsive: rail e lettura a 390 px finivano affiancate, con testi verticali lettera per lettera. L'override corretto impila i pannelli, limita l'altezza della lista delle schede e lascia alla rappresentazione di lettura l'intera larghezza. Questa è una correzione di composizione percettiva, non un semplice vincolo di breakpoints.

6. **Test degli effetti, non soltanto delle classi.** Il ridimensionamento del pannello destro sembrava non reagire in un test subito dopo l'apertura perché la transizione di ingresso ne cambiava ancora le coordinate: il puntatore finiva su un altro elemento. Il test deve attendere che l'entrata si assesti; durante un ridimensionamento effettivo il pannello usa `transition:none` per mantenere il bordo sotto il puntatore. Verificare `getBoundingClientRect`, colonne CSS effettive e stato esportato, oltre al click handler.

**Prove osservate:** Chromium/Playwright con contenuto HTML realmente caricato via `set_content`: entrambe le copie, sette o tre schede, commutazione elenco/miniature, selezione scheda, show/hide, sette gruppi strumenti, ricerca, espansione dei controlli su tre e quattro colonne, pulsanti e drag dei bordi, dock top/bottom/right, modalità Presenta con pannelli nascosti, salvataggio HTML e riapertura con preferenze e dati conservati, lettura e tools su viewport mobile 390 px. Test JavaScript con `node --check` senza errori. Le prove non attestano touch fisico, apertura diretta `file://` nel browser dell'operatore, PDF finale, efficacia nella presentazione reale o assimilazione in altri receiver. Il limite pratico di file rimane sotto 2 MB.

**Seguito:** chiedere riscontro dell'operatore sulla navigazione a sinistra e sul catalogo largo a destra con contenuti reali. Solo le conseguenze d'uso devono giustificare ulteriori opzioni; lasciare all'owner dei contenuti la qualità e l'esattezza delle schede.


## 12 novembre 2026 — Studio 09 — il file modificabile è una fonte di lavoro per l'LLM

**Fonte operatore:** la presentazione con template agentici deve spiegare, in una piccola guida nel proprio HTML, la sua funzione di **mezzo per interagire con gli LLM costruendo un documento utilizzabile anche verso le persone**. L'operatore chiede inoltre una prova reale della capacità di ChatGPT di ricevere questo tipo di file, leggerne contenuti e relazioni con le competenze del sistema, e restituire una presentazione già organizzata, che l'operatore possa aggiustare. Altri metodi devono restare possibili.

**Esercizio del ricevente, non nuova promessa del runtime:** l'istanza ChatGPT ha letto il file Studio 08 e il JSON `ccm.document.v1`, conservando il catalogo di cinque template. Ha raggiunto le sorgenti owner-native MPK/Competence Formation, Source Transformation and Effect, Continuing Activities, Meta_Skill e K-UX-AI. Da queste ha **composto una nuova esposizione illustrativa in sette schede**, non una copia non modificata dei template: intenzione e contesto; formazione del saper fare; interazione persona/AI; cooperazione fra agenti; differenza fra proposta ed effetto; continuità dopo un evento; uso dell'HTML stesso. Ogni scheda porta nodi, relazioni con referenti validi, appunti privati per il relatore e URL delle fonti nel campo `sourceRefs`. Le frasi dei diagrammi sono sintesi e rappresentazioni situate, non prove di implementazioni agentiche attive.

**Artefatti locali:** `MAIOS_CCM_Studio09_Editor_Guida.html` (151.399 byte; SHA-256 `a8e427622337d7c178ff0d7acbb6217510fbd13c217449a449ee0b529185bf03`); `MAIOS_CCM_Studio09_Presentazione_Preconfigurata.html` (165.934 byte; SHA-256 `61b7a327bf9e220f6556ea345c18a3e757dfb3872628ab4bbf84bd34ca7d5caf`); JSON della presentazione (28.977 byte; SHA-256 `c089b5e3b3dccd8b5853b4176a0ad0b27eb2aacb9b4439531cd07b4fcc1c7c8d`); ZIP verificato come contenitore di file identici. Questi artefatti sono locali alla conversazione e non parte di una release, sito o runtime K-UX-AI.

**Guida in superficie:** il comando visibile `? Guida` apre un dialogo nativo HTML accessibile, chiudibile con Escape, con tre azioni comprensibili: formare/modificare la rappresentazione; salvarla e allegarla a un LLM chiedendo lettura strutturata e restituzione revisionata; presentarla o prepararne una copia pubblica. Una richiesta pronta e copiabile orienta il ricevente al JSON nel tag `script#ccm-data`, distinguendo fatti, ipotesi e stato dell'effetto. La clipboard può essere indisponibile su file locali; in tal caso il testo viene selezionato per copia manuale. Il dialogo non occupa il canvas quando chiuso e non collega automaticamente alcun provider.

**Meccanismo riusabile per il prossimo caso:** l'artefatto non deve essere letto soltanto come screenshot o «slide da abbellire». Prima si recuperano **identità e stato del documento** dal JSON, contenuto dei nodi, relazioni e loro predicati, provenienza, note e destinatario. Si raggiungono le fonti e competenze reali che possono cambiare la domanda; si forma una sequenza comunicativa, eventualmente con una topologia diversa, conservando modificabilità, stato privato/pubblico, ID coerenti e capacità di ritorno. La capacità del modello si esercita ricevendo e interpretando il file in questa conversazione; non diventa per questo AI integrata offline né monitoraggio o collaborazione in tempo reale. Un prompt che richiede solo «riordina slide» può perdere ragioni e relazioni; un ingresso consapevole permette anche di proporre nuove domande e rapporti, lasciando all'operatore la correzione.

**Prove:** HTML reale caricato in Chromium/Playwright tramite `set_content`: sette schede e collegamenti renderizzati senza errori JS, dialogo guida aperto/chiuso, modifica titolo → download del file → lettura JSON → riapertura, modalità Presenta con note private escluse, nuovo template aggiunto senza perdita delle sette schede, copia pubblica senza testo delle note, interfaccia di lettura a 390 px, editor generico iniziale con tre schede e catalogo ancora operativo. Ispezione della resa su tutte le sette schede: nessun avviso di testo fuori campo dopo la correzione di un riquadro. ZIP letto e confrontato byte-per-byte coi tre artefatti. La prova non implica che l'operatore abbia già scaricato e usato Studio 09, né assimilazione in un altro LLM, test `file://` nativo, touch fisico o validazione da un pubblico reale.

**Conseguenza:** per questa competenza, l'HTML è **medium reciproco fra comprensione, codice e esposizione**: lo stesso documento è materiale di lavoro per l'operatore, fonte strutturata per il modello e presentazione per terzi. La guida riguarda il *come riceverlo e restituirlo* e non impone una forma unica di utilizzo. Il prossimo caso umano può correggere sia il racconto sia le affordance, conservando l'owner delle fonti e la prova del gesto.


## 12 novembre 2026 — Studio 08 — template agentici come ipotesi modificabili

**Fonte:** dopo il rafforzamento del motore delle frecce, l'operatore propone di creare template perché K-UX-AI ha ormai capacità sufficienti per rappresentare e organizzare le logiche di sistemi agentici. Non chiede di definire l'unica ontologia dei sistemi agentici. Il lavoro è stato formato con Collaborative Communication Medium, K-UX-AI, MPK / Competence Formation e Meta_Skill, lasciando ai singoli owner i fatti del loro dominio.

**Risultante locale esercitata nel ricevente ChatGPT:**
- `MAIOS_Comunicazione_Collaborativa_Studio08.html` (145.276 byte, SHA-256 `279014c28f060f1eddc07ed561b1e753fa5866bb136919e44cf458e03972bc91`): editor autonomo con nuova sezione «Template · Sistemi agentici», cinque modelli preconfigurati e un comando per aggiungerli tutti.
- `MAIOS_Template_Sistemi_Agentici.html` (153.266 byte, SHA-256 `6e775f94929f17943ecc21f2ceb18bf575e8ffc5b360c81afdbbf26440d4a1cb`): presentazione autonoma già composta dalle cinque schede.
- `MAIOS_Template_Sistemi_Agentici.json` (18.802 byte, SHA-256 `27b47078465e2d1a6ec6e89b25656936a057fd63fbb20925e9f1c92c2c99166b`): modello dati della presentazione per lettura/revisione da parte di un ricevente AI.
- `MAIOS_Studio08_Template_Agentici.zip` (90.915 byte, SHA-256 `4cab7f38b3af33416935379e800da678dc65039af3aa0e1b367866cc61807925`), contenente i tre file identici ai singoli artefatti.
Sono artefatti della conversazione; **non** una nuova release, integrazione nel runtime K-UX-AI, deploy sul sito o adozione presso altri kernel.

### Contenuto e funzione dei cinque template

1. **Dall'intento alla competenza**: contesto/fonti, competenza, lavoro/risultante e apprendimento. È una relazione aperta: formazione della capacità e ritorno dall'esperienza non sono sempre una sequenza lineare né equivalgono a un automatismo.
2. **Lavoro reciproco umano–AI**: persona, oggetto condiviso, sistema AI e interlocutore. Una freccia in entrambe le direzioni rappresenta scambio possibile, non accesso completo o sincronizzazione già esercitata.
3. **Cooperazione fra agenti**: Agente A, contesto di progetto, Agente B e risultante esposta. «Contesto di progetto» non diventa per questo un supervisore autoritario, memoria perfettamente condivisa o controller della realtà esterna.
4. **Dalla proposta all'effetto**: sorgente, proposta, decisione, effetto/ricevuta. Il disegno preserva la differenza fra proposta, autorizzazione ed esito verificato; anche una «ricevuta» può riferirsi alla richiesta e non all'effetto.
5. **Continuità dopo un evento**: evento, presente esposto, seguito e ritorno al metodo. Stato precedente ed evidenza nuova partecipano senza riscrivere retroattivamente il passato.

### Metodo e insegnamento

**Template come ipotesi modificabile, non topologia imposta.** Un diagramma preconfigurato può abbreviare il lavoro quando la sua grammatica aiuta a esporre una relazione reale. Non prova che gli agenti, le fonti, i controller, i permessi o gli effetti esistano nel sistema del destinatario. Ogni nodo ha un riferimento testuale, ogni freccia ha soggetti e predicato e, quando utile, due ancoraggi iniziali scelti per la leggibilità. Queste connessioni restano modificabili. Non promuovere le parole e le frecce del template a fatti operativi senza sorgente e conseguenza.

**Inserzione non distruttiva e continuità.** La scelta di un template aggiunge una scheda dopo quella attiva, senza cancellare le esistenti; aggiungerne cinque produce cinque schede nuove. La funzione forma nuovi ID stabili per nodi e relazioni, conservando `templateSource:{id,revision,kind:'illustrative'}`, e usa il medesimo `ccm.document.v1` del mezzo. La presentazione precompilata usa le stesse schede come documento autonomo, riproducibile da file. Il catalogo è disponibile soltanto come codice dentro questo HTML locale, non come funzione già presente nei consumer pubblici.

**Percepibilità del diagramma.** La prima prova visuale mostrava un collegamento orizzontale agganciato al bordo inferiore, sebbene i nodi fossero affiancati. La correzione ha fornito ai modelli lati iniziali espliciti per i collegamenti ordinati (`right→left`, `bottom→top` ecc.), lasciando al motore Studio 07 la modifica del tragitto quando le forme vengono spostate. L'insegnamento è che un buon preset non deve lasciare al router il compito di dedurre ciò che la forma iniziale del template già determina; quel preset resta però una proiezione, non un vincolo sul significato o un percorso obbligatorio.

**Prova qualificata:** JavaScript sintatticamente valido; Chromium/Playwright via `set_content`: cinque inserimenti singoli, inserimento dell'intero insieme, documento salvato e riaperto con ID unici e link a nodi esistenti, tema Grafite, copia pubblica e modalità Presenta, nessun errore JavaScript osservato. Cinque template e sedici collegamenti esaminati nella disposizione iniziale: nessuna freccia campionata attraversa il corpo dei nodi nella prova. HTML pack salvato/riaperto con cinque scene, ZIP verificato byte-per-byte. Non è stata esercitata l'apertura `file://` sull'host dell'operatore, comprensione reale di interlocutori, touch o assimilazione della libreria in un altro ricevente. Ogni eventuale caso cliente conserva la propria conoscenza e non entra per default nel catalogo pubblico.

**Seguito:** provare la personalizzazione di un template su un sistema concreto, distinguere graficamente osservato/proposto/unknown, e far ritornare alla competenza la grammatica che aiuta davvero la comunicazione dopo l'uso.

## 12 novembre 2026 — Studio 07: il gancio è un oggetto percettivo, non un nuovo referente

**Ingresso dell'operatore:** dopo il caso-limite di Studio 06 con due riquadri orizzontalmente a contatto, viene selezionato un motore di percorso che aggiri l'unione delle sagome senza strisciare sui lati. Il nuovo contributo chiede punte attivabili **all'inizio, alla fine, a entrambi gli estremi** (e facoltà di disattivarle), estremi e ganci sempre visibili davanti ai riquadri, e **quattro ingressi standard per lato** perché più relazioni possano convergere sulla stessa scheda senza coincidere nello stesso punto.

**Prima incarnazione esercitata:** HTML autonomo locale `MAIOS_Comunicazione_Collaborativa_Studio07.html`, **135.511 byte**, SHA-256 `d56564923d767f09119e75984ec54a885a64f5ad2aaac6eeae2da8a7b591a7c8`; ZIP alternativo di 39.948 byte con lo stesso HTML verificato byte-per-byte. Il nuovo codice conserva lo schema `ccm.document.v1`, i tre fogli dimostrativi e il medium offline. Sorgente e prove sono nel ricevente ChatGPT; non c'è una modifica del runtime, del package, del sito o della release di K-UX-AI.

### Metodo corretto dall'esperienza

**1. La relazione resta attribuita mentre l'itinerario cambia.** `from`/`to` e `label` conservano il referente e il predicato. Il routing automatico forma le sue alternative secondo le posizioni presenti. Se due riquadri si toccano o si sovrappongono parzialmente, una linea diretta è penalizzata perché corta o perché attraverserebbe lo spazio delle sagome. Le alternative includono segmenti che escono dal lato scelto, gomiti brevi e aggiramenti esterni al gruppo da sopra, sotto, destra e sinistra, con angoli morbidi. Il confronto penalizza collisioni con sagome e zone di rispetto, ripiegamenti, direzioni d'uscita/ingresso sbagliate, tragitti troppo corti e cattiva collocazione dell'etichetta. La sua nuova geometria non è un nuovo significato.

**2. Quattro porte su ogni lato.** Per ogni riquadro ci sono quattro punti di bordo alle frazioni `0,2 / 0,4 / 0,6 / 0,8` di ogni lato. Le frecce normalmente centrali possono usare la coppia di porte interne; più relazioni verso lo stesso lato vengono distribuite fra le quattro posizioni con un ordine deterministico legato ai nodi di provenienza. `fromAnchor/toAnchor` e `fromPort/toPort` sono proprietà esplicite e opzionali del collegamento. La selezione di una relazione rende raggiungibili nell'HTML i 16 piccoli punti trasparenti del nodo sorgente e i 16 di quello di destinazione; un click o la tastiera possono fissare il punto desiderato. L'editor avanzato permette di scegliere lato e porta direttamente. Oltre quattro frecce sullo stesso lato non si dichiara una disponibilità illimitata di porte uniche: si può usare un altro lato o un attacco manuale.

**3. Gancio visibile, senza cancellare la sagoma.** Il layer SVG della freccia ora ha precedenza visiva sugli elementi del canvas. Cerchi di aggancio semitrasparenti e punte rimangono percepibili sul bordo. I tracciati non devono attraversare il corpo degli oggetti automaticamente per beneficiare dello z-index superiore: i collegamenti sono disegnati fuori dal corpo e solo i loro ganci toccano il bordo. Hit-target espliciti permettono di scegliere e trascinare la linea; la superficie SVG trasparente non intercetta indiscriminatamente il lavoro sui riquadri. Una curva **manuale** può attraversare un oggetto se l'utente la porta lì: è una scelta grafica distinta dal comportamento di aggiramento automatico.

**4. La direzione grafica è configurabile.** Nuova proprietà `heads: none | start | end | both`, con selezione dal mini editor e dall'editor avanzato. La vecchia `arrow:false` si legge come `none`; l'assenza della nuova proprietà conserva per compatibilità la punta finale. Le punte sono renderizzate su `marker-start` e/o `marker-end`; una doppia punta **non modifica** in automatico gli ID di origine/destinazione né implica reciprocità causale del rapporto. Il comando «Inverti» scambia anche preferenze di lato e porta, non solo gli ID e le coordinate.

**5. Continuità tra gesto, proiezione e file.** Trascinare un estremo vicino a un punto di bordo seleziona esplicitamente nodo, lato e numero della porta; trascinarlo nel vuoto conserva la posizione libera. Il centro conserva la distinzione già acquisita tra deformazione e ricablaggio del rapporto. L'export HTML porta nel JSON questi nuovi campi senza introdurre dipendenze esterne. La copia pubblica e la vista di presentazione mantengono le punte scelte; gli appunti restano privati secondo il controllo già formato.

### Prova osservata e limiti

Browser Chromium/Playwright in ambiente di test con l'HTML effettivo: **sette** casi geometrici — baseline, contatto orizzontale, distanza di 4 px, sovrapposizione di 18 px, sfalsamento con ostacolo, contatto verticale, ordine invertito — su **due** collegamenti ciascuno. Nei 14 percorsi controllati nessun punto campionato ha attraversato l'interno dei riquadri e le etichette non si sono sovrapposte ai riquadri in quegli scenari. Su quattro relazioni forzate verso il lato sinistro del medesimo nodo, le quattro destinazioni sono risultati punti differenti a `20/40/60/80%` del lato. Le quattro modalità di punta sono state verificate nel DOM SVG. Il test di interazione ha cliccato realmente un punto di aggancio, salvato l'HTML, riaperto il risultato e confermato lato/porta; ha cambiato le punte tramite mini editor e ne ha confermato la conservazione dopo un nuovo download e rientro. È stata verificata l'assenza del testo di una nota privata nel sorgente della copia pubblica e l'identità byte-per-byte dello ZIP. Prova di render: 24 collegamenti su 12 nodi senza errori JavaScript, tempo iniziale misurato nel particolare harness circa 0,24 s; non è una garanzia universale di performance.

Questi riscontri **non** attestano ogni possibile intreccio denso, collisione fra tutte le etichette, più di quattro ingressi unici per lato, uso touch fisico, apertura `file://` nel browser dell'operatore, export PDF finale, accessibilità certificata o comprensione reale dell'interlocutore. La presentazione di esempio rimane neutra; non incorpora le modifiche che l'operatore può aver salvato sul proprio computer. La prova di assimilazione in un lavoro non identico rimane aperta.

**Apprendimento riusabile:** una comunicazione grafica non è una linea fra due centri. Il rapporto ha soggetti/ruoli; la resa ha una topologia vincolata dalle sagome; l'attacco ha una posizione percepibile e un'identità di porta; il testo ha la propria leggibilità; la direzione della punta è una proprietà grafica che può sostenere il significato senza inventarlo. Questo metodo deve continuare a K-UX-AI/Collaborative Communication Medium e comporsi con Source-Grounded Infographic/Interaction Quality quando un nuovo dominio rende necessarie altre distinzioni.

## 12 novembre 2026 — Studio 06: relazione, percorso ed etichetta non coincidono

**Evento sorgente:** il feedback dell'operatore sulla resa reale di Studio 05 in Chrome/Windows, con screenshot della scheda «Un'idea diventa condivisibile», segnala che «la logica delle frecce va rafforzata». L'immagine mostra tre riquadri sfalsati e una relazione che si incurva nell'interstizio fino a perdere leggibilità dell'etichetta. Il problema non è semplicemente il colore del tratto: **associazione semantica dei nodi, calcolo del tragitto e leggibilità dell'etichetta** sono tre oggetti differenti, con mutazioni e prove proprie. La modifica grafica non può attribuire un significato diverso a `from`, `to` o `label`.

**Prima implementazione esercitata nel ricevente ChatGPT:** `MAIOS_Comunicazione_Collaborativa_Studio06.html`, file HTML/JS/SVG autonomo di 126.062 byte (SHA-256 `602d1358382f93faf89a95c2747dbb71e8b0fe817c0d582eab582ae306bb5567`), con ZIP alternativo byte-identico. È disponibile come artefatto locale della conversazione, **non** installato nel runtime pubblico.

### Capacità esercitate e sapere da riutilizzare

1. **Collegamento tipizzato, resa derivata.** `from` e `to` conservano gli ID dei nodi; `fromAnchor`, `toAnchor` conservano eventuali lati scelti esplicitamente; la geometria automatica è calcolata dal presente degli oggetti e può cambiare senza mutarne i significati. `label` è predicato testuale attribuito al collegamento, distinto sia dal tratto sia dalla posizione del badge. Un oggetto cancellato lascia punti estremi liberi con coordinate reali, secondo il comportamento già esistente.

2. **Calcolo delle ancore e del percorso in modo situato.** Per un collegamento automatico il renderer confronta lati candidati, segmenti diretti ed elbow/percorsi ortogonali con angoli arrotondati, qualificando lunghezza, numero di svolte, uscita/ingresso sul lato giusto, attraversamento delle forme, disposizione dell'etichetta e limite del canvas. Una forma che si avvicina a un'altra può rendere sensato passare da `right→left` a `right→top` senza cambiare i nodi collegati. Questo è un piccolo selettore di percorsi, **non** un motore universale di graph-layout: relazioni sovrapposte o scene molto dense possono richiedere azione esplicita.

3. **Etichetta percepibile e indipendente.** Il testo è posto in un badge SVG contrastato che cerca un'area esterna alle forme, può avvolgere un testo lungo su più righe e può essere trascinato indipendentemente: gli offset restano dati `labelDx`/`labelDy`, conservati nel file. Un'etichetta che finisce dietro un riquadro non è riparata da `z-index` indiscriminato: prima cambia la scelta del posto rispetto alla relazione.

4. **Drag dal centro con effetti distinti.** Con entrambi gli estremi liberi, muove insieme i punti; con uno solo libero, muove quel punto; con entrambi agganciati, modifica un percorso di curva manuale mediante `control` conservando `from`/`to`. Il drag dell'estremità cambia il nodo di attacco o lascia un punto libero. L'interfaccia espone le modalità `Automatico`, `Dritto`, `Ad angoli morbidi`, `Curva manuale`, e un `Ripristina percorso` che libera le preferenze visive senza cancellare gli ID dei referenti.

5. **Continuità del gesto e del file.** Il target percettivo della linea selezionata mantiene l'hit path, il centro e due endpoint indipendenti; il badge resta una superficie di intervento distinta. Le modifiche di label e percorso sono atomiche per undo; il formato documentale resta `ccm.document.v1`, aggiungendo proprietà opzionali alla relazione e lasciando leggibili le forme precedenti. Una curva salvata precedentemente conserva la sua identità visiva salvo ripristino esplicito.

### Prove e limiti

Controllo sintattico JavaScript con Node, Playwright/Chromium via `set_content`: sei configurazioni spaziali (allineata, sfalsata, ostacolo aggiuntivo, verticale, invertita, quasi a contatto), dodici frecce in totale senza attraversare l'interno dei riquadri e senza collisioni fra badge ed elementi nelle configurazioni scelte; drag dal centro e salvataggio/riapertura con `from/to` immutati e `control` disponibile; drag etichetta con offset conservati; scelta e ripristino di percorso; testo lungo a più righe; contrasto di badge nel tema Grafite; esportazione pubblica senza gli appunti privati. Una scena sintetica con venti riquadri e quaranta collegamenti ha renderizzato senza errori JavaScript nel test di carico iniziale; questo non dimostra framerate o scala illimitata.

**Limiti del giudizio:** lo screenshot è un'osservazione dell'operatore sulla vecchia versione; non prova che abbia utilizzato Studio 06. I test browser sono headless e non attestano apertura `file://` in Chrome/Edge dell'operatore, gesto touch reale, comprensione dell'interlocutore, PDF finale, pubblicazione, installazione o assimilazione in un caso non identico. La nuova UI contiene ancora il file esempio neutro, non le modifiche locali dell'utente allo Studio 05 sul suo computer.

**Apprendimento per il seguito:** in un diagramma collaborativo il significato sopravvive alla trasformazione della geometria. Rafforzare la freccia significa permettere di correggere separatamente referente/relazione, ancoraggio/percorso e posizione della descrizione; ricalcolare l'espressione dove il contesto cambia senza inventare un nuovo significato. La differenza torna a questa competenza K-UX-AI; Design/Source-Grounded Infographic e Interaction Quality restano i metodi complementari per grammatica spaziale, focus e comprensione, senza duplicare le rispettive fonti.


## 12 novembre 2026 — Studio 05: lo spazio di lavoro non è lo schermo del pannello

**Selezione dell'operatore:** prima di rigenerare Studio 04 dopo un download non riuscito, è stata richiesta una revisione UX fondata sul file e su viewport reali. La revisione ha esposto perdita di leggibilità su telefono, sovrapposizione del dock con contenuti e appunti, finestre contestuali troppo alte e un'etichetta di salvataggio che attribuiva un esito non osservato. L'operatore ha autorizzato di procedere con la correzione e di richiamarlo quando serva la sua valutazione.

**Risultante locale nel ricevente ChatGPT:** `MAIOS_Comunicazione_Collaborativa_Studio05.html` (114.556 byte, SHA-256 `5e496e0031de67670fdedc308781847c3a8503b90890b369f805be405e4082c4`), più archivio ZIP alternativo verificato byte-per-byte. Non sono stati modificati `src/`, pubblicazione, release o installazione K-UX-AI.

### Sapere che deve cambiare il prossimo editor

**Occlusione reale e adattamento:** un pannello fisso a destra può lasciare il canvas sotto di sé anche quando il pannello è dichiarato «laterale». Il calcolo CSS dell'inset deve risolversi in uno scope che dispone davvero della variabile `--dock-width`: un alias definito prematuramente in `:root` con `var(--dock-width)` inesistente nel suo scope ha prodotto valore non valido e padding computato di `0px`. Spostare l'alias su `body` ha reso operante la riserva. Verificare nel render **rect del canvas e rect del pannello**, non solamente il nome della classe. Dock destro/sinistro su desktop non copre più il documento; sopra/sotto riserva un campo; mobile usa un pannello esplicito a piena larghezza con ritorno/focus e backdrop, senza tentare di conservare contemporaneamente due spazi illeggibili.

**Stesso documento, due proiezioni raggiungibili:** su schermi stretti la vista spaziale 16:9 comprime testo e note sotto soglia leggibile. Lo stesso modello `ccm.document.v1` forma allora una vista di lettura a 17px su 390px, con contenuti, relazioni etichettate e possibilità di richiamare il mini editor del referente; una vista spaziale rimane disponibile con scroll/zoom, non un secondo documento. La vista lineare conserva i nodi anche quando geometria e ruolo visivo cambiano. Un pannello/modalità non trasferisce significato o stato aziendale.

**Mini editor contestuale:** la finestra già mobile e ridimensionabile diventa compatta soltanto se i campi di uso meno frequente sono subordinati a una disclosure (stile, forma, colore, approfondimento). Togliere il solo `height:480px` non bastava: l'altezza naturale superava ancora 490px. Con proprietà secondarie collassate l'editor osservato è alto circa 386px e mantiene le sue funzioni. La geometria manuale resta una scelta dell'operatore e il comando di ritorno vicino al referente rimane disponibile.

**Perdita nella copia pubblica:** eliminare note e libreria dal JSON non è sufficiente se il renderer ha anche creato una **seconda proiezione testuale** (`#readingView`). La prima esportazione Studio 05 manteneva lì gli appunti privati come HTML statico: il test di ricerca del testo sensibile nel file esportato l'ha rilevato. Il nuovo export svuota anche quella regione, come gli altri output runtime, prima di serializzare e riapre la copia in lettura senza strumenti né note. Il metodo generale è `private domain data != every DOM projection`: ogni nuova proiezione modifica la copertura del controllo di condivisione. Non chiamare una copia pubblica protetta: il codice HTML resta ispezionabile.

**Salvataggio osservabile:** `a.click()` su un Blob richiede un download al browser; non fornisce ricevuta del salvataggio a disco. Non scrivere «copia salvata» né azzerare lo stato modificato su quel solo gesto. Esporre «download richiesto» e invitare alla verifica del file; nel test harness Playwright è stato ricevuto un file via `expect_download` e riaperto con i dati modificati. Questa prova non dimostra consegna del collegamento sandbox nell'interfaccia dell'operatore.

**Troncamento testuale:** un avviso vicino al nodo segnala `scrollHeight > clientHeight`; non abbassare i font fino a nascondere il problema. La vista di lettura rende disponibili i testi completi, e l'operatore può ridimensionare o correggere il riquadro. La nota iniziale dell'esempio è stata spostata e ampliata nel canvas perché il testo era effettivamente tagliato. La vista PDF può avere altre necessità e rimane prova separata.

### Osservazioni tecniche e limiti

**45/45 controlli Playwright/Chromium locali**: 35 su dock non occlusivi, lettura, zoom, mini editor, data roundtrip, privacy e modalità pubblica/mobile; 10 su temi, frecce trascinabili dal centro, preparazione print senza note, avviso overflow, editing nella vista mobile e assenza di errori pagina. Le prime quattro anomalie della suite principale sono state corrette e riprovate: padding dock non risolto, altezza editor naturale, seconda proiezione privata non eliminata. L'HTML non carica librerie esterne e resta ampiamente sotto il budget dei 2 MB.

**Non esercitati:** apertura tramite `file://` nel browser dell'operatore (il runner Chromium restituisce `ERR_BLOCKED_BY_ADMINISTRATOR`), touch su dispositivo fisico, qualità del PDF finale, riuscita del download via interfaccia ChatGPT, esperienza comunicativa di una persona reale, assimilazione in un altro dominio. Il primo riscontro del destinatario cambia il successivo lavoro senza riscrivere le prove già svolte.

## 11 novembre 2026 — Studio 04: mini editor mobili e tema sull'intero ambiente

**Fonte:** l'operatore distingue il salvataggio completo dalla «Copia pubblica» e seleziona due cambiamenti del mezzo: gli editor contestuali devono essere riposizionabili e ridimensionabili, in analogia alle finestre chat già conosciute, senza caricare un framework esterno; la scelta di uno dei quattro temi deve interessare anche l'interfaccia esterna alla scheda.

**Metodo esercitato nel codice locale:** `MAIOS_Comunicazione_Collaborativa_Studio04.html` estende Studio 03 con CSS nativo `resize:both` e drag `pointerdown/move/up` sulla testata del mini editor, evitando il re-render della superficie di lavoro per ogni pixel di movimento. Il primo ingresso resta ancorato all'oggetto; dopo una modifica manuale la posizione e la geometria restano nell'UI state `state.ui.quickWindow`, vengono limitate alle dimensioni del viewport e conservate nel download HTML. Il pulsante «↩ Vicino» restituisce la finestra all'ancora dell'oggetto. Un resize manuale è distinto dal drag della testata e dalla selezione dentro un controllo. Elementi diversi possono riusare la stessa geometria; l'identità dell'elemento continua a essere quella del documento, non della finestra.

**Tema coerente:** `state.theme` viene proiettato anche su `body[data-theme]` con variabili CSS e palette per Carta, Perla, Oceano e Grafite. Toolbar, sfondo esterno, pannelli, pulsanti, campi, avvisi, mini editor e dialoghi partecipano allo stesso tema; la scheda mantiene la propria proiezione. Colori degli elementi già personalizzati restano attributi del contenuto, non vengono sovrascritti solo perché cambia il tema generale. La stampa continua su superficie bianca e le note private mantengono la propria disciplina di esportazione.

**Qualificazione della copia pubblica:** esporta una copia di comunicazione senza appunti e libreria; non è una protezione da lettura del sorgente, un canale autenticato o una sincronizzazione con il file di lavoro. Contenuti pubblicabili già visibili e approfondimenti vanno verificati da chi invia.

**Prove:** HTML locale autonomo, 101.419 byte (SHA-256 `579c7f2ee7891b34eb60b7ef3e749ebe8cd373a71d3b76acbda70014f3c25a32`), nessuna dipendenza software esterna. Chromium Playwright via `set_content`: colori effettivi di body/header/pannello differenziati sui quattro temi; mini editor editabile, trascinabile, ridimensionabile, con geometria stabile durante modifica e riuso su altro oggetto; reset all'ancora; export/import HTML con posizione/dimensione conservate; copia pubblica senza testo degli appunti; controllo viewport mobile a 390 px. Tutti i 16 scenari principali di regressione Studio 03 restano verdi, zero errori JavaScript pagina negli scenari osservati. L'ambiente ha bloccato la navigazione `file://`, quindi l'apertura diretta da disco e l'uso fisico touch restano da verificare. Non si trasferisce questa prova al runtime pubblico K-UX-AI.

**Apprendimento:** la personalizzazione dell'editor è stato UI situato e trasferibile nello stesso file, distinto dalla semantica del documento; lo schema cromatico della scheda e il tema dell'ambiente sono proiezioni coordinate dello stesso tema, mantenendo possibili colori specifici degli oggetti. Se il pannello è ricostruito da un cambio di elemento, il layout scelto dall'operatore continua; un comando esplicito lo riporta al referente. Il lavoro successivo deve osservare utilità reale e comportamento dei browser dell'operatore.

## 11 novembre 2026 — Studio 03: mini editor, magnetismo e continuità tra DOM e documento

**Mandato diretto dell'operatore:** la superficie di lavoro resta il risultato, l'editor generale appare solo da Strumenti e l'intervento locale emerge vicino all'oggetto. Il successivo HTML locale `MAIOS_Comunicazione_Collaborativa_Studio03.html` incarna questo principio con pannello a destra/sinistra/alto/basso/flottante, mini editor per oggetti, schede e frecce, magnetismo, allineamenti visibili, forme, livelli, appunti spostabili e approfondimenti.

**Evidenza del prototipo locale:** 92.537 byte, SHA-256 `f00442c79ada3433a05f417c046af5d0f4fbfbdc81bed15298037416f869ebd6`. È stato prodotto e consegnato nella conversazione come singolo file HTML offline, senza dipendenze esterne; **non** installato nel runtime, non pubblicato sul sito e non copiato nella repository. 16/16 scenari principali e 6/6 prove ulteriori eseguiti in Playwright/Chromium tramite `set_content`, zero errori JavaScript di pagina negli scenari principali. Includono editor testo/frecce, selezione senza inspector, dock in cinque modalità, note private, snap da x≈448 a x=457 con guida visibile, triplo clic su livelli sovrapposti, attacco di freccia a metà lato (da 362,394 a 457,394), drag centrale, salvataggio-riapertura, dettaglio live e pagina PDF aggiuntiva preparata, copia pubblica e resa a 390 px. Il browser non ha permesso di validare direttamente `file://`; touch fisico, export PDF finale, efficacia comunicativa reale e assimilazione in un nuovo caso restano aperti.

**Differenze riusabili nel metodo del medium:**

1. `selection != edit intent`. Un clic seleziona e conserva il nodo; un doppio clic forma un editor locale, un triplo clic può scegliere il livello sotto la sovrapposizione. L'editor generale non entra da ogni selezione; la sua apertura ha un controller esplicito. L'alternativa Livelli + Enter rende raggiungibile lo stesso oggetto senza imporre gesto multiplo a touch o tastiera.
2. `drag source != click target` in un SVG. Un primo prototipo perdeva il doppio clic al centro della freccia: il pointerup del primo click ricreava il suo hit target e, quando gli handle coincidevano, quello di estremità copriva il centro. Il nuovo esercizio privilegia nodi significativi per le frecce predefinite, preserva il target durante semplici click, usa la sequenza pointerup per identificare la modifica della freccia e porta l'handle centrale al livello interattivo utile. `drag center` modifica la curvatura se l'estremo è agganciato; `drag endpoint` modifica il riferimento al nodo, o lo lascia libero. La linea grafica conserva il significato attribuito alla relazione, senza dedurlo dalla forma.
3. Lo snap è **una proposta di geometria osservabile**, non una mutazione semantica: mostra guide temporanee e aggancia vicino a bordi/centri di altri elementi o del canvas; la selezione, gli ID e i legami restano invariati. L'attacco automatico di una freccia calcola il punto di metà lato pertinente alla posizione relativa dei nodi; un override esplicito del lato è disponibile nell'editor avanzato.
4. **Appunti come elementi privati del lavoro.** Le note della vecchia scheda vengono migrate in un oggetto `note` trascinabile, senza duplicazione dopo il successivo export. La vista pubblica e i fogli di stampa li escludono; l'HTML di lavoro li conserva. Gli approfondimenti sono diversi dalle note: si aprono in presentazione e possono avere una pagina di stampa dedicata.
5. **La copia pubblica deve pulire dati canonici e proiezione temporanea.** La sola rimozione delle note dal JSON incorporato non basta: `cloneNode(documentElement)` include il DOM già renderizzato (appunti, libreria, editor, schede di stampa). Prima del download, azzerare le regioni del runtime in cui tali contenuti erano proiettati e ripartire dal JSON intenzionalmente condivisibile. È stato verificato con ricerca dell'effettivo testo degli appunti nel sorgente HTML pubblico, non solo controllando lo stato JSON. La copia pubblica continua a esporre i contenuti delle schede, da verificare nel loro significato prima di inviare.
6. Le sezioni con `containerId` mantengono legame con gli elementi durante spostamento. La duplicazione delle schede deve rimappare sia gli ID delle frecce sia i `containerId` dei figli; un auto-layout interno può riordinare dopo il rilascio senza cancellare la possibilità di disposizione libera.

**Prossimo uso:** aprire il file effettivo nel browser dell'operatore, comporre un caso comunicativo reale, correggere dall'uso le dimensioni, i gesti e l'orientamento, poi trasferire soltanto la parte realmente generalizzata alla forma pubblica K-UX-AI. La prova test harness non sostituisce il riscontro umano né la successiva assimilazione della competenza.

## 11 novembre 2026 — Studio 02: superficie libera, strumenti situati e diagrammi manipolabili

**Movimento selezionato dall'operatore:** fare del risultato visibile la superficie primaria. Il pannello con elementi, layout, temi, schede e libreria emerge dalla rotellina a destra; le proprietà dell'elemento emergono dalla sua selezione. Il primo HTML tecnico è stato quindi affinato nel file locale `MAIOS_Comunicazione_Collaborativa_Studio02.html` (66.438 byte; SHA-256 `1023ca424ead3b10d49541d895ee2ba6af006e32ba27aa8781cf914970fa085c`). È un artefatto consegnato nella conversazione, non un file installato nel repository o una release del prodotto.

**Semantica dei gesti da preservare:**
- clic: riconoscere il referente e raggiungerne l'editor contestuale;
- doppio clic: modificare il testo e raggiungere il relativo font;
- triplo clic: se nello stesso punto vi è una sovrapposizione, selezionare il livello sottostante; altrimenti raggiungere le proprietà visive, per esempio il colore di sfondo;
- un elenco Livelli richiamabile fornisce una via esplicita equivalente per chi non usa i clic multipli, in particolare su touch e tastiera.

**Distinzione tecnica appresa:** il triplo clic non è un evento universale o un solo significato. Il doppio clic può già avere avviato un edit `contenteditable`. La sequenza deve conservare ID dell'oggetto, luogo e intervallo dei gesti, senza ricreare il nodo fra secondo e terzo clic; se compare un terzo clic su elementi sovrapposti deve uscire dall'editing del primo e selezionare quello sottostante. Quando un oggetto è soltanto selezionato, il DOM deve restare lo stesso: re-renderarlo ad ogni rilascio interrompe la sequenza. I contesti e i controlli alternativi restano pertinenti; un numero di clic non sostituisce la selezione esplicita di un livello.

**Diagrammi:** la freccia è un elemento con identità propria, significato, spessore, colore, tratto, curva e orientamento. Gli estremi possono riferirsi a due nodi o a coordinate libere. Il trascinamento di un estremo produce un nuovo riferimento a un nodo solo se il rilascio ha realmente individuato quel nodo; il tratto nello spazio resta libero, senza inventare una relazione. Selezione, editor della freccia, estremi trascinabili e scelta numerica/testuale delle destinazioni sono due mezzi per modificare lo stesso stato. Un collegamento visivo non certifica un rapporto causale; il campo semantico resta nel dato `label`.

**Qualità del gesto e del livello:** i piccoli handle degli estremi erano sotto i riquadri a causa del livello grafico. Il livello SVG deve andare in primo piano *solo durante la modifica di una freccia selezionata*, senza coprire gli oggetti quando la freccia non è attiva. Nella prima revisione della nuova superficie, il canvas persistente riceveva più `addEventListener` ad ogni redraw, generando duplicati nei drop da catalogo. La correzione utilizza handler sostituibili (`onpointerdown`, `ondragover`, `ondrop`) e li elimina in vista Presenta; il conteggio del drop torna esattamente a uno per gesto. Per la resa SVG occorre verificare anche lo stile **computed**, perché una regola CSS può prevalere sugli attributi SVG di spessore e colore.

**Layout e temi:** le sezioni hanno una propria identità e possono essere riordinate, trascinate e ridimensionate. Un elemento dentro una sezione conserva `containerId`; quando la sezione si sposta, i suoi elementi si spostano con essa mentre l'ordine e le relazioni restano leggibili. Due temi chiari e due scuri cambiano la proiezione; il default di testo e freccia va compensato in scuro per non perdere contrasto, senza riscrivere il valore semantico dell'oggetto per ogni cambio di tema. Una palette rapida e preset di layout possono accelerare la costruzione senza delimitare le nuove forme.

**Portabilità e dimensione:** file HTML unico, nessuna dipendenza esterna, stato JSON incorporato. Immagini importate vengono ridotte e codificate nel file; import ed export stimano un budget inferiore a 2 MB e rifiutano un aumento che lo oltrepasserebbe. Il limite è una scelta di consegna per questo prototipo, non una regola generale di K-UX-AI. Restano distinti copia salvata, copia pubblica senza note/libreria, rappresentazione presentata, esportazione JSON per un LLM e presenza di un reale servizio AI.

**Evidenza locale:** 11/11 scenari Playwright in Chromium per pannelli, clic singolo/doppio/triplo, selezione del livello sottostante, frecce collegate e libere, proprietà, layout drag-and-drop, temi, salvataggio e riapertura HTML, copia pubblica, Presenta e viewport da 390 px. Verifiche aggiuntive: una sezione che sposta effettivamente il suo contenuto, immagine compressa incorporata e ripristinata, tre fogli preparati per la stampa, zero errori pagina nei percorsi osservati. Browser tramite `set_content` del documento; apertura diretta `file://` non esercitata per restrizioni del ricevente, PDF finale e uso umano touch/desktop non ancora verificati. I test appartengono a questo HTML locale e non si trasferiscono al runtime K-UX-AI.

**Ritorno al sapere operativo:** la percezione dell'operatore e la struttura del documento sono due proiezioni dello stesso oggetto; i pannelli sono richiami situati e non il contenuto del lavoro. L'identità del referente deve continuare tra selezione, edit, sovrapposizione, relazione diagrammatica, disposizione, presentazione ed export. Il prossimo caso deve prima osservare se questi gesti permettono realmente all'operatore di comunicare meglio, non solo se i test passano.


## 11 novembre 2026 — primo esercizio del medium HTML neutro

**Fonte dell'oggetto:** richiesta dell'operatore di provare che cosa si possa fare con una pagina HTML dopo la formazione della competenza. È stato costruito nella chat un prototipo locale autonomo `MAIOS_Comunicazione_Collaborativa_Prototipo.html`, senza contenuti Schnell e senza dipendenze esterne (SHA-256 `f7d7761ef5876c85a47309b882b593c1a91c7cc4c37c1893d20e8c4df49b59c7`; 42.639 byte). Non è stato aggiunto al repository o distribuito nel runtime.

**Esercizio osservato in Chromium tramite Playwright con contenuto caricato direttamente nel test harness**: tre schede con dati JSON incorporati e IDs stabili; modifica testuale nell'ispettore e direttamente nell'oggetto; aggiunta e duplicazione di nodi e relazioni etichettate; trascinamento e ridimensionamento; undo della geometria; aggiunta/duplicazione/eliminazione di schede; immagini incorporate e salvate nella libreria; export HTML con riapertura e recupero di oggetti, note, libreria e immagini; esportazione di una copia con note e libreria eliminate; modalità Presenta e navigazione da tastiera; struttura e strumenti raggiungibili con viewport mobile; composizione di tre fogli per la stampa; export dati JSON. Tre suite locali sono passate senza errori JavaScript di pagina nei percorsi osservati. I test non provano comprensione umana, comportamento diretto su `file://` in tutti i browser, stampa PDF finale, touch reale, sincronizzazione o connessione LLM.

**Apprendimento riusabile emerso da un difetto nella prima costruzione:** il click per selezionare un oggetto e il doppio clic per editarlo partecipano allo **stesso gesto in continuità**. Se il componente viene ricreato a ogni `pointerup`, anche quando non vi è stato movimento, il secondo click non raggiunge lo stesso nodo DOM: il doppio clic smette di funzionare. La correzione locale mantiene vivo l'oggetto quando l'interazione è una semplice selezione; il resize handle viene aggiunto allo stesso nodo; solo una trasformazione effettiva conclude il gesto in stato persistito e render. Questo cambia il prossimo editor in cui selezione, trascinamento ed editing coesistono; non si risolve con un pulsante supplementare o con un ritardo artificiale.

**Rilettura semantica:** il file esportato conserva un modello JSON strutturato oltre all'apparenza delle schede. L'HTML è un carrier autoportante; il modello documentale è il canale con cui un altro LLM può comprendere ID, testi e relazioni dopo il trasferimento. Il trasferimento del file non attiva un agente, non trasferisce autorità e non equivale all'assimilazione della competenza. Per un destinatario esterno una proiezione pubblica può eliminare le note e gli elementi della libreria senza eliminare i contenuti visibili delle schede: il campo *inserito nella presentazione* richiede comunque controllo dell'operatore.

**Stato del learning:** risultato esercitato nel ricevente ChatGPT in modo locale e attribuito, conoscenza conservata nell'owner K-UX-AI; assimilazione nel successivo caso non identico ancora da osservare. La sorgente pubblica non contiene il prototipo e la versione del prodotto non cambia.

## Sapere acquisito dal primo HTML

Il file MAIOS_Schnell_Presentazione_modificata(1).html, fornito dall'operatore nella conversazione dell'11 novembre, rende già possibile:

- intervenire direttamente sui campi marcati `contenteditable` e sui testi degli appunti;
- navigare sei schede (introduzione più cinque) con barra laterale, controlli e tastiera;
- passare alla modalità Presenta e uscirne con un controllo visibile;
- esportare con Blob e download un HTML che incorpora le modifiche testuali DOM;
- stampare o generare PDF tramite la funzione di stampa del browser;
- distribuire manualmente quel file come allegato o copia su un altro dispositivo.

L'operatore giudica utile poter modificare e salvare negli ultimi minuti prima dell'incontro. Il codice disponibile mostra le funzioni, ma non dimostra ancora il comportamento di un editor generalizzato su dispositivi/browser differenti.

**Differenza concreta:** l'HTML è contemporaneamente luogo di lavoro, rappresentazione per il pubblico e pacchetto trasferibile. L'evoluzione non deve sacrificare una di queste funzioni per arricchire le altre.

## Problemi resi visibili nel primo caso

- Campi e forme non hanno tutti una proprietà modificabile: alcuni titoli di sezione e metadati sono testo fisso del markup.
- La struttura delle schede e dei diagrammi è scritta nel DOM; non vi sono comandi per aggiungere/eliminare/duplicare elementi, collegarli o modificarne liberamente disposizione e relazioni.
- La funzione di export clona il documento HTML corrente, ma non definisce una identità strutturata di elementi e relazioni né una storia di revisioni.
- Il download non aggiorna automaticamente il file originale, le copie già inviate o gli altri dispositivi.
- In modalità Presenta gli appunti scompaiono anche per il relatore: la vista pubblica e quella privata potrebbero richiedere superfici diverse.
- Un altro LLM può leggere il file, ma senza identificatori semantici espliciti deve ricostruire dal DOM il rapporto fra testo, forma, posizione e significato.

Queste mancanze sono **possibilità di sviluppo** da verificare sull'uso, non difetti universali del file precedente.

## Prima architettura possibile, aperta alle conseguenze

Un artefatto autonomo può portare un **documento semantico incorporato** e proiettarlo in un DOM/SVG modificabile. Separare almeno, quando materialmente rilevante:

```text
identità e versione dell'artefatto
oggetto / intenti / sorgenti attribuite
scene, schede o sezioni
elementi con ID stabili e contenuto modificabile
relazioni con significato distinto dalla freccia grafica
proiezione/layout/stile e modalità di lettura
note del relatore e dettagli da condividere o non condividere
revisioni e differenze dove servono davvero
asset incorporati o dipendenze dichiarate
```

È un **modello candidato**, non schema canonico imposto a ogni lavoro. Scegliere DOM, SVG, Canvas o composizioni secondo l'oggetto. Un diagramma visuale può avere un percorso testuale equivalente; i connettori devono seguire gli elementi durante il trascinamento e il resize. I layout responsivi possono cambiare forma preservando soggetto e relazioni.

Per il salvataggio di base conservare **HTML autonomo esportabile e riapribile**. Verificare che dati, elementi aggiunti, diagrammi, note e asset utili siano recuperati dal file appena scaricato. Le API di scrittura diretta sul filesystem e lo storage del browser possono essere miglioramenti opzionali; non sostituiscono la portabilità della copia.

Il ciclo collaborativo candidato:

```text
persona modifica il lavoro e conserva una revisione
→ artefatto trasferito al ricevente AI con la sua identità
→ AI legge sorgente, contenuti, relazioni e variazioni
→ comprensione, nuove domande, proposta o modifica attribuita
→ nuovo HTML / differenza presentata alla persona
→ persona esercita, presenta, condivide, risponde
→ conseguenza reale cambia artefatto e, quando riusabile, competenza
```

Non inventare sincronizzazione, consenso, interpretazioni semantiche o effetto esterno a partire dal solo scambio di file.

## Economia del gesto

La semplicità riuscita del primo caso è una qualità da preservare. L'uso quotidiano deve poter restare vicino a:

`Apri → Modifica → Salva HTML → Presenta / Condividi`.

Gli strumenti di composizione avanzata possono emergere in una barra laterale a scomparsa e in proprietà dell'elemento selezionato. Una libreria di elementi può conservare testo, figura, diagramma o composizioni formate dall'operatore, senza rinchiuderne il saper fare in preset fissi.

Distinguere sempre ciò che un pulsante promette da ciò che esercita. Un selettore di elemento non applica automaticamente una trasformazione di significato. Annulla/ripristina deve preservare sia stato sia referente/sele­zione; copia HTML e condivisione devono esplicitare il documento realmente consegnato.

## Contesti diversi, stesso nucleo

- **Presentazione:** sequenza leggibile, profondità e note del relatore.
- **Content web:** stessa relazione come contenuto di pagina, con struttura e responsabilità editoriali del sito ricevente.
- **Progetto/prodotto:** oggetti, decisioni, dipendenze e alternative comunicabili, senza scambiare un mockup per un requisito approvato.
- **Sistemi complessi:** mappe, dati, stati e conseguenze con sorgenti e relazioni distinguibili, senza inventare stato operativo.

L'oggetto e il dominio determinano forma, destinatario ed effetti. Non assumere che tutto debba essere organizzato in slide o che ogni diagramma richieda uno schema rigido.

## Primo esercizio successivo che può insegnare

Partire dall'HTML Schnell come evidenza privata, formare un **artefatto neutro autosufficiente** che conservi funzionanti editing, salvataggio e presentazione e introduca almeno un tipo di elemento/relazione realmente modificabile. Verificare in browser il percorso completo: modifica → export → riapertura → stessa struttura → navigazione/presentazione; recupero da tastiera e su viewport stretto. Solo dopo osservare se pannelli, drag, libreria o collegamento AI aprono nuove possibilità senza appesantire l'uso.

La prova deve riguardare il file esatto e il ricevente usato. Conservare nella guida i meccanismi riusabili, nel CURRENT l'evidenza e il seguito, nella competenza generale K-UX-AI soltanto ciò che cambia più casi.
