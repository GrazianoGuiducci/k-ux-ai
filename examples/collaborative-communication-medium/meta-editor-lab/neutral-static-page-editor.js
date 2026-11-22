/* SPDX-License-Identifier: MPL-2.0
 * Copyright (c) 2026 Graziano Guiducci.
 * MetaEditor static-page workbench: one opt-in controller for trusted static HTML.
 * Uses MetaEditorStaticPageAdapter for source-faithful clean export.
 * Does not import unknown HTML, publish the source or control scene ccm.document.v1.
 */
(function(root) {
  'use strict';
  const LOCAL = 'data-local-';
  const EDITABLE = 'p,h1,h2,h3,h4,h5,h6,li,blockquote,figcaption';
  const fail = message => { throw new Error('MetaEditor static workbench: ' + message); };
  const escapeHtml = text => String(text).replace(/[&<>"]/g, c =>
    ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  function mount({document: doc, sourceHtml}) {
    if (!doc || !doc.defaultView || !doc.querySelector) fail('document required');
    if (doc.querySelector('#me-neutral-toolbar') || root.__metaEditorNeutralMounted) fail('already mounted');
    const main = doc.querySelector('main');
    if (!main) fail('no main element');
    if (!root.MetaEditorStaticPageAdapter) fail('static-page source adapter required');
    const exporter = root.MetaEditorStaticPageAdapter.create({sourceHtml, regionElement:main});
    const allowedMain = doc.querySelectorAll('main');
    if (allowedMain.length !== 1) fail('exactly one main required');
    const sectionRoots = () => [...main.querySelectorAll(':scope > section, :scope > article > section')];
    const safeNode = node => node && main.contains(node) && node.matches(EDITABLE) &&
      !node.closest('[contenteditable="false"],form,nav,aside,script,style');
    let selected = null, editing = null, beforeTyping = null;
    let history = [], future = [];
    let dirty = false;
    const toolbar = doc.createElement('aside');
    toolbar.id = 'me-neutral-toolbar';
    toolbar.setAttribute('aria-label', 'MetaEditor – editor locale');
    toolbar.innerHTML =
      '<strong>MetaEditor · HTML statico</strong>' +
      '<p>File di lavoro locale. Pubblica solo l’HTML pulito dopo averlo controllato.</p>' +
      '<label for="me-neutral-element">Elemento da modificare</label>' +
      '<select id="me-neutral-element" aria-label="Elemento da modificare"></select>' +
      '<label for="me-neutral-section">Sezione di destinazione</label>' +
      '<select id="me-neutral-section"></select>' +
      '<div class="me-neutral-actions">' +
      '<button data-me-action="edit">Modifica testo</button>' +
      '<button data-me-action="bold">Grassetto</button>' +
      '<button data-me-action="italic">Corsivo</button>' +
      '<button data-me-action="insert-p">+ Paragrafo</button>' +
      '<button data-me-action="insert-h">+ Titolo</button>' +
      '<button data-me-action="up">↑ Sposta</button>' +
      '<button data-me-action="down">↓ Sposta</button>' +
      '<button data-me-action="transfer">Sposta a sezione</button>' +
      '<button data-me-action="duplicate">Duplica blocco aggiunto</button>' +
      '<button data-me-action="delete">Elimina blocco aggiunto</button>' +
      '<button data-me-action="undo">Annulla</button>' +
      '<button data-me-action="redo">Ripristina</button>' +
      '<button data-me-action="clean">Esporta pagina pulita</button>' +
      '<button data-me-action="work">Salva lavoro modificabile</button>' +
      '</div><p id="me-neutral-status" role="status" aria-live="polite"></p>';
    const style = doc.createElement('style');
    style.id = 'me-neutral-style';
    style.textContent = [
      '#me-neutral-toolbar{position:fixed;z-index:2147483000;right:12px;top:12px;width:min(350px,calc(100vw - 24px));',
      'max-height:calc(100dvh - 24px);overflow:auto;box-sizing:border-box;padding:12px;background:#fff;color:#182d37;',
      'border:1px solid #a5bcb6;border-radius:10px;box-shadow:0 5px 25px #0003;font:13px/1.4 system-ui,sans-serif}',
      '#me-neutral-toolbar *{box-sizing:border-box}#me-neutral-toolbar strong{display:block;font-size:15px}',
      '#me-neutral-toolbar p{margin:6px 0}#me-neutral-toolbar select{width:100%;padding:5px;margin:3px 0 8px}',
      '#me-neutral-toolbar .me-neutral-actions{display:grid;grid-template-columns:1fr 1fr;gap:5px}',
      '#me-neutral-toolbar button{cursor:pointer;padding:7px 4px;background:#f1f7f5;border:1px solid #a7c6ba;border-radius:5px;color:#123128}',
      '#me-neutral-toolbar button:disabled{opacity:.5;cursor:not-allowed}',
      '#me-neutral-toolbar button:focus-visible{outline:2px solid #087b70;outline-offset:2px}',
      'main [data-local-selected]{outline:2px solid #087b70;outline-offset:2px}',
      'main [data-local-editing]{outline:2px dashed #087b70;outline-offset:2px}',
      '@media(max-width:500px){#me-neutral-toolbar{top:auto;bottom:8px;max-height:38dvh}}',
    ].join('');
    doc.head.append(style);
    doc.body.append(toolbar);
    const selector = toolbar.querySelector('#me-neutral-section');
    const elementPicker = toolbar.querySelector('#me-neutral-element');
    const status = toolbar.querySelector('#me-neutral-status');
    const button = action => toolbar.querySelector('[data-me-action="' + action + '"]');
    const pristineSource = sourceHtml;

    function workRootSnapshot() {
      const clone = main.cloneNode(true);
      for (const element of [clone, ...clone.querySelectorAll('*')]) {
        element.removeAttribute('contenteditable');
        element.removeAttribute('data-local-selected');
        element.removeAttribute('data-local-editing');
      }
      // These are work/history snapshots, NOT public HTML. An inserted block
      // retains data-local-block across Undo/Redo and save/reopen; the source
      // adapter removes that marker only for clean export.
      return clone;
    }
    const snapshot = () => workRootSnapshot().innerHTML;
    function notify(message) { status.textContent = message; }
    const selectableNodes = () => [...main.querySelectorAll(EDITABLE)].filter(safeNode);
    function refreshElements() {
      const nodes = selectableNodes();
      elementPicker.replaceChildren();
      const blank = doc.createElement('option');
      blank.value = '-1';
      blank.textContent = '— Seleziona un elemento —';
      elementPicker.append(blank);
      nodes.forEach((node, index) => {
        const option = doc.createElement('option');
        option.value = String(index);
        const title = node.textContent.trim().replace(/\s+/g, ' ').slice(0, 62);
        option.textContent = node.localName.toUpperCase() + ': ' + (title || 'Testo vuoto');
        elementPicker.append(option);
      });
      const current = nodes.indexOf(selected);
      elementPicker.value = String(current);
      return nodes;
    }
    function refreshSections() {
      const former = selector.value;
      const sections = sectionRoots();
      selector.replaceChildren();
      sections.forEach((node, index) => {
        const title = node.querySelector('h1,h2,h3,h4,h5,h6')?.textContent.trim() || node.id || 'Sezione ' + (index + 1);
        const option = doc.createElement('option');
        option.value = String(index);
        option.textContent = String(index + 1) + '. ' + title.slice(0, 65);
        selector.append(option);
      });
      if (sections.length && [...selector.options].some(o => o.value === former)) selector.value = former;
      refreshElements();
      return sections;
    }
    function record(before) {
      if (before == null) return false;
      const after = snapshot();
      if (after === before) return false;
      history.push(before);
      if (history.length > 80) history.shift();
      future = [];
      dirty = true;
      syncButtons();
      return true;
    }
    function leaveEditing() {
      if (!editing) return;
      const current = editing, previous = beforeTyping;
      editing = null; beforeTyping = null;
      current.removeAttribute('contenteditable');
      current.removeAttribute('data-local-editing');
      record(previous);
    }
    function select(element) {
      if (editing && editing !== element) leaveEditing();
      if (selected && selected.isConnected) selected.removeAttribute('data-local-selected');
      selected = safeNode(element) ? element : null;
      if (selected) {
        selected.setAttribute('data-local-selected','true');
        const section = sectionRoots().findIndex(section => section.contains(selected));
        if (section >= 0) selector.value = String(section);
      }
      refreshElements();
      syncButtons();
      return !!selected;
    }
    function syncButtons() {
      const active = selected && selected.isConnected;
      for (const action of ['edit','bold','italic']) button(action).disabled = !active;
      const movable = !!active && selected.hasAttribute('data-local-block');
      for (const action of ['up','down','transfer','duplicate','delete']) button(action).disabled = !movable;
      button('undo').disabled = history.length === 0;
      button('redo').disabled = future.length === 0;
      button('insert-p').disabled = sectionRoots().length === 0;
      button('insert-h').disabled = sectionRoots().length === 0;
    }
    function edit() {
      if (!selected || !selected.isConnected) return {ok:false,reason:'select text first'};
      if (editing === selected) return {ok:true,noop:true};
      leaveEditing();
      beforeTyping = snapshot();
      editing = selected;
      editing.setAttribute('contenteditable','true');
      editing.setAttribute('data-local-editing','true');
      editing.focus();
      notify('Modifica il testo; esci dal campo per registrare una modifica.');
      return {ok:true};
    }
    function format(command) {
      if (!['bold','italic'].includes(command) || !editing) return {ok:false,reason:'edit mode required'};
      const selection = doc.getSelection();
      if (!selection || !selection.rangeCount || selection.isCollapsed ||
          !editing.contains(selection.anchorNode) || !editing.contains(selection.focusNode)) {
        return {ok:false,reason:'select an editable text range'};
      }
      const success = doc.execCommand(command, false, null);
      if (success) notify('Formattazione applicata; esci dal testo per registrarla.');
      return {ok:!!success};
    }
    function transact(effect) {
      leaveEditing();
      const before = snapshot();
      const output = effect();
      const changed = record(before);
      refreshSections();
      syncButtons();
      return {ok:true,changed,...(output || {})};
    }
    // A section is a semantic boundary, not necessarily its content column.
    // In MAIOS and other real layouts the text lives inside nested flow wrappers.
    // Inserting directly into <section> can put new blocks outside the layout.
    const flowTags = 'p,h1,h2,h3,h4,h5,h6,blockquote';
    function flowChild(node, section) {
      const parent = node?.parentElement;
      return !!(node && parent && section.contains(node) &&
        node.matches(flowTags) &&
        ['div','section','article'].includes(parent.localName) &&
        !parent.closest('nav,aside,form,figure,ul,ol,table'));
    }
    function insertionPoint(section, useSelection = true) {
      if (!section) return null;
      if (useSelection && flowChild(selected, section)) {
        return {parent:selected.parentElement, after:selected};
      }
      const headings = [...section.querySelectorAll('h1,h2,h3,h4,h5,h6')];
      const labelled = (section.getAttribute('aria-labelledby') || '')
        .trim().split(/\s+/).filter(Boolean);
      const heading = labelled.length ?
        headings.find(h => labelled.includes(h.id)) :
        headings.find(h => flowChild(h, section));
      if (!flowChild(heading, section)) return null;
      const parent = heading.parentElement;
      // Only direct text-flow siblings: never append to a CSS grid, list,
      // nav or wrapper guessed from its class name.
      const siblings = [...parent.children].filter(n =>
        flowChild(n, section) && n.parentElement === parent);
      return {parent, after:siblings[siblings.length - 1] || heading};
    }
    function insertAtPoint(node, point) {
      if (!point || point.after.parentElement !== point.parent) return false;
      point.after.insertAdjacentElement('afterend', node);
      return true;
    }
    function insert(tag) {
      const sections = sectionRoots();
      const index = Number(selector.value);
      if (!['p','h3'].includes(tag) || !Number.isInteger(index) || !sections[index]) {
        return {ok:false,reason:'no supported destination'};
      }
      leaveEditing();
      const point = insertionPoint(sections[index]);
      if (!point) {
        return {ok:false,reason:'layout destination ambiguous: select a text paragraph or heading in this section'};
      }
      const sectionHeading = sections[index].querySelector('h1,h2,h3,h4,h5,h6');
      const headingLevel = sectionHeading ?
        Math.min(6, Number(sectionHeading.localName.slice(1)) + 1) : 3;
      const actualTag = tag === 'h3' ? 'h' + headingLevel : 'p';
      return transact(() => {
        const node = doc.createElement(actualTag);
        node.setAttribute('data-local-block', 'true');
        node.textContent = tag === 'p' ? 'Nuovo paragrafo' : 'Nuovo titolo';
        insertAtPoint(node, point);
        select(node);
        notify('Blocco aggiunto nel contenitore del testo selezionato.');
      });
    }
    function move(action) {
      if (!selected || !selected.hasAttribute('data-local-block') || !selected.isConnected) {
        return {ok:false,reason:'only added blocks can move'};
      }
      const node = selected;
      if (action === 'transfer') {
        const sections = sectionRoots();
        const next = sections[Number(selector.value)];
        if (!next) return {ok:false,reason:'invalid destination'};
        // A transfer to the current section is a no-op, not an opportunity
        // to silently relocate an existing block across grid/layout groups.
        if (next.contains(node)) return {ok:true,changed:false};
        const point = insertionPoint(next, false);
        if (!point) return {ok:false,reason:'layout destination ambiguous: cannot transfer safely'};
        return transact(() => {
          insertAtPoint(node, point);
          select(node);
          notify('Blocco trasferito nel contenitore testuale di destinazione.');
        });
      }
      if (action === 'up' && node.previousElementSibling) {
        return transact(() => node.parentElement.insertBefore(node, node.previousElementSibling));
      }
      if (action === 'down' && node.nextElementSibling) {
        return transact(() => node.parentElement.insertBefore(node.nextElementSibling, node));
      }
      return {ok:true,changed:false};
    }
    function changeAddedBlock(action) {
      if (!selected || !selected.isConnected || !selected.hasAttribute('data-local-block')) {
        return {ok:false,reason:'only inserted blocks may be duplicated or deleted'};
      }
      const node = selected;
      if (action === 'duplicate') {
        // A clone with author IDs would break document references; decline
        // instead of producing a second element with the same ID.
        if (node.id || node.querySelector('[id]')) {
          return {ok:false,reason:'cannot duplicate a block containing an ID'};
        }
        return transact(() => {
          const copy = node.cloneNode(true);
          copy.removeAttribute('data-local-selected');
          copy.removeAttribute('data-local-editing');
          copy.removeAttribute('contenteditable');
          node.insertAdjacentElement('afterend', copy);
          select(copy);
          notify('Blocco aggiunto duplicato. La modifica è annullabile.');
        });
      }
      if (action === 'delete') {
        return transact(() => {
          node.remove();
          select(null);
          notify('Blocco aggiunto eliminato. Puoi usare Annulla.');
        });
      }
      return {ok:false,reason:'unsupported action'};
    }
    function restore(html) {
      leaveEditing();
      if (selected?.isConnected) selected.removeAttribute('data-local-selected');
      selected = null;
      main.innerHTML = html;
      refreshSections();
      syncButtons();
    }
    function undo() {
      leaveEditing();
      if (!history.length) return {ok:true,changed:false};
      const before = snapshot();
      const previous = history.pop();
      future.push(before);
      restore(previous);
      dirty = true;
      notify('Annullato.');
      return {ok:true,changed:true};
    }
    function redo() {
      leaveEditing();
      if (!future.length) return {ok:true,changed:false};
      const before = snapshot();
      history.push(before);
      const next = future.pop();
      restore(next);
      dirty = true;
      notify('Ripristinato.');
      return {ok:true,changed:true};
    }
    function cleanHtml() {
      leaveEditing();
      return exporter.exportHtml();
    }
    function workHtml() {
      leaveEditing();
      const copy = doc.documentElement.cloneNode(true);
      copy.querySelector('#me-neutral-toolbar')?.remove();
      copy.querySelector('#me-neutral-style')?.remove();
      const workRoot = workRootSnapshot();
      const target = copy.querySelector('main');
      target.replaceWith(workRoot);
      // data-local-block remains in the editable working file so that a
      // newly inserted block can still be moved after reopening. Clean
      // export strips that marker via the source-preserving adapter.
      // A work document retains its immutable original baseline.
      return '<!doctype html>\n' + copy.outerHTML;
    }
    function download(name, contents) {
      const blob = new Blob([contents], {type:'text/html;charset=utf-8'});
      const url = URL.createObjectURL(blob);
      const a = doc.createElement('a');
      a.href = url; a.download = name;
      a.setAttribute('data-me-neutral-download', 'true');
      toolbar.append(a);
      a.click();
      a.remove();
      root.setTimeout(() => URL.revokeObjectURL(url), 2000);
      notify('Download richiesto: verifica il file e riaprilo prima dell’uso.');
    }

    elementPicker.addEventListener('change', () => {
      const nodes = selectableNodes();
      const index = Number(elementPicker.value);
      const node = Number.isInteger(index) && index >= 0 ? nodes[index] : null;
      select(node);
      if (node) {
        node.scrollIntoView({block:'center', behavior:'auto'});
        notify('Elemento selezionato. Premi Modifica testo per lavorarci.');
      }
    });
    main.addEventListener('click', event => {
      const node = event.target.closest(EDITABLE);
      if (!node || !safeNode(node)) return;
      if (event.target.closest('a')) event.preventDefault();
      select(node);
    });
    main.addEventListener('dblclick', event => {
      const node = event.target.closest(EDITABLE);
      if (safeNode(node)) { select(node); edit(); }
    });
    main.addEventListener('focusout', event => {
      if (editing && event.target === editing) {
        // A toolbar command handling a text range prevents pointerdown focus
        // loss, so a normal blur remains the transaction boundary.
        leaveEditing();
      }
    });
    toolbar.addEventListener('pointerdown', event => {
      if (event.target.closest('[data-me-action="bold"],[data-me-action="italic"]')) event.preventDefault();
    });
    toolbar.addEventListener('click', event => {
      const action = event.target.closest('[data-me-action]')?.getAttribute('data-me-action');
      if (!action) return;
      const results = {
        edit: edit, bold: () => format('bold'), italic: () => format('italic'),
        'insert-p': () => insert('p'), 'insert-h': () => insert('h3'),
        up: () => move('up'), down: () => move('down'), transfer: () => move('transfer'),
        duplicate: () => changeAddedBlock('duplicate'), delete: () => changeAddedBlock('delete'),
        undo, redo,
        clean: () => download('MetaEditor_Pagina_Pulita.html', cleanHtml()),
        work: () => download('MetaEditor_Lavoro_Modificabile.html', workHtml()),
      };
      try {
        const output = results[action]?.();
        if (output && output.ok === false) notify(output.reason);
      } catch (error) { notify('Esportazione o comando rifiutato: ' + String(error.message)); }
    });
    refreshSections();
    syncButtons();
    notify('Seleziona un testo per modificarlo. L’HTML originale rimane distinto.');
    return Object.freeze({
      status: () => Object.freeze({carrier:'static-page',regions:sectionRoots().length,dirty,
                                    canUndo:history.length>0,canRedo:future.length>0}),
      select, edit, format, insert, move, changeAddedBlock, undo, redo, cleanHtml, workHtml,
      toolbar, main
    });
  }
  root.MetaEditorNeutralStaticPage = Object.freeze({mount});
})(typeof window !== 'undefined' ? window : globalThis);
