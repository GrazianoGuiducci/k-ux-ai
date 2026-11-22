# MetaCanvas + MetaEditor — consolidamento e rilascio

## 22 novembre — Progressive disclosure del MetaEditor: gate UX candidato

[Controller neutro](meta-editor-lab/neutral-static-page-editor.js) e [test browser](../../tests/metaeditor-neutral-static-page.browser.py) aggiornati: il pannello mostra i comandi solo quando hanno un referente esercitabile, mantiene persistenti le azioni sul documento, usa stato contestuale e toggle senza mutare la sorgente, conclude l'editing da comando e Escape. [CI 45066893656](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45066893656) con quattro job verdi (compresa pagina MAIOS originale letta in sola lettura). L'[artefatto Windows v3](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45066893656) permette la prova reale ma **non è una ricevuta di accettazione umana**. Non è una conferma di accessibilità completa o sanitizzazione clipboard. Nessun merge/deploy; PR #2 draft.

## 22 novembre — Gate B: sorgente live verificato, prossimo gate umano Windows

**Prova puntuale:** [CI 45045287380](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45045287380), **quattro job verdi**, include nuovo test in sola lettura sul `consulting-ai.html` pubblicato su MAIOS.it, eseguito soltanto dopo confronto byte-esatto (Git blob `0fda8ce0...`) con l'originale `maios_it`. Riusciti a 1440 e 390 pixel (Chrome Linux) editing, formattazione, picker dei testi, blocchi aggiunti duplicati/eliminati, spostamenti, Undo/Redo, esportazione pulita e riapertura del lavoro. Nessuna copia dell'HTML MAIOS pubblicata in K-UX-AI; nessun effetto sul sito. La PR #2 resta draft.

**Operatore in condizione di provare:** il job `neutral-static-browser` ha allegato l'artefatto `metaeditor-neutral-windows-preview` (ID `14762989805`, solo fixture sintetica più [protocollo](meta-editor-lab/WINDOWS_ACCEPTANCE_20261122.md)). [Comparazione Bridge11](meta-editor-lab/BRIDGE11_COMPARISON_20261122.md) documenta capacità esercitate, non trasferite e rischi. Non confondere un dropdown operabile da tastiera con un'attestazione screen reader, né una pagina servita al browser Linux con `file://` Windows.

**Stato gate:** prova pagina MAIOS live superata nel perimetro, release generale ancora **non** approvata. Restano verifica umana Windows, compatibilità e UX rispetto a Bridge11, ingressi incollati/HTML non fiduciato, accessibilità e la distribuzione owner `maios_it` distinta. Nessuna modifica dei download pubblici MetaCanvas.

## 22 novembre — Gate B avanzato: controller neutro reale, ancora candidato

**Nuovo portatore prodotto:** [Neutral Static Workpage](meta-editor-lab/NEUTRAL_WORKPAGE.md) monta, su input HTML statico fiduciato, un controller limitato e una sola UI, riusando l'export source-preserving. Il [builder](../../tools/build_metaeditor_neutral_workpage.py) crea una copia lavoro con originale incorporato, non riscrive l'originale né usa materiale privato Bridge11. La separazione è concreta: il lavoro/storico conserva `data-local-block` per i blocchi aggiunti; la copia pubblica pulita elimina marker e UI, preserva gli altri byte e torna all'origine dopo Undo completo.

**Prove:** [CI 45043342858](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45043342858) con tre job verdi, incluso [test browser neutro](../../tests/metaeditor-neutral-static-page.browser.py) su struttura simil-MAIOS *sintetica* e documento MDN CC0 reale, entrambi a 1440/390 Chrome Linux. Editing/formattazione nativa, inserimento, trasferimento fra sezioni, Undo/Redo, clean export, work save/reopen ed esatta restaurazione. La pagina MAIOS *originale* `consulting-ai.html` non è stata copiata nel prodotto; il [workflow privato di prova](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/.github/workflows/metaeditor-neutral-site-integration.yml) nel ramo non produttivo è pronto, ma **esito CI non verificato** dall'attuale receiver.

**Gate non chiuso:** il supporto è esplicitamente limitato a HTML statici fiduciati e topologie dichiarate; non certifica HTML arbitrario, import sanitizzato, equivalenza UX con Bridge11, Windows file://, touch, screen reader o deploy. La decisione su un editor neutro vendibile/usabile e i successivi Gate C–F restano aperti. Mantenere PR #2 draft, nessuna modifica a `maios_it/main` o agli asset IT/EN pubblici fino a selezione di release distinta.

## 22 novembre — Proiezioni private e roundtrip AI: difetto originale, candidato corretto

