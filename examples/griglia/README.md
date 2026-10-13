# Griglia del fare — v5.12 originale

Questa è l'incarnazione interattiva formata con GPT e selezionata come
riferimento concreto per il consolidamento K-UX-AI. La UI conserva attività,
card, focus, bozze, barra Attività e chat continua attraverso trasformazioni.

Servi la root del prodotto e apri `examples/griglia/`:

```sh
python -m http.server 8080 --bind 127.0.0.1
```

La sorgente HTML è conservata integralmente, senza riscrittura:
`25-griglia-rail-composer-v512.html` dalla candidata pubblica
`45152db3ca5e7dca1de524f7d02301adbe857cfe`.
Il file dell'operatore `KUX_Griglia_v5_12_Chat_Attivita.html` ha gli stessi byte.
SHA-256: `1879dbe0d2ccba4c7db4701fe067c05ad1d20761aa2a6cf053f90b478118430b`.

[Origine della sorgente](https://github.com/GrazianoGuiducci/k-ux-ai/blob/45152db3ca5e7dca1de524f7d02301adbe857cfe/labs/nautico-ui-v4/25-griglia-rail-composer-v512.html).

Puoi usare subito le interazioni del dimostratore. Fonti, eventi e risposte
sono locali e sintetici. Il collegamento a un LLM o al dominio Nautico
prosegue attraverso i controller del ricevente; l'HTML conserva questa
qualificazione nell'interfaccia.

Il [kernel di competenza](../../KERNEL.md) e la
[guida](../../competences/ux-ai/GUIDE.md) portano il sapere per comprendere,
costruire ed evolvere queste forme in altri lavori. La griglia è un risultato
concreto e un riferimento di qualità; nuovi contesti possono richiedere
un'altra composizione.

L'[esercizio tecnico](../workspace/README.md) separato verifica il trasporto
MessagePort e la continuità di una bozza. Le sue prove appartengono a
quell'esercizio, mentre la griglia conserva la propria identità.
