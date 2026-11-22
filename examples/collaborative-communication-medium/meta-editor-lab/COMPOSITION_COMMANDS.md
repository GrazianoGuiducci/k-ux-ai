# MetaEditor — comando compositivo comune, effetti nativi

## 22 novembre — Prova successiva: intero Studio21 in browser

Il precedente paragrafo «Scena: mock» descriveva correttamente la prova di allora. La lacuna è stata esercitata nel [nuovo test Chrome](../../../tests/metaeditor-studio21-composition.browser.py): caricamento dei **veri** `MetaCanvas_Studio21_Consulenza_IT.html` e `_EN.html`, prove a 1440/390, inserimento nativo `text` e `card`, un solo nuovo ID e conservazione dei nodi precedenti, `#undoBtn` e `#redoBtn` che tornano a stato e ID, e rifiuti senza mutazione di richieste pagina. [Actions run riuscito 45030544046](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45030544046), con entrambi i job verdi.

**Banco:** prima installazione Chromium fallita (run 45030431494) e test non eseguito; corretta la dipendenza usando il browser Chrome preinstallato nel runner. Il test non dimostra sicurezza di import, accessibilità, uso Windows `file://` né pubblicazione di una nuova edizione. La composizione `move` resta da formare separatamente; non duplicare il controller `addNode`.


**Candidato non distribuito · 22 novembre 2026 · owner:** K-UX-AI / CCM / MetaEditor Evolution

[Modulo](metaeditor-composition-commands.js) · [test del contratto](../../../tests/metaeditor-composition-commands.test.js) · [Gate B](../RELEASE_STABILIZATION_20261122.md)

## Perché esiste

Bridge07 aveva già condiviso `begin / setText / commit / cancel / undo / redo` fra pagina HTML e scene Studio, **senza fondere i loro documenti**. Il Bridge11 e la R3 possiedono `addBlock` e storia nativi, mentre Studio21 possiede `addNode`, `commit` e `ccm.document.v1`. Questo modulo mette in comune soltanto la **richiesta di inserire un elemento**: non crea un terzo modello di stato, una nuova toolbar, un editor parallelo o un gestore Undo.

Il modulo crea `window.MetaEditorCompositionCommands`. Scegliere il carrier reale, **non** inferirlo da una pagina arbitraria:

```js
const commands = MetaEditorCompositionCommands.create({carrier:'page',document});
commands.status(); // tipi page e posizioni supportate
commands.execute('insert', {type:'paragraph',position:'end'});
// Per navigare esplicitamente in una sezione supportata:
commands.execute('insert', {type:'heading',position:'end',sectionIndex:1});
```

Il carrier delle scene usa lo stesso nome di azione con tipi propri, e non accetta posizioni pagina:

```js
const commands = MetaEditorCompositionCommands.create({carrier:'scene',document});
commands.execute('insert',{type:'text'});
commands.execute('insert',{type:'card'});
```

I due comandi modificano **oggetti semanticamente differenti**. `paragraph/heading/list/callout` producono blocchi HTML nel documento statico; `text/card/tag/section/circle/oval/pill/note` producono nodi nel documento di scena. Non convertire `paragraph` in `text` né trasferire attributi DOM nel modello `ccm.document.v1`.

## Proprietà e fallimenti

- **Pagina:** riusa le selezioni `#local-section`, `#local-kind`, `#local-insert-position` e il pulsante `[data-local-action="insert"]`, collegato a `addBlock`. Verifica l'incremento di un solo `[data-local-block]`. Non inventa il markup e non scrive nella history.
- **Scena:** invoca il pulsante nativo `[data-add="…"]`, che chiama `addNode` con `commit` e genera l'ID; misura un nuovo `#canvas .node[data-id]`. Il significato resta del controller Studio.
- **Esito:** `{ok:true,carrier,effect:'inserted',type,...}` solo dopo l'effetto osservato; `{ok:false,carrier,reason}` per tipo/azione/ancoraggio indisponibile. Non esiste una mutazione simulata di successo.
- Se la sezione selezionata cambia per un inserimento ma l'ancoraggio richiesto non è ammesso, ripristina la selezione precedente. Non promette Undo per i cambi di UI, solo per le mutazioni native.
- Non gestisce ancora `move`, `delete`, selezione multipla, layout, immagini o import HTML. I loro proprietari restano i controller esistenti.
- L'inserimento in modalità Presenta/lettura di Studio va riesercitato nel carrier reale: il test simulato della scena **non** è prova E2E di Studio21.

## Evidenza e prossimi controlli

- **Node:** 6 test di contratto su delega, rifiuto e ripristino della sezione; eseguiti localmente e inclusi in `npm test` della PR candidata.
- **Chromium:** inserimento blocco e Undo nel vero Bridge11 e nella R3 MDN, su 1440×844 e 390×844, nessun `pageerror` nei percorsi. L'editor HTML era già operativo; il nuovo modulo è iniettato nel test, non pubblicato come UI.
- **Scena:** contratto provato contro fixture DOM con pulsante nativo simulato; l'implementazione Studio21 è stata ispezionata (`[data-add]` chiama `addNode`, `commit` e `render`), ma un browser test sullo Studio completo rimane necessario.
- Test browser ripetibile sul carrier privato: `maios_it/work/metaeditor-current/workbench/metaeditor/experiments/test_composition_native_bridge.py`, con `--bridge11`, `--mdn-r3`, `--composition-js` e `--chromium`.

**Gate B non chiuso.** Quest'estrazione è un contratto esercitato, non MetaEditor generico o una release di MetaCanvas. Nessuna modifica ai download o a `maios_it/main`.
