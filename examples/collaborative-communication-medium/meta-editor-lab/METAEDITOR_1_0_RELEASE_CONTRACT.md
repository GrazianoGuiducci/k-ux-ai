# MetaEditor 1.0 — perimetro di chiusura e release candidate

## Stato del primo candidato tecnico — 23 novembre 2026

**A · Definizione:** otto percorsi funzionali e funzionalità escluse fissati qui sotto; non ampliare la 1.0 con nuove competenze non necessarie. **B · Pacchetto:** builder `tools/build_metaeditor_starter_pack.py` produce `1.0.0-rc.1` in uno ZIP deterministico, con `VERSIONE_E_FILE.json` e checksum SHA-256 per ciascuno dei sei file d'uso. I test confrontano due build byte per byte e verificano tutti gli hash. **C · Piattaforme:** [CI 45168573050](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45168573050), **5/5 job verdi**, compreso Chrome su Windows e Linux con `file://`; i test indipendenti Studio21 e MAIOS live sono verdi. Il pacchetto generato da quel run è l'artefatto `metaeditor-1-0-rc1` (ID `14815467429`), non un annuncio pubblico. **D · Uso umano:** non ancora esercitato; resta un solo percorso integrato sul PC dell'operatore quando scegliamo la candidata.

**Lavoro rimasto per la decisione 1.0:** mantenere verde la CI su ogni correzione materiale, riesaminare packaging/licenze e guida d'uso, eseguire il singolo collaudo d'uso D e risolvere solo gli impedimenti emersi. Il test automatico Windows non chiude D. La patch privacy di MetaCanvas rimane un'altra linea di distribuzione.

