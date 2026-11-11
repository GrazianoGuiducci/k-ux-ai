# Collaborative Communication Medium — guida viva

**Owner:** K-UX-AI / collaborative-communication-medium.  
**Stato:** 0.1.0 candidate, 11 novembre 2026.  
**Ingresso:** [SKILL](SKILL.md) → [CURRENT](CURRENT.md) → la sorgente del lavoro e la differenza reale da costruire.

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
