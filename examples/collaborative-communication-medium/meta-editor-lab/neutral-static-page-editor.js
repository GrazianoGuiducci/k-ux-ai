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
      "<div class=\"me-neutral-head\"><div><strong>MetaEditor</strong><span>Pagina HTML · copia di lavoro</span></div><button id=\"me-neutral-toggle\" type=\"button\" aria-controls=\"me-neutral-body\" aria-expanded=\"true\">Riduci</button></div>" +
      "<div id=\"me-neutral-body\">" +
      "<p id=\"me-neutral-context\" aria-live=\"polite\">Seleziona un testo nella pagina o nell’elenco.</p>" +
      "<div class=\"me-neutral-group\"><label for=\"me-neutral-element\">Testo da modificare</label><select id=\"me-neutral-element\" aria-label=\"Testo da modificare\"></select>" +
      "<div class=\"me-neutral-actions\" data-me-group=\"edit\" hidden><button data-me-action=\"edit\">Modifica testo</button></div>" +
      "<div class=\"me-neutral-actions\" data-me-group=\"format\" hidden><button data-me-action=\"bold\">Grassetto</button><button data-me-action=\"italic\">Corsivo</button></div></div>" +
      "<div class=\"me-neutral-group\"><label for=\"me-neutral-section\">Sezione in cui inserire</label><select id=\"me-neutral-section\"></select>" +
      "<div class=\"me-neutral-actions\"><button data-me-action=\"insert-p\">+ Paragrafo</button><button data-me-action=\"insert-h\">+ Titolo</button></div></div>" +
      "<details class=\"me-neutral-group\" data-me-group=\"block\" hidden><summary>Gestisci blocco aggiunto</summary>" +
      "<p>Lo spostamento usa la sezione scelta sopra.</p>" +
      "<div class=\"me-neutral-actions\"><button data-me-action=\"up\">↑ Sposta</button><button data-me-action=\"down\">↓ Sposta</button><button data-me-action=\"transfer\">Sposta a sezione</button><button data-me-action=\"duplicate\">Duplica</button><button data-me-action=\"delete\">Elimina blocco</button></div></details>" +
      "<div class=\"me-neutral-group me-neutral-persistent\"><div class=\"me-neutral-actions\"><button data-me-action=\"undo\">Annulla</button><button data-me-action=\"redo\">Ripristina</button></div>" +
      "<div class=\"me-neutral-actions\"><button data-me-action=\"work\">Salva lavoro</button><button data-me-action=\"clean\">Esporta pagina pulita</button></div></div>" +
      "<p id=\"me-neutral-status\" role=\"status\" aria-live=\"polite\"></p></div>";
    const style = doc.createElement('style');
    style.id = 'me-neutral-style';
    style.textContent = [
      "#me-neutral-toolbar{position:fixed;z-index:2147483000;right:12px;top:12px;width:min(318px,calc(100vw - 24px));max-height:calc(100dvh - 24px);overflow:auto;box-sizing:border-box;background:#fff;color:#182d37;border:1px solid #a5bcb6;border-radius:10px;box-shadow:0 5px 25px #0003;font:13px/1.4 system-ui,sans-serif}",
      "#me-neutral-toolbar *{box-sizing:border-box}",
      "#me-neutral-toolbar [hidden]{display:none!important}",
      "#me-neutral-toolbar .me-neutral-head{display:flex;align-items:center;gap:9px;justify-content:space-between;padding:10px 11px;background:#f5faf8;border-radius:10px 10px 0 0}",
      "#me-neutral-toolbar strong{display:block;font-size:15px}",
      "#me-neutral-toolbar .me-neutral-head span{display:block;font-size:11px;color:#536b63}",
      "#me-neutral-body{padding:10px 11px}",
      "#me-neutral-context{background:#eff7f4;color:#174439;border-radius:5px;padding:8px;margin:0 0 8px;line-height:1.45;overflow-wrap:anywhere}",
      "#me-neutral-toolbar .me-neutral-group{border:0;border-top:1px solid #dce6e1;padding:9px 0 0;margin-top:9px}",
      "#me-neutral-toolbar label{display:block;margin-bottom:4px;font-weight:650}",
      "#me-neutral-toolbar select{width:100%;padding:6px;margin-bottom:6px;min-height:34px;background:white;color:#182d37;border:1px solid #b9c9c2;border-radius:5px}",
      "#me-neutral-toolbar .me-neutral-actions{display:grid;grid-template-columns:1fr 1fr;gap:5px;margin-top:5px}",
      "#me-neutral-toolbar .me-neutral-actions>button:only-child{grid-column:span 2}",
      "#me-neutral-toolbar button{cursor:pointer;min-height:32px;padding:7px 6px;background:#f1f7f5;border:1px solid #a7c6ba;border-radius:5px;color:#123128;font:inherit}",
      "#me-neutral-toolbar button:disabled{opacity:.48;cursor:not-allowed}",
      "#me-neutral-toolbar button:focus-visible,#me-neutral-toolbar select:focus-visible,#me-neutral-toolbar summary:focus-visible{outline:2px solid #087b70;outline-offset:2px}",
      "#me-neutral-toolbar #me-neutral-toggle{flex:none;background:#fff;padding:4px 8px;min-height:29px}",
      "#me-neutral-toolbar summary{cursor:pointer;font-weight:650;padding:2px 0;list-style:revert}",
      "#me-neutral-toolbar details>p{margin:6px 0;color:#4d645b;font-size:12px}",
      "#me-neutral-toolbar [data-me-action=\"work\"]{background:#dcefe8}",
      "#me-neutral-toolbar [data-me-action=\"delete\"]{color:#79351e}",
      "#me-neutral-status{margin:8px 0 0;font-size:12px;color:#3a5149}",
      "main [data-local-selected]{outline:2px solid #087b70;outline-offset:2px}",
      "main [data-local-editing]{outline:2px dashed #087b70;outline-offset:2px}",
      "@media(max-width:500px){#me-neutral-toolbar{top:auto;bottom:8px;max-height:42dvh}}"
    ].join('');
    doc.head.append(style);
    doc.body.append(toolbar);
    const selector = toolbar.querySelector('#me-neutral-section');
    const elementPicker = toolbar.querySelector('#me-neutral-element');
    const contextLine = toolbar.querySelector('#me-neutral-context');
    const editGroup = toolbar.querySelector('[data-me-group="edit"]');
    const formatGroup = toolbar.querySelector('[data-me-group="format"]');
    const blockGroup = toolbar.querySelector('[data-me-group="block"]');
    const toggle = toolbar.querySelector('#me-neutral-toggle');
    const body = toolbar.querySelector('#me-neutral-body');
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
      refreshElements();
      syncButtons();
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
      const active = !!(selected && selected.isConnected);
      const isEditing = !!(editing && editing.isConnected);
      const movable = active && selected.hasAttribute('data-local-block');
      editGroup.hidden = !active;
      formatGroup.hidden = !isEditing;
      blockGroup.hidden = !movable;
      for (const action of ['edit','bold','italic']) button(action).disabled = !active;
      button('bold').disabled = !isEditing;
      button('italic').disabled = !isEditing;
      button('edit').textContent = isEditing ? 'Termina modifica' : 'Modifica testo';
      for (const action of ['up','down','transfer','duplicate','delete']) button(action).disabled = !movable;
      button('undo').disabled = history.length === 0;
      button('redo').disabled = future.length === 0;
      button('insert-p').disabled = sectionRoots().length === 0;
      button('insert-h').disabled = sectionRoots().length === 0;
      const heading = active ? selected.textContent.trim().replace(/\s+/g,' ').slice(0,48) : '';
      const section = active ? sectionRoots().findIndex(item=>item.contains(selected)) : -1;
      const sectionName = section>=0 ? selector.options[section]?.textContent || '' : '';
      contextLine.textContent = isEditing ?
        'Modifica in corso: '+heading+' · termina la modifica prima di cambiare blocco.' :
        active ? (movable?'Blocco aggiunto: ':'Testo selezionato: ')+heading+
          (sectionName?' · '+sectionName:'') :
          'Seleziona un testo nella pagina o dall’elenco, oppure aggiungi un blocco.';
    }
    function edit() {
      if (!selected || !selected.isConnected) return {ok:false,reason:'select text first'};
      if (editing === selected) {
        leaveEditing();
        notify('Modifica terminata. Annulla e Ripristina rimangono disponibili.');
        return {ok:true};
      }
      leaveEditing();
      beforeTyping = snapshot();
      editing = selected;
      editing.setAttribute('contenteditable','true');
      editing.setAttribute('data-local-editing','true');
      editing.focus();
      syncButtons();
      notify('Modifica il testo e premi Termina modifica oppure esci dal campo.');
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

    toggle.addEventListener('click', () => {
      const expanded = toggle.getAttribute('aria-expanded') === 'true';
      if (expanded) leaveEditing();
      body.hidden = expanded;
      toggle.setAttribute('aria-expanded', String(!expanded));
      toggle.textContent = expanded ? 'Espandi' : 'Riduci';
    });
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
    // This is a bounded text editor, not an HTML importer. Clipboard HTML
    // is never inserted; only text/plain is accepted into the active block.
    // Each authored heading/paragraph remains one structural element.
    function hasTextSelectionInside(target) {
      const range = doc.getSelection();
      return !!(range && range.rangeCount && target &&
        target.contains(range.anchorNode) && target.contains(range.focusNode));
    }
    main.addEventListener('paste', event => {
      if (!editing || !editing.contains(event.target)) return;
      event.preventDefault();
      const raw = event.clipboardData?.getData('text/plain') || '';
      if (!raw) {
        notify('Il contenuto copiato non contiene testo semplice da incollare.');
        return;
      }
      if (raw.length > 50000) {
        notify('Testo troppo lungo per un singolo blocco (limite 50.000 caratteri).');
        return;
      }
      if (!hasTextSelectionInside(editing)) {
        notify('Posiziona il cursore nel testo prima di incollare.');
        return;
      }
      const plain = raw.replace(/\\r\\n?|\\n/g, ' ');
      // execCommand inserts text as a native editing action and preserves
      // selection/caret behavior; the source/history adapter remains owner.
      if (!doc.execCommand('insertText', false, plain)) {
        notify('Incolla non riuscito: il documento non è stato modificato.');
        return;
      }
      notify(plain !== raw ? 'Testo incollato senza formattazione; gli a capo sono stati convertiti in spazi.' :
        'Testo incollato senza formattazione esterna.');
    });
    main.addEventListener('beforeinput', event => {
      if (!editing || !editing.contains(event.target)) return;
      if (event.inputType === 'insertFromDrop' ||
          event.inputType === 'insertFromPaste' ||
          event.inputType === 'insertFromPasteAsQuotation') {
        // The paste handler above owns the text insertion; never allow
        // default rich-HTML paste or drop to bypass that route.
        event.preventDefault();
      }
    });
    main.addEventListener('dragover', event => {
      if (editing && editing.contains(event.target)) event.preventDefault();
    });
    main.addEventListener('drop', event => {
      if (!editing || !editing.contains(event.target)) return;
      event.preventDefault();
      notify('Il trascinamento nel testo non è supportato. Usa Incolla come testo.');
    });
    main.addEventListener('keydown', event => {
      if (event.key === 'Enter' && editing && editing.contains(event.target) &&
          editing.matches('h1,h2,h3,h4,h5,h6,p,blockquote,figcaption,li')) {
        // Keep the source document's block structure intact. Add separate
        // paragraphs/headings through explicit composition commands.
        event.preventDefault();
        notify('Per un nuovo blocco usa + Paragrafo o + Titolo.');
        return;
      }
      if (event.key === 'Escape' && editing && editing.contains(event.target)) {
        event.preventDefault();
        leaveEditing();
        button('edit').focus();
        notify('Modifica terminata. Le modifiche sono disponibili in Annulla.');
      }
    });
    toolbar.addEventListener('pointerdown', event => {
      const formatControl = event.target.closest('[data-me-action="bold"],[data-me-action="italic"]');
      const finishingEdit = editing && event.target.closest('[data-me-action="edit"]');
      if (formatControl || finishingEdit) event.preventDefault();
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
    notify('Le modifiche rimangono nel file di lavoro finché non scegli Salva lavoro.');
    return Object.freeze({
      status: () => Object.freeze({carrier:'static-page',regions:sectionRoots().length,dirty,
                                    canUndo:history.length>0,canRedo:future.length>0}),
      select, edit, format, insert, move, changeAddedBlock, undo, redo, cleanHtml, workHtml,
      toolbar, main
    });
  }
  root.MetaEditorNeutralStaticPage = Object.freeze({mount});
})(typeof window !== 'undefined' ? window : globalThis);
