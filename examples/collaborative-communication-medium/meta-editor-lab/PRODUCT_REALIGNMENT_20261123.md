# MetaEditor / MetaCanvas — recupero della direzione di prodotto

## Primo passo esercitato: R1 contestuale in Studio21 · 23 novembre

Il [builder visual R1](../../../tools/build_studio21_visual_actions.py) non genera un altro editor. Sulla **vera scena Studio21** collega la selezione di un nodo ai comandi native `Modifica testo`, `Stile`, `Dimensioni`, `Duplica` vicino al punto di lavoro, conservando history e salvataggio già posseduti. [CI 45234069873](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45234069873): 5 job verdi; [regressione browser](../../../tests/metacanvas-studio21-visual-actions.browser.py) su IT/EN, 1440/390, edit, Undo/Redo, work/public export. L'artefatto `metacanvas-studio21-visual-r1` ID `14848068598` è una candidata **non pubblicata**. Screenshots reali `14848043425` ispezionati: il gesto è percepibile sul desktop, ma a 390px il canvas rimane sacrificato dall'intestazione/intro e dal pannello schede. Questo è il **prossimo attrito di esperienza da correggere**, non un problema risolto per aver superato CI.

**Data del feedback:** 23 novembre 2026. **Owner della capacità:** `competences/ux-ai/collaborative-communication-medium/meta-editor`. **Stato:** riesame autoriale, non nuova release, non deploy, non sostituzione dei portatori.

> Operatore: «È ancora abbastanza poco utilizzabile. Non credo, non vedo tanti sviluppi da dove eravamo partiti».

Questa correzione non annulla ciò che era accaduto. Cambia il significato attribuito all'ultima risultante: i test verdi della RC HTML attestano qualità **di un banco tecnico circoscritto**, non il grado d'utilità raggiunto dal MetaEditor come progetto.

## 1. Le sorgenti che determinano il punto di partenza

- **[MetaEditor Evolution SKILL](../../../competences/ux-ai/collaborative-communication-medium/meta-editor/SKILL.md)**: la funzione è formare la facoltà di editing diretto nel medium MetaCanvas per **pagine web e presentazioni**, con gesto umano come referente, non un editor generico arbitrario.
- **Bridge11 owner-native**: `GrazianoGuiducci/maios_it`, branch `work/metaeditor-current`, `workbench/metaeditor/CURRENT.html`, blob `9f4f843124f8619eee02ece40a7efc1470881b07`. È il lavoro reale di editing della pagina Consulenza, **non** una build generalizzata. Nel DOM originale sono presenti Sezioni/Elementi/Dimensioni/Colori, finder, focus, mini-toolbar, resize, movimento, liste/callout, anteprima desktop/mobile, salvare e export.
- **Studio20 MetaCanvas pubblico**, `GrazianoGuiducci/k-ux-ai/main/examples/collaborative-communication-medium/AI_Collaboration_Studio.html`, blob `d057d68c60061dd9e8f5c2d704cfff2016ea19b1`. Un editor spaziale di scene con schede, trascinamento, elementi e relazioni, temi/pannelli adattivi, template `Sostituisci / Sopra / Sotto`, riuso JSON, presentazione e ritorno dall'AI. Studio21 IT/EN è il carrier successivo con due patch candidate di integrità.
- **MetaEditor neutro RC1**: `examples/collaborative-communication-medium/meta-editor-lab/neutral-static-page-editor.js`, 46 KB, toolbar fissa larga fino a `318px`, controllo testuale tramite dropdown, quattro pagine HTML sintetiche e salvataggio fedele. `MetaEditor_1.0.0-rc.1.zip`, CI [45169380830](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45169380830), **5/5 job verdi**. Questo è un **harness di integrazione/portabilità**, non un successore d'uso dei primi due.

La [comparazione Bridge11/Neutro](BRIDGE11_COMPARISON_20261122.md) aveva già registrato molte di queste lacune **prima** di fissare prematuramente il contratto ridotto v1. Il sapere esisteva, ma non ha determinato la scelta del rilascio: è un errore di **entry/routing** della competenza, non una necessità di creare un'altra ontologia o un altro motore.

## 2. Perché la 1.0 ridotta non può chiudere il progetto

| Capacità percepibile | Sorgente che già la esercita | RC neutra | Differenza attuale |
| --- | --- | --- | --- |
| Agire direttamente sul punto selezionato | Bridge11 quick-add, mini-toolbar, focus, maniglie; Studio20 canvas | Picker/toolbar quasi sempre separati dal contenuto | Il gesto visivo richiede troppi passaggi |
| Comporre e cambiare la struttura | Bridge11 sezioni/elementi, lista/callout, dimensioni e colori; Studio20 layout, oggetti, livelli | Titolo/paragrafo, blocchi propri, pochi stili | L'utente non governa forma, gerarchie e spazio |
| Modelli davvero operativi | Studio20 template sostituibili, sopra/sotto, salvabili/trasferibili | Quattro HTML prefabbricati aprono altre schede | Avvio utile, ma non composizione guidata e riuso |
| Percepire ciò che è stato fatto | Bridge11 anteprima desktop/mobile, selezione e resize; Studio20 Presenta/Leggi | Editing DOM e due export | Manca un ciclo visivo chiaro modifica → risultato |
| Conservare senza perdere | Bridge11 lavoro/export; Studio20 HTML/JSON; RC neutra work/clean | **Forte nel sottoinsieme**: hash, source/undo, Windows CI | Quest'ultimo avanzamento resta valido, non definisce da solo il prodotto |

