#!/usr/bin/env python3
"""Build (without publishing) Studio21 HTML candidates with coherent keyboard movement.

The source is pinned to the current K-UX-AI public Studio21 IT/EN files. Only the
native keyboard handler is changed. No document model, renderer, or new history
owner is introduced.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

SOURCE_BLOBS={
    'MetaCanvas_Studio21_Consulenza_IT.html':'cba76881d4afbb48c0fa38f76bbd04eda764f7c9',
    'MetaCanvas_Studio21_Consulenza_EN.html':'dfddc6d1de728b45996a3f6628ea657da8db33f9',
}
SOURCE='commit(()=>{n.x=clamp(n.x+dx,0,WIDTH-n.w);n.y=clamp(n.y+dy,0,HEIGHT-n.h);setContainerAfterMove(n)})'
REPLACEMENT='''const nextX=clamp(n.x+dx,0,WIDTH-n.w),nextY=clamp(n.y+dy,0,HEIGHT-n.h);
  const movedX=nextX-n.x,movedY=nextY-n.y;
  if(!movedX&&!movedY)return;
  commit(()=>{
   n.x=nextX;n.y=nextY;
   if(n.type==='section'){
    // Keyboard and pointer movements must preserve the native group relation.
    for(const child of current().elements.filter(x=>x.containerId===n.id)){
     child.x=clamp(child.x+movedX,0,WIDTH-child.w);
     child.y=clamp(child.y+movedY,0,HEIGHT-child.h);
    }
   }else setContainerAfterMove(n);
  })'''


def blob_sha(raw: bytes) -> str:
    header=b'blob '+str(len(raw)).encode('ascii')+b'\0'
    return hashlib.sha1(header+raw).hexdigest()


def build(source_root: Path, output_root: Path) -> None:
    output_root.mkdir(parents=True,exist_ok=True)
    for name,expected in SOURCE_BLOBS.items():
        src=source_root/name
        raw=src.read_bytes()
        observed=blob_sha(raw)
        if observed!=expected:
            raise ValueError(f'{name}: source drift: {observed} != {expected}')
        data=raw.decode('utf-8')
        if data.count(SOURCE)!=1:
            raise ValueError(f'{name}: native keyboard source anchor ambiguous')
        patched=data.replace(SOURCE,REPLACEMENT)
        target=output_root/name
        target.write_bytes(patched.encode('utf-8'))
        print('BUILT',name,'blob',blob_sha(target.read_bytes()))


def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument('--source-root',type=Path,default=Path(__file__).resolve().parents[1]/'examples/collaborative-communication-medium')
    p.add_argument('--output-root',type=Path,required=True)
    args=p.parse_args()
    build(args.source_root,args.output_root)

if __name__=='__main__':
    main()
