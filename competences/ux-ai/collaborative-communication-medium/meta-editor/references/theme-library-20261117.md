# MetaEditor Evolution — libreria temi come competenza di composizione
Data: 17 novembre 2026 · owner: K-UX-AI / CCM / MetaEditor Evolution
Stato: **metodo esercitato in laboratorio HTML autonomo locale**, non compatibilità dichiarata con tutti i MetaCanvas, né sito pubblicato.

## Differenza selezionata
L'operatore vuole rendere l'artefatto di base più utile e semplice, partendo dalla creazione e recupero di **temi** standard, MAIOS, D-ND e presentazioni. Fornisce il proprio HTML `Collaborazioni_professionali_e_progetti.html` e schermate Canva del catalogo/template/editor, e domanda di acquisire quanto già posseduto nelle competenze e nei diversi tipi di MetaCanvas. **Il tema deve anche aiutare a comprendere quali oggetti/layout siano utili da inserire**, non diventare soltanto un interruttore cromatico.

## Sorgenti già possedute e conoscenza da comporre
- **K-UX-AI / CCM Studio 20 e 21:** `AI_Collaboration_Studio.html`, `MetaCanvas_Studio21_Consulenza_IT.html`, `DOCUMENT_CONTRACT.md`: modello scene `ccm.document.v1`, palette e template personali `savedTemplates[]`, passaggio selettivo a AI, privacy dei template, editor della label già diretto. Non convertire i template personali in libreria pubblica né assumere che la palette Studio sia lo stesso stato del documento web.
- **MAIOS.it:** `site.css` e HTML Collaborazioni fornito mostrano `--air:#c7ecec`, `--substrate:#b9d8c5`, `--choice:#fff8e4`, `--ink:#14313a`, `--ink-soft:#35545c`, `--green-dark:#285d49`, varianti `data-context-expression` (institutional/everyday/research/builder). Secondo [D-ND Design / profilo MAIOS](https://github.com/GrazianoGuiducci/d-nd-ux-ai-seed/blob/main/design/profiles/maios/BRAND_FIELD.md), **le varianti sono espressioni di un campo comune**, non quattro marchi o skin che si sostituiscono.
- **D-ND:** `d-nd_com/lib/themeService.ts` ha palette DARK e LIGHT nel codice, ma `loadThemeState()` forza dark-only. Non annunciare LIGHT disponibile nel sito. Il laboratorio usa una proiezione della palette DARK senza prendere logo, codice runtime o dati.
- **D-ND Design:** [Relational Chromatic Design](https://github.com/GrazianoGuiducci/d-nd-ux-ai-seed/blob/main/design/references/relational-chromatic-design.md) distingue campo cromatico, vettori locali, stati di focus/relations/control e identità; [Web Quality Gate](https://github.com/GrazianoGuiducci/d-nd-ux-ai-seed/blob/main/design/references/web-quality-gate.md) conserva riferimenti e prove su contrasto, gesto, responsive e controlli.
- **Fonti esterne, non autorità:** [Penpot Design Tokens](https://help.penpot.dev/user-guide/design-systems/design-tokens/) lega tokens, set, theme groups e export; [Figma Variables](https://help.figma.com/hc/en-us/articles/14506821864087-Overview-of-variables-collections-and-modes) distingue valori e modes; [Canva Brand Kit](https://www.canva.com/help/brand-kit-best-practices/) collega palette/font/template ai brand; [GrapesJS Style Manager](https://grapesjs.com/docs/modules/Style-manager.html) riguarda proprietà di componenti. Sono meccanismi da assimilare selettivamente, non motivi per spostare l'autorità del progetto.

## Metodo risultante
La capacità `Tema` non è la pagina né la composizione e non determina automaticamente che cosa inserire:

```
identità / ruoli visuali di un profilo
    + (eventuale) espressione contestuale
    + composizioni suggerite, mai autoinserite
    -> forma leggibile per il documento attivo
```

Tenere distinti **tema** (ruoli percettivi, palette, tipografia, forma, spaziatura), **espressione** (variazioni locali su un campo persistente), **composizione** (scelta esplicita di sezioni, card, diagramma+note), **contenuto** (parole, nodi, collegamenti, asset, authority del sito) e **controlli editor** (non devono essere ricolorati insieme al documento). Una palette viene proiettata via CSS custom properties `--doc-*`, non riscrive un `style` di sito arbitario. Le variazioni MAIOS vivono come overlay sul medesimo profilo `maios-field`; D-ND resta un esempio dark-first. Il tema può **suggerire** composizioni, ma l'operatore decide e l'effetto su sezione esistente rispetto all'aggiunta di nuova sezione è visibile.

## Esercizio Lab 02 realmente formato
HTML `MetaEditor_Lab02_Theme_Library_IT.html` generato in questa conversazione dal Lab 01, non ancora trasferito nel runtime canonicale K-UX-AI né in MAIOS.it. Contiene catalogo con cinque preset (Carta chiara, Grafite, MAIOS Campo, D-ND Notte, Presentazione Blu), cambiamenti visivi senza mutare i blocchi, modalità espressive MAIOS (balanced/institutional/everyday/research/builder), creazione personalizzata da tema attivo, modifica di otto ruoli cromatici, font, raggio, gap, lista di composizioni suggerite, avvisi contrasti campione, cancellazione solo dei temi personali.

**Conservazione:** libreria `metaeditor.themes.v1` inclusa nel file HTML salvato e, dove l'origine lo consente, copia browser `localStorage`; import/export JSON portabile per passare a altri file o dispositivi, con validazione di schema/valori e senza esecuzione di JS da import. La lettura `Da HTML…` riconosce un sottinsieme dichiarato di custom properties `:root` tramite testo, senza eseguire script o importare contenuti: sul file Collaborazioni sono stati verificati `--ink:#14313a` e `--air:#c7ecec`. In presenza di CSS arbitrario o con variabili composte, la derivazione è solo parziale.

**Prove eseguite:** Node `--check` sul runtime; Chromium headless `page.set_content` ha esercitato applicazione profili, cambio espressione MAIOS, verifica del contenuto e posizionamento invariati, creazione/aggiornamento tema personale, anteprima e salvataggio, Undo/Redo, export/import di tema JSON su pagina separata, derivazione da HTML allegato, doppio clic e modifica nel testo di un nodo dopo cambio tema, export e riapertura HTML su viewport 390 px senza overflow nel caso, e assenza di `pageerror` nei percorsi. Controllato render dei profili MAIOS e D-ND; corretta spaziatura dei nodi/visibilità dei connettori e leggibilità dello status anche su sfondo scuro. Il runner amministrato ha bloccato l'apertura `file://` (`ERR_BLOCKED_BY_ADMINISTRATOR`); non attribuire all'artefatto la prova sul Chrome Windows dell'operatore.

## Apprendimento che deve cambiare il prossimo fare
1. **Tema come kit, non skin:** nel primo disegno i preset erano solo colori; l'intento ha reso visibile la necessità di conservare anche **composizioni suggerite modificabili**, senza confondere suggerimento e azione. Per i layout 1/2/3 colonne il gesto è `Imposta` sulla sezione; per `diagramma+note` è `Aggiungi` una nuova sezione: il lessico è parte della funzionalità.
2. **Creare e recuperare senza dispersione:** la UI iniziale collocava la creazione solo sotto cinque preset, raggiungibile con scroll e poco percepibile. Si è spostato `+ Crea tema` vicino al punto di ingresso; gli strumenti meno frequenti restano sotto. Una nuova capacità deve ridurre la ricerca dei comandi.
3. **Fonte del brand e dati di progetto non sono lo stesso stato:** un tema MAIOS derivato da CSS/HTML è una **bozza di proiezione** finché l'owner del sito non ne valida la fedeltà. La lettura CSS non importa contenuti né giustifica portabilità universale.
4. **Persistenza divisa per portatore:** file HTML conserva editor e libreria, browser conserva copie quando consentito, pacchetto JSON porta temi fra file. Non scrivere `sempre disponibile` quando la persistenza `file://` varia; i dati personali nei temi entrano nell'HTML di lavoro e vanno revisionati prima della condivisione.
5. **Qualità del gesto prima di nuove funzioni:** prima la modifica diretta del nodo (Lab01), poi scelta tema, poi verifica che il nodo continui a essere editabile e che l'export non duplichi controlli. Un test dell'input o una schermata non prova l'uso umano.

## Limite e prosecuzione
Questo è **Lab 02 su modello sintetico `metaeditor.lab.v2`**, non un adattatore realizzato per la pagina Collaborazioni, né porting del sistema dei temi a Studio20 `ccm.document.v1`. Rimane da provare import/patch di regioni HTML dichiarate su due siti diversi, scambio semantico con Codex, screenshot e gesto su Chrome Windows e trattamento dei temi in esportazioni private/pubbliche. Non scegliere automaticamente un nuovo motore (GrapesJS/Puck/Excalidraw) perché ora c'è una libreria di temi.

La competenza deve trovare questo documento attraverso [SKILL](../SKILL.md) e [GUIDE](../GUIDE.md), e il [CURRENT](../CURRENT.md) deve distinguere prova di codice locale, pubblicazione in K-UX-AI e applicazione nel ricevente. Un commit di documentazione non installa il Lab02.

## Trasferimento successivo, stesso movimento — disponibilità del codice

Dopo la prova locale, il file HTML autonomo è stato scritto nell'owner K-UX-AI come [MetaEditor Lab 02](../../../../../examples/collaborative-communication-medium/meta-editor-lab/MetaEditor_Lab02_Theme_Library_IT.html), commit `a860debde019b376c67a2534697f3bf1f5600b64`. Un readback di `fetch_file` ha confrontato integralmente la sorgente pubblicata con i 52018 caratteri del file locale e ha trovato identità byte-per-byte nella rappresentazione UTF-8. La frase precedente «non ancora trasferito» descriveva lo stato **prima** di questo commit, non lo stato presente. Rimane un esempio pubblicato nella repository, non una release runtime o un aggiornamento di MAIOS.it.
