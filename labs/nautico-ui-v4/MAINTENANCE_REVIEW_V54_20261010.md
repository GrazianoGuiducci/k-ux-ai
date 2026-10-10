# K-UX-AI v5.4 — revisione di manutenzione e apertura ai moduli contestuali

Data: 10 ottobre 2026. Proprietà del risultato: `GrazianoGuiducci/k-ux-ai`.
Sorgente esaminata: [Griglia v5.4](15-griglia-focus-tour-tools.html), Git blob `a431c48c310f904f954804a9e6504c986b602d84`; branch `work/ux-ai-ui-library-20261008`, head letto prima del commit `dfaf6cd3762e859b9050b2084a5c5500f97eefa4`.
Ingresso: osservazione dell'operatore su Edge tramite due schermate + richiesta di audit di ottimizzazioni, residui e semplificazione. Semantica di K-UX-AI in [KERNEL.md](../../KERNEL.md); riferimento [Interaction Quality](https://github.com/GrazianoGuiducci/d-nd-ux-ai-seed/blob/main/design/skills/interaction-quality/SKILL.md) e Code Medium Construction nella propria sorgente privata.

**Tipo di prova: ispezione statica sorgente + confronto documentale e visivo.** Non è stata eseguita qui una nuova suite Chromium/Edge. I 334/334 controlli restano l'evidenza precedente riferita all'HTML esatto nel [receipt v5.4](EVIDENCE_FOCUS_TOUR_V54_20261010.json). Nessun controllo addizionale è dichiarato passato. Il file HTML, l'interfaccia e la sua identità di prova sono rimasti invariati.

## Risultante

Il prototipo soddisfa in modo sufficiente il passaggio Home/preparazione → canvas contestuale e offre ormai un percorso comprensibile di ingresso, navigazione, focus, disposizione e aiuto. L'operatore è sostanzialmente soddisfatto. Non emerge una ragione per un altro redesign generale o per aggiungere pulsanti per inerzia. Il prossimo movimento utile riguarda mantenibilità e regressioni mirate, distinto dalla futura ricezione di account/permessi reali.

## Osservazioni qualificate

### Rilevazioni esatte nel sorgente

1. **Indicatore diagnostico non aggiornato:** `window.KUXAIDemo.version` vale ancora `lab-2026-10-10-r5.1` nell'HTML v5.4. È metadato di debug; non è stato osservato un difetto funzionale. Una correzione dei byte HTML crea una nuova identità e richiede un receipt appropriato.
2. **Composizione ancora a strati:** l'HTML contiene circa 349 kB, tre blocchi `style` e tre `script`. Una scansione testuale trova 207 selettori CSS ripetuti (anche in contesti responsive, quindi *non* 207 difetti). La leggibilità e l'isolamento delle revisioni costituiscono il costo principale; consolidare soltanto su un nuovo candidato verificato.
3. **Possibili residui CSS:** le classi `case-symbol`, `drop-arrow`, `work-heading`, `chip-button`, `off` (in `.status-chip.off`), `progress-track`, `stage-steps`, `avatar-preview-trigger`, `kux-primary-context`, `kux-tools-layout` appaiono nei blocchi di stile ma non come token nel resto dell'HTML/JS. È un rilevamento statico, non prova definitiva di inutilizzo dinamico; rimuoverle solo dopo readback del DOM e regressioni di viewport.
4. **Funzioni JS:** sono state identificate 137 dichiarazioni nominate distinte; nessuna compare una sola volta nella sorgente complessiva. Questo **non dimostra** raggiungibilità runtime né assenza di rami dormienti. Il vecchio `#contextSelect`, per esempio, è nascosto intenzionalmente come ancora di compatibilità: non va rimosso perché non visibile.
5. **Riproducibilità fonte/versione:** la [ricevuta](EVIDENCE_FOCUS_TOUR_V54_20261010.json) attesta builder `build_v54.py` e suite QA nel pacchetto ZIP dell'operatore. Nelle directory GitHub esaminate (`labs/nautico-ui-v4/`, `tools/`, `tests/`) tali file specifici non risultano presenti; il ramo conserva invece l'HTML e il receipt. Raggiungere o ricollocare i sorgenti di build/test prima di un refactor, preservando base hash-guarded e identità della prova.

