# MetaCanvas / MetaEditor — handoff per receiver implementativo

## 22 novembre — Nuove prove disponibili senza cambiare il mandato

Il gate Studio21 ha ora un candidato combinato e verificabile: [spostamento Arrow](../../tools/build_studio21_keyboard_section_move.py) e [proiezioni con link privati protetti](../../tools/build_studio21_public_projection.py) su HTML originali IT/EN, sempre in directory temporanee. I [test di trascinamento](../../tests/metaeditor-studio21-pointer-relations.browser.py), [proiezione privacy](../../tests/metaeditor-studio21-privacy.browser.py) e [ritorno AI selettivo](../../tests/metaeditor-studio21-ai-roundtrip.browser.py) sono integrati nella [CI verde 45040754731](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45040754731). Il lavoro privato resta nel documento; link `private:true` con entrambi gli estremi pubblici non devono uscire per inerzia. L'esercizio AI applica solo la modifica selezionata e preserva la parte privata locale con Undo/Redo.

Queste prove **non sostituiscono la candidata neutra MetaEditor** richiesta da questo handoff. Il receiver che prosegue non deve rifare Bridge11/R3, i test nativi o gli stessi controlli privacy per riottenere contesto. Deve formare il prossimo risultato proprio del Gate B: un adattatore non vincolato al file sorgente, con prova sulle due topologie pagina MAIOS e non-MAIOS e con preservazione reale di HTML/export. I successivi gate touch/Windows/accessibilità e distribuzione restano distinti; non convertire automaticamente il successo CI in release.

**Data:** 22 novembre 2026  
**Mandato autoriale:** «Finiamo di fare tutto quello che serve fare per fare bene, l'obiettivo finale è pubblicare tutto e stabilizzare il progetto metaeditor e metacanvas.»  
**Modo scelto in questa fonte:** `PRIVATE_BUILD + VERIFY`; **non** `PUBLIC_EFFECT`.  
**Proprietà:** K-UX-AI prodotto/metodo; `maios_it` portatori e distribuzione; Codex esercita solo nel proprio checkout secondo i suoi ingressi.

## Esito richiesto

Costruire una candidata MetaEditor per pagine HTML statiche **esplicitamente supportate**, utilizzabile insieme a MetaCanvas Studio senza appiattire il formato a scene `ccm.document.v1`. Deve permettere di modificare un documento reale, salvare il lavoro e ottenere HTML pulito/diff non distruttivo, conservando ID, contenuti non toccati e possibili script/CSS della pagina. Integrare o riusare le capacità già implementate, eliminando duplicazioni della UI.

Non imporre un design, framework, struttura interna o sequence di micro-commit da questo documento: il receiver vedrà meglio il proprio checkout. Può scoprire una soluzione diversa, ma deve preservare invarianti e restituire evidenza.

## Fonti da raggiungere per comprendere il campo

