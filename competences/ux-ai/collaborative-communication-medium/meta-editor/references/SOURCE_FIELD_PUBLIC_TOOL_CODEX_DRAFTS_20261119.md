# MetaCanvas / MetaEditor — riconciliazione delle sorgenti prima della convergenza
**Data:** 19 novembre 2026 · **Owner della competenza:** K-UX-AI / Collaborative Communication Medium / MetaEditor Evolution  
**Stato:** ricognizione e prova circoscritta dell'editor Codex; **nessuna nuova versione del prodotto, nessun deploy, nessuna fusione del runtime**.

## Correzione esplicita dell'operatore

L'operatore segnala che abbiamo ridotto il contesto del MetaCanvas ai laboratori e a una R5 della pagina Consulenza. La situazione è maggiore: **MetaCanvas è già uno strumento pubblico MAIOS, ma incompleto**, distribuito da [Risorse → Strumenti → MetaCanvas](https://maios.it/risorse/strumenti/metacanvas/). Il file nuovo `MAIOS_Consulenza_AI_revisionata(1).html` è una **bozza del sito editabile con Codex**. È difficile da usare ma contiene capacità valide, soprattutto un editor di testo che la R5 sperimentale non aveva adeguatamente assimilato. La richiesta è **acquisire le informazioni e il saper fare in modo completo prima di procedere**, studiando anche altre sorgenti. Non scegliere per inerzia la prossima numerazione R6.

La correzione è alla **formazione del campo e all'ingresso della competenza**, non soltanto un elenco di pulsanti. Non perdere nessuna funzione valida quando un oggetto passa fra MetaCanvas pubblico, bozza del sito e riceventi AI.

## Inventario delle identità, con prova e owner

| Identità | Sorgente/contratto | Capacità documentate | Cosa non dimostra |
|---|---|---|---|
| **Pagina pubblica del tool MAIOS** | `maios_it/risorse/strumenti/metacanvas/index.html` e `maios_it/docs/RESOURCE_COLLECTIONS.md` | Descrive revisione di pagine, presentazioni, progetto (Apollo/dossier), tavole creative, interfacce/template, scambio del file HTML con persone e AI; IT/EN; download di Playground r4, editor generale e demo Studio21 | Non è di per sé il runtime dell'editor; la ricognizione ha letto il codice GitHub della pagina, non verificato il deploy con browser remoto |
| **Playground r4 IT/EN** | `k-ux-ai/examples/collaborative-communication-medium/MetaCanvas_Guida_Playground_r4_*.html` e `maios_it/assets/downloads/metacanvas/playground-r4-*.bin` | Guida interattiva rimovibile, esercizio in scheda, passaggio AI, esportazione | Non equivale al file della pagina Consulenza né ai laboratori |
| **Studio 20 generale** | `k-ux-ai/examples/collaborative-communication-medium/AI_Collaboration_Studio.html`, `README.it.md`, `DOCUMENT_CONTRACT.md` | Modello `ccm.document.v1` con scene/elements/links, testo dei nodi diretto, forme, frecce, note, immagini locali, Standard/Flat, Presenta, miniature, pannelli spostabili, undo, template salvati e portabili, AI roundtrip selettivo, copia pubblica, recupero opzionale | Non importa arbitrariamente l'HTML/CSS/JS di un sito preservandolo byte per byte; non contiene un LLM |
| **Studio21 demo Consulenza IT/EN** | `MetaCanvas_Studio21_Consulenza_IT/EN.html` e `studio-21-it/en.bin` | Sette schede editabili, due lingue distinte, Demo/Canvas vuoto | Non sono due localizzazioni intercambiabili di una pagina web, né editor universale |
| **Editor di bozza usato con Codex** | File utente `MAIOS_Consulenza_AI_revisionata(1).html` in conversazione | Rich text, gestione pagina/elementi, CSS/colore sito, preview device, ridimensionamento, storia, recupero locale, export | Non rappresenta il runtime pubblico; non importa il modello scene; non ha un editor di diagrammi analogo allo Studio |
| **MetaEditor Labs 01–05** | `k-ux-ai/.../meta-editor-lab/` | Gesti diretti, temi standard/MAIOS/D-ND, elementi e sezioni, multi-selezione blocchi, clipboard interna, allineamento/nodi in diagramma, strumenti spaziali | Modello sintetico; non sostituisce Studio20/21 o l'editor Codex |
| **R5 specifica sulla pagina R4** | `meta-editor/references/first-real-page-r5-20261119.md`; HTML in conversazione | Dock ridotto, testo/nodo diretto, diagrammi, immagini, 4 regioni e patch JSON per regione, progetto/statico | È derivata da una **R4 allegata precedente**; non è la pagina Codex ora fornita, il prodotto distribuito o la sorgente attuale del sito |
| **Siteman Studio D-ND** | `d-nd_com/components/admin/SitemanStudio.tsx` | Editing redazionale visuale/sorgente, operazioni AI, metadati e percorso di pubblicazione in contesto nativo | Non è un importatore fedele di qualsiasi sito |