**Regressione che cambia il gate:** Studio21 originale IT/EN conservava un `link.private===true` fra nodi pubblici durante la produzione di copia HTML pubblica, dati per AI senza privati e template. La [prova su runtime reale](../../tests/metaeditor-studio21-privacy.browser.py) lo caratterizza, invece di dedurlo da una sola lettura del codice. Nel ramo PR #2 il [builder addizionale](../../tools/build_studio21_public_projection.py) trasforma **soltanto la copia candidata Arrow già source-pinned** e filtra esplicitamente i link privati nelle quattro proiezioni interessate (incluso riuso di template). [CI verde 45040754731](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45040754731) per original/candidato, IT/EN e 1440/390 nei percorsi pertinenti: HTML lavoro, copia pubblica, dati AI, template, immagine remota rifiutata, preservazione link/note privati locali su [import AI selettivo + Undo/Redo](../../tests/metaeditor-studio21-ai-roundtrip.browser.py). Anche il precedente movimento della scena rimane verde sul candidato composto.

**Confini:** la prova di esclusione è limitata ai campi esplicitamente `private`, non riconosce segreti in testi ordinari e non copre ogni payload avverso. Il test sul layout da 390 px usa mouse emulato, non touch reale. Restano Gate B adattatore pagina neutro, regressioni più ampie su template/AI, accessibilità e Windows file://, asset versionati e deploy con readback separato. **Il sito e gli originali pubblici contengono ancora la vecchia logica**: non trattare questa correzione del candidato come hotfix già distribuito.

## 22 novembre — Gate movimento pointer: nuova prova sul runtime originale e candidato

[Regressione di vero trascinamento](../../tests/metaeditor-studio21-pointer-relations.browser.py) IT/EN a 1440/390 su Studio21 **originale** e sulla copia candidata Arrow: `section` con tre figli (due card, immagine incorporata), due link interni/esterni; target di presa browser verificato, coordinate relative coerenti, `containerId` e dati immagine preservati, stessi ID/estremi link, path aggiornato, export del lavoro, Undo/Redo. [CI 45040063638](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45040063638) `verify` e `studio21-browser` riusciti. Il [primo test 45039940356](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45039940356) era non discriminante: un gesto da punto geometrico non qualificato non muoveva la sezione, ma non provava un bug del prodotto.

**Gate C / confini:** il percorso pointer diretto testato è verde; il movimento Arrow è corretto **solo nel candidato**. Mouse a viewport 390 non certifica touch fisico. Non sono ancora provati annidamento, import/AI roundtrip, dati privati, template/scene avverse, accessibilità, Chrome Windows file:// o pubblicazione. Procedere alla prova import/export/privacy senza inferire chiusura globale da questo passaggio.

## 22 novembre — Prova delle relazioni nello spostamento, candidato ancora privato al rilascio

Il vecchio test Studio21 aveva verificato il movimento di un nodo isolato. Il [nuovo test sulle relazioni](../../tests/metaeditor-studio21-relations.browser.py) ha dimostrato che il runtime Studio21 originale (IT/EN) muoveva la sola sezione su Arrow: [CI negativa 45037096198](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45037096198). Il [builder IT/EN source-pinned](../../tools/build_studio21_keyboard_section_move.py) applica una correzione di un solo handler a copie temporanee e il [test CI positivo 45037298632](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45037298632) conferma che i figli, compresa un'immagine, accompagnano la sezione, `containerId` e link restano coerenti, il percorso si aggiorna e Undo/Redo serializzati funzionano a 1440/390. La suite precedente rimane verde.

**Gate:** l'invariante sul movimento composto via tastiera è ora provato **nel candidato**, non nell'asset pubblico. Pointer/touch, import/AI roundtrip, privacy, accessibilità, Chrome Windows `file://`, versionamento IT/EN e pubblicazione restano da verificare. Nessun passaggio di gate B–F è stato dichiarato globalmente chiuso.


## 22 novembre — Inserimento scene: test E2E ora acquisito

Il [contratto compositivo `insert`](meta-editor-lab/COMPOSITION_COMMANDS.md), prima verificato per le pagine reali e per le scene soltanto con mock, è stato esercitato nello [Studio21 standalone IT/EN](../../tests/metaeditor-studio21-composition.browser.py) in GitHub Actions (Chrome Linux 1440/390, richiesta `text`/`card`, integrità ID e scene visibile, Undo/Redo, invalid request). [Workflow riuscito 45030544046](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45030544046). **Questo chiude la lacuna del test scena per l'azione insert**, non i gate B/C/D complessivi: movimento, import/export scena, template, privacy e compatibilità richiedono ulteriori prove e un release decision separato.


