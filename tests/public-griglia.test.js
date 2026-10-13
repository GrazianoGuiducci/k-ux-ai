import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

function receiver(fetch) {
  const profile=JSON.parse(fs.readFileSync(new URL('../examples/public-griglia/PROFILE.json',import.meta.url),'utf8'));
  const window={__UXAI_CONFIG__:{profile}},listeners={},wire=[];
  const document={addEventListener(){},dispatchEvent(){},getElementById(){return {};}};
  const parent={postMessage:data=>wire.push(data)};
  let id=0,focused;
  const state={screen:'work',activeContext:'poppa',panels:[],notes:[{text:'PRIVATE-DRAFT-DO-NOT-SEND'}]};
  const core={state,getFocused:()=>focused,switchWorkspaceContext:c=>{state.activeContext=c;},activateScreen:s=>{state.screen=s;},openPanel:(intent,context,options)=>{focused={intent,context,options,el:{isConnected:true,getClientRects:()=>[{}]}};return focused;}};
  const scope={window,parent,document,location:{origin:'https://maios.test'},fetch,crypto:{randomUUID:()=>`id-${++id}`},getComputedStyle:()=>({display:'block',visibility:'visible'}),CustomEvent:class{},MutationObserver:class{observe(){}},requestAnimationFrame:fn=>fn(),addEventListener:(name,fn)=>{listeners[name]=fn;}};
  vm.runInNewContext(fs.readFileSync(new URL('../src/ui/public-griglia.js',import.meta.url),'utf8'),scope);
  window.KUXHostedGriglia.install(core);
  return {api:window.KUXHostedGriglia,state,profile,listeners,parent,wire};
}

test('explicit questions use their own public context and history and omit other drafts',async()=>{
  const payloads=[];
  const r=receiver(async(_url,request)=>{payloads.push(JSON.parse(request.body));return {ok:true,json:async()=>({message:'A public answer'})};});
  const first=await r.api.askShared({text:'First question',context:'poppa'});
  assert.equal(first.reply,'A public answer');
  await r.api.askShared({text:'Second question',context:'poppa'});
  await r.api.askShared({text:'Different context',context:'cantiere'});
  assert.equal(payloads[0].history.length,0);
  assert.deepEqual(payloads[1].history,[{role:'user',content:'First question'},{role:'assistant',content:'A public answer'}]);
  assert.equal(payloads[2].history.length,0);
  assert.equal(payloads[2].context.active_label,'Composizione · capire');
  assert.equal(JSON.stringify(payloads).includes('PRIVATE-DRAFT-DO-NOT-SEND'),false);
  assert.deepEqual(payloads[0].allowed_action_kinds,['focus_section']);
  assert.notEqual(payloads[0].request_id,payloads[1].request_id);
});

test('a failed connection creates no learning proposal; a later reply retains its card owner',async()=>{
  let succeed=false;
  const r=receiver(async()=>{if(!succeed)throw new Error('No connection');return {ok:true,json:async()=>({message:'A proposal to discuss'})};});
  const discussions=r.api.createDiscussions();
  r.state.panels=[{id:'card-a',context:'poppa',intent:'capire'},{id:'card-b',context:'cantiere',intent:'fare'}];
  discussions.post('card-a','A question',r.profile.contexts.poppa);
  await new Promise(resolve=>setImmediate(resolve));
  assert.equal(discussions.propose('card-a'),null);
  succeed=true;
  discussions.post('card-b','Another question',r.profile.contexts.cantiere);
  r.state.activeContext='fornitori';
  await new Promise(resolve=>setImmediate(resolve));
  const proposal=discussions.propose('card-b');
  assert.equal(proposal.owner,'card-b');
  assert.equal(proposal.context,'Composizione');
  assert.equal(proposal.status,'proposed_not_applied');
  const exported=discussions.exportPacket('card-b');
  assert.equal(exported.assimilated,false);
  assert.equal(exported.authority,'proposal_only');
  assert.equal(discussions.getMessages('card-a').length,2);
});

test('only the matching same-origin parent can select a known target and receive confirmation',()=>{
  const r=receiver(async()=>{throw new Error('Not invoked');});
  r.listeners.message({source:r.parent,origin:'https://wrong.test',data:{schema:'kux.public-view-hello.v2',session:'s'}});
  assert.equal(r.wire.length,1);
  r.listeners.message({source:r.parent,origin:'https://maios.test',data:{schema:'kux.public-view-hello.v2',session:'s'}});
  r.listeners.message({source:r.parent,origin:'https://maios.test',data:{schema:'kux.public-view-command.v2',session:'s',requestId:'r',target:'kux-fare'}});
  assert.equal(r.wire.at(-1).schema,'kux.public-view-state.v2');
  assert.equal(r.wire.at(-1).requestId,'r');
  assert.equal(r.wire.at(-1).target,'kux-fare');
  assert.equal(r.wire.at(-1).ok,true);
  r.listeners.message({source:r.parent,origin:'https://maios.test',data:{schema:'kux.public-view-command.v2',session:'s',requestId:'bad',target:'__proto__'}});
  assert.equal(r.wire.at(-1).ok,false);
});
