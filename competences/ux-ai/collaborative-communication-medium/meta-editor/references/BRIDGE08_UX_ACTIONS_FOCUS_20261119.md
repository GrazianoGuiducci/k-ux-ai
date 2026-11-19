# Bridge 08 — accesso contestuale alle capacità esistenti
Data: 19 novembre 2026 · Owner: K-UX-AI / CCM / MetaEditor Evolution  
Stato: due HTML sperimentali creati e verificati in conversazione; sorgente del livello UX e builder hash-guarded disponibili in K-UX-AI; nessun deploy pubblico.

## Intento e campo
Dopo Bridge07, l'operatore seleziona «funzioni utili e migliorare il design della UI per essere più intuitivo». Il problema non è mancanza di un terzo editor: gli editor di bozza Codex e Studio21 hanno ricche capacità ma difficoltà di scoperta e sovrapposizione di pannelli. La competenza ha studiato [Penpot Interface](https://help.penpot.dev/user-guide/first-steps/the-interface/), [GrapesJS Components](https://grapesjs.com/docs/modules/Components) e [Figma Actions](https://help.figma.com/hc/en-us/articles/23570416033943-Use-the-actions-menu-in-Figma-Design) per reperire **gesti di selezione, struttura e ricerca delle azioni**, non per adottare i loro modelli o codice.

Le due sorgenti esatte sono i Bridge07 già verificati:
- Codex HTML: SHA-256 `1ab5e4589953302ddd16b7b98dcd9c3017b7b61db63908a5dc43d93bc24b77f8`
- Studio21 IT: SHA-256 `e709d738531fa1023c404e4bbc8fc3326d3fc6033ca38ee7d391e07867da3a89`

Il [builder K-UX-AI](../../../../examples/collaborative-communication-medium/meta-editor-lab/bridge08_build.py) rifiuta sorgenti con hash differente. [JavaScript](../../../../examples/collaborative-communication-medium/meta-editor-lab/bridge08_ui.js) e [CSS](../../../../examples/collaborative-communication-medium/meta-editor-lab/bridge08_ui.css) sono la nuova capacità trasportabile, separata dal contenuto del sito. Le varianti HTML effettive restano file scaricabili nella conversazione; la bozza del sito non viene committata nel prodotto.

## Cosa cambia nel gesto
- Un **piccolo ingresso Azioni** con ricerca e tasti Ctrl+Maiusc+P (oppure / quando non si sta digitando), frecce, Invio ed Esc. In Codex cerca operazioni/regioni, in Studio cerca operazioni/schede. Il comando chiama l'handler nativo e non duplica la storia né i modelli dati.
- **Riferimento contestuale** all'elemento selezionato e «Modifica» quando applicabile. Le scorciatoie Bridge07 restano proprietarie delle modifiche al testo e ai nodi.
- **Progressive disclosure Codex:** mini-toolbar essenziale per G/C/S, storia e uscita; **Formato ▾** recupera tipo titolo, misura, colore, rimozione formato ed eliminazione. Il pannello globale è ancora disponibile su richiesta, ora comunicato come **Struttura**; le funzioni dell'editor originale non sono eliminate.
- **Studio21:** barra superiore con Salva/Presenta/Schede/Strumenti; Leggi/Flat/Guida rimangono accessibili nella ricerca. Focus, solo su scelta, nasconde la rail e la guida per mostrare più canvas; non cambia `ccm.document.v1`.
- La palette è un **indice di possibilità contestuali**, non un nuovo router che decide l'autorità sull'effetto.

## Prove ed errori riusabili
Node `--check` ha verificato gli script nuovi e preesistenti. Chromium headless via Playwright `page.set_content` ha esercitato palette, ricerca, scorciatoie, navigazione, comandi nativi, formattazione progressiva, modalità Focus, export/riapertura e viewport 390 px. Nei due casi originali le azioni indicizzate erano rispettivamente 16 (Codex) e 24 (Studio, inclusa navigazione di sette schede). Nessun `pageerror` osservato in tali percorsi. Il focus Studio allarga il canvas da circa 1019 a 1150 px nel viewport test a 1360 px; inizialmente lo **restringeva**, a causa delle due colonne grid che rimanevano anche dopo aver nascosto la sidebar: la correzione è impostare un'unica colonna durante Focus.

**Regressione scoperta dopo il primo export:** quando l'HTML di lavoro serializzava la UI runtime, alla riapertura si creava una *seconda* palette. L'inizializzazione ora attende DOMContentLoaded, rimuove i controlli serializzati e ne costruisce una sola copia; prova di salvataggio/riapertura su entrambi i carrier = una sola palette, con comandi funzionanti. Questo non può essere verificato da test JavaScript di sola apertura.

**Copia pubblica Studio21:** la logica di esportazione elimina anche `#me08-launcher`, dialog, toast, CSS e script **dal file HTML pubblico**, non solo dalla vista browser, prima del download. Test della copia pubblica: nessun elemento o sorgente UX08 nel file; alla riapertura nessuna palette e modello con `ui.publicCopy=true`. Le regole native di filtraggio note/nodi/template privati restano invarianti, ma la prova sintetica completa di privacy è quella esercitata nel Bridge07, non una nuova attestazione in questo turno.

**Limiti:** il runner Chromium non verifica l'apertura `file://` sul Chrome Windows dell'operatore, i touch gesture, lo screen reader, la fedeltà su HTML arbitrari, né l'installazione nel checkout Codex. Lo Studio20/21 pubblico, i download MAIOS.it, il sito e l'owner del contenuto non sono stati aggiornati. Questo layer migliora *l'accesso* agli strumenti; non ha ancora introdotto griglie riutilizzabili, editing immagini, unificazione del motore diagrammi o importazione universale.

## Saper fare da conservare
La ricchezza funzionale non deve apparire tutta insieme. Mostrare **azione pertinente e referente**, mantenere le altre capacità raggiungibili con ricerca e disclosure progressiva; le azioni restano native e l'effetto è dell'owner del documento. La forma della UI è anch'essa soggetta a round-trip: i controlli del runtime devono essere ricreati una sola volta e **non appartenere alla copia pubblica**. Un Focus che nasconde la sidebar ma riduce il canvas è una trasformazione fallita nonostante il CSS sia sintatticamente corretto.

Il prossimo discrimine è far provare all'operatore in Chrome Windows i due documenti e rilevare quali gesti o posizioni siano ancora macchinosi. Solo allora scegliamo nuova manipolazione degli elementi o l'adapter HTML inter-sito; nessun nuovo pannello per inerzia.
