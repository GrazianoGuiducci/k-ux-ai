# K-UX-AI — Griglia v4.5 / Campo focale

**9 ottobre 2026.** Candidato owner-native di K-UX-AI sul branch `work/ux-ai-ui-library-20261008`, dati di dominio illustrativi.

## Fonte della correzione

Schermate e istruzioni dell'operatore sulla v4.4 mostrano il costo di popup attivati da micro-icone e schede distribuite con occupazione poco pertinente. Il risultato scelto non è aggiungere modalità: è ridurre il gesto ordinario a **hover per capire, click per lavorare, drag per collocare**. Il campo deve avere due superfici operative — principale e secondarie — accanto a una barra avatar ridimensionabile. Due secondarie affiancate sono utili soltanto quando ogni card resta leggibile.

## Contratto di partecipazione

```text
owner/source/object/revision (Kernel Nautico or receiving field)
  != work activity identity
  != semantic primary focus
  != avatar / preview / panel location
  != assistant/section competence authority

hover avatar -> local read-only peek
click avatar -> promote as primary (explicit); prior primary becomes secondary
drag avatar/card -> change placement/order (view only)
full page -> temporary foreground and return
existing free manual position -> preserved as alternate mode
```

Il lock del focus protegge dagli ingressi *impliciti*; il click deliberato dell'avatar è esplicito. Sul mobile il picker già presente offre un'alternativa agli avatar nascosti; le card sono riorganizzate nel normale flusso scorrevole. Non trasformare una card in un vero Section Kernel per la sola presenza di menu, fonti o conversazione: ciò appartiene alle fonti di dominio, alle competenze e alla capacità reale.

## Dettagli dell'implementazione candidata

- `focus-rail` è il default di `Adatta`. Una sola `module` principale resta nel canvas e una `.kux-secondary-rail` contiene tutte le altre. L'ordine DOM segue `slotOrder`: un focus cambiato non lascia gli elementi in ordine di creazione.
- Barra avatar 62–150 px con maniglia pointer e frecce/Home/End; preferenza memorizzata soltanto nello storage locale del browser. La preview non richiede un pulsante aggiuntivo negli avatar; si ancora all'avatar al passaggio del mouse e si chiude dopo l'uscita, salvo che il puntatore sia entrato nella preview. La sua promozione rimane un altro gesto.
- `fastRail` affianca due attività complementari **solo** quando il frame del workspace raggiunge almeno 2050 px e ci sono due complementari. La soglia è locale: qualità di lettura, non regola del Kernel.
- In schermi stretti la griglia è un campo in colonna con scroll. Durante il collaudo un difetto reale mostrava `module-content` oltre il fondo della card mobile: `moduleStyles` reimpostava `data-placement=floating` dopo la configurazione tiled, annullando le regole CSS del normale flusso. La correzione riapplica il placement dopo `moduleStyles` e rende espliciti flex, altezza e footer sul mobile.
- La riorganizzazione delle secondarie tramite drag cambia l'ordine reale dei nodi e quello visuale; il focus non viene promosso da un mero hover. Le animazioni strutturali restano circa 750 ms; durante il trascinamento diretto il puntatore non aspetta easing e in reduced motion il finale è lo stesso.
- `KUXAIDemo.perception().view` aggiunge un readback leggibile da ricevitori: composizione, modalità delle secondarie, larghezza avatar, preview/hover. Non dimostra che una AI o un Kernel esterno lo abbia consumato.

## Audit dei controlli visibili

| Comando | Effetto realmente esercitato | Disponibilità |
|---|---|---|
| ◇ Sezione | Quadro / Fonti / Conversazione locale / Collegamenti | Card |
| ◉ Anteprima | Lettura della sorgente demo senza focus | Card; hover nell'avatar |
| ▤ Compatta | Nasconde contenuto esteso e può ripristinarlo | Card |
| □ Full | Temporanea pagina intera, Escape ripristina | Card |
| − Riduci | Minimizza, lascia l'attività recuperabile | Card |
| × Chiudi | Rimuove la card dal medium, non i fatti del dominio | Card |
| Porta al centro | Promozione esplicita a principale | Footer card |
| ◧ Aggancia | Dock laterale; commuta alla geometria manuale | Solo Libero |

Questi comandi non sono un'ontologia definitiva. Non sono state aggiunte nuove icone o proprietà AI reali nella barra avatar.

## Prove e limiti

Le suite Chromium Playwright a comportamento correlato hanno ottenuto **74/74** (6 dimensioni + superwide, principi di layout e ridimensionamento avatar), **32/32** (preview, lock, riordino card, bozza, assistant demo e icone), **17/17** (geometria del contenuto/scroll mobile e drag nativo dall'avatar), zero JS page errors osservati. Prove eseguite con `page.set_content` sul file identico SHA256 `e8dd429f61a2814aa529dd0b908b105290b72afe3af2cca480347283cd2275ae`; gli script e le immagini sono consegnati anche nel pacchetto scaricabile della conversazione. Le 123 assertions **non** sono valutazioni indipendenti del prodotto.

Fuori scope: hosting MAIOS, installazione THIA/provider AI, dati autentici Nautico, autorizzazioni industriali, touch fisico, Edge file://, WCAG/AT integrale. I testi di sezione e le notifiche restano sintetici; nessun modello autonomo o SK è stato creato. Versione K-UX-AI pubblica ancora `0.1.0-alpha.1`.

## Ritorno alla competenza

L'apprendimento Code Medium è più circoscritto della tipologia grafica: la **continuità di un focus** esige tre coerenze diverse — semantica (`focused`), ordine della presentazione (`slotOrder` + DOM), contenimento dei contenuti nel viewport effettivo. Ognuna può restare corretta mentre un'altra si perde. Il progetto ha scoperto e corretto una differenza non emersa dalle prove precedenti; il metodo reusable è distinguere la proprietà dello stato da quella della disposizione, osservare geometria del contenuto oltre ai bounds della card, e offrire due velocità per puntatore e ricomposizione. Interaction Quality del Design Kernel possiede già il principio generale; la costruzione esercitata appartiene alla competenza privata Code Medium Construction.

**Stop:** osservazione del candidato in Edge da parte dell'operatore; nessun effetto su Kernel Nautico per inerzia.
