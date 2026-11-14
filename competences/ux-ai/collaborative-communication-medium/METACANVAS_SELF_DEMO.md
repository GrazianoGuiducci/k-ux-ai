# MetaCanvas come guida modificabile

Proposta di lavoro del 14 novembre 2026 per la demo di MetaCanvas e per
la sua presentazione su MAIOS.it. Fonte dei casi osservati: Graziano,
nella conversazione Codex del 14 novembre.

## L'oggetto che passa tra le persone

Una rappresentazione espositiva può diventare anche il luogo in cui si
sistema ciò che si vuole dire. La persona interviene su parole, geometria
e relazioni e può far ripartire il lavoro dalla modifica visibile. Nello
scambio con l'AI, lo stesso documento porta il contesto disponibile nel
testo, negli elementi e nei collegamenti. Al ritorno si possono esaminare
le differenze e far proseguire le parti utili. In presentazione emergono
domande che possono cambiare il diagramma o il lavoro successivo.

L'invariante utile è poter ritrovare a quale lavoro e a quali relazioni
si riferisce il documento attraverso le modifiche e le viste. Due persone
possono usare la stessa rappresentazione per prendere decisioni diverse.
Un quadro per la direzione può mostrare ragioni e decisioni; quello per
il gruppo di lavoro può esporre responsabilità, dipendenze e verifiche.
L'esercizio di comprensione consiste nel vedere se ciascuno sa quale
passaggio gli riguarda e perché.

## Punti di forza e conseguenze

| Capacità | Meccanismo | Conseguenza nel lavoro |
| --- | --- | --- |
| Correzione nel punto in cui emerge | La persona cambia il testo o la relazione sulla vista che sta valutando. | La correzione porta già posizione, gerarchia e rapporto con il resto, riducendo le ricostruzioni tra due giri. |
| Ragionamento visibile | I riquadri rendono individuabili i concetti e le frecce esplicitano dipendenze, contributi o successioni. Etichettare una freccia permette di discuterne il significato. | Si può scoprire che due persone usano la stessa parola per passaggi diversi o che una fase ha un prerequisito ancora aperto. |
| Condivisione a grana utile | Si prepara una scheda per il destinatario. Una selezione concettuale comprende anche le relazioni indispensabili a interpretarla. | Si può spiegare una funzione in una riunione o chiedere un contributo circoscritto senza dover trasferire l'intera storia del progetto. |
| Contributo AI verificabile sul documento | Il ricevente può leggere il modello strutturato, usare le competenze disponibili nel proprio ambiente e restituire una proposta confrontabile. | Una competenza può far emergere un passaggio mancante, distinguere ipotesi e fatti o rendere visibile un'alternativa. Chi lavora sul documento vede dove intervenire e sceglie cosa integrare. |
| Trasporto e ripresa | L'HTML autonomo conserva editor e stato salvato, si apre in un browser compatibile e funziona offline. Il JSON permette di trasferire i dati strutturati. | Una copia passa tra dispositivi e persone e rimane lavorabile. Cambiare formato in futuro ha senso quando preserva la relazione e offre un gesto più adatto al destinatario. |
| Miglioramento del metodo | Una domanda o correzione ricorrente individua una relazione che meritava di apparire prima. Una scheda utile può diventare un modello riutilizzabile. | Un caso chiarisce il lavoro corrente e può cambiare come si preparano i casi successivi. |

In Studio 21 il perimetro di esportazione AI è scheda corrente o intero
documento. Per condividere alcune funzioni di una mappa si prepara prima
una scheda autonoma, con il minimo contesto da cui si capisce il
frammento. Il gesto di estrarre direttamente nodi e relazioni selezionati
è una possibilità da esplorare. Il ritorno JSON o HTML passa dal
confronto delle schede prima dell'integrazione. Vedi il
[contratto del documento](../../../examples/collaborative-communication-medium/DOCUMENT_CONTRACT.md).

## I due usi già emersi

- **Revisione delle pagine MAIOS con Codex.** Graziano corregge copy,
  ordine e relazioni concettuali direttamente sull'anteprima locale della
  pagina. Codex riporta le modifiche nel sorgente del sito dopo il ritorno
  dell'HTML. Graziano riferisce un forte guadagno di produttività. Il caso
  riguarda il metodo di revisione HTML e usa l'editor della pagina, con
  una relazione comune a MetaCanvas. La demo può riprodurre il gesto su
  un esempio pubblico sintetico.
- **Presentazioni MAIOS per aziende con GPT.** Il canvas permette di
  costruire con il modello una rappresentazione dei passaggi di
  adattamento a partire dal contesto aziendale. Presentarla rende
  osservabili disaccordi o lacune che una sequenza di messaggi può
  lasciare impliciti. Nella demo si può usare un caso fittizio in cui la
  direzione vuole capire quale decisione serve e il team tecnico vuole
  capire da quali dati dipende una prova.

## Traccia della demo modificabile

Il primo incontro propone una sola azione: cambiare una parola o una
relazione. Le altre istruzioni compaiono quando serve quel gesto.

