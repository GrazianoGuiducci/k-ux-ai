# K-UX-AI v5.1 — Campo preparato

Data: 10 ottobre 2026. Owner: `GrazianoGuiducci/k-ux-ai`, branch `work/ux-ai-ui-library-20261008`. Stato: **candidate lab, sintetico, non rilasciato**.

## Movimento reale e confine

Quattro screenshot e le indicazioni dell'operatore dopo v5.0 hanno selezionato la **Home come punto di preparazione del lavoro**, non solo ingresso grafico. La persona sceglie il contesto, combina attività e poi entra nel canvas. Sono stati indicati anche: un selettore dei cinque contesti subito disponibile, pulsante d'ingresso percepibile solo quando la preparazione è pronta, tour facoltativo, rimozione dell'anteprima duplicata nelle schede aperte, maniglie riposizionate dalla geometria finale dopo drag avatar e ridimensionamenti e migliore occupazione della regione destra e del basso.

## Risultante implementata

- [HTML autonomo 12](12-griglia-campo-preparato.html) ricostruibile dalla baseline v5.0 mediante builder con hash di ingresso verificato (builder, test e baseline nel pacchetto ZIP fornito all'operatore).
- La Home usa i cinque contesti esistenti, mostrando chip leggibili che aggiornano **l'unico** `state.activeContext`, condiviso con il selettore del workspace. `state.homeSelected` prepara attività *di vista*, distinte dallo scambio di ruoli delle tessere tramite drag.
- Il pulsante **Entra nel campo** è disponibile con almeno una selezione e pulsa brevemente, salvo reduced motion. Entra solo nel contesto e nelle attività preparate, riusando pannelli esistenti; le altre card diventano minimizzate, non eliminate, e conservano bozze. Il ritorno alla Home rende visibile la selezione. Su mobile c'è un comando Home accessibile nella topbar perché la sidebar è nascosta.
- Un tour nativo a tre passi spiega contesto, scelta attività e ingresso; è chiudibile, opzionale e privo di effetti. Il pulsante e il gestore di anteprima sono rimossi **dalla toolbar delle card aperte**; gli avatar non aperti mantengono la loro anteprima situata.
- La coordinazione dei divisori segue la geometria dei settori **dopo** l'assestamento della disposizione. Durante il drag del principale nasconde le maniglie secondarie, poi le riposiziona sui bordi effettivamente renderizzati; il divisore trascinato risponde direttamente al puntatore. Anche l'aggiunta di avatar posticipa il readback delle maniglie fino al nuovo layout.
- Con 3–6 medie affiancate il layout riempie righe e larghezza disponibile, distribuendo anche l'ultima card dispari; se il frame non basta rimane uno stack leggibile e scorrevole.

La UI continua a essere una dimostrazione locale del caso Nautico, **non** un controller di fonti nautiche autentiche. `selezione != apertura != effetto owner-native`. Non sono collegati LLM, Section Kernel, provider, filesystem PC/Codex, dati aziendali o autorizzazioni. Il codice è una trasformazione verificabile della baseline v5.0 esistente, non un altro controller runtime sovrapposto; la base rimane parzialmente monolitica, quindi non rivendicare refactor completo.

## Prove e identità

[Receipt](EVIDENCE_PREPARED_FIELD_20261010.json). Git blob HTML `ac8de5bf2597759e9098c680d0295f730df26b51`, SHA256 `b5f11f4227a92e4f731d595c904ba93ec26e702036ac280319b12f6438f4d007`, 311180 byte. Tre suite Chromium/Playwright `page.set_content`: **103/103 Home/configurazione + 26/26 divisori/riempimento + 23/23 regressioni/bozze = 152/152 controlli correlati**, zero JS page errors nei percorsi; `node --check` sui tre script. `file://` bloccato nel browser di prova: Edge reale dell'operatore, touchscreen, screen reader, utenti indipendenti, storage inter-sessione e dominio vero non validati. Un risultato di laboratorio non trasferisce automaticamente prove a un prodotto futuro.

## Continuità

La v5.0 precedente, `main`, Kernel Nautico e MAIOS restano invariati. Non è stato eseguito merge, deploy, release o contatto esterno. La differenza riusabile riguarda la Home che forma l'intento senza eseguire il lavoro e i divisori che si accordano alla geometria davvero conclusa. Restituire al già esistente Code Medium Construction e mantenere raggiungibile Interaction Quality del Design Kernel; non creare competenze duplicate o attribuire nuovi difetti al semantic owner Nautico.

**Prossimo passo:** osservazione dell'operatore in Edge del flusso Home → canvas → Home e dei divisori durante inserimento di un avatar e ridimensionamento di più medie.
