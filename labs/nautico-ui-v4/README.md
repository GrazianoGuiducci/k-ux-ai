# K-UX-AI · Griglia del fare v4 — assistente modulare

## 9 ottobre 2026 — v4.8 Contesto e Focus stabili

[HTML autonomo](09-griglia-contesto-focus.html) · [sorgente/decisioni](CONTEXT_FOCUS_20261009.md) · [prove attribuite](EVIDENCE_CONTEXT_FOCUS_20261009.json) · [moduli della composizione](source-v48/). Divisore centrale stabile sul tap, drag con isteresi di pairing e allineamento al bordo delle medie anche con assistente dock; avatar già aperto senza hover peek duplicato e click ripetuto idempotente; uno scroller degli avatar; **Contesto → Azione** sempre visibili in testata, incluso mobile.

100+97+51 = 248 check Chromium correlati, zero errori JS osservati. Builder e suite riproducibili nel pacchetto della conversazione. Nessuna AI reale, data-source Nautico, merge/release/deploy. La v4.7 e le prove precedenti restano intatte.

## 9 ottobre 2026 — v4.7 Sidebar + Medie affiancate

[Apri HTML](08-griglia-campo-medie.html) · [metodo, significato e orizzonte artefatti](FIELD_AND_RESPONSE_MEDIUM_20261009.md) · [ricevuta](EVIDENCE_FIELD_20261009.json) · [JS/CSS](source-v47/). La barra chiusa è larga 86px, con icone distanziate e anteprima solo su hover; quella aperta contiene già preview scorrevoli e non apre un ulteriore popup dagli avatar. La mappa tratta le medie come un solo settore; affianca due card solo con larghezza adeguata o le impila conservando lo scroll. Divisore 27–60%.

148/148 controlli Chromium **correlati**, nessun errore JS osservato, senza AI o Nautico live. Costruzione fail-closed riproducibile nel pacchetto ZIP consegnato; HTML v4.6 e precedenti conservati. Nessun merge, release, deploy.

## Candidato 9 ottobre — v4.6 Convergenza

[Prototipo v4.6](07-griglia-convergenza.html) · [contratto e confini](CONVERGENCE_20261009.md) · [receipt](EVIDENCE_CONVERGENCE_20261009.json) · [nuovi moduli](source-v46/). Chat per scheda e chat generale **dimostrative**, barra avatar espandibile, divisore principale/complementari, card Presentare e Media affiancata. Build/test riproducibili nel pacchetto dell'interazione, non un provider live. 64/64 + 30/30 test correlati. Nessun merge, deploy, Nautico o MAIOS modificato.


## Griglia v4.5 — 9 ottobre 2026 · campo focale e avatar diretti

[Apri il candidato autonomo](06-griglia-campo-focale.html) e [leggi il contratto situato](FOCAL_FIELD_20261009.md) con [ricevuta](EVIDENCE_FOCAL_FIELD_20261009.json). Questa revisione risponde all'osservazione dell'operatore sulla v4.4; le versioni precedenti e le loro ricevute restano intatte.

La barra avatar è ridimensionabile con maniglia e frecce (62–150 px). **Hover** sull'avatar apre direttamente una anteprima non invasiva, senza pulsante mini; **click** lo porta nel ruolo principale e sposta la scheda precedente nella colonna delle complementari, anche con Mantieni focus attivo (gesto esplicito); **drag** dispone la scheda nel campo o riorganizza le secondarie. La disposizione normale è composta da **una scheda principale + una colonna secondaria scorrevole**, dentro due aree operative oltre agli avatar. Solo quando il frame secondario è adeguato e ci sono almeno due complementari, una modalità Veloce può affiancarle. Mobile: sequenza principale → secondarie in normale flusso verticale, senza sovrapposizioni di contenuto.

Le icone delle card sono state esercitate per sezione, anteprima, compatta, full/ritorno, riduci, chiudi, Porta al centro e dock in Libero. La loro disponibilità non conferisce autorità di dominio. Il readback `KUXAIDemo.perception().view` espone geometria concettuale/focus/peek per osservazione, non una AI live.

