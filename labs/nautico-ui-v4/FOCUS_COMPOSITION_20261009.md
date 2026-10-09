# K-UX-AI Griglia v4.3 — composizione situata del focus

Data: 2026-10-09. Owner artefatto: `GrazianoGuiducci/k-ux-ai`, branch `work/ux-ai-ui-library-20261008`.
Sorgenti: quattro schermate fornite dall'operatore sulla v4.2, più la [v4.2 precedente](03-griglia-responsive-workspace.html), suoi componenti comuni K-UX-AI e Interaction Quality del Design Kernel.

## Differenza che ha formato la revisione

Il numero delle attività vive è distinto dalle modalità in cui la persona intende relazionarsi a esse. L'operatore può voler:
- aprire una sola scheda e dedicare a essa l'intero campo;
- condividere il campo fra due attività, senza una metà vuota;
- aggiungere una terza attività per il lavoro principale, mentre le altre diventano complementari;
- preservare un focus già importante mentre porta una sorgente/attività vicina;
- leggere soltanto l'ultimo dato o una notifica tramite una mini-anteprima, senza aprire un'area di lavoro;
- aprire una superficie temporanea dominante (full/modal), poi tornare al lavoro precedente;
- riorganizzare deliberatamente tutto quando la disposizione non è più adatta.

La v4.2 rendeva tutte le card raggiungibili, ma non distingueva abbastanza **leggere senza promuovere** da **aprire e focalizzare**; il semplice `pointerdown` di una intestazione poteva avviare lo sgancio dalla griglia verso Libero. Le maniglie di Chat e delle altre card possedevano forma e comportamento differente.

## Contratto candidato della v4.3

```text
owner-native object + work state + existing activities (immutati)
+ human gesture / observation need
-> read-only peek | add to work field | explicit focus change | transient fullscreen
-> attention/placement/focus changes in the receiver
-> domain effect remains owned and explicitly authorized by its controller
```

- **Anteprima**: vista sola lettura di oggetto/fonte/stato noto, ultima nota e segnale locale; nessun pannello aggiunto o promozione del principale. Il testo indica che il dato è sintetico.
- **Attività presente**: istanza di card nel workspace, con proprie bozze; il suo stato operativo non equivale al focus spaziale.
- **Focus principale**: identità preferita per una composizione proporzionale; in Adatta, il candidato usa 1 card intera, 2 card condivise, 3/4 card con principale maggiore e complementari, 5+ card con griglia scorrevole. La variazione rispetta il frame disponibile, non un conteggio obbligatorio di colonne.
- **Mantieni focus**: blocca solo la promozione implicita conseguente all'aggiunta di una nuova attività. Selezionare esplicitamente dal menu focus o da "Porta al centro" resta possibile. Chiudere una scheda secondaria non toglie il focus protetto.
- **Pagina intera**: precedenza percettiva esplicitamente selezionata; uscita con Escape/controllo ripristina il precedente principale e la disposizione.
- **Ricomponi**: azione di layout idempotente che seleziona Adatta, senza eliminare o minimizzare card, cancellare input o assegnare nuovi significati. Le posizioni manuali memorizzate in Libero restano.
- **Resize**: libero = maniglia esplicita e cursore `nwse-resize` coerenti fra Window Surface e card; griglia = dimensionamento del layout. Il trascinamento dell'intestazione richiede una soglia prima di lasciare la griglia.

## Esiti e prove

L'HTML autonomo v4.3 è un candidato di laboratorio. Le due suite locali Playwright/Chromium testano la stessa superficie:
- 160/160 prove di 1,2,3,4 card; focus mantenuto, preview non mutante, cambio esplicito di focus, Ricomponi, full/Escape/ritorno, mobile e grafica/cursore resize;
- 66/66 prove su 8 card, non sovrapposizione, scroll, preview sopra il campo, evento dimostrativo, chiusura secondaria senza cambiare focus, recompose; desktop grande, intermedio e mobile;
- zero errori JavaScript di pagina osservati nei percorsi coperti; prova con `page.set_content`, poiché la navigazione `file://` era bloccata nel browser di prova.

Le suites sono correlate e non certificano usabilità generale, qualità percettiva per altre persone, tecnologie assistive, touchscreen fisico, connessioni aziendali o operatività AI. I click non scrivono su Nautico reale; `src/ui/window-surface.js` e `src/medium.js` restano invariati. L'UI non applica un'ontologia del focus a Kernel Nautico.

## Apprendimento verso la competenza

Una rappresentazione visiva del focus non è il focus semantico, né lo stacking-order, né l'autorità su un effetto. In una composizione multi-entity, leggere/aggiungere/promuovere/massimizzare devono restare azioni discriminabili; il sistema può proteggerne la continuità senza impedire un nuovo gesto deliberato. Questo specifico metodo di implementazione appartiene alla costruzione Code Medium e all'Interaction Quality già esistente, non richiede una nuova competenza.