**Formato:** piano di esecuzione e criteri di accettazione, 22 novembre 2026  
**Owner prodotto e metodo:** K-UX-AI / Collaborative Communication Medium / MetaEditor Evolution  
**Owner sito e distribuzione:** `maios_it`  
**Stato:** release candidate **non ancora formata**; lavoro su ramo non di rilascio. Nessuna pubblicazione autorizzata da questo documento.

## Direzione selezionata dall'operatore

«Finiamo di fare tutto quello che serve fare per fare bene, l'obiettivo finale è pubblicare tutto e stabilizzare il progetto metaeditor e metacanvas.»

La conseguenza non è continuare i Bridge all'infinito né sostituire il prodotto già distribuito con il file di una pagina MAIOS. Il lavoro deve portare a strumenti effettivamente utilizzabili, con sorgenti verificabili, uno scopo supportato e la capacità di correggersi senza perdere i dati dell'operatore.

## Identità e stato di partenza verificati

| Superficie | Identità e capacità | Stato del 22 novembre |
| --- | --- | --- |
| **MetaCanvas — medium** | HTML autonomo, scene e diagrammi `ccm.document.v1`, template `metacanvas.templates.v1`, salvataggio lavoro, copia pubblica e AI roundtrip sui dati | **Già pubblico**: editor generale, guida Playground r4 IT/EN e demo Studio21 IT/EN; cinque copie nel sito hanno lo stesso Git blob SHA delle fonti K-UX-AI |
| **MetaEditor — competenza/editor** | Editing contestuale del testo, focus, inserimento e posizionamento su pagina HTML tramite adattatore Codex | **Bridge11 sperimentato** dall'operatore («non vedo problemi»), workbench privato, ma non distribuito come editor neutro e non dimostrato su HTML arbitrario |
| **Pagina MAIOS.it** | Distribuzione, spiegazione e accesso in Risorse → Strumenti | Pubblicata, localizzata IT/EN; modificare `maios_it/main` innesca deploy. I file della pagina di consulenza non sono il prodotto |
| **K-UX-AI runtime npm** | Runtime generale di interazione, `0.2.0-alpha.3` | Distinto dal standalone MetaCanvas e dalla competenza MetaEditor; nessun bump npm implicito |

**Nuova precisione di identità:** l'editor generale K-UX-AI corrente (`AI_Collaboration_Studio.html`, blob `d057d68c60061dd9e8f5c2d704cfff2016ea19b1`) coincide con il download del sito `editor-generale-aaa6702-it.bin`. La copia precedente `studio-20-it.bin` (blob `dd9192515930c55fd70741b32510450440f2a8f4`) rimane storica. Alcune guide documentano ancora le dimensioni e l'hash **della vecchia copia** come se fossero quelle del file canonico corrente: correggerle prima di annunciare una versione stabilizzata. I riferimenti agli stati prima del rilascio, datati 13 novembre, sono storia, non stato corrente.

[Manifesto con impronte del baseline](distribution-manifest.json) · [verifica dei download](../../tools/verify_metacanvas_distribution.py) (run in checkout, anche con `--site`).

## Architettura da stabilizzare, senza falsa fusione

```text
                    MetaCanvas — medium collaborativo
                                 |
              MetaEditor — gesti e comandi situati
                                 |
                  comando + referente + effetto
                   /             |             \
          pagina HTML        scene Studio     diagramma
          regioni note       ccm.document.v1  nodi/relazioni
          DOM/CSS/ARIA       template/note     geometria/porte
                   \             |             /
             lavoro modificabile / copia pubblica
                    + proposta diff verificabile
```

Un'**interfaccia coerente** non richiede che una pagina HTML responsive e una presentazione geometrica siano convertite nello stesso formato. I receiver documentali conservano autorità su mutazioni, storico, ID, privacy e serializzazione. Non sostituire `execCommand` o ricostruire il DOM selezionato per principio senza prove sul caret/undo.

## Criteri di release — essenziali

