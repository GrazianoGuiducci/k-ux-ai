---
name: meta-editor-evolution
description: Formare ed evolvere il MetaEditor di MetaCanvas come capacità riusabile di modifica diretta, composizione e trasformazione documentale per pagine web e presentazioni; attivare quando il gesto, l'architettura o la fedeltà dell'editing richiedono costruzione o correzione.
owner: GrazianoGuiducci/k-ux-ai
parent: competences/ux-ai/collaborative-communication-medium
status: candidate-formed-2026-11-16
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

## Attuale prova iniziale
La correzione R4 è una fonte già esercitata: una prova dell'inspector venne scambiata per prova di editing diretto, benché Studio 20 possedesse già `contentEditable` per i nodi. [GUIDE](GUIDE.md) conserva il meccanismo e il banco da verificare. [CURRENT](CURRENT.md) distingue capacità formata, prototipo costruito, test e uso reale. La prova su un nuovo banco ancora non può essere dedotta da questo testo.