### Comportamenti da esercitare prima di chiamarli bug

6. **Ingresso e layout:** `activateScreen('home')` conserva `state.contextViews[...]`, ma `enterPreparedField()` riassegna `state.layout='auto'` e `contextViews[context]={layout:'auto',locked:false}`. È necessario verificare con l'operatore se `Entra nel campo` debba sempre preparare una vista adattiva oppure recuperare la disposizione scelta per quel contesto. Entrambe sono semantiche possibili, non risolvere la differenza come refactor accidentale.
7. **Input durante aggiornamenti:** `refreshModules()` richiama `renderModule(p)`, che sostituisce `body.innerHTML`. I valori delle bozze vengono reidratati da `state.drafts`, ma non risulta ripristino specifico di focus/caret/selezione del campo durante questa ricostruzione. Verificare digitazione in corso + nuovo evento demo: la persistenza del *valore* non equivale alla continuità del gesto.
8. **Reset e preferenze:** `resetSession` azzera gli stati demo di lavoro, mentre i piani Home hanno un deposito `localStorage` distinto. Chiarire in etichetta/contratto se il reset riguarda solo la sessione operativa o anche le preferenze preparative.

## Apertura al futuro ricevente multi-attore

Questa Griglia è una proiezione sintetica con cinque contesti e un catalogo locale di intenti; non contiene autenticazione né controllo di autorizzazioni reali. `role` nel vecchio codice indica spesso **ruolo geometrico** della card (principal/medium/small), non ruolo aziendale. Non confondere le due identità.

Progettisti, cantiere, fornitori, assistenza e clienti possono condividere un medium e ricevere card pertinenti al proprio lavoro. La generazione non deve ridursi a una tabella fissa `ruolo → schermata`. Quando Kernel Nautico e host forniranno realmente identità dell'attore, oggetto/contesto, fonte/revisione, capacità disponibili, azioni ammesse e ricevute d'effetto, K-UX-AI potrà comporre moduli con quella base. L'owner del dominio autorizza l'azione; la UI rende disponibili e comprensibili i gesti; il ricevente effettua e registra gli effetti. Nascondere un controllo non è autorizzazione.

Il `localStorage` della demo attuale non è segregato per account. Prima di ricevere dati o persone autentiche servono separazione di preferenze/draft per attore e progetto nel receiver, e un controller che ricontrolli i permessi ad ogni azione. Identità semantica della card, sorgente e capacità applicabili precedono la morphology. Nessuna UI multi-utente, autenticazione o card generata dall'AI è stata implementata con questa revisione.

## Prossimo movimento proporzionale

- **Prima verifica comportamentale**: Edge/Chromium su `Home → layout manuale → Home → Entra`, digitazione attiva + `Simula evento`, reset sessione/preparazione, zoom e tab focus. Produrre un receipt separato con l'identità del file realmente esercitato.
- **Poi igiene sorgente**: ricondurre builder e controlli portabili al branch; introdurre sorgenti modulari e build deterministica lasciando la v5.4 validata come riferimento; qualificare i CSS effettivamente morti e il metadato debug nella nuova candidata. Nessun refactor obbligatorio finché queste azioni non cambiano il risultato.
- **Solo su integrazione reale selezionata**: risolvere owner Nautico, attore/account, permessi, proiezione dei moduli e readback tramite un contratto sorgente/autorizzazione verificato. Una futura capacità generativa non concede permessi, non implica codice arbitrario eseguibile e non apre automaticamente una release.

**Effetti di questo passaggio:** solo nota documentale source-bound e collegamento di reentry nel branch candidato. Nessun cambiamento all'HTML v5.4, API `createMedium`, Nautico, `main`, package, permessi, sito, deploy, release o automazione.
