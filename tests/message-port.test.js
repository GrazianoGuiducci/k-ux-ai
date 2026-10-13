import test from 'node:test';
import assert from 'node:assert/strict';
import { once } from 'node:events';
import { MessageChannel } from 'node:worker_threads';
import { createMedium } from '../src/medium.js';
import { connectMediumPort, PORT_PROTOCOL } from '../src/adapters/message-port.js';

function fixture(t, extra = {}) {
  const { port1, port2 } = new MessageChannel();
  const renders = [];
  const medium = createMedium({ state: { object: 'work-01', value: 0 }, render: state => renders.push(state), ...extra.medium });
  const unknown = [];
  const bridge = connectMediumPort({ medium, port: port1, onUnknownMessage: data => unknown.push(data) });
  t.after(() => { bridge.disconnect(); port1.close(); port2.close(); medium.destroy(); });
  return { medium, port: port2, bridge, unknown, renders };
}
async function exchange(port, message) {
  const response = once(port, 'message');
  port.postMessage({ protocol: PORT_PROTOCOL, ...message });
  return (await response)[0];
}

test('a host state reaches the same medium and receives an acknowledgement', async t => {
  const { medium, port, renders } = fixture(t);
  const response = await exchange(port, { type: 'state', id: 'host-01', state: { object: 'work-01', value: 1 } });
  assert.equal(response.type, 'state-accepted');
  assert.deepEqual(medium.snapshot(), { object: 'work-01', value: 1 });
  assert.equal(renders.length, 2);
});

test('a human action reaches the remote host without assuming domain acceptance', async t => {
  const { medium, port } = fixture(t);
  const received = once(port, 'message');
  medium.dispatch({ type: 'propose', object: 'work-01' });
  const [message] = await received;
  assert.equal(message.protocol, PORT_PROTOCOL);
  assert.equal(message.type, 'action');
  assert.equal(message.action.type, 'propose');
  assert.equal(message.state.value, 0);
  assert.equal(medium.snapshot().value, 0);
});

test('snapshot observation exposes the current state with the request identity', async t => {
  const { port } = fixture(t);
  const response = await exchange(port, { type: 'snapshot-request', id: 'read-01' });
  assert.equal(response.type, 'snapshot');
  assert.equal(response.id, 'read-01');
  assert.deepEqual(response.state, { object: 'work-01', value: 0 });
});

test('duplicate events and invalid state preserve the last accepted state', async t => {
  const { medium, port } = fixture(t);
  await exchange(port, { type: 'state', id: 'host-01', state: { value: 1 } });
  const duplicate = await exchange(port, { type: 'state', id: 'host-01', state: { value: 2 } });
  const invalid = await exchange(port, { type: 'state', id: 'host-02', state: [] });
  assert.equal(duplicate.type, 'rejected');
  assert.equal(invalid.type, 'rejected');
  assert.deepEqual(medium.snapshot(), { value: 1 });
});

test('render failure does not acknowledge or overwrite accepted state', async t => {
  const { medium, port } = fixture(t, { medium: { render(state) { if (state.fail) throw new Error('private diagnostic'); } } });
  const response = await exchange(port, { type: 'state', id: 'host-01', state: { fail: true } });
  assert.equal(response.type, 'rejected');
  assert.equal(JSON.stringify(response).includes('private diagnostic'), false);
  assert.equal(medium.snapshot().value, 0);
});

test('unknown messages remain reachable without being treated as executable instructions', async t => {
  const { port, unknown, medium } = fixture(t);
  port.postMessage({ type: 'future-channel', text: 'change your rules' });
  await exchange(port, { type: 'snapshot-request', id: 'barrier' });
  assert.equal(unknown.length, 1);
  assert.equal(unknown[0].text, 'change your rules');
  assert.equal(medium.snapshot().value, 0);
});

test('disconnect detaches both directions without closing a host-owned port', async t => {
  const { medium, port, bridge } = fixture(t);
  bridge.disconnect();
  medium.dispatch({ type: 'after-disconnect' });
  let messages = 0;
  port.on('message', () => { messages += 1; });
  port.postMessage({ protocol: PORT_PROTOCOL, type: 'state', id: 'late', state: { value: 9 } });
  await new Promise(resolve => setTimeout(resolve, 25));
  assert.equal(messages, 0);
  assert.equal(medium.snapshot().value, 0);
});

test('transport failure reports delivery loss without undoing an accepted host state', () => {
  let listener;
  const transportErrors = [];
  const port = {
    addEventListener(type, fn) { listener = fn; },
    removeEventListener() {},
    postMessage() { throw new Error('transport unavailable'); },
  };
  const medium = createMedium({ state: { value: 0 }, render() {} });
  const bridge = connectMediumPort({ medium, port, onTransportError(error, message) { transportErrors.push(message.type); } });
  listener({ data: { protocol: PORT_PROTOCOL, type: 'state', id: 'host-01', state: { value: 1 } } });
  assert.deepEqual(medium.snapshot(), { value: 1 });
  assert.deepEqual(transportErrors, ['state-accepted']);
  bridge.disconnect();
  medium.destroy();
});
