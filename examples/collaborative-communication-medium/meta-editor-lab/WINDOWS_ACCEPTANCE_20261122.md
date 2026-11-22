# MetaEditor neutro — prova di accettazione Chrome Windows

## Seconda prova (v2) dopo il primo screenshot Windows

Nel primo screenshot dell'operatore il file si apre da `file://`, ma due titoli aggiunti appaiono sul margine sinistro fuori dall'allineamento del contenuto. Il controller precedente appendeva alla `section` invece che al suo flusso testuale interno. Una [CI a quattro job verdi](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45059052731) verifica ora parent/colonna/livello del titolo sulle topologie supportate, senza sostituire la conferma visiva Windows.

**Ripetizione minima:** usare il **nuovo** `MetaEditor_Prova_Neutra_v2.html` (artefatto `metaeditor-neutral-windows-preview`, ID `14768332537`, run `45059052731`) e non la precedente pagina già aperta. Selezionare `H1: Pagina campione`, mantenere la prima sezione come destinazione, premere `+ Titolo` due volte: entrambi devono comparire allineati al testo interno della fascia chiara, non al margine sinistro. Provare Undo e Redo. Se l'errore persiste, conservare screenshot ed esito; non dichiarare completata la prova.

**Stato:** candidato, non rilascio. Questa prova non è sostituita dai test GitHub Actions Linux Chrome. Non è richiesto installare server o collegare credenziali.

## Identità della prova

L'artefatto GitHub Actions `metaeditor-neutral-windows-preview` contiene un unico HTML di lavoro generato a partire dalla fixture **sintetica** `tests/fixtures/metaeditor/maios_topology_synthetic.html`. Non contiene la pagina MAIOS reale, dati personali, chiavi o progetti dell'utente. Il file dimostrativo è autonomo e l'editor è incorporato.

Scaricare l'artefatto dall'ultima esecuzione verde del workflow `MetaCanvas baseline and release preflight` sulla PR #2, estrarre lo ZIP e aprire `MetaEditor_Prova_Neutra.html` in Chrome Windows con doppio clic: deve aprirsi come `file://` senza server.

L'operatore verifica **l'esperienza reale**, non deve registrare credenziali, installare estensioni o pubblicare pagine.

## Percorso di controllo (tutti effetti distinti)

1. Aprire l'HTML locale. Devono essere presenti pagina originale, collegamenti e una sola barra `MetaEditor · HTML statico`; nessun errore evidente di layout o pannello sovrapposto.
2. Selezionare una voce dal menu **Elemento da modificare** usando la tastiera, poi **Modifica testo**. L'elemento deve essere visibile e raggiungibile. Verificare caret e selezione, inserire testo, applicare grassetto/corsivo; uscire dal campo e premere **Annulla**, poi **Ripristina**.
3. Aggiungere un paragrafo alla prima sezione; modificarlo; spostarlo alla seconda sezione. Duplicarlo e cancellare solo la copia. Annulla e Ripristina devono riprodurre tutte le operazioni senza perdere il riferimento al blocco.
4. Richiedere **Salva lavoro modificabile**, verificare che il browser abbia effettivamente scaricato il file, chiuderlo e riaprirlo con doppio clic. Deve apparire un **solo editor**, e il blocco aggiunto deve restare modificabile e trasferibile.
5. Richiedere **Esporta pagina pulita**. Verificare il file scaricato, riaprirlo e controllare contenuti, formattazione, ancore, link, responsive e assenza di UI/attributi dell'editor.
6. Ripetere a finestra stretta; verificare che toolbar, contenuto e controlli restino leggibili e azionabili. Controllare anche con Tab, Shift+Tab, Enter, Escape e frecce.
7. In caso di problema: annotare **azione**, **risultato osservato**, **risultato atteso**, **file coinvolto** e **versione Chrome**. Non serve incollare dati riservati.

## Confini e gate

- La CI verifica il core su Chrome Linux a 1440/390, incluse due topologie, e sulla pagina MAIOS reale pubblicata solo quando il suo Git blob è identico al sorgente atteso. Ciò non certifica il comportamento locale Windows.
- Questa pagina non deve essere usata per introdurre HTML sconosciuti o privati: il builder legge il sorgente completo e la copia lavoro lo incorpora inerte come dato, ma gli script originali del documento possono essere eseguiti dal browser.
- Il candidato non supporta ogni HTML, layout dinamico/CMS, editor di diagrammi arbitrari né gesti di spostamento di sezioni originali.
- Se la prova reale Windows è positiva, restano comunque una verifica di accessibilità più ampia, regressioni su paste/HTML non fidato, packaging/versionamento e **un movimento distinto di pubblicazione**.
