# MetaEditor Evolution — guida viva

## 16 novembre — primo gesto esercitato, senza importare la pagina MAIOS

La competenza è stata esercitata attraverso un [banco neutro HTML autonomo](../../../../examples/collaborative-communication-medium/meta-editor-lab/MetaEditor_Lab01.html) (e [guida del banco](../../../../examples/collaborative-communication-medium/meta-editor-lab/README.md)). Il primo confronto è concreto: **doppio clic sulla label del nodo → il contenuto è `contenteditable` nel nodo → digitazione → Enter → Undo → Redo**. È distinto da R4, dove si editava un campo remoto dell'inspector. Il modello `metaeditor.lab.v1` con sezioni e diagrammi è un dato sintetico, non il formato Studio20 `ccm.document.v1`. L'editor consente anche muovere il nodo conservando i collegamenti, trascinare una card fra sezioni, usare layout responsive, aggiungere un template diagramma+note senza cancellare contenuto, vedere una proiezione in formato slide e scaricare/riaprire l'HTML. L'esercizio tecnico non certifica percezione o uso reale da parte dell'operatore.

**Due apprendimenti del banco hanno cambiato il fare:**
- Il JavaScript passava i controlli e i testi erano editabili, ma uno stile `[contenteditable="true"]` mancava della parentesi di chiusura. Il diagramma perdeva la geometria. Il rendering visto nel browser ha corretto il risultato: per una competenza visiva, **sintassi ed eventi non bastano senza verifica della resa**.
- Il primo comando «Diagramma + note» rimpiazzava l'intero contenuto della sezione. L'azione è stata riformata come **aggiunta di nuova sezione**, con un singolo checkpoint Undo. L'operatore deve poter scegliere una sostituzione soltanto quando esplicita: un template non può distruggere per sorpresa il contenuto esistente.

**Prove effettive:** Node 22 sul runtime; Chromium headless via `page.set_content` su testo del nodo, Undo/Redo, text edit ordinario, trascinamento del nodo (coordinate), Undo, duplicazione card, drag-drop fra sezioni, template, passaggio pagina/proiezione, download, lettura e nuova inizializzazione in altro contesto, viewport 390 px e zero pageerrors osservati nel percorso. `file://` e `http://localhost` sono risultati bloccati dall'ambiente browser di test; la verifica è stata eseguita senza attribuire il blocco al codice. Non è prova su Chrome Windows, import web arbitrario o usabilità universale.

**Saper fare che continua:** la competenza ha ora un banco minimo del gesto da preservare. La prossima differenza materiale non è aggiungere tutte le funzioni Canva, ma confrontare **fedeltà import/patch di regioni HTML reali** senza perdere il diretto `contenteditable` dei nodi. Studio20 resta fonte delle capacità di edit dei nodi e la relazione CCM rimane il medium, senza importare automaticamente tutto il suo runtime.


## 16 novembre 2026 — perché la competenza nasce ora
**Fonte:** l'operatore, dopo R3/R4 aperte in Chrome Windows e screenshot di Canva, chiede un editor generale per pagine e presentazioni, con editing immediato dentro i diagrammi; successivamente seleziona esplicitamente una **competenza dedicata capace di evolvere il MetaEditor**. Questo segna un oggetto operativo distinto: non solo un artefatto editabile da consegnare e condividere (CCM), ma il *metodo di costruire e correggere gli editor stessi* attraverso il loro uso.

**Causalità conservata:** Studio 20 possedeva già `.node-edit[contenteditable]`; una scelta di renderer SVG nella R4 ha deviato il gesto su `#mc-node-label` nell'inspector. La verifica Chromium ha certificato azioni su quel campo, senza falsare il dato tecnico; l'uso reale ha rivelato che non certificava **il gesto richiesto**. La capacità esisteva ed era raggiungibile ma non ha formato l'azione. La prossima prova deve recuperare quel saper fare e verificare la micro-interazione reale. L'owner CCM ha già il [riesame di architettura](../references/metacanvas-editor-architecture-reset-20261116.md): qui non se ne duplica la genealogia.

### Domanda che cambia la progettazione
Quale combinazione di selezione, testo editabile sul posto, relazione tra nodi, flusso responsive e document adapter produce il minor numero di passaggi preservando il contenuto originale e gli effetti esportabili? Il progetto non nasce dalla necessità di sommare toolbar e controlli, ma dalla **continuità dell'oggetto modificato**. L'esperimento può preferire un motore già disponibile, una sua parte, un'integrazione di libreria o una costruzione minima; la scelta deve dipendere dalle differenze verificate.

### Banco discriminante inaugurale
1. Su HTML sintetico, fare doppio clic sulla **scritta** del nodo del diagramma, ottenere focus nello stesso nodo, cambiare il testo, completare la modifica, e annullarla con Undo. La freccia resta agganciata quando il nodo si sposta.
2. Duplicare una card e ricollocarla in una sezione a due colonne; la resa mobile conserva l'ordine logico.
3. Esportare e riaprire il documento, con ID e contenuti stabili, senza toolbar duplicate e senza perdere dati. Mostrare la differenza prima di applicarla a un altro file.
4. Ripetere il test su un documento non MAIOS; import/export arbitrary HTML è **ipotesi**, non promessa.
5. Valutare come proiezione distinta una scheda di presentazione; nessuna uguaglianza automatica fra layout CSS di pagina e coordinate di scena.

### Fonti di capacità da confrontare
- [Studio 20](../../../../examples/collaborative-communication-medium/AI_Collaboration_Studio.html): nodo editabile direttamente, scene, links, undo, selezione e round-trip AI.
- [Siteman Studio](https://github.com/GrazianoGuiducci/d-nd_com/blob/main/components/admin/SitemanStudio.tsx): contentEditable nell'editor redazionale e passaggio visuale/sorgente, non importatore arbitrario di siti.
- [GrapesJS core](https://grapesjs.com/docs/), [Puck](https://puckeditor.com/docs), [Tiptap](https://tiptap.dev/docs/editor/), [Excalidraw](https://github.com/excalidraw/excalidraw), [tldraw](https://tldraw.dev/): strumenti/referenti con ambiti e licenze differenti, da rivalidare nella forma scelta.
- [D-ND Design](https://github.com/GrazianoGuiducci/d-nd-ux-ai-seed): Interaction Quality e Perceptual Composition.

### Come questa guida impara
Registrare una differenza solo quando cambia un gesto o il prossimo metodo. Per ogni episodio utile conservare: **fonte e intento → implementazione/competenza realmente selezionata → prova eseguita → differenza vista → ragione fondata o ipotesi → cambiamento della capacità → prova successiva discriminante**. Non costruire report ripetitivi. L'operatore può cambiare priorità nell'uso e il nucleo deve seguire la trasformazione, non un backlog chiuso per inerzia.

**Stato di formazione:** metodo scritto nell'owner K-UX-AI; una prova futura non identica dovrà mostrare che la nuova competenza viene esercitata e corretta senza doverla reinsegnare.
