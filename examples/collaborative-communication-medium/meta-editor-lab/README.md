# MetaEditor · Lab 01 — banco neutro

**Stato:** esperimento tecnico verificato in Chromium headless, 16 novembre 2026; **non** è MetaCanvas Studio 22, una nuova release npm o una modifica al sito MAIOS.it.

**Apri** [MetaEditor_Lab01.html](MetaEditor_Lab01.html) in un browser (file autonomo, senza dipendenze). Usa doppio clic **sulla scritta dentro un nodo** o su un testo per modificare in loco, Invio per confermare, Esc per annullare la singola editazione; Annulla/Ripristina hanno uno storico del documento. Seleziona un riquadro e trascina la maniglia a un'altra posizione; seleziona un nodo e trascina il piccolo punto di presa per cambiarne la posizione mantenendo le frecce agganciate. Le composizioni 1/2/3 colonne sono responsive. «Diagramma + note» **aggiunge** una nuova sezione e non cancella la precedente. «Presentazione» è una **proiezione dimostrativa** della stessa relazione, non il motore completo Studio20 delle schede. «Salva HTML» scarica un documento autonomo modificabile e riapribile, con i controlli runtime ricostruiti una volta.

## Cosa è stato verificato

**Prova locale Node + Chromium headless:** l'HTML contiene due script (modello JSON + runtime JS); runtime sintatticamente valido in Node 22. Playwright tramite `page.set_content` ha esercitato: editing diretto di testo del nodo, Undo/Redo, text editing ordinario, spostamento del nodo con coordinate modificate, Undo della posizione, duplica card, drag-drop fra sezioni, creazione del template in nuova sezione, passaggio pagina/presentazione, export e riapertura in un contesto browser pulito, un solo script dati e un solo menu, presenza di label modificata dopo riapertura, assenza di errori JS osservati, viewport 390 px senza overflow nel documento provato.

**Correzione durante lo stesso esercizio:** una parentesi mancante nella regola CSS `[contenteditable="true"]` invalidava la geometria dei nodi, pur con JavaScript perfettamente valido e test funzionali inizialmente verdi. La verifica della resa ha scoperto il difetto e la prova è stata ripetuta. Il template «diagramma + note» inizialmente sostituiva il contenuto di una sezione; è stato corretto per aggiungere un'altra sezione non distruttivamente. Entrambe le differenze sono ritornate alla [competenza MetaEditor Evolution](../../../competences/ux-ai/collaborative-communication-medium/meta-editor/SKILL.md).

## Cosa il banco NON prova

Non importa HTML arbitrario, non modifica CSS/JS di siti esistenti, non gestisce siti React/CMS, non conserva integralmente una pagina MAIOS, non ha editor geometrico Studio20 o scambio AI, non integra generazione di immagini e non dimostra che la modalità presentazione gestisca slide e note. L'editor usa un modello sintetico `metaeditor.lab.v1`, **non `ccm.document.v1`**. La verifica ha usato `set_content` perché in questo ricevente Chromium bloccava navigazioni file:// e localhost; non prova apertura reale su Chrome Windows dell'operatore, accessibilità completa, touch o usabilità esterna.

## Prossimo discriminante

Rendere importabili **solo regioni HTML dichiarate** preservando il resto della sorgente, produrre una patch leggibile ed esercitare un secondo documento non MAIOS. Confrontare GrapesJS core su import/export soltanto quando serve a discriminare fedeltà e costo di adattamento. Il metodo e l'apprendimento restano nel [CURRENT della competenza](../../../competences/ux-ai/collaborative-communication-medium/meta-editor/CURRENT.md) e nella [GUIDE](../../../competences/ux-ai/collaborative-communication-medium/meta-editor/GUIDE.md).

**Licenza:** i file dell'esempio rientrano nell'ambito della directory `examples/collaborative-communication-medium` e del suo avviso MPL-2.0; copyright 2026 Graziano Guiducci. Il banco contiene solo dati sintetici.
