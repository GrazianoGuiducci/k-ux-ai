# K-UX-AI · Contratti di composizione delle superfici

**8 ottobre 2026 · candidato di costruzione nel prodotto K-UX-AI · non installato nel sito**

## Punto d'ingresso

Questo documento descrive **quali unità possono diventare operative nel medium K-UX-AI** e quali relazioni tecniche devono restare unite quando si adottano.

- Catalogo machine-readable e identità pinned: [`../../ui-library/catalog.v0.1.json`](../../ui-library/catalog.v0.1.json).
- Lettura dettagliata delle sorgenti: [`SOURCE_ADOPTION_20261008.md`](SOURCE_ADOPTION_20261008.md).
- Prototipi HTML autonomi: [`../../labs/nautico-ui-v3/`](../../labs/nautico-ui-v3/README.md).
- Core già esercitabile: [`../../src/medium.js`](../../src/medium.js) (`receive`, `dispatch`, `observe`).
- Proprietà semantica di UX-AI: [`Meta_Skill/ux-ai-kernel-design`](https://github.com/GrazianoGuiducci/Meta_Skill/blob/main/skills/ux-ai-kernel-design/SKILL.md).
- Proprietà del design: [`D-ND Design Kernel`](https://github.com/GrazianoGuiducci/d-nd-ux-ai-seed/blob/main/DESIGN_KERNEL.md).

Questo è un **cabinetto di sorgenti, contratti e prove**. Non rappresenta un sistema THIA installato, un nuovo runtime o una libreria contenente copie autorizzate di tutti i componenti upstream.

## Prima relazione — la UI non possiede il lavoro

```text
Kernel Nautico / altro owner
  oggetto + fonte + evento + stato + competenze + azioni autorizzate
          ⇅
K-UX-AI medium
  stato esposto / gesto umano / osservazione / percezione
          ⇅
Surface composer
  avatar ↔ card ↔ floating ↔ dock ↔ split ↔ full
          ⇅
Modulo ricevente
  chat / form / editor / dashboard / inspector / 3D / documento
          ⇅
Host
  disponibilità di mezzi, trasporto, persistenza, provider, effetti
```

Una **entity del dominio** e un'**entity percettiva aperta nel workspace** non sono la stessa cosa. L'avatar può cambiare forma mentre `id`, provenienza, stato e revisione dell'oggetto rimangono nel kernel di dominio. Lo stesso lavoro può non richiedere alcuna mutazione visuale.

### Eventi, status, messaggi

- `snapshot` esposto ≠ nuovo evento; rileggerlo non deve produrre un avviso fittizio.
- L'evento deve mantenere identità dell'owner, revisione e disponibilità/applicabilità della fonte; a parità di schermata due eventi possono restare causalmente distinti.
- Badge, pulsazione, avviso contestuale o chiusura suggerita devono derivare da una differenza realmente materiale o dal gesto operatore, non da una regola estetica di animazione.
- `interazione UI`, `proposta`, `modifica locale`, `invio esterno`, `approvazione` ed `esecuzione` sono classi di effetti distinte.
- L'assistente conserva capacità di spiegare anche quando non può eseguire; non riceve automaticamente autorità perché la finestra è stata aperta o portata al centro.

## Comportamento delle finestre — unità completa

Ogni componente che occupa il workspace ha **un'identità stabile e una geometria percepibile**, e distingue lo stato del lavoro dalla disposizione scelta per mostrarlo.

| Forma | Contenuto | Continuità necessaria |
| --- | --- | --- |
| Avatar | ingresso, stato essenziale, eventuale attenzione attribuita | origine/destinazione della finestra e stato non perso |
| Card rapida | titolo, attività, evidenza o azione utile | stesso `entityId`, niente duplicazione del controller |
| Floating | contenuto pertinente e ridimensionabile | geometria manuale ripristinabile; mouse/touch/tastiera |
| Dock / sidebar | lettura o collaborazione vicino al focus | altri pannelli fanno spazio quando possibile, senza occupare il primario |
| Split | due relazioni simultanee / confronto / chat+modulo | proporzione, limite minimo, recovery gutter |
| Full-page | modulo completo, presentazione, editor o analisi | ritorno alla geometria/alla selezione precedente |

**Non adottare soltanto lo scheletro della finestra.** Da THIA/DOMUS e Agentic UX Seed devono viaggiare insieme:

1. avatar e frame di origine, open/close e chiusura che torna a una posizione riconoscibile;
2. drag senza easing mentre la persona controlla l'oggetto, resize e soglie coerenti;
3. passaggio compact → readable al primo drag, drag-down che sgancia il fullscreen, re-target di un'animazione interrotta;
4. dimensione manuale distinta da quella di `due`, `quattro`, `dock` o `full`, con recupero della posizione personalizzata;
5. draft, selezione, conversazione, scroll utile e focus preservati nelle trasformazioni;
6. persistenza con namespace del ricevente per geometria, sessione e split; nessuna chiave THIA copiata indiscriminatamente;
7. comandi e stati corretti su viewport stretti, zoom e in `prefers-reduced-motion: reduce`;
8. apertura di un *vero modal* con contenimento del focus solo quando quel contenuto lo richiede. Floating e inspector non devono bloccare tutta la pagina per default.

### Direzione e tempo del movimento

Il movimento serve a rendere percepibile dove va a finire ciò che si chiude e da dove nasce ciò che si apre. La sorgente Lab impiega transizioni di geometria intorno a **1,21 secondi**; questa è una proprietà della sua implementazione, **non una durata normativa**.

Il sorgente Lab elimina lo stato aperto dalla vista con un timeout intorno a **190 ms**, mentre alcune transizioni CSS durano più a lungo. Il nuovo port deve verificare la conclusione *effettiva* dell'animazione, evitare cut-off, gestire un nuovo gesto durante il movimento ed evitare salti di focus. Non imporre un timer ad ogni scheda per imitare la sorgente.

Per i controlli puntuali usare un movimento breve; per le trasformazioni strutturali più ampie scegliere una durata che preservi l'orientamento. In reduced motion consegnare lo stesso significato con una configurazione statica e un marcatore persistente quando pertinente.

## Adattamento responsive **dentro il modulo**

Un modulo in un dock desktop di 420 px ha vincoli diversi da un desktop full-page anche se la viewport è la stessa. Il ricevente deve poter osservare la **larghezza disponibile del frame**.

Dal Lab `domus-widget.js` osserviamo soglie di servizio come 940, 816, 767 px e una modalità mobile sotto 768 px; non sono regole universali. Contano soprattutto le trasformazioni che inducono:

- Chat/Form affiancati con splitter su frame capiente;
- Chat **oppure** Form su tab quando il frame non può mantenere entrambe le aree leggibili (non due colonne compresse né nested-scroll trap);
- Header/azioni riaggregati su frame stretto;
- Campo operativo primario conservato; sidebar/gutter/modal decidono la propria collocazione senza rubare righe al canvas;
- Quando il layout ricompone il contenuto, non cancellare `textarea`, input allegati, bozza né la decisione non ancora confermata;
- Una sezione guidata può aprirsi e spostare il viewport quando il suo contenuto diventa una nuova decisione; selezione reversibile non significa avanzamento implicito.

## Canvas prima del chrome

Il caso Nautico ha mostrato il costo dei titoli troppo grandi, degli stati ripetuti e delle barre permanenti. Il laboratorio v3 usa una **barra operativa compatta** e un menu di funzioni secondarie: nel confronto registrato a **1600×900**, il canvas misurato passa da circa **631** a **735 px** di altezza. È una misura locale sullo stesso prototipo, non un benchmark generalizzato.

Un megamenu è pertinente quando permette di ritrovare i gruppi senza imporre un percorso profondo. Un titolo può ridursi quando la situazione attiva è già riconoscibile; una breadcrumb o pannello dovrebbero comparire quando migliorano il prossimo gesto, non per decorazione.

La navigazione per **intenti neutri** è un ingresso, non un menu fisso di modalità. `Capire`, `Fare`, `Controllare`, `Esplorare`, `Progettare` ecc. possono rendere raggiungibili le entity effettive; il contesto aziendale e la semantica del Nautico rimangono distinti dall'azione che la persona vuole compiere.

## Chat, form, editor e dashboard non sono varianti del testo della chat

**Chat**: sorge quando dialogare con un assistente contestuale cambia la comprensione o il movimento; l'host deve fornire adattatori reali per contesto, conoscenza, competenze e trasporto. La sola presenza di un avatar non prova un AI attivo.

**Form**: raccoglie input accettati, distingue ignoto/derivato e invalida risposte dipendenti; l'invio è esplicito e del suo controller. Il modulo può essere assistito dalla stessa conversazione senza creare un secondo stato canonico.

**Editor**: conserva bozza, versione, selezione e rapporto fra chat, canvas e metadati. SITEMAN Studio porta un modello di composizione a pannelli, ma la sua pubblicazione e le sue credenziali non viaggiano con il widget.

**Dashboard/Monitoraggio**: stato e segnali appartengono alla fonte; quattro card monitor non implicano quattro processi autonomi o una sincronizzazione multiutente già disponibile. Full-page e split possono espandere la lettura senza approvare un effetto.

## Sorgente unica, incarnazioni diverse

I componenti React di Agentic UX Seed restano nella loro libreria; il Lab dispone di una chat **vanilla JS** realmente scritta. K-UX-AI attualmente usa un medium minimale JS e prototipi HTML autonomi. Se il primo ricevente Nautico continua in JS, possiamo **estrarre un nucleo headless e portare il comportamento vanilla pertinente**; se Codex selezionerà un bundle React, dovrà importare l'unità Seed con dipendenze/CSS/adapter completi.

Le fonti originarie nel catalogo sono **collegamenti a commit fissati**, non codice copiato. Agentic UX Seed dichiara PolyForm-Noncommercial-1.0.0 in `package.json`: non assumere una licenza commerciale riutilizzabile soltanto perché i progetti hanno lo stesso autore. Qualificare l'effetto di distribuzione con l'owner quando viene selezionato.

## Cosa è disponibile ora, e cosa no

**Disponibile in questo branch:** due HTML v3 autonomi, codice laboratorio funzionante, sorgenti originali pinned, catalogo di moduli, conoscenza di integrazione, ricevente K-UX-AI (`createMedium`) e ricevute storiche attribuite.

**Non disponibile in K-UX-AI runtime:** chat THIA con provider/gestore, port ufficiale `ThiaChatSeed`, autorità MAIOS/THIA, dashboard ed editor collegati, due pannelli Nautico scrivibili contemporaneamente, live capability learning, notifiche causate da reali eventi aziendali, integrazione del sito pubblico.

## Prove minime prima di dare a Codex la UI finale

1. Verificare con un browser moderno i due HTML **esatti** che il branch contiene, desktop, tablet, mobile e zoom 200%; non riusare alla cieca le ricevute di un diverso percorso su disco.
2. `avatar → card → floating → dock → split → full → ritorno → avatar`, anche durante interruzioni e slow transitions.
3. Ricomposizione `libero → due/quattro → libero`, mantenendo la geometria precedente, senza mascherare i pulsanti e senza perdita di draft.
4. Nel modulo Chat/Form, testare dimensione del frame, split, tab mobile, recupero input ed effettivo controller host al confine.
5. Verificare `Escape`, Tab/Shift-Tab, ritorno a trigger visibile, backdrop solo per vero modal, focus di tastiera dopo chiusura del megamenu.
6. Legare avvisi e proposte a eventi owner-native; separare lettura, interpretazione, domanda AI, azione e receipt.
7. Usare un caso reale del demo Nautico con sorgente/revisione: nessun `snapshot` ripetuto diventa per ciò stesso un nuovo evento.
8. Testare il nuovo componente originale nello stesso receiver e confrontarlo con il sorgente adottato; registrare tutti i controesempi prima della promozione.

**Stop condition:** K-UX-AI rimane il luogo del sapere componibile. Codex integra un solo modulo selezionato nel Site quando l'operatore ha visto e scelto la composizione; questa nota non esegue quel passaggio.
