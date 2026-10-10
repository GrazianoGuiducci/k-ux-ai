# K-UX-AI → Kernel Nautico → sito: raccordo operativo per Codex

10 ottobre 2026. Stato: preparazione source-bound; nessuna integrazione/live publication autorizzata dalla sola esistenza di questo documento.

## Rientro sulle sorgenti correnti

**K-UX-AI** (`GrazianoGuiducci/k-ux-ai`): repo del medium pubblico indipendente. Branch candidato `work/ux-ai-ui-library-20261008`; v5.4.1 con `16-griglia-continuity-v541.html`, builder, test e ricevuta. Versione pubblica del package `0.1.0-alpha.1` non modificata. Manifesto, `KERNEL.md`, `docs/interface.md` e `docs/ui-library/CURRENT.md` possiedono la relazione UI generica. I dieci verbi della demo K-UX-AI sono **intenti sintetici**, non le dieci entità Nautico reali.

**Kernel Nautico** (`GrazianoGuiducci/kernel-nautico`): owner del dominio, degli eventi, della revisione/continuità prodotto e dei target pubblici. Main osservato `82896de01829752614d04cfa6e3ffacbd9544a0a`; branch candidato separato `work/ux-ai-entity-desk-20261008` a `81f6dfb426c930108ee4d0cc94f4505ab6398a21`, con `work/UX_AI_ENTITY_DESK_FIRST_VERTICAL_20261008.md`, `work/UX_AI_ENTITY_DESK_RETURN_20261008.md` e `work/UX_AI_ENTITY_DESK_EVIDENCE_20261008.json`. Contiene un ingresso alternativo `entity-desk.html` che usa dieci **target owner-native** e `public-bridge.js` (hello/command/confirmed state), senza sostituire la vista Atlas né collegare una chat host. Le prove precedenti di quel ramo sono 15/15 checks statici, **non browser**. Rileggere gli head prima di dipenderne.

**Sito/host Nautico**: l'operatore riferisce una versione precedente già presente su un sito, ma la sua URL/versione/deployment-owner non sono stabilite da questa sola sorgente. Non presumere che sia `maios_it`, `lab-d-nd-site`, `chatgpt_sites` o un iframe della demo. In `GrazianoGuiducci/maios_it`, il catalogo Prodotti registra Nautico come **presentation_pending** al suo readback del 6 ottobre: ciò non smentisce un'altra superficie sito reale. Codex con browser/computer-use e workspace pertinenti deve prima identificare la superficie effettiva, owner, codice e percorso di pubblicazione mediante prove, conservando l'eventuale stato più recente.

**Codex**: receiver con ambiente di implementazione/browser che potrà svolgere integrazione end-to-end quando selezionata. Prima entra dal proprio Boot, dalle competenze Code Medium Construction (fonte privata corrente tm7), UX-AI/Meta_Skill, Design Kernel e dai source owner dei due prodotti. L'accesso GitHub e la possibilità tecnica non autorizzano un deploy.

## Relazione tra i componenti

```text
source/domain/kernel Nautico
  oggetti / entità reali / contesto / eventi / revisione / permessi / autorità
       ↓ exposed bounded state + target identity + permitted actions
adapter di ricezione nel progetto Nautico
       ↕
K-UX-AI medium
  focus / card / spazio / motion / draft UI / gesto umano / observable readback
       ↕
host/site realmente qualificato
  bundle / viewport / chat host se esiste / persistenza autorizzata
       ↕
Codex come receiver di costruzione e prova
```

I dieci target Nautico (`nautico-presentazione`, `nautico-apprendimento`, `nautico-collaborazione`, `nautico-studio`, `nautico-cantiere`, `nautico-fornitori`, `nautico-showroom`, `nautico-bordo`, `nautico-assistenza`, `nautico-progetto`) **non** vanno rinominati o sostituiti per somigliare ai dieci verbi del demo KUX. La relazione fra intenti/gesti e entità/viste deve essere ricavata dal contratto Nautico e resa riusabile nel medium, non inventata nel sito.

## Contratti da ricomporre prima della consegna

1. Reperire sorgenti/ref e delta attuali dei due rami; **non** usare un HTML di screenshot come nuovo owner dei dati; conservare la presentazione 3D FORM/BUILD/LIVE/RETURN, la demo e le origini delle note/proposte.
2. Usare il contratto `createMedium({state, render, onAction})` e l'adapter del Kernel Nautico. Il bridge deve distinguere richiesta, stato/ack confermato, origine/revisione e fallimento/non disponibilità. Una stessa schermata aggiornata non è necessariamente un nuovo evento.
3. Conservare autonomia UI, continuità di layout, caret/focus/bozze, moduli accessibili, mobile/tastiera/reduced motion; leggere `v5.4.1` come qualità di interazione e il branch Nautico come struttura owner-native, non sceglierne uno cancellando l'altro.
4. La prima incarnazione può mantenere **una vista reale scrivibile** alla volta e altri pannelli informativi, finché il controller non dimostra gestione coerente di due viste scrivibili. La card non diventa una nuova fonte delle decisioni Nautico.
5. Solo quando l'host reale lo consente, connettere chat/form, notifiche e AI attraverso il loro controller. Le attuali notifiche e capacità demo restano esplicitamente dimostrative.
6. Per progettisti, operatori, fornitori, responsabili, clienti ed equipaggio: il contratto potrà ricevere identità/account, oggetto corrente, lifecycle, fonti e azioni ammesse dall'owner dell'ambiente. Ruolo dichiarato ≠ permesso. UI può adeguare forma e profondità, server/controller rivalida ogni effetto.
7. Qualificare prima l'esatto **sito di destinazione**: differenza fra versione host attuale, candidato compilato, credenziali/servizi, preview privata e stato pubblicato. Non inventare endpoint, mapping di domini o URL di deploy.

## Chi prepara / chi agisce

- **K-UX-AI owner:** medium neutrale, contratti, componenti riusabili, builder, regressioni, apprendimento UX/codice. La sua repo non possiede l'oggetto nave, la policy degli account o le sorgenti del sito.
- **Kernel Nautico owner:** schema/identità dei target, ruolo dell'entità nel lifecycle, origine delle fonti, bridge e applicabilità delle capacità/permessi reali, prova di continuità dei dati.
- **Sito/host owner (da qualificare):** route, bundle, assistente host, isolamento account, pubblicazione e ricezione reale. Altre superfici MAIOS possono semplicemente collegarlo e non ne diventano owner.
- **Codex receiver:** raggiunge le tre sorgenti, identifica il loro effettivo presente e implementa/testa la composizione selezionata nel checkout giusto. Non assorbe owner di competenze e dominio.
- **Operatore:** valuta il candidato integrato e seleziona distintamente eventuale merge/release/deploy e account/permessi/contatti esterni.

## Ordine del prossimo lavoro Codex, non pipeline obbligatoria

Freshness/owner → readback browser del sito già presente → confronto v5.4.1 / native entity desk / host → adattatore/composizione minima completa → QA reale con 10 ACK source-owned, presentazione, bozza, rientro, zoom, popup, keyboard, mobile, reduced motion, failure states → screenshot/receipt e differenze tornate alle competenze → candidato mostrato all'operatore.

**Stop prima di merge e pubblicazione**, salvo una nuova selezione esatta dell'effetto. L'operatore potrà quindi decidere quando sostituire la versione ospitata dopo aver visto il risultato.
