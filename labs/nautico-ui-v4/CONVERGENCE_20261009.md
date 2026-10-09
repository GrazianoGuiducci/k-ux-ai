# K-UX-AI · v4.6 Convergenza
9 ottobre 2026 · prototipo autonomo candidato · non pubblicato.

## Movimento selezionato
Dall'osservazione dell'operatore sul campo focale v4.5: sidebar collassata con avatar e sidebar estesa con schede/preview trascinabili; divisione regolabile fra principale e complementari; chat generale contestualizzata e chat in ogni scheda; contributi candidati a competenza con fonte e contesto; Presentare con FORM/BUILD/LIVE/RETURN e spiegazione di Kernel/UI; rinominare «Piccola» in «Media affiancata». Evitare sovrapposizione di controller, una nuova stratificazione di legacy o falsa assimilazione di competenze.

## Candidato implementato
[Apri l'HTML](07-griglia-convergenza.html). Estrazione del nuovo comportamento in [convergence.js](source-v46/convergence.js) (sidebar, divisore, dialoghi locali e registro candidati) e [convergence.css](source-v46/convergence.css) (layout, split, responsive, percezione e presentazione). Entrambi sono incorporati nel bundle HTML consegnato. Il pacchetto ZIP fornito con il risultato comprende inoltre builder originale, baseline v4.5 immutata, suite Playwright e screenshot: il solo sorgente JS/CSS di questa directory non rigenera autonomamente il legacy. La v4.5 resta conservata.

L'avatar è un ingresso percettivo, **non** un owner di competenza automaticamente costituito. Un messaggio locale produce una lettura deterministica della sorgente sintetica, non inferenza di AI; «candidato» non significa competenza formata, esercitata o assimilata. Il packet JSON richiede un receiver e un owner esterni prima di qualunque effetto reale. Non è connesso il filesystem PC/Codex, un backend AI, un vero Section Kernel o un evento operativo di Kernel Nautico. K-UX-AI non trasferisce autorità dal controller del dominio alla UI.

La sidebar adatta il **comportamento** già presente nel Nautico `main@82896de01829752614d04cfa6e3ffacbd9544a0a` `product-navigation.js/css`, senza copiarne API o codice. La card Presentare è una prima illustrazione dinamica propria; non sostituisce la presentazione tridimensionale posseduta da Nautico. La topologia Nautico resta federata: dominio, azienda, progetto e imbarcazione mantengono identità distinte.

## Prova e stop
[Receipt](EVIDENCE_CONVERGENCE_20261009.json): **64/64 + 30/30** controlli Chromium/Playwright correlati sul bundle esatto Git blob `39cdf482ec810437b79aa16d6e39a6653c1f8f87`, SHA256 `6ac5ac378e7cb06b8756e31aeec91a7b5c51616cedd407b658f586c08cca2574`. Nessun JS page error nei percorsi osservati. Il browser di test non apre `file://`, dunque test tramite `page.set_content`. Edge dell'operatore, reale touchscreen/assistive tech, sincronizzazione file, inferenza AI e uso aziendale restano non verificati.

Successivo: osservazione dell'operatore in Edge. Eventuale integrazione con le sorgenti Nautico e promozione di apprendimento richiede un separato movimento owner-native con capacità e autorità effettive. Nessun merge, release o deploy.