La suite locale (Playwright Chromium, `page.set_content`) registra **74/74 + 32/32 + 17/17 = 123/123 controlli correlati** e zero errori JavaScript di pagina osservati. Test e screenshot riproducibili sono nel pacchetto consegnato nel turno; non costituiscono prova di Edge fisico, interazione touch reale, assistive technology, kernel Nautico collegato o rilascio pubblico. Nessun merge, deploy o modifica di `src/medium.js` eseguita.


## 9 ottobre 2026 — Griglia del fare v4.4, ruoli e ambiente di sezione

**Candidato successivo alla v4.3**, conservando tutte le precedenti versioni. [Apri il nuovo HTML](05-griglia-ecosistemi-smart-slots.html) e leggi [dinamiche, significato, limiti e sezione](SMART_GRID_SECTION_ECOSYSTEM_20261009.md) e la [ricevuta](EVIDENCE_SMART_GRID_20261009.json).

La mappa (▦) dell'avatar rende raggiungibili Grande/Media/Piccola; un click semplice aggiunge l'attività come complemento quando è attivo Mantieni focus. Il drag in griglia assegna lo slot senza sganciare l'intero campo; le altre card restano scrollabili. La quick preview ora consente spostamento e resize reali. Le transizioni strutturali hanno durata indicativa 750 ms, mentre la manipolazione diretta segue il puntatore. L'ambiente interno della card (◇) comprende quadro/fonti/conversazione/collegamenti, ma conserva solo note demo: nessuna AI o Section Kernel operativo è montato.

59/59 controlli Playwright Chromium correlati su tre suite con dati locali e zero page errors nei casi osservati; non è prova di Edge, touch fisico, source Nautico live o agenti AI. Codice pubblico, `src/medium.js`, Kernel Nautico e MAIOS Site non modificati. Nessun rilascio o merge.


## Griglia del fare v4.3 — focus, anteprime e riorganizzazione, 9 ottobre 2026

[Apri la **v4.3 Focus dinamico**](04-griglia-focus-dinamico.html), candidato HTML autonomo originato dalle quattro schermate e dalla nuova richiesta dell'operatore. La [fonte del comportamento](FOCUS_COMPOSITION_20261009.md) e [la ricevuta](EVIDENCE_FOCUS_20261009.json) conservano le distinzioni esercitate.

Il nuovo *campo operativo* interpreta **aprire**, **leggere in anteprima**, **promuovere a focus** e **pagina intera** come azioni differenti:
- 1 attività: occupa il campo. 2: dividono il campo. 3 o 4: la principale riceve più spazio, le altre restano consultabili. 5+: campo scorrevole, principale riconoscibile, le altre non scompaiono. Le modalità scelte 2/3/4 e Libero restano disponibili e soggette allo spazio reale.
- **Mantieni focus** protegge il principale dalle aperture ordinarie, ma un'esplicita selezione dal menu focus o "Porta al centro" può cambiarlo.
- **Anteprima** è un livello di sola lettura che mostra informazioni e notifiche della demo; non apre un'attività, non cambia il controller e non prende il focus. Nel picker "Aggiungi" e accanto agli avatar si può scegliere senza aprire.
- **Ricomponi** riporta alla disposizione adattiva senza minimizzare le attività, perdere input locali o sostituire la geometria manuale salvata per Libero.
- La pagina intera prende temporaneamente la precedenza e ripristina il focus precedente quando termina; la chiusura di una scheda secondaria non sottrae il focus bloccato.
- Le card libere usano una maniglia esplicita con lo stesso aspetto e cursore diagonale della Window Surface/Chat. Nella griglia, la misura della card appartiene al layout anziché a una maniglia inefficace. Un semplice click sull'intestazione non porta più la griglia in Libero: il trascinamento richiede un gesto misurabile.

[Verifiche](EVIDENCE_FOCUS_20261009.json): 160/160 controlli di comportamento e 66/66 controlli aggiuntivi multi-card, correlati sullo stesso HTML e tramite `page.set_content`. Sono prove locali sintetiche; nessuna compatibilità con touchscreen fisici/tecnologie assistive, eventi owner-native Nautico, AI remota o MAIOS deploy è attestata.

Le versioni v4.0–v4.2 e relative ricevute rimangono intatte, così come `src/ui/window-surface.js` e il contratto pubblico `src/medium.js`. La v4.3 è una candidata privata, non una release.


