function jsonCopy(value, seen = new Set()) {
  if (value === null || typeof value === 'string' || typeof value === 'boolean') return value;
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  if (typeof value !== 'object' || seen.has(value)) throw new TypeError('Use acyclic JSON values');
  if (!Array.isArray(value) && Object.getPrototypeOf(value) !== Object.prototype) {
    throw new TypeError('Use plain JSON objects');
  }
  seen.add(value);
  const copy = Array.isArray(value) ? [] : {};
  for (const [key, item] of Object.entries(value)) {
    Object.defineProperty(copy, key, {
      value: jsonCopy(item, seen), enumerable: true, writable: true, configurable: true,
    });
  }
  seen.delete(value);
  return copy;
}

function freeze(value) {
  if (value && typeof value === 'object') {
    Object.values(value).forEach(freeze);
    Object.freeze(value);
  }
  return value;
}

function objectCopy(value) {
  if (!value || Array.isArray(value) || typeof value !== 'object') {
    throw new TypeError('State and actions must be JSON objects');
  }
  return freeze(jsonCopy(value));
}

export function createMedium({ state: initialState, render, onAction = () => {}, onObserverError = () => {} }) {
  if ([render, onAction, onObserverError].some(callback => typeof callback !== 'function')) {
    throw new TypeError('Supply function callbacks');
  }
  let state = objectCopy(initialState);
  let sequence = 0;
  let closed = false;
  const observers = new Set();
  const ids = new Set();
  const assertOpen = () => { if (closed) throw new Error('Medium is closed'); };
  const emit = record => {
    freeze(record);
    for (const listener of [...observers]) {
      try { listener(record); }
      catch (error) {
        try { onObserverError(error, record); } catch { /* Diagnostics cannot block human action. */ }
      }
    }
  };
  render(state);

  return {
    receive({ id, state: nextState }) {
      assertOpen();
      if (typeof id !== 'string' || !id.trim()) throw new TypeError('Supply an event identity');
      if (ids.has(id)) throw new Error('Event identity already received');
      const next = objectCopy(nextState);
      render(next);
      const before = state;
      state = next;
      ids.add(id);
      emit({ kind: 'state', sequence: ++sequence, id, before, after: state });
    },
    dispatch(action) {
      assertOpen();
      const copied = objectCopy(action);
      emit({ kind: 'action', sequence: ++sequence, action: copied, state });
      return onAction(copied);
    },
    observe(listener) {
      assertOpen();
      if (typeof listener !== 'function') throw new TypeError('Supply an observer');
      observers.add(listener);
      return () => observers.delete(listener);
    },
    snapshot() { assertOpen(); return jsonCopy(state); },
    destroy() { closed = true; observers.clear(); ids.clear(); },
  };
}
