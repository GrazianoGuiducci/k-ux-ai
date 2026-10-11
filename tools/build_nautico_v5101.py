"""K-UX-AI v5.10.1 — exact standalone home layout adjustment.

Usage: python tools/build_nautico_v5101.py [--check]
Retains v5.10 as an attributed local candidate, without transferring its test history.
"""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / 'labs/nautico-ui-v4/22-griglia-motion-contrast-v510.html'
CSS = ROOT / 'tools/kux_home_balance_v5101.css'
OUT = ROOT / 'labs/nautico-ui-v4/23-griglia-home-balance-v5101.html'
BASE_SHA256 = '5b0903536ca128bba527ca4b8d2d7f65c28a7e35edf8b572e10dbc3eef4eb399'
EXPECTED_SHA256 = 'e448bd07dc406a68932e90ff220acc7b509a287cd8b91e9742593794849d6004'


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build() -> bytes:
    raw=BASE.read_bytes()
    if sha(raw)!=BASE_SHA256:
        raise RuntimeError('v5.10 local candidate changed: source identity not qualified')
    content=raw.decode('utf-8')
    old_title='<title>MAIOS · K-UX-AI — Griglia del fare v5.9 · Continuità percettiva</title>'
    new_title='<title>MAIOS · K-UX-AI — Griglia del fare v5.10.1 · Home bilanciata</title>'
    old_description='K-UX-AI v5.9: gerarchia delle schede, tour guidato continuo e microinterazioni. Demo sintetica Nautico.'
    new_description='K-UX-AI v5.10.1: Home bilanciata, copy leggibile e attività senza clipping. Demo sintetica Nautico.'
    for a,b in [(old_title,new_title),(old_description,new_description)]:
        if content.count(a)!=1:
            raise RuntimeError('expected exact header string once: '+a[:75])
        content=content.replace(a,b,1)
    if content.count('</head>')!=1:
        raise RuntimeError('head injection ambiguous')
    css=CSS.read_text(encoding='utf-8')
    content=content.replace('</head>', '<style id="kux-v5101-home-balance">\n'+css+'</style>\n</head>',1)
    result=content.encode('utf-8')
    if EXPECTED_SHA256!='__PENDING__' and sha(result)!=EXPECTED_SHA256:
        raise RuntimeError('v5.10.1 candidate mismatch')
    return result


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    expected=build()
    if args.check:
        if not OUT.exists() or OUT.read_bytes()!=expected:
            raise SystemExit('v5.10.1 output differs from deterministic source')
        print('CHECK PASS',sha(expected))
    else:
        OUT.write_bytes(expected)
        print('BUILT',len(expected),'bytes',sha(expected))

if __name__=='__main__':
    main()
