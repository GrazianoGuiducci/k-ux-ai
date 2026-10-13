import { createMedium } from '../medium.js';

// A kernel-owned context supplies meaning; this surface supplies interaction.
// The receiver alone implements actions. Local notes are not shared perception.
export function createKernelGrid({ host, context, locale = 'it', onAction = async () => ({ ok: false }) }) {
  const text = value => typeof value === 'string' ? value : value[locale] || value.it;
  const en = locale === 'en';
  const word = (name, fallback) => text(context.labels?.[name] || fallback);
  const key = `kux:kernel-grid:${context.id}:v1`;
  const element = (tag, className, content) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (content) node.textContent = content;
    return node;
  };
  let notes = [];
  try {
    const stored = JSON.parse(localStorage.getItem(key) || '[]');
    if (Array.isArray(stored)) notes = stored.filter(note => note &&
      typeof note.cardId === 'string' && note.cardId.length <= 96 &&
      typeof note.text === 'string' && note.text.length <= 4000);
  } catch { /* A missing local store does not remove the guide. */ }
  const root = element('section', 'kux-kernel-grid');
  root.setAttribute('aria-label', text(context.title));
  const heading = element('h2', '', text(context.title));
  const premise = element('p', 'kux-kernel-grid-premise', text(context.premise));
  const board = element('div', 'kux-kernel-grid-cards');
  const detail = element('section', 'kux-kernel-grid-detail');
  detail.setAttribute('aria-live', 'polite');
  const title = element('h3');
  const body = element('p');
  const action = element('button', 'kux-kernel-grid-action');
  action.type = 'button';
  const source = element('a', 'kux-kernel-grid-source', word('guide', en ? 'Read the kernel’s guide ↗' : 'La guida del kernel ↗'));
  source.href = context.guide;
  source.target = '_blank'; source.rel = 'noreferrer';
  const memory = element('div', 'kux-kernel-grid-memory');
  memory.dataset.privateContext = 'true';
  const label = element('label', '', word('note', en ? 'A question or something to remember about this card' : 'Una domanda o qualcosa da ricordare su questa scheda'));
  const draft = element('textarea');
  draft.maxLength = 4000; draft.rows = 3;
  label.append(draft);
  const save = element('button', '', word('save', en ? 'Save the contribution' : 'Conserva il contributo'));
  save.type = 'button';
  const exportButton = element('button', '', word('export', en ? 'Export these notes' : 'Esporta queste note'));
  exportButton.type = 'button';
  const count = element('span', 'kux-kernel-grid-note-count');
  const remembered = element('details', 'kux-kernel-grid-remembered');
  remembered.append(element('summary', '', word('remembered', en ? 'Contributions retained for this card' : 'Contributi conservati in questa scheda')));
  const recalled = element('div'); remembered.append(recalled);
  const status = element('p', 'kux-kernel-grid-status');
  status.setAttribute('role', 'status');
  memory.append(label, save, exportButton, count, remembered);
  detail.append(title, body, action, source, memory, status);
  const scope = element('p', 'kux-kernel-grid-scope', word('scope', en
    ? 'The cards describe the kernel’s competences and first activities. Here, contributions stay in this browser or in the exported file. A connected AI environment can use them to continue the work and improve the method.'
    : 'Le schede descrivono competenze e prime attività del kernel. Qui i contributi restano in questo browser o nel file esportato. Un ambiente AI collegato può usarli per continuare il lavoro e migliorare il metodo.'));
  root.append(heading, premise, board, detail, scope);
  host.append(root);
  const buttons = new Map();
  const drafts = new Map();
  let sequence = 0, medium;
  const viewKey = `${key}:view`;
  let previousCard = context.cards[0].id;
  try {
    const prior = localStorage.getItem(viewKey);
    if (context.cards.some(card => card.id === prior)) previousCard = prior;
  } catch { /* The first-use guide remains available. */ }
  let actionRun = 0;
  const initial = { source: context.source, contextId: context.id,
    subject: context.subject || '', object: context.object || '', case: context.case || '',
    cardId: previousCard, contributionCount: notes.length, lastConfirmedTarget: '' };
  function publish(change) {
    medium.receive({ id: `kernel-grid-${++sequence}`, state: { ...medium.snapshot(), ...change } });
  }
  for (const card of context.cards) {
    const button = element('button', 'kux-kernel-grid-card');
    button.type = 'button';
    button.id = `${context.id}-${card.id}`;
    button.dataset.cardId = card.id;
    button.append(element('strong', '', text(card.title)), element('span', '', text(card.short)));
    button.addEventListener('click', () => medium.dispatch({ type: 'select-card', cardId: card.id }));
    board.append(button); buttons.set(card.id, button);
  }
  function render(state) {
    const card = context.cards.find(item => item.id === state.cardId);
    if (previousCard !== state.cardId) {
      drafts.set(previousCard, draft.value);
      draft.value = drafts.get(state.cardId) || '';
      previousCard = state.cardId;
    }
    for (const [id, button] of buttons) button.setAttribute('aria-pressed', String(id === state.cardId));
    detail.dataset.cardId = state.cardId;
    detail.dataset.agentMarker = `${context.id}/${state.cardId}`;
    title.textContent = text(card.title);
    body.textContent = text(card.body);
    source.href = card.guide || context.guide;
    action.hidden = !card.action;
    action.textContent = card.action ? text(card.action.label) : '';
    const one = state.contributionCount === 1;
    count.textContent = word(one ? 'countOne' : 'countMany', en
      ? `{count} saved contribution${one ? '' : 's'}`
      : `{count} contribut${one ? 'o conservato' : 'i conservati'}`).replace('{count}', state.contributionCount);
    recalled.replaceChildren();
    for (const note of notes.filter(item => item.cardId === state.cardId).slice(-10)) {
      const area = element('textarea'); area.readOnly = true; area.rows = 2;
      area.value = note.text;
      area.setAttribute('aria-label', word('retained', en ? 'Retained contribution' : 'Contributo conservato'));
      recalled.append(area);
    }
    root.dataset.lastConfirmedTarget = state.lastConfirmedTarget;
  }
  medium = createMedium({ state: initial, render, async onAction(request) {
    const card = context.cards.find(item => item.id === request.cardId);
    if (!card) return { ok: false, reason: 'unknown-card' };
    if (request.type === 'select-card') {
      actionRun++; status.textContent = ''; action.disabled = false;
      try { localStorage.setItem(viewKey, card.id); } catch { /* Session continuation still works. */ }
      publish({ cardId: card.id }); return { ok: true };
    }
    if (request.type !== 'use-card' || !card.action) return { ok: false, reason: 'unknown-action' };
    const run = ++actionRun;
    action.disabled = true;
    status.textContent = word('opening', en ? 'Opening the selected view…' : 'Apertura della vista scelta…');
    let result;
    try { result = await onAction({ ...card.action, cardId: card.id, contextId: context.id }); }
    catch { result = { ok: false }; }
    if (run !== actionRun) return { ok: false, reason: 'superseded' };
    action.disabled = false;
    status.textContent = result?.ok
      ? word('opened', en ? 'The view has been opened.' : 'La vista è stata aperta.')
      : word('unavailable', en ? 'This view is not available here yet.' : 'Questa vista qui non è ancora disponibile.');
    if (result?.ok) publish({ lastConfirmedTarget: card.action.target });
    return result;
  } });
  action.addEventListener('click', () => medium.dispatch({ type: 'use-card', cardId: medium.snapshot().cardId }));
  save.addEventListener('click', () => {
    if (!draft.value.trim()) return;
    notes.push({ cardId: medium.snapshot().cardId, text: draft.value.trim(),
      context: { id: context.id, subject: context.subject || '', object: context.object || '', case: context.case || '' },
      kind: 'human_contribution', source: context.source, createdAt: new Date().toISOString() });
    let persisted = false;
    try { localStorage.setItem(key, JSON.stringify(notes)); persisted = true; } catch { /* Export remains available. */ }
    publish({ contributionCount: notes.length });
    status.textContent = persisted
      ? word('saved', en ? 'Contribution saved in this browser.' : 'Contributo conservato in questo browser.')
      : word('sessionOnly', en ? 'Contribution kept in this session. Export it to retain it.' : 'Contributo conservato nella sessione. Esportalo per mantenerlo.');
  });
  exportButton.addEventListener('click', () => {
    const blob = new Blob([JSON.stringify({ schema: 'kux.context-contributions.v1',
      contextId: context.id, source: context.source, notes }, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = element('a'); link.href = url; link.download = `${context.id}-contributi.json`;
    link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  return { snapshot: () => medium.snapshot(),
    select: cardId => medium.dispatch({ type: 'select-card', cardId }),
    destroy() { medium.destroy(); root.remove(); } };
}
