# MetaCanvas / MetaEditor — controllo di qualità dalle sorgenti, 24 novembre 2026

**Domanda autoriale:** prima di riprendere il lavoro, controllare la qualità sotto i vari aspetti, ricomprendendo le possibilità dai file sorgente; osservare il saper fare che emerge per integrarlo nel sistema quando sarà sufficientemente compreso.
**Owner:** MetaEditor Evolution / Collaborative Communication Medium. **Stato:** riesame e nuove prove, nessuna modifica del codice prodotto, nessun rilascio.

## Differenze che cambiano la scelta

1. **Il problema della superficie non nasce oggi.** [Bridge08, 19 novembre](../../../competences/ux-ai/collaborative-communication-medium/meta-editor/references/BRIDGE08_UX_ACTIONS_FOCUS_20261119.md) e i file [JS](bridge08_ui.js), [CSS](bridge08_ui.css) e [builder](bridge08_build.py) già possiedono ricerca azioni, riferimento contestuale, disclosure progressiva, Focus volontario e roundtrip della UI. Il Focus aveva già richiesto la correzione della grid a una colonna (1019 → 1150 px nel precedente esercizio). Il [Bridge07 builder](bridge07_build.py) possiede contratto begin/setText/commit/cancel/undo/redo e adattatori per due carrier; Bridge08 dipende da esatti sorgenti Bridge07 e dalla loro API. Il [Bridge11 privato corrente](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/workbench/metaeditor/CURRENT.html), blob 9f4f843124f8619eee02ece40a7efc1470881b07, contiene il livello Bridge08 oltre a editing rich text, sezioni, proprietà e preview. **Disponibile non significa già trasferito nel candidato R1.** Il prossimo movimento non deve inventare ancora Focus o una palette concorrente: riconciliare le implementazioni e scegliere i contributi pertinenti al runtime reale.

2. **Campo di distribuzione incompleto.** [Manifest](../distribution-manifest.json) riletto; i cinque sorgenti K-UX-AI main coincidono per Git blob con i cinque asset di maios_it/main, e i pin sono ancora corretti. I cinque sorgenti hanno ciascuno esattamente una occorrenza di ogni ancoraggio dei quattro filtri mancanti del [builder privacy](../../../tools/build_studio21_public_projection.py) e una del gestore Arrow-move precedente al [builder keyboard](../../../tools/build_studio21_keyboard_section_move.py). I builder correnti coprono solo Studio21 IT/EN. L'identità degli ancoraggi rende concreta la possibilità di propagazione all'editor generale e ai due Playground, **non prova il comportamento dei tre candidati non ancora costruiti**.

| Sorgente | Git blob, coincidente con asset MAIOS in repository | Ancore privacy | Ancore keyboard |
|---|---|---|---|
| AI_Collaboration_Studio.html | d057d68c60061dd9e8f5c2d704cfff2016ea19b1 | 1,1,1,1 | 1 |
| MetaCanvas_Guida_Playground_r4_IT.html | e26321eca0a00a4f840fb3b47bc2e4c45e511464 | 1,1,1,1 | 1 |
| MetaCanvas_Guida_Playground_r4_EN.html | f5e6cb9c9ce3d5156cf6f12b331c2e9d0b6dc808 | 1,1,1,1 | 1 |
| MetaCanvas_Studio21_Consulenza_IT.html | cba76881d4afbb48c0fa38f76bbd04eda764f7c9 | 1,1,1,1 | 1 |
| MetaCanvas_Studio21_Consulenza_EN.html | dfddc6d1de728b45996a3f6628ea657da8db33f9 | 1,1,1,1 | 1 |

La coincidenza è dei repository, non nuovo readback dal VPS. La PR #2 e i builder restano candidati. Priorità di integrità: estendere in modo verificabile le correzioni comuni a tutti i portatori pertinenti, mantenendo contenuti, lingua e guida specifici. Una sorgente comune dei contributi compatibili può produrre HTML autonomi; non occorre imporre un formato comune a scene e DOM responsive.

## Prove di uso aggiuntive sul file R1

Artefatto effettivo IT di CI [45234069873](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45234069873), SHA-256 669e074f72abe0f43d5c21096031fcf9f0cadb245c8542879cd4927f78d0bec9, 298755 byte. I cinque job sono stati riletti verdi. In questo host esiste Chromium + Playwright: apertura via set_content del file effettivamente scaricato, interazioni click non forzate, viewport desktop 1440×850, 1024×768 e 390×850. Non equivale a Chrome Windows file:// o dispositivo touch umano. Nessun pageerror nei percorsi nuovi.

