import { createMedium } from '../../src/medium.js';
import { initialState } from './case.js';

const byId = id => document.getElementById(id);
const escape = value => String(value).replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
let eventNumber = 0;
const records = [];

function render(state) {
  byId('question').textContent = state.question;
  byId('intent').textContent = state.intent;
  byId('view-label').textContent = state.view === 'detail' ? 'LE POSSIBILITÀ DELLA POPPA' : "VISTA D'INSIEME";
  byId('vessel').classList.toggle('detail', state.view === 'detail');
  byId('overview-panel').hidden = state.view === 'detail';
  byId('detail-panel').hidden = state.view !== 'detail';
  byId('toggle-view').innerHTML = state.view === 'detail' ? 'Ritorna al ciclo <span aria-hidden="true">↙</span>' : 'Esplora la poppa <span aria-hidden="true">↗</span>';
  byId('scene-state').textContent = state.selected ? 'proposta ' + state.selected + ' nel campo.' : 'attraversa il ciclo.';
  byId('last-change').textContent = state.lastChange;
  byId('simulate').textContent = state.supplyCheck ? 'Ricevi un altro evento di verifica ↓' : 'Ricevi verifica di fornitura ↓';
  byId('phases').innerHTML = state.phases.map((p, i) => '<div class="phase"><span class="phase-number">0' + (i + 1) + '</span><div><strong>' + escape(p.label) + '</strong><p>' + escape(p.detail) + '</p></div></div>').join('');
  const activeOption = document.activeElement?.dataset?.option;
  byId('options').innerHTML = state.options.map(o => '<button class="option" data-option="' + escape(o.id) + '" aria-pressed="' + (state.selected === o.id) + '"><span class="option-title"><strong>' + escape(o.label) + '</strong><span>' + escape(o.state) + '</span></span><p>' + escape(o.detail) + '</p></button>').join('');
  if (activeOption && state.view === 'detail') {
    [...byId('options').querySelectorAll('button')].find(b => b.dataset.option === activeOption)?.focus({ preventScroll: true });
  }
}

const ui = createMedium({ state: initialState, render, onAction(action) {
  const state = ui.snapshot();
  if (action.type === 'navigate') {
    state.view = action.view;
    state.lastChange = action.view === 'detail' ? 'La domanda entra nel dettaglio. Il suo ciclo resta presente.' : 'Ritrovi il ciclo con la stessa domanda e la scelta conservata.';
  } else if (action.type === 'select') {
    state.selected = action.option;
    state.lastChange = 'La proposta ' + action.option + ' orienta l’esplorazione. Progetto, costruzione e uso restano collegati.';
  } else return;
  ui.receive({ id: 'human-response-' + ++eventNumber, state });
} });

ui.observe(record => {
  records.push(record);
  byId('record-count').textContent = records.length + ' passaggi';
  byId('trace').textContent = records.map(r => JSON.stringify(r, null, 2)).join('\n\n');
});
byId('toggle-view').addEventListener('click', () => ui.dispatch({ type: 'navigate', caseId: initialState.caseId, view: ui.snapshot().view === 'detail' ? 'overview' : 'detail' }));
byId('options').addEventListener('click', event => {
  const button = event.target.closest('[data-option]');
  if (button) ui.dispatch({ type: 'select', caseId: initialState.caseId, option: button.dataset.option });
});
byId('simulate').addEventListener('click', () => {
  const state = ui.snapshot();
  state.supplyCheck = true;
  state.options.find(o => o.id === 'B').state = 'Verifica aperta';
  state.phases.find(p => p.id === 'build').detail = 'La proposta B richiede una verifica di integrazione e fornitura.';
  state.lastChange = 'Una verifica si apre sulla proposta B. La tua domanda e la scelta restano presenti.';
  ui.receive({ id: 'supply-event-' + ++eventNumber, state });
});

// This local development surface exposes only the synthetic example controller.
window.nauticoDevelopment = Object.freeze({ snapshot: ui.snapshot, records: () => structuredClone(records) });
