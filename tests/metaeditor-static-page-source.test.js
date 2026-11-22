// SPDX-License-Identifier: MPL-2.0
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';

const code = readFileSync(new URL('../examples/collaborative-communication-medium/meta-editor-lab/static-page-source-adapter.js', import.meta.url), 'utf8');
const context = {};
runInNewContext(code, context);
const {locateMain} = context.MetaEditorStaticPageAdapter;

test('selects real main, not comments or quoted script contents', () => {
  const source = '<!doctype html><html><head><script>const x="<main>fake</main>";</script>'+
    '<style>.x::before{content:"<main>"}</style></head><body><!-- <main>fake</main> -->'+
    '<main data-x="a > b"><p>A</p></main><footer>keep</footer></body></html>';
  const span = locateMain(source);
  assert.equal(source.slice(span.openStart, span.openEnd), '<main data-x="a > b">');
  assert.equal(source.slice(span.openEnd, span.closeStart), '<p>A</p>');
  assert.equal(source.slice(span.closeEnd), '<footer>keep</footer></body></html>');
});

test('rejects missing, duplicate, nested and orphan main regions', () => {
  for (const html of [
    '<html><body><p>no main</p></body></html>',
    '<main>one</main><main>two</main>',
    '<main><main>nested</main></main>',
    '</main>', '<main>unclosed', '<main/>',
  ]) assert.throws(() => locateMain(html), /MetaEditor static source:/);
});

test('refuses malformed comments and tags rather than guessing', () => {
  assert.throws(() => locateMain('<!-- not closed <main>x</main>'), /unterminated comment/);
  assert.throws(() => locateMain('<main class="not closed>'), /unterminated HTML tag/);
});
