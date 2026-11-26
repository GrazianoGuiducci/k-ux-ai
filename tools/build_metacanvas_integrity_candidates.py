#!/usr/bin/env python3
"""Build the five manifest-pinned MetaCanvas integrity candidates.

Reuse the existing keyboard and public-projection patches, not a second
implementation. The distribution baseline and historical Studio21 builders
remain untouched. Outputs are standalone, unpublished candidates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from build_studio21_keyboard_section_move import SOURCE, REPLACEMENT, blob_sha
from build_studio21_public_projection import REPLACEMENTS

EXAMPLES = Path(__file__).resolve().parents[1] / "examples" / "collaborative-communication-medium"
MANIFEST = EXAMPLES / "distribution-manifest.json"
MODEL = re.compile(r'<script id="ccm-data" type="application/json">(.*?)</script>', re.S)


def build(output_root: Path, source_root: Path = EXAMPLES) -> list[Path]:
    output_root, source_root = output_root.resolve(), source_root.resolve()
    if output_root == source_root or (output_root.exists() and any(output_root.iterdir())):
        raise ValueError("Refusing to overwrite source or an existing candidate directory")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = manifest["artifacts"]
    names = [Path(entry["source"]).name for entry in entries]
    if len(names) != 5 or len(set(names)) != 5:
        raise ValueError("Distribution carrier set changed; review manifest coverage")
    results = {}
    receipt = {}
    for entry, name in zip(entries, names):
        raw = (source_root / name).read_bytes()
        if blob_sha(raw) != entry["git_blob"] or hashlib.sha256(raw).hexdigest() != entry["sha256"]:
            raise ValueError(f"{name}: source drift against distribution manifest")
        original = raw.decode("utf-8")
        html = original
        for before, after in [(SOURCE, REPLACEMENT), *REPLACEMENTS.items()]:
            if html.count(before) != 1:
                raise ValueError(f"{name}: ambiguous integrity patch anchor: {before[:75]}")
            html = html.replace(before, after, 1)
        old_model, new_model = MODEL.search(original), MODEL.search(html)
        if not old_model or not new_model or old_model.group(1) != new_model.group(1):
            raise ValueError(f"{name}: document model changed")
        patched = html.encode("utf-8")
        results[name] = patched
        receipt[name] = {
            "source_blob": entry["git_blob"],
            "candidate_blob": blob_sha(patched),
            "candidate_sha256": hashlib.sha256(patched).hexdigest(),
            "locale": entry["locale"],
            "status": "unpublished-integrity-candidate",
        }
    # Validate the complete set before creating any output.
    output_root.mkdir(parents=True, exist_ok=True)
    for name, data in results.items():
        (output_root / name).write_bytes(data)
        print("BUILT", name, receipt[name]["candidate_blob"])
    (output_root / "integrity-receipt.json").write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return [output_root / name for name in names]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, default=EXAMPLES)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()
    build(args.output_root, args.source_root)
