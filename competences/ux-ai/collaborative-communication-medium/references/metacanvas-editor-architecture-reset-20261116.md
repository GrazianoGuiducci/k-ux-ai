# MetaCanvas — riesame del modello editoriale dopo l'esercizio R4
Data: 16 novembre 2026  
Owner del metodo e prodotto: K-UX-AI / Collaborative Communication Medium  
Stato: **architettura candidata; ricerca e discriminazione tecniche svolte, nessuna R5 implementata, nessuna modifica al sito**.

## Origine: correzione dell'operatore in uso reale
L'operatore ha aperto R4 sul proprio Chrome Windows e ha segnalato: «Faccio fatica a usarlo», «non posso neanche editare il testo nel diagramma». Ha fornito schermate dell'editor R4, della selezione di template Canva e dell'editor Canva con selezione di un oggetto, toolbar, libreria di forme, azioni contestuali e allineamenti. Propone di **rivedere completamente il progetto**, studiando idee e codice esistenti, per ottenere un artefatto generale riusabile su siti web diversi e in presentazioni.

Non confondere:
- **R4 tecnicamente provata** in Chromium headless per i gesti che i test eseguivano;
- **R4 incontrata dall'operatore**, che non fornisce la modifica diretta e comprensibile del testo del nodo, la funzione fondamentale di quel gesto.
Un test di modifica del campo `#mc-node-label` in un inspector non dimostra che una persona possa fare doppio clic sulla scritta del diagramma e digitare sul posto. La lacuna è nel metodo di prova e nel modello di interazione, non soltanto nell'assenza di un pulsante.

## Riscontro nel codice già posseduto
1. `k-ux-ai/examples/collaborative-communication-medium/AI_Collaboration_Studio.html` (Studio 20) **contiene già** la via di editing diretto dei nodi: classe `.node-edit`, `contentEditable` e gestori `clickNode` / chiusura della modifica. Il sistema è a scene e usa `ccm.document.v1` con elementi, link, scene, undo e round-trip AI.
2. La R4 privata deriva dall'HTML MAIOS R2 con un diverso modello `data-mc-model`; `mcDrawGraph` restituisce un SVG di nodi e label e `mcOpenVisual` apre un editor con campo `#mc-node-label`. È una **regressione funzionale rispetto al gesto disponibile in Studio 20**. Recuperare prima il saper fare esistente; non ricreare da zero il sistema di selezione/testo.
3. `d-nd_com/components/admin/SitemanStudio.tsx` fornisce un'altra incarnazione: editor HTML visuale con `contentEditable`, passaggio sorgente/visuale, contesto per l'AI e separazione redazione/pubblicazione. Può contribuire al flusso redazionale, ma **non** è evidenza di un editor visuale arbitrario di tutti i siti.
4. `maios_it` contiene le pagine statiche produttive e le proprie regole: push su main può provocare sync su VPS; non usarla per test esplorativi. L'HTML R2 fornito ha CSS personalizzato, script runtime, sezione hero, contenuti, pulsanti e un editor inglobato; non è un template vuoto.
5. `d-nd-ux-ai-seed` possiede la capacità di design (Interaction Quality/Perceptual Composition), non una seconda copia dell'applicazione.

## Soluzioni esterne studiate come fonti, non autorità
- **Canva** (schermate operator): selezione locale, strumenti collegati all'oggetto, libreria, allineamenti, pagine e template; utilizzare i principi di interazione, non copiarne stile, elementi grafici o codice.
- **GrapesJS core**: modello a componenti con view distinta, parser HTML/CSS, blocchi e text editor; candidato da esercitare per composizione di pagine esistenti. I documenti ufficiali chiariscono che **HTML/CSS riesportato non conserva da solo tutto lo stato di progetto**: persistenza progetto in JSON. Il core è open source BSD-3-Clause; lo Studio SDK commerciale è un prodotto/licenza diversi.
  - https://grapesjs.com/docs/modules/Components
  - https://grapesjs.com/docs/modules/Storage
  - https://grapesjs.com/docs/guides/Custom-CSS-parser.html
- **Puck**: editor React a componenti, nesting e layouts, MIT; buon candidato dove la pagina viene già progettata con componenti React registrati, meno ovvio come importatore fedele di HTML/JS eterogeneo.
  - https://puckeditor.com/docs
- **Tiptap**: node views per editing misto di testo e widget; riferimento per l'inserimento di oggetti dentro il testo, non per sostituire da solo l'intero site builder.
  - https://tiptap.dev/docs/editor/extensions/custom-extensions/node-views
- **Excalidraw**: canvas React incorporabile, componenti con frecce, testi, binding, SVG/PNG e JSON; package MIT. Candidato per un motore diagrammi separato e incorporabile, da confrontare con quello Studio 20.
  - https://github.com/excalidraw/excalidraw
- **tldraw**: editing diagrammi/infinite canvas molto sviluppato; SDK con produzione regolata da licenza specifica, non automaticamente adatto alla distribuzione libera prevista per MetaCanvas.
  - https://tldraw.dev/faq

## Nuova domanda di architettura
Non «come fondere tutta la R4 con Studio 21?», ma:

**Quale nucleo di editing di oggetti, testo e relazioni può operare nel documento di partenza, con proiezioni diverse per pagina web e presentazione, senza appropriarsi del DOM e del codice che appartengono a un altro sito?**

Possibile composizione candidata:

