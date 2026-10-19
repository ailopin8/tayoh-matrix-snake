import * as THREE from './vendor/three.module.js';
/** Small, fixed world-anchored console. No third-party component code copied. */
export class SpatialInterface{
 constructor(scene,parent,actions){
  this.actions=actions;this.root=new THREE.Group();parent.add(this.root);this.hitTargets=[];this.ray=new THREE.Raycaster();this.rotation=new THREE.Matrix4();this.labels=[];this.signature='';
  this.banner=this.panel(1.65,.25,[0,.88,0]);
  this.roles=[this.panel(.72,.3,[-.93,.36,0]),this.panel(.72,.3,[-.93,-.1,0]),this.panel(.72,.3,[.93,-.1,0])];
  this.roleNames=['Protector','Healer','Children'];
  this.lines=[];
  for(const [a,b] of [[[-.58,.32,0],[-.58,-.05,0]],[[-.55,-.18,0],[.55,-.18,0]],[[.55,.05,0],[-.55,.42,0]]]){
   const d=new THREE.Vector3(...b).sub(new THREE.Vector3(...a));const arrow=new THREE.ArrowHelper(d.clone().normalize(),new THREE.Vector3(...a),d.length(),0x718d99,.035,.025);this.root.add(arrow);this.lines.push(arrow);
  }
  this.buttons=[];
  for(let i=0;i<6;i++){
   const button=this.panel(.31,.16,[-.85+i*.34,-.78,0]);button.mesh.userData.action=i;this.hitTargets.push(button.mesh);this.buttons.push(button);
  }
  this.controllers=[];
  for(let i=0;i<2;i++){
   const c=actions.renderer.xr.getController(i),line=new THREE.Line(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(),new THREE.Vector3(0,0,-1)]),new THREE.LineBasicMaterial({color:0xa6e3d0}));line.scale.z=4;c.add(line);scene.add(c);this.controllers.push(c);
   c.addEventListener('selectstart',()=>this.select(c));
  }
 }
 panel(width,height,pos){
  const canvas=document.createElement('canvas');canvas.width=1024;canvas.height=360;
  const texture=new THREE.CanvasTexture(canvas);texture.colorSpace=THREE.SRGBColorSpace;
  const mesh=new THREE.Mesh(new THREE.PlaneGeometry(width,height),new THREE.MeshBasicMaterial({map:texture,transparent:false,side:THREE.DoubleSide}));mesh.position.set(...pos);this.root.add(mesh);
  return {canvas,texture,mesh};
 }
 text(panel,lines,accent='#7cebc2',active=false){
  const ctx=panel.canvas.getContext('2d');ctx.fillStyle=active?'#173c48':'#10212b';ctx.fillRect(0,0,1024,360);ctx.strokeStyle=accent;ctx.lineWidth=12;ctx.strokeRect(6,6,1012,348);
  lines.slice(0,4).forEach((line,i)=>{ctx.fillStyle=i===0?accent:'#e6f4f3';ctx.font=`${i===0?'bold ':''}${lines.length<=2?65:49}px sans-serif`;ctx.fillText(String(line).slice(0,58),28,78+i*77,970);});panel.texture.needsUpdate=true;
 }
 update(s,p,context,running,draft){
  const signature=JSON.stringify([s.tick,p.mode,p.lens,p.focus,context.purpose,context.inspection,running,draft?.effect,draft?.spatialSupport]);if(signature===this.signature)return;this.signature=signature;
  this.text(this.banner,[`${p.mode.toUpperCase()} / ${p.lens}`,context.purpose,draft?draft.effect:p.alert||context.inspection||p.reason],p.urgent?'#ffad83':'#7cebc2');
  const x=s.systems;
  const values=[[`Protector ${x?.integrity??'?'} / 100`,`Repair reserve ${x?.protector.reserve??'?'}`,`External pressure ${x?.pressure??'?'} / 10`],[`Healer ${x?.healer.vitality??'?'} / 100`,x?.healer.safe?'Safe production':'Production paused',`Expired food → protector ${x?.protector.consumed??0}`],[`Children A / B`,...s.agents.map(a=>`${a.id}: food ${a.score} · battery ${a.battery}/${a.capacity}`)]];
  values.forEach((v,i)=>this.text(this.roles[i],v,p.focus===this.roleNames[i].toLowerCase()||p.focus==='relationships'?'#7cebc2':'#829fa8',p.focus===this.roleNames[i].toLowerCase()));
  this.lines.forEach(line=>line.visible=p.lens==='relationships');
  const names=[running?'Pause':'Run','Step','Next lens',draft?.spatialSupport?'Confirm +2':'Support +2','Cancel draft',this.actions.renderer.xr.isPresenting?'Exit VR':'Headset only'];
  names.forEach((name,i)=>this.text(this.buttons[i],[name],i===3&&draft?'#ffd08a':'#c8e9e2'));
 }
 select(c){
  c.updateWorldMatrix(true,false);this.rotation.extractRotation(c.matrixWorld);this.ray.ray.origin.setFromMatrixPosition(c.matrixWorld);this.ray.ray.direction.set(0,0,-1).applyMatrix4(this.rotation);
  const hit=this.ray.intersectObjects(this.hitTargets,false)[0];if(hit)this.activate(hit.object.userData.action);else this.actions.inspect?.(this.ray);
 }
 activate(i){const a=this.actions;[a.toggle,a.step,a.lens,a.support,a.cancel,a.exit][i]?.();}
}
