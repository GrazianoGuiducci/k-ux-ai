# K-UX-AI

**Una UI attraverso cui un kernel rende percepibile il proprio lavoro e riceve l'intervento umano.**

Il [Manifesto del Web vivente](MANIFESTO.md) esprime la direzione di K-UX-AI: **dal Web che consultiamo al Web che abitiamo**. Il [Kernel](KERNEL.md) descrive la relazione operativa; il [repertorio UI](docs/ui-library/CURRENT.md) rende raggiungibili i componenti e gli esercizi del ramo corrente.

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

## Repertorio UI del Kernel — candidato, 8 ottobre 2026

La lane privata [`work/ux-ai-ui-library-20261008`](https://github.com/GrazianoGuiducci/k-ux-ai/tree/work/ux-ai-ui-library-20261008) rende disponibili **sorgenti e contratti completi di interazione** per finestre, avatar, chat, moduli, editor, dashboard e superfici componibili, senza cambiare l'interfaccia `createMedium()`.

- [Rientro corrente della lane](docs/ui-library/CURRENT.md)
- [Catalogo JSON di nove famiglie e sorgenti owner-native](ui-library/catalog.v0.1.json)
- [Contratti di composizione, focus, responsive, motion ed effetti](docs/ui-library/OPERATING_CONTRACT.md)
- [Prove Nautico UI v3: due HTML autonomi](labs/nautico-ui-v3/README.md)

Questo è un **repertorio di fonti e prototipi**, non un'installazione dei componenti THIA/DOMUS né un'integrazione già funzionante nel Site MAIOS. Le sorgenti esterne hanno propri owner, licenze e confini di esecuzione. La versione pubblica del prodotto resta `0.1.0-alpha.1` fino a selezione e qualifica separate.
## Primo modulo UI originale — candidato nel branch privato

Il repertorio include ora una **prima unità eseguibile originale**: [Window Surface](src/ui/window-surface.js) + [Chat/Form](src/ui/chat-form-module.js), con CSS separato e un [esempio integrato al contratto `createMedium()`](examples/window-surface/index.html).

La superficie può passare da avatar a finestra libera, sidebar agganciata e pagina intera; il contenuto Chat/Form si ricompone per **larghezza interna** e mantiene la bozza nelle trasformazioni. Nessuna API THIA o permesso del Lab è incorporato. Consulta [limiti, prove e prossimo movimento](docs/ui-library/CURRENT.md).

### Integrazione corrente: Griglia del fare v4

La lane privata comprende anche il [prototipo HTML v4](labs/nautico-ui-v4/01-griglia-chat-window-surface.html): la Griglia del fare utilizza ora i moduli K-UX-AI `Window Surface` e `Chat/Form` per l'assistente, invece di creare un'ulteriore card-chat locale. Dock e sidebar fanno spazio al canvas; la vista piena e il ritorno conservano bozza, focus e contesto. Il funzionamento esercitato è documentato in [EVIDENCE.json](labs/nautico-ui-v4/EVIDENCE.json).

È ancora una prova **sintetica**, senza AI/Nautico live, Site o release. Il codice principale `createMedium()` e la versione pubblica `0.1.0-alpha.1` restano invariati.

## Percezione ed evoluzione

Immagine, spazio, movimento, testo, suono e modalità ulteriori possono
esprimere la stessa relazione secondo persona, contesto e mezzi disponibili.
Questo primo esempio usa testo e grafica SVG accessibile. Tatto, olfatto e
altri canali richiedono adattatori e dispositivi propri.

Il risultato percettivo e l'intervento umano possono far cambiare ciò che il
kernel comprende e ciò che la UI rende presente. Una forma ancora adeguata
può persistere mentre lo stato evolve.

Versione: **0.1.0-alpha.1**. Per verificare il contratto: `npm test` (Node.js 20+).
