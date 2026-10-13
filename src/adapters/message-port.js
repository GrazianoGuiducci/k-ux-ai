export const PORT_PROTOCOL = 'kux.port.v1';

/**
 * Bind an already-authorized MessagePort to a medium.
 * The host owns the port's identity, transport, domain and action authority.
 */
export function connectMediumPort({ medium, port, onUnknownMessage = () => {}, onTransportError = () => {} }) {
  if (!medium || ['receive', 'observe', 'snapshot'].some(key => typeof medium[key] !== 'function')) {
    throw new TypeError('Supply a medium instance');
  }
  if (!port || ['postMessage', 'addEventListener', 'removeEventListener'].some(key => typeof port[key] !== 'function')) {
    throw new TypeError('Supply an authorized MessagePort');
  }
  if ([onUnknownMessage, onTransportError].some(callback => typeof callback !== 'function')) {
    throw new TypeError('Supply observation callbacks');
  }
  let connected = true;
  const send = message => {
    if (!connected) return;
    try { port.postMessage({ protocol: PORT_PROTOCOL, ...message }); }
    catch (error) {
      try { onTransportError(error, message); } catch { /* Diagnostics do not undo accepted state. */ }
    }
  };
  const unsubscribe = medium.observe(record => {
    if (record.kind === 'action') {
      send({ type: 'action', sequence: record.sequence, action: record.action, state: record.state });
    }
  });
  const onMessage = event => {
    if (!connected) return;
    const message = event.data;
    if (!message || typeof message !== 'object' || message.protocol !== PORT_PROTOCOL) {
      onUnknownMessage(message);
      return;
    }
    try {
      if (message.type === 'state') {
        medium.receive({ id: message.id, state: message.state });
        send({ type: 'state-accepted', id: message.id });
      } else if (message.type === 'snapshot-request') {
        if (typeof message.id !== 'string' || !message.id.trim()) throw new TypeError('Supply a request identity');
        send({ type: 'snapshot', id: message.id, state: medium.snapshot() });
      } else {
        onUnknownMessage(message);
      }
    } catch {
      send({
        type: 'rejected',
        id: typeof message.id === 'string' ? message.id : null,
        operation: message.type,
        reason: 'The medium did not accept this operation; the current state is unchanged.',
      });
    }
  };
  port.addEventListener('message', onMessage);
  port.start?.();
  return {
    disconnect() {
      if (!connected) return;
      connected = false;
      unsubscribe();
      port.removeEventListener('message', onMessage);
    },
  };
}
