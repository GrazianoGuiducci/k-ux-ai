#!/usr/bin/env python3
"""Deterministic, source-pinned MetaCanvas Studio21 IT/EN release handoff.

Package ONLY the two candidate HTML files after the existing keyboard,
private-link filtering pipelines. This is not a publication or site update.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
import zipfile
from pathlib import Path

from build_studio21_keyboard_section_move import build as build_keyboard, SOURCE_BLOBS
from build_studio21_public_projection import build as build_safe

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "collaborative-communication-medium"
VERSION = "Studio21-privacy-rc.1"
MANIFEST = "VERSIONE_E_FILE.json"
NAMES = ("MetaCanvas_Studio21_Consulenza_IT.html", "MetaCanvas_Studio21_Consulenza_EN.html")
GUIDE = """MetaCanvas Studio21 IT/EN — candidato di correzione per release

Questo archivio contiene due copie HTML autonome IT/EN costruite dai
sorgenti Studio21 pubblicati e verificati per hash. La modifica candidata
mantiene i figli delle sezioni durante il movimento da tastiera e
rimuove i link con private:true dalle proiezioni pubbliche, dati AI e
template. Il documento di lavoro conserva i propri dati fino all'export.

L'intero flusso è stato verificato con test browser sul candidato.
Queste sono COPIE PER IL RILASCIO, non la versione già pubblicata e
non una nuova versione del tool generale o del Playground.

Non sostituire i file di MAIOS.it o di main sulla base di questo ZIP:
l'owner del sito deve decidere nomi/versioni delle nuove copie,
verificare gli hash, aggiornare i collegamenti IT/EN e fare readback
del contenuto effettivamente servito. Conservare la baseline attuale.
La licenza del codice è MPL-2.0, con NOTICE e testo integrale inclusi.

Il manifest contiene checksum SHA-256 dei file distribuiti e
identificativi Git blob esatti dei sorgenti di partenza.
Lo stato della release è: candidata, NON pubblicata.
"""


def build_pack(output: Path, source_root: Path = EXAMPLES) -> None:
    output = output.resolve()
    source_root = source_root.resolve()
    if output.exists():
        raise ValueError(f"Refusing to overwrite existing pack: {output}")
    if not source_root.is_dir():
        raise FileNotFoundError(source_root)
    with tempfile.TemporaryDirectory(prefix="metacanvas-studio21-rc-") as tmp:
        base = Path(tmp)
        keyboard = base / "keyboard"
        safe = base / "safe"
        build_keyboard(source_root, keyboard)
        build_safe(keyboard, safe)
        staged = {name: (safe / name).read_bytes() for name in NAMES}
        staged["LEGGIMI_RILASCIO.txt"] = GUIDE.encode("utf-8")
        staged["LICENZA_MPL-2.0.txt"] = (source_root / "LICENSE").read_bytes()
        staged["NOTICE_ORIGINALE.md"] = (source_root / "NOTICE.md").read_bytes()
        manifest = {
            "schema": "metacanvas.studio21.release-candidate.v1",
            "version": VERSION,
            "status": "not-published",
            "source_pins_git_blob": dict(sorted(SOURCE_BLOBS.items())),
            "replaced_by_site_owner_only": True,
            "files_sha256": {
                name: hashlib.sha256(data).hexdigest()
                for name, data in sorted(staged.items())
            },
        }
        staged[MANIFEST] = (json.dumps(manifest, ensure_ascii=False,
                           sort_keys=True, indent=2) + "\n").encode("utf-8")
        output.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED,
                             compresslevel=9) as archive:
            for name, data in sorted(staged.items()):
                item = zipfile.ZipInfo(name)
                item.date_time = (2026, 11, 23, 10, 0, 0)
                item.compress_type = zipfile.ZIP_DEFLATED
                item.external_attr = 0o644 << 16
                archive.writestr(item, data)
    print("CREATED", output, "files", len(staged), "SHA256",
          hashlib.sha256(output.read_bytes()).hexdigest())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-zip", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, default=EXAMPLES)
    args = parser.parse_args()
    build_pack(args.output_zip, args.source_root)


if __name__ == "__main__":
    main()
