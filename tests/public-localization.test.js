import assert from 'node:assert/strict';
import {localizeDocument,translateCopy} from '../tools/localize_public_griglia.mjs';
import test from 'node:test';

const entries=[{key:'card.understand',it:'Capire',en:'Understand'},
 {key:'card.open',it:'Apri scheda',en:'Open card'},
 {key:'dialog.question',it:'Scrivi una domanda',en:'Write the person’s question'}];

test('compiled literal and template copy preserve expressions, code IDs and quotes',()=>{
 const source='<html lang="en"><body><button title="Apri scheda">Capire</button><script>const id="capire";const name="Capire";const hint=`Scrivi una domanda: ${id}`;const markup=`<button>Apri scheda</button>`;</script></body></html>';
 const result=localizeDocument(source,entries);
 assert.match(result,/<button title="Open card">Understand<\/button>/);
 assert.match(result,/const id="capire"/);
 assert.match(result,/const name="Understand"/);
 assert.match(result,/Write the person’s question: \$\{id\}/);
 assert.match(result,/<button>Open card<\/button>/);
});

test('longer bindings take priority and replacements are not translated again',()=>{
 assert.equal(translateCopy('Capire e Apri scheda',entries),'Understand e Open card');
 const bindings=[{it:'Fonte',en:'Source'},{it:'Fonte e limiti',en:'Source and limits'}];
 assert.equal(translateCopy('Fonte e limiti',bindings),'Source and limits');
});