**Contratti distinti:** K-UX-AI è owner del prodotto e della competenza MetaEditor; `maios_it` è owner della pagina pubblica, delle copie distribuite, delle bozze del sito e del deploy; D-ND Design conserva il metodo percettivo; Codex conserva il receiver e il checkout effettivo. La licenza del tool nella directory CCM è MPL-2.0; non si applica automaticamente ad ogni pagina del sito o alle competenze. La pagina pubblica è presentazione e distribuzione, non autorità sullo stato del codice eseguibile.

## Analisi diretta del nuovo allegato Codex — capacità che NON dobbiamo perdere

**Identità del file letto:** `MAIOS_Consulenza_AI_revisionata(1).html`, **419.563 byte**, SHA-256 `f227b61b0a813ad7312f805dcec63def03b87201d5d5fb6ae0ae729d2541f190`. Meta `maios-review-source-sha256` = `8384a4f172298ca7ddd0fcd94fff99cec707c60b46ae6a67d7d618b2715ac399` (riferimento dichiarato dal documento, **non** prova di identità con la versione live). `data-local-document-id=d0c6d644-2f32-4353-a269-ecb3201bec83`. Quattro `main > section`; CSS e JS MAIOS e un editor HTML incorporati. `robots=noindex,nofollow` è coerente con una bozza, non prova di deploy.

**Preservare e assimilare:**
1. Testo editato **sul punto reale**, con `contenteditable` anche fuori dalla modalità globale «Modifica testi», selezione DOM e toolbar `#local-mini`: H1–H6/paragrafo, dimensione, grassetto, corsivo, sottolineato, rimozione formato, colore, eliminazione della selezione, Undo/Redo e chiusura. Usa bookmark di selezione/range per recuperare il caret dopo la toolbar. Non ridurlo a campo stringa remoto e non eliminare il testo formattato nell'esportazione.
2. **Sezioni e struttura**: selettore sezioni/elementi, ricerca testo, mostra/riordina/duplica/elimina sezioni con remap degli ID e ARIA e conversione dell'H1 duplicato in H2, inserimenti `paragraph/heading/list/callout` prima/dopo/in fondo, movimento di elementi fra sezioni e selezione con ancoraggio.
3. **Proprietà della pagina**: palette dagli effettivi ruoli cromatici MAIOS, sfondo/testo per sezione o elemento, larghezza percentuale, altezza minima, ridimensionamento e maniglie visive, CSS responsive e contesto `data-context-expression`.
4. **Operatività Codex**: menu local-tools spostabile/ridimensionabile, mini-barra autonoma, anteprima Desktop/Mobile in iframe `srcdoc`, snapshot Undo/Redo (30), salvataggio/recovery `localStorage` condizionato all'origine/file, bozza sporca, file HTML portabile. Il salvataggio nel browser non equivale a un file modificato su disco.
5. **Separazione dalla pagina editoriale**: la navigazione, i link, la call-to-action, il CSS e gli script del sito esistono indipendentemente dalla UI di modifica; il futuro adapter deve preservarli e non clonare/esportare controlli temporanei.

