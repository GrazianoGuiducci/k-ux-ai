# MetaEditor neutro vs Bridge11 — differenze ancora materiali

**Sorgenti confrontate (22 novembre 2026)**

- Bridge11: `GrazianoGuiducci/maios_it/work/metaeditor-current/workbench/metaeditor/CURRENT.html`, Git blob `9f4f843124f8619eee02ece40a7efc1470881b07`, portatore privato MAIOS e non prodotto universale.
- Neutro: `neutral-static-page-editor.js`, nel ramo candidato K-UX-AI PR #2, riusa `static-page-source-adapter.js`; test su HTML statici con regioni supportate.
- Studio21 `ccm.document.v1`: portatore diverso, non incluso in questa comparazione né da convertire in `main` HTML.

La presenza di un controllo nell'interfaccia Bridge11 è evidenza della capacità di quel portatore, **non** prova di equivalenza con un controllo neutro né autorizzazione a replicare ogni effetto.

| Competenza / gesto | Bridge11 | Neutro candidato | Stato / differenza |
| --- | --- | --- | --- |
| Selezione testo e orientamento | Doppio clic; ricerca e selezione di blocchi; pulsante per portare l'elemento nel focus | Clic/doppio clic; elenco elementi raggiungibile anche da tastiera, con scorrimento al bersaglio | Percorso minimo esercitato in CI; ricerca testuale e navigazione ricca non trasferite |
| Editazione/formattazione | Mini editor, grassetto, corsivo, sottolineato, rimozione formattazione, colore e dimensione | `contenteditable` nativo, grassetto e corsivo | Solo sottinsieme; caret su Windows, selezione complessa e paste rich text ancora da verificare |
| Inserimento | Paragrafo, titolo, lista, callout e inserimenti secondo sezione/riferimento | Paragrafo, titolo in una sezione supportata | Tipi e ancoraggi ridotti intenzionalmente |
| Posizionamento | Riordino di elementi, trasferimento e riferimento in varie sezioni, movimento via handle | Spostamento prima/dopo o in altra sezione per **soli blocchi aggiunti** | L'HTML originale rimane protetto; non attribuire capacità di spostare ogni struttura |
| Eliminazione/duplicazione | Sezione e blocco, secondo controller nativo | Duplica/elimina **solo blocchi aggiunti**, con Undo/Redo; vieta duplicazione con ID che diverrebbe doppio | Nuova capacità limitata e provata in CI; gestione originale protetta |
| Stile e dimensioni | Controllo larghezza/altezza, palette, target proprietà | Non disponibile | Serve un receiver che possieda davvero queste trasformazioni e preservi responsive/layout |
| Anteprima e strumenti | Anteprima desktop/mobile, mini toolbar, ricerca, resize pannello, selezione elemento con focus | File di lavoro in browser; toolbar responsiva di base | Non completo né approvato dall'operatore nella UX |
| Esportazione | HTML di lavoro, export pulito nelle prove R2/R3, salvataggio/rientro | Originale immutabile incorporato; file lavoro autonomo; clean source-preserving, no-op e full Undo byte-identici | Rappresentazioni distinte, testate su due topologie e pagina MAIOS pubblicata |
| Accessibilità e piattaforme | Esperimenti Chrome, gesti nativi | Picker con label, messaggi status, tasti standard; Linux Chrome automatizzato | **Non** prova completa screen reader, sola tastiera o Windows `file://` |
| Privacy/sicurezza | Portatore privato, dati originali nel workbench | Solo sorgenti statici fiduciati; HTML di lavoro include l'intero originale e non va condiviso | Non garantisce sanitizzazione di HTML arbitrario/paste e non sostituisce filtri dati scene |

## Scelte operative prima del rilascio

**Da stabilizzare nel neutro senza duplicare portatori:** identità del blocco in history/reopen; selezione accessibile; azioni minime su blocchi propri; clean export fedele. La [CI 45045156708](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45045156708) ha quattro job verdi su fixture indipendenti e pagina MAIOS live source-identical, per i percorsi esercitati.

**Rimanenti discriminanti critici:** prova umana Windows `file://` e caret/focus con tastiera, sicurezza degli input incollati e HTML autore, revisione UX su contenuti reali, eventuali perdite dopo riapertura, controllo dei limiti di non supporto. Per non vincolare il prodotto a una topologia, un comando che manca non deve comparire nella UI finché il carrier non può esercitarlo coerentemente.

**Da non trasferire automaticamente:** ridimensionamento/riordino delle sezioni originali, palette globali e preview nativa specifica del sito. Occorre una diversa competenza di trasformazione che dimostri come incidere sul documento autore senza rompere responsive, CSS e script.

**Decisione di release ancora aperta:** quali gesti oltre il nucleo minimo formano una versione utile senza introdurre vulnerabilità o false promesse; il passaggio a `maios_it/main` è indipendente e non discende dalla CI.

