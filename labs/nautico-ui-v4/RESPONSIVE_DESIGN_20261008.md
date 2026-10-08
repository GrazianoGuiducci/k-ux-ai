# Griglia v4.2 — decisioni responsive e organizzazione del campo

Data: 2026-10-08. Owner della candidata: `GrazianoGuiducci/k-ux-ai`, branch `work/ux-ai-ui-library-20261008`. Il caso ospitato è Nautico sintetico; non c'è connessione live.

## Osservazione dell'operatore

Tre schermate mostravano difetti effettivamente visibili: più card sovrapposte in modalità desktop, popover Strumenti intercettato dalle card, e su mobile colonna di avatar costosa con card non scorrevoli insieme. L'operatore chiedeva anche 3 colonne, maggiore spazio sopra il canvas, menu a discesa e riorganizzazione automatica migliore. L'effetto scelto riguarda il **layout/UI locale**, non uno stato industriale o un'azione del Kernel Nautico.

## Causa nella v4.1

- `placePanels()` posizionava con coordinate assolute solo i primi 2/4 elementi nei layout `split/quad`. I restanti usavano coordinate `free`, potendo sovrapporsi.
- `enforcePanelCapacity` minimizzava altre attività per rispettare il numero del preset: `numero di colonne/aree != cardinalità del lavoro`.
- Quando `stage.width < 700`, una sola card era resa visibile; `workspace-stage` aveva `overflow:hidden`, quindi non era una pila scorrevole.
- Il popover Strumenti stava in una barra con z-index fisso, mentre il valore z delle finestre cresceva: l'ordine di dipendenza non proteggeva il menu.
- Il titolo occupava una barra ridondante e la colonna avatar sottraeva larghezza al frame mobile.

## Nuova composizione situata

```text
domain panels / notes / events / focus (unchanged synthetic demo owner)
  != rendered position / breakpoint / visibility / animation
Adatta:
  measure usable stage width -> up to 3 columns
  rows expand to include ALL non-minimized cards -> stage scroll
2 / 3 / 4:
  requested composition -> fit according to actual stage width
  never force-minimize otherwise active domain activities
Libero:
  preserve explicit free coordinates
Mobile:
  one reading column, card content in normal flow, stage pan/scroll
  title/focus + tool menu + assistant avatar in shared topbar
```

**Il componente K-UX-AI Window Surface/Chat/Form è lo stesso della v4.1**. La modifica riguarda il campo ricevente. Un tooltip, un layout, un resize o il suo scroll non approvano né modificano il dominio. La modalità full-page è temporanea: al rientro conserva il layout da cui proveniva; l'interfaccia locale continua senza attendere animazioni opzionali.

La disposizione libera mantiene finestre sovrapponibili intenzionalmente: non è una griglia. In presenza di troppe finestre non piazzate manualmente, il calcolo di free-space può proporre/ritornare ad Adatta. Un controllo di docking laterale in un layout a griglia non viene esposto come se l'aggancio fosse possibile in quella morfologia.

## Evidenza e limiti

[Receipt v4.2](EVIDENCE_RESPONSIVE_20261008.json): 121 assertions responsive su sei viewport/condizioni, 19 assertion di transizione/stato (medesimo HTML), zero JS page error nei percorsi controllati. Test: `page.set_content` Chromium headless/Playwright, 8 ottobre 2026. Sono suite correlate, non 140 prove indipendenti.

Copertura: 9 attività non minimizzate con disposizione adattiva, assenza di intersezioni a layout stabilizzato, scroll, menu sopra le card, 3 colonne con fallback, menu focus, header mobile, rimappatura avatar e demo-controls, bozza preservata, full/ESC, viewport desktop-mobile-desktop, geometria manuale conservata.

Non provato: navigazione `file://` in questo browser di prova (bloccata dal receiver), touchscreen/dispositivi reali o studio utenti indipendente, WCAG audit completo, integrazione Nautico owner-native, chat AI, provider, privilegi, persistenza server, host MAIOS, autorizzazioni del dominio.

## Learning return

Il meccanismo d'interazione generalizzabile è che **una disposizione non deve diventare autorità sul numero di attività esistenti**. Layout adattivo = una trasformazione di vista reversibile; gli elementi di lavoro restano raggiungibili e scrollabili. Un popover di controllo deve vivere in una gerarchia di overlay che non dipenda dall'aumento dinamico dello z delle finestre. Quando la struttura si impila, il contenuto può diventare scroll di flusso invece di restare intrappolato in scroll interni di card fissate a un viewport.

Conservare questa differenza presso la competenza privata di Code Medium Construction e, quando materialmente utile, Interaction Quality del Design Kernel; la documentazione locale non pretende assimilazione generica.
