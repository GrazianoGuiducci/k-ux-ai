export const initialState = {
  caseId: 'stern-access',
  question: 'Un accesso a poppa più agevole',
  intent: 'Salire a bordo con più continuità, mantenendo riconoscibili i passaggi di progetto e uso.',
  view: 'overview',
  selected: null,
  supplyCheck: false,
  lastChange: 'La domanda apre un campo di progetto.',
  phases: [
    { id: 'design', label: 'Progetto', detail: 'Confrontare geometria e movimento di accesso.' },
    { id: 'build', label: 'Costruzione', detail: 'Rendere presenti integrazione e verifiche della proposta.' },
    { id: 'use', label: 'Uso a bordo', detail: 'Raccogliere esperienza e conseguenze per il progetto.' },
    { id: 'return', label: 'Ritorno', detail: 'Lasciare che il riscontro faccia evolvere il sapere.' },
  ],
  options: [
    { id: 'A', label: 'Passaggio continuo', detail: 'Una transizione più graduale fra banchina e bordo.', state: 'Da esplorare' },
    { id: 'B', label: 'Elemento mobile', detail: 'Un elemento che accompagna la salita e si ritrae durante la navigazione.', state: 'Da esplorare' },
  ],
};
