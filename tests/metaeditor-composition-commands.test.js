// SPDX-License-Identifier: MPL-2.0
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';

const code=readFileSync(new URL('../examples/collaborative-communication-medium/meta-editor-lab/metaeditor-composition-commands.js',import.meta.url),'utf8');
const sandbox={};runInNewContext(code,sandbox);
const {create}=sandbox.MetaEditorCompositionCommands;
function mockPage(){
 let count=0, clicks=0;
 const main={querySelectorAll:()=>Array.from({length:count},()=>({}))};
 const choice=value=>({value,disabled:false});
 const section={value:'0',options:[choice('0'),choice('1')],dispatchEvent() {this.changed=true;}};
 const kind={value:'paragraph',options:['paragraph','heading','list','callout'].map(choice)};
 const position={value:'end',options:['end','before','after'].map(choice)};
 const button={disabled:false,click(){count++;clicks++;}};
 const selectors={'#main-content':main,'#local-section':section,'#local-kind':kind,'#local-insert-position':position,'[data-local-action="insert"]':button};
 const document={querySelector:q=>selectors[q]||null,defaultView:{Event:class Event{}}};
 return {document,section,position,clicks:()=>clicks,count:()=>count,button};
}
function mockScene(){
 let count=1,clicks=0;
 const canvas={querySelectorAll:q=>q==='.node[data-id]'?Array(count).fill({}):[]};
 const controls={text:{click(){count++;clicks++}},card:{click(){count++;clicks++}}};
 const document={querySelector:q=>q==='#canvas'?canvas:q==='[data-add="text"]'?controls.text:q==='[data-add="card"]'?controls.card:null};
 return {document,clicks:()=>clicks,count:()=>count};
}
test('page: delegates native insertion without owning history',()=>{
 const state=mockPage();const commands=create({carrier:'page',document:state.document});
 assert.deepEqual([...commands.status().types],['paragraph','heading','list','callout']);
 assert.equal(commands.execute('insert',{type:'heading',position:'end',sectionIndex:1}).ok,true);
 assert.equal(state.count(),1);assert.equal(state.clicks(),1);assert.equal(state.section.value,'1');
});
test('page: rejects invalid kind/position and disabled anchor without native mutation',()=>{
 const state=mockPage();const commands=create({carrier:'page',document:state.document});
 assert.equal(commands.execute('insert',{type:'text'}).ok,false);
 assert.equal(commands.execute('insert',{type:'paragraph',position:'adjacent'}).ok,false);
 state.position.options.find(x=>x.value==='before').disabled=true;
 assert.equal(commands.execute('insert',{type:'paragraph',position:'before'}).ok,false);
 assert.equal(state.count(),0);
});
test('page: unsupported relative position restores prior section selection',()=>{
 const state=mockPage();const commands=create({carrier:'page',document:state.document});
 const original=state.section.dispatchEvent;
 state.section.dispatchEvent=function(){original.call(this);state.position.options.find(x=>x.value==='before').disabled=this.value==='1';};
 const result=commands.execute('insert',{type:'paragraph',position:'before',sectionIndex:1});
 assert.equal(result.ok,false);assert.equal(state.section.value,'0');assert.equal(state.count(),0);
});
test('page: unavailable panel does not pretend success',()=>{
 const state=mockPage();state.button.disabled=true;
 assert.equal(create({carrier:'page',document:state.document}).execute('insert',{type:'paragraph'}).ok,false);
 assert.equal(state.clicks(),0);
});
test('scene: delegates native scene node insertion but refuses page semantics',()=>{
 const state=mockScene();const commands=create({carrier:'scene',document:state.document});
 assert.deepEqual([...commands.status().types].slice(0,3),['text','card','tag']);
 assert.equal(commands.execute('insert',{type:'paragraph'}).ok,false);
 assert.equal(commands.execute('insert',{type:'text',position:'before'}).ok,false);
 assert.equal(commands.execute('insert',{type:'text'}).ok,true);
 assert.equal(state.count(),2);assert.equal(state.clicks(),1);
});
test('scene: unavailable native control and unsupported operations fail closed',()=>{
 const state=mockScene();const commands=create({carrier:'scene',document:state.document});
 assert.equal(commands.execute('move',{type:'text'}).ok,false);
 assert.equal(commands.execute('insert',{type:'note'}).ok,false);
 assert.equal(state.clicks(),0);
});
