# K-UX-AI v5.0 — Campo coerente: toolbar, divisori, Home

**9 ottobre 2026.** Owner del prototipo: `GrazianoGuiducci/k-ux-ai`; branch `work/ux-ai-ui-library-20261008`. Dominio dimostrativo Kernel Nautico, senza integrazione operativa.

## Differenza dell'operatore

Quattro screenshot Edge sulla v4.9 segnalano: con 2 schede la maniglia non muove effettivamente le colonne; con 3 una card segue in ritardo; toolbar da ricomporre come insieme funzionale; in Home una tessera trascinata sopra un'altra deve assumere il **ruolo di forma della posizione di arrivo**, non diventare sempre principale. La Home desktop dovrebbe mostrare tutti e 10 gli ingressi nel viewport.

## Cause realmente osservate

- La regola storica `.workspace-stage.kux-tiled[data-count='2']:not([data-composition=stack])` imponeva un 50/50, prevalendo sul rapporto `--kux-secondary-ratio`: a 1680px la baseline misurava 774,5/774,5px anche dopo un drag che aggiornava lo stato.
- Ricomposizioni FLIP (750ms) e callback di reflow potevano agire mentre il gesto doveva restare diretto, producendo ritardo.
- La Home assegnava sempre `homeFeatured` alla tessera trascinata e usava minimi di altezza incompatibili con il viewport desktop.

## Risultante esercitata

- **2 schede:** la composizione focale esclude l'override 50/50 e l'handle agisce direttamente sulla geometria.
- **Durante resize:** si sospende il FLIP e si evita il reflow ridondante; rilascio e tastiera applicano un commit visivo senza trasformare ogni frame in nuovo evento semantico.
- **Toolbar:** un'unica sequenza Contesto → Azione → Griglia/Campo → strumenti/aggiunta, con gli stessi controlli DOM già esistenti, riaggregati; sui viewport stretti va su due righe, senza controller duplicati.
- **Home:** le 10 tessere conservano identità d'attività ma scambiano la morfologia della posizione in cui vengono lasciate, principale/larga/media/compatta, anche per un drop fra due tessere non principali. `Entra` resta separato dal drag; Alt+freccia e Shift+Invio danno accesso equivalente da tastiera. «Disponi per uso» e «Ripristina ordine» conservano recuperabilità.
- **Viewport:** desktop ≥900px e sufficientemente alto (≥680px) mostra tutte le tessere; a 900px si contrae il testo secondario, non il comando Entra. Mobile e finestre basse possono scorrere per mantenere leggibilità.

## Artefatti e prove

[HTML autonomo](11-griglia-campo-coerente.html), [ricevuta](EVIDENCE_CAMPO_COHERENTE_20261009.json). Git blob dell'HTML **byte-identico**: `a533b4e2751580c3fd0dae28c4025470a8011ff1`; SHA256 `baecb8930291f05aa07acf96888ec8147260183b8187e9f458a49b9e5343c56e`. Il pacchetto ZIP della conversazione conserva la baseline esatta v4.9, il builder con ancoraggi fail-closed, tre suite Playwright, screenshot e ricevuta.

- Test nuovi: **103/103 PASS**.
- Suite principale v4.9 ripetuta sulla nuova sorgente: **53/53 PASS**.
- Suite estesa v4.9 adattata alla toolbar (Ricomponi in Strumenti, nessun duplicato): **39/39 PASS**.
- Tre blocchi JavaScript passano `node --check`; nessun errore pagina osservato nel browser nelle prove.

**195 controlli correlati** non costituiscono prove indipendenti d'usabilità. Test Chromium headless via `page.set_content`; Edge sul PC operatore, touchscreen fisico, screen reader, font/zoom estremi e continuità fra sessioni restano da verificare.

## Confine e continuità

La forma principale di una tessera nella Home non è la competenza attiva né un'approvazione. La ripartizione del campo non possiede il caso Nautico, gli effetti o le autorizzazioni. Il codice modifica punti pertinenti della base v4.9 e concentra il CSS in un blocco riconoscibile; **la modularizzazione completa del prototipo legacy non è conclusa**. Non attiva LLM/provider, Section Kernel o filesystem PC/Codex. `main`, Kernel Nautico e Site MAIOS non sono stati cambiati.

Prossimo movimento: prova dell'operatore in Edge sul candidato v5.0; successiva integrazione owner-native solo se selezionata da una differenza materiale.
