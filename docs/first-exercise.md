# First Nautico exercise

Date: 2026-10-07. Source version: 0.1.0-alpha.1.

The browser exercise used the synthetic stern-access case in this repository.
Keyboard activation opened the detail and selected proposal A. A simulated
supply event marked proposal B as requiring verification while preserving the
question, detail view and A selection. The verification control retained
keyboard focus. Returning to the overview preserved A and showed the changed
construction relation. The local observer contained seven ordered records:
three human actions and their state responses, plus the supply event.

Desktop composition and a 375-pixel mobile viewport were observed. The mobile
document had no horizontal overflow. These observations cover this renderer
and local controller; they are not measurements of human comprehension,
latency or a live receiving-kernel connection.

The Node contract tests cover before/after snapshots, human-action return,
state isolation, duplicate identities, unsupported values, record ordering,
observer lifetime and an observer failure that must not swallow human action.
Run `npm test` to exercise the current contract.

The exercise exposed one UI correction: disabling the simulated-event button
after the first event lost keyboard focus. It now remains available to receive
another illustrative event. This preserves the control while the case changes.
