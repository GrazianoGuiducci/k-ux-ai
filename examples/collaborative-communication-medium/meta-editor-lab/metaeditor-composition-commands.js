/* SPDX-License-Identifier: MPL-2.0
 * Copyright (c) 2026 Graziano Guiducci.
 * MetaEditor: a common insertion request, interpreted by native page/scene editors.
 * Does not own document state, history, selection or layout.
 */
(function(root) {
  'use strict';
  const TYPES = Object.freeze({
    page: Object.freeze(['paragraph','heading','list','callout']),
    scene: Object.freeze(['text','card','tag','section','circle','oval','pill','note'])
  });
  const PAGE_POSITIONS = Object.freeze(['end','before','after']);
  const fail = (reason, carrier) => Object.freeze({ok:false,carrier,reason});

  function create(options) {
    const carrier=options?.carrier;
    const doc=options?.document;
    if (!TYPES[carrier]) throw Error('MetaEditor: unsupported carrier');
    if (!doc || typeof doc.querySelector !== 'function') throw Error('MetaEditor: document required');
    const rootNode=()=>doc.querySelector('#main-content');
    const find=selector=>doc.querySelector(selector);
    const status=()=>Object.freeze({carrier,
      operation:'insert',
      types:TYPES[carrier].slice(),
      positions:carrier==='page'?PAGE_POSITIONS.slice():[],
      nativeHistory:true
    });

    function insertPage(request) {
      const sectionPicker=find('#local-section');
      const kindPicker=find('#local-kind');
      const positionPicker=find('#local-insert-position');
      const button=find('[data-local-action="insert"]');
      const main=rootNode();
      if(!main || !sectionPicker || !kindPicker || !positionPicker || !button || button.disabled) return fail('page editor unavailable','page');
      const position=request.position??'end';
      if(!PAGE_POSITIONS.includes(position)) return fail('unsupported insertion position','page');
      const sectionIndex=request.sectionIndex;
      const previousSection=sectionPicker.value;
      let navigated=false;
      const restoreSection=()=>{
        if(navigated && sectionPicker.value!==previousSection){
          sectionPicker.value=previousSection;
          sectionPicker.dispatchEvent(new doc.defaultView.Event('change',{bubbles:true}));
        }
      };
      if(sectionIndex!==undefined) {
        if(!Number.isInteger(sectionIndex) || sectionIndex<0) return fail('invalid section index','page');
        const option=[...sectionPicker.options].find(item=>item.value===String(sectionIndex));
        if(!option || option.disabled) return fail('destination section unavailable','page');
        if(sectionPicker.value!==option.value) {
          sectionPicker.value=option.value;
          sectionPicker.dispatchEvent(new doc.defaultView.Event('change',{bubbles:true}));
          navigated=true;
        }
      }
      const kind=[...kindPicker.options].find(item=>item.value===request.type);
      if(!kind || kind.disabled) {restoreSection();return fail('native block type unavailable','page');}
      const choice=[...positionPicker.options].find(item=>item.value===position);
      if(!choice || choice.disabled) {restoreSection();return fail('native insertion anchor unavailable','page');}
      kindPicker.value=kind.value;
      positionPicker.value=choice.value;
      const previous=main.querySelectorAll('[data-local-block]').length;
      button.click(); // Only the native editor can change the document and record Undo.
      const created=main.querySelectorAll('[data-local-block]').length-previous;
      if(created!==1){restoreSection();return fail('native insertion did not create exactly one block','page');}
      return Object.freeze({ok:true,carrier:'page',effect:'inserted',type:request.type,position});
    }

    function insertScene(request) {
      if(request.position!==undefined || request.sectionIndex!==undefined) return fail('scene insertion does not use page positions','scene');
      const button=find('[data-add="'+request.type+'"]');
      const canvas=find('#canvas');
      if(!button || !canvas || button.disabled || button.hidden) return fail('scene insertion unavailable','scene');
      const previous=canvas.querySelectorAll('.node[data-id]').length;
      button.click(); // Own scene commit, node IDs, relations and Undo remain native.
      const created=canvas.querySelectorAll('.node[data-id]').length-previous;
      return created===1 ? Object.freeze({ok:true,carrier:'scene',effect:'inserted',type:request.type})
        : fail('native scene insertion did not create exactly one node','scene');
    }

    function execute(action, request={}) {
      if(action!=='insert') return fail('unsupported action',carrier);
      if(!request || typeof request!=='object' || Array.isArray(request)) return fail('invalid request',carrier);
      if(!TYPES[carrier].includes(request.type)) return fail('unsupported type for carrier',carrier);
      return carrier==='page' ? insertPage(request) : insertScene(request);
    }
    return Object.freeze({status,execute});
  }

  root.MetaEditorCompositionCommands=Object.freeze({create});
})(typeof window!=='undefined'?window:globalThis);
