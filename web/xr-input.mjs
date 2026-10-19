import * as THREE from './vendor/three.module.js';
export const deadzone=v=>Number.isFinite(v)&&Math.abs(v)>.18?Math.sign(v)*(Math.abs(v)-.18)/.82:0;
export const clampScale=v=>Math.max(.25,Math.min(4,v));
export class XRControls {
 constructor(world,actions){this.world=world;this.actions=actions;this.previous=new Map();this.grab=null;this.vertical=false;this.last=0;this.message='A: Run / pause · Y: controls';}
 reset(){this.previous.clear();this.grab=null;this.last=0;}
 home(){this.world.position.set(0,1.3,-2);this.world.quaternion.identity();this.world.scale.setScalar(1);this.grab=null;this.message='View restored · simulation unchanged';}
 update(sources,time){
  const dt=this.last?Math.min(.05,Math.max(0,(time-this.last)/1000)):0;this.last=time;
  const present=new Set(sources.map(s=>s.id));for(const id of this.previous.keys())if(!present.has(id))this.previous.delete(id);
  const grips=[];
  for(const s of sources){
   if(s.mapping!=='xr-standard')continue;
   const b=s.buttons.map(b=>!!(b?.pressed||b?.value>.7)),prev=this.previous.get(s.id);
   const edge=i=>prev&&!prev[i]&&b[i];
   if(s.quest){if(edge(4)){const a=s.hand==='right'?'toggle':'lens';this.actions[a]?.();this.message=s.hand==='right'?'A: Run / pause':'X: Next lens';}if(edge(5)){this.actions[s.hand==='right'?'step':'help']?.();this.message=s.hand==='right'?'B: Pause and step':'Y: Toggle controls';}}
   if(edge(3)){if(s.hand==='right')this.home();else{this.vertical=!this.vertical;this.message=this.vertical?'Left stick: sideways / up-down':'Left stick: sideways / forward-back';}}
   this.previous.set(s.id,b);
   if(b[1]&&s.pose)grips.push(s);
   const x=deadzone(s.axes[2]),y=deadzone(s.axes[3]);
   if(!b[1]){
    if(s.hand==='left'){this.world.position.x+=x*dt*.7;if(this.vertical)this.world.position.y-=y*dt*.7;else this.world.position.z+=y*dt*.7;}
    if(s.hand==='right'){if(b[0]){this.world.scale.setScalar(clampScale(this.world.scale.x*Math.exp(-y*dt)));this.world.rotateZ(-x*dt);}else{this.world.rotateOnWorldAxis(new THREE.Vector3(0,1,0),-x*dt*1.3);this.world.rotateX(-y*dt*1.3);}}
   }
  }
  // Rebase whenever the tracked grip set changes; no jumps on release or tracking loss.
  const key=grips.map(g=>g.id);
  if(!grips.length)this.grab=null;
  else if(!this.grab||this.grab.key.length!==key.length||this.grab.key.some((id,i)=>id!==key[i])){
   this.grab={key,position:this.world.position.clone(),q:this.world.quaternion.clone(),scale:this.world.scale.x,poses:grips.map(g=>g.pose.clone())};
  }else{
   const a=this.grab;
   if(grips.length===1){const delta=grips[0].pose.clone().multiply(a.poses[0].clone().invert());this.world.position.copy(a.position).applyMatrix4(delta);const q=new THREE.Quaternion().setFromRotationMatrix(delta);this.world.quaternion.copy(q.multiply(a.q));}
   else{const startA=new THREE.Vector3().setFromMatrixPosition(a.poses[0]),startB=new THREE.Vector3().setFromMatrixPosition(a.poses[1]),nowA=new THREE.Vector3().setFromMatrixPosition(grips[0].pose),nowB=new THREE.Vector3().setFromMatrixPosition(grips[1].pose),v=startB.clone().sub(startA),w=nowB.clone().sub(nowA);if(v.length()>.05&&w.length()>.05){const scale=clampScale(a.scale*w.length()/v.length()),rotation=new THREE.Quaternion().setFromUnitVectors(v.normalize(),w.normalize());this.world.scale.setScalar(scale);this.world.quaternion.copy(rotation.clone().multiply(a.q));this.world.position.copy(a.position).sub(startA.add(startB).multiplyScalar(.5)).multiplyScalar(scale/a.scale).applyQuaternion(rotation).add(nowA.add(nowB).multiplyScalar(.5));}}
  }
  this.world.position.x=THREE.MathUtils.clamp(this.world.position.x,-5,5);this.world.position.y=THREE.MathUtils.clamp(this.world.position.y,-2,5);this.world.position.z=THREE.MathUtils.clamp(this.world.position.z,-8,2);
 }
}
export function sampleInputs(session,frame,space){return Array.from(session.inputSources).filter(s=>s.handedness==='left'||s.handedness==='right').map(s=>({id:s,hand:s.handedness,mapping:s.gamepad?.mapping,quest:s.profiles?.some(p=>/^(meta-quest-touch|oculus-touch)/.test(p)),buttons:Array.from(s.gamepad?.buttons||[]),axes:Array.from(s.gamepad?.axes||[]),pose:(()=>{const p=s.gripSpace?frame.getPose(s.gripSpace,space):null;return p?new THREE.Matrix4().fromArray(p.transform.matrix):null;})()}));}
