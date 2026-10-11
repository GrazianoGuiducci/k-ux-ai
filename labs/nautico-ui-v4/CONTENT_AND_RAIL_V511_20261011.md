# K-UX-AI v5.11 — gerarchia operativa, stato della barra e tempo delle aperture

11 ottobre 2026 · candidata nel ramo `work/ux-ai-ui-library-20261008` di `GrazianoGuiducci/k-ux-ai`.

## Sorgente della differenza

L'operatore osserva in Edge la v5.10.1. Il ritorno non chiede soltanto una nuova intestazione: segnala l'ordine di lettura **dentro** le schede. Un lungo testo «Azione nella scheda…», una seconda riga «DATI DIMOSTRATIVI…» e poi sezione, titolo e descrizione fanno perdere il referente nel lavoro. Chiede inoltre che l'intestazione porti il testo su un'unica riga accanto all'icona dove possibile; che l'icona Attività si disattivi sempre quando una scheda viene chiusa con doppio clic; che il richiamo dal bordo abbia movimento lento e diretto; e che le aperture rimaste sotto 750 ms siano qualificate e corrette.

La fonte attuale è il prototipo sintetico, non il sito MAIOS né i dati del Kernel Nautico reale. La v5.10.1 rimane invariata, con sorgente SHA-256 `e448bd07dc406a68932e90ff220acc7b509a287cd8b91e9742593794849d6004`.

## Nuova risultante

- **Lettura del contenuto:** all'inizio della scheda rimangono la categoria semantica («DOMANDA PRESENTE», «RISCONTRO E CRITERI», ecc.), il titolo e la descrizione quando prevista. L'origine illustrativa viene resa da **una sola** riga compatta `DATI DIMOSTRATIVI · KN/…` che apre «Fonte e limiti». Il testo lungo è ancora recuperabile nello stesso oggetto; non è cancellato, trasformato in fonte reale o sostituito con prova che non possiede. I contenuti del caso, check, bozze e azioni restano proprietari della stessa sessione.
- **Intestazione:** icona, contesto, azione e nome funzionale scorrono in una sola riga, con troncamento e `title` quando lo spazio è insufficiente. Nelle schede strette resta riconoscibile l'azione; il vero titolo del lavoro resta nel contenuto. I sei comandi operativi conservano posizione, etichette e comportamento. La presentazione CSS non determina autorità sul dominio.
- **Doppio clic Attività:** il vecchio `closePanel` aggiorna correttamente stato e schede, ma non invocava sempre `renderDock` se rimaneva una scheda focalizzata differente. L'icona relativa a una scheda non focalizzata poteva restare `data-active=true`. Ora il pending close relativo viene invalidato e `renderDock()` / `updateHeader()` vengono applicati dopo la mutazione, indipendentemente dal percorso di focus. Non basta che la scheda sparisca: anche il comando che la rappresenta deve essere derivato dallo stesso stato.
- **Riattivazione della barra:** il passaggio `hidden/peek/icons` prima esponeva immediatamente la barra perché cambiava `position` da fixed (anteprima) a flow (icone). La v5.11 anima il proprio ingresso con `clip-path`, opacità e provenienza da sinistra per **860 ms** (normale movimento); il click continua a determinare subito il nuovo stato semantico. Non sono introdotti altri controller permanenti.
- **Aperture:** `geometryMotion` dell'assistente, contenuto del tour e riposizionamento delle tessere Home che erano ancora a 390/240/440 ms passano rispettivamente a 840/780/800 ms; ingresso delle anteprime Attività a 800 ms al posto di 290; menu Contesto, menu Focus, anteprima Quick Peek e dialoghi disponibili ricevono un ingresso situato di 800 ms. Il menu Strumenti mantiene 750 ms e i movimenti card / chat già sono a 750 ms. Il feedback hover non viene equiparato automaticamente all'apertura di una superficie. Quando l'utente richiede movimento ridotto, lo stato finale resta accessibile senza animazione decorativa.

## Sorgente esatta e prove

- [HTML candidato](24-griglia-content-hierarchy-v511.html): SHA-256 `67e8a1104d2abd66b886fad5354753a4db8964321c93947937de15f1917f434a`; Git blob `9a711dc02f8ff64d346415ca086aac54b991b98b`.
- [Builder deterministico](../../tools/build_nautico_v511.py): richiede la v5.10.1 esatta, applica sostituzioni puntuali e CSS originale in [kux_card_rail_v511.css](../../tools/kux_card_rail_v511.css); `python tools/build_nautico_v511.py --check` legge la candidata e ne verifica i byte.
- [QA contenuto e controllo](../../tests/qa_nautico_v511.py): [65/65](EVIDENCE_CONTENT_RAIL_V511_20261011.json), quattro viewport (1715, 1366, 768, 390), movimento normale e ridotto, chiusura di una scheda **non focalizzata** e icona disattivata, ordine semantico, fonte espandibile, barra e zero errori JS osservati.
- [QA tempi](../../tests/qa_motion_v511.py): [9/9](EVIDENCE_OPENING_MOTION_V511_20261011.json), durate letto dal browser su menu Contesto, Strumenti, picker, riapertura della barra e stato senza movimento.
- [Regressione Home](../../tests/qa_home_compat_v511.py): [67/67](EVIDENCE_HOME_COMPAT_V511_20261011.json), stessi sette viewport della QA v5.10.1, proporzioni e accessibilità dei controlli nelle tessere conservati.
- I **quattro script embedded** passano `node --check` sul nuovo HTML. Le prove Playwright Chromium usano `page.set_content`, non la URL pubblica, Edge installato, API Nautico, credenziali o un modello AI collegato. Le verifiche delle tre suite si riferiscono allo stesso HTML e sono correlate.

## Soglie e seguito

La fascia di 750 ms si riferisce alle aperture percettive in condizioni di movimento ordinario: non impone inerzia a input, tastiera, click, conferme o preferenza `prefers-reduced-motion`. L'origine/provenienza conserva il proprio significato di demo e rimane raggiungibile; una riga più compatta non la trasforma in fonte aziendale. La prima osservazione visiva su Edge dell'operatore resta necessaria per valutare qualità percepita con layout diversi.

**Stop condition:** candidata verificata e documentata nel solo ramo K-UX-AI. La v5.10.1, `main`, package pubblico, Kernel Nautico, sito MAIOS, account, provider, deployment e pubblicazioni non sono modificati da questo esercizio.
