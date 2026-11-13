# MetaCanvas — consegna per Risorse → Tool su MAIOS.it

## Studio 21 — due demo distinte per le pagine italiane e inglesi (13 novembre 2026)

**Decisione dell'operatore:** MAIOS.it avrà una pagina italiana e una pagina inglese nella categoria **Risorse → Tool**; ciascuna rimanderà alla **propria versione HTML autonoma pubblicata in K-UX-AI**. Il selettore interno EN/IT non è il modello di distribuzione. La coppia è stata pubblicata, mentre **le due pagine del sito restano da realizzare con Codex**.

- **Pagina Risorse IT → Demo IT:** [MetaCanvas Studio 21 · Consulenza IT](MetaCanvas_Studio21_Consulenza_IT.html), file GitHub [IT](https://github.com/GrazianoGuiducci/k-ux-ai/blob/main/examples/collaborative-communication-medium/MetaCanvas_Studio21_Consulenza_IT.html). Commit pubblicazione `e33424be5b1230816a7e262187075cd99c0764b8`, 293.797 byte, SHA-256 `abbdbd9e749453434fddb140505c0586ce594990739742c8106f37ab542165df`.
- **Pagina Resources EN → Demo EN:** [MetaCanvas Studio 21 · Consulting EN](MetaCanvas_Studio21_Consulenza_EN.html), file GitHub [EN](https://github.com/GrazianoGuiducci/k-ux-ai/blob/main/examples/collaborative-communication-medium/MetaCanvas_Studio21_Consulenza_EN.html). Commit pubblicazione `ce227936bda32e0e507352f1974e0737b66c9dfb`, 314.444 byte, SHA-256 `066f604c62ef761d9ee6a2db2d6cdcd7e8c6f79423fa6b5039f3126fb185faab`.

Entrambe le versioni contengono la reinterpretazione presentabile in **sette schede** della [pagina Consulenza AI fornita dall'operatore il 13 novembre](https://maios.it/consulting-ai.html) (sorgente allegata: `MAIOS_Consulenza_AI_hero_revisione.html`, **non** prova che la pagina sia già online). La demo non replica il layout del sito: conserva le relazioni da mostrare e resta modificabile. Controlli **Demo MAIOS / Show demo** e **Canvas vuoto / Blank canvas** sono annullabili; Presenta, navigazione, template e salvataggio HTML restano disponibili. La versione inglese ha anche l'interfaccia principale, la guida e i template incorporati in inglese.

**Contratto del sito per Codex:** leggere le regole e le pagine native di `maios_it`, progettare le due schede IT/EN secondo la sezione Tool effettiva, con URL linguistici reciproci e collegamenti ai due file specifici. Distinguere **tool generale** ([MetaCanvas Studio 20](AI_Collaboration_Studio.html)) dalla **demo Consulenza AI Studio 21**. La pagina può presentare il tool e usarne questa demo, senza pretendere che la pagina Consulenze diventi un editor o che l'AI sia incorporata. Non copiare due volte il codice nella repository del sito; se serve distribuire download da maios.it, verificare la sincronizzazione e gli hash delle copie. Nessun deploy è autorizzato da questo handoff.

**Prove delimitate:** controlli di sintassi Node, sette schede senza clipping, avvio demo/Presenta, nuovo canvas, conferme, salvataggio e riapertura, adattamento mobile 390 px, nessun page error Chromium nei flussi verificati; readback GitHub esatto per entrambi i file. Restano da verificare apertura `file://` su Chrome Windows dell'operatore, storage locale reale, accessibilità completa e prova di ricezione da terzi.

---


Stato al 13 novembre 2026: **file pubblico disponibile; pagina MAIOS.it non creata; Codex non attivato**.
Questo documento è un passaggio di conoscenza, non un ordine a un controller.

## Fonte canonica e download

- Tool: **MetaCanvas Studio 20 — AI Collaboration Studio**
- Repository prodotto: `GrazianoGuiducci/k-ux-ai`
- File stabile: [AI_Collaboration_Studio.html](AI_Collaboration_Studio.html)
- [File pubblico GitHub](https://github.com/GrazianoGuiducci/k-ux-ai/blob/main/examples/collaborative-communication-medium/AI_Collaboration_Studio.html)
- Dimensione versione 20: **272.490 byte**
- SHA-256 versione 20: `c8c1be74c7d9b91d99b0c7888c40cee387579ca26f3079d0fa44ea81f1817a19`
- Licenza software: **MPL-2.0**, limitata alla directory del tool; copyright del contributo originale: Graziano Guiducci. Marchi e contenuti inseriti dagli utenti hanno statuti propri
- Testo UI attuale: italiano. HTML autonomo, utilizzabile offline in un browser moderno, nessun modello AI o account incorporato
- [Guida italiana](README.it.md) · [Guida inglese](README.md) · [Contratto dati](DOCUMENT_CONTRACT.md) · [Prove e limiti](SOURCE_AND_SCOPE.md)

## Identità per il primo incontro

Il pubblico deve riconoscere un **editor di idee, diagrammi e presentazioni editabili**, che permette di costruire una scena, presentarla a persone, salvarla in un file portabile e passarla a un modello AI per un contributo. È un tool, non una meta-skill e non un servizio ChatGPT incorporato.

Principali possibilità concrete:
- Partire da quattro esempi neutri o una scheda vuota, modificare testi, forme, relazioni/frecce, ordine delle schede, immagini locali e note del relatore
- Disporre gli strumenti attorno al canvas, scegliere Standard o Flat, passare a lettura e presentazione
- Inserire template sopra/sotto o sostituire la scheda con conferma, personalizzare e riutilizzare modelli, Annulla/Ripristina
- Salvare e riaprire un HTML autonomo, esportare una copia pubblica privata dei dati esplicitamente marcati
- Esportare dati strutturati per l'AI di una scheda o del documento; scegliere esplicitamente se includere elementi personali
- Ricevere un JSON/HTML da un modello, confrontare le schede diverse e integrare selettivamente o sostituire con conferma
- Facoltativamente mantenere una bozza locale di recupero, disattivata inizialmente e dipendente dal browser; non sostituisce Salva lavoro

## Passaggio operativo a Codex / owner MAIOS.it (futuro)

Quando l'operatore attiverà Codex per questa pagina:
1. Leggere **le sorgenti native attuali di MAIOS.it**: regole di Risorse, tipologie, card/tool, struttura URL, lingua, stile, metadati, download/collegamenti e contratto di deploy. Non inferire quelle regole dal presente documento né imporre una struttura inventata.
2. Selezionare la sezione **Risorse → Tool** (o etichetta equivalente già proprietaria del sito); non inserire MetaCanvas tra le Meta-skill. Allineare descrizione IT/EN e materiali alle regole vere degli altri tool.
3. Linkare il **file canonico pubblicato in K-UX-AI**: evitare di creare una seconda sorgente divergente del codice. Se il sito dovesse distribuire una copia, definire e verificare un meccanismo/versione di sincronizzazione con la sorgente K-UX-AI, incluse le licenze.
4. Preparare spiegazioni d'uso e una dimostrazione leggibile, senza sovraccaricare il primo incontro; mantenere profondità accessibile su richiesta. La pagina deve distinguere cosa fa l'editor, come si usa con una AI esterna, cosa rimane personale e come si scarica.
5. Comporre Editoriali, Design e UX-AI per il risultato pubblico; mantenere prodotto e versione canonici presso K-UX-AI. Prima di proclamare la pagina pubblica, leggere diff e readback del vero deployment.

Non affermare: editing AI diretto nel browser; sincronizzazione/cloud; collaborazione multiutente in tempo reale; backup locale universale in `file://`; certificazione generale di sicurezza/accessibilità o test su ogni dispositivo.

## Relazione con D-ND Design Kernel

- **Design owner:** `GrazianoGuiducci/d-nd-ux-ai-seed`, con un riferimento di metodo a Studio 20.
- D-ND Design possiede gerarchia percettiva, responsive interno, continuità del focus e controllo del carico visuale; K-UX-AI/Collaborative Communication Medium possiede il codice dell'editor e le operazioni del documento.
- Il principio appreso: *aumentare le capacità del medium senza obbligare l'operatore a vedere più controlli nell'uso ordinario*. Le scelte compaiono presso l'effetto (consegna AI, importazione/confronto, recupero) e conservano l'autorità della persona.
- Pubblicare il collegamento al Design Kernel non significa installare il tool nel runtime npm del Seed né duplicare la sorgente.

## Verifiche e confini della consegna

L'HTML Studio 20 pubblicato è stato riletto da GitHub e confrontato esattamente con il file locale consegnato. JavaScript syntax test con Node; prove locali Chromium sono dichiarate in SOURCE_AND_SCOPE. L'interazione con Chrome Windows `file://` dell'operatore, screen reader, touch fisico e storage reale restano non attestati.

**Nessuna pagina MAIOS.it, PR del sito, effetto Codex o deploy è dichiarato eseguito dal presente handoff.**
