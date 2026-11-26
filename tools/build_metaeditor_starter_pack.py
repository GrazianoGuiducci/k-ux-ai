#!/usr/bin/env python3
"""Create a local-first MetaEditor start pack with independent starter documents.

Four original, synthetic HTML template sources are shipped in K-UX-AI; the
distributed ZIP contains only a chooser, individually editable work pages and
instructions. No MetaCanvas ccm.document.v1 templates are converted.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
import zipfile
from pathlib import Path

from build_metaeditor_neutral_workpage import build, LAB, MODULES

TEMPLATES = {
    "Essenziale": "essenziale.html",
    "Progetto": "progetto.html",
    "Articolo": "articolo.html",
    "Da_zero": "vuota.html",
}
ROOT = LAB / "starter-templates"
GALLERY = ROOT / "Apri_MetaEditor.html"
VERSION = "1.0.0-rc.1"
MANIFEST = "VERSIONE_E_FILE.json"
LICENSE_SOURCE = LAB.parent / "LICENSE"
NOTICE_SOURCE = LAB.parent / "NOTICE.md"
CREDITS = """MetaEditor 1.0 RC — crediti e ambito di licenza

Il pacchetto include codice dell'editor nella directory:
GrazianoGuiducci/k-ux-ai/examples/collaborative-communication-medium/

Copyright (c) 2026 Graziano Guiducci.
Licenza del codice coperto: Mozilla Public License 2.0.
Il testo integrale della licenza è in LICENZA_MPL-2.0.txt.
La nota originale del tool è in NOTICE_ORIGINALE.md.

La licenza del codice dell'editor non trasferisce automaticamente
la titolarità delle pagine, dei testi, delle immagini e dei contenuti
realizzati da chi usa lo strumento, che seguono i propri diritti.

Sorgente del tool:
https://github.com/GrazianoGuiducci/k-ux-ai
Il progetto non concede diritti su marchi o loghi.
Questo archivio è un release candidate non ancora pubblicato.
"""

GUIDE = """MetaEditor — scegli da dove iniziare

1. Estrai TUTTO il contenuto dello ZIP in una cartella.
2. Fai doppio clic su Apri_MetaEditor.html (si apre in Chrome).
3. Seleziona uno dei quattro modelli. Ogni scelta apre una nuova scheda
   con una copia di lavoro indipendente e già modificabile.
4. Seleziona un testo e usa Modifica testo. Oppure aggiungi un blocco
   nella sezione scelta.
5. Prima di chiudere la scheda, premi Salva lavoro per ottenere un
   nuovo HTML modificabile. Esporta pagina pulita crea invece una pagina
   senza i comandi MetaEditor.

La scelta del modello non sovrascrive file esistenti. La schermata
di scelta e i quattro modelli sono esempi sintetici, senza dati
riservati e senza collegamenti a servizi remoti.

MetaEditor 1.0 RC — una prima versione con confini precisi

COSA PUOI FARE:
- Modificare il testo e la formattazione semplice di una pagina modello.
- Inserire titoli, paragrafi, collegamenti e immagini locali supportate.
- Riordinare i blocchi aggiunti e posizionarli con riferimenti precisi.
- Annullare/ripristinare e salvare una copia di lavoro modificabile.
- Esportare una pagina HTML pulita, senza il pannello di modifica.

UN PERCORSO COMPLETO:
1. Apri Pagina essenziale.
2. Cambia il titolo, poi termina la modifica.
3. Aggiungi un paragrafo e un collegamento.
4. Scegli una tua immagine PNG/JPEG/WebP/GIF (max 1,5 MB)
   e scrivi la descrizione accessibile.
5. Annulla e ripristina una modifica.
6. Premi Salva lavoro o Ctrl+S: controlla che il file HTML sia scaricato.
7. Riapri quel file: deve ritornare l'editor con il lavoro conservato.
8. Premi Esporta pagina pulita: controlla che il file scaricato
   contenga la pagina senza l'interfaccia MetaEditor.

