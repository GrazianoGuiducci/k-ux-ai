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
  const SELECTABLE = EDITABLE + ',a,figure[data-local-block]';
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
    // Authored non-editable/inert islands are outside every editing action,
    // including selection, precise placement and work-history transfers.
    const protectedIsland = node => !!node?.closest(
      '[contenteditable="false"],[inert],form,nav,aside,script,style,template,dialog'
    );
    const safeNode = node => node && main.contains(node) && node.matches(SELECTABLE) &&
      !protectedIsland(node);
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
      "<div class=\"me-neutral-actions\"><button data-me-action=\"insert-p\">+ Paragrafo</button><button data-me-action=\"insert-h\">+ Titolo</button></div>" +
      "<details id=\"me-neutral-position-group\"><summary>Posizionamento preciso (opzionale)</summary>" +
      "<label for=\"me-neutral-anchor\">Vicino a quale elemento?</label><select id=\"me-neutral-anchor\" aria-label=\"Riferimento per inserimento\"></select>" +
      "<label for=\"me-neutral-placement\">Posizione</label><select id=\"me-neutral-placement\" aria-label=\"Posizione rispetto al riferimento\"><option value=\"after\">Dopo</option><option value=\"before\">Prima</option></select>" +
      "<p>Se la sezione ha più gruppi, scegli il testo della scheda desiderata.</p></details></div>" +
      "<details class=\"me-neutral-group\" id=\"me-neutral-sections\"><summary>Componi la pagina</summary><label for=\"me-neutral-section-template\">Modello di sezione</label><select id=\"me-neutral-section-template\"><option value=\"text\">Titolo e testo</option><option value=\"columns\">Due colonne adattive</option><option value=\"callout\">Riquadro in evidenza</option></select><button type=\"button\" data-me-action=\"section-add\">+ Sezione dopo quella scelta</button><div class=\"me-neutral-actions\" id=\"me-neutral-section-management\" hidden><button type=\"button\" data-me-action=\"section-up\">↑ Sezione</button><button type=\"button\" data-me-action=\"section-down\">↓ Sezione</button><button type=\"button\" data-me-action=\"section-copy\">Duplica sezione</button><button type=\"button\" data-me-action=\"section-delete\">Elimina sezione</button></div><div class=\"me-neutral-actions\"><button type=\"button\" data-me-action=\"section-export\" disabled>Salva modello di sezione</button></div><label for=\"me-neutral-section-import\">Riusa un modello salvato</label><input type=\"file\" id=\"me-neutral-section-import\" accept=\".json,application/json\"></details>" +
      "<details class=\"me-neutral-group\" id=\"me-neutral-appearance\" hidden><summary>Stile e dimensioni</summary><label for=\"me-neutral-font-size\">Dimensione testo (px)</label><input id=\"me-neutral-font-size\" type=\"number\" min=\"10\" max=\"96\" step=\"1\"><label for=\"me-neutral-color\">Colore testo</label><input id=\"me-neutral-color\" type=\"color\"><label for=\"me-neutral-background\">Sfondo</label><input id=\"me-neutral-background\" type=\"color\"><label for=\"me-neutral-align\">Allineamento</label><select id=\"me-neutral-align\"><option value=\"start\">Inizio</option><option value=\"center\">Centro</option><option value=\"end\">Fine</option><option value=\"justify\">Giustificato</option></select><label for=\"me-neutral-width\">Larghezza massima</label><select id=\"me-neutral-width\"><option value=\"\">Automatica / originale</option><option value=\"100%\">100%</option><option value=\"75%\">75%</option><option value=\"50%\">50%</option></select></details>" +
      "<details class=\"me-neutral-group\" id=\"me-neutral-link-group\"><summary>Aggiungi o modifica collegamento</summary>" +
      "<label for=\"me-neutral-link-text\">Testo del collegamento</label><input id=\"me-neutral-link-text\" type=\"text\" maxlength=\"200\" placeholder=\"Testo del link\">" +
      "<label for=\"me-neutral-link-url\">Indirizzo (https, email o #sezione)</label><input id=\"me-neutral-link-url\" type=\"text\" placeholder=\"https://esempio.it\" spellcheck=\"false\">" +
      "<button data-me-action=\"link\" type=\"button\">Inserisci collegamento</button></details>" +
      "<details class=\"me-neutral-group\" id=\"me-neutral-image-group\"><summary>Inserisci immagine dal computer</summary>" +
      "<label for=\"me-neutral-image-alt\">Descrizione dell’immagine</label><input id=\"me-neutral-image-alt\" type=\"text\" maxlength=\"160\" placeholder=\"Che cosa rappresenta?\">" +
      "<label for=\"me-neutral-image-file\">File PNG, JPEG, WebP o GIF (max 1,5 MB)</label><input id=\"me-neutral-image-file\" type=\"file\" accept=\"image/png,image/jpeg,image/webp,image/gif\">" +
      "<button data-me-action=\"image-alt\" type=\"button\" hidden>Aggiorna descrizione immagine</button></details>" +
      "<details class=\"me-neutral-group\" data-me-group=\"block\" hidden><summary>Gestisci blocco aggiunto</summary>" +
      "<p>Lo spostamento usa la sezione scelta sopra.</p>" +
      "<div class=\"me-neutral-actions\"><button data-me-action=\"up\">↑ Sposta</button><button data-me-action=\"down\">↓ Sposta</button><button data-me-action=\"transfer\">Sposta a sezione</button><button data-me-action=\"duplicate\">Duplica</button><button data-me-action=\"delete\">Elimina blocco</button></div></details>" +
      "<div class=\"me-neutral-group me-neutral-persistent\"><div class=\"me-neutral-actions\"><button data-me-action=\"undo\">Annulla</button><button data-me-action=\"redo\">Ripristina</button></div>" +
      "<div class=\"me-neutral-actions\"><button data-me-action=\"work\">Salva lavoro</button><button data-me-action=\"clean\">Esporta pagina pulita</button></div></div>" +
      "<p id=\"me-neutral-status\" role=\"status\" aria-live=\"polite\"></p>" +
      "<p id=\"me-neutral-save-state\" aria-live=\"polite\">Nessuna modifica da salvare · Ctrl+S per Salvare lavoro</p></div>";
    // One runtime-only entry to native commands, outside the editable source.
    const contextual = doc.createElement('div');
    contextual.id = 'me-neutral-context-actions';
    contextual.hidden = true;
    contextual.setAttribute('role','group');
    contextual.setAttribute('aria-label','Azioni sull’elemento selezionato');
    for (const [action,label] of [['edit','Modifica testo'],['insert-p','+ Paragrafo'],['insert-h','+ Titolo'],['duplicate','Duplica']]) {
      const control = doc.createElement('button');
      control.type='button';
      control.dataset.meContextAction=action;
      control.textContent=label;
      contextual.append(control);
    }
    const style = doc.createElement('style');
    style.id = 'me-neutral-style';
    style.textContent = [
      "#me-neutral-toolbar{position:fixed;z-index:2147483000;right:12px;top:12px;width:min(318px,calc(100vw - 24px));max-height:min(60dvh,calc(100dvh - 24px));overflow:auto;box-sizing:border-box;background:#fff;color:#182d37;border:1px solid #a5bcb6;border-radius:10px;box-shadow:0 5px 25px #0003;font:13px/1.4 system-ui,sans-serif}",
      "#me-neutral-toolbar *{box-sizing:border-box}",
      "#me-neutral-toolbar [hidden]{display:none!important}",
      "#me-neutral-toolbar .me-neutral-head{display:flex;align-items:center;gap:9px;justify-content:space-between;padding:10px 11px;background:#f5faf8;border-radius:10px 10px 0 0;position:sticky;top:0;z-index:2}",
      "#me-neutral-toolbar strong{display:block;font-size:15px}",
      "#me-neutral-toolbar .me-neutral-head span{display:block;font-size:11px;color:#536b63}",
      "#me-neutral-body{padding:10px 11px}",
      "#me-neutral-context{background:#eff7f4;color:#174439;border-radius:5px;padding:8px;margin:0 0 8px;line-height:1.45;overflow-wrap:anywhere}",
      "#me-neutral-toolbar .me-neutral-group{border:0;border-top:1px solid #dce6e1;padding:9px 0 0;margin-top:9px}",
      "#me-neutral-toolbar label{display:block;margin-bottom:4px;font-weight:650}",
      "#me-neutral-toolbar select,#me-neutral-toolbar input{width:100%;padding:6px;margin-bottom:6px;min-height:34px;background:white;color:#182d37;border:1px solid #b9c9c2;border-radius:5px;font:inherit}",
      "#me-neutral-toolbar input[type=file]{font-size:12px;max-width:100%}",
      "#me-neutral-toolbar input[type=color]{height:34px;padding:3px;cursor:pointer}",
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
      "#me-neutral-save-state{margin:8px 0 0;font-size:11px;color:#49645b}",
      "#me-neutral-context-actions{position:fixed;z-index:2147482999;display:flex;align-items:center;gap:4px;flex-wrap:wrap;max-width:calc(100vw - 16px);padding:5px;background:#fff;border:1px solid #a5bcb6;border-radius:8px;box-shadow:0 4px 18px #0003;font:13px/1.3 system-ui,sans-serif}",
      "#me-neutral-context-actions[hidden],#me-neutral-context-actions button[hidden]{display:none!important}",
      "#me-neutral-context-actions button{font:inherit;color:#123128;background:#f1f7f5;border:1px solid #a7c6ba;border-radius:5px;min-height:32px;padding:5px 7px;cursor:pointer;white-space:nowrap}",
      "#me-neutral-context-actions button:focus-visible{outline:2px solid #087b70;outline-offset:2px}",
      "main [data-local-selected]{outline:2px solid #087b70;outline-offset:2px}",
      "main [data-local-editing]{outline:2px dashed #087b70;outline-offset:2px}",
      "@media(max-width:500px){#me-neutral-toolbar{top:auto;bottom:8px;max-height:42dvh}}"
    ].join('');
    doc.head.append(style);
    doc.body.append(toolbar,contextual);
    const contextButton = action => contextual.querySelector('[data-me-context-action="'+action+'"]');
    let contextFrame = 0;
    function scheduleContextual() {
      if (contextFrame) return;
      contextFrame = doc.defaultView.requestAnimationFrame(() => {
        contextFrame=0;
        positionContextual();
      });
    }
    function positionContextual() {
      if (!safeNode(selected) || !selected.isConnected || editing) {
        contextual.hidden=true; return;
      }
      const section=sectionRoots().find(s=>s.contains(selected));
      const anchor=flowChild(selected,section || main) && !!section;
      contextButton('edit').hidden=!selected.matches(EDITABLE);
      contextButton('insert-p').hidden=!anchor;
      contextButton('insert-h').hidden=!anchor;
      contextButton('duplicate').hidden=!selected.hasAttribute('data-local-block');
      if ([...contextual.children].every(b=>b.hidden)) {contextual.hidden=true;return;}
      const r=selected.getBoundingClientRect(), panel=toolbar.getBoundingClientRect();
      const view=doc.defaultView, vw=view.innerWidth, vh=view.innerHeight;
      if (r.bottom<8 || r.top>vh-8 || r.right<8 || r.left>vw-8 || !r.width || !r.height) {
        contextual.hidden=true;return;
      }
      contextual.hidden=false;
      const size=contextual.getBoundingClientRect(), w=size.width,h=size.height,gap=7;
      const clamp=(x,min,max)=>Math.min(Math.max(x,min),max);
      const x=clamp(r.left,8,Math.max(8,vw-w-8));
      const positions=[
        [x,r.top-h-gap],[x,r.bottom+gap],
        [r.right+gap,clamp(r.top,8,Math.max(8,vh-h-8))],
        [r.left-w-gap,clamp(r.top,8,Math.max(8,vh-h-8))]
      ];
      const overlaps=(px,py,q)=>px<q.right&&px+w>q.left&&py<q.bottom&&py+h>q.top;
      const place=positions.find(([px,py])=>px>=8&&py>=8&&px+w<=vw-8&&py+h<=vh-8&&!overlaps(px,py,panel)&&!overlaps(px,py,r));
      if (!place) {contextual.hidden=true;return;}
      contextual.style.left=Math.round(place[0])+'px';
      contextual.style.top=Math.round(place[1])+'px';
    }
    contextual.addEventListener('pointerdown',event=>event.preventDefault());
    contextual.addEventListener('click',event=>{
      const control=event.target.closest('[data-me-context-action]');
      if (!control || control.hidden || contextual.hidden || !safeNode(selected) || editing) return;
      const action=control.dataset.meContextAction;
      let result;
      if (action==='edit') result=edit();
      else if (action==='duplicate') result=changeAddedBlock('duplicate');
      else if (action==='insert-p'||action==='insert-h') {
        const section=sectionRoots().findIndex(s=>s.contains(selected));
        if (section<0 || !flowChild(selected,sectionRoots()[section])) return;
        // This gesture explicitly names the current visual anchor; do not
        // inherit a different destination from the advanced placement picker.
        selector.value=String(section);
        explicitAnchorNode=selected;
        placementPicker.value='after';
        refreshAnchors();
        result=insert(action==='insert-p'?'p':'h3');
      }
      if (result?.ok===false) notify(result.reason);
      scheduleContextual();
    });
    doc.defaultView.addEventListener('scroll',scheduleContextual,true);
    doc.defaultView.addEventListener('resize',scheduleContextual);
    if (doc.defaultView.ResizeObserver) new doc.defaultView.ResizeObserver(scheduleContextual).observe(toolbar);
    const selector = toolbar.querySelector('#me-neutral-section');
    const anchorPicker = toolbar.querySelector('#me-neutral-anchor');
    const placementPicker = toolbar.querySelector('#me-neutral-placement');
    const elementPicker = toolbar.querySelector('#me-neutral-element');
    const linkGroup = toolbar.querySelector('#me-neutral-link-group');
    const linkTextInput = toolbar.querySelector('#me-neutral-link-text');
    const linkUrlInput = toolbar.querySelector('#me-neutral-link-url');
    const linkButton = toolbar.querySelector('[data-me-action="link"]');
    const imageFileInput = toolbar.querySelector('#me-neutral-image-file');
    const imageAltInput = toolbar.querySelector('#me-neutral-image-alt');
    const imageAltButton = toolbar.querySelector('[data-me-action="image-alt"]');
    const imageGroup = toolbar.querySelector('#me-neutral-image-group');
    const contextLine = toolbar.querySelector('#me-neutral-context');
    const editGroup = toolbar.querySelector('[data-me-group="edit"]');
    const formatGroup = toolbar.querySelector('[data-me-group="format"]');
    const blockGroup = toolbar.querySelector('[data-me-group="block"]');
    const toggle = toolbar.querySelector('#me-neutral-toggle');
    const body = toolbar.querySelector('#me-neutral-body');
    const status = toolbar.querySelector('#me-neutral-status');
    const saveState = toolbar.querySelector('#me-neutral-save-state');
    const button = action => toolbar.querySelector('[data-me-action="' + action + '"]');
    const pristineSource = sourceHtml;
    const sectionTemplate=toolbar.querySelector('#me-neutral-section-template');
    const sectionManagement=toolbar.querySelector('#me-neutral-section-management');
    const sectionImport=toolbar.querySelector('#me-neutral-section-import');
    const appearance=toolbar.querySelector('#me-neutral-appearance');
    const appearanceFields={
      fontSize:toolbar.querySelector('#me-neutral-font-size'),
      color:toolbar.querySelector('#me-neutral-color'),
      backgroundColor:toolbar.querySelector('#me-neutral-background'),
      textAlign:toolbar.querySelector('#me-neutral-align'),
      maxWidth:toolbar.querySelector('#me-neutral-width')
    };

    // Work/history objects require stable identity independent of their
    // visible text and markup. Two identical paragraphs exchanged in the
    // DOM must still be a real ordering change to the editing history.
    // This identity is editor-private and stripped from clean/public HTML.
    let blockSequence = 0;
    function assignBlockIdentity(node) {
      const occupied = new Set([...main.querySelectorAll('[data-local-block-id]')]
        .filter(other => other !== node)
        .map(other => other.getAttribute('data-local-block-id')));
      let id;
      do { id = 'b' + (++blockSequence).toString(36); } while (occupied.has(id));
      node.setAttribute('data-local-block-id',id);
      return id;
    }
    const observedIdentities = new Set();
    for (const node of main.querySelectorAll('[data-local-block]')) {
      let id = node.getAttribute('data-local-block-id');
      if (!id || observedIdentities.has(id)) id = assignBlockIdentity(node);
      observedIdentities.add(id);
    }

    function workRootSnapshot() {
      const clone = main.cloneNode(true);
      for (const element of [clone, ...clone.querySelectorAll('*')]) {
        // Respect authored contenteditable="false" islands in the saved
        // working document; only active editing state is transient.
        if ((element.getAttribute('contenteditable') || '').toLowerCase() !== 'false')
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
    // A reopened work document is already the baseline for this session.
    // Pending edits are a document difference, not a count of history steps.
    const openedSnapshot = snapshot();
    function pendingWork() { return snapshot() !== openedSnapshot; }
    function setSaveState(pending) {
      if (dirty===pending&&saveState.dataset.pending===String(pending)) return;
      saveState.textContent = pending ?
        'Modifiche da conservare · Ctrl+S richiede il download del lavoro' :
        'Nessuna modifica da conservare · Ctrl+S salva il lavoro';
      saveState.dataset.pending=String(pending);
      dirty=pending;
    }
    function refreshSaveState() {setSaveState(pendingWork());}
    function notify(message) { status.textContent = message; }
    const selectableNodes = () => [...main.querySelectorAll(SELECTABLE)].filter(safeNode);
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
    // Exact DOM nodes are chosen only from the selected semantic section,
    // never from a global query or from a visual CSS class assumption.
    function anchorCandidates(section) {
      return section ? [...section.querySelectorAll('h1,h2,h3,h4,h5,h6,p,blockquote')]
        .filter(node => flowChild(node, section)) : [];
    }
    let explicitAnchorNode = null;
    function refreshAnchors() {
      const section = sectionRoots()[Number(selector.value)];
      const candidates = anchorCandidates(section);
      // Preserve identity, not an array index: adding a block before an
      // anchor must not silently redirect the next operation elsewhere.
      if (explicitAnchorNode && !candidates.includes(explicitAnchorNode))
        explicitAnchorNode = null;
      anchorPicker.replaceChildren();
      const automatic = doc.createElement('option');
      automatic.value = '';
      automatic.textContent = 'Automatico, se non ambiguo';
      anchorPicker.append(automatic);
      candidates.forEach((node, index) => {
        const option = doc.createElement('option');
        option.value = String(index);
        const preview = node.textContent.trim().replace(/\s+/g,' ').slice(0,55);
        option.textContent = (index+1)+'. '+node.localName.toUpperCase()+' · '+(preview||'Senza testo');
        anchorPicker.append(option);
      });
      const current = explicitAnchorNode ? candidates.indexOf(explicitAnchorNode) : -1;
      anchorPicker.value = current >= 0 ? String(current) : '';
      return candidates;
    }
    function chosenAnchor(section) {
      return explicitAnchorNode && flowChild(explicitAnchorNode, section) ?
        explicitAnchorNode : null;
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
      refreshAnchors();
      return sections;
    }
    function record(before) {
      if (before == null) return false;
      const after = snapshot();
      if (after === before) return false;
      history.push(before);
      if (history.length > 80) history.shift();
      future = [];
      refreshSaveState();
      syncButtons();
      return true;
    }
    function leaveEditing() {
      if (!editing) return;
      const current = editing, previous = beforeTyping;
      editing = null; beforeTyping = null;
      current.removeAttribute('contenteditable');
      current.removeAttribute('data-local-editing');
      if (!record(previous)) refreshSaveState();
      refreshElements();
      syncButtons();
    }
    function select(element) {
      if (editing && editing !== element) leaveEditing();
      if (selected && selected.isConnected) selected.removeAttribute('data-local-selected');
      selected = safeNode(element) ? element : null;
      if (selected) {
        selected.setAttribute('data-local-selected','true');
        if (selected.matches('a')) {
          linkTextInput.value = selected.textContent;
          linkUrlInput.value = selected.getAttribute('href') || '';
          linkGroup.open = true;
        }
        if (selected.matches('figure[data-local-block]')) {
          imageAltInput.value = selected.querySelector('img')?.alt || '';
          imageGroup.open = true;
        }
        const section = sectionRoots().findIndex(section => section.contains(selected));
        if (section >= 0 && selector.value !== String(section)) {
          selector.value = String(section);
          // Programmatic selection changes the semantic destination too;
          // keep its reference list tied to that section, not the old one.
          explicitAnchorNode = null;
          refreshAnchors();
        }
      }
      refreshElements();
      syncButtons();
      return !!selected;
    }
    function syncButtons() {
      const active = !!(selected && selected.isConnected);
      const textSelected = active && selected.matches(EDITABLE);
      const isEditing = !!(editing && editing.isConnected);
      const movable = active && selected.hasAttribute('data-local-block');
      editGroup.hidden = !textSelected;
      formatGroup.hidden = !isEditing;
      blockGroup.hidden = !movable;
      for (const action of ['edit','bold','italic']) button(action).disabled = !textSelected;
      button('bold').disabled = !isEditing;
      button('italic').disabled = !isEditing;
      button('edit').textContent = isEditing ? 'Termina modifica' : 'Modifica testo';
      for (const action of ['transfer','duplicate','delete']) button(action).disabled = !movable;
      // Quick arrows reorder only adjacent editor-owned blocks. Passing an
      // authored media, link, figure or protected widget needs an explicit
      // destination reference instead of silently crossing its boundary.
      button('up').disabled = !movable ||
        !selected.previousElementSibling?.hasAttribute('data-local-block');
      button('down').disabled = !movable ||
        !selected.nextElementSibling?.hasAttribute('data-local-block');
      button('undo').disabled = history.length === 0;
      button('redo').disabled = future.length === 0;
      button('insert-p').disabled = sectionRoots().length === 0;
      button('insert-h').disabled = sectionRoots().length === 0;
      const heading = active ? (selected.matches('figure') ?
        selected.querySelector('img')?.alt || 'Immagine' :
        selected.textContent.trim().replace(/\s+/g,' ').slice(0,48)) : '';
      const section = active ? sectionRoots().findIndex(item=>item.contains(selected)) : -1;
      const sectionName = section>=0 ? selector.options[section]?.textContent || '' : '';
      linkButton.textContent = active && selected.matches('a') ?
        'Aggiorna collegamento' : 'Inserisci collegamento';
      imageAltButton.hidden = !(active && selected.matches('figure[data-local-block]'));
      contextLine.textContent = isEditing ?
        'Modifica in corso: '+heading+' · termina la modifica prima di cambiare blocco.' :
        active ? (movable?'Blocco aggiunto: ':'Testo selezionato: ')+heading+
          (sectionName?' · '+sectionName:'') :
          'Seleziona un testo nella pagina o dall’elenco, oppure aggiungi un blocco.';
      if (!active || isEditing) contextual.hidden=true;
      syncCompositionControls();
      scheduleContextual();
    }
    function edit() {
      if (!selected || !selected.isConnected || !selected.matches(EDITABLE))
        return {ok:false,reason:'select a text block first'};
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
    // Bridge11's revealSelection principle, adapted to the actual neutral
    // toolbar and DOM viewport. Keep the current caret, selection and history.
    function revealSelection(node) {
      if (!safeNode(node) || !node.isConnected) return false;
      const view = doc.defaultView;
      const rect = node.getBoundingClientRect();
      if (!rect.width || !rect.height) return false;
      let top = 12, bottom = view.innerHeight - 12;
      const panel = toolbar.getBoundingClientRect();
      const overlapsHorizontally = panel.left < rect.right && panel.right > rect.left;
      if (overlapsHorizontally && panel.width && panel.height) {
        // Neutral toolbar is top/right on desktop and bottom-docked on mobile.
        if (panel.top <= 28) top = Math.max(top, panel.bottom + 12);
        else if (panel.bottom >= view.innerHeight - 28) bottom = Math.min(bottom, panel.top - 12);
      }
      // Do not move the page to an impossible or even less useful position.
      const available = bottom - top;
      if (available < 72) return false;
      if (rect.top >= top && rect.bottom <= bottom) return true;
      const destination = rect.height > available ? top : top + (available - rect.height) / 2;
      const delta = rect.top - destination;
      if (Math.abs(delta) > 3) view.scrollBy({top:Math.round(delta),behavior:'instant'});
      return true;
    }
    function transact(effect, reveal=false) {
      leaveEditing();
      const before = snapshot();
      const output = effect();
      const changed = record(before);
      refreshSections();
      syncButtons();
      if (changed && reveal) revealSelection(selected);
      return {ok:true,changed,...(output || {})};
    }
    // Bridge11's section and appearance capacities are adapted to the
    // neutral DOM owner. Use semantic elements and responsive flow, not MAIOS
    // classes, absolute coordinates, a second history or editable HTML input.
    const sectionAt=()=>sectionRoots()[Number(selector.value)] || null;
    const ownedSection=node=>!!(node && sectionRoots().includes(node) && node.hasAttribute('data-local-section') && !protectedIsland(node));
    function safeSectionNeighbor(section,direction) {
      const node=direction<0?section?.previousElementSibling:section?.nextElementSibling;
      return node && sectionRoots().includes(node) && !protectedIsland(node) ? node : null;
    }
    function colorValue(value,fallback) {
      const m=String(value).match(/^rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$/);
      return m?'#'+m.slice(1).map(n=>Number(n).toString(16).padStart(2,'0')).join(''):fallback;
    }
    function syncCompositionControls() {
      const section=sectionAt(), own=ownedSection(section);
      sectionManagement.hidden=!own;
      button('section-export').disabled=!own;
      button('section-up').disabled=!own||!safeSectionNeighbor(section,-1);
      button('section-down').disabled=!own||!safeSectionNeighbor(section,1);
      const active=safeNode(selected) && selected.isConnected && !editing &&
        !selected.querySelector('[inert],[contenteditable="false"],form,nav,aside');
      appearance.hidden=!active;
      if (!active) return;
      const style=doc.defaultView.getComputedStyle(selected);
      appearanceFields.fontSize.value=String(Math.round(parseFloat(style.fontSize)||16));
      appearanceFields.color.value=colorValue(style.color,'#183146');
      appearanceFields.backgroundColor.value=colorValue(style.backgroundColor,'#ffffff');
      appearanceFields.textAlign.value=({left:'start',right:'end'})[style.textAlign]||style.textAlign;
      appearanceFields.maxWidth.value=['100%','75%','50%'].includes(selected.style.maxWidth)?selected.style.maxWidth:'';
    }
    function changeAppearance(property,value) {
      if (!safeNode(selected)||editing||selected.querySelector('[inert],[contenteditable="false"],form,nav,aside'))
        return {ok:false,reason:'Seleziona un elemento modificabile.'};
      let next;
      if (property==='fontSize' && /^\d{1,2}$/.test(value) && Number(value)>=10 && Number(value)<=96) next=value+'px';
      else if (['color','backgroundColor'].includes(property) && /^#[0-9a-f]{6}$/i.test(value)) next=value;
      else if (property==='textAlign' && ['start','center','end','justify'].includes(value)) next=value;
      else if (property==='maxWidth' && ['','100%','75%','50%'].includes(value)) next=value;
      else return {ok:false,reason:'Valore di stile non supportato.'};
      const target=selected;
      return transact(()=>{
        target.style[property]=next;
        if (!target.style.length) target.removeAttribute('style');
        notify('Aspetto aggiornato · Annulla per ripristinare.');
      });
    }
    function createSection(kind) {
      if (!['text','columns','callout'].includes(kind)) return {ok:false,reason:'Modello non disponibile.'};
      const reference=sectionAt();
      // A document without sections can still start from a semantic section.
      // Do not move authored nodes or cross a protected insertion boundary.
      if (reference && protectedIsland(reference)) return {ok:false,reason:'Sezione protetta.'};
      return transact(()=>{
        const section=doc.createElement('section');
        section.dataset.localSection=kind;
        section.style.cssText='padding:clamp(20px,4vw,56px) 4%;';
        const shell=doc.createElement('div');
        shell.style.cssText='max-width:1080px;margin-inline:auto;';
        section.append(shell);
        const heading=doc.createElement('h2');
        heading.textContent=kind==='columns'?'Due colonne':kind==='callout'?'In evidenza':'Nuova sezione';
        shell.append(heading);
        const paragraph=parent=>{
          const p=doc.createElement('p');
          p.textContent='Scrivi qui il contenuto.';
          parent.append(p);
        };
        if (kind==='columns') {
          const flow=doc.createElement('div');
          flow.style.cssText='display:flex;flex-wrap:wrap;gap:24px;align-items:flex-start;';
          for (const name of ['Prima colonna','Seconda colonna']) {
            const cell=doc.createElement('div');
            cell.style.cssText='flex:1 1 220px;min-width:0;';
            const title=doc.createElement('h3');title.textContent=name;
            cell.append(title);paragraph(cell);flow.append(cell);
          }
          shell.append(flow);
        } else {
          if (kind==='callout') shell.style.cssText+='padding:24px;border:1px solid #c7d7dc;border-radius:12px;background:#f4faf8;color:#183146;';
          paragraph(shell);
        }
        if (reference) reference.after(section); else main.append(section);
        refreshSections();
        select(heading);
        notify('Sezione aggiunta · modifica il testo direttamente.');
      },true);
    }
    function changeSection(action) {
      const section=sectionAt();
      if (!ownedSection(section)) return {ok:false,reason:'Gestione strutturale disponibile per le sezioni aggiunte.'};
      if (action==='up'||action==='down') {
        const neighbor=safeSectionNeighbor(section,action==='up'?-1:1);
        if (!neighbor) return {ok:true,changed:false};
        return transact(()=>{
          if (action==='up') neighbor.before(section);else neighbor.after(section);
          refreshSections();
          selector.value=String(sectionRoots().indexOf(section));explicitAnchorNode=null;refreshAnchors();
          select(section.querySelector('h2,h3,p')); 
        },true);
      }
      if (action==='copy') {
        if (section.id||section.querySelector('[id],[inert],[contenteditable="false"]'))
          return {ok:false,reason:'La sezione contiene riferimenti o elementi protetti.'};
        return transact(()=>{
          const copy=section.cloneNode(true);
          for (const item of copy.querySelectorAll('[data-local-block]')) assignBlockIdentity(item);
          for (const item of copy.querySelectorAll('[data-local-selected],[data-local-editing]')) {
            item.removeAttribute('data-local-selected');item.removeAttribute('data-local-editing');
          }
          section.after(copy);refreshSections();
          select(copy.querySelector('h2,h3,p'));
        },true);
      }
      if (action==='delete') return transact(()=>{
        section.remove();select(null);explicitAnchorNode=null;
        notify('Sezione eliminata · Annulla per recuperarla.');
      });
      return {ok:false,reason:'Azione non supportata.'};
    }
    // Native scene template portability inspires a page-specific, structured
    // section file. No HTML parsing, external stylesheet or executable content.
    // Export and import use the same bounded representation.
    const sectionSchema='metaeditor.section.v1';
    const sectionTags=new Set(['section','div','h2','h3','h4','h5','h6','p','strong','em','b','i','u','s','span','br','ul','ol','li','blockquote','a']);
    const sectionStyles=new Set(['padding','padding-top','padding-right','padding-bottom','padding-left','max-width','min-width','margin-inline','margin-inline-start','margin-inline-end','display','flex-wrap','gap','row-gap','column-gap','align-items','flex','flex-grow','flex-shrink','flex-basis','border','border-width','border-style','border-color','border-top-width','border-right-width','border-bottom-width','border-left-width','border-top-style','border-right-style','border-bottom-style','border-left-style','border-top-color','border-right-color','border-bottom-color','border-left-color','border-radius','border-top-left-radius','border-top-right-radius','border-bottom-left-radius','border-bottom-right-radius','background-color','color','font-size','text-align','font-weight','font-style','text-decoration','text-decoration-line','text-decoration-style','text-decoration-color','text-decoration-thickness']);
    const sectionKinds=new Set(['text','columns','callout']);
    function sectionStyleValue(property,value) {
      if (!sectionStyles.has(property)||typeof value!=='string'||value.length>180||
          !/^[#a-zA-Z0-9.,()%+ \-]+$/.test(value)||
          /url|image|var\(|attr\(|expression|javascript/i.test(value)) return false;
      // Only CSS values for this exact property, never arbitrary declarations.
      if (property==='display' && !['flex','block','inline','inline-block'].includes(value)) return false;
      return doc.defaultView.CSS.supports(property,value);
    }
    function sectionTemplateLink(value) {
      if (typeof value!=='string'||value.startsWith('#')) return null;
      return normalizedLink(value);
    }
    function sectionBudget() {return {nodes:0,text:0};}
    function checkSectionBudget(budget,depth) {
      if (++budget.nodes>500||depth>18||budget.text>80000) throw Error('Modello troppo complesso.');
    }
    function packSectionNode(node,budget,depth=0) {
      checkSectionBudget(budget,depth);
      if (node.nodeType===3) {
        budget.text+=node.data.length;
        if (budget.text>80000) throw Error('Testo del modello troppo lungo.');
        return node.data;
      }
      if (node.nodeType!==1||!sectionTags.has(node.localName)||(depth===0)!==(node.localName==='section'))
        throw Error('Il modello contiene elementi non ancora trasferibili, per esempio immagini.');
      const out={tag:node.localName,children:[]};
      for (const attr of node.getAttributeNames()) {
        if (['style','data-local-selected','data-local-editing','data-local-block-id','data-local-block','data-local-section'].includes(attr)) continue;
        if (attr==='href'&&node.localName==='a') {
          const href=sectionTemplateLink(node.getAttribute(attr));
          if (!href) throw Error('Il collegamento dipende dalla pagina originale.');
          out.href=href;continue;
        }
        throw Error('Il modello contiene attributi o riferimenti dipendenti dalla pagina.');
      }
      if (node.hasAttribute('data-local-block')) out.block=true;
      if (node.style.length) {
        out.style={};
        for (const property of node.style) {
          const value=node.style.getPropertyValue(property);
          if (node.style.getPropertyPriority(property)||!sectionStyleValue(property,value))
            throw Error('Stile non trasferibile: '+property);
          out.style[property]=value;
        }
      }
      out.children=[...node.childNodes].map(child=>packSectionNode(child,budget,depth+1));
      return out;
    }
    function unpackSectionNode(value,budget,depth=0) {
      checkSectionBudget(budget,depth);
      if (typeof value==='string') {
        budget.text+=value.length;
        if (budget.text>80000) throw Error('Testo del modello troppo lungo.');
        return doc.createTextNode(value);
      }
      if (!value||typeof value!=='object'||Array.isArray(value)||
          Object.keys(value).some(key=>!['tag','children','style','block','href'].includes(key))||
          !sectionTags.has(value.tag)||(depth===0)!==(value.tag==='section')||
          !Array.isArray(value.children)) throw Error('Struttura di modello non supportata.');
      const node=doc.createElement(value.tag);
      if (value.href!==undefined) {
        const href=sectionTemplateLink(value.href);
        if (value.tag!=='a'||!href) throw Error('Collegamento non trasferibile.');
        node.setAttribute('href',href);
      } else if (value.tag==='a') throw Error('Collegamento senza destinazione.');
      if (value.style!==undefined) {
        if (!value.style||typeof value.style!=='object'||Array.isArray(value.style)) throw Error('Stile non valido.');
        for (const [property,val] of Object.entries(value.style)) {
          if (!sectionStyleValue(property,val)) throw Error('Stile non trasferibile.');
          node.style.setProperty(property,val);
        }
      }
      if (value.block!==undefined) {
        if (value.block!==true||!['p','h2','h3','h4','h5','h6','blockquote'].includes(value.tag))
          throw Error('Tipo di blocco non valido.');
        node.setAttribute('data-local-block','true');
      }
      for (const child of value.children) node.append(unpackSectionNode(child,budget,depth+1));
      return node;
    }
    function exportSectionTemplate() {
      leaveEditing();
      const section=sectionAt();
      if (!ownedSection(section)||!sectionKinds.has(section.dataset.localSection))
        return {ok:false,reason:'Seleziona una sezione creata con MetaEditor.'};
      const pack={schema:sectionSchema,kind:section.dataset.localSection,tree:packSectionNode(section,sectionBudget())};
      const raw=JSON.stringify(pack,null,2);
      if (new Blob([raw]).size>300000) return {ok:false,reason:'Modello troppo grande.'};
      if (!doc.defaultView.confirm('Il modello contiene testo e stili della sezione. Salvarlo come JSON riutilizzabile?')) return {ok:true,changed:false};
      download('MetaEditor_Modello_Sezione.json',raw,'application/json;charset=utf-8');
      return {ok:true,changed:false};
    }
    async function importSectionTemplate(file) {
      if (!file||file.size>300000) throw Error('File modello assente o troppo grande.');
      const pack=JSON.parse(await file.text());
      if (!pack||pack.schema!==sectionSchema||!sectionKinds.has(pack.kind)||
          Object.keys(pack).some(key=>!['schema','kind','tree'].includes(key))) throw Error('Formato modello di sezione non valido.');
      const section=unpackSectionNode(pack.tree,sectionBudget());
      if (section.localName!=='section'||!section.querySelector('h2,h3,p')) throw Error('Sezione incompleta.');
      section.dataset.localSection=pack.kind;
      const reference=sectionAt();
      if (reference&&protectedIsland(reference)) throw Error('Sezione protetta.');
      return transact(()=>{
        if (reference) reference.after(section);else main.append(section);
        for (const node of section.querySelectorAll('[data-local-block]')) assignBlockIdentity(node);
        refreshSections();select(section.querySelector('h2,h3,p'));
        notify('Modello inserito · Annulla per rimuoverlo.');
      },true);
    }
    // A section is a semantic boundary, not necessarily its content column.
    // In MAIOS and other real layouts the text lives inside nested flow wrappers.
    // Inserting directly into <section> can put new blocks outside the layout.
    const flowTags = 'p,h1,h2,h3,h4,h5,h6,blockquote';
    function flowChild(node, section) {
      const parent = node?.parentElement;
      return !!(node && parent && section.contains(node) &&
        node.matches(flowTags) && !protectedIsland(node) &&
        ['div','section','article'].includes(parent.localName) &&
        !parent.closest('figure,ul,ol,table,details') &&
        !node.closest('figure,ul,ol,table,details'));
    }
    function insertionPoint(section, useSelection = true) {
      if (!section) return null;
      const mode = placementPicker.value === 'before' ? 'before' : 'after';
      const explicit = chosenAnchor(section);
      if (explicitAnchorNode) {
        // An explicit but stale reference must not silently fall back to a
        // different card; it is a request to reselect a valid destination.
        return flowChild(explicit, section) ?
          {parent:explicit.parentElement, reference:explicit, mode} : null;
      }
      if (useSelection && flowChild(selected, section)) {
        return {parent:selected.parentElement, reference:selected, mode};
      }
      const candidates = anchorCandidates(section);
      const headings = candidates.filter(node=>node.matches('h1,h2,h3,h4,h5,h6'));
      const labelled = (section.getAttribute('aria-labelledby') || '')
        .trim().split(/\s+/).filter(Boolean);
      const heading = labelled.length ?
        headings.find(h => labelled.includes(h.id)) : null;
      if (heading) {
        const group = candidates.filter(node=>node.parentElement===heading.parentElement);
        const reference = group[group.length-1] || heading;
        return {parent:heading.parentElement, reference, mode};
      }
      // Multiple independent text-flow parents indicate multiple cards or
      // nested composition zones. DOM order is NOT a sufficient choice.
      const groups = new Set(candidates.map(node=>node.parentElement));
      if (groups.size !== 1) return null;
      const reference = candidates[candidates.length-1];
      return reference ? {parent:reference.parentElement, reference, mode} : null;
    }
    function insertAtPoint(node, point) {
      if (!point || !point.reference || point.reference.parentElement !== point.parent ||
          point.reference === node || node.contains(point.reference)) return false;
      point.reference.insertAdjacentElement(
        point.mode === 'before' ? 'beforebegin' : 'afterend', node);
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
        assignBlockIdentity(node);
        node.textContent = tag === 'p' ? 'Nuovo paragrafo' : 'Nuovo titolo';
        insertAtPoint(node, point);
        select(node);
        notify('Blocco aggiunto nel contenitore del testo selezionato.');
      }, true);
    }

    // Links are supported as explicit author actions, never as HTML pasted
    // into contenteditable. An existing plain <a> may be updated in place.
    function normalizedLink(raw) {
      const value = String(raw || '').trim();
      if (!value || value.length > 2048 || /[\s\u0000-\u001f\u007f]/.test(value)) return null;
      if (value.startsWith('#')) {
        const id = value.slice(1);
        return /^[A-Za-z][A-Za-z0-9_.:-]*$/.test(id) && doc.getElementById(id) ? value : null;
      }
      if (/^mailto:[a-z0-9.!#$%&'*+/=?^_~-]+@[a-z0-9.-]+\.[a-z]{2,}$/i.test(value))
        return value;
      if (/^tel:\+?[0-9().-]{5,25}$/i.test(value)) return value;
      try {
        const parsed = new URL(value);
        if (!['http:','https:'].includes(parsed.protocol) ||
            !parsed.hostname || parsed.username || parsed.password) return null;
        return parsed.href;
      } catch (_) { return null; }
    }
    function linkAction() {
      leaveEditing();
      const label = linkTextInput.value.trim();
      const href = normalizedLink(linkUrlInput.value);
      if (!label || label.length > 200) return {ok:false,reason:'Scrivi un testo breve per il collegamento.'};
      if (!href) return {ok:false,reason:'Indirizzo non supportato. Usa https, email, telefono o una #sezione esistente.'};
      if (selected?.isConnected && selected.matches('a')) {
        if (selected.children.length) return {ok:false,reason:'Collegamento strutturato: modifica non supportata.'};
        const node = selected;
        return transact(() => {
          node.textContent = label;
          node.setAttribute('href',href);
          select(node);
          notify('Collegamento aggiornato con una modifica annullabile.');
        });
      }
      const section = sectionRoots()[Number(selector.value)];
      const point = insertionPoint(section);
      if (!point) return {ok:false,reason:'Scegli un testo nella sezione di destinazione.'};
      return transact(() => {
        const p = doc.createElement('p');
        p.setAttribute('data-local-block','true');
        assignBlockIdentity(p);
        const a = doc.createElement('a');
        a.textContent = label;
        a.setAttribute('href',href);
        p.append(a);
        insertAtPoint(p,point);
        select(p);
        notify('Collegamento inserito nel flusso della pagina.');
      });
    }
    function imageType(bytes) {
      if (bytes.length < 12) return null;
      if (bytes[0] === 0x89 && bytes[1] === 0x50 && bytes[2] === 0x4e &&
          bytes[3] === 0x47 && bytes[4] === 0x0d && bytes[5] === 0x0a &&
          bytes[6] === 0x1a && bytes[7] === 0x0a) return 'image/png';
      if (bytes[0] === 0xff && bytes[1] === 0xd8 && bytes[2] === 0xff) return 'image/jpeg';
      const ascii = slice => String.fromCharCode(...slice);
      if (ascii(bytes.slice(0,4)) === 'RIFF' && ascii(bytes.slice(8,12)) === 'WEBP')
        return 'image/webp';
      if (['GIF87a','GIF89a'].includes(ascii(bytes.slice(0,6)))) return 'image/gif';
      return null;
    }
    async function addLocalImage(file, alt) {
      leaveEditing();
      const description = String(alt || '').trim();
      if (!description || description.length > 160)
        return {ok:false,reason:'Scrivi una descrizione breve dell’immagine prima di scegliere il file.'};
      if (!file || file.size < 12 || file.size > 1572864)
        return {ok:false,reason:'File assente o superiore a 1,5 MB.'};
      const type = imageType(new Uint8Array(await file.slice(0,16).arrayBuffer()));
      if (!type || (file.type && file.type !== type))
        return {ok:false,reason:'Sono ammesse solo immagini PNG, JPEG, WebP e GIF valide.'};
      const url = await new Promise((resolve,reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = () => reject(reader.error || new Error('Image read failed'));
        reader.readAsDataURL(file);
      });
      if (typeof url !== 'string' || !url.startsWith('data:'+type+';base64,'))
        return {ok:false,reason:'Impossibile incorporare i dati dell’immagine.'};
      const probe = new Image();
      probe.src = url;
      try { await probe.decode(); } catch (_) {
        return {ok:false,reason:'I dati dell’immagine non sono decodificabili.'};
      }
      if (!probe.naturalWidth || !probe.naturalHeight ||
          probe.naturalWidth > 6000 || probe.naturalHeight > 6000 ||
          probe.naturalWidth * probe.naturalHeight > 25000000)
        return {ok:false,reason:'Dimensioni dell’immagine non supportate.'};
      // Re-evaluate destination AFTER async work.
      const point = insertionPoint(sectionRoots()[Number(selector.value)]);
      if (!point) return {ok:false,reason:'Seleziona un punto di inserimento nella sezione.'};
      return transact(() => {
        const figure = doc.createElement('figure');
        figure.setAttribute('data-local-block','true');
        assignBlockIdentity(figure);
        figure.style.maxWidth = '100%';
        figure.style.margin = '1.3em 0';
        const img = doc.createElement('img');
        img.src = url; img.alt = description;
        img.style.maxWidth = '100%'; img.style.height = 'auto'; img.style.display = 'block';
        const caption = doc.createElement('figcaption');
        caption.textContent = description;
        figure.append(img,caption);
        insertAtPoint(figure,point);
        select(figure);
        notify('Immagine locale incorporata. Salva il lavoro per conservarla.');
      });
    }
    function updateImageDescription() {
      leaveEditing();
      if (!selected?.matches('figure[data-local-block]') || !selected.isConnected)
        return {ok:false,reason:'Seleziona un’immagine aggiunta dall’editor.'};
      const description = imageAltInput.value.trim();
      if (!description || description.length > 160)
        return {ok:false,reason:'La descrizione dell’immagine non può essere vuota.'};
      const figure = selected;
      const img = figure.querySelector(':scope > img');
      const caption = figure.querySelector(':scope > figcaption');
      if (!img) return {ok:false,reason:'Figura priva di immagine gestibile.'};
      return transact(() => {
        const oldAlt = img.alt;
        img.alt = description;
        // If an author has edited the caption independently, preserve it:
        // the accessible alt and the visible caption have distinct meaning.
        if (caption && caption.textContent === oldAlt) caption.textContent = description;
        select(figure);
        notify('Descrizione accessibile aggiornata. Annulla e Ripristina disponibili.');
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
        if (next.contains(node) && !explicitAnchorNode) return {ok:true,changed:false};
        const point = insertionPoint(next, false);
        if (!point) return {ok:false,reason:'Destinazione non univoca: scegli un riferimento preciso.'};
        if (point.reference === node || node.contains(point.reference) ||
            (node.parentElement===point.parent &&
              (point.mode==='before'?node.nextElementSibling:node.previousElementSibling)===point.reference))
          return {ok:true,changed:false};
        return transact(() => {
          insertAtPoint(node, point);
          select(node);
          notify('Blocco trasferito nel contenitore testuale di destinazione.');
        }, true);
      }
      if (action === 'up' && node.previousElementSibling?.hasAttribute('data-local-block')) {
        return transact(() => node.parentElement.insertBefore(node, node.previousElementSibling));
      }
      if (action === 'down' && node.nextElementSibling?.hasAttribute('data-local-block')) {
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
          assignBlockIdentity(copy);
          copy.removeAttribute('data-local-selected');
          copy.removeAttribute('data-local-editing');
          copy.removeAttribute('contenteditable');
          node.insertAdjacentElement('afterend', copy);
          select(copy);
          notify('Blocco aggiunto duplicato. La modifica è annullabile.');
        }, true);
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
      refreshSaveState();
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
      refreshSaveState();
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
      copy.querySelector('#me-neutral-context-actions')?.remove();
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
    function download(name, contents, mime='text/html;charset=utf-8') {
      const blob = new Blob([contents], {type:mime});
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

    selector.addEventListener('change', () => {
      explicitAnchorNode = null;
      refreshAnchors();
      syncCompositionControls();
    });
    sectionImport.addEventListener('change',async()=>{
      try { await importSectionTemplate(sectionImport.files?.[0]); }
      catch(error){notify('Modello rifiutato: '+String(error.message));}
      finally {sectionImport.value='';}
    });
    for (const [property,field] of Object.entries(appearanceFields)) {
      field.addEventListener('change',()=>{
        const result=changeAppearance(property,field.value);
        if (result.ok===false) notify(result.reason);
      });
    }
    anchorPicker.addEventListener('change', () => {
      const value = anchorPicker.value;
      const section = sectionRoots()[Number(selector.value)];
      const candidates = anchorCandidates(section);
      const index = value === '' ? -1 : Number(value);
      explicitAnchorNode = Number.isInteger(index) && index >= 0 ?
        candidates[index] || null : null;
    });
    imageFileInput.addEventListener('change', async () => {
      const file = imageFileInput.files?.[0];
      try {
        const result = await addLocalImage(file, imageAltInput.value);
        if (result.ok === false) notify(result.reason);
      } catch (error) { notify('Immagine rifiutata: ' + String(error.message)); }
      finally { imageFileInput.value = ''; }
    });
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
        revealSelection(node);
        notify('Elemento selezionato. Premi Modifica testo per lavorarci.');
      }
    });
    main.addEventListener('click', event => {
      // The image and its visible caption form one editor-owned component.
      // One click selects the figure; double click still edits figcaption.
      const node = event.target.closest('figure[data-local-block]') ||
        event.target.closest(SELECTABLE);
      if (!node || !safeNode(node)) return;
      if (event.target.closest('a')) event.preventDefault();
      select(node);
    });
    main.addEventListener('dblclick', event => {
      const node = event.target.closest(SELECTABLE);
      if (safeNode(node)) { select(node); if (node.matches(EDITABLE)) edit(); }
    });
    main.addEventListener('input', event => {
      // Typing must not clone the entire document for each character.
      // Exact no-op/dirty reconciliation happens on leaveEditing and unload.
      if (editing && editing.contains(event.target)) setSaveState(true);
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
      const plain = raw.replace(/\r\n?|\n/g, ' ');
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
      if (event.key === 'Enter' && !(event.ctrlKey||event.metaKey) && editing && editing.contains(event.target) &&
          editing.matches('h1,h2,h3,h4,h5,h6,p,blockquote,figcaption,li')) {
        // Keep the source document's block structure intact. Add separate
        // paragraphs/headings through explicit composition commands.
        event.preventDefault();
        notify('Per un nuovo blocco usa + Paragrafo o + Titolo.');
        return;
      }
      if ((event.key === 'Escape' || (event.key==='Enter'&&(event.ctrlKey||event.metaKey))) && editing && editing.contains(event.target)) {
        event.preventDefault();
        leaveEditing();
        if (!body.hidden) button('edit').focus();
        else { scheduleContextual(); }
        notify('Modifica terminata. Le modifiche sono disponibili in Annulla.');
      }
    });
    doc.addEventListener('keydown', event => {
      if ((event.ctrlKey || event.metaKey) && !event.shiftKey && !event.altKey &&
          String(event.key).toLowerCase() === 's') {
        event.preventDefault();
        // Never delegate Ctrl+S to Chrome's Save Page, which can produce a
        // browser-serialized document rather than the owned work format.
        download('MetaEditor_Lavoro_Modificabile.html', workHtml());
      }
    }, true);
    root.addEventListener('beforeunload', event => {
      if (!pendingWork()) return;
      // Browsers decide whether to show the confirmation dialog, usually
      // requiring prior user activation. Do not claim a download succeeded.
      event.preventDefault();
      event.returnValue = '';
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
        link: linkAction, 'image-alt': updateImageDescription,
        'section-add':()=>createSection(sectionTemplate.value),'section-export':exportSectionTemplate,
        'section-up':()=>changeSection('up'),'section-down':()=>changeSection('down'),
        'section-copy':()=>changeSection('copy'),'section-delete':()=>changeSection('delete'),
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
    refreshSaveState();
    notify('Le modifiche rimangono nel file di lavoro finché non scegli Salva lavoro.');
    return Object.freeze({
      status: () => Object.freeze({carrier:'static-page',regions:sectionRoots().length,dirty,
                                    canUndo:history.length>0,canRedo:future.length>0}),
      select, edit, format, insert, move, linkAction, addLocalImage, updateImageDescription, changeAddedBlock, undo, redo, cleanHtml, workHtml,
      toolbar, main
    });
  }
  root.MetaEditorNeutralStaticPage = Object.freeze({mount});
})(typeof window !== 'undefined' ? window : globalThis);
