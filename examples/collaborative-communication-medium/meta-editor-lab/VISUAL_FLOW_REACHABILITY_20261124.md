# Visual Flow — conferma raggiungibile e geometria guidata, 24 novembre

Run [45365062026](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45365062026) su 5cda5d7: 6/7 job verdi. Il generale completa i tre percorsi, proprietà effettive, riapertura, privacy e movimento. Playground IT 1440/1024 completa il percorso; a 390 il mini-editor intercetta realmente il click su OK. Non è un test da forzare.

Misure raccolte sul precedente candidato (prima/dopo proprietà): generale 1440 1082×609 / 742×417; 1024 692×389 / 590×332. Playground IT 1024 201×113 / 993×559, con sovrapposizione del pannello a x664: il grid comune sovrascrive il portatore guidato. Sul telefono non trasferire la larghezza 900 del canvas scrollabile a spazio utile visibile.

La correzione mantiene il layout guidato separato dal grid comune, riserva lo spazio del pannello laterale sul portatore guidato e, fino a 700px, separa il mini editor scrollabile e la conferma nativa in due bande del viewport. Non aggiunge un secondo OK. Il test richiede non sovrapposizione geometrica su telefono, sufficiente ampiezza della guida desktop e nessuna copertura dell'oggetto canvas da parte dell'ispettore laterale sul Playground. L'esito nuovo è da osservare; non equivale a una prova d'uso. Bridge11 privato e sito invariati.
