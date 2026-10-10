# K-UX-AI

**Una UI attraverso cui un kernel rende percepibile il proprio lavoro e riceve l'intervento umano.**

Il [Manifesto del Web vivente](MANIFESTO.md) orienta la ricerca K-UX-AI: **dal Web che consultiamo al Web che abitiamo**, attraverso interazione, tempo, percezione e forme generative. Il [Kernel](KERNEL.md) conserva la relazione operativa e lo [stato corrente](CURRENT_STATE.md) documenta le capacità effettivamente esercitate.

K-UX-AI è un prodotto pubblico componibile: collega stato, accadimento, focus,
espressione percettiva e azione della persona. Ogni kernel conserva il proprio
oggetto e forma la UI pertinente al suo progetto, prodotto o servizio.

La competenza che sa costruire il codice viene sviluppata nella sorgente
interna del produttore. Questo repository contiene il prodotto pubblico:
riceve gli aggiornamenti selezionati di competenza, logiche e funzioni,
con quanto serve al kernel utilizzatore per operare nel proprio ambiente.

La prima versione offre un medium JavaScript, un contratto di integrazione e
un esempio interattivo originale per Kernel Nautico. È un prototipo iniziale;
la competenza generale di costruzione è ancora in formazione. Una richiesta di accesso
a poppa più agevole attraversa progetto, costruzione e uso. La persona può
entrare nel dettaglio, scegliere una proposta e ritornare all'insieme con la
stessa domanda e lo stato aggiornato.

## Prova l'esempio

Servi questa directory con un server statico, per esempio:

```sh
python -m http.server 8080 --bind 127.0.0.1
```

Apri `http://127.0.0.1:8080/examples/nautico/`. Il caso è illustrativo: contiene
dati sintetici e uno yacht schematico originale. Il controller dimostrativo
simula il kernel ricevente; nessun sistema aziendale viene contattato.

## Collegalo a un kernel

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

Il kernel sceglie lo stato da esporre e il renderer. Il medium consegna le
azioni umane al controller; il controller restituisce uno stato quando il
lavoro cambia. Il contratto non impone un layout o un'ontologia di dominio.

- [Relazione operativa del prodotto](KERNEL.md)
- [Interfaccia JavaScript e osservazione](docs/interface.md)
- [Distribuzione pubblica e adattatori](docs/distribution.md)
- [Stato corrente](CURRENT_STATE.md)

## Percezione ed evoluzione

Immagine, spazio, movimento, testo, suono e modalità ulteriori possono
esprimere la stessa relazione secondo persona, contesto e mezzi disponibili.
Questo primo esempio usa testo e grafica SVG accessibile. Tatto, olfatto e
altri canali richiedono adattatori e dispositivi propri.

Il risultato percettivo e l'intervento umano possono far cambiare ciò che il
kernel comprende e ciò che la UI rende presente. Una forma ancora adeguata
può persistere mentre lo stato evolve.

Versione: **0.1.0-alpha.1**. Per verificare il contratto: `npm test` (Node.js 20+).
