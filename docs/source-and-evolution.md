# Sorgenti selezionate e continuità del prodotto

Il kernel pubblico porta una derivazione operativa delle capacità del
produttore: generazione e trasferimento di kernel, Meta_Skill, UX-AI,
Design e costruzione del medium. Questa derivazione conserva significato,
metodo e apprendimento raggiungibili nel prodotto. Le sorgenti interne
mantengono contesti di formazione e profondità che non sono dipendenze runtime.

## Meccanismi di kernel di competenza

La formazione riusa sapere del produttore già incarnato in kernel complessi
di gestione ed espressione: un owner semantico, facoltà componibili,
fonti e ragioni che partecipano al metodo, incarnazioni nei riceventi e
apprendimento che cambia il prossimo lavoro.

K-UX-AI deriva questi meccanismi per il proprio campo percettivo e operativo.
Il metodo pubblico conserva la capacità di comprenderli ed esercitarli;
contenuti di dominio e contesti interni restano alle sorgenti di formazione.

## Codice originale selezionato

Il nucleo `src/medium.js` conserva il contratto pubblico della versione
0.1.0-alpha.1. Window Surface e Chat/Form, con i CSS associati, sono selezionati
dalle sorgenti originali del ramo K-UX-AI UI alla revisione
`45152db3ca5e7dca1de524f7d02301adbe857cfe`:
[origine pubblica](https://github.com/GrazianoGuiducci/k-ux-ai/tree/45152db3ca5e7dca1de524f7d02301adbe857cfe/src/ui).

I comportamenti studiati da altre sorgenti hanno informato il metodo;
questo pacchetto non importa asset Rive, codice di altri owner, endpoint,
dati aziendali o diritti di quelle sorgenti. Il collegamento MessagePort
e il workspace neutrale sono costruzioni originali di questa versione.

La Griglia v5.12 è selezionata nella sua sorgente originale e resa
raggiungibile in examples/griglia/index.html. Il file dell'operatore
KUX_Griglia_v5_12_Chat_Attivita.html coincide con la sorgente a quella revisione:
SHA-256 1879dbe0d2ccba4c7db4701fe067c05ad1d20761aa2a6cf053f90b478118430b.
Builder, iterazioni e prove attribuite rimangono nel ramo d'origine.
Una nuova integrazione o un esercizio separato conserva la propria identità.

## Versione e riuso

Lo stato alpha descrive la distribuzione sorgente del kernel e del medium.
Non rappresenta maturità universale, installazione di un agente o una release
npm. La visibilità pubblica del repository e la distribuzione sorgente restano
distinte dalla licenza e dai diritti degli eventuali asset aggiunti.
Questo consolidamento non cambia le condizioni di licenza del repository
né introduce una licenza upstream per supposizione.

Le future versioni possono ampliare renderer, adattatori e sapere conservando
contratti e identità utili. Il ricevente mantiene evoluzioni e dati propri
e può insegnare al prodotto attraverso il contributo autorizzato che possiede.

## Costruire la presentazione interattiva

`examples/griglia/index.html` conserva il riferimento GPT v5.12 originale.
`src/ui/public-griglia.js` fornisce contenuti, dialoghi e osservazione delle
viste. `examples/public-griglia/PROFILE.json` definisce il servizio K-UX-AI;
un kernel di dominio usa un profilo proprio. Il builder compone questi file
senza modificare l’originale e registra le identità in BUILD.json.

```sh
python tools/build_public_griglia.py --profile examples/public-griglia/PROFILE.json --output examples/public-griglia/demo
```

La domanda esplicita usa `/api/setup/v1/assistant/site-turn` con lo schema
`maios.public-assistant-request.v1`. Per un campo incorporato, il sito attende
una conferma correlata della vista effettiva, verifica origine e frame e
non riceve le altre note locali. Un host statico può servire l’interfaccia
senza fornire il servizio AI. Una fixture esercita il trasporto senza LLM.
I cinque identificatori di contesto sono compatibilità del riferimento;
i loro nomi e significati appartengono al profilo ospitante.

Queste informazioni servono alla costruzione e all’integrazione tecnica.
La [guida all’uso](public-griglia.md) conduce l’incontro con il prodotto.

## English and Italian builds

English is the default public UI. `PROFILE.json` and `demo/` carry English;
`PROFILE.it.json` and `demo/it/` support Italian. Install pinned build dependencies
with `npm ci --ignore-scripts`. The compiler uses `tools/localize_public_griglia.mjs`
and the semantic-key `src/ui/locales/public-workspace.json` catalogue. The tours
use `src/ui/locales/public-tours.json`. Source-reference bytes remain unchanged;
JavaScript literals and template chunks are localised during build, preserving
code expressions. Visitor drafts and model replies are not translated.

```sh
npm ci --ignore-scripts
python tools/build_public_griglia.py --profile examples/public-griglia/PROFILE.json --output examples/public-griglia/demo
python tools/build_public_griglia.py --profile examples/public-griglia/PROFILE.json --output examples/public-griglia/demo/it --locale it
```

Both builds record locale and source identities. A hosting page must select the
artifact matching its locale and pass that locale to the conversation endpoint.
