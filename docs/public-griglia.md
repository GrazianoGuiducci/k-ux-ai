# La Griglia come presentazione, guida e mezzo di lavoro

La persona entra in un ambiente, riconosce l'oggetto e sceglie che cosa fare.
Le schede proiettano funzioni diverse dello stesso kernel; la composizione
mantiene il lavoro principale, il focus e le bozze. La presentazione spiega
il kernel e rimane una guida raggiungibile durante l'uso.

## Sorgenti e composizione

- `examples/griglia/index.html`: riferimento GPT v5.12 originale, invariato.
- `src/ui/public-griglia.js`: contenuti, dialoghi e protocollo della derivata.
- `examples/public-griglia/PROFILE.json`: significati e primo assetto neutro K-UX-AI.
- `tools/build_public_griglia.py`: compone il profilo con il motore originale.
- `examples/public-griglia/demo/`: HTML generato e identità dei suoi input in BUILD.json.

```sh
python tools/build_public_griglia.py --profile examples/public-griglia/PROFILE.json --output examples/public-griglia/demo
```

Il builder controlla l'identità del riferimento e gli ancoraggi che modifica.
La derivata continua Home, campo, rail, schede, composizione, focus e bozze
di GPT. Un altro kernel conserva il proprio profilo e usa lo stesso builder
e adattatore. I cinque carrier di questa incarnazione sono una forma del
riferimento, non il confine della competenza K-UX-AI.

## Funzioni delle schede

Presentazione e guida spiegano scopo e metodo. Il contributo conserva una
traccia nella sessione; il controllo raccoglie riscontri del caso; il confronto
rende visibili termini condivisi e differenze. Organizzazione e comunicazione
preparano un seguito locale. Gli scenari e gli eventi rendono esplorabile una
possibilità illustrativa. La ripresa raggiunge i contributi della sessione.

La domanda di una scheda mantiene il proprio oggetto anche quando arriva
una risposta dopo un cambio di contesto. Il dialogo generale offre anche un
modulo di contributo locale. Le proposte restano attribuite: l'export le rende
disponibili al kernel che lavora nel contesto e ne può comprendere le conseguenze.

## Dialoghi collegati al servizio MAIOS

Nel sito configurato, Invio manda la domanda esplicita, la sua storia e il
contesto pubblico della scheda a `/api/setup/v1/assistant/site-turn`, con il
contratto `maios.public-assistant-request.v1`. Il backend usa la conoscenza
pubblica del kernel presentato. L'adattatore esclude le altre bozze locali.
Nel server statico semplice l'endpoint manca: la UI rende percepibile quella
indisponibilità. Una fixture può esercitare il trasporto senza inferenza LLM.

Per il campo embedded, il parent invia un target conosciuto e attende la
conferma correlata della scheda effettivamente presente. Solo lo stesso parent
e la stessa origine partecipano. Il parent osserva contesto/attività confermati;
non riceve le note locali o la pretesa di una modifica aziendale.

Il dominio continua a possedere fonti, significati e autorità sui suoi effetti.
L'adozione aziendale collega gli strumenti di quell'ambiente e conserva
il sapere locale. Un aggiornamento sorgente rende disponibile un miglioramento;
la sua adozione preserva la configurazione e le competenze del ricevente.

## Neutral first encounter — 14 October 2026

Home now names K-UX-AI and its interface-construction purpose, introduces
people and AI working with documents, tools and decisions, then explains
the first useful gestures. Five service contexts are Presentation,
Composition, Tools, Interaction and Learning; their source identifiers and
card contracts are unchanged. The neutral Home uses its own compact styles.
The original GPT file and nautical derivative remain byte-identical.

On the MAIOS site candidate, confirmed-view shortcuts scroll the field under
the actual fixed header and respect reduced motion. Four introduction choices
remain visible and nine work-card choices can be expanded. The final bilingual
map explains K-UX-AI's method, environment composition and Grid, with source
links, the original reference, the nautical application and the entry guide.
Publication and assistant activation retain their own receiving owners.
