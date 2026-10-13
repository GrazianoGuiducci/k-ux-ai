# La Griglia come presentazione e primo uso del kernel

Una persona incontra un sistema che ancora non conosce. Le schede spiegano
il lavoro, presentano il kernel e rendono raggiungibili guida, caso e prime
attività. `contexts.json` è il template pubblico dei due primi contesti:
K-UX-AI che presenta se stesso, e Kernel Nautico applicato al ciclo dello yacht.

`createKernelGrid` usa il medium esistente. Il contesto possiede soggetti,
oggetto, caso, fonti, schede e azioni; il ricevente fornisce il controller.
Una scheda può rappresentare una competenza o un'attività contestuale.
La composizione attuale è un assetto iniziale modificabile, non la tassonomia
o il limite del kernel.

`python tools/build_kernel_mirror.py` aggiorna gli stili incorporati nel primo
incontro dalla sorgente unica `src/ui/kernel-grid.css`. Il ricevente può usare
il file CSS o il proprio bundler; la resa effettiva resta da osservare.

```js
import { createKernelGrid } from '../../src/ui/kernel-grid.js';
const contexts = await fetch('./contexts.json').then(response => response.json());
const grid = createKernelGrid({
  host: document.querySelector('#kernel-grid'),
  context: contexts['k-ux-ai'], locale: 'it',
  onAction: action => receiver.openView(action.target),
});
```

Il ricevente conferma l'apertura; una richiesta non la dimostra. Un'azione
precedente non cambia la scheda che l'utente ha selezionato nel frattempo.
La variazione di stato non cancella il testo in corso.

Le note sono contributi della persona, conservati per contesto e scheda nel
browser o nel file esportato. La vista condivisa espone solo il conteggio,
non i testi delle note. Un ambiente AI collegato può ricevere i contributi
quando la persona li condivide e usarli nel lavoro e nel ritorno di metodo.
Questa superficie locale non dichiara una modifica autonoma della competenza.

La Griglia v5.12 in `../griglia/` conserva la propria sorgente originale e il
proprio contratto. L'incarnazione di questo template nel sito MAIOS ha identità
e riscontri distinti. Il demo 3D e le azioni nautiche appartengono a Nautico.
