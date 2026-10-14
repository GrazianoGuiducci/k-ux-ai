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
Kernel Nautico applica questa competenza al lavoro nel cantiere navale.

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

## Presentazione e primo uso

Lo [spazio di lavoro](examples/public-griglia/demo/) permette di conoscere
K-UX-AI e provare le sue funzioni. Presentazione, Composizione, Strumenti,
Interazione e Apprendimento sono gli argomenti del servizio. La Panoramica
prepara le attività; Lavoro in corso apre schede complementari e conserva
focus e bozze mentre cambia ciò che serve vedere.

Le schede hanno funzioni diverse: presentare e guidare, ricevere un contributo,
controllare, esplorare, progettare, organizzare, comunicare, riprendere,
sperimentare, monitorare eventi illustrativi, confrontare testi e dialogare.
Il kernel ospitante fornisce significati e fonti attraverso il proprio profilo.
Nel cantiere, le schede di Kernel Nautico collegano esigenze dell’armatore,
progettazione, costruzione e vita dell’imbarcazione nel lessico del settore.

Servi il repository con un server statico:

```sh
python -m http.server 8080 --bind 127.0.0.1
```

Apri `http://127.0.0.1:8080/examples/public-griglia/demo/`.
Il campo e le schede funzionano localmente. Le domande inviate esplicitamente
usano il servizio pubblico MAIOS del sito configurato; il server statico
semplice non fornisce quel servizio e la UI mostra il collegamento indisponibile.
Le altre bozze restano locali. Dialoghi e proposte si esportano su richiesta;
il trasferimento al kernel ricevente continua il lavoro e il suo apprendimento.

La [guida all’uso delle schede](docs/public-griglia.md) spiega preparazione,
attività, dialogo e continuazione dei contributi. La [documentazione delle
sorgenti](docs/source-and-evolution.md) conserva attribuzioni, costruzione
e riferimenti per chi sviluppa o integra il codice.

La versione `0.2.0-alpha.3` comprende il kernel di competenza, i moduli
JavaScript e questa interfaccia pubblica.
La competenza può costruire altre forme per altre situazioni.

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
Versione sorgente: **0.2.0-alpha.3**.
