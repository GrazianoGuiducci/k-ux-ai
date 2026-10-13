# Adattamento al sistema ospitante

K-UX-AI porta sapere operativo e sorgenti del medium. Il sistema agentico
fornisce il modello, gli strumenti, le sorgenti del dominio e i controller.
Il ricevente li compone con [BOOT.md](../BOOT.md) e la competenza del prodotto.

## Metodo condiviso, mezzi del ricevente

Il [campo di competenza](../competences/ux-ai/COMPETENCE.md) sa comprendere
cosa e come rendere percepibile e operabile. La sua
[guida](../competences/ux-ai/GUIDE.md) conserva ragioni, meccanismi e learning.
Fai partecipare questo sapere mentre formi domanda, scelte e codice.

Il [raccordo LLM](../adapters/llm/ENTRY.md) permette a chat e harness di
raggiungere lo stesso kernel. Un modello può esercitarne il metodo con
contesto e strumenti differenti. Costruzione, esecuzione e osservazione
dipendono dai mezzi presenti: il sapere semantico e il trasporto JavaScript
partecipano a livelli diversi della stessa incarnazione.

## Sistema già governato da un core

Con MPK o un altro core già operante, fai partecipare K-UX-AI attraverso
il suo metodo e il suo ingresso. Conserva contesto, owner e facoltà di
apprendimento/rientro già presenti. Il medium riceve lo stato utile e
restituisce gesti; non duplica il governo del dominio o le autorizzazioni.

## Harness e mezzi differenti

Un coder con filesystem può leggere questo repository, costruire il renderer
e osservare il browser. Un agente con accesso ai file via strumenti può
raggiungere gli stessi corpi e produrre sorgenti o aggiornamenti nel proprio
owner. Una chat che riceve l'archivio può usarne il sapere e preparare il codice
attraverso i mezzi disponibili. La presenza del kernel non installa un browser,
un provider o nuove autorizzazioni nell'host.

Riconosci i mezzi realmente necessari alla costruzione scelta. Risolvi
una mancanza solo quando cambia il risultato; un ambiente differente può
incarnare la stessa relazione con un adattatore più semplice.

## Collegamento diretto

`createMedium({ state, render, onAction })` collega sorgente, UI e controller
nello stesso ambiente JavaScript. Il callback può essere asincrono. Il
controller conferma il proprio risultato con `receive({ id, state })`:
`dispatch` conserva lo stato finché quella conferma non arriva.

`observe` raggiunge azione e snapshot esposti. Un readback AI può comporre
questi dati con provenienza, focus recente e render significativo forniti
dal ricevente; il pacchetto non inventa un modello visivo o una conferma.

## Collegamento MessagePort

`connectMediumPort({ medium, port, onUnknownMessage, onTransportError })` collega un MessagePort
già autorizzato dal ricevente. Può essere un canale verso un Worker, una
applicazione o un adattatore ai mezzi di un agente. Il port è proprietà dell'host;
la disconnessione del collegamento non lo chiude. Un errore di consegna raggiunge
onTransportError: lo stato accettato non viene revocato perché una conferma
non è arrivata al destinatario. Il controller può recuperare con un nuovo readback.

Tutti i messaggi riconosciuti portano `protocol: 'kux.port.v1'`.

| Direzione | Messaggio | Conseguenza |
| --- | --- | --- |
| Host → medium | `{ type:'state', id, state }` | Pubblica lo snapshot con la sua identità; risponde `state-accepted` dopo accettazione. |
| Medium → host | `{ type:'action', sequence, action, state }` | Espone il gesto e il contesto; il controller decide il risultato. |
| Host → medium | `{ type:'snapshot-request', id }` | Riceve `{ type:'snapshot', id, state }`. |
| Medium → host | `{ type:'rejected', id, operation, reason }` | L'operazione non è stata accettata. Il controller può correggere o riprendere. |

`state-accepted` conferma l'accettazione dello snapshot nel medium, non un
effetto aziendale. Una richiesta sconosciuta raggiunge `onUnknownMessage`
senza diventare istruzione o codice eseguito. Identità duplicate o stato
invalido non sovrascrivono il presente accettato. Un renderer può avere
effetti propri: il suo contratto di errore/recovery resta al ricevente.

L'esempio [workspace](../examples/workspace/README.md) esercita realmente
questo canale con un host sintetico locale. Per un agente esterno l'adattatore
host deve tradurre i suoi mezzi nel medesimo confine. HTTP, file o strumenti
MCP sono possibili trasporti del ricevente, da scegliere quando pertinenti;
questo pacchetto non ne dichiara installazioni o controller già presenti.

## Stato e possibilità d'intervento

Lo schema del dominio rimane aperto. Identità, fonte/revisione, contesto,
lifecycle, capacità ed effetti disponibili possono diventare pertinenti
senza formare una tassonomia universale. Non trasformare il nome di una
vista in un permesso o una simulazione in una fonte aziendale.

Geometria e bozze appartengono al ricevente UI. Le azioni esterne e i dati
canonici appartengono ai loro controller. Un host può impostare la retention,
conservare le correzioni e qualificare l'accesso secondo il proprio ambiente.
