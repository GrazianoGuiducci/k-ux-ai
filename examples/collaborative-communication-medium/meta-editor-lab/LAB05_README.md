# MetaEditor Lab 05 — strumenti spaziali dei diagrammi

19 novembre 2026 · **Laboratorio autonomo, non una nuova release Studio 20/21 o un adattatore per siti esterni.**

[Apri l'HTML Lab 05](MetaEditor_Lab05_Diagrammi.html). Il codice deriva da Lab 04, conservandone editing diretto, selezione multipla **di blocchi della pagina**, clipboard interna, gestione delle sezioni, temi, Undo e salvataggio HTML. Non sostituisce quel laboratorio, le pagine MAIOS/D-ND o la presentazione canonica.

## Nuovo gesto

Il livello del **diagramma** ha ora una propria selezione di nodi, distinta dalla selezione dei blocchi:

- **Clic sul nodo**: selezione singola; **Maiusc+clic** su altri nodi *dello stesso diagramma*: selezione multipla. La barra dell'oggetto mostra «N nodi selezionati» e comandi contestuali.
- **Allinea** a sinistra / centro X / destra, alto / centro Y / basso. **Distribuisci** orizzontalmente e verticalmente (da tre nodi in poi). Sono effetti geometrici espliciti; un allineamento può sovrapporre forme che si trovano già sulla stessa seconda coordinata. In quel caso usare Distribuisci o Annulla, senza promettere prevenzione automatica di tutte le collisioni.
- **Trascina la maniglia di un nodo selezionato**: se appartiene a un insieme selezionato, l'insieme si muove con la stessa traslazione; gli altri nodi non vengono alterati e i collegamenti seguono il modello. Anche le frecce tastiera muovono l'insieme con passo 1, o 5 con Maiusc.
- **Duplica / elimina nodi selezionati**: un unico checkpoint Undo. Le copie acquisiscono identificativi propri; i collegamenti interni al sottogruppo sono rimappati. La duplicazione cerca uno spazio libero per l'intero gruppo; se non disponibile, comunica il limite e non forza copie sovrapposte.
- **Doppio clic sullo spazio libero del diagramma**: inserisce un nodo e mette subito il cursore nel suo testo. Se il punto è occupato, prova una posizione libera e lo dichiara. Non richiede un'altra finestra per modificare la scritta.
- **Griglia: ON/OFF**, nel pannello di diagramma o della selezione di nodi: l'aggancio al passo del 5% opera durante il drag e l'inserimento; la preferenza viene salvata nel modello del laboratorio, e il comando non perde la selezione corrente.

Il diagramma aumenta l'altezza quando cresce il numero di nodi. La geometria relativa continua a usare coordinate 0–100 *all'interno del diagramma*; **le sezioni HTML restano griglie responsive**, non diventano canvas assoluti. Questa separazione è essenziale per una futura proiezione su pagine reali.

## Come si è formata la versione

Dal confronto mirato con [Penpot / Layers, snapping e interfaccia](https://help.penpot.dev/user-guide/first-steps/the-interface/), [Figma / Smart selection e allineamento](https://help.figma.com/hc/en-us/articles/360039956914-Adjust-alignment-rotation-position-and-dimensions) e [GrapesJS / Layer Manager](https://grapesjs.com/docs/modules/Layers.html) sono stati assimilati **i principi d'interazione pertinenti**: controllo sull'oggetto selezionato, struttura distinta dalla geometria, disposizione e selezione omogenea. Non è stato importato codice delle UI esterne né presunta una compatibilità automatica con i loro formati.

Un test iniziale di duplicazione di gruppo assegnava una semplice traslazione (+7,+9); i dati erano corretti ma le forme si sovrapponevano, rendendo impossibile selezionare un nodo sottostante. L'ispezione browser ha portato a cercare una traslazione libera per il gruppo e a bloccare la duplicazione se nessuna è disponibile. Una seconda differenza era il doppio clic in uno spazio visivamente occupato: prima creava un nuovo nodo sopra le forme esistenti. Il gesto ora discrimina lo spazio libero e rende esplicita l'eventuale rilocazione. Il laboratorio espande anche il canvas con la densità. La prova dell'azione completa è più importante di una semplice modifica corretta nel JSON.

Un'altra correzione riguarda la cronologia: un'azione di allineamento senza variazioni non deve aggiungere un passaggio fittizio ad Annulla. La trasformazione viene prima simulata su una copia del sottoinsieme, poi impegnata nel modello solo se cambia davvero una coordinata. Il toggle della griglia non disperde la selezione corrente.

## Prove osservate

- **Node v22**: sintassi dello script senza errori.
- **Chromium headless / Playwright `page.set_content`**: Maiusc+clic su due nodi e verifica della selezione, allineamento, Undo esatto, distribuzione su tre nodi, frecce su due nodi, duplicazione e unicità ID, aggiunta e modifica diretta da doppio clic sul canvas, griglia ON persistente, export/riapertura in nuovo browser a 390 px e nessun `pageerror` nei percorsi provati.
- **Seconda prova distinta**: drag con maniglia su due nodi selezionati; entrambi hanno la stessa traslazione, il terzo resta fermo, un Undo ripristina i tre valori originali; eliminazione collettiva e recupero con Undo.
- **Resa**: screenshot desktop e mobile ispezionati dopo la correzione, nessun overflow orizzontale del documento mobile testato. La crescita del canvas consente di mostrare sei nodi senza le collisioni prodotte dall'inserimento e dalla duplicazione del primo tentativo.

Queste sono prove del **laboratorio su documento sintetico** e della sua resa nel browser di test: non certificano l'usabilità dell'operatore sul suo Chrome Windows, touch, accessibilità completa, comportamento su grafi grandi o round-trip di HTML di terzi. Le modalità Pagina/Presentazione rimangono proiezioni limitate del modello `metaeditor.lab.v4` evoluto; **nessuna importazione di pagine MAIOS.it, modifica live, generazione AI, conversione Studio20 `ccm.document.v1` o Codex receiver è stata esercitata**.

## Saper fare e prossimo discrimine

La [competenza MetaEditor Evolution](../../../competences/ux-ai/collaborative-communication-medium/meta-editor/SKILL.md) forma il gesto e si corregge dal rapporto tra intenzione, selezione, layout, risultato visibile e recupero del file. Questo laboratorio **non** introduce una seconda competenza per i diagrammi; conserva il sapere nell'owner specializzato e aggiorna GUIDE/CURRENT. Dopo una prova umana di Lab05, il discrimine ancora aperto resta l'adattatore **a regioni HTML editabili dichiarate e patch selettiva** su due siti diversi, mantenendo intatti gli altri file e le funzioni del sito.