## Griglia v4.2 — workspace adattivo, 8 ottobre 2026

**Nuovo esercizio selezionato dall'osservazione dell'operatore**: nelle schermate originali la griglia non rendeva usabili insieme le card su mobile, il menu Strumenti poteva essere coperto, le disposizioni numeriche sovrapponevano o minimizzavano card, mancavano tre colonne e le barre/attività laterali occupavano spazio utile.

- [Apri Griglia v4.2 responsiva](03-griglia-responsive-workspace.html) — HTML autonomo con le funzioni demo originali e il componente K-UX-AI Chat/Form della v4.1 conservato.
- [Decisioni di composizione](RESPONSIVE_DESIGN_20261008.md) — sorgente del difetto, separazione fra disposizione e attività, comportamento desktop/mobile e confini.
- [Ricevuta v4.2](EVIDENCE_RESPONSIVE_20261008.json) — due suite locali correlate, 121/121 controlli responsive su sei dimensioni/condizioni e 19/19 controlli di continuità, zero page error nelle prove. Prove effettuate tramite `page.set_content`; nel receiver di test `file://` è bloccato dall'ambiente, quindi la navigazione locale reale non è attestata.

La nuova modalità **Adatta** è il punto d'ingresso iniziale; sono disponibili anche Libero, 2, 3 e 4. In griglia tutte le attività restano disponibili e il campo scorre senza un tetto artificiale di 2/4 card. **Libero** conserva la geometria scelta manualmente. Sotto spazio ridotto le card diventano una colonna scorrevole e gli avatar laterali lasciano posto all'assistente accessibile nella barra. Focus e contesto sono raggiungibili da un menu a discesa. La versione v4 originale, la v4.1 motion-parity e le relative ricevute restano immutate.

La v4.2 è un laboratorio locale sintetico, non un evento owner-native collegato al Kernel Nautico, non un modello AI attivo, non una release né una distribuzione MAIOS.


## Rientro 8 ottobre — v4.1 motion parity, candidata locale

L'HTML originale [01](01-griglia-chat-window-surface.html) e la sua ricevuta storica [EVIDENCE.json](EVIDENCE.json) restano invariati.
Il nuovo [02 — Griglia v4.1, motion parity](02-griglia-chat-window-surface-motion-parity.html) incorpora la correzione anche della sorgente condivisa [Window Surface](../../src/ui/window-surface.js).

**Differenza:** `minimize()` cattura il token di movimento *dopo* avere avviato `avatarToWindow(false)`. Prima, nella modalità `prefers-reduced-motion` (o senza Web Animations), il movimento non incrementava il token: la chiusura era scartata, il frame restava aperto e l'avviso non raggiungeva l'avatar.

[Nuova ricevuta mirata](EVIDENCE_MOTION_PARITY_20261008.json): sul file precedente 11/13 controlli in reduced-motion (due controesempi); sul candidato 13/13 in reduced-motion e 13/13 in movimento normale, zero errori di pagina nei due percorsi nuovi. I controlli sono correlati e non sostituiscono i 93 precedenti; nessuna prova di AI live, evento Nautico reale, accessibilità completa o integrazione Site.


**8 ottobre 2026 · PROTOTYPE_INTEGRATED_SYNTHETIC / non pubblicato**

## Apri il prototipo

[Griglia del fare con Window Surface e Chat/Form](01-griglia-chat-window-surface.html).

Si tratta di **un solo HTML autonomo** che riutilizza il codice originale K-UX-AI `src/ui/window-surface.js`, `src/ui/chat-form-module.js` e `src/medium.js`, incorporati in una versione da osservare offline. Non installa THIA, non invoca API, non usa dati del Nautico reale e non sostituisce il Site MAIOS.

## Differenza dalla v3

La v3 disponeva di un pannello "Assistente" come un'altra scheda del proprio sistema locale. La v4 lascia inalterate le altre attività e fa passare **tutti gli ingressi di assistenza** attraverso **un unico componente Window Surface** con modulo Chat/Form separato.

Lo stesso assistente può essere:
- avatar chiuso nella Home o nel dock delle attività;
- finestra libera, spostabile/ridimensionabile;
- sidebar sinistra/destra che **fa spazio** al canvas;
- superficie a pagina intera;
- Chat/Form affiancati, oppure tab Chat e tab Modulo quando la **larghezza del frame** non basta.

