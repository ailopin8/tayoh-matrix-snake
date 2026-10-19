import test from 'node:test';
import assert from 'node:assert/strict';
import {explainRole,ROLES} from '../web/simple-interface.mjs';
test('plain model view reports actual self and boundary estimates without mutating state',()=>{const s={tick:8,systems:{models:{child_A:{child_A:{estimate:61},protector:{estimate:89}}}},purpose:{roles:[{role:'child_A',observed:'Consumed 2 food',rules:'Forage'}]}};const before=JSON.stringify(s);const r=explainRole(s,'child_A');assert.equal(r.self,61);assert.equal(r.environment,89);assert.match(r.model,/Snake A: 61/);assert.equal(r.observed,'Consumed 2 food');assert.equal(JSON.stringify(s),before);});
test('all roles have relationships and an honest no-data model state',()=>{for(const key of ROLES){const r=explainRole({tick:0},key);assert.ok(r.relationship);assert.equal(r.model,'Waiting for model estimates');assert.equal(r.self,undefined);}});
