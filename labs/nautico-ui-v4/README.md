# K-UX-AI · Griglia del fare v4 — assistente modulare

## Rientro 8 ottobre — v4.1 motion parity, candidata locale

L'HTML originale [01](01-griglia-chat-window-surface.html) e la sua ricevuta storica [EVIDENCE.json](EVIDENCE.json) restano invariati.
Il nuovo [02 — Griglia v4.1, motion parity](02-griglia-chat-window-surface-motion-parity.html) incorpora la correzione anche della sorgente condivisa [Window Surface](../../src/ui/window-surface.js).

**Differenza:** `minimize()` cattura il token di movimento *dopo* avere avviato `avatarToWindow(false)`. Prima, nella modalità `prefers-reduced-motion` (o senza Web Animations), il movimento non incrementava il token: la chiusura era scartata, il frame restava aperto e l'avviso non raggiungeva l'avatar.

[Nuova ricevuta mirata](EVIDENCE_MOTION_PARITY_20261008.json): sul file precedente 11/13 controlli in reduced-motion (due controesempi); sul candidato 13/13 in reduced-motion e 13/13 in movimento normale, zero errori di pagina nei due percorsi nuovi. I controlli sono correlati e non sostituiscono i 93 precedenti; nessuna prova di AI live, evento Nautico reale, accessibilità completa o integrazione Site.


**8 ottobre 2026 · PROTOTYPE_INTEGRATED_SYNTHETIC / non pubblicato**

## Apri il prototipo

[Griglia del fare con Window Surface e Chat/Form](01-griglia-chat-window-surface.html).

Si tratta di **un solo HTML autonomo** che riutilizza il codice originale K-UX-AI `src/ui/window-surface.js`, `src/ui/chat-form-module.js` e `src/medium.js`, incorporati in una versione da osservare offline. Non installa THIA, non invoca API, non usa dati del Nautico reale e non sostituisce il Site MAIOS.

## Differenza dalla v3

La v3 disponeva di un pannello "Assistente" come un'altra scheda del proprio sistema locale. La v4 lascia inalterate le altre attività e fa passare **tutti gli ingressi di assistenza** attraverso **un unico componente Window Surface** con modulo Chat/Form separato.

Lo stesso assistente può essere:
- avatar chiuso nella Home o nel dock delle attività;
- finestra libera, spostabile/ridimensionabile;
- sidebar sinistra/destra che **fa spazio** al canvas;
- superficie a pagina intera;
- Chat/Form affiancati, oppure tab Chat e tab Modulo quando la **larghezza del frame** non basta.

Nel passaggio `full -> floating` il sistema conserva la bozza e **trasferisce il focus** al comando ancora visibile quando quello usato scompare. In `minimize -> avatar` il focus torna a un punto raggiungibile e il contenuto rimane vivo.

## Provalo in questa sequenza

1. Apri la **Griglia** e scegli una voce d'intento. Le altre attività restano nel layout v3 originale.
2. Nel campo, apri l'avatar assistente dalla colonna sinistra. **Al primo ingresso di lavoro** è suggerito un dock a destra, che lascia spazio al canvas; puoi tornare alla finestra libera.
3. Apri `Modulo`, inizia un testo e passa a **Pagina intera**. Rientra con il comando o con **Escape**: la bozza resta.
4. Riduci ad avatar, riapri, registra una traccia locale. Il controller del laboratorio aggiorna il proprio registro con identità e origine, ma **non invia nulla fuori dal browser**.
5. Riduci ancora, scegli **Simula variazione** e usa la barra di evento. Soltanto accettando `Componi 2 schede` il campo adotta quella disposizione; al ritorno alla Home l'avatar può segnalare un evento ancora da esaminare.
6. Prova il passaggio mobile e torna su desktop. La geometria manuale non deve essere sostituita dalla forma temporanea richiesta su schermo stretto.

## Confini e implementazione

```text
v3 domain demonstrator state (synthetic Nautico context)
    ↕ local K-UX-AI createMedium receive/dispatch/observe
reusable Window Surface (presentation/geometry/focus)
    ↕
reusable Chat/Form module (unsent draft, local question, receipt)
```

`createMedium()` conserva la direzione di ritorno delle azioni: `dispatch()` da solo non approva nulla; il controller locale decide se registrare una nota e genera l'evento che viene poi restituito a `receive()`. Questa è una prova di composizione del mezzo, **non** una connessione al Kernel Nautico operativo.

Alcune parti storiche `panelContents('chat')` rimangono nel grande HTML v3, ma `openPanel('chat')` nella v4 usa il componente riutilizzabile e non crea più una card di chat duplicata. Potranno essere eliminate durante la futura migrazione dal laboratorio a un bundle modulare, evitando di ricostruire l'intero canvas in questa formazione.

L'assistente dispone di due comandi cognitivi distinti: quando è chiuso, `notify({id,text})` riceve solo eventi di prova identificati; quando è aperto, una nuova attività può diventare un messaggio di stato. Le comunicazioni rimangono **etichette dimostrative**, non inferenze autonome di un modello.

## Qualifica e prove

Leggi [EVIDENCE.json](EVIDENCE.json) per le ricevute esatte: **28/28 + 28/28** controlli sul prototipo integrato e **23/23 + 14/14** sullo stesso componente riutilizzabile. Sono suite correlate e non attestano comprensione umana o comportamento di un prodotto installato.

I difetti osservati durante questo passaggio e corretti:
- il click dell'avatar bypassava la politica host di docking iniziale;
- in full-page si nascondeva il bottone sotto il focus, impedendo a Escape di operare;
- un avviso sospeso non ritornava all'avatar una volta rientrati alla Home.

### Non verificato

- chat MAIOS reale, autenticazione, destinatari e API THIA/DOMUS;
- continuità del caso su server/Nautico e stato di impianti;
- agenti AI, DSH/Codex/ChatGPT runtime;
- simultaneità di più pannelli di **dominio** scrivibili;
- assistive technology e utenti esterni;
- inserimento nel Site e pubblicazione.

## Per il prossimo rientro

Parti da [CURRENT del cabinet](../../docs/ui-library/CURRENT.md), dal [contratto delle superfici](../../docs/ui-library/OPERATING_CONTRACT.md) e dalla [sorgente owner-native del Kernel Nautico](https://github.com/GrazianoGuiducci/kernel-nautico). Non migliorare la superficie per inerzia: usa una situazione realmente cambiata nel dominio per comprendere se la prossima capacità da formare è la comunicazione con il kernel, una diversa percezione o una nuova operazione.

Questa lane resta privata. Nessun merge, deploy o incarico a Codex Site è implicito nel suo stato.
