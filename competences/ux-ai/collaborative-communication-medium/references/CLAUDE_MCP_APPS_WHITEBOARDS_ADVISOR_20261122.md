# Claude novembre 2026 — MCP Apps, Whiteboards e Advisor: sorgenti, discriminazione e possibilità per CCM

Data di ricognizione: 22 novembre 2026
Owner ricevente: K-UX-AI / Collaborative Communication Medium; MetaEditor Evolution per eventuale trasformazione di editor.
Statuto: **apprendimento da sorgenti pubbliche / comparazione di possibilità**, NON prova di integrazione, nuovo componente, benchmark prestazionale, decisione di adozione o disponibilità della UI dentro ChatGPT.
Intento operatorio: approfondire tre novità di Claude e confrontarle con le capacità MAIOS già realmente incarnate, senza trasferire autorità da sorgenti esterne al kernel.

## Fonti ufficiali e fatti osservabili

1. Anthropic, 10 novembre 2026, 'Your apps can now open in Claude': https://claude.com/resources/articles/interactive-connectors-full-tool. Una MCP App può esporre la UI a fianco della conversazione o a schermo intero, quando host e connettore la supportano; la disponibilità è in rollout. In public preview per sviluppatori. L'interfaccia e gli strumenti sono mediati dall'host; non equivalgono a un kernel semantico.
2. MCP Apps, documentazione del protocollo: https://apps.extensions.modelcontextprotocol.io/api/documents/overview.html. Risorsa HTML `ui://`, collegamento tramite metadata dello strumento, rendering sandboxed; messaggi bidirezionali host-view via JSON-RPC; `tools/call`, `ui/message`, `ui/update-model-context`; modalità di visualizzazione e privilegi stabiliti dall'host; CSP dichiarata. Risultati modello vs `structuredContent` UI restano distinti. Un protocollo di trasporto non specifica da sé continuità dell'oggetto, identità semantica o prova del cambiamento.
3. Anthropic, Whiteboards beta: https://support.claude.com/en/articles/18324319-get-started-with-claude-whiteboards. Persone e Claude co-editano, possono lavorare su un'area selezionata e convertire in doc/deck. Esportazione come file: PNG; può inviare a Miro/Lucid/Zoho Vani. Non importa una lavagna da file e al lancio Claude usa ciò che è sulla board, NON il contesto delle app connesse. Il co-editing in piattaforma non dimostra roundtrip semantico fra receiver diversi.
4. Anthropic, Advisor API beta: https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool. L'executor decide quando consultare un advisor; inferenza server-side riceve il transcript, produce suggerimento e ritorna all'executor; non possiede automaticamente fonti/owner o autorità di effetti distinti. Alcuni advisor restituiscono `advisor_redacted_result` cifrato lato client e consultabile dall'executor solo nel successivo turno server-side: la revisione esterna non è dunque sempre ispezionabile come testo. Richiede combinazioni compatibili e budget di chiamate; costi/performance dipendono dal task. Non assimilare `advisor` a una metacompetenza Meta_Skill.
5. Fonte dell'implementazione MAIOS/K-UX-AI: `competences/ux-ai/collaborative-communication-medium/SKILL.md`, `meta-editor/SKILL.md`, `meta-editor/CURRENT.md`, `references/metacanvas-editor-architecture-reset-20261116.md` e `GrazianoGuiducci/maios_it/work/metaeditor-current`. MetaCanvas Studio 20 ha un proprio documento scena `ccm.document.v1`; MetaEditor Bridge11 ha un portatore HTML di pagina con modifiche native, Undo/Redo, export e workbench privato; nessuna distribuzione di una MCP App o live multiutente è provata.

## Discriminazione utile per i prossimi movimenti