```text
                    MetaCanvas Workbench
    selezione · comandi · history · libreria · handoff AI
                            |
              +-------------+--------------+
              |                            |
         Page adapter                Presentation adapter
   sezioni / flow / responsive       scene / pagina / note
   import HTML + safe regions        Studio20 scene model
              |                            |
              +-------------+--------------+
                            |
                  Diagram editor interno
            nodo · testo diretto · link · SVG
                            |
                 preview / export / diff
```

L'interfaccia può essere comune; la geometria, il carrier e la fonte di verità dei due tipi di documento **non devono per forza coincidere**. È possibile una relazione/proiezione fra pagina e scena, ma la traslazione va esercitata anziché postulata. Preferire il riuso di Studio 20 sul diagramma prima di adottare nuovo SDK esterno.

## Contratto d'uso — minimo e falsificabile
- **Single click** seleziona un elemento e rende visibili pochi comandi (duplica, elimina, sposta, altro). **Doppio clic sul testo di una pagina o su una label dentro il diagramma** piazza il cursore **sul testo stesso**, digitazione diretta, `Esc` annulla la modifica in corso, `Enter` conferma dove congruente. Non deve aprire automaticamente un pannello distante per l'operazione più comune.
- Un contenitore non deve competere con i suoi figli: distinzione esplicita di **selezione sezione**, **oggetto**, **nodo interno al diagramma**. La toolbar dipende dall'oggetto selezionato. Il ramo «Avanzate» può aprire un inspector; non tenerlo permanentemente aperto.
- Rail discreta di sinistra per Inserisci / Struttura / Template, canvas centrale dominante, toolbar contestuale; Inspector destro **solo su richiesta** per stile e dati approfonditi. Nessun contorno permanente su ogni paragrafo.
- Sezioni template: 1, 2, 3 colonne, diagramma più note. Le sezioni compongono **griglie responsive**, non coordinate assolute imposte alla pagina web. Nel canvas diagramma vale la geometria propria dei nodi.
- Un diagramma è un oggetto della pagina con editor interno, versione dati, SVG/render esportabile e testo direttamente modificabile; non confondere cambiamento di label con titolo/caption HTML del contenitore.
- Stato unico per ogni documento e una cronologia coerente. Salva la sorgente autoriale insieme al progetto e produce un **diff/patch** leggibile prima di trasferire a Codex. Preview e export non includono toolbar e codici temporanei dell'editor.
- L'interazione «Genera immagine qui» connette il punto scelto a un vero provider/receiver quando disponibile, altrimenti prepara una richiesta e riceve poi un asset. Non dichiarare generazione diretta se esiste solo un prompt copiato.

## Adattarsi a siti diversi: tre classi, non compatibilità inventata
1. **HTML statico importabile:** importare con preservazione di CSS, semantica, media e strutture; trasformare soltanto componenti riconosciuti; gli altri rimangono non distruttivi.
2. **Siti dinamici/CMS:** usare componenti o regioni editabili dichiarate dall'adapter del sito; l'editor non riscrive arbitrariamente React, script o dati applicativi.
3. **Siti arbitrari non riconosciuti:** visualizzare in sola lettura o proporre un adapter; non promettere round-trip fedele quando non è dimostrato.

La portabilità è una capacità dei **connettori di documento**, non la capacità magica di riscrivere qualsiasi pagina senza conoscere il suo owner. Non scrivere su `maios_it/main` durante il lavoro esplorativo: il suo push può diventare pubblicazione.

## Primo esperimento discriminante, prima di una R5
Un **banco neutro e piccolo**, non la pagina MAIOS completa:
1. Importare e riconoscere una sezione di HTML esistente, conservando intatti script/CSS e attributi sconosciuti.
2. Inserire un diagramma, fare doppio clic **sulla scritta di un nodo** e digitare in situ, spostare il nodo e vedere le frecce seguire; salvare/riaprire con un solo Undo per modifica.
3. Duplicare una card e trascinarla in una sezione a due colonne; il layout resta leggibile su mobile.
4. Rendere la stessa relazione in una scheda di presentazione **senza** dichiarare equivalenza dei due modelli.
5. Generare diff del cambiamento sulla pagina, riaprire il documento non modificato, e applicare la modifica soltanto all'oggetto selezionato.
6. Ripetere su una seconda pagina HTML estranea a MAIOS; se fallisce, classificare correttamente il limite dell'adapter.
7. A ogni iterazione misurare il **gesto umano** e il ritorno completo del file, non soltanto `pageerror == 0`.

**Primo motore da discriminare:** GrapesJS core per l'editing di pagina, confrontato con l'attuale editor DOM per *fedeltà di import/reexport*; per diagramma esercitare prima il motore Studio20, poi comparare Excalidraw se servono funzione o manutenzione non già possedute. Non adottare GrapesJS, React, Excalidraw, Tiptap o altra tecnologia prima di questo confronto mirato.

## Autorità ed effetto
Questo documento corregge il **modo di preparare il prossimo lavoro**, non produce un'app già migliorata. R3/R4 rimangono casi storici, non sorgenti canoniche della nuova architettura. Owner K-UX-AI conserva metodo e prodotto, MAIOS.it e d-nd.com i propri contenuti, Codex il proprio receiver e checkout. Per una nuova implementazione: nuova formazione di competenza, poi scelta distinta dell'oggetto e suo esercizio reale. Nessuna pubblicazione o implementazione in questo deposito.
