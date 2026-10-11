"""Reproduce K-UX-AI v5.12 from the exact exercised v5.11 laboratory HTML.

This remains a synthetic local Nautico example, not the K-UX-AI released package.

Run: python tools/build_nautico_v512.py [--check]
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASELINE = ROOT / 'labs/nautico-ui-v4/24-griglia-content-hierarchy-v511.html'
OUTPUT = ROOT / 'labs/nautico-ui-v4/25-griglia-rail-composer-v512.html'
CSS = ROOT / 'tools/kux_rail_chat_v512.css'
BASE_SHA256 = '67e8a1104d2abd66b886fad5354753a4db8964321c93947937de15f1917f434a'
OUTPUT_SHA256 = '1879dbe0d2ccba4c7db4701fe067c05ad1d20761aa2a6cf053f90b478118430b'


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def once(source: str, before: str, after: str) -> str:
    n = source.count(before)
    if n != 1:
        raise RuntimeError(f'Expected exactly one source target; found {n}: {before[:92]!r}')
    return source.replace(before, after, 1)


def generate() -> bytes:
    raw = BASELINE.read_bytes()
    if sha(raw) != BASE_SHA256:
        raise RuntimeError(f'v5.11 base drift: {sha(raw)}')
    s = raw.decode('utf-8')
    s = once(s,
        'K-UX-AI v5.11: gerarchia del contenuto nelle schede, stato Attività riconciliato e animazioni contestuali. Demo sintetica Nautico.',
        'K-UX-AI v5.12: continuità nel fissare la barra Attività e chat a una riga espandibile. Demo sintetica Nautico.')
    s = once(s,
        '<title>MAIOS · K-UX-AI — Griglia del fare v5.11 · Gerarchia e continuità</title>',
        '<title>MAIOS · K-UX-AI — Griglia del fare v5.12 · Attività e chat continua</title>')
    # Empty composer at rest, one line; an explicit accessible name remains available.
    s = once(s,
        "const ask=div('','textarea');ask.placeholder='Scrivi una domanda…';ask.rows=2;ask.setAttribute('aria-label','Messaggio chat');",
        "const ask=div('','textarea');ask.placeholder='';ask.rows=1;ask.setAttribute('aria-label','Scrivi un messaggio nella chat');")
    # A programmatic clear after send must also shrink the field back to one line.
    s = once(s,
        "busy=true;askButton.disabled=true;appendMessage('operator',msg);ask.value='';",
        "busy=true;askButton.disabled=true;appendMessage('operator',msg);ask.value='';ask.dispatchEvent(new Event('input',{bubbles:true}));")
    # Pinning a rail already perceived in peek must continue its current motion.
    # Replaying the reveal (clipPath 100% -> 0) caused the reported disappearance.
    s = once(s,
        "if(next==='hidden'||!['hidden','peek','icons'].includes(previous))return;",
        "if(next==='hidden'||previous==='peek'&&next==='icons'||!['hidden','peek','icons'].includes(previous))return;")
    # The edge trigger disappears after pinning; keyboard focus returns to a live control.
    s = once(s,
        "activityEdge.addEventListener('click',()=>setActivitiesMode('icons'));",
        "activityEdge.addEventListener('click',()=>{setActivitiesMode('icons');railVisibility.focus({preventScroll:true});});")
    # The v5.10 autosize helper was hard-coded to a two-row minimum even for empty chat.
    s = once(s,
        "const next=Math.min(Math.max(textarea.scrollHeight,54),190);",
        "const floor=textarea.closest('.kux-chat-inputrow')?46:54;const next=Math.min(Math.max(textarea.scrollHeight,floor),190);")
    s = once(s,
        "version:'lab-2026-10-11-r5.9',liveAI:false",
        "version:'lab-2026-10-11-r5.12',liveAI:false")
    s = once(s, '</head>', '<style id="kux-v512-rail-chat">\n'+CSS.read_text(encoding='utf-8')+'\n</style>\n</head>')
    return s.encode('utf-8')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    a=parser.parse_args()
    built=generate();digest=sha(built)
    if OUTPUT_SHA256!='1879dbe0d2ccba4c7db4701fe067c05ad1d20761aa2a6cf053f90b478118430b' and digest!=OUTPUT_SHA256:
        raise RuntimeError(f'Unexpected v5.12 digest: {digest}')
    if a.check:
        if not OUTPUT.exists() or OUTPUT.read_bytes()!=built:
            raise SystemExit('Failed exact builder check')
        print('OK exact v5.12 SHA-256 '+digest)
    else:
        OUTPUT.write_bytes(built)
        print(f'Wrote {OUTPUT.name}; {len(built)} bytes; SHA-256 {digest}')

if __name__=='__main__':main()
