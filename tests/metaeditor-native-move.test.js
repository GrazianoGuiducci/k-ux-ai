// SPDX-License-Identifier: MPL-2.0
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';

const code=readFileSync(new URL('../examples/collaborative-communication-medium/meta-editor-lab/metaeditor-native-move.js',import.meta.url),'utf8');
const sandbox={};
runInNewContext(code,sandbox);
const {create}=sandbox.MetaEditorNativeMove;

function sceneMock({x=20,reading=false,presenting=false}={}) {
  let dispatchCount=0;
  const node={
    dataset:{id:'scene-1'}, tabIndex:0,
    style:{left:x+'%',top:'20%',width:'10%',height:'10%'},
    querySelector:()=>null,
    dispatchEvent(event){
      dispatchCount++;
      if(event.key==='ArrowRight')this.style.left=(parseFloat(this.style.left)+5/1200*100)+'%';
      if(event.key==='ArrowLeft')this.style.left=(parseFloat(this.style.left)-5/1200*100)+'%';
    }
  };
  const canvas={querySelectorAll:selector=>selector==='.node[data-id]'?[node]:[]};
  const document={
    querySelector:selector=>selector==='#canvas'?canvas:null,
    body:{classList:{contains:name=>name==='reading-mode'?reading:name==='presenting'?presenting:false}},
    defaultView:{KeyboardEvent:class KeyboardEvent{constructor(type,options){this.key=options.key;}}}
  };
  return {document,node,dispatches:()=>dispatchCount};
}

test('distinct move semantics remain visible in status',()=>{
  const scene=sceneMock();
  const s=create({carrier:'scene',document:scene.document}).status();
  assert.equal(s.operation,'nudge-scene-node');
  assert.deepEqual(Array.from(s.directions),['left','right','up','down']);
  assert.deepEqual(Array.from(s.placements),[]);
  const page=create({carrier:'page',document:{querySelector:()=>null}}).status();
  assert.equal(page.operation,'place-added-block');
  assert.deepEqual(Array.from(page.placements),['end','before','after']);
});

test('scene: native key handler, not external state mutation, performs one nudge',()=>{
  const scene=sceneMock();
  const move=create({carrier:'scene',document:scene.document});
  const prior=scene.node.style.left;
  const result=move.execute({nodeId:'scene-1',direction:'right'});
  assert.equal(result.ok,true);
  assert.equal(result.operation,'nudge-scene-node');
  assert.notEqual(scene.node.style.left,prior);
  assert.equal(scene.dispatches(),1);
});

test('scene: invalid reference, page position or inherited direction fail closed',()=>{
  const scene=sceneMock();
  const move=create({carrier:'scene',document:scene.document});
  assert.equal(move.execute({nodeId:'missing',direction:'right'}).ok,false);
  assert.equal(move.execute({nodeId:'scene-1',direction:'toString'}).ok,false);
  assert.equal(move.execute({nodeId:'scene-1',direction:'__proto__'}).ok,false);
  assert.equal(move.execute({nodeId:'scene-1',direction:'right',placement:'before'}).ok,false);
  assert.equal(move.execute([]).ok,false);
  assert.equal(scene.dispatches(),0);
});

test('scene: read and presentation modes forbid mutation',()=>{
  for(const opts of [{reading:true},{presenting:true}]) {
    const scene=sceneMock(opts);
    assert.equal(create({carrier:'scene',document:scene.document})
      .execute({nodeId:'scene-1',direction:'right'}).ok,false);
    assert.equal(scene.dispatches(),0);
  }
});

test('scene: boundary nudge fails before recording a native checkpoint',()=>{
  const scene=sceneMock({x:0});
  assert.equal(create({carrier:'scene',document:scene.document})
    .execute({nodeId:'scene-1',direction:'left'}).ok,false);
  assert.equal(scene.dispatches(),0);
});

test('page: no native selected block means no move and no synthetic fallback',()=>{
  const cmd=create({carrier:'page',document:{querySelector:()=>null}});
  assert.equal(cmd.execute({sectionIndex:0,placement:'end'}).ok,false);
  assert.throws(()=>create({carrier:'unknown',document:{querySelector:()=>null}}));
});
