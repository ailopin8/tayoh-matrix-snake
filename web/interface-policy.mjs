/** Presentation decisions never mutate the authoritative simulation. */
export const LENSES=['relationships','boundary','energy','material','information'];
export const DEFAULT_CONTEXT={purpose:'Understand reciprocal viability',boundary:'The 10 × 10 × 10 environment and its two children',outside:'External causes remain unknown',question:'Which relationship is supporting viability?',objective:'understand',automatic:true,lens:'relationships'};
export function deriveNeed(s,objective='understand'){
  const systems=s.systems,children=s.agents||[],minBattery=Math.min(100,...children.map(a=>a.alive?a.battery/a.capacity*100:0));
  if(!s.alive||systems?.failed)return {mode:'review',focus:'protector',lens:'boundary',urgent:true,reason:'The system has stopped. Inspect its boundary and outcome before resetting.'};
  if(systems&&systems.integrity<50)return {mode:'stabilize',focus:'protector',lens:'boundary',urgent:true,reason:`Boundary integrity is ${systems.integrity}/100; examine protection and repair.`};
  if(systems&&!systems.healer.safe)return {mode:'stabilize',focus:'healer',lens:'material',urgent:true,reason:'Safe production is paused; inspect food deadlines and the safety condition.'};
  if(minBattery<25)return {mode:'stabilize',focus:'children',lens:'material',urgent:true,reason:'A child has less than 25% battery; inspect reachable food and competing claims.'};
  if((systems?.pressure||0)>=5)return {mode:'investigate',focus:'protector',lens:'boundary',urgent:false,reason:'External pressure is elevated. Its cause is still uncertain.'};
  if(objective==='experiment'||systems?.pending?.length)return {mode:'experiment',focus:'relationships',lens:'information',urgent:false,reason:'Trace an explicitly mapped input through its queued and applied outcome.'};
  if(objective==='maintain')return {mode:'maintain',focus:'relationships',lens:'relationships',urgent:false,reason:'Compare contributions, reserves and needs before intervening.'};
  return {mode:'observe',focus:'relationships',lens:'relationships',urgent:false,reason:'No immediate viability threshold is breached. Explore the reciprocal relationships.'};
}
export function updatePresentation(previous,s,context){
  const next=deriveNeed(s,context.objective),tick=s.tick;
  // Urgency enters immediately; nonurgent changes need five logical ticks.
  const switchMode=!previous||next.urgent||(tick-Math.max(previous.since,previous.lastUrgent??previous.since)>=5);
  const chosen=switchMode?{...next,since:previous?.mode===next.mode?previous.since:tick,lastUrgent:next.urgent?tick:previous?.lastUrgent}:previous;
  const reason=!switchMode&&previous.mode!==next.mode?'Keeping the lens stable briefly. '+next.reason:chosen.reason;
  return {...chosen,urgent:next.urgent,alert:next.urgent?next.reason:null,
          lens:context.automatic?chosen.lens:context.lens,
          reason:context.automatic?reason:`Lens pinned by you. ${next.reason}`};
}
export function flowSummary(s){
 const x=s.systems;if(!x)return [];
 return [
  {from:'Protector',to:'Healer',kind:'condition',value:x.healer.safe?'safe production permitted':'production paused'},
  {from:'Healer',to:'Protector',kind:'material intake',value:`${x.protector.consumed} expired food consumed`},
  {from:'Healer',to:'Children',kind:'material intake',value:`${s.agents.reduce((n,a)=>n+a.score,0)} food consumed`},
  {from:'Children',to:'Healer',kind:'energy',value:`${x.healer.pollination} GU returned`},
  {from:'Children',to:'Protector',kind:'conditional energy',value:'up to 1 GU per healthy-food intake when its model indicates need'},
  {from:'Children',to:'Information',kind:'signal',value:'visits leave decaying trails'}
 ];
}
export function previewInput(input){
 if(!input.label?.trim()||input.label.length>120)throw Error('Give the observation a label of 1–120 characters.');
 if(!['stress','support','information'].includes(input.kind)||!Number.isInteger(input.value)||input.value<0||input.value>10)throw Error('Choose a channel and an integer intensity from 0 to 10.');
 if(input.position&&(!Array.isArray(input.position)||input.position.length!==3||input.position.some(v=>!Number.isInteger(v)||v<0||v>9)))throw Error('Supply all three integer coordinates from 0 to 9.');
 return {input:{label:input.label,kind:input.kind,value:input.value,...(input.position?{position:input.position.slice()}: {})},effect:input.kind==='stress'?`Increase pressure by up to ${input.value}; the next random damage remains uncertain.`:input.kind==='support'?`Supply ${8*input.value} GU to the protector and reduce pressure by up to ${input.value}.`:`Add ${input.value} novelty units and a bounded signal; food phenotype still depends on conditions.`};
}