| Scheda | Cosa mostra | Gesto da provare |
| --- | --- | --- |
| **Una decisione da chiarire** | Un piccolo diagramma «esigenza → prova → decisione» con una dipendenza ancora da precisare. | Modifica il testo di un riquadro con doppio clic. |
| **La pagina che correggi direttamente** | Una revisione sintetica di una pagina con un titolo e due blocchi da riordinare. | Sposta un blocco e prova Annulla. |
| **La stessa decisione per due interlocutori** | Due schede dello stesso caso con azioni, ragioni e approfondimenti pertinenti al destinatario. | Duplica una scheda, adattala a chi la riceve e prova Presenta. |
| **Invia una sola scheda** | Una vista autonoma del diagramma, con le dipendenze essenziali. | In Dati per AI scegli Solo scheda corrente e leggi il riepilogo dell’esportazione. |
| **Scegli cosa integrare** | Una proposta fittizia rende esplicito un prerequisito per la prova. | Importa il JSON d'esercizio, confronta e integra la scheda proposta. Prova Annulla. |
| **Salva e riprendi** | Copia di lavoro, copia pubblica e riapertura. | Salva l'HTML, riaprilo e verifica di ritrovare la modifica. |

Il JSON di ritorno va preparato come materiale del caso e dichiarato
esempio, così il giro si può esercitare anche offline. Un invio reale a
un assistente resta esercitabile con il proprio ambiente AI. Il confronto
strutturale aiuta a trovare i cambiamenti, mentre le persone giudicano
le affermazioni e il significato delle relazioni.

**Caso di esempio.** Un'azienda vuole ridurre il tempo necessario per
preparare un preventivo. All'inizio il diagramma collega «Richiesta»,
«Prova su preventivi già chiusi» e «Decisione di estendere la prova».
Per la direzione, la scheda mette in evidenza quale decisione prendere
dopo aver visto il risultato. Per il gruppo tecnico, lo stesso diagramma
mostra da dove arrivano i preventivi e chi verifica che siano confrontabili.
Una proposta AI potrebbe inserire un passaggio fra richiesta e prova:
«Selezionare casi comparabili». La persona può cambiare il criterio o
scegliere di mantenere la versione precedente. Il caso fa vedere una
differenza di ragionamento, oltre a mostrare come trascinare riquadri.

## Possibilità da far emergere nei casi d'uso

- **Presentazioni distribuite e comunicazione interna.** Un progetto
  può produrre una vista di sintesi, una mappa per chi coordina e una
  scheda per chi esegue. Se i destinatari rispondono con correzioni
  localizzate, si può capire come far tornare le proposte alla sorgente
  e quali relazioni devono restare riconoscibili quando le viste cambiano.
- **Mappe di progetto, metodologie e passaggio di consegne.** Una scelta
  può portare con sé fonte, ragione, data e domanda ancora aperta. Chi
  riceve il documento può proseguire e riportare una modifica
  attribuibile. Per un documento che rispecchi lo stato di un sistema
  occorre sapere da quale sorgente arriva quel dato e quando è stato
  osservato. L'HTML attuale si scambia come copia salvata. Collegamenti
  ai dati e integrazione tra revisioni sono direzioni da esplorare.
- **Espressione attraverso più media.** Una scheda può fornire la
  struttura per una spiegazione audio o per un video che renda visibile
  il cambiamento nel tempo. Audio e video incorporati potrebbero servire
  in contesti specifici. La scelta dipende da come la persona riceve il
  materiale e da ciò che il mezzo deve rendere comprensibile.
- **Condivisione dal contesto di lavoro.** La UI di Codex o di un altro
  ricevente può tenere il documento accanto al sistema AI. In una
  versione connessa, inviare via email una vista o allegare un file
  richiede una scelta esplicita di destinatario, perimetro e versione.
  Export e rientro rimangono utili anche dove il destinatario usa altri
  strumenti.
- **Apprendimento dal punto in cui ci si blocca.** Se un destinatario
  non riesce a ricostruire una dipendenza, può indicare la freccia o il
  riquadro da cui nasce l'equivoco. La risposta può cambiare sia quella
  scheda sia il modello con cui si spiega un caso simile la prossima volta.

Le edizioni per singoli, aziende e organizzazioni possono combinare
contratti comuni: struttura del caso, azioni esercitabili, modalità di
consegna e ritorno. La grafica deve far riconoscere che cosa si guarda e
che cosa si può cambiare. Una mappa può dare priorità a collegamenti e
stato, una presentazione a sequenza e ritmo, una consegna AI a intento,
fonti e perimetro della proposta. Partire da pochi casi verificabili
permette di vedere dove questa base comune basta e dove serve una forma
diversa.

## Passaggio a MAIOS.it

Nella scheda Strumenti, proposta di primo incontro: «Crea, modifica e
condividi schede, diagrammi e presentazioni che restano lavorabili.
Prova la guida interattiva, poi usa lo stesso documento per lavorare
con altre persone o con il tuo assistente AI».

Con la prossima edizione approvata, la guida modificabile IT/EN diventa
il download dimostrativo principale, con le istruzioni brevi sulla
pagina e due esempi visibili di uso. Consulenza AI può restare come
esempio di applicazione. L'aggiornamento del sito segue la revisione
autoriale delle due anteprime modificabili. Gli HTML pubblicati e i
download diretti vanno collegati alle revisioni esatte del tool.
