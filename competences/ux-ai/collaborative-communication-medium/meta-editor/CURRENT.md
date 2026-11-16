# MetaEditor Evolution — CURRENT

updated: 2026-11-16
owner: GrazianoGuiducci/k-ux-ai / collaborative-communication-medium / meta-editor
status: competence_formed; neutral_lab01_node_edit_browser_exercised; end_user_usability_unobserved
runtime_owner: examples/collaborative-communication-medium/ (future candidate)
distribution: no release; no MAIOS.it deployment

## Presente selezionato
L'operatore chiede una competenza dedicata che evolva il MetaEditor. La forma pertinente è una specializzazione **interna a CCM/K-UX-AI** sul metodo di progettare e verificare editor generalizzabili. L'architettura da discriminare conserva differenze fra pagina web, presentazione, diagramma, contenuto originale e strumenti di modifica; non prosegue automaticamente R4.

## Prima risultante tecnica — Lab 01

Il [prototipo neutro](../../../../examples/collaborative-communication-medium/meta-editor-lab/MetaEditor_Lab01.html) è ora in K-UX-AI con [documentazione della prova](../../../../examples/collaborative-communication-medium/meta-editor-lab/README.md). Node + Chromium tramite set_content hanno verificato `contenteditable` direttamente nella label, Enter, Undo/Redo, trascinamento del nodo con link, card fra sezioni, sezione template non distruttiva, salvataggio/riapertura HTML e viewport 390 px. Sono stati corretti due difetti trovati in corso d'opera: parentesi CSS mancante che alterava la geometria e template che sostituiva indebitamente una sezione. La [GUIDE](GUIDE.md) custodisce il saper fare emergente.

**Limiti:** pagina/proiezione slide sono due viste del documento sintetico `metaeditor.lab.v1`; non integrazione con Studio20 `ccm.document.v1`. Il banco non importa HTML arbitrario né è stato esercitato su Chrome Windows reale; la qualità percepita dal ricevente resta da osservare. Fonte pubblica non equivale a runtime installato in Codex o MAIOS.it.

## Primo banco / stato degli effetti
Il primo esercizio deve testare **doppio clic sulla label di un nodo e digitazione in situ**, una card duplicabile su layout responsive e round-trip del documento con un solo storico. Soluzioni esterne restano candidate, non importate. La copia del sito MAIOS non è il banco neutro. Un documento o un test creato in una conversazione non equivale a un file già residente in K-UX-AI; registrare qui il percorso reale se e quando trasferito.

## Limiti
Competenza scritta ≠ runtime integrato ≠ sito modificato ≠ funzionalità esercitata dall'operatore ≠ assimilazione futura. Esercizi precedenti R3/R4 conservano prove specifiche e difetti, ma non soddisfano la nuova prova. Codex non è automaticamente attivato.