**Limiti osservati nel codice e nell'uso riferito dall'operatore:**
- I controlli competono per lo stesso spazio: `#local-tools`, `#local-mini`, selettori sezioni/elementi e le maniglie. Nel Chromium del ricevente, facendo doppio clic sul titolo con pannello aperto si vedono simultaneamente inspector e barra testo.
- La duplicazione di **blocchi già aggiunti** è condizionata da `data-local-block`; i componenti originari della pagina non hanno automaticamente lo stesso trattamento. Mancano inserimento immagini e diagrammi come blocchi dell'editor Codex, template di sezione compositi, selezione multipla strutturale e patch differenziale strutturata.
- `snapshot()` e `restore()` serializzano/reimpostano l'intero `main.innerHTML`, mentre l'esportazione clona il documento. È un rischio di ricostruzione del DOM, perdita di identità e interazioni associate a nodi sostituiti; **rischio tecnico motivato dal codice**, non errore osservato su questa bozza.
- Il formato testo usa `document.execCommand` e `queryCommandState`. MDN classifica `execCommand` come deprecated, ma segnala il vantaggio storico nel preservare l'undo nativo: **non sostituire indiscriminatamente** senza test caret, selezione, formattazione mista, paste, Undo e re-open.
- I menu posizione prima/dopo possono risultare disabilitati finché manca un referente valido: non inferire che siano sempre disabilitati. Recupero `file://`/localStorage è dipendente dal browser; il file di bozza può cambiare nome e quindi storage key.

**Verifica diretta del file in questo turno:** entrambi gli script inline passano `node --check` (Node 22). Chromium headless caricato tramite `page.set_content`: quattro sezioni; pannello chiuso inizialmente, aperto col comando «Modifica»; doppio clic su H1 → `contenteditable=true` e `#local-mini` visibile; nessun `pageerror` nel percorso. `file://` è stato bloccato da `ERR_BLOCKED_BY_ADMINISTRATOR`; non attestare Chrome Windows dell'operatore, usabilità generale, salvataggio locale o sicurezza. La visualizzazione mostra bene il problema di ingombro.

## Cosa preserva il prodotto pubblico che l'editor Codex non possiede

**Studio20 non è un semplice diagrammatore.** Il suo `ccm.document.v1` conserva scene, nodi, collegamenti, porte, frecce/route, geometria, notes, miniature, template personali (`metacanvas.templates.v1`) e le scelte di privacy. L'esportazione `Dati per AI` può essere limitata a scheda o documento; per default esclude note private e libreria personale. L'importazione legge **solo dati** JSON/HTML, mostra scene nuove, cambiate, mancanti e permette integrazione selettiva o sostituzione confermata, senza eseguire script esterni. La **Copia pubblica** è diversa dal file di lavoro. L'Undo dei template e l'ID remap delle frecce sono competenze già esercitate, non da riscrivere in una R6 inferiore.

**Playground r4** ha una funzione specifica di onboarding interattivo e rimovibile, non va sacrificata per ridurre i controlli. **Studio21** contiene due demo separate IT/EN e non è una sola interfaccia multilingue. **Pagina pubblica MAIOS** è già un riferimento per cinque usi (pagina, presentazione, progetto, creatività, interfacce/template), inclusi Apollo e dossier; il tool deve poter ampliare i casi senza imporre una cornice solo commerciale.

## Formazione di MetaEditor convergente — ipotesi di architettura da esercitare

Non fondere tre HTML trascinandovi tutti gli handler. Il nucleo pertinente comprende:

```text
                            MetaEditor Workbench (UX)
      libreria · struttura · selezione · azioni · testo ricco · storia
                                      |
                    comando semantico + referente + effetto
                                      |
            +-------------------------+----------------------+
            |                         |                      |
        Site/Page adapter         Scene/Slides adapter   Diagram editor
    DOM dichiarato / CSS sito     ccm.document.v1       nodi / frecce /
    regioni protette / patch      notes / AI merge      testo in situ
            |                         |                      |
            +-------------------------+----------------------+
                                      |
                 lavoro editabile · export pubblico · patch
                             provenance + review
```

