import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const html = fs.readFileSync(new URL('../examples/public-griglia/demo/index.html', import.meta.url), 'utf8');
const between = (start, end) => html.slice(html.indexOf(start), html.indexOf(end, html.indexOf(start)));

// Exercise the generated engine's real resize listeners and rendered dimensions.
// The DOM double supplies measurements and pointer capture, not a second resize algorithm.
function cardFixture({scale = 1, compact = true} = {}) {
  const listeners = new Map();
  const capture = new Set();
  const handle = {
    addEventListener(type, fn) { if (!listeners.has(type)) listeners.set(type, new Set()); listeners.get(type).add(fn); },
    removeEventListener(type, fn) { listeners.get(type)?.delete(fn); },
    setPointerCapture(id) { capture.add(id); },
    hasPointerCapture(id) { return capture.has(id); },
    releasePointerCapture(id) { capture.delete(id); },
  };
  const stage = {clientWidth: 1200, clientHeight: 800,
    getBoundingClientRect: () => ({left: 70, top: 100, width: 1200 * scale, height: 800 * scale})};
  const leaf = {hidden: false, inert: false, textContent: '', setAttribute() {}, querySelector() { return leaf; }};
  const node = {style: {}, dataset: {}, setAttribute() {}, removeAttribute() {}, getAnimations: () => [],
    querySelector: selector => selector === '.kux-entity-resize' ? handle : leaf,
    getBoundingClientRect() {
      return {left: 70 + parseFloat(this.style.left) * scale, top: 100 + parseFloat(this.style.top) * scale,
        width: parseFloat(this.style.width) * scale, height: parseFloat(this.style.height) * scale};
    }};
  const p = {x: 100, y: 100, w: 700, h: 600, z: 4, context: 'test', intent: 'fare', compact,
    maximized: false, minimized: false, dock: null, el: node};
  const context = {p, node, state: {layout: 'free'}, shell: {stage}, contexts: {test: {next: 'Continue'}},
    readIntent: () => ({verb: 'Fare'}), ctxName: () => 'Test', focusPanel() {}, switchToFreeFromCurrent() {}};
  context.placePanels = () => context.moduleStyles(p, context.screenRect(p));
  vm.createContext(context);
  const helper = html.includes('function preparePanelResize(p){')
    ? between('function preparePanelResize(p){', 'function moduleElement(p){') : '';
  vm.runInContext(between('const limit=(v,lo,hi)', 'function overlapArea(') + '\n' + helper + '\n' +
    between('function moduleStyles(p,rect){', 'const fitRect=p=>screenRect(p);') + '\n' +
    between("const handle=node.querySelector('.kux-entity-resize');", "node.addEventListener('click',event=>"), context);
  context.moduleStyles(p, context.screenRect(p));
  const emit = (type, value) => {
    const event = {button: 0, pointerId: 1, preventDefault() {}, stopPropagation() {}, ...value};
    for (const fn of [...(listeners.get(type) || [])]) fn(event);
  };
  const size = () => ({w: parseFloat(node.style.width), h: parseFloat(node.style.height)});
  return {p, node, size, emit};
}

test('keyboard resize grows a compact card from its visible dimensions', () => {
  const card = cardFixture();
  assert.deepEqual(card.size(), {w: 350, h: 235});
  card.emit('keydown', {key: 'ArrowRight', shiftKey: true});
  card.emit('keydown', {key: 'ArrowDown', shiftKey: true});
  assert.deepEqual(card.size(), {w: 390, h: 275});
  assert.equal(card.p.compact, true);
});

test('pointer resize follows the displayed corner without a first-move jump', () => {
  const card = cardFixture();
  card.emit('pointerdown', {clientX: 500, clientY: 435});
  card.emit('pointermove', {clientX: 501, clientY: 436});
  assert.deepEqual(card.size(), {w: 351, h: 236});
  card.emit('pointermove', {clientX: 580, clientY: 495});
  card.emit('pointerup', {});
  assert.deepEqual(card.size(), {w: 430, h: 295});
  assert.equal(card.p.savedFreeRect.w, 430);
  assert.equal(card.p.savedFreeRect.h, 295);
});

test('pointer coordinates respect a scaled stage and retain viewport bounds', () => {
  const card = cardFixture({scale: 2});
  card.emit('pointerdown', {clientX: 1000, clientY: 900});
  card.emit('pointermove', {clientX: 1080, clientY: 960});
  assert.deepEqual(card.size(), {w: 390, h: 265});
  card.emit('pointermove', {clientX: 9000, clientY: 9000});
  card.emit('pointerup', {});
  assert.equal(card.size().w, 1188);
  assert.equal(card.size().h, 788);
  assert.ok(card.p.x + card.p.w <= 1200 && card.p.y + card.p.h <= 800);
});

test('ordinary free cards retain their resize behavior', () => {
  const card = cardFixture({compact: false});
  card.emit('keydown', {key: 'ArrowLeft', shiftKey: false});
  assert.deepEqual(card.size(), {w: 685, h: 600});
});
