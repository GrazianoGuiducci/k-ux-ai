import { createMedium } from '../../src/medium.js';
import { connectMediumPort, PORT_PROTOCOL } from '../../src/adapters/message-port.js';
import { createWindowSurface } from '../../src/ui/window-surface.js';
import { createChatFormModule } from '../../src/ui/chat-form-module.js';

const byId = id => document.getElementById(id);
const copy = value => JSON.parse(JSON.stringify(value));
const initial = {
  object: { id: 'project/object-01', title: 'Una scelta da comprendere', summary: 'Il progetto mantiene il proprio riferimento mentre arrivano nuove informazioni.' },
  source: { id: 'reference-01', title: 'Riferimento iniziale', description: 'Fonte sintetica del ricevente locale.' },
  revision: 0,
  consequence: { title: 'Possibilità aperta', description: 'Puoi preparare una domanda o contribuire una nuova traccia.' },
  acceptedContributions: [],
  lastResult: null,
};
let hostState = copy(initial);
let exposed = copy(initial);
let medium, windowSurface, chat, connection;
let eventCounter = 0, requestCounter = 0;
const pending = new Map();
const records = [];
const channel = new MessageChannel();

function readback() {
  return {
    state: copy(exposed),
    view: windowSurface?.snapshot() ?? null,
    interaction: chat?.snapshot() ?? null,
    recentEvents: copy(records),
  };
}
function showReadback() { byId('readback').textContent = JSON.stringify(readback(), null, 2); }
function render(state) {
  exposed = copy(state);
  byId('object-title').textContent = state.object.title;
  byId('object-summary').textContent = state.object.summary;
  byId('revision').textContent = 'Revisione ' + state.revision;
  byId('source-title').textContent = state.source.title;
  byId('source-description').textContent = state.source.description;
  byId('consequence-title').textContent = state.consequence.title;
  byId('consequence-description').textContent = state.consequence.description;
  if (state.lastResult && pending.has(state.lastResult.requestId)) {
    pending.get(state.lastResult.requestId).resolve(copy(state.lastResult));
    pending.delete(state.lastResult.requestId);
  }
  showReadback();
}
medium = createMedium({ state: initial, render });
connection = connectMediumPort({ medium, port: channel.port1 });
medium.observe(record => {
  records.push(copy(record));
  if (records.length > 12) records.shift();
  showReadback();
});

function publishHostState() {
  channel.port2.postMessage({
    protocol: PORT_PROTOCOL, type: 'state', id: 'host-event-' + (++eventCounter), state: copy(hostState),
  });
}
function request(action) {
  const requestId = 'human-' + (++requestCounter);
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => { pending.delete(requestId); reject(new Error('Local controller did not confirm')); }, 2500);
    pending.set(requestId, { resolve(result) { clearTimeout(timer); resolve(result); } });
    medium.dispatch({ ...action, requestId, objectId: hostState.object.id });
  });
}
channel.port2.addEventListener('message', event => {
  const message = event.data;
  if (message?.protocol !== PORT_PROTOCOL || message.type !== 'action') return;
  const action = message.action;
  const accepted = action.objectId === hostState.object.id && ['ask', 'contribute'].includes(action.type);
  const result = {
    requestId: action.requestId, accepted,
    message: accepted ? 'Il controller locale ha accettato il tuo intervento.' : 'Azione non disponibile per questo oggetto.',
  };
  if (accepted && action.type === 'contribute') {
    hostState.acceptedContributions.push(copy(action.draft));
    hostState.consequence = { title: 'Contributo conservato', description: action.draft.note };
  } else if (accepted) {
    result.reply = 'Ricezione locale confermata per ' + hostState.object.id + '. La fonte corrente è: ' + hostState.source.title + '. Nessun modello AI è stato chiamato.';
  }
  hostState.revision += 1;
  hostState.lastResult = result;
  publishHostState();
});
channel.port2.start();

chat = createChatFormModule({
  id: 'workspace-interaction', storage: null,
  initialMessage: 'Questo dialogo riceve una risposta sintetica dal controller locale. Puoi usare il modulo per contribuire al progetto.',
  onAsk: text => request({ type: 'ask', text }),
  onSubmit: draft => request({ type: 'contribute', draft }),
});
chat.setActions([{ label: 'Comprendi la fonte', prompt: 'Quale fonte sostiene il punto attuale?' }]);
windowSurface = createWindowSurface({
  id: 'workspace-window', title: 'Intervento sul progetto', subtitle: hostState.object.id,
  avatar: 'UX', content: chat.element, storage: null,
  onLayoutChange() { chat.refreshLayout(); showReadback(); },
  onPresenceChange() { showReadback(); },
});
chat.element.addEventListener('input', showReadback);
byId('open-interaction').addEventListener('click', event => {
  windowSurface.open(event.currentTarget); chat.refreshLayout(); showReadback();
});
byId('source-event').addEventListener('click', () => {
  hostState.source = { id: 'reference-02', title: 'Nuovo riscontro', description: 'Un evento sintetico rende disponibile una nuova relazione da approfondire.' };
  hostState.revision += 1;
  hostState.consequence = { title: 'Nuova fonte da comprendere', description: 'Il riferimento del progetto e la tua bozza restano disponibili.' };
  hostState.lastResult = null;
  publishHostState();
  windowSurface.notify({ id: 'source-event-' + hostState.revision, title: 'Nuovo riscontro sul progetto', text: 'La fonte è cambiata; puoi continuare dal punto e dalla bozza presenti.' });
  byId('guide').textContent = 'Il nuovo riscontro aggiorna la fonte. Apri il dialogo oppure continua la bozza: un evento non deve cancellare ciò che stai preparando.';
  showReadback();
});
showReadback();
globalThis.kuxDemo = {
  medium, windowSurface, chat, readback,
  destroy() { connection.disconnect(); channel.port1.close(); channel.port2.close(); windowSurface.destroy(); chat.destroy(); medium.destroy(); },
};