- **Medium vs host**: MetaCanvas/MetaEditor ha come prima identità un documento portabile e modificabile. Claude Whiteboards ha come prima esperienza una lavagna collaborativa nel proprio host. MCP Apps è un *adattamento possibile* che può portare una UI di K-UX-AI in più host senza sostituire il documento owner-native.
- **Referente stabile vs layout**: in una futura UI MCP non bastano post-it, frecce o testi; mantenere ID del documento, nodo, relazione, origine, significato della freccia, revisione e differenza. `ui/update-model-context` non coincide con memoria/continuità né prova che il modello abbia esercitato il sapere.
- **Oggetto vs diritto di modificarlo**: la UI può proporre o richiedere tool call; solo owner/controller del documento e host autorizzano gli effetti. Una conferma visuale non prova che la scrittura remota sia avvenuta.
- **Advisor vs competenza**: il parere di un altro modello è contributo inferenziale. La decisione responsabile richiede fonti, possibilità, ragioni, stato dell'oggetto, controller e readback; con advisor cifrato non affermare ispezionabilità della motivazione interna. Un test con un modello non equivale a una competenza nuova né alla sua assimilazione.
- **Rappresentato != raggiungibile != discoverable != esercitato != assimilato**: le feature ufficiali sono descritte/tecnicamente documentate; qui NON è stata eseguita una Claude Whiteboard nel tenant, né un MCP App server MAIOS, né una chiamata Advisor su credenziali dell'operatore.

## Comparazione orientativa — non classifica

| Dimensione | Claude Whiteboards / MCP Apps | MetaCanvas / MetaEditor osservato |
| --- | --- | --- |
| Co-editing live nello stesso host | Whiteboards lo offre; MCP Apps rende possibile UI connessa | Non provato nel workbench attuale |
| Portatore autonomo fuori dall'host | Whiteboards esporta PNG (non file board importabile); MCP Apps dipende da server e host | HTML autonomo/workbench; modello Studio a scene e modello pagina distinti |
| Handoff tra AI e umano | Collaborazione dentro Claude; MCP Apps tool/view | Trasferimento HTML e differenze; integrazione live AI nel prototipo non provata |
| Stabilità del referente dopo export | Da verificare per casi specifici | ID/Undo/export esercitati solo in percorsi limitati dei Bridge, non generalizzati |
| Autorità e audit sugli effetti | Host/permessi/protocollo e owner app | Documento e owner ricevente; confronto/diff e controllo prima del deploy |

## Prima possibilità falsificabile, NON task automaticamente selezionato

Se il lavoro futuro richiede una superficie AI-host live, confrontare **lo stesso documento sintetico** con 3 nodi e 2 relazioni nel portatore MetaCanvas e in un adapter MCP App minimale di sola lettura:
1. Aprire il referente in un host che dichiari il supporto MCP Apps; mostrare ID e provenance senza estendere i permessi.
2. Selezionare un nodo, chiedere all'AI una proposta di variazione e distinguere chiaramente la proposta dalla modifica del documento.
3. Verificare se la UI riporta selezione, testo e nuova versione al modello attraverso il contratto host; monitorare byte, identificatori, ordine degli effetti e controllo di conferma. Nessuna chiamata tool di scrittura prima dell'autorizzazione del proprietario.
4. Riprendere il risultato nel documento originario e chiedere cosa sopravvive al cambio host/versione, senza assumere equivalenza fra il PNG Whiteboards e lo stato editabile.
5. Misurare utilità effettiva (numero di passaggi, comprensione in uso reale, recuperabilità, fedeltà del roundtrip), non la sola bellezza della dimostrazione.

Il test nasce solo se l'operatore seleziona l'integrazione. A questo stadio l'apprendimento è un criterio di discriminazione in CCM, non una variazione di prodotto o di kernel assiomatico.

## Effetti e limiti del movimento del 22/11

Osservato: lettura delle pagine ufficiali e degli owner K-UX-AI/MetaEditor; confronto architetturale, differenze e prossimo caso falsificabile.
Non osservato: accesso al tenant Claude, uso reale delle beta, pricing effettivo del caso MAIOS, codice MCP attivo, verifica con utenti, aggiornamento del prodotto pubblico, deploy, transazione. La descrizione dei protocolli esterni non trasferisce autorità sul sistema.
Il routing è nel corpo CCM che già possiede questa funzione; MetaEditor Evolution e i receiver possono partecipare solo se una futura conseguenza li rende pertinenti.
