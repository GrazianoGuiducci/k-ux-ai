# K-UX-AI v4.9 — Campo evolutivo: Home, avatar, colonne e Libero

9 ottobre 2026 · owner del prototipo GrazianoGuiducci/k-ux-ai · branch di lavoro privato rispetto alla release. Prima vertical Nautico con stato sintetico.

## Osservazione diretta e nuovo movimento

L'operatore ha evidenziato quattro difetti materiali nella v4.8: Home con vaste celle inutilizzate e drag che riordina soltanto; comandi Contesto/Azione da rendere più riconoscibili; click su avatar aperto che deve consentire chiusura con doppia conferma; sidebar che perde altezza per Chat e Home separati; dividers incompleti fra colonne; Libero con possibile conflitto fra ridimensionamento e successivo posizionamento.

## Comportamento implementato nel file autonomo

- [10-griglia-campo-evolutivo.html](10-griglia-campo-evolutivo.html) riempie la Home con una mappa deterministica senza celle interne mancanti: 12×3 nel desktop ampio, 8×6 o 4×6 nei frame intermedi, 2×6 su mobile. Dieci accessi restano presenti. Trascinare *Controllare* su *Capire* promuove **Controllare a tessera principale della Home**. Non simula l'avvio del lavoro: *Entra* rimane un effetto separato. Shift+Enter su tessera ne promuove il ruolo; Alt+frecce permette riordino da tastiera.
- Nella sidebar il primo click sull'avatar inattivo apre una scheda; il primo click su un avatar già aperto arma la chiusura e il secondo click ravvicinato la conferma. La chiusura riguarda il pannello del medium, non gli oggetti o le fonti Nautico. *Porta al centro* rimane il controllo esplicito per cambiare focus fra schede presenti.
- Chat e Home formano una sola fascia inferiore nella sidebar, fuori dall'unico scroller di avatar. Contesto attivo precede Azione nel primo piano dell'header; non è stato introdotto uno stato contestuale duplicato. Sul mobile la Home non mostra comandi da workspace e i controlli restano nel viewport.
- Una maniglia regola il confine principale/medie nel campo Adatta; se le medie sono affiancate compare una seconda maniglia fra le due colonne. Le modalità manuali a due/tre colonne dispongono di una/due maniglie indipendenti **solo quando i minimi di larghezza consentono davvero quelle colonne**. La divisione delle medie dispari fa occupare l'intera ultima riga all'ultima scheda.
- In Libero il resize CSS nativo concorrente è disattivato: soltanto la maniglia esplicita possiede dimensioni e ritocco. Il drag della testata sposta senza alterare w/h. I rientri dalla griglia recuperano la geometria manuale, e aprire/chiudere altre finestre non provoca riorganizzazione automatica delle finestre libere.

## Codice, prova, confini

La revisione riscrive i punti pertinenti nel codice della v4.8 con patch sorgente verificabili; **non carica un altro controller runtime sovrapposto**. Il [pacchetto v4.9 consegnato all'operatore] contiene `build_v49.py`, baseline byte-identica v4.8, CSS aggiuntivo, suite e immagini. La base è ancora parzialmente monolitica: il refactor completo resta una trasformazione distinta nel ricevente K-UX-AI/Nautico, non un risultato rivendicato oggi.

HTML Git blob `bd85631db3bfe8e25333f1dcf684db2989a4d22a`; SHA256 `8448c1eb8bd2a76237ebb66763535b40e0fe223baa65521e8013f1de3d978d8e`.

[Evidenza distinta](EVIDENCE_CAMPO_EVOLUTIVO_20261009.json): Playwright Chromium `page.set_content`, 53/53 + 39/39 test correlati e 2/2 smoke normale-motion, zero page errors nei percorsi osservati. `localStorage` era negato nell'host del test: persistenza inter-sessione best effort non verificata; Edge `file://`, touch e tecnologia assistiva reali, LLM/provider, state/eventi Nautico e assimilazione competenze non provati.

Un'interfaccia non costituisce un Section Kernel, non qualifica un dato industriale né possiede gli effetti; i controlli cambiano proiezione/focus. Nessun merge, release, deploy o scrittura in Kernel Nautico.

**Prossimo movimento:** osservazione Edge della v4.9. Le carenze che emergeranno potranno cambiare le competenze pertinenti senza reintrodurre nuove stratificazioni.
