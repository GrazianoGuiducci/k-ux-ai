const playgroundCopy = /* PLAYGROUND_COPY */ null;
const playgroundCues = new Set(['edit', 'move', 'share', 'save']);
const isGuideScene = scene => playgroundCues.has(scene.guideCue);
const playgroundBar = $('#publicFirstUse');
let practiceHighlight = null;

function clearPracticeHighlight() {
  practiceHighlight?.removeAttribute('data-guide-highlight');
  practiceHighlight = null;
}

function renderPlayground() {
  clearPracticeHighlight();
  const hasGuide = !publicMode && state.scenes.some(isGuideScene);
  playgroundBar.hidden = !hasGuide || !isGuideScene(current());
  $('#guideExample').hidden = current().guideCue !== 'share';
  for (const id of ['demoRail', 'demoTools']) $('#' + id).hidden = !hasGuide;
}

function showPracticeTarget() {
  clearPracticeHighlight();
  const cue = current().guideCue;
  if (!playgroundCues.has(cue) || publicMode || presenting) return;
  if (readingMode && (cue === 'edit' || cue === 'move')) {
    highlight($('#viewBtn'));
    toast(playgroundCopy.showEditor);
    return;
  }
  if (cue === 'share') {
    openPanel('tools');
    const target = $('#exportData');
    target.closest('details').open = true;
    highlight(target);
    return;
  }
  if (cue === 'save') {
    highlight($('#saveBtn'));
    return;
  }
  const node = $('#canvas .node[data-id="practice"]');
  if (node) highlight(node);
  else toast(playgroundCopy.missing);
}

function highlight(target) {
  practiceHighlight = target;
  target.setAttribute('data-guide-highlight', '');
  target.scrollIntoView({block: 'nearest', inline: 'nearest'});
}

function makeBlankSlide() {
  return {id: uid('sc'), title: playgroundCopy.blank, notes: '',
          elements: [], links: [], background: '#fffdf5'};
}

function removePlayground() {
  if (publicMode || !state.scenes.some(isGuideScene) || !confirm(playgroundCopy.confirm)) return;
  if (editingId) cancelDirectEdit(true);
  closeQuick();
  commit(() => {
    state.scenes = state.scenes.filter(scene => !isGuideScene(scene));
    if (!state.scenes.length) state.scenes.push(makeBlankSlide());
    if (!state.scenes.some(scene => scene.id === state.activeSceneId)) {
      state.activeSceneId = state.scenes[0].id;
      selectedId = selectedLinkId = portPickerLinkId = null;
    }
  });
  toast(playgroundCopy.removed);
  $('#saveBtn').focus();
}

function showExampleReturn() {
  const source = current();
  if (publicMode || source.guideCue !== 'share') return;
  const scene = publicSceneForComparison(safeClone(source));
  if (!['practice', 'outcome'].every(id => scene.elements.some(node => node.id === id))) {
    toast(playgroundCopy.missing);
    return;
  }
  if (scene.elements.some(node => node.id === 'comparable-cases')) {
    toast(playgroundCopy.alreadyApplied);
    return;
  }
  scene.elements.push({id: 'comparable-cases', type: 'card', x: 465, y: 340,
    w: 270, h: 148, fontSize: 27, text: playgroundCopy.addition,
    fill: '#fff0df', color: '#183146'});
  scene.links = scene.links.filter(link => link.id !== 'relationship');
  for (const [id, from, to] of [
    ['case-selection', 'practice', 'comparable-cases'],
    ['trial-prerequisite', 'comparable-cases', 'outcome'],
  ]) {
    scene.links.push({id: uid(id), from, to, fromAnchor: 'right', toAnchor: 'left',
      color: '#087b70', width: 3, arrow: true, heads: 'end'});
  }
  const incoming = {schema: state.schema, id: state.id, title: playgroundCopy.proposal,
    theme: state.theme, activeSceneId: scene.id, scenes: [scene]};
  openReviewIncoming(validatePortableModel(incoming));
}

for (const id of ['demoRail', 'demoTools']) {
  $('#' + id).onclick = () => {
    const scene = state.scenes.find(isGuideScene);
    if (!scene) return;
    if (editingId) cancelDirectEdit(true);
    closeQuick();
    openPanel(null);
    state.activeSceneId = scene.id;
    selectedId = selectedLinkId = portPickerLinkId = null;
    render();
    showPracticeTarget();
  };
}
for (const id of ['blankRail', 'blankTools']) {
  $('#' + id).onclick = () => {
    if (publicMode) return;
    if (editingId) cancelDirectEdit(true);
    closeQuick();
    openPanel(null);
    const scene = makeBlankSlide();
    commit(() => {
      state.scenes.push(scene);
      state.activeSceneId = scene.id;
      selectedId = selectedLinkId = portPickerLinkId = null;
    });
  };
}
$('#guideHint').onclick = showPracticeTarget;
$('#guideRemove').onclick = removePlayground;
$('#guideExample').onclick = showExampleReturn;
