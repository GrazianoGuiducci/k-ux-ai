# K-UX-AI · Griglia v4.4 — slot intelligenti e ambiente di sezione

Data: 9 ottobre 2026. **Candidato privato nel branch di lavoro**, non release. Fonte: schermata e richieste dirette dell'operatore sulla v4.3; ricevente del primo caso Kernel Nautico (dati dimostrativi).

## Differenza che forma il movimento

L'identità del focus della v4.3 non bastava a garantire la collocazione delle nuove card: in Libero la geometria poteva sovrapporsi, mentre trascinare un'intestazione in griglia poteva sganciare tutto il campo. L'anteprima rapida non aveva un movimento/resize completo. La forma di una scheda può inoltre approfondirsi in un ambiente di lavoro specifico, senza diventare automaticamente un kernel.

Conservare distinti:

```
oggetto/contesto/owner/fonte/revisione
!= attività presente
!= focus semantico prioritario
!= ruolo percettivo (grande/media/piccola/full)
!= surface di ambito/Section Kernel effettivamente formato
!= assistente AI connesso
!= autorità sull'effetto
```

## Composizione UI del prototipo

- **Solo:** una card usa tutto il campo. **Due:** condividono il campo. **Tre o più:** si distinguono la superficie principale Grande, una Media e una Piccola; ulteriori schede scorrono in righe successive. 2/3/4 colonne e Libero restano possibilità selezionabili. Su mobile l'espressione diventa stack scorrevole senza perdita degli oggetti.
- **Mantieni focus:** il click sull'avatar aggiunge la card come complemento quando il blocco è attivo. Una promozione esplicita tramite Porta al centro/mappa rimane consentita. Il lock non pretende di bloccare un nuovo intento dell'operatore.
- **Mappa:** l'icona ▦ dell'avatar può mostrare Grande, Media, Piccola al passaggio del mouse, col focus da tastiera o con click. Anche la quick preview può aprirla. Il click ordinario sull'avatar continua a essere l'ingresso principale.
- **Drag:** in griglia un gesto intenzionale assegna lo slot tramite drop, senza cambiare l'intero campo in Libero; il trascinamento da avatar e la mappa sono percorsi alternativi. Libero conserva la disposizione manuale. Il movimento con il puntatore non viene rallentato.
- **Motion:** le transizioni di ricomposizione e auto-resize convergono a circa 750 ms, con stato finale corretto senza animazione e in reduced motion. Micro-cue possono essere più brevi.
- **Preview:** regione di sola lettura, X/Y drag, resize diagonale e via tastiera, con affiancamento o promozione esplicita. Non apre di per sé una nuova attività e non attribuisce nuovi fatti.
- **Ricomponi:** ridistribuisce gli spazi senza cancellare i contenuti, la sequenza causale o il focus selezionato; un pannello full ritorna al contesto precedente.

## Ambiente della scheda e possibile SK

La v4.4 implementa un **Section Workspace sintetico** raggiungibile dal pulsante ◇ della card. È un solo componente con pannelli interni Quadro / Fonti / Conversazione / Collegamenti; conserva note locali attribuite, bozze durante i cambi di tab e collega altre schede come complementari. L'azione «AI di sezione» è **disabilitata** perché nessun provider AI o sottokernel operativo è connesso. Questo esercita la navigazione locale, non coordinamento autonomo.

Un futuro SK non nasce perché la card abbia menu, avatar, subview o chat. La competenza e l'eventuale owner devono emergere da funzione, continuità, identità, fonte e autonomia operativa reale. Kernel Nautico ha già una topologia di owner federati e distingue Domain / Enterprise / Project / Vessel nei documenti `KERNEL.md` e `docs/ENTERPRISE_BOOTSTRAP_AND_KERNEL_TOPOLOGY_0_1.md`; non duplicarla in K-UX-AI.

Contratto futuro candidato:

```
owner Nautico / azienda / progetto / istanza
 + object, source, revision, event, role, lifecycle, allowed effect
 -> section context capsule
 -> K-UX-AI medium: section state + readback + operator intervention
 -> pertinente owner-native competence / optional real section kernel / AI receiver
 -> attributed proposal or contribution
 -> owner-authorized effect gate
 -> effect receipt + learning return to responsible owner
```

L'AI locale non eredita privilegi dall'avatar. I contributi di un altro ambito mantengono origine, significato, fase temporale e competenza; il kernel Nautico può coordinare ciò che gli appartiene senza diventare autorità universale sugli owner esterni.

## Prova e limiti

HTML: [v4.4](05-griglia-ecosistemi-smart-slots.html). [Receipt](EVIDENCE_SMART_GRID_20261009.json).
Tre suite **correlate** in Chromium Playwright `page.set_content` hanno passato 23/23, 26/26, 10/10 controlli (59 complessivi), zero errori JS di pagina nei casi osservati. Coprono 1/2/3+ e 8 schede a 1680/1040/390/375 px, focus bloccato, drag slot, menu hover/keyboard, quick peek X/Y/resize, full/ESC/ritorno, ricomposizione, sezione/bozza/note/collegamenti. Le prove riproducibili sono consegnate anche nel pacchetto locale di questo passaggio.

**Non provato:** Edge con apertura file:// dell'operatore, touchscreen e screen reader fisici, comprensione umana indipendente, sorgenti Nautico reali, un SK installato, eventi enterprise, competenze evolute automaticamente, inferenza AI, autorizzazioni o site MAIOS. La v4.3 e le sue prove restano genealogia separata. Non trasferire test da una versione all'altra.

**Stop:** osservazione dell'operatore della v4.4. Il prossimo eventuale movimento con una fonte vera di Nautico richiede il suo receiving owner e una condizione materiale distinta. Nessun merge/release/deploy/contatto esterno.
