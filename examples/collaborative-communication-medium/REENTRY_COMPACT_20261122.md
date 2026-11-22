# MetaCanvas + MetaEditor — checkpoint di rientro compatto · 22 novembre 2026

**Scopo:** ridurre la lunghezza e il costo dei rientri in ChatGPT, conservando l'avanzamento reale senza ripetere l'intera conversazione. Questo è un cursore operativo, non autorità su release o prova esterna.

## Risultato effettivo
- MetaCanvas generale, Playground r4 IT/EN e Studio21 IT/EN: cinque sorgenti K-UX-AI confrontate con copie della repository del sito `maios_it`, blob Git corrispondenti.
- [PR K-UX-AI #2](https://github.com/GrazianoGuiducci/k-ux-ai/pull/2) su `work/metacanvas-metaeditor-stabilization-20261122`: aperta **in bozza**, controlli di baseline/CI riusciti; non equivale a rilascio stabilizzato.
- MetaEditor Bridge11: versione di lavoro privata nel ramo `maios_it/work/metaeditor-current`; l'operatore riferisce «Nella versione 11 non vedo problemi». Non è un editor universale.
- Neutral Probe R2: file e generatore nella [cartella esperimenti privata](https://github.com/GrazianoGuiducci/maios_it/tree/work/metaeditor-current/workbench/metaeditor/experiments); esercitati editing, inserimento, spostamento, Undo, export lavoro e pagina pulita su desktop/mobile. Struttura ancora vicina a MAIOS.
- **R3 su pagina MDN indipendente:** in questa conversazione sono stati prodotti e provati artefatti locali (HTML di test e ZIP). Le prove riferite comprendono export no-op identico all'originale, modifiche circoscritte a `main`, Undo/Redo, salvataggio/riapertura e desktop/mobile; è emersa e stata corretta una perdita del riferimento alla sorgente originale dopo salvataggio. **Non risulta un commit GitHub verificato di R3**: non dichiararlo persistito in repository o rilasciato. Identità dell'ultima copia fornita in chat: `MetaEditor_Independent_R3.html`, SHA-256 riferito `8af2f8b18605f25f8a0e2da9e965c46364cb2756964699c52af7ef940cf75189`; pacchetto `MetaEditor_R3_Prova_Indipendente.zip` (verificare gli allegati esatti al rientro).
- Nessun nuovo deploy `maios_it/main`. La prova umana su Bridge11 non certifica gli altri carrier, accessibilità, sicurezza o uso Windows `file://` di R3.

## Blocco materiale, non narrativo
La R3 resta un esercizio documentale in chat: occorre renderla raggiungibile con sorgente/build/test riproducibili nell'owner corretto e chiarire quali invarianti del documento l'adattatore può garantire. Il Gate B di [RELEASE_STABILIZATION_20261122.md](RELEASE_STABILIZATION_20261122.md) è **parziale**, non chiuso. Poi i gate C–F (regressioni MetaCanvas, accessibilità/compatibilità, candidata e distribuzione) restano aperti.

## Prossimo movimento, in una nuova istanza
1. Leggere soltanto questo checkpoint, la [guida di stabilizzazione](RELEASE_STABILIZATION_20261122.md), l'[handoff implementativo](WORK_HANDOFF_STABILIZATION_20261122.md) e [MetaEditor CURRENT](../../competences/ux-ai/collaborative-communication-medium/meta-editor/CURRENT.md); rivalidare PR e branch, senza rigiocare tutta la chat.
2. Recuperare gli artefatti R3 della conversazione o dal file Library **prima** di dichiararli disponibili; controllare SHA e ricostruibilità. Se non materializzabili, non inventare l'HTML: il codice/fixture va ricostruito dal builder verificato.
3. Chiudere soltanto il prossimo gate: consegna dell'adattatore e fixture neutri con test di regressione e prova di preservazione del documento; nel ricevente Codex usare il suo checkout nativo, non fingere di averlo modificato da ChatGPT.
4. Consegnare un risultato durevole per volta: codice + test + readback + limiti, poi un riepilogo breve. Non produrre molti allegati temporanei né aprire sottoprogetti mentre il gate corrente è ancora aperto.

## Regola di economia di contesto acquisita
L'operatore segnala blocchi ripetuti dell'istanza. Non attribuirne con certezza la causa a limiti non osservabili. In lavori lunghi: checkpoint essenziale owner-native, rientri selettivi, massima una risultante testabile per turno, tool calls raggruppate, nessun riversamento di interi file/log in risposta e passaggio tempestivo a nuova istanza. Conservare prove e stati nell'owner, non nella memoria verbosa della chat.

**Effetti non autorizzati o non eseguiti:** fusione PR, pubblicazione MetaCanvas/MetaEditor stabilizzati, push production, aggiornamento del sito live, esecuzione autonoma Codex.