| Evidenza riprodotta | Significato |
|---|---|
| 1440: canvas 1098×618 → 758×426 con Dimensioni. | Il pannello sottrae spazio al referente. |
| 1024: canvas 708×398 → 359×202 con Dimensioni. | Circa metà larghezza e un quarto area utile; il solo ingombro mobile non rappresenta il problema. |
| 390: canvas interno 900×506, viewport 366×307; comincia a y=454, contenuto tagliato nella viewport. | La navigazione e la guida si sommano al minimo di larghezza del canvas; Focus da solo va verificato rispetto a fit/zoom/pan, non assunto risolutivo. |
| Aprire Dimensioni e inviare un evento resize: la barra R1 ricompare mentre l'ispettore resta aperto, a tutte e tre le larghezze. | visualActionsSync ignora lo stato drawer-open. Il controllo va legato al ciclo di interazione, non soltanto alla selezione. |
| Selezionare d1-h, aprire Modifica testo, premere OK senza cambiare testo: d1-h ancora selezionato ma barra assente. | Rientro dal gesto senza commit/render non risincronizza la UI. |
| Selezione d1-h, focus da tastiera su d1-c, Enter: mini editor aperto, evidenziazione resta d1-h. | Il keydown nativo apre openQuick per il nodo focalizzato senza selezionarlo. Referente dell'azione ed evidenziazione possono divergere. |
| Cinque template agentici presenti all'avvio, nascosti dietro Strumenti e details Template agentici chiuso. | La facoltà è presente, ma non raggiungibile direttamente nel momento iniziale della composizione. |
| Click reali Strumenti → Template agentici → primo modello → Sotto; salvataggio tramite Salva lavoro; riapertura del vero HTML scaricato: 7 → 8 schede, 8 righe nel rail, una nuova scena conservata. | Riutilizzo e persistenza esistono già. Non reinventare il motore template. |
| Stessa prova con link privato sintetico fra due nodi pubblici nella prima scena, copia lavoro conserva il link; copia pubblica da Strumenti → Salva ed esporta lo esclude anche come marker nell'HTML; markup della barra R1 assente da entrambi; riapertura del work senza barra duplicata. | Prova circoscritta R1 di persistenza e proiezione pubblica, non certificazione generale privacy o verifica di tutte le combinazioni. |
| ZIP MetaEditor 1.0 RC1 9/9 checksum; ZIP Studio21 Privacy RC1 5/5 checksum; lista file coerente con i manifest. | Integrità di pacchetti precedenti ancora utile, non giudizio di usabilità. |

## Qualità della prova, documentazione, mantenibilità

Il [test visuale R1](../../../tests/metacanvas-studio21-visual-actions.browser.py) prova selezione e testo nativi, apertura del mini editor e dell'ispettore, duplicazione/history, export pubblico senza barra, screenshot. Usa force=True per la selezione, e click programmatici per diversi comandi di salvataggio/history. Verifica accesso alle proprietà, non una modifica completa di misura/stile. Non riapre l'HTML di lavoro scaricato nel suo percorso precedente. I job privacy/relazioni/AI sono esercitati sul candidato privacy precedente, non tutti sul file finale R1. Il job Windows esercita il laboratorio HTML neutro, non R1. **Cinque job verdi non equivalgono a cinque portatori di prodotto verificati**, e non equivalgono a una prova d'uso. Integrare le prove nel candidato finale e distinguere test di contratto da navigabilità reale.

[README.it.md](../README.it.md) indica ancora il vecchio SHA-256 c8c1be74... del download storico Studio20 anziché il pin cbbafe148... del generale corrente nel manifest. Anche la localizzazione richiede controllo: nella sorgente EN diversi comandi del runtime, ad esempio l'etichetta nativa Chiudi la modalità di modifica, restano italiani; R1 traduce i propri quattro comandi ma non l'intero ambiente. Non certificare un'interfaccia EN completa dal nome del file.

La struttura di scena, i template, le relazioni, la history e l'AI roundtrip nativi sono un patrimonio consistente; il difetto di prodotto riguarda integrazione/discoverability e coerenza delle superfici. Bridge11 è un portatore di pagina specifico, non un editor universale. La RC neutra conserva il lavoro source-preserving, non sostituisce l'editing visuale originario.

## Conseguenza sul lavoro

- Prima sistemare le correzioni comuni di integrità nei cinque portatori, senza pubblicare una correzione limitata alla demo come chiusura di MetaCanvas.
- Sul vero Studio: riconciliare Focus/Flat, orientamento, barra e selezione/uscita dal gesto; provare la modifica di proprietà nello spazio utile, e la raggiungibilità delle funzioni senza pannelli concorrenti. Riutilizzare Bridge07/08 dove applicabile, non sovrapporli alla cieca.
- Rendere i template nativi una possibilità evidente all'ingresso e conservare il percorso composizione → modifica → salvataggio → rientro. Per la pagina web, partire da Bridge11 e dal suo motore di modifica reale, integrando selettivamente la robustezza del laboratorio. Non fondere i documenti.
- Verificare il candidato esatto che sarà distribuito (regressione, gesti, resa, persistenza e proiezioni); poi un test d'uso dell'operatore. Niente nuovo prototipo o rilascio soltanto per generare un altro artefatto.

## Osservazione del metodo — materiale per MRO/Meta-Focus, non una nuova competenza matura

Il controllo ha cambiato la scelta **prima di un nuovo intervento**: (a) recuperando una facoltà già implementata (Focus), (b) allargando il referente da una demo ai cinque prodotti effettivamente raggiungibili, (c) confrontando contratto, sorgente, artefatto e uso, (d) esercitando passaggi non coperti dalle prove precedenti. Il valore è la differenza che cambia il prossimo gesto, non il numero di file letti, test o rapporti. Per il prossimo esercizio osservare se questa ricomposizione avviene durante la nascita della soluzione e se evita duplicazioni/omissioni senza introdurre audit rituali. [MRO](https://github.com/GrazianoGuiducci/Meta_Skill/blob/main/skills/meta-skill-semantic-kernel/references/MRO_TASK_FIELD_COMPREHENSION_2026_11_19.md) e [Meta-Focus](https://github.com/GrazianoGuiducci/Meta_Skill/blob/main/skills/meta-focus/SKILL.md) possiedono già la funzione generale: il caso concreto torna alla loro osservazione, non crea un nuovo kernel. La misura di assimilazione futura resta aperta.