Nel passaggio `full -> floating` il sistema conserva la bozza e **trasferisce il focus** al comando ancora visibile quando quello usato scompare. In `minimize -> avatar` il focus torna a un punto raggiungibile e il contenuto rimane vivo.

## Provalo in questa sequenza

1. Apri la **Griglia** e scegli una voce d'intento. Le altre attività restano nel layout v3 originale.
2. Nel campo, apri l'avatar assistente dalla colonna sinistra. **Al primo ingresso di lavoro** è suggerito un dock a destra, che lascia spazio al canvas; puoi tornare alla finestra libera.
3. Apri `Modulo`, inizia un testo e passa a **Pagina intera**. Rientra con il comando o con **Escape**: la bozza resta.
4. Riduci ad avatar, riapri, registra una traccia locale. Il controller del laboratorio aggiorna il proprio registro con identità e origine, ma **non invia nulla fuori dal browser**.
5. Riduci ancora, scegli **Simula variazione** e usa la barra di evento. Soltanto accettando `Componi 2 schede` il campo adotta quella disposizione; al ritorno alla Home l'avatar può segnalare un evento ancora da esaminare.
6. Prova il passaggio mobile e torna su desktop. La geometria manuale non deve essere sostituita dalla forma temporanea richiesta su schermo stretto.

## Confini e implementazione

```text
v3 domain demonstrator state (synthetic Nautico context)
    ↕ local K-UX-AI createMedium receive/dispatch/observe
reusable Window Surface (presentation/geometry/focus)
    ↕
reusable Chat/Form module (unsent draft, local question, receipt)
```

`createMedium()` conserva la direzione di ritorno delle azioni: `dispatch()` da solo non approva nulla; il controller locale decide se registrare una nota e genera l'evento che viene poi restituito a `receive()`. Questa è una prova di composizione del mezzo, **non** una connessione al Kernel Nautico operativo.

Alcune parti storiche `panelContents('chat')` rimangono nel grande HTML v3, ma `openPanel('chat')` nella v4 usa il componente riutilizzabile e non crea più una card di chat duplicata. Potranno essere eliminate durante la futura migrazione dal laboratorio a un bundle modulare, evitando di ricostruire l'intero canvas in questa formazione.

L'assistente dispone di due comandi cognitivi distinti: quando è chiuso, `notify({id,text})` riceve solo eventi di prova identificati; quando è aperto, una nuova attività può diventare un messaggio di stato. Le comunicazioni rimangono **etichette dimostrative**, non inferenze autonome di un modello.

## Qualifica e prove

Leggi [EVIDENCE.json](EVIDENCE.json) per le ricevute esatte: **28/28 + 28/28** controlli sul prototipo integrato e **23/23 + 14/14** sullo stesso componente riutilizzabile. Sono suite correlate e non attestano comprensione umana o comportamento di un prodotto installato.

I difetti osservati durante questo passaggio e corretti:
- il click dell'avatar bypassava la politica host di docking iniziale;
- in full-page si nascondeva il bottone sotto il focus, impedendo a Escape di operare;
- un avviso sospeso non ritornava all'avatar una volta rientrati alla Home.

### Non verificato

- chat MAIOS reale, autenticazione, destinatari e API THIA/DOMUS;
- continuità del caso su server/Nautico e stato di impianti;
- agenti AI, DSH/Codex/ChatGPT runtime;
- simultaneità di più pannelli di **dominio** scrivibili;
- assistive technology e utenti esterni;
- inserimento nel Site e pubblicazione.

## Per il prossimo rientro

Parti da [CURRENT del cabinet](../../docs/ui-library/CURRENT.md), dal [contratto delle superfici](../../docs/ui-library/OPERATING_CONTRACT.md) e dalla [sorgente owner-native del Kernel Nautico](https://github.com/GrazianoGuiducci/kernel-nautico). Non migliorare la superficie per inerzia: usa una situazione realmente cambiata nel dominio per comprendere se la prossima capacità da formare è la comunicazione con il kernel, una diversa percezione o una nuova operazione.

Questa lane resta privata. Nessun merge, deploy o incarico a Codex Site è implicito nel suo stato.
