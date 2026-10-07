import test from 'node:test';
import assert from 'node:assert/strict';
import { createMedium } from '../src/medium.js';

test('receive exposes before/after while preserving supplied focus', () => {
  const rendered = [], records = [];
  const ui = createMedium({ state: { focus: 'stern', choice: null }, render: s => rendered.push(s) });
  ui.observe(r => records.push(r));
  ui.receive({ id: 'supply-1', state: { focus: 'stern', choice: 'A' } });
  assert.equal(rendered.length, 2);
  assert.deepEqual(records[0].before, { focus: 'stern', choice: null });
  assert.deepEqual(records[0].after, { focus: 'stern', choice: 'A' });
});

test('human action returns to controller and does not imply a state change', () => {
  let received;
  const ui = createMedium({ state: { choice: null }, render() {}, onAction: a => { received = a; } });
  ui.dispatch({ type: 'choose', value: 'A' });
  assert.deepEqual(received, { type: 'choose', value: 'A' });
  assert.deepEqual(ui.snapshot(), { choice: null });
});

test('producer, renderer, observer and consumer cannot mutate internal state', () => {
  const input = { focus: { id: 'stern' } };
  let rendered, record;
  const ui = createMedium({ state: input, render: s => { rendered = s; } });
  input.focus.id = 'elsewhere';
  assert.throws(() => { rendered.focus.id = 'elsewhere'; }, TypeError);
  ui.observe(r => { record = r; });
  ui.dispatch({ type: 'inspect' });
  assert.throws(() => { record.state.focus.id = 'elsewhere'; }, TypeError);
  const copy = ui.snapshot(); copy.focus.id = 'elsewhere';
  assert.equal(ui.snapshot().focus.id, 'stern');
});

test('duplicate identity and non-JSON values do not advance exposed state', () => {
  const ui = createMedium({ state: { x: 1 }, render() {} });
  ui.receive({ id: 'event-1', state: { x: 2 } });
  assert.throws(() => ui.receive({ id: 'event-1', state: { x: 3 } }));
  assert.throws(() => ui.receive({ id: 'event-2', state: { x: NaN } }), TypeError);
  assert.throws(() => ui.dispatch({ type: 'x', handler() {} }), TypeError);
  assert.deepEqual(ui.snapshot(), { x: 2 });
});

test('controller responses are ordered after the human action', () => {
  const records = [];
  let ui;
  ui = createMedium({ state: { chosen: false }, render() {}, onAction: () => {
    ui.receive({ id: 'response-1', state: { chosen: true } });
  } });
  ui.observe(r => records.push(r)); ui.dispatch({ type: 'choose' });
  assert.deepEqual(records.map(r => [r.kind, r.sequence]), [['action', 1], ['state', 2]]);
});

test('unsubscribe and destroy close the observation lifetime', () => {
  let count = 0;
  const ui = createMedium({ state: {}, render() {} });
  const stop = ui.observe(() => { count++; }); stop(); ui.dispatch({ type: 'inspect' });
  assert.equal(count, 0); ui.destroy();
  assert.throws(() => ui.dispatch({ type: 'inspect' }));
});

test('a faulty observer cannot swallow a human intervention', () => {
  const errors = [], records = [];
  let acted = false;
  const ui = createMedium({ state: {}, render() {}, onAction() { acted = true; },
    onObserverError(error) { errors.push(error.message); } });
  ui.observe(() => { throw new Error('observer failed'); });
  ui.observe(record => records.push(record));
  ui.dispatch({ type: 'continue' });
  assert.equal(acted, true);
  assert.deepEqual(errors, ['observer failed']);
  assert.equal(records[0].kind, 'action');
});
