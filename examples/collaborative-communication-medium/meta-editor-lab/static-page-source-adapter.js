/* SPDX-License-Identifier: MPL-2.0
 * Copyright (c) 2026 Graziano Guiducci.
 * A bounded, source-preserving export adapter for supported static HTML pages.
 * This module does not import, execute, or publish source HTML.
 */
(function (root) {
  'use strict';

  function fail(reason) { throw new Error('MetaEditor static source: ' + reason); }

  // Locate exactly one main element without confusing tags in comments,
  // quoted attributes, script/style raw-text elements or ordinary text.
  // This is a conservative scanner for a supported static subset, NOT an HTML parser.
  function locateMain(source) {
    if (typeof source !== 'string' || !source.trim()) fail('empty/non-text source');
    const lower = source.toLowerCase();
    let pos = 0;
    let found = null;
    let depth = 0;
    while (pos < source.length) {
      const lt = source.indexOf('<', pos);
      if (lt < 0) break;
      if (source.startsWith('<!--', lt)) {
        const end = source.indexOf('-->', lt + 4);
        if (end < 0) fail('unterminated comment');
        pos = end + 3;
        continue;
      }
      if (source.startsWith('<![CDATA[', lt)) {
        const end = source.indexOf(']]>', lt + 9);
        if (end < 0) fail('unterminated CDATA');
        pos = end + 3;
        continue;
      }
      const head = source.slice(lt, lt + 100).match(/^<\s*(\/?)\s*([a-z][a-z0-9:-]*)\b/i);
      if (!head) { pos = lt + 1; continue; }
      const closing = !!head[1];
      const name = head[2].toLowerCase();
      let index = lt + head[0].length;
      let quote = null;
      while (index < source.length) {
        const c = source[index++];
        if (quote) { if (c === quote) quote = null; }
        else if (c === '"' || c === "'") quote = c;
        else if (c === '>') break;
      }
      if (index > source.length || source[index - 1] !== '>') fail('unterminated HTML tag');
      const selfClosing = /\/\s*>$/.test(source.slice(lt, index));
      if (name === 'main') {
        if (selfClosing) fail('self-closed main not supported');
        if (!closing) {
          if (depth || found) fail('duplicate or nested main');
          found = {openStart: lt, openEnd: index}; depth = 1;
        } else {
          if (depth !== 1 || !found) fail('orphan closing main');
          found.closeStart = lt;
          found.closeEnd = index;
          depth = 0;
        }
      }
      pos = index;
      if (!closing && !selfClosing && (name === 'script' || name === 'style')) {
        const endMarker = '</' + name;
        const start = lower.indexOf(endMarker, pos);
        if (start < 0) fail('unclosed ' + name);
        // Resume at the closing tag (which will then be read normally).
        pos = start;
      }
    }
    if (!found || depth || found.closeStart == null) fail('exactly one complete main required');
    return found;
  }

  const attrsToStrip = name => name === 'contenteditable' ||
    name.startsWith('data-local-') || name.startsWith('data-me0') || name.startsWith('data-me1');

  function stripRuntime(element) {
    const copy = element.cloneNode(true);
    for (const el of [copy, ...copy.querySelectorAll('*')]) {
      for (const attribute of el.getAttributeNames()) {
        if (attrsToStrip(attribute)) el.removeAttribute(attribute);
      }
    }
    // A selected text fragment should never be exported as an active input.
    return copy;
  }

  function create({sourceHtml, regionElement, runtimeRootAttributes = {}}) {
    const region = locateMain(sourceHtml);
    const parsed = new DOMParser().parseFromString(sourceHtml, 'text/html');
    const original = parsed.querySelector('main');
    if (!original || parsed.querySelectorAll('main').length !== 1) fail('unsupported parsed document');
    if (!regionElement || regionElement.localName !== 'main') fail('editable root must be main');
    if (original.querySelector('script,style,template,iframe,object,embed'))
      fail('active/embedded content inside editable main is unsupported');
    for (const el of [original, ...original.querySelectorAll('*')]) {
      for (const name of el.getAttributeNames()) {
        if (attrsToStrip(name)) fail('author source uses editor-reserved attributes: ' + name);
      }
    }
    const originalRootAttrs = [...original.attributes].map(a => [a.name, a.value]);
    const baseline = original.innerHTML;
    const pre = sourceHtml.slice(0, region.openStart);
    const opening = sourceHtml.slice(region.openStart, region.openEnd);
    const closing = sourceHtml.slice(region.closeStart, region.closeEnd);
    const post = sourceHtml.slice(region.closeEnd);

    function exportHtml() {
      const clean = stripRuntime(regionElement);
      for (const [name, value] of Object.entries(runtimeRootAttributes)) {
        if (!original.hasAttribute(name) && clean.getAttribute(name) === value) clean.removeAttribute(name);
      }
      const currentAttrs = [...clean.attributes].map(a => [a.name, a.value]);
      if (JSON.stringify(currentAttrs) !== JSON.stringify(originalRootAttrs))
        fail('main root attributes changed; outside scope');
      if (clean.querySelector('script,style,template,iframe,object,embed'))
        fail('active/embedded content inside edited main is unsupported');
      const html = clean.innerHTML;
      // Identity is a feature: no-op export keeps the exact source bytes after UTF-8 encode.
      return html === baseline ? sourceHtml : pre + opening + html + closing + post;
    }
    return Object.freeze({exportHtml, initialContent:baseline, modified: () => stripRuntime(regionElement).innerHTML !== baseline});
  }

  root.MetaEditorStaticPageAdapter = Object.freeze({create, locateMain});
})(typeof window !== 'undefined' ? window : globalThis);
