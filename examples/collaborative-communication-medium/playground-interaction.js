const playgroundCopy = /* PLAYGROUND_COPY */ null;
const playgroundCues = new Set(['edit', 'move', 'share', 'save']);
const isGuideScene = scene => playgroundCues.has(scene.guideCue);
const playgroundBar = $('#publicFirstUse');
let practiceHighlight = null;
let guidedMode = true;
let lastGuidedScene = null;

function guideSlides() {
  return state.scenes.filter(isGuideScene);
}

function clearPracticeHighlight() {
  practiceHighlight?.removeAttribute('data-guide-highlight');
  practiceHighlight = null;
}

function renderPlayground() {
  clearPracticeHighlight();
  const slides = guideSlides();
  const hasGuide = !publicMode && slides.length > 0;
  const scene = current();
  const guided = hasGuide && guidedMode && isGuideScene(scene) && !presenting;
  document.body.classList.toggle('guided-playground', guided);
  playgroundBar.dataset.cue = scene.guideCue || '';
  playgroundBar.hidden = !hasGuide || !isGuideScene(current());
  const isPractice = ['edit', 'move'].includes(scene.guideCue);
  const hint = $('#guideHint');
  hint.textContent = isPractice
    ? (readingMode ? playgroundCopy.compose : playgroundCopy.pointCard)
    : playgroundCopy[scene.guideCue] || playgroundCopy.hint;
  $('#guideExample').hidden = scene.guideCue !== 'share'
    || scene.elements.some(node => node.id === 'comparable-cases');
  const index = slides.indexOf(scene);
  $('#guideStep').textContent = index < 0 ? '' : `${playgroundCopy.stepLabel} ${index + 1} / ${slides.length}`;
  $('#guideTitle').textContent = scene.title;
  $('#guideInstruction').textContent = scene.elements.find(node => node.id === 'instructions')?.text || '';
  $('#guidePrevious').hidden = index <= 0;
  $('#guideNext').hidden = index >= slides.length - 1;
  $('#guideExplore').textContent = guidedMode ? playgroundCopy.explore : playgroundCopy.resume;
  $('#guideOptions summary').textContent = guidedMode ? playgroundCopy.explore : playgroundCopy.resume;
  for (const id of ['demoRail', 'demoTools']) $('#' + id).hidden = !hasGuide;
  if (!guided) {
    lastGuidedScene = null;
    return;
  }
  const selector = isPractice && !readingMode ? '#canvas .node[data-id="practice"]' : '#guideHint';
  const target = $(selector);
  if (target) highlight(target, false);
  if (lastGuidedScene !== scene.id) {
    $('#guideTitle').focus({preventScroll: true});
    lastGuidedScene = scene.id;
  }
}

function showPracticeTarget() {
  clearPracticeHighlight();
  const cue = current().guideCue;
  if (!playgroundCues.has(cue) || publicMode || presenting) return;
  if (readingMode && (cue === 'edit' || cue === 'move')) {
    changeView(false);
  }
  if (cue === 'share') {
    openAIShare();
    const scope = $('input[name="aiShareScope"][value="scene"]');
    scope.checked = true;
    updateAISharePreview();
    scope.focus();
    return;
  }
  if (cue === 'save') {
    exportHTML();
    return;
  }
  const node = $('#canvas .node[data-id="practice"]');
  if (node) {
    clearPracticeHighlight();
    highlight(node);
    node.focus({preventScroll: true});
  }
  else toast(playgroundCopy.missing);
}

function highlight(target, scroll = true) {
  practiceHighlight = target;
  target.setAttribute('data-guide-highlight', '');
  if (scroll) target.scrollIntoView({block: 'nearest', inline: 'nearest'});
}

function goToGuideSlide(scene) {
  if (!scene || publicMode) return;
  if (editingId) cancelDirectEdit(true);
  closeQuick();
  openPanel(null);
  guidedMode = true;
  state.activeSceneId = scene.id;
  selectedId = selectedLinkId = portPickerLinkId = null;
  render();
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
  $('#' + id).onclick = () => goToGuideSlide(guideSlides()[0]);
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
$('#guidePrevious').onclick = () => {
  const slides = guideSlides();
  goToGuideSlide(slides[slides.indexOf(current()) - 1]);
};
$('#guideNext').onclick = () => {
  const slides = guideSlides();
  goToGuideSlide(slides[slides.indexOf(current()) + 1]);
};
$('#guideExplore').onclick = () => {
  $('#guideOptions').open = false;
  guidedMode = !guidedMode;
  render();
  (guidedMode ? $('#guideTitle') : $('#guideOptions summary')).focus({preventScroll: true});
};
