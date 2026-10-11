# K-UX-AI v5.6 — Canvas guidato, attività accessibili, primo ingresso coerente

11 ottobre 2026 · owner: `GrazianoGuiducci/k-ux-ai` · branch candidato `work/ux-ai-ui-library-20261008`.

## Fonte e selezione

Le tre nuove schermate Edge dell'operatore sulla v5.5 hanno portato quattro differenze concrete:

- `Esplora` nelle tessere contestuali non mostrava chiaramente un cambiamento di contesto e il divisore restava nello spazio vuoto quando era aperta una sola scheda;
- in fullscreen la barra **Attività** copriva la scheda e il pulsante flottante in basso sembrava un secondo ingresso all'assistente;
- nella Home erano ripetuti stato dimostrativo, selettore del contesto e chip del laboratorio, pur essendo il contesto già controllato da **Prepara il campo**;
- il Canvas contiene più funzioni di quante un nuovo operatore possa riconoscere dal tour iniziale; la colonna Attività e i controlli richiedono spiegazioni e comportamenti effettivi.

L'operatore conferma che il Manifesto non va ridotto al Web: la ricerca K-UX-AI riguarda **UX per l'AI su Web, applicazioni e altri ambienti digitali**. Il [Manifesto](../../MANIFESTO.md) è stato completato presso il suo owner, preservando il testo precedente. K-UX-AI mantiene significato e competenze del medium; Kernel Nautico conserva oggetti e verità di dominio; il sito MAIOS e Codex restano riceventi e owner distinti per i loro effetti.

## Risultato esercitato nel candidato v5.6

- **Home:** la toolbar della sola Home lascia brand, scelta di superficie e aiuto, mantenendo le informazioni contestuali dentro il pannello di preparazione; la toolbar del Canvas resta funzionale. La chat è in basso a destra nella Home, in basso a sinistra nel campo.
- **Canvas tour:** sette passaggi con spotlight sul controllo effettivo: contesto/azione, accessi Attività, comandi delle schede e possibilità di movimento, disposizione e ricomposizione, dialogo di sezione, assistente generale, eventi e ripresa. Il tour della Home resta distinto. Escape, indietro/avanti, chiusura e ritorno al focus mantengono la funzione originaria. Il `?` apre il tour nel Canvas; su mobile è raggiungibile anche da Strumenti.
- **Attività:** barra affiancata al campo con **dieci ingressi sintetici** in elenco scorrevole e indicazione dello stato; non è un inventario di dieci applicazioni o competenze Nautico effettive. Un controllo esplicito la nasconde, un ingresso al bordo la riapre e il mouse può farla comparire temporaneamente. Tastiera e focus restano disponibili; al collasso la barra è esclusa dall'albero interattivo.
- **Fullscreen e divisori:** la scheda a tutto schermo si dispone **accanto** alla barra, che non diventa un overlay sul suo contenuto. Nascondendo la barra, la superficie può espandersi. Il divisore non compare in assenza di una seconda regione reale e viene aggiornato dopo la geometria finale; lo stato del layout non si deduce da un pannello fantasma.
- **Esplora e controller:** i pulsanti contestuali della scheda Esplorare selezionano l'ambiente di destinazione e aprono il suo oggetto percettivo con nuovo stato di vista, **senza riassegnare il contesto/source owner alla scheda precedente**. Si conserva la distinzione `entità sorgente != proiezione != gesto != conseguenza`. L'azione è locale e illustrativa.
- **Assistente:** un unico ingresso visibile secondo la superficie. Con barra attività nascosta resta raggiungibile in basso a sinistra; la chat generale e il Dialogo scheda preservano proprietari e confini già esistenti. Nessun modello, capacità autonoma o permesso reale è stato installato.

## Identità e ricevuta

- Nuovo [HTML standalone](18-griglia-situated-v56.html): SHA-256 `8bb3939c44ab46bdfe7fff14beea8b63f8ad07afa723bd595e423022dcc3c617`, Git blob `82ed7a973883e30e5e781f11120aa27bf668bdba`; 372417 byte.
- Baseline preservata: [v5.5](17-griglia-situated-v55.html), Git blob `b84046ab5285823ba418d131bc36e56810cdc0fc`.
- [Builder deterministico](../../tools/build_nautico_v56.py): genera la v5.6 dalla baseline hash-guarded; `python tools/build_nautico_v56.py --check` verifica output byte-identico.
- [QA nuovo](../../tests/qa_nautico_v56.py): **126/126** controlli correlati su 1715 desktop normale, 1280 desktop reduced motion, 390 mobile reduced motion e percorso aggiuntivo 1440 per Esplora. [Ricevuta](EVIDENCE_CANVAS_V56_20261011.json).
- [QA regressivo](../../tests/qa_nautico_v56_compat.py): **59/59** controlli correlati al comportamento v5.5 nel nuovo file; tre script embedded passano `node --check`. Nessun errore JS di pagina osservato nelle suite finali.

**Limiti:** le prove usano Chromium/Playwright con `page.set_content`, non l'Edge fisico dell'operatore, non una vera pagina ospitata, né un audit di lettori indipendenti/assistive technology/touch fisico. Le due suite sono correlate sulla stessa sorgente, non 185 validazioni indipendenti. Non sono stati connessi il bridge Nautico, la chat MAIOS, i provider o account reali.

## Apprendimento e ritorno

Una barra di navigazione diventa **regione operativa reale**, non un elemento decorativo, solo se rimane accessibile e coerente con le geometrie delle viste. La visibilità di un divisore deve dipendere da due regioni occupate, non da un handle presente nel vecchio DOM. Le azioni chiamate Esplora devono cambiare effettivamente la proiezione mantenendo il referente sorgente: mutare il contesto di una card preesistente per ottenere un effetto grafico sarebbe una sostituzione dell'oggetto. L'ingresso unico all'assistenza segue la superficie e il controllo del focus; l'hover rende raggiungibile, non esegue.

Questo sapere operativo appartiene alla [Code Medium Construction](https://github.com/GrazianoGuiducci/tm7/blob/gpt/ux-ai-code-competence/chatgpt/competences/code-medium-construction/SKILL.md) e alla sua guida; Design/Interaction Quality preserva il metodo di agenzia, accessibilità e recovery, UX-AI la comprensione in corso d'opera, Editoriali la forma del Manifesto e dei microtesti.

## Condizione di arresto e rientro

Candidato v5.6 costruito, testato, attestato e mantenuto distinto dalla v5.5. **Nessun merge, package release, deploy, mutazione di Kernel Nautico o di `maios_it`, provider/account, contatto esterno.** Da nuova istanza entrare da `AGENTS.md` → `docs/ui-library/CURRENT.md` → questa ricevuta → file concreto → competenze pertinenti. Il successivo evento utile è il readback dell'operatore in Edge oppure l'integrazione Codex, da selezionare separatamente e basare su owner reali.
