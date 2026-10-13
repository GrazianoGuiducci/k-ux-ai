# K-UX-AI

**Una competenza che un LLM usa per rendere il lavoro percepibile e operabile,
costruirne il codice e imparare attraverso il suo uso.**

K-UX-AI è un kernel pubblico di competenza componibile con sistemi agentici
e kernel di dominio. Il suo sapere collega intento, fonti, accadimenti,
focus, espressione e intervento umano. Può formare siti, mappe concettuali,
ambienti interattivi e pannelli di lavoro attraverso i mezzi del ricevente.

Il [Manifesto del Web vivente](MANIFESTO.md) custodisce l'orizzonte:
**dal Web che consultiamo al Web che abitiamo**. Il [Kernel](KERNEL.md)
porta la relazione operativa, la [competenza](competences/ux-ai/COMPETENCE.md)
il metodo e la [guida](competences/ux-ai/GUIDE.md) le ragioni e il saper fare.
Kernel Nautico è riferimento e primo dominio operativo.

## Usarlo nel proprio sistema

Rendi raggiungibile il repository o allega i corpi pertinenti al modello.
Parti da [BOOT.md](BOOT.md) e dal [raccordo LLM](adapters/llm/ENTRY.md),
insieme alla fonte del lavoro. Un core come MPK può comporre K-UX-AI
tra le proprie competenze; un altro harness usa gli stessi metodi con
i suoi strumenti e controller.

La competenza comprende cosa deve diventare possibile, compone le capacità
utili e costruisce una forma originale. Movimento, testo, spazio, immagine
e altri canali partecipano secondo il lavoro. La resa e le conseguenze
possono cambiare la comprensione e il codice. La guida conserva quanto
cambia il prossimo fare.

Il [raccordo all'ambiente](docs/receiving-environment.md) collega metodo
e mezzi effettivi. Il dominio custodisce dati, fonti e significato degli
effetti; il ricevente mantiene contesto e learning propri.

## Sorgenti eseguibili

La versione `0.2.0-alpha.1` include il medium JavaScript, un adattatore
MessagePort, Window Surface e Chat/Form originali. Sono mezzi componibili
e sorgenti da cui continuare la costruzione.

La [Griglia del fare v5.12](examples/griglia/README.md) è l'esempio principale:
la UI interattiva formata con GPT, conservata nella sua sorgente originale.
Attività, card, focus, barra e chat possono ricomporsi mantenendo continuità.

Servi questa directory con un server statico:

```sh
python -m http.server 8080 --bind 127.0.0.1
```

Apri `http://127.0.0.1:8080/examples/griglia/` per usare la v5.12.
Il dimostratore ha fonti e risposte sintetiche locali. Il collegamento a
un LLM e al dominio prosegue dai controller del ricevente.

L'[esercizio tecnico MessagePort](examples/workspace/README.md) resta
raggiungibile a `examples/workspace/`. Il controller sintetico
aggiorna una fonte mentre l'operatore prepara un contributo; oggetto e
bozza continuano attraverso le trasformazioni. Evento, azione e conferma
percorrono un MessageChannel locale. La chat riceve una risposta sintetica.

Il primo [esempio Nautico](examples/nautico/) conserva la domanda di accesso
a poppa attraverso esplorazione e scelta. Gli esempi usano dati sintetici.
Lo [stato corrente](CURRENT_STATE.md) attribuisce sorgenti ed esercizi.

## Collegare il runtime

```js
import { createMedium } from './src/medium.js';

const ui = createMedium({
  state: initialPublicState,
  render: state => renderYourInterface(state),
  onAction: action => yourKernel.receiveHumanAction(action),
});

ui.receive({ id: 'event-001', state: nextPublicState });
ui.dispatch({ type: 'compare', objectId: 'your-object' });
ui.observe(record => yourDevelopmentObserver(record));
```

Il controller decide il risultato del gesto e restituisce lo stato.
Schema di dominio, renderer e trasporto si compongono secondo il ricevente.
Per il contratto eseguibile: `npm test`, Node.js 20+.

- [Interfaccia JavaScript](docs/interface.md)
- [Adattamento e MessagePort](docs/receiving-environment.md)
- [Continuità e apprendimento](docs/continuity.md)
- [Distribuzione](docs/distribution.md)
- [Sorgenti ed evoluzione](docs/source-and-evolution.md)

Il produttore continua la formazione nella propria sorgente e trasferisce
aggiornamenti selezionati a questo prodotto. Il sapere pubblico permette
di comprendere, costruire e continuare nel proprio ambiente.
Versione sorgente: **0.2.0-alpha.1**.
