#!/usr/bin/env python3
"""Correzione verificabile della selezione MetaEditor Bridge08/Codex.

Applica soltanto la correzione del passaggio fra selezione di struttura ed
editing del testo; preserva il file originale e i dati della pagina.
"""
from pathlib import Path
from hashlib import sha256
import argparse

EXPECTED_SOURCE = 'be278d0ddaaf5430c8168d78c18600968453fe242339b4c74272af8caf5f880f'
BEFORE_SELECTION = '''      if (!tools.hidden) {
        tools.hidden = true;
        launcher.setAttribute('aria-expanded', 'false');
      }
    } else {
      setTools(true, false);'''
AFTER_SELECTION = '''      if (!tools.hidden) {
        tools.hidden = true;
        launcher.setAttribute('aria-expanded', 'false');
      }
      // Il referente attivo è il testo, non il vecchio oggetto della struttura.
      // syncTools aggiorna picked e rimuove i contorni di selezione strutturale
      // mentre il pannello è nascosto, senza alterare Range, caret o documento.
      syncTools(section);
    } else {
      setTools(true, false);'''
BEFORE_CONTEXT = '''context.textContent=state.editing?'Modifica in corso':text;
 editBtn.hidden=!!state.editing;'''
AFTER_CONTEXT = '''if(carrier==='codex' && state.editing){
   const field=document.activeElement?.closest?.('#main-content [data-local-editing]') ||
      document.querySelector('#main-content [data-local-editing]');
   const name=safeText(field?.textContent);
   context.textContent=name?'Testo · '+name.slice(0,34)+(name.length>34?'…':''):'Modifica testo';
   context.title=name||'Testo in modifica';
 } else {
   context.textContent=state.editing?'Modifica in corso':text;
   context.removeAttribute('title');
 }
 editBtn.hidden=!!state.editing;'''

def replace_once(src,old,new,label):
    matches=src.count(old)
    if matches!=1: raise ValueError(f'{label}: expected 1 anchor, found {matches}; no file modified')
    return src.replace(old,new)

def fix(source:Path,destination:Path):
    raw=source.read_bytes()
    digest=sha256(raw).hexdigest()
    if digest!=EXPECTED_SOURCE:
        raise ValueError(f'Source drift: {digest}; expected {EXPECTED_SOURCE}; no file modified')
    if source.resolve()==destination.resolve():
        raise ValueError('The original cannot be overwritten')
    data=raw.decode('utf-8')
    data=replace_once(data,BEFORE_SELECTION,AFTER_SELECTION,'selection handoff')
    data=replace_once(data,BEFORE_CONTEXT,AFTER_CONTEXT,'active text indicator')
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(data,encoding='utf-8')
    print(destination,sha256(destination.read_bytes()).hexdigest())

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    fix(args.source,args.output)