**Stato:** definizione di prodotto per il ramo candidato [K-UX-AI PR #2](https://github.com/GrazianoGuiducci/k-ux-ai/pull/2). Non è un annuncio, un merge o una pubblicazione su MAIOS.it. Data di determinazione: 23 novembre 2026.

## 1. Che cos'è la 1.0

**MetaEditor 1.0 è un editor locale, autonomo e utilizzabile da un non tecnico per creare pagine HTML statiche a partire da quattro modelli inclusi.**

Una persona apre `Apri_MetaEditor.html` senza installare software, seleziona un modello (Essenziale, Progetto, Articolo, Da zero), modifica una pagina nel browser, salva una copia di lavoro HTML e, quando ha finito, esporta una pagina pulita senza il pannello editoriale.

La forma della prima versione è **un solo ZIP versione 1.0 con entrypoint, quattro pagine modificabili, istruzioni e manifest di integrità**, non una collezione di prototipi sparsi. Il file di lavoro contiene l'originale completo e non è un documento da pubblicare. Il file HTML pulito è il risultato destinato alla pubblicazione eventuale da parte di chi ne possiede l'autorità.

**MetaCanvas è un prodotto distinto**, rivolto a scene e presentazioni `ccm.document.v1` e template `metacanvas.templates.v1`. I cinque asset MetaCanvas già pubblicati rimangono invariati durante la chiusura di MetaEditor. Non serve convertire scene MetaCanvas in HTML per dichiarare riuscita questa release.

**La chiusura di MetaCanvas ha un unico problema di rilascio separato già individuato:** Studio21 originale IT/EN può includere un collegamento marcato `private:true` nelle proiezioni pubbliche se collega due nodi pubblici. La [regressione browser](../../../tests/metaeditor-studio21-privacy.browser.py) e il [builder candidato](../../../tools/build_studio21_public_projection.py) caratterizzano e correggono il difetto nella candidata; la **pubblicazione degli asset corretti e il readback del sito** sono ancora un effetto distinto. Per chiudere MetaCanvas non serve creare nuove funzioni: serve applicare e verificare la correzione nelle copie versionate IT/EN con decisione dell'owner del sito. Fino ad allora non dichiarare MetaCanvas completamente chiuso.

## 2. Funzioni comprese, congelate per la 1.0

| Percorso | Risultato minimo che deve funzionare |
| --- | --- |
| Avvio | Scegliere uno dei quattro modelli e aprire un documento modificabile `file://` senza server |
| Contenuto | Selezionare testi, modificarli, formattare grassetto/corsivo; aggiungere titolo/paragrafo |
| Collegamenti | Inserire e aggiornare link testuali semplici; URL validati, riferimenti originali conservati |
| Immagini | Aggiungere PNG/JPEG/WebP/GIF locali entro i limiti dichiarati, con alt e didascalia; mantenere i byte incorporati dopo export |
| Composizione | Inserire/trasferire blocchi propri nei flussi supportati; in layout ambigui scegliere un riferimento prima/dopo o ottenere un rifiuto senza modifica |
| Protezione | Preservare i componenti originali `contenteditable=false`/`inert`, i link/ID autoriali e il contenuto fuori da `main` |
| Storia | Annulla/Ripristina coerenti, identità dei blocchi anche quando hanno testo uguale, nessun effetto per azioni rifiutate |
| Continuità | `Salva lavoro`/`Ctrl+S`, riapertura del file modificabile; export pulito senza codice, pannelli o metadati editor |

Questi otto percorsi formano il **contratto chiuso** della 1.0. Una nuova funzionalità è ammissibile soltanto se necessaria a far funzionare uno di essi senza perdita di dati o confusione sostanziale nell'uso.

## 3. Funzioni fuori dalla 1.0 (non difetti di rilascio)

Non vengono promessi import di HTML arbitrario o sconosciuto, CMS o modifica diretta di MAIOS.it, gestione remota di immagini, SVG, layout builder universale, editing libero di ogni struttura originale, collaborazione o sincronizzazione cloud, salvataggio automatico su disco, pubblicazione automatica, editor AI di scene `ccm.document.v1`, ridimensionamento generale di elementi CSS, palette globale, anteprima professionale multipagina, app desktop installabile o supporto mobile touch completo.

Queste possibilità sono un **backlog distinto per 1.x/2.0**, non un elenco di impedimenti che continua a riaprire la 1.0. La presenza di una facoltà in Bridge11 o in Studio21 non la rende obbligatoria nel portatore HTML neutro.

## 4. Le quattro porte di chiusura

| Gate | Prova e proprietario dell'effetto | Criterio |
| --- | --- | --- |
| **A · Prodotto definito** | Owner K-UX-AI / questa specifica | Gli otto percorsi e le esclusioni sono stabili; un solo ZIP e un solo punto di ingresso. **Definito; verifica CI ancora necessaria** |
| **B · Integrità e riproducibilità** | Builder e test GitHub Actions | Due build producono ZIP identici; manifest SHA-256 corrisponde ai file inclusi; file lavoro/reopen/export e invarianti di protezione passano senza regressioni |
| **C · Compatibilità minima** | GitHub Actions separati Linux e Windows | I test `file://` con Chrome desktop sono verdi su Linux e Windows, inclusi ingresso ai quattro modelli, editing/salvataggio e composizioni miste. Non equivalgono a verifica umana |
| **D · Un solo collaudo d'uso** | Operatore sul proprio PC Chrome Windows | Senza istruzioni ulteriori riesce a scegliere un modello, modificare testo, inserire link/immagine, usare Annulla, salvare, riaprire ed esportare; nessun blocco grave, perdita di dati o dubbio insanabile su cosa conservare |

I test visivi/di tastiera di base e gli avvisi di privacy fanno parte dei gate tecnici, non sono autorizzazione a dichiarare una certificazione formale di accessibilità o sicurezza universale.

**Basta un test d'uso integrato per la prima release, non un test umano dopo ogni commit.** I problemi che impediscono uno degli otto percorsi riaprono il relativo gate; altre richieste vanno nel backlog. La decisione di distribuire/pubblicare dopo i gate resta un **effetto distinto**, di competenza dell'owner di release e del sito.

## 5. Stati che non vanno confusi

- **Sorgenti verificate:** codice, template e prove nel ramo della PR; non significa prodotto distribuito.
- **Pacchetto RC raggiungibile:** ZIP generato e verificato da CI; non significa che l'utente lo abbia usato.
- **Chrome Windows esercitato in CI:** browser automatico sul runner Windows; non equivale all'esperienza fisica dell'operatore.
- **Accettazione d'uso:** osservazione manuale sul sistema dell'operatore, una volta raggiunta maturità tecnica.
- **Rilascio:** azione separata con versione finale, licenze, owner del repository/sito e readback pubblico; non nasce dal semplice completamento del documento.

La PR resta **draft** fino alla verifica e alla decisione di release. Non modificare `maios_it/main` o gli HTML MetaCanvas pubblici per raggiungere artificiosamente un gate.

## 6. Prossimo movimento selezionato

Chiudere B e C: pack versione `1.0.0-rc.1`, manifest SHA-256 e confronto riproducibile, suite browser su Windows, readback di GitHub Actions. Se il run risulta verde, preparare **un solo pacchetto RC** per il collaudo d'uso, non nuove anteprime per singole funzioni. Eventuali problemi emersi diventano correzioni ai percorsi definiti, non nuovi prodotti.

**Owner:** K-UX-AI → MetaEditor Evolution. **Competenza di controllo:** KA/FDLA e KERNEL_EVOLUTION per differenze che modificano realmente gate o campo.
