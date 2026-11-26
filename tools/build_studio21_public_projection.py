#!/usr/bin/env python3
"""Build private-data-safe Studio21 candidates from the verified Arrow-move candidates.

Never mutates the distributed Studio21 originals. Four existing native
projections gain one explicit check: links marked private must not be exported
to public HTML, default AI JSON, saved templates or template reuse.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

SOURCE_BLOBS = {
    "MetaCanvas_Studio21_Consulenza_IT.html": "698d28bf3ddbd38197ec48d776726f43d2f693bc",
    "MetaCanvas_Studio21_Consulenza_EN.html": "10294b195cb49243dc356861cf10e9061ad78e2a",
}
REPLACEMENTS = {
    "s.links=s.links.filter(l=>(!l.from||s.elements.some(n=>n.id===l.from))&&(!l.to||s.elements.some(n=>n.id===l.to)))":
    "s.links=s.links.filter(l=>l.private!==true&&(!l.from||s.elements.some(n=>n.id===l.from))&&(!l.to||s.elements.some(n=>n.id===l.to)))",

    "sc.links=sc.links.filter(l=>(!l.from||ids.has(l.from))&&(!l.to||ids.has(l.to)))":
    "sc.links=sc.links.filter(l=>l.private!==true&&(!l.from||ids.has(l.from))&&(!l.to||ids.has(l.to)))",

    "sc.links=(sc.links||[]).filter(l=>(!l.from||ids.has(l.from))&&(!l.to||ids.has(l.to)))":
    "sc.links=(sc.links||[]).filter(l=>l.private!==true&&(!l.from||ids.has(l.from))&&(!l.to||ids.has(l.to)))",

    "sc.links=sc.links.filter(l=>(!l.from||map.has(l.from))&&(!l.to||map.has(l.to)))":
    "sc.links=sc.links.filter(l=>l.private!==true&&(!l.from||map.has(l.from))&&(!l.to||map.has(l.to)))",
}


def blob_sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()


def build(source_root: Path, output_root: Path):
    if source_root.resolve() == output_root.resolve():
        raise ValueError("Refusing to overwrite the source directory")
    output_root.mkdir(parents=True, exist_ok=True)
    for name, expected in SOURCE_BLOBS.items():
        source = (source_root / name).read_bytes()
        current = blob_sha(source)
        if current != expected:
            raise ValueError(f"{name}: input candidate changed: {current} != {expected}")
        html = source.decode("utf-8")
        for anchor, replacement in REPLACEMENTS.items():
            count = html.count(anchor)
            if count != 1:
                raise ValueError(f"{name}: projection anchor count {count}; expected exactly one")
            html = html.replace(anchor, replacement)
        output = output_root / name
        output.write_text(html, encoding="utf-8")
        print("BUILT", name, "blob", blob_sha(output.read_bytes()))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True,
                        help="Directory with the pinned Arrow-move candidate")
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()
    build(args.source_root, args.output_root)


if __name__ == "__main__":
    main()
