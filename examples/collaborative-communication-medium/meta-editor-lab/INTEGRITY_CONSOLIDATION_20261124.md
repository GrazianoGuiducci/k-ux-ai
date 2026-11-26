# MetaCanvas — consolidamento comune, 24 novembre 2026

Ripresa operatore dopo il [riesame source-first](QUALITY_REVIEW_SOURCE_FIRST_20261124.md).
Le cinque sorgenti sono state rilette: pin Git del manifest concordanti,
ciascuna delle cinque ancore compare una sola volta. La prima scena di
Playground e dell'editor generale usa ID diversi da Studio21: la fixture
di movimento sceglie il referente realmente disponibile anziché imporre d1-c.

Il builder `tools/build_metacanvas_integrity_candidates.py` usa il manifest
di distribuzione e importa le correzioni native già esistenti (tastiera e
quattro proiezioni privacy). Conserva il modello JSON integrale; richiede
blob e SHA256 esatti; verifica il gruppo prima di scrivere; produce una
ricevuta con identità dei cinque HTML. Nessun originale, asset del sito o
versione pubblica modificato. I builder Studio21 storici restano invariati.

Il test integrato riusa le prove browser di privacy e movimento, con fixture
adattata al referente reale; verifica parità byte con la precedente coppia
Studio21, determinismo, rifiuto del drift e assenza di modifiche agli originali.
Il job CI dedicato esercita i cinque portatori a 1440 e 390 px e allega
i candidati solo dopo esito positivo. Al momento della proposta la prova
browser del nuovo insieme è da osservare, non già passata.

Prossimo contributo dopo il riscontro: coordinamento Focus/Flat, selezione,
proprietà e template sul runtime corrente. Il candidato integrità non
include ancora la barra R1 e non è un rilascio o un test d'uso umano.
