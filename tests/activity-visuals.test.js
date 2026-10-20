import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const scope = {};
vm.runInNewContext(fs.readFileSync(new URL('../src/ui/activity-visuals.js', import.meta.url), 'utf8'), scope);
const {activityState, workspaceEmpty, install} = scope.KUXActivityVisuals;

test('presence follows the selected context, actual focus, minimization and removal', () => {
  const state = {activeContext:'yard', focused:'other', events:[], panels:[
    {id:'other', intent:'fare', context:'boat'},
    {id:'yard-card', intent:'fare', context:'yard', minimized:true}
  ]};
  assert.equal(activityState(state, 'fare').presence, 'minimized');
  state.panels[1].minimized = false;
  assert.equal(activityState(state, 'fare').presence, 'open');
  state.focused = 'yard-card';
  assert.equal(activityState(state, 'fare').presence, 'focused');
  state.panels.pop();
  assert.equal(activityState(state, 'fare').presence, 'closed');
  assert.equal(activityState(state, 'fare', 'boat').presence, 'open');
});

test('notification is independent of presence and retires when examined', () => {
  const state = {activeContext:'yard', focused:null, panels:[], events:[
    {intent:'controllare', context:'boat', status:'pending'},
    {intent:'fare', context:'yard', status:'pending'}
  ]};
  assert.equal(activityState(state, 'controllare').notification, false);
  assert.equal(activityState(state, 'fare').presence, 'closed');
  assert.equal(activityState(state, 'fare').notification, true);
  state.events[1].status = 'examined';
  assert.equal(activityState(state, 'fare').notification, false);
});

test('receivers without a visual profile retain their native rendering', () => {
  assert.equal(install({state:{}}), null);
});

test('empty canvas follows visible work, not retained or minimized cards', () => {
  const state = {activeContext:'yard', panels:[
    {context:'boat', minimized:false}, {context:'yard', minimized:true}
  ]};
  assert.equal(workspaceEmpty(state), true);
  state.panels[1].minimized = false;
  assert.equal(workspaceEmpty(state), false);
  state.activeContext = 'suppliers';
  assert.equal(workspaceEmpty(state), true);
  state.panels = [];
  assert.equal(workspaceEmpty(state), true);
});
