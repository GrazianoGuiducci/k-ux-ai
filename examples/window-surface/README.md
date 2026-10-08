# K-UX-AI — Window Surface + Chat/Form v0.1 (8 ottobre 2026)

## Che cosa contiene

Questo pacchetto è **codice K-UX-AI originale** che esercita il comportamento osservato nel widget JS di Lab D-ND. Non incorpora DOMUS/THIA, i suoi endpoint, segreti, autorizzazioni o il codice dei manager.

- `src/ui/window-surface.js` / `.css` — contenitore riusabile per una entity: avatar, cue attribuita a evento, apertura/chiusura direzionale, drag, resize, docking, full-page, ripristino preferenze, focus e reduced motion.
- `src/ui/chat-form-module.js` / `.css` — modulo Chat/Form indipendente, Chat/Form affiancati o tab quando il **frame** è stretto; divisore e input persistenti durante il morph; nessun servizio AI incorporato.
- `src/medium.js` — **copia del contratto pubblico K-UX-AI già esistente**, utilizzata solo per l'esempio offline.
- `examples/window-surface/index.html` / `main.js` — esempio modulare: va servito con un HTTP server locale per gli import ES modules.
- `examples/window-surface/standalone.html` — copia autosufficiente per aprire direttamente il demo, senza server né dipendenze.
- `tests/qa_primary.py` / `qa_extended.py` — verifiche Chromium tramite Playwright usando HTML self-contained, senza network.
- `examples/window-surface/*.png` — render controllati desktop/mobile.

## Prova direttamente

Apri `examples/window-surface/standalone.html` in un browser moderno.

1. Apri *Assistente* da una card, esplora Chat e Modulo.
2. Trascina l'intestazione e la maniglia di resize; usa frecce sulla maniglia da tastiera.
3. Aggancia a destra/sinistra, espandi a piena pagina, ritorna alla geometria libera.
4. Scrivi una bozza nel Modulo: non scompare dopo docking e minimizzazione.
5. Riduci ad avatar e usa *Simula evento*: un evento **sintetico con ID** produce un messaggio da chiuso.
6. Registra il contributo: passa tramite `createMedium().dispatch()` e il controller **dimostrativo locale**, che poi invia uno snapshot identificato con `receive()`.

**Non è un agente AI connesso.** Il pulsante “Simula evento” non legge lo stato del Kernel Nautico reale. La consegna del modulo non invia dati fuori dal browser. L'avviso non promette aggiornamenti automatici d'azienda.

## Riutilizzo nel kernel K-UX-AI

L'host deve chiamare:

```js
import { createWindowSurface } from './src/ui/window-surface.js';
import { createChatFormModule } from './src/ui/chat-form-module.js';

const content = createChatFormModule({
  id: 'nautico-assistant',
  onAsk: question => kernelMedium.dispatch({ type:'ask', question }),
  onSubmit: draft => kernelMedium.dispatch({ type:'contribute', draft }),
});
const surface = createWindowSurface({
  id: 'nautico-assistant', title: 'Assistente', avatar: 'AI',
  content: content.element,
});
// source event (actually produced by the receiving owner)
surface.notify({ id: 'source:event:123', text: 'Richiesta qualificata da esaminare' });
```

La versione base conserva la posizione `floating`, `dock-left`, `dock-right`, `full`, con `minimize` e `open`. La struttura `onLayoutChange` permette all'host di fare spazio sul canvas, invece di sovrapporvi ciecamente la sidebar.

La persistenza **delle bozze** non viene attivata implicitamente; l'host deve passare uno storage esplicito e valutare policy e riservatezza. La geometria del contenitore può usare lo storage locale dove disponibile, con fallback quando è negato.

## Origine e limiti della formazione

Sorgente osservata: [GrazianoGuiducci/lab-d-nd-site, `domus-widget.js`](https://github.com/GrazianoGuiducci/lab-d-nd-site/blob/bc92ae3f90786ceaaf84d6042aef0aec876a50cb/assets/js/domus-widget.js).

Contratto di trasferimento: [THIA Chat Port Parity Contract](https://github.com/GrazianoGuiducci/d-nd-ux-ai-seed/blob/main/docs/THIA_CHAT_PORT_PARITY_CONTRACT.md).

Da Lab D-ND abbiamo appreso comportamenti: avatar, bubble, moduli chat/form, split, dimensionamento condizionato, movimento orientativo, accessibilità e confini tra visitatore e gestore. Questo codice è una **implementazione nuova, generalizzata e delimitata**, non un port completo della chat originale e non ne eredita backend o identità.

**Ancora aperto:** parità della chat THIA completa, auto-espansione al primo drag e drag-down da fullscreen, controllo completo ARIA/focus per ogni ricevente, interoperabilità reale con eventi Nautico, più entity contemporanee con scheduling attentivo, autorizzazioni ed effetti host, test umano.

## Prove

Testate due sequenze Playwright nello stesso laboratorio v0.1: **23/23** funzionali (desktop/mobile/reduced motion) e **14/14** aggiuntivi (drag/resize, tastiera, full/ESC, evento/avviso con ID, viewport). Zero errori JS osservati in queste esecuzioni. Le suite condividono codice ed ambiente, quindi **non sono validazioni indipendenti**.

I controlli sono stati eseguiti caricando il file self-contained mediante Playwright `page.set_content`, poiché il browser di prova non consentiva navigazioni file:// o localhost. Questo non equivale alla verifica del bundle ES module consegnato dentro il Site MAIOS.

*Stato*: candidato del primo modulo completo di K-UX-AI; nessun merge o deploy.
