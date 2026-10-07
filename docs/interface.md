# JavaScript medium interface

`createMedium({ state, render, onAction, onObserverError })` returns a local interface. State
and actions are JSON values; the top-level state and action are objects.
The receiving kernel owns their domain schema. Strings, booleans, null,
finite numbers, arrays and plain objects are accepted. Unsupported values
are rejected rather than silently discarded.

`render` receives an immutable copy of the exposed state. The initial state
is rendered immediately. Supply accessible controls and a text equivalent
when a spatial renderer carries meaningful content.

## Kernel → UI

`receive({ id, state })` publishes a complete exposed snapshot. `id` is the
receiving controller's nonempty event identity, unique for this medium
instance. A repeated identity is rejected. The domain can keep the same
focus and layout while changing a proposal, consequence or available action.

Observers receive `{ kind: 'state', sequence, id, before, after }`.
`sequence` orders this instance's observable records; it is not wall-clock
time or an interaction-latency measurement. Snapshots permit reconstruction
of exposed state, not of hidden reasoning or a physical sensory experience.

## Human → kernel

`dispatch(action)` emits `{ kind: 'action', sequence, action, state }`, then
calls `onAction(action)`. Dispatch alone does not change the medium state.
The receiving controller interprets the action and can publish a resulting
state through `receive`. An asynchronous controller can do so later; the
medium imposes no model provider or transport.

## Observation and lifetime

`observe(listener)` returns an unsubscribe function. Records and internal
snapshots are immutable. `snapshot()` returns a separate copy. Observers
subscribe to future records; the controller can retain only the history its
application needs. `destroy()` closes this interface and clears observers.

An observer failure calls optional `onObserverError(error, record)` and does
not block another observer or the human-action callback. The default error
handler does nothing; supply one when the application needs diagnostic reporting.

The medium does not embed a fixed vocabulary of considerations, options,
opportunities, sensory channels or views. The receiving state can carry
them where their meaning is useful. Renderer and transport adapters can
change while retaining the same state/action relation.

For one exercised composition, see `examples/nautico/app.js`. Its controller
is illustrative and independent of a live domain kernel.
