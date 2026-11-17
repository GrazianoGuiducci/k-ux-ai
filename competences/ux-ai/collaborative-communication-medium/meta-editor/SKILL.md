---
name: meta-editor-evolution
description: Formare ed evolvere il MetaEditor di MetaCanvas come capacità riusabile di modifica diretta, composizione e trasformazione documentale per pagine web e presentazioni; attivare quando il gesto, l'architettura o la fedeltà dell'editing richiedono costruzione o correzione.
owner: GrazianoGuiducci/k-ux-ai
parent: competences/ux-ai/collaborative-communication-medium
status: candidate-with-neutral-lab01-observed-2026-11-16
---

# MetaEditor Evolution — competenza di costruzione ed evoluzione

## Funzione
Questa competenza è il **saper formare, esercitare e migliorare l'editor** con cui l'operatore costruisce oggetti, testo, diagrammi, sezioni e documenti. MetaCanvas è il prodotto/medium; MetaEditor è una facoltà specializzata del [Collaborative Communication Medium](../SKILL.md), dentro K-UX-AI. Non è un nuovo kernel, un agente autonomo, un rifacimento indiscriminato delle pagine o la promessa di adattarsi a qualsiasi sito.

Il gesto umano è il referente operativo: seleziono un oggetto, modifico **sul posto** la parola, sposto, duplico, compongo e salvo; il sistema conserva identità, relazioni, differenza e possibilità di tornare indietro. Le capacità di pagina e di presentazione possono condividere interazione, storia, componenti e conoscenza, senza supporre che DOM responsive e scene 16:9 siano lo stesso documento.

## Ingresso situato
Al lavoro su editor di pagina, MetaCanvas, diagrammi, componenti, template, HTML importato o presentazione, raggiungi questo metodo **quando va formato/corretto l'editor**; se serve soltanto utilizzare un artefatto, resta in CCM. Prima di scegliere una libreria o iniziare una nuova versione, leggi il [CURRENT](CURRENT.md), poi il margine della [GUIDE](GUIDE.md) e il [riesame dopo R4](../references/metacanvas-editor-architecture-reset-20261116.md). Recupera la parte di Studio 20 che già possiede `contentEditable` dei nodi; non replicare una capacità esistente per ignoranza del routing. Verifica drift delle librerie esterne soltanto per il comportamento che cambia l'esito. Codice e guida formano il movimento con KA/FDLA, Meta_Skill, Interaction Quality, Perceptual Composition e Code Medium Construction secondo pertinenza, non per checklist fissa.

## Come opera
**Gesto prima di controllo.** Descrivi il minimo gesto concreto in termini verificabili (es.: doppio clic sulla scritta di un nodo → cursore dentro la scritta → digitazione → Enter salva → Undo recupera). Associa a quel gesto stato, focus, coordinate, commit e recupero. Non usare un campo in un inspector come surrogato del testo editato dentro il nodo. Una prova JavaScript che passa non equivale alla facilità d'uso reale.

**Sorgente e compatibilità.** Studia codice posseduto e soluzioni esterne per le loro funzioni, limiti, licenze e costi di integrazione; non adottare un engine perché famoso. Parti da un banco neutro e da documenti differenti; verifica separatamente fedeltà di import, trasformazione, esportazione e riapertura. Se una pagina contiene HTML/CSS/script o è un'app CMS/React, modifica regioni note attraverso un adapter; regioni ignote rimangono intatte o non editabili. Una dimostrazione sul sito MAIOS non diventa automaticamente compatibilità generale.

**Modello e proiezioni.** Distingui documento sorgente, modello di lavoro, nodo/elemento selezionato, geometria di diagramma, layout responsive, schema di presentazione, DOM transitorio, output esportabile e patch per Codex. Conserva ID e link, Undo coerente con un gesto, note private e confini della copia pubblica. Le toolbar e gli inspector del runtime non devono essere serializzati due volte nell'HTML di destinazione. Il provider immagini rimane responsabilità del ricevente: un prompt copiato non è una generazione.

