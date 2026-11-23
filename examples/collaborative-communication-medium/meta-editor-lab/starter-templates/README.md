# MetaEditor — scelta del modello iniziale

## 23 novembre — Conservazione del lavoro e incolla

Dopo la scelta di un modello, **Salva lavoro** e `Ctrl+S` richiedono lo stesso download del file HTML modificabile; non usare `Salva pagina con nome` di Chrome per conservare lo stato dell'editor. `Esporta pagina pulita` produce invece l'HTML senza i controlli MetaEditor. Le modifiche rispetto al file aperto sono segnalate dalla UI, e Annulla completo le riporta a zero; i browser possono avvertire quando si chiude una scheda con modifiche, ma non sempre mostrano l'avviso. Controlla che il download esista prima di chiudere una pagina importante.

Il campo testuale accetta incolla **solo come testo semplice**, trasformando gli a capo in spazi per evitare la creazione implicita di altri blocchi. Per creare un nuovo elemento usa `+ Paragrafo` o `+ Titolo`. Il trascinamento dall'esterno nel testo non è supportato. Questi comportamenti sono esercitati nei test, ma non costituiscono una garanzia generale di sanitizzazione di HTML arbitrario. [CI 45133248996](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45133248996) è verde su quattro job.

**Stato:** candidato non pubblicato; parte del ramo K-UX-AI [PR #2](https://github.com/GrazianoGuiducci/k-ux-ai/pull/2).

## Il problema che risolve

Il MetaEditor neutro ha già il controller per modificare una pagina statica e il builder di copie di lavoro, ma la prima esperienza precedente apriva direttamente **una singola pagina sintetica** con molti contenuti dimostrativi. Non offriva una scelta e una pagina vuota, da sola, non rende comprensibile il lavoro a chi si avvicina allo strumento.

L'operatore ha richiamato l'esigenza di **un template da selezionare per prendere confidenza**. Questa differenza riguarda il *punto di ingresso* e l'orientamento, non l'aggiunta di un nuovo formato di documento o una riscrittura del controller.

## Risultato

La pagina [Apri_MetaEditor.html](Apri_MetaEditor.html) è una **schermata statica di scelta**, senza script. Presenta quattro avvii distinti:

| Scelta | Originale dimostrativo | Uso |
| --- | --- | --- |
| Pagina essenziale | [essenziale.html](sources/essenziale.html) | Presentazione breve a tre sezioni: consigliata per imparare |
| Progetto o servizio | [progetto.html](sources/progetto.html) | Proposta, punti di forza e percorso di ingresso |
| Articolo | [articolo.html](sources/articolo.html) | Apertura, approfondimento e conclusione, con topologia `main > article > section` |
| Parti da zero | [vuota.html](sources/vuota.html) | Una sezione minima con titolo e paragrafo iniziali; **non completamente vuota**, per garantire un primo punto di selezione |

Il [builder di avvio](../../../../tools/build_metaeditor_starter_pack.py) usa il *builder neutro esistente*, crea per ogni scelta una **pagina di lavoro autonoma e già modificabile** e confeziona uno ZIP con `Apri_MetaEditor.html`, quattro pagine nella cartella `Modelli` e `LEGGIMI.txt`.

```bash
python tools/build_metaeditor_starter_pack.py --output-zip /path/to/MetaEditor_Scegli_Modello.zip
```

Estrai l'intero archivio, apri `Apri_MetaEditor.html` e scegli un modello. Il click apre una nuova scheda: non sostituisce il lavoro aperto. Il documento di partenza è incorporato immutabilmente in ciascuna copia di lavoro, mentre **Salva lavoro** produce un nuovo HTML riapribile e **Esporta pagina pulita** rimuove editor e marcatori. Tornare alla galleria e scegliere un secondo modello non trasferisce automaticamente il contenuto precedente.

## Prova e limiti

Il [test in Chrome](../../../../tests/metaeditor-starter-chooser.browser.py) costruisce ed estrae realmente lo ZIP, apre la schermata con `file://`, seleziona ognuno dei quattro link, modifica il titolo, inserisce un blocco allineato, verifica l'export pulito, conserva e riapre il lavoro, torna all'originale byte-identico tramite Undo e verifica l'immutabilità del file distribuito. Ripete a 1440 e 390 px. [CI 45124239776](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45124239776): quattro job verdi insieme alle regressioni Studio21 e alla pagina MAIOS originale.

Questo **non è** il formato `metacanvas.templates.v1` per scene `ccm.document.v1`, che rimane in [TEMPLATE_COLLECTION.md](../../TEMPLATE_COLLECTION.md): condividiamo l'orientamento di un avvio a modello, **non** conversioni o import di scene.

Lo ZIP non contiene la pagina MAIOS reale, credenziali, dati personali o riferimenti a servizi esterni. La CI esercita Chrome Linux: non equivale a un'accettazione manuale su Chrome Windows `file://`. La pagina di avvio non è un CMS e il builder non permette HTML arbitrario/non fidato. Il Gate B resta parziale e la PR draft; nessuna modifica a `maios_it/main` o alla distribuzione pubblica.

## Prossimi discriminanti

Verificare se l'operatore comprende facilmente la scelta e le prime due operazioni senza spiegazioni esterne; identificare eventuali ambiguità nella separazione **modello** / **copia di lavoro** / **HTML pulito**. Solo dopo valutare se serve l'anteprima reale o una guida interattiva contestuale. Evitare di portare nella pagina di ingresso selezioni avanzate prima che la prima esperienza risulti chiara.
