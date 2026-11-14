# MetaCanvas — candidata alla distribuzione

La coppia Playground r4 porta la guida modificabile e rimovibile nelle
due lingue. Al passo 3 si esporta una scheda o si confronta una proposta
di esempio. Al passo 4 si scarica l'HTML. La demo Consulenza AI resta
disponibile come esempio applicativo.

| Artefatto | Uso |
| --- | --- |
| [Guida e Playground IT](MetaCanvas_Guida_Playground_r4_IT.html) | Primo incontro in italiano |
| [Guide and Playground EN](MetaCanvas_Guida_Playground_r4_EN.html) | Primo incontro in inglese |
| [Editor neutro](AI_Collaboration_Studio.html) | Composizione di un documento di lavoro |

L'editor neutro include il contorno del canvas e il calcolo dello spazio
utile dal contributo [aaa6702](https://github.com/GrazianoGuiducci/k-ux-ai/commit/aaa6702eb3d82ce086c486bf18b9e1e942958124)
nato nel raccordo con Apollo. Il documento di Apollo resta nel suo progetto
e usa il modello dati portabile dell'editor. Il
[metodo condiviso](../../competences/ux-ai/collaborative-communication-medium/GUIDE.md)
segue le migliorie che emergono dai casi d'uso.

Per ricostruire i due HTML Playground dalla directory:
`python -B build_playground.py .`. Il generatore applica un tetto di
500.000 byte per file. Le copie IT/EN misurano 288.033 e 308.864 byte. Gli
HTML includono l'avviso di licenza. [Licenza MPL 2.0](LICENSE).

Verifica della candidata: apertura da file in Chrome Windows, 1440×900
e 390×844, contorno del canvas, modifica e salvataggio HTML dei tre
artefatti. Il modello salvato conserva il numero di schede e la modifica.
Segue la revisione autoriale delle anteprime IT/EN della scheda MAIOS.it.
La pubblicazione seleziona i byte da servire come download diretto.