**Esercizio e confronto.** Per ogni nuova capacità usa almeno un controllo nel browser che riproduca davvero il percorso dell'utente, un secondo caso non identico quando affermi generalità, e un round-trip del documento. Conserva la distinzione fra prova tecnica, percezione dell'operatore, fattibilità condizionata e ignoto. Correggi nell'implementazione il difetto osservato; se il problema nasce da una scelta di fonti, domande, architettura o criterio di prova, modifica anche questa competenza.

**Apprendimento causale.** Riconosci non soltanto errore ma anche valore nuovo, latenza, passo inutile o competenza già disponibile ma non esercitata. Riporta la differenza a GUIDE, lo stato a CURRENT, il codice al prodotto che ne è owner; cambia il routing se il sapere era presente ma non partecipava. Preserva distinti accaduto, compreso allora e compreso ora. Una scrittura in Git rende conoscenza raggiungibile, non prova assimilazione futura. Una correzione da parte dell'operatore non deve richiedere una seconda spiegazione in un rientro successivo.

## Confini e rapporto fra owner
- **K-UX-AI / CCM:** competenza, modello interattivo condiviso e prodotto MetaCanvas.
- **MetaEditor Evolution (qui):** costruzione, selezione dei mezzi, progettazione dei gesti, prove e apprendimento dell'editor.
- **D-ND Design:** conoscenza percettiva e qualità dell'interazione; **Meta_Skill / Meta_Metodo:** composizione, formazione e trasformazione delle competenze/metodi.
- **MAIOS.it / altri siti:** HTML, CSS, copy, rilascio e compatibilità specifica; **Codex/ricevente:** checkout, tool, autorizzazioni e applicazione di patch.
Nessun commit documentale pubblica il prodotto, modifica automaticamente il sito o attiva un altro agente.

## Gestione dell'elemento prima del tema — 17 novembre

Per ogni evoluzione dell'editor, la prima prova è l'azione concreta sull'oggetto pertinente: selezionare una sezione, inserire un elemento dove serve, convertire/duplicare/spostare, editare direttamente un nodo, collegarlo, annullare e riaprire senza sorprese. Raggiungere [Lab03 ed evidenza](../../../../examples/collaborative-communication-medium/meta-editor-lab/LAB03_README.md) e la [GUIDE corrente](GUIDE.md). Non fare di un nuovo catalogo di temi una risposta automatica alla difficoltà di manipolazione. La prova visiva della densità è parte del test: un allineamento su una sola riga faceva collidere i nodi dopo aver superato le asserzioni funzionali. Il nuovo metodo seleziona stato/controllo pertinente a sezione, oggetto e nodo e verifica bounding box oltre a Undo e round-trip.

## Tema e recupero delle capacità, 17 novembre

Quando il lavoro riguarda temi o design kit, raggiungi il [metodo di tema/composizione e il Lab02 locale](references/theme-library-20261117.md) e non introdurre per inerzia una «skin». Distingui sempre `tema/token`, `espressione locale`, `composizione suggerita`, `azione`, `documento` e `UI editor`. MAIOS possiede un campo cromatico comune con espressioni, D-ND è dark-first, i preset di presentazione sono proiezioni di laboratorio. Conserva tema e sua sorgente in una raccolta JSON portabile, ma non trasferire automaticamente contenuto personale o template privati. Se un ruolo o una grammatica è già presente in K-UX-AI, D-ND Design o nel sito owner, riusala anziché rifarla e prova il gesto completo dopo il tema.

## Attuale prova iniziale
La correzione R4 è una fonte già esercitata: una prova dell'inspector venne scambiata per prova di editing diretto, benché Studio 20 possedesse già `contentEditable` per i nodi. [GUIDE](GUIDE.md) conserva il meccanismo e il banco da verificare. [CURRENT](CURRENT.md) distingue capacità formata, prototipo costruito, test e uso reale. Il [banco neutro Lab 01](../../../../examples/collaborative-communication-medium/meta-editor-lab/MetaEditor_Lab01.html) è stato costruito e verificato con Node/Chromium per i gesti indicati nel [CURRENT](CURRENT.md). Restano non osservati uso reale dell'operatore, fedeltà su pagine HTML di terzi e assimilazione in un futuro caso non identico.
