#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
# Copyright (c) 2026 Graziano Guiducci.
"""Rebuild MetaEditor Bridge08 UX from the exact two Bridge07 HTML carriers.

Uses bridge08_ui.css + bridge08_ui.js beside this file. Never overwrites its inputs.
Example:
  python bridge08_build.py --codex MetaEditor_Bridge07_Bozza_Codex_IT.html \
    --studio MetaEditor_Bridge07_Studio21_IT.html --out-dir bridge08-out
"""
from pathlib import Path
from hashlib import sha256
import argparse

SOURCE_HASHES = {
    "codex": "1ab5e4589953302ddd16b7b98dcd9c3017b7b61db63908a5dc43d93bc24b77f8",
    "studio": "e709d738531fa1023c404e4bbc8fc3326d3fc6033ca38ee7d391e07867da3a89",
}
FOLDER = Path(__file__).resolve().parent


def build(source: Path, kind: str, destination: Path) -> None:
    raw = source.read_bytes()
    found = sha256(raw).hexdigest()
    if found != SOURCE_HASHES[kind]:
        raise SystemExit(f"Source drift ({kind}): {found}; expected {SOURCE_HASHES[kind]}")
    body = raw.decode("utf-8")
    if body.count("</body>") != 1 or 'id="me08-ui-runtime"' in body:
        raise SystemExit(f"Ambiguous or already modified HTML: {source}")

    css = (FOLDER / "bridge08_ui.css").read_text(encoding="utf-8")
    js = (FOLDER / "bridge08_ui.js").read_text(encoding="utf-8")
    if js.count("const carrier='__CARRIER__';") != 1:
        raise SystemExit("Invalid Bridge08 carrier placeholder")

    # Studio public copies must not even contain the UX08 authoring source.
    if kind == "studio":
        anchor = "let doc=document.documentElement.cloneNode(true);"
        if body.count(anchor) != 1:
            raise SystemExit("Studio export contract changed, no output written")
        body = body.replace(
            anchor,
            anchor + "if(publicCopy){doc.querySelectorAll("
            "'#me08-launcher,#me08-dialog,#me08-toast,#me08-ui-style,#me08-ui-runtime'"
            ").forEach(n=>n.remove());}",
        )
    layer = (
        '<style id="me08-ui-style">' + css + "</style>\n"
        '<script id="me08-ui-runtime">' + js.replace("__CARRIER__", kind) + "</script>"
    )
    output = body.replace("</body>", layer + "\n</body>")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(output, encoding="utf-8")
    print(destination, sha256(destination.read_bytes()).hexdigest())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex", required=True, type=Path)
    parser.add_argument("--studio", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()
    build(args.codex, "codex", args.out_dir / "MetaEditor_Bridge08_Bozza_Codex_IT.html")
    build(args.studio, "studio", args.out_dir / "MetaEditor_Bridge08_Studio21_IT.html")
