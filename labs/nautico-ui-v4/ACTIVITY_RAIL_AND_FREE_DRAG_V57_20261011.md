# K-UX-AI v5.7 — leggibilità, attività e origine del trascinamento

**11 ottobre 2026 · candidato nel branch `work/ux-ai-ui-library-20261008` · dominio Nautico sintetico.**

## Fonte e differenza

L'operatore osserva in Edge la Griglia v5.6. In modalità Libero, una scheda può apparire spostarsi da un punto diverso da quello in cui viene afferrata dopo aver cambiato focus. La sidebar Attività ha acquisito la possibilità di essere nascosta, ma ora due gestori indipendenti controllano visibilità e anteprime: la linguetta può sovrapporsi alle schede anche quando sono mostrate anteprime estese. Nei pannelli molti testi normali sono a 9–12 px. La richiesta è migliorare leggibilità e coerenza del gesto preservando l'architettura del medium neutrale.

L'ultima frase della fonte, «aprire la versione con anteprima solo con», è incompleta. La decisione locale e reversibile di questo candidato è **apertura delle anteprime estese solo tramite clic esplicito su “Anteprime”**; il passaggio del puntatore sul bordo richiama soltanto le icone. Questa scelta può essere corretta dalla continuazione della fonte, senza trattare parole mancanti come decisione già ricevuta.

## Cambiamenti del codice

- **Barra Attività:** tre stati semantici espliciti `hidden`, `icons` e `previews`. Il `peek` transitorio rappresenta soltanto le icone e ritorna a `hidden` all'uscita. Un pulsante interno fissa le icone; dal bordo è disponibile una linguetta cliccabile. Per ampliare a `previews` serve il clic sulla sola azione **Anteprime**. In quel caso la barra torna nel flusso dello spazio e prende la propria larghezza 255–395 px, evitando un overlay sulle card. La linguetta laterale non compare in anteprime estese. Si continua a usare il controller storico `mountSidebar`: nessun secondo deposito di dominio.
- **Gesto in Libero:** `startDrag` acquisisce al `pointerdown` il rettangolo renderizzato e la distanza del puntatore dal punto di presa *prima* di promuovere il focus o passare da griglia a Libero. I movimenti successivi derivano dal puntatore in coordinate dello stage, con conversione rispetto alla sua scala/zoom e limiti del viewport. I pannelli agganciati cambiano dimensione soltanto con origine sotto il gesto; il fullscreen conserva il proprio controller distinto.
- **Leggibilità:** testo normale di pannelli, spiegazioni, note di fonte, etichette e pulsanti piccoli aumenta generalmente di 1–2 px; corpo da 12 a 14 px sulle card desktop e a 13 px nei viewport stretti. Titoli `h1/h2/h3` non sono stati rimodellati. La sidebar con anteprime può scorrere; il comando per ridurla rimane sticky.

Non è stato rimosso CSS storico sulla base della sola ricerca statica: esistono più strati di override e stati responsive. La separazione dei moduli rimane un refactor ulteriore, non una condizione della correzione presente.

## Identità e prova

- Baseline invariata: [18-griglia-situated-v56.html](18-griglia-situated-v56.html), SHA256 `8bb3939c44ab46bdfe7fff14beea8b63f8ad07afa723bd595e423022dcc3c617`.
- Candidato: [19-griglia-rail-free-v57.html](19-griglia-rail-free-v57.html), SHA256 `e733a306b85f2ac3abefe20fa6801aa73b2b178e7c108b40d05bb07c5021db2d`.
- Builder source-bound: `python tools/build_nautico_v57.py --check`, richiede lo SHA esatto della v5.6 e confronta i byte della v5.7.
- Suite [nuova](../../tests/qa_nautico_v57.py): 124/124 controlli Chromium Playwright correlati; quattro viewport 1715/1280/768/390 e normale/reduced motion; controllati testo, rail hidden/icons/peek/previews, larghezze, focus/tastiera, assenza di linguetta nella forma estesa, trascinamento destro e successivo cambio focus in Libero, assenza di errori JS.
- [Regressione](../../tests/qa_nautico_v57_compat.py): 126/126 controlli di compatibilità adattati ai nomi del nuovo stato, fra Home, tour Canvas, 10 accessi, fullscreen, chat senza duplicati e cambio di contesto.
- Ricevute: [nuova](EVIDENCE_ACTIVITY_DRAG_TYPOGRAPHY_V57_20261011.json), [compatibilità](EVIDENCE_COMPATIBILITY_V57_20261011.json). Tre script embedded validati anche con `node --check`.

Queste verifiche sono correlate sullo stesso HTML caricato con Playwright `page.set_content`. **Non provano** esecuzione sull'Edge installato dell'operatore, navigazione reale `file://`, mouse/touch fisico, accessibilità integrale, persistenza fra riavvii, connessione LLM, account/permessi reali, Kernel Nautico installato o sito MAIOS pubblicato.

## Ritorno e prossimo rientro

La relazione riusabile di costruzione è: la geometria visualizzata e l'intenzione del gesto precedono la mutazione del focus; i tre stati della barra non possono derivare da due controller concorrenti. Code Medium Construction possiede il meccanismo di codice; Interaction Quality possiede orientamento, controllo e ritorno. Il comportamento demo non autorizza né simula nuove capacità del Nautico.

Il punto successivo è l'osservazione Edge della v5.7: trascinare una scheda da destra in modalità Libero dopo averne cambiato il focus; nascondere le attività, richiamarle dal bordo e fissare le icone; espandere/ridurre le anteprime; verificare la lettura di schede brevi e dense. Tornare a questo owner solo se l'osservazione espone differenze materiali.

Nessun merge, tag, release, cambio del package pubblico, aggiornamento di Kernel Nautico/maios.it o deploy viene effettuato da questa candidata.
