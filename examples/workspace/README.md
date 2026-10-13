# Esercizio tecnico — MessagePort e continuità

Questo esercizio verifica il medium, un vero MessageChannel
locale e i moduli originali Window Surface e Chat/Form. Il controller è
sintetico: non chiama un modello AI o un servizio di dominio.

Servi la root del repository e apri `examples/workspace/`:

    python -m http.server 8080 --bind 127.0.0.1

Puoi aprire la finestra da avatar o pulsante, passare floating/dock/full,
preparare una bozza, simulare un nuovo riscontro e inviare esplicitamente
il contributo. Il controller conserva l'oggetto e conferma il risultato
con uno snapshot; una chat sintetica percorre lo stesso canale.

Il readback espone stato, geometria, bozza e ultimi eventi. Il controller
del tuo dominio può sostituire quello locale senza usare il suo vocabolario.
Il kernel operativo è raggiunto da [BOOT.md](../../BOOT.md); la forma
di questa pagina è un esempio, non un layout obbligatorio.

Stato locale in memoria; storage dei moduli disabilitato in questa demo.
Per il collegamento ad altri agenti:
[adattamento del ricevente](../../docs/receiving-environment.md).

Il riferimento interattivo principale è la [Griglia v5.12](../griglia/README.md)
formata con GPT. Questa pagina isola il collegamento tecnico e la conferma
del controller; la sua forma serve a quell'esercizio.
