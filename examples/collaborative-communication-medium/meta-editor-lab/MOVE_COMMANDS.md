# MetaEditor — spostamento nativo, due significati distinti

**Owner:** K-UX-AI / Collaborative Communication Medium / MetaEditor Evolution  
**Stato:** componente di lavoro nel ramo `work/metacanvas-metaeditor-stabilization-20261122`, **non distribuito**.

## Contratto comune, mutazioni differenti

Il [modulo `metaeditor-native-move.js`](metaeditor-native-move.js) espone:

```js
const move = MetaEditorNativeMove.create({carrier:'page', document});
move.status(); // operation: place-added-block
move.execute({sectionIndex:1, placement:'end'});
move.execute({sectionIndex:0, placement:'before', targetIndex:2});
```

Per la pagina l'operatore deve aver **selezionato un blocco aggiunto** e aperto l'editor nativo. `targetIndex` è l'indice della lista dei **riferimenti sicuri mostrati** da `#me11-target`, esclusa la voce `end`; non è l'indice di un figlio DOM arbitrario. Il comando seleziona la destinazione nel pannello Bridge11, convalida il riferimento, poi usa il solo bottone nativo `data-local-action="transfer"`. Mantiene il markup e il controller dello storico esistenti. Non rende spostabili i componenti originali protetti.

```js
const move = MetaEditorNativeMove.create({carrier:'scene', document});
move.status(); // operation: nudge-scene-node
move.execute({nodeId:'el-...', direction:'right'});
```

Nelle scene è **un solo passo di 5 unità** sul nodo attualmente renderizzato nel canvas (non una nuova API per assegnare coordinate arbitrarie). L'evento di tastiera nativo di Studio21 sposta il nodo e possiede `commit`, Undo, Redo e l'eventuale adeguamento del `containerId`. Non si altera `ccm.document.v1` fuori dal controller. Non si promette che riordinare il DOM e variare una posizione spaziale siano lo stesso effetto: sono richieste omonime con referenti, parametri e prove specifici del carrier.

## Controlli di integrità

- **Pagina:** il controller ammette solo blocchi con `data-local-block` attivi; riferimento non sicuro o posizione nulla produce `ok:false`. Cambi alla sola scelta del pannello vengono ripristinati dopo un rifiuto di ancoraggio. L'identità del blocco passa attraverso il controller Bridge11; non si sostituiscono nodi tramite un nuovo engine.
- **R3:** il receiver riconosce anche `main > article`, oltre al `main > section` del portatore Consulenza. La prima prova aveva scambiato questa differenza strutturale per un movimento fallito; il controllo dell'esito è stato corretto e provato.
- **Scena:** `nodeId` deve corrispondere a un nodo editabile visibile nella scena; direzione valida fra `left/right/up/down`; la verifica del limite evita un checkpoint inutile sul bordo; presentazione, lettura e copia pubblica rifiutano il movimento. Non accetta le posizioni relative della pagina.
- **Storia:** un singolo evento delegato ai controller che già gestiscono la storia; questo modulo non crea snapshot o serializzazioni.

## Prove esercitate il 22 novembre

- **Pagine reali:** Playwright Chromium `set_content`, Bridge11 e R3 MDN, a 1440×844 e 390×844. Due blocchi aggiunti, riferimento `before`, Undo/Redo, no-op senza checkpoint e rifiuto di riferimento inesistente; Bridge11 provato anche fra sezioni. Risultati locali positivi; nessun `pageerror` nei percorsi. [Test ripetibile nel workbench privato](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/workbench/metaeditor/experiments/test_move_native_bridge.py), vincolato agli SHA originali.
- **Studio21 IT/EN veri:** [GitHub Actions run 45035705911](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45035705911) con entrambi i job riusciti; Chrome Linux a 1440 e 390. Dopo l'inserimento di nodi mediante comando condiviso, il test esercita movimento di un passo, persistenza degli ID, Undo/Redo, rifiuto di richiesta `page` e movimento bloccato nella vista lettura.
- **Test contrattuali Node:** [`tests/metaeditor-native-move.test.js`](../../../tests/metaeditor-native-move.test.js), sei verifiche (delega, casi non validi, lettura/presentazione, bordo, distinzione semantica), suite CI riuscita, [run 45035753475](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45035753475).
- **Sorgenti intatte:** il codice dell'editor condiviso non è stato inserito nei download pubblici; i test lo caricano come modulo separato sui documenti originali.

## Limiti e prossimo discriminante

Questo **non** certifica gesture touch, siti HTML arbitrari, portabilità Windows `file://`, accessibilità globale, sicurezza dell'import o fedeltà di immagini, diagrammi, template e link dopo spostamenti complessi. Lo spostamento di un contenitore di scena e dei suoi figli, la posizione geometrica completa e le relazioni dei collegamenti meritano una prova dedicata prima della release. I Gate B–F di [stabilizzazione](../RELEASE_STABILIZATION_20261122.md) restano aperti; PR #2 in bozza, nessun commit a `maios_it/main` e nessun deploy pubblico.