La differenza non si risolve con **più test della stessa toolbar**, più ZIP o un nuovo elenco di micro-funzioni. Non serve nemmeno convertire il DOM HTML in scene `ccm.document.v1`: sono rappresentazioni con owner diversi. È necessario costruire un'esperienza **coerente** che sfrutti le capacità già possedute dai due portatori.

## 3. Direzione ripristinata, senza inventare un prodotto terzo

La competenza MetaEditor rimane una **facoltà evolutiva del medium**. La declinazione per una pagina DOM e quella per una scena 16:9 condividono principi d'interazione (selezionare, agire sul posto, cambiare forma, riordinare, annullare, vedere, salvare), ma **non condividono a forza un solo modello di documento**.

Le prossime trasformazioni devono partire dai gesti che l'operatore vuole esercitare, non dalla facilità di montare una toolbar e raggiungere CI verde. Se una facoltà è già in Bridge11 o Studio20, individuarne l'owner e riutilizzare l'implementazione pertinente oppure il metodo, preservando source, history e relazioni. Il Bridge11 rimane sul suo branch privato finché non esiste un'estrazione coerente: non copiare una intera pagina privata nel pacchetto pubblico.

## 4. Tre risultanti dimostrabili, non un'espansione infinita

**R1 · Superficie di lavoro realmente editoriale.** Una pagina documento o una scena raggiungibile in cui il click seleziona l'oggetto visivamente; i comandi pertinenti appaiono dove si lavora, con feedback/focus e uscita chiari. Navigazione fra sezioni/schede e pannello strumenti non impediscono di vedere il contenuto. Sorgenti: Bridge11 e Studio20. *Prova richiesta:* editing diretto con pochi passaggi, non mera presenza di controlli.

**R2 · Composizione visiva e riuso.** Inserire e spostare gli elementi nel punto desiderato, cambiare dimensioni/stile, gestire parti e sezioni/schede secondo il portatore, scegliere un modello già composto e applicarlo con semantica riconoscibile. Per le scene, template già posseduti `Sostituisci / Sopra / Sotto`; per HTML non fingere conversioni: determinare l'equivalente supportato dalla pagina. *Prova richiesta:* partire da un modello e produrre una pagina/scena sensibilmente diversa senza editing di markup o ricerca nei menu.

**R3 · Risultato, persistenza e rientro.** Anteprima appropriata (anche stretta), Annulla/Ripristina, salvataggio del lavoro modificabile, riapertura e export corretto con conservazione delle relazioni. Le prove della RC neutra sono utili qui come sottosistema, non come surrogato di R1 e R2. *Prova richiesta:* una persona riesce a recuperare il lavoro e a distinguere il file modificabile dal risultato pubblico.

R1–R3 sono **casi d'uso verificabili**, non tre nuove architetture, pacchetti o rilasci. La priorità è recuperare capacità già reali e correggere le frizioni d'uso che le nascondono, prima di espandere il catalogo di componenti.

## 5. Prova d'uso con l'operatore

L'operatore ha già specificato che farà **test d'uso, non QA tecnica**. Prima del prossimo collaudo, presentare **un solo percorso integrato** con la stessa superficie dell'editor, non un'altra galleria di HTML che ricomincia da zero: scegliere un contenuto, modificarlo sul posto, aggiungere/spostare un elemento, intervenire su dimensione/aspetto, verificare visivamente, salvare e riaprire. Le verifiche automatiche restano al codice e agli owner dei portatori.

La sensazione di «non vedo tanti sviluppi» è un **fallimento di riuscita di prodotto reale** anche quando gli snapshot e le pipeline sono verdi. Non si chiede all'operatore di validare di nuovo la RC ridotta per confermare un problema già osservato.

## 6. Stato e autorità

- `MetaEditor_1.0.0-rc.1.zip`: **diagnostico/harness tecnico, non v1 accettata**. Non cancellare o falsificare il suo passato; non promuoverlo.
- `METAEDITOR_1_0_RELEASE_CONTRACT.md`: conserva un contratto storico tecnicamente esercitato, **superato come criterio sufficiente di release del prodotto** dal feedback del 23 novembre.
- Bridge11 `maios_it/work/metaeditor-current`: prototipo autoriale con capacità maggiori, ancora specifico alla pagina, non pubblicato.
- Studio20/21: prodotto pubblico di scena; candidate IT/EN corrette per privacy, ma release owner-site distinta.
- K-UX-AI PR #2: draft, nessun merge e nessun effetto su `maios_it/main`. Il prossimo movimento seleziona owner e portatore in base a R1, non rigenera la RC tecnica.

**Stop condition:** non accumulare nuovi milestone per inerzia. La nuova differenza osservabile (gesto migliorato, composizione esercitabile, persistenza verificata o nuovo feedback umano) deve cambiare veramente la risultante. Fermarsi quando l'ulteriore lavoro aggiunge solo latenza.
