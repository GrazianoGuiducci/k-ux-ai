#!/usr/bin/env python3
"""Create a local-first MetaEditor start pack with independent starter documents.

Four original, synthetic HTML template sources are shipped in K-UX-AI; the
distributed ZIP contains only a chooser, individually editable work pages and
instructions. No MetaCanvas ccm.document.v1 templates are converted.
"""
from __future__ import annotations

import argparse
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

Questa è una candidata di prova locale per pagine HTML statiche.
I template per le scene di MetaCanvas sono un altro formato.
Non sostituisce una verifica umana di Chrome Windows file://.
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
            for file in produced:
                info = zipfile.ZipInfo(file.relative_to(base).as_posix())
                info.date_time = (2026, 11, 22, 10, 0, 0)
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
