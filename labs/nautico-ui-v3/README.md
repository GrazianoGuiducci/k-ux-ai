# K-UX-AI Laboratorio · revisione 3

**Prototipi autonomi. Nessuna AI connessa e nessuna integrazione con il Kernel Nautico live.**

## Prova questi comportamenti

Apri [01 — Griglia del fare v3](01-griglia-del-fare.html) oppure [02 — Campo a quattro fonti v3](02-campo-quattro-fonti.html) in un browser moderno.

- Entra nel campo con un avatar o una scheda. La barra operativa è intenzionalmente compatta: **Strumenti ▾** apre contesto, disposizioni e “Perché qui?” senza togliere altezza al canvas.
- Apri **+ Attività** per una nuova scheda. Il nuovo comando **▤** passa da finestra completa a *card rapida*. Usa **□** per portare la scheda a tutta pagina; premi **Escape** per tornare alla disposizione precedente. I dati non vengono approvati o inviati da questi comandi.
- L'**Assistente** può aprire un modulo. In una finestra ampia Chat e Modulo sono affiancati e puoi regolare il divisore; in una finestra stretta/mobile appaiono le schede **Chat / Modulo**. Prova una bozza, cambia scheda, espandi, torna e verifica che il testo sia preservato.
- **Copia / Esporta / Reset** riguardano la conversazione locale; reset richiede conferma. **Prepara contributo** riguarda il form locale e **non invia nulla**; l'eventuale invio reale appartiene al controller del sito.
- Riduci una finestra ad avatar e riaprila: mantiene la conversazione e torna a una forma leggibile, non al full-page precedente.
- In modalità “due schede” o “quattro”, i pannelli non attivi rimangono recuperabili. Le disposizioni calcolate dal sistema non devono sovrascrivere le coordinate libere scelte dall'operatore.

## Sorgenti e file

- `template_v3.html`, `style_v3.css`, `app_v3.js`, `build_v3.py` — laboratorio modificabile.
- `test_v3.py`, `test_geometry_v3_reg.py`, `test_logic_v3.py`, `test_deep_v3_reg.py`, `preview_v3.py` — prove Playwright.
- `../../docs/ui-library/SOURCE_ADOPTION_20261008.md` — fonti esatte da importare nella vera applicazione e differenze ancora aperte.
- `UX_AI_KERNEL_MEDIUM_LOGICHE_v2.md` — derivazione cognitiva della revisione precedente.
- `screenshots_v3/` — anteprime su desktop, piena pagina, e mobile.

## Risultato e limiti

Browser Chromium, configurazioni desktop/mobile. Test di stato/geom/comp. **Non equivalgono a validazione indipendente di UX, sicurezza o idoneità in produzione**; non dimostrano apprendimento autonomo.

Il codice v3 deriva dal laboratorio v2: è **un adattamento parziale dei contratti d'interazione** di `GrazianoGuiducci/d-nd-ux-ai-seed`, non un port ufficiale/paritario di `ThiaChatSeed`/`AgenticChatSystem`.

Il trasferimento nella demo MAIOS/Kernel Nautico dovrà adottare i componenti owner-native con relative dipendenze CSS, responsive, focus/awareness e host submit/transport. Nessuna modifica o pubblicazione del sito è inclusa in questo pacchetto.
## Organizzazione nel K-UX-AI Kernel

I due HTML contenuti in questa directory sono **gli stessi esempi autonomi di laboratorio v3**, ora raggiungibili da un branch K-UX-AI. Non sono una chat THIA installata né una build del Site Nautico.

- [Catalogo machine-readable delle nove famiglie di moduli](../../ui-library/catalog.v0.1.json)
- [Contratto completo dei comportamenti e della composizione](../../docs/ui-library/OPERATING_CONTRACT.md)
- [Rientro della lane](../../docs/ui-library/CURRENT.md)
- [Ricevuta attribuita del laboratorio](EVIDENCE.json)

Lo stato delle azioni del Kernel Nautico non viene importato dall'HTML: gli esempi mostrano dati dimostrativi. Alcuni riferimenti ai file sorgente originali (`app_v3.js`, `style_v3.css`, test Playwright) erano parte del laboratorio locale ZIP, ma **non** di questa directory: i due HTML sono autosufficienti. Le prove vengono conservate qui come ricevuta precedente, non come test eseguiti su questa copia di GitHub.
