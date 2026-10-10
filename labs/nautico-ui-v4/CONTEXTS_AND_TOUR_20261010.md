# K-UX-AI v5.2 — preparazioni per contesto, tour situato e geometria delle medie

10 ottobre 2026 · owner `GrazianoGuiducci/k-ux-ai` · solo branch `work/ux-ai-ui-library-20261008` · candidato di laboratorio Nautico sintetico.

## Fonte dell'operatore e differenza

Quattro screenshot Edge della v5.1 mostrano il tour modal centrato che copre la Home, una X da centrare, messaggi da rendere esplicitamente contestuali/causali e leggibili, preparazioni delle attività che scompaiono cambiando contesto, una maniglia tra medie centrata solo sulla prima scheda e piccoli margini/disallineamenti nelle card.

La causa delle preparazioni perse è precisa: `state.homeSelected` era un unico insieme e veniva ricostruito dai pannelli aperti quando si cambiava contesto o si rientrava nella Home. Questo sostituiva la **preparazione dell'operatore** con lo **stato transitorio dei pannelli**. La v5.2 introduce `homePlans` distinti per i cinque contesti, ciascuno con attività selezionate, ordine e ruolo principale; il contesto corrente recupera il proprio piano. Quando il browser lo consente, il piano usa `localStorage` `kux:home-prepared-contexts:v1`; altrimenti mantiene continuità in memoria nella sessione. Le attività non vengono approvate o eseguite da questa configurazione.

La guida Home mantiene i tre passaggi già validi ma non usa più `showModal()` né un backdrop che nasconde ciò che spiega. Il dialogo **non modale** viene disposto accanto alla sorgente reale di ciascun passaggio: scelta del contesto, tessera selezionabile, condizione d'ingresso. Il referente ha outline riconoscibile e resta raggiungibile. Ogni spiegazione distingue **ambito**, **quando serve**, **conseguenza**; non attribuisce fatti a Nautico e non crea un effetto. X centrata (bersaglio 40px), chiusura Escape/Concludi e ritorno del focus all'apertura. Il riquadro si riposiziona con resize e scroll, sostiene lettura ingrandita simulata tramite CSS zoom dal 100% al 200% e usa scroll interno per i testi lunghi; queste prove non sostituiscono un audit reale con persone ipovedenti/AT.

Nel settore Medie affiancate, il secondo divisore si centra sui bounds delle righe **effettivamente divise**. Per un numero pari di card complementari usa il centro del settore intero; nella forma mista con ultima card a larghezza piena usa solo le righe con coppie. Riusa l'assestamento e la sospensione dei divisori già presenti nella v5.1, senza un controller successivo. Migliorati margini e spazi dei titoli, righe, fonti, form, footer. Non cambiano dati/owner delle schede.

## Artefatto, prove e confini

[HTML v5.2](13-griglia-contesti-tour.html) · [receipt](EVIDENCE_CONTEXTS_TOUR_20261010.json). HTML SHA256 `624d18f6b95e6d6703a898075e590457e1c65425f533f23e0f0a7b2f2d0201fa`, Git blob `6461b505b358bcce3e7bf78aacc47135a850e139`, 321357 byte. Builder patch-based SHA-guarded, baseline v5.1, screenshot, test, metodo e receipt sono nel pacchetto ZIP consegnato nella conversazione.

Nuove verifiche sul codice esatto: 41/41 (preparazioni/tour), 107/107 (geometria su 2050–390 px), 7/7 (ruoli per contesto e accesso tastiera), 12/12 (zoom CSS 100–200%). Regres­sioni v5.1 rieseguite: 103/103 Home, 26/26 divider, 23/23 bozze/Libero con un passaggio di prova adattato per non deselezionare la preparazione ora conservata. Totale **319/319 controlli correlati**, zero JS page errors osservati nei percorsi; tre script `node --check` superati.

Il ricevente Chromium di prova ha bloccato la navigazione HTTP/file locale: serializzazione/lettura `localStorage` in un nuovo documento sono state esercitate con archivio simulato, **non** la persistenza effettiva sul disco Edge fra riavvii. Browser native zoom, screen reader, touch fisico, utenti indipendenti, IA/LLM, filesystem Codex, kernel/sezioni Nautico reali, produzione e provider esterni non sono attestati. La base HTML è ancora parzialmente monolitica: questa modifica è una patch owner-native verificabile, non la modularizzazione del prodotto.

**Stop:** prova dell'operatore in Edge: preparare due contesti, tornare da Canvas alla Home, ricaricare la pagina e ispezionare il tour con zoom; non fare merge/deploy o creare nuove competenze per inerzia.