1. **Perimetro dichiarato.** Definire un supporto realmente provato per HTML statico con regioni editabili; dire esplicitamente che React/CMS, siti arbitrari e modifica remota non sono garantiti. MetaCanvas scene rimane `ccm.document.v1`. Riconoscere rischi di formattazione, contenuto privato, storage `file://`.
2. **Versione neutra MetaEditor.** Estrarre i comandi e la UI validi dal Bridge11, senza pubblicare l'HTML Consulenza o Collaborazioni con contenuti del sito. Esercitare lo stesso gesto su **due pagine diverse** (MAIOS e un fixture neutro non MAIOS), preservando semantica, CSS e script non selezionati. L'export HTML pulito o patch non deve contenere strumenti transitori, chiavi di test o un secondo editor.
3. **Nucleo delle funzioni.** Testo ricco e caret; selezione/focus; inserimento; riordino intra/intersezione; immagini/diagrammi/section template *nei carrier che li supportano*; Undo/Redo/no-op; salvataggio lavoro ed export; integrità di scene, link e template. Evitare controlli che promettono azioni non supportate su un dato adapter. Migliorie mancanti vengono esercitate nella competenza proprietaria, non aggiunte come nomi vuoti.
4. **Privacy e sicurezza del documento.** Copia pubblica distinta da lavoro, note e template privati esclusi negli export previsti; importazione di dati strutturati senza eseguire script esterni; rifiuto di link/nodi invalidi, immagini remote e file eccessivi; niente segreti nel bundle. Test negative con modifiche reali e successivo Undo.
5. **Esperienza e accessibilità.** Desktop e 390px; navigazione da tastiera/esc/focus; pan/zoom o scroll contestuale senza spostare il caret; pannelli che non coprono i comandi; reduced motion; provare navigazione `file://` reale, download/reopen, screen reader o audit assistivo proporzionato. Il feedback positivo su Bridge11 non equivale a tutti questi test.
6. **Tracciabilità e build.** Versione, sorgente, licenza MPL-2.0 e notice, SHA-256 e Git blob per ogni artefatto; documentare sorgenti e generazione dei Playground. Preservare le versioni pubblicate senza riscrivere asset cacheati. Test automatico per sorgente e copie: `python tools/verify_metacanvas_distribution.py --site <checkout-maios_it>`.
7. **Distribuzione bilingue.** Pagina Risorse IT/EN, spiegazione del primo uso, download corrispondenti, guide, demo, link e nota che l'AI è esterna, diritti e privacy. Versionare nuovi asset; controllare URL, headers/download, sitemap/llms quando la loro relazione cambia. Source commit, commit sito e versione live restano tre prove distinte.

## 22 novembre — prima prova discriminante su documento neutro

Dall'esatto Bridge11 Consulenza privato (SHA-256 `c0c1078d...`) è stato ricostruito un [**fixture HTML neutro R2**](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/workbench/metaeditor/experiments/MetaEditor_Neutral_Probe_R2_20261122.html) con [builder source-pinned e registro delle prove](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/workbench/metaeditor/experiments/README.md). L'HTML R2 produce SHA-256 `dab81b7ee10e003c2027eb0972ad0fc701dd90759c5a1979ffb5936a60fdeea4` ed è stato riletto nel repo privato (Git blob `cc27f5660e9cc687364a3a786a13cc273dd1423b`).

**Esercizio osservato** in Chromium `set_content` desktop/mobile: editing di testo, inserimento e trasferimento tra sezioni, Undo, export work HTML riapribile con una sola UI ed export statico pulito senza script/markup editor, preservando il paragrafo di controllo. Due errori realmente incontrati: accesso a nav MAIOS assente nel fixture e link download bloccato da protezione editor quando fuori dalla sua shell. Entrambi sono corretti nel R2, con prova della nuova sequenza. Il builder riproduce esattamente il file R2 con impronta verificata.

**Non è l'adempimento del Gate B:** il fixture conserva la struttura `main > section > .site-shell`, il runtime mantiene selettori e stili ereditati dal sito, l'importazione HTML arbitraria e la fedeltà di una pagina esterna reale sono da dimostrare. Il codice è in workbench privato perché deriva dal portatore specifico MAIOS; non entra nei download pubblici. Una UI neutra provata non equivale a un editor generale stabilizzato.

## 22 novembre — R3 indipendente e primo componente pubblico di patch fedele

La R2 è stata esercitata nuovamente su un documento HTML esterno reale, `mdn/learning-area/html/introduction-to-html/document_and_website_structure/index.html` (CC0-1.0, Git blob `0a2636f1c1bb30ffa6515141c831e348b9bd6150`). In questo caso la struttura è **`main > article` con sottosezioni e `aside`**, e non `main > section > .site-shell`.