- **Interfaccia unica di gesti**, non un singolo formato universale: un clic seleziona; doppio clic entra nel testo già presente; Maiusc+clic seleziona omogenei; «+» nel punto inserisce; toolbar breve contestuale; struttura/libreria laterale discreta; proprietà avanzate solo quando richieste; nessuna tripla toolbar.
- **Testo come componente autonomo**: preservare la formattazione con una rappresentazione coerente di span/mark e gestione selection/focus. Tiptap/ProseMirror e `NodeViews` sono una possibilità da confrontare su un microtest, **non scelta definitiva**. Non ricostruire il DOM selezionato fra mousedown, click e dblclick.
- **Adapter pagina non distruttivo**: editare solo regioni dichiarate, mantenere CSS/JS/semantica/ARiA e contenuto non riconosciuto. **No-op → patch vuota**; una modifica testuale → una differenza locale; import/export del progetto separato da HTML pubblicabile. Verificare secondo sito prima di chiamarlo «generale».
- **Adapter presentazione**: preservare `ccm.document.v1`, scene, notes, template, AI delta/reconciliation e Copia pubblica. Niente equivalenza fittizia fra page CSS flow e artboard 16:9.
- **Stesso comando, receiver distinti**: toolbar, shortcut, drag e un futuro intervento AI devono produrre lo stesso tipo di operazione e lo stesso checkpoint, ma l'autorità sull'effetto rimane all'owner del documento e al controller che lo applica.
- **Set di test progressivo**: (1) bozza Codex allegata con formattazione ricca, selezione e caret/Undo; (2) Studio20 con 3 scene, privato/pubblico/template e AI merge; (3) pagina MAIOS corrente con patch minima + un secondo sito non-MAIOS; (4) R5 e Lab05 come sorgenti di prove, non nuove autorità; (5) Chrome Windows reale, touch, keyboard/focus, mobile 390, HTML export/reopen e versioni IT/EN.

### Rapporto con strumenti esterni, aggiornato
- [MDN `execCommand`](https://developer.mozilla.org/en-US/docs/Web/API/Document/execCommand): deprecated, ma presenta casi di editing/undo nativo non facilmente rimpiazzabili; caratteristica da provare.
- [GrapesJS components](https://grapesjs.com/docs/modules/Components) e [Storage](https://grapesjs.com/docs/modules/Storage): document model e HTML/CSS d'uscita non coincidono necessariamente; candidato per adapter pagine solo dopo la prova di fedeltà.
- [Tiptap NodeViews](https://tiptap.dev/docs/editor/extensions/custom-extensions/node-views): possibile modo per comporre testo ricco e nodi interattivi senza un inspector obbligato, non importatore universale di siti.
- Figma/Canva/Penpot: fonti di gesti (toolbar contestuali, struttura, allineamento), non sorgenti o ontologie da copiare.

## Conseguenza da conservare e prossimo movimento discriminante

**La prossima versione non deve essere «R6 = R5 + toolbar Codex».** Deve essere un primo prototipo di **gesto comune** che preservi insieme: ricchezza del testo Codex, modello scene e privacy Studio20, manipolazione nodi Lab05 e patch della pagina R5. Prima fare un piccolo banco su **una pagina Codex vera e una scena Studio20**, con la stessa azione `setText` e selezione locale. Richiedere proof di roundtrip di entrambi prima di aggiungere altri controlli. Preservare le due superfici e non migrare tutto a un terzo schema per inerzia.

La ricognizione e il miglioramento della competenza non autorizzano un merge in `main` delle copie distributive, la sostituzione del file pubblico o una pubblicazione. Per il sito, i download sono asset versionati e devono mantenere SHA/URL sino a release verificata dall'owner.