- [K-UX-AI / BOOT](https://github.com/GrazianoGuiducci/k-ux-ai/blob/main/BOOT.md) e [MetaEditor SKILL/CURRENT/GUIDE](https://github.com/GrazianoGuiducci/k-ux-ai/blob/main/competences/ux-ai/collaborative-communication-medium/meta-editor/CURRENT.md), incluse differenze emerse dai Bridge06–11.
- [Stabilizzazione: criteri, baseline, gate e storia](RELEASE_STABILIZATION_20261122.md); [manifest verificabile](distribution-manifest.json).
- Repository privata `GrazianoGuiducci/maios_it`, ramo `work/metaeditor-current`: [Bridge11 Consulenza](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/workbench/metaeditor/CURRENT.html) e [neutral R2 + builder con limiti](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/workbench/metaeditor/experiments/README.md).
- [Il pubblico MetaCanvas / documento scene](DOCUMENT_CONTRACT.md) e Studio20/21 IT/EN, Playground r4, codice pubblico nel loro owner.
- `maios_it/AGENTS.md` per la separazione fra branch di lavoro e distribuzione automatica da `main`; Codex `AGENTS.md` e TM9 routing owner-native.

## Invarianti

- La pagina HTML originaria rimane l'oggetto: l'editor non può cancellare componenti ignoti per comodità, inventare un nuovo layout globale o esportare una pagina con l'interfaccia/handler transitori ancora presenti.
- Il motore di presentazioni conserva `ccm.document.v1`, link, scene, note, template, AI diff/import e copia pubblica secondo i propri contratti. Non convertire DOM e scene uno nell'altro se il compito non lo richiede.
- Rich text, caret, focus, Undo/Redo, riferimento dell'elemento, inserimento/trasferimento e salvataggio già funzionanti sono capacità da conservare. Un no-op non genera checkpoint.
- Nessuna credenziale, recupero locale personale, pagina MAIOS in bozza o altro contenuto editoriale entra nel bundle pubblico. Preservare licenza MPL-2.0 e avvisi appropriati senza estenderla automaticamente ad altri owner.
- Conservare i file storici e `maios_it/work/metaeditor-current/workbench/metaeditor/CURRENT.html` fino a una versione materialmente accettata. Non confondere il fixture R2 con una release.
- **Non scrivere o fondere `maios_it/main` senza distinta selezione del rilascio**; quel ramo alimenta automaticamente la VPS.

## Libertà di costruzione

Sono ammessi refactoring, moduli, adapter, test browser, librerie sostenibili o un editor autonomo diverso, purché il rapporto tra sorgente originale, documento editabile e file esportato resti dimostrabile. Se un adapter non può garantire un HTML arbitrario, scegliere e dichiarare l'ambito più ristretto supportato. Non aggiungere pulsanti senza gesti funzionanti o opzioni prive di effetti.

## Prova minima della candidata

1. Controllo **senza modifiche**: export statico confrontato con la sorgente (differenze solo quelle dichiarate; risorse non riconosciute non perdute).
2. Su una pagina MAIOS e su un HTML reale **non MAIOS**: modifica del testo formattato, selezione, inserimento, posizionamento, Undo/Redo, export lavoro e riapertura; HTML statico pulito o patch verificabile. Mostrare esattamente le differenze.
3. Controlli su ID, anchor/ARIA, script e CSS non toccati, link, immagini, responsive desktop/mobile, tastiera, focus e perdita di dati dopo export/reopen.
4. Suite MetaCanvas separata: scene, collegamenti, diagrammi, immagini, template, import AI basato sui dati, note private, copia pubblica e fallback/undo; input avversi (schema errato, duplicati, immagini remote, dati privati).
5. Se un criterio non è dimostrabile nel receiver, segnalarlo come blocco con fonte e stato, non chiamarlo passato.

## Nuova conseguenza del 22 novembre — seconda topologia e source-preserving patch

Il [Gate B](RELEASE_STABILIZATION_20261122.md) è avanzato con [R3 MDN indipendente](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/workbench/metaeditor/experiments/README.md): `main > article` con sottosezioni, sidebar e CSS distinto. In Chromium desktop/mobile, il no-op pulito torna ai byte originali; dopo una modifica si altera soltanto `main`; Undo/Redo e roundtrip work→clean conservano gli interventi. La prova di un editor generale non è ancora stata ottenuta. Il difetto emerso dal ritorno a un HTML di lavoro è istruttivo: **non prendere il documento salvato come nuovo originale**, altrimenti l'export può annullare le modifiche.

Come capacità di infrastruttura già esercitata nel ramo K-UX-AI sono disponibili [patch source-preserving](../../tools/metaeditor_region_patch.py) e [test positivi/negativi](../../tools/test_metaeditor_region_patch.py). Non rappresentano un importer o un sanitizzatore: l'editor deve validare il frammento prima dell'effetto e decidere se un documento esterno è supportato. Il receiver può riusarli o proporre una migliore implementazione, ma deve dimostrare l'equivalente contratto di conservazione dei dati **su un unico adapter realmente usato da più documenti**, non su due build vincolate separatamente.

**Prossimo discriminante:** produrre un modulo/adattatore non source-pinned che si installi esplicitamente su HTML statici dichiarati, con una sola UI e un insieme di comandi consentiti dalle loro regioni, e ripetere la stessa prova su un documento MAIOS e uno esterno, conservando fedeltà e limiti. L'uso Chrome Windows per il nuovo adapter e la pubblicazione restano effetti distinti.

## Contratto di ritorno

Restituire nel ramo candidato di K-UX-AI **sorgenti, fixture non sensibili, test automatici, README di utilizzo e istruzioni di build**; nel ramo privato `maios_it/work/metaeditor-current` soltanto gli artefatti di bozza che appartengono al documento. Informare K-UX-AI / MetaEditor Evolution delle modifiche di capacità che devono essere apprese e rese discoverable.

Per ogni effetto: commit/ref, file prima/dopo, esito dei test, screenshots/prove quando utili, limiti, avvisi su privacy/licenza e gate raggiunti. L'operatore può valutare la candidata in Chrome Windows. La pubblicazione IT/EN, asset versionati, sitemap/link e readback live sono un movimento successivo del sito e non discendono automaticamente dalla disponibilità della candidata.

**Condizione di arresto di questo handoff:** una candidata tecnicamente verificata, riesaminabile, pronta alla selezione del rilascio; non un commit su produzione o un prodotto falsamente dichiarato universale.
