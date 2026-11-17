# MetaEditor Lab 04 — gesti su più elementi

**17 novembre 2026 — stato:** esempio HTML autonomo sperimentale di K-UX-AI, derivato da Lab 03. Non sostituisce MetaCanvas Studio 20/21 e non modifica MAIOS.it o D-ND.com.

[Apri l'editor Lab 04](MetaEditor_Lab04_Manipolazione.html). Tutto il documento è un modello neutro; non importa ancora HTML arbitrario di altri siti.

## Il gesto da provare

1. Fai clic su un titolo o un riquadro, poi tieni premuto **Maiusc** e fai clic su un altro elemento, anche da una sezione differente. Entrambi devono restare evidenziati. Maiusc+clic su un elemento già incluso lo rimuove dalla selezione.
2. Usa **Copia**, **Taglia**, **Incolla qui** nel pannello Elementi (appunti interni, non clipboard Windows). Dopo la copia seleziona una sezione e clicca Incolla qui, oppure seleziona l'oggetto dopo il quale inserire.
3. Con più elementi selezionati usa **Duplica tutti**, **Elimina tutti** o **Sposta gli elementi insieme in sezione** nell'editor contestuale. Ogni trasformazione multipla deve essere annullabile con un solo Undo.
4. Da tastiera, senza focus in un input o testo in modifica: `Ctrl+C`, `Ctrl+X`, `Ctrl+V`, `Ctrl+D`, `Ctrl+A` (soltanto se una sezione è attiva), e Canc. L'editing con doppio clic sul testo e sulle label dei nodi mantiene le proprie scorciatoie ordinarie.

Gli appunti non vengono inseriti nell'HTML esportato e non passano automaticamente ad un'altra scheda/browser. I duplicati ottengono ID nuovi e i diagrammi rigenerano anche gli ID dei nodi preservando i collegamenti nel proprio modello.

## Contratto di interazione

- La selezione collettiva riguarda **elementi della pagina**, non i singoli nodi del diagramma. Se scegli un nodo si attiva il livello del nodo, senza trasformarlo in un blocco della selezione collettiva.
- Un solo stato documento e una sola cronologia, indipendentemente dal numero di elementi.
- Il cambio tema continua a riguardare la visualizzazione, non il testo, i nodi o la raccolta degli oggetti selezionati.
- Non reintrodurre doppi pannelli copia/taglia: la barra di appunti è stabile; l'inspector della selezione collettiva ospita solo i controlli ulteriori di composizione.
- Maiusc+clic non deve creare selezione testuale involontaria. I controlli devono restare usabili con tastiera e a schermo stretto.

## Prove tecniche effettuate

**Node v22 `--check` sullo script** e Chromium headless tramite Playwright `page.set_content`. Percorsi esercitati: selezione di due blocchi con Maiusc+clic, duplicazione con un checkpoint, Annulla e Ripristina, copia dei due blocchi e incolla in seconda sezione, taglio e reinserimento, unicità degli ID dopo la copia, doppio clic sul testo del nodo e salvataggio in situ, persistenza del testo dopo esportazione/nuova apertura, selezione di una seconda vista e 390 px senza overflow orizzontale nel documento di prova. Nessun `pageerror` osservato nei percorsi verificati.

La visualizzazione a 1360 px e a 390 px è stata ispezionata; nel primo rendering la barra degli appunti e l'inspector ripetevano **Copia/Taglia** e occupavano troppo spazio. L'ultima revisione ha mantenuto gli appunti in un'unica barra compatta, lasciando nell'inspector collettivo solo **Duplica tutti / Elimina tutti / Sposta**. La prova browser è stata rieseguita.

**Limiti:** la navigazione diretta `file://` è bloccata nel Chromium del runner (`ERR_BLOCKED_BY_ADMINISTRATOR`). L'apertura sul Chrome Windows dell'operatore e la valutazione di usabilità rimangono da esercitare. `set_content` non prova che l'editor adatti e restituisca senza perdita un sito HTML esistente, né che i due modelli documento/presentazione siano interoperabili. Non attribuire a questa versione il supporto a gruppi persistenti o a selezione di più nodi interni; la selezione multipla riguarda blocchi della pagina e operazioni atomiche su di essi.

## Prossima prova discriminante

Una pagina HTML reale con *regioni editabili dichiarate* + una seconda pagina differente; consentire al Lab04 di selezionare un componente già presente, produrre una patch minima leggibile e applicabile da Codex, verificando che contenuto esterno, CSS, JS e interazioni non siano riscritti. La qualità di selezione e recupero acquisita in Lab04 va mantenuta nel porting.

**Competenze/owner:** [MetaEditor Evolution](../../../competences/ux-ai/collaborative-communication-medium/meta-editor/SKILL.md), [GUIDE](../../../competences/ux-ai/collaborative-communication-medium/meta-editor/GUIDE.md), [CURRENT](../../../competences/ux-ai/collaborative-communication-medium/meta-editor/CURRENT.md). K-UX-AI/CCM custodisce il medium, MetaEditor Evolution il metodo costruttivo; MAIOS.it possiede le proprie pagine e Codex la propria applicazione delle modifiche.
