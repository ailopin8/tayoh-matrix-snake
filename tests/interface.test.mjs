import test from 'node:test';
import assert from 'node:assert/strict';
import {DEFAULT_CONTEXT,deriveNeed,updatePresentation,previewInput,flowSummary} from '../web/interface-policy.mjs';
const healthy=()=>({tick:0,alive:true,agents:[{alive:true,battery:80,capacity:100,score:3},{alive:true,battery:70,capacity:100,score:4}],systems:{failed:false,integrity:100,pressure:0,pending:[],protector:{consumed:2},healer:{safe:true,pollination:14}}});
test('purpose changes attention, not simulation',()=>{const s=healthy(),before=JSON.stringify(s);assert.equal(deriveNeed(s,'experiment').mode,'experiment');assert.equal(JSON.stringify(s),before);});
test('boundary need takes priority over experiment',()=>{const s=healthy();s.systems.integrity=30;assert.equal(deriveNeed(s,'experiment').lens,'boundary');assert.equal(deriveNeed(s).urgent,true);});
test('unsafe healer brings deadlines into view',()=>{const s=healthy();s.systems.healer.safe=false;assert.equal(deriveNeed(s).focus,'healer');assert.equal(deriveNeed(s).lens,'material');});
test('child low battery changes relevant information',()=>{const s=healthy();s.agents[1].battery=10;assert.equal(deriveNeed(s).focus,'children');});
test('pressure remains uncertain',()=>{const s=healthy();s.systems.pressure=8;assert.equal(deriveNeed(s).mode,'investigate');assert.match(deriveNeed(s).reason,/uncertain/);});
test('manual lens preserves critical warning',()=>{const s=healthy();s.systems.integrity=20;const p=updatePresentation(null,s,{...DEFAULT_CONTEXT,automatic:false,lens:'energy'});assert.equal(p.lens,'energy');assert.equal(p.urgent,true);assert.match(p.reason,/pinned/);});
test('recovery hold prevents lens chatter',()=>{const s=healthy();s.systems.integrity=20;let p=updatePresentation(null,s,DEFAULT_CONTEXT);s.tick=1;p=updatePresentation(p,s,DEFAULT_CONTEXT);s.systems.integrity=100;s.tick=2;p=updatePresentation(p,s,DEFAULT_CONTEXT);assert.equal(p.lens,'boundary');assert.equal(p.urgent,false);s.tick=6;p=updatePresentation(p,s,DEFAULT_CONTEXT);assert.equal(p.lens,'relationships');});
test('failure enters inspectable review',()=>{const s=healthy();s.alive=false;assert.equal(deriveNeed(s).mode,'review');});
test('preview quantifies only its encoded intervention',()=>{const p=previewInput({label:'support',kind:'support',value:2});assert.match(p.effect,/16 GU/);assert.deepEqual(p.input,{label:'support',kind:'support',value:2});});
test('incomplete coordinates and invalid intensity rejected',()=>{assert.throws(()=>previewInput({label:'x',kind:'stress',value:2,position:[0,null,1]}));assert.throws(()=>previewInput({label:'x',kind:'stress',value:11}));});
test('explicit coordinates copied, not aliased',()=>{const position=[1,2,3],p=previewInput({label:'x',kind:'information',value:2,position});position[0]=9;assert.equal(p.input.position[0],1);});
test('relational view distinguishes conditions from flows',()=>{const flows=flowSummary(healthy());assert.equal(flows.length,6);assert.equal(flows[0].kind,'condition');assert.match(flows[3].value,/14 GU/);});

test('purpose-gap evidence directs attention without overriding urgent viability',()=>{
 const s={tick:10,alive:true,agents:[{alive:true,battery:80,capacity:100}],purpose:{roles:[{gap:true}],attention:{focus:'child_A',lens:'material',reason:'No intake and falling battery'}}};
 assert.equal(deriveNeed(s).mode,'investigate');assert.equal(deriveNeed(s).focus,'children');
 s.agents[0].battery=10;assert.equal(deriveNeed(s).urgent,true);
});
