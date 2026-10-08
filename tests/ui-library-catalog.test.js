import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';

const root = new URL('../', import.meta.url);
const read = path => readFileSync(new URL(path, root), 'utf8');
const catalog = JSON.parse(read('ui-library/catalog.v0.1.json'));

test('cabinet is explicitly source-backed, not an installed UI system', () => {
  assert.equal(catalog.schema, 'kux-ai.ui-library.source-catalog.v0.1');
  assert.equal(catalog.state, 'CANDIDATE_SOURCE_CABINET_NOT_INSTALLED');
  assert.equal(catalog.owner, 'GrazianoGuiducci/k-ux-ai');
  assert.ok(catalog.evidence.no_live_AI);
  assert.ok(catalog.evidence.no_public_site_effect);
});

test('source catalog uses pinned commits and unique identifiers', () => {
  const r = new Map(catalog.repositories.map(item => [item.id, item]));
  assert.equal(r.size, catalog.repositories.length);
  const ids = new Set();
  for (const s of catalog.sources) {
    assert.ok(!ids.has(s.id), `Duplicate source ${s.id}`);
    ids.add(s.id);
    const owner = r.get(s.repository);
    assert.ok(owner, `Missing owner ${s.repository}`);
    assert.equal(s.url, `https://github.com/${owner.full}/blob/${owner.commit}/${s.path}`);
    assert.ok(s.status);
  }
  assert.ok(catalog.sources.length >= 15);
});

test('every module refers to a reachable source, never an invented dependency', () => {
  const sources = new Set(catalog.sources.map(item => item.id));
  const ids = new Set();
  for (const m of catalog.modules) {
    assert.ok(!ids.has(m.id), `Duplicate module ${m.id}`);
    ids.add(m.id);
    assert.ok(m.references.length > 0, `No reference for ${m.id}`);
    for (const id of m.references) assert.ok(sources.has(id), `${m.id}: ${id}`);
    assert.ok(m.mustTravel.length >= 3, `${m.id} missing behavior boundary`);
    assert.ok(m.integration, `Missing integration status for ${m.id}`);
  }
  assert.ok(ids.has('assistant-presence'));
  assert.ok(ids.has('chat-form'));
  assert.ok(ids.has('window-morphology'));
});

test('the two actual standalone v3 HTML files are available in this branch', () => {
  for (const item of catalog.existing_local_experiments) {
    assert.ok(existsSync(new URL(item.path, root)), item.path);
    const s = read(item.path);
    assert.match(s, /^<!doctype html>/i);
    assert.match(s, /sourceChatSeed:/);
    assert.match(s, /liveAI\s*:\s*false/);
    assert.match(s, /situationReadback/);
    assert.match(s, /Strumenti/);
  }
});

test('the source adoption and operating contracts are present', () => {
  const adoption = read('docs/ui-library/SOURCE_ADOPTION_20261008.md');
  const contract = read('docs/ui-library/OPERATING_CONTRACT.md');
  const receipt = JSON.parse(read('labs/nautico-ui-v3/EVIDENCE.json'));
  assert.match(adoption, /lab-d-nd-site\/assets\/js\/domus-widget\.js/);
  assert.match(contract, /L'evento/);
  assert.match(contract, /Controlli/);
  assert.equal(receipt.passed, 63);
  assert.equal(receipt.total, 63);
  assert.equal(receipt.evidence_type, 'reported_prior_turn_browser_run_not_rerun_in_kuxai_repo');
});