**Risultato R3 nel workbench privato:** [HTML MDN R3](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/workbench/metaeditor/experiments/MetaEditor_MDN_Independent_R3_20261122.html), SHA-256 `8af2f8b18605f25f8a0e2da9e965c46364cb2756964699c52af7ef940cf75189`, Git blob `5b1dcb244dfcfc9d90f545174ce2a58ae5eb4734`; [builder/test](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/workbench/metaeditor/experiments/README.md). Chromium `set_content` a 1440×844 e 390×844: selezione articolo, inserimento, Undo/Redo, export statico no-op **byte-identico** all'originale, modifica limitata a `main`, salvataggio work HTML, riapertura con un editor e riesportazione senza perdere il cambiamento. Un difetto di baseline dopo riapertura è stato trovato e corretto nello stesso esercizio. CSS MDN esterno conservato come asset; file:// bloccato nel runner. **Non** è ancora un adapter generico su due pagine eseguito con il medesimo bundle.

**Capacità riusabile costituita in K-UX-AI:** [`tools/metaeditor_region_patch.py`](../../tools/metaeditor_region_patch.py) e [test negativi](../../tools/test_metaeditor_region_patch.py) rendono esplicito l'effetto di una modifica di `main` senza riscrivere il contesto non posseduto. Sono stati testati localmente su due sorgenti di differente topologia (HTML MDN e Bridge11 Consulenza) per il caso no-op byte-identico; altri cinque test assicurano regione unica, protezione da duplicati, testo di script/stylesheet non interpretato come tag e mancata esportazione di marcatori runtime. Le nuove prove di CI devono ancora avere esito verificato. Il componente **non è un sanificatore HTML**, né importa file in un browser; il caller deve fornirgli un frammento già validato.

**Gate B aggiornato:** portabilità editor su un documento esterno dimostrata nel caso limitato MDN; patching source-preserving su due sorgenti supportate; ancora aperte l'estrazione di un adapter non source-pinned, la prova funzionale della stessa versione su più pagine reali, UX/ARIA/accessibilità, media e la suite completa di rilascio.

## Prove e gate

| Gate | Evidenza minima | Stato attuale |
| --- | --- | --- |
| A — baseline pubblico tracciato | Sorgenti 5 HTML ↔ copie Git del sito; pin in manifest e script di controllo | **Riconciliati** i Git blob; il nuovo script va eseguito nel checkout reale |
| B — editor di pagina portabile | Bridge11 neutralizzato, due documenti diversi, test di fedeltà/export/undo | **Parziale**: R2 e R3 su HTML MDN indipendente; stesso adapter su due pagine e supporto generale ancora aperti |
| C — scena/diagramma/immagini/template | Regressioni strutturali e privacy dal prodotto pubblico + percorso reale | **Prove storiche**, suite release ripetibile ancora aperta |
| D — ergonomia e compatibilità | Windows Chrome file://, keyboard, mobile e revisione accessibilità | Bridge11 umano **positivo**; matrice completa **aperta** |
| E — candidata IT/EN, codice e licenza | Artefatti versionati e documentazione coerente | **Aperto** |
| F — rilascio e ricezione | Commit K-UX-AI, copie site versionate, push pubblicazione esplicito, readback live su IT/EN e download, rollback | **Non eseguito** |

Non passare da un gate con prove parziali a una dichiarazione «stabile». **B** è il prossimo discriminante tecnico: prima la neutralità e il secondo documento, poi funzioni ulteriori solo se necessarie all'uso. Un test di prova non autorizza da solo la pubblicazione.

## Relazione con gli owner e la consegna

- **K-UX-AI** possiede il mezzo e il metodo; i miglioramenti riusabili tornano a CCM e MetaEditor Evolution nello stesso movimento.
- **`maios_it`** possiede la pubblicazione e le copie dei download; il ramo privato `work/metaeditor-current` conserva i portatori Consulenza/Collaborazioni, che non sono il prodotto da distribuire.
- **Codex** può esercitare test, build e sito con il proprio checkout quando l'effetto è selezionato; il receiver deve riferire file, diff, comando, esito e limiti. L'accesso GitHub da ChatGPT non simula né modifica la cartella locale di Codex.
- **Operatore** valuta il gesto e il significato finale: l'assenza di problemi in Bridge11 chiude quella regressione osservata, non una garanzia generale di compatibilità.

## Cosa non entra automaticamente nel rilascio

Cloud sync, editing collaborativo realtime, integrazione LLM dentro il file, import di siti qualsiasi, CMS/React, PDF completo, touch e screen-reader universali, integrazioni MCP: possibilità o lavori separati finché non richiesti da un caso e provati.

**Condizione di chiusura:** un utente può scaricare l'editor corretto, modificare un documento supportato, salvarlo, riaprirlo, distinguere la copia pubblica, usare l'AI esterna se vuole, senza perdere la fonte. La repository mostra versioni e test; il sito serve gli stessi byte ed è verificato dopo la pubblicazione. Questo documento non afferma che la condizione sia già raggiunta per entrambi i carrier.
