#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
# Copyright (c) 2026 Graziano Guiducci.
"""Rebuild MetaEditor Bridge06 from two exact original HTML carriers.

python bridge06_build.py --codex 'MAIOS_Consulenza_AI_revisionata(1).html' \
    --studio MetaCanvas_Studio21_Consulenza_IT.html --out-dir bridge06-out

Both sources are read-only. Requires Python 3.11+ standard library only.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

CODEX_SHA256 = "f227b61b0a813ad7312f805dcec63def03b87201d5d5fb6ae0ae729d2541f190"
STUDIO_SHA256 = "abbdbd9e749453434fddb140505c0586ce594990739742c8106f37ab542165df"

CODEX_BEFORE = """    setTools(true, false);
    picked = element;
    selectToolTab(resizable(element) ? 'local-size' : 'local-view-element');
    syncTools(section);
    if (field) {
      miniDismissed = null;
      openMini(field);
    }
  });"""
CODEX_AFTER = """    // Bridge06: edit rich text in situ without showing the entire inspector.
    // Do not call setTools(false), because it would stop the direct edit.
    if (field && !editing) {
      picked = element;
      if (!tools.hidden) {
        tools.hidden = true;
        launcher.setAttribute('aria-expanded', 'false');
      }
    } else {
      setTools(true, false);
      picked = element;
      selectToolTab(resizable(element) ? 'local-size' : 'local-view-element');
      syncTools(section);
    }
    if (field) {
      miniDismissed = null;
      openMini(field);
    }
  });"""

STUDIO_BEFORE = "else if(count===2){laterQuick('node',n.id);}"
STUDIO_AFTER = """else if(count===2){
  // The wrapper captures pointerup, so use the visual hit to identify text.
  if((document.elementFromPoint(e.clientX,e.clientY)?.closest('.node-text')||e.target.closest('.node-text'))&&n.type!=='image'){
   if(quickTimer){clearTimeout(quickTimer);quickTimer=null}
   closeQuick();startDirectEdit(n.id);
  }else{laterQuick('node',n.id)}
 }"""

def patch(source: Path, expected_hash: str, before: str, after: str) -> str:
    raw = source.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != expected_hash:
        raise SystemExit(f"Source drift at {source}: {digest}; expected {expected_hash}. No patch applied.")
    text = raw.decode("utf-8")
    if text.count(before) != 1:
        raise SystemExit(f"Interaction anchor missing or ambiguous in {source}")
    return text.replace(before, after)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex", type=Path, required=True)
    parser.add_argument("--studio", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, default=Path("bridge06-out"))
    args = parser.parse_args()

    codex = patch(args.codex, CODEX_SHA256, CODEX_BEFORE, CODEX_AFTER)
    studio = patch(args.studio, STUDIO_SHA256, STUDIO_BEFORE, STUDIO_AFTER)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for name, text in (
        ("MetaEditor_Bridge06_Bozza_Codex_IT.html", codex),
        ("MetaEditor_Bridge06_Studio21_Consulenza_IT.html", studio),
    ):
        destination = args.out_dir / name
        destination.write_text(text, encoding="utf-8")
        print(destination)

if __name__ == "__main__":
    main()
