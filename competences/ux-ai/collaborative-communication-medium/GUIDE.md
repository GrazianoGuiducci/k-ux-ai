# Collaborative Communication Medium — guida viva

**Owner:** K-UX-AI / collaborative-communication-medium.  
**Stato:** 0.1.0 candidate, 11 novembre 2026.  
**Ingresso:** [SKILL](SKILL.md) → [CURRENT](CURRENT.md) → la sorgente del lavoro e la differenza reale da costruire.

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