COSA NON È:
- Un CMS, un editor HTML universale o un sistema di pubblicazione.
- Un editor di scene/presentazioni MetaCanvas.
- Un programma con salvataggio automatico permanente.
- Uno strumento per aprire codice HTML sconosciuto o non fidato.

Le quattro pagine sono esempi locali e non inviano dati a server.
Lo ZIP include la licenza del codice MPL-2.0, i crediti originali e
un manifest VERSIONE_E_FILE.json con gli SHA-256
di tutti i file distribuiti; non include pagine MAIOS riservate.
La copia di lavoro incorpora l'intero originale: trattala come privata.
Questa è una candidata RC, non una release pubblica approvata.
La prova umana di usabilità rimane distinta dai test automatici.
"""


def stage(destination: Path) -> list[Path]:
    destination.mkdir(parents=True, exist_ok=True)
    if any(destination.iterdir()):
        raise ValueError("Refusing to populate an output folder that is not empty")
    if not GALLERY.is_file():
        raise FileNotFoundError(GALLERY)
    modules = [(LAB / name).read_text(encoding="utf-8") for name in MODULES]
    produced = []
    index = destination / "Apri_MetaEditor.html"
    index.write_text(GALLERY.read_text(encoding="utf-8"), encoding="utf-8")
    produced.append(index)
    workdir = destination / "Modelli"
    workdir.mkdir()
    for short, source_name in TEMPLATES.items():
        original = (ROOT / "sources" / source_name).read_text(encoding="utf-8")
        work = build(original, *modules)
        output = workdir / (short + ".html")
        output.write_text(work, encoding="utf-8")
        produced.append(output)
    guide = destination / "LEGGIMI.txt"
    guide.write_text(GUIDE, encoding="utf-8")
    produced.append(guide)
    if not LICENSE_SOURCE.is_file() or not NOTICE_SOURCE.is_file():
        raise FileNotFoundError("Missing owner-native MPL license or notice")
    license_file = destination / "LICENZA_MPL-2.0.txt"
    license_file.write_bytes(LICENSE_SOURCE.read_bytes())
    produced.append(license_file)
    notice_file = destination / "NOTICE_ORIGINALE.md"
    notice_file.write_bytes(NOTICE_SOURCE.read_bytes())
    produced.append(notice_file)
    credit_file = destination / "CREDITI_E_CONDIZIONI.txt"
    credit_file.write_text(CREDITS, encoding="utf-8")
    produced.append(credit_file)

    files = {
        file.relative_to(destination).as_posix():
            hashlib.sha256(file.read_bytes()).hexdigest()
        for file in produced
    }
    manifest = {
        "schema": "metaeditor.local-pack.v1",
        "product": "MetaEditor",
        "version": VERSION,
        "status": "release-candidate-not-published",
        "entrypoint": "Apri_MetaEditor.html",
        "source_scope": "four built-in trusted static HTML examples only",
        "files_sha256": dict(sorted(files.items())),
    }
    manifest_path = destination / MANIFEST
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    produced.append(manifest_path)
    return produced


def pack(path: Path) -> None:
    path = path.resolve()
    if path.exists():
        raise ValueError(f"Output already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="metaeditor-starter-") as tmp:
        base = Path(tmp)
        produced = stage(base)
        with zipfile.ZipFile(path, "x", compression=zipfile.ZIP_DEFLATED,
                             compresslevel=9) as archive:
            for file in sorted(produced, key=lambda f: f.relative_to(base).as_posix()):
                info = zipfile.ZipInfo(file.relative_to(base).as_posix())
                info.date_time = (2026, 11, 23, 10, 0, 0)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                archive.writestr(info, file.read_bytes())
    print("CREATED", path, "entries", len(produced))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-zip", type=Path, required=True)
    args = parser.parse_args()
    pack(args.output_zip)


if __name__ == "__main__":
    main()
