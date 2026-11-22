/* SPDX-License-Identifier: MPL-2.0
 * Copyright (c) 2026 Graziano Guiducci.
 * Move requests delegate to native page/scene controllers and their history.
 * This module does not own document state, coordinates, layout or Undo.
 */
(function(root) {
  'use strict';
  const fail=(carrier,reason)=>Object.freeze({ok:false,carrier,reason});
  const PAGE_PLACEMENTS=['end','before','after'];
  const SCENE_DIRECTIONS={left:'ArrowLeft',right:'ArrowRight',up:'ArrowUp',down:'ArrowDown'};
  const WIDTH=1200,HEIGHT=675,STEP=5; // Studio21's documented scene coordinates and native key step.

  function create({carrier,document:doc}={}) {
    if(carrier!=='page' && carrier!=='scene') throw Error('MetaEditor move: unsupported carrier');
    if(!doc || typeof doc.querySelector!=='function') throw Error('MetaEditor move: document required');
    const find=selector=>doc.querySelector(selector);
    const status=()=>Object.freeze({carrier,action:'move',nativeHistory:true,
      operation:carrier==='page'?'place-added-block':'nudge-scene-node',
      placements:carrier==='page'?PAGE_PLACEMENTS.slice():[],
      directions:carrier==='scene'?Object.keys(SCENE_DIRECTIONS):[]});

    function movePage(request) {
      const main=find('#main-content'), tools=find('#local-tools');
      const targetSection=find('#local-destination'), target=find('#me11-target'),side=find('#me11-side');
      const button=find('[data-local-action="transfer"]');
      if(!main || !tools || tools.hidden || !targetSection || !target || !side || !button || button.disabled)
        return fail(carrier,'native page transfer unavailable');
      const source=main.querySelector('[data-local-picked][data-local-block]');
      if(!source || !source.isConnected) return fail(carrier,'select an added block in the native editor first');
      if(request.nodeId!==undefined || request.direction!==undefined)
        return fail(carrier,'page placement does not use scene coordinates');
      if(!Number.isInteger(request.sectionIndex) || request.sectionIndex<0)
        return fail(carrier,'invalid destination section');
      const sectionOption=[...targetSection.options].find(o=>o.value===String(request.sectionIndex) && !o.disabled);
      if(!sectionOption) return fail(carrier,'destination section unavailable');
      const placement=request.placement??'end';
      if(!PAGE_PLACEMENTS.includes(placement)) return fail(carrier,'unsupported page placement');
      if(placement!=='end' && (!Number.isInteger(request.targetIndex) || request.targetIndex<0))
        return fail(carrier,'invalid reference index');
      if(placement==='end' && request.targetIndex!==undefined)
        return fail(carrier,'end placement does not use a reference');

      const original={section:targetSection.value,target:target.value,side:side.value};
      const fire=el=>el.dispatchEvent(new doc.defaultView.Event('change',{bubbles:true}));
      const restore=()=>{
        if(targetSection.value!==original.section){targetSection.value=original.section;fire(targetSection);}
        if([...target.options].some(o=>o.value===original.target)){target.value=original.target;fire(target);}
        if([...side.options].some(o=>o.value===original.side))side.value=original.side;
      };
      if(targetSection.value!==sectionOption.value){targetSection.value=sectionOption.value;fire(targetSection);}
      if(placement!=='end'){
        const choice=[...target.options].find(o=>o.value===String(request.targetIndex) && !o.disabled);
        if(!choice){restore();return fail(carrier,'reference not safe in destination');}
        target.value=choice.value;fire(target);
        const sideOption=[...side.options].find(o=>o.value===placement && !o.disabled);
        if(!sideOption){restore();return fail(carrier,'native relative placement unavailable');}
        side.value=placement;
      }else{
        target.value='end';fire(target);
      }
      const oldParent=source.parentElement,oldNext=source.nextElementSibling;
      button.click(); // Native Bridge11 transfer does the single Undo checkpoint.
      const destSections=main.querySelectorAll(':scope > section, :scope > article, :scope > [data-metaeditor-region]');
      const actual=source.closest('main > section, main > article, main > [data-metaeditor-region]');
      if(!source.isConnected || actual!==destSections[request.sectionIndex])
        return fail(carrier,'native transfer did not reach intended section');
      if(oldParent===source.parentElement && oldNext===source.nextElementSibling){
        restore();return fail(carrier,'already positioned; no document change');
      }
      return Object.freeze({ok:true,carrier,effect:'moved',operation:'place-added-block',
        sectionIndex:request.sectionIndex,placement});
    }

    function moveScene(request) {
      if(typeof request.nodeId!=='string' || !request.nodeId.trim())return fail(carrier,'nodeId required');
      const key=SCENE_DIRECTIONS[request.direction];
      if(!Object.hasOwn(SCENE_DIRECTIONS,request.direction) ||
         request.placement!==undefined || request.sectionIndex!==undefined || request.targetIndex!==undefined)
        return fail(carrier,'use a native scene nudge direction');
      const canvas=find('#canvas');
      if(!canvas || doc.body?.classList.contains('presenting') ||
         doc.body?.classList.contains('reading-mode') || doc.body?.classList.contains('public-copy'))
        return fail(carrier,'scene unavailable in current mode');
      const nodes=[...canvas.querySelectorAll('.node[data-id]')];
      const node=nodes.find(el=>el.dataset.id===request.nodeId);
      if(!node || node.tabIndex<0 || node.querySelector('.node-edit'))
        return fail(carrier,'editable scene node not available');
      const n=(prop,limit)=>parseFloat(node.style[prop])/100*limit;
      const x=n('left',WIDTH),y=n('top',HEIGHT),w=n('width',WIDTH),h=n('height',HEIGHT);
      if(![x,y,w,h].every(Number.isFinite))return fail(carrier,'invalid scene geometry');
      if((key==='ArrowLeft' && x<=0) || (key==='ArrowRight' && x>=WIDTH-w) ||
         (key==='ArrowUp' && y<=0) || (key==='ArrowDown' && y>=HEIGHT-h))
        return fail(carrier,'node already at canvas boundary');
      const before={left:node.style.left,top:node.style.top};
      node.dispatchEvent(new doc.defaultView.KeyboardEvent('keydown',{key,bubbles:true,cancelable:true}));
      const moved=[...canvas.querySelectorAll('.node[data-id]')].find(el=>el.dataset.id===request.nodeId);
      if(!moved || (moved.style.left===before.left && moved.style.top===before.top))
        return fail(carrier,'native scene nudge did not move node');
      return Object.freeze({ok:true,carrier,effect:'moved',operation:'nudge-scene-node',
        nodeId:request.nodeId,direction:request.direction,step:STEP});
    }
    function execute(request={}){
      if(!request || typeof request!=='object' || Array.isArray(request))return fail(carrier,'invalid request');
      return carrier==='page'?movePage(request):moveScene(request);
    }
    return Object.freeze({status,execute});
  }
  root.MetaEditorNativeMove=Object.freeze({create});
})(typeof window!=='undefined'?window:globalThis);
