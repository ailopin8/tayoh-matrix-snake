/** Plain-language views of existing authoritative observations; no simulation mutation. */
export const ROLES=['protector','healer','child_A','child_B'];
export function explainRole(s,key){
 const names={protector:'Boundary',healer:'Food producer',child_A:'Snake A',child_B:'Snake B'},name=names[key];
 const purpose=s.purpose?.roles.find(r=>r.role===key),models=s.systems?.models?.[key]||{};
 const model=Object.entries(models).map(([role,m])=>`${names[role]||role}: ${m.estimate}/100`).join(' · ');
 const relations={protector:'Protects the producer and snakes. Uneaten food supplies its repair reserve.',healer:'Makes timed food when conditions are safe. Snakes return energy when they eat.',child_A:'Seeks food and avoids Snake B when autonomy is on. Eating returns energy to the producer.',child_B:'Seeks food and avoids Snake A. Both snakes compete for the same resources.'};
 return {name,relationship:relations[key],observed:purpose?.observed||'Waiting for observations',model:model||'Waiting for model estimates',self:models[key]?.estimate,environment:models.protector?.estimate,rule:purpose?.rules||'',tick:s.tick};
}
export function installSimpleInterface(actions){
 const $=id=>document.getElementById(id),main=document.querySelector('main'),sections=[...main.children];
 const advanced=document.createElement('details');advanced.id='advanced';advanced.innerHTML='<summary>More tools & detailed evidence</summary><div class="advanced-content"></div>';
 const content=advanced.lastElementChild;
 const spatial=$('space').closest('section');
 // Keep all existing tools and their IDs available, but disclose them only on request.
 for(const section of sections)if(section!==spatial)content.append(section);
 main.replaceChildren(spatial,advanced);spatial.className='matrix-stage wide';spatial.querySelector('h2').textContent='Explore the matrix';
 const viewBar=document.createElement('div');viewBar.className='simple-actions';
 for(const [label,fn] of [['Home view',actions.home],['Turn left',()=>actions.turn(-1)],['Turn right',()=>actions.turn(1)],['Smaller',()=>actions.size(.8)],['Larger',()=>actions.size(1.25)]]){const b=document.createElement('button');b.textContent=label;b.onclick=fn;viewBar.append(b);}spatial.insertBefore(viewBar,$('space'));const legend=document.createElement('p');legend.className='matrix-key';legend.textContent='Green: Snake A · Blue: Snake B · Gold: food · Drag to orbit · Scroll to zoom';spatial.insertBefore(legend,$('space')); 
 const detail=document.createElement('details');detail.innerHTML='<summary>Manual steering & numbers</summary>';for(const el of [...spatial.children])if(!['H2'].includes(el.tagName)&&el!==viewBar&&el.id!=='space'&&el.id!=='expandSpace'&&el!==legend)detail.append(el);spatial.append(detail);
 const introduction=document.createElement('p');introduction.className='simple-intro';introduction.textContent='A living system in 1,000 cells. The boundary protects, the producer makes food, and two snakes seek it. Each follows its own rules and updates estimates of itself and the other roles.';main.before(introduction);
 const console=document.createElement('section');console.className='wide simple-console';console.innerHTML='<h2>What is happening?</h2><p class="relationship-path">Boundary → safe production → food → snakes → returned energy<br>Uneaten food → boundary repair reserve</p><p id="simpleNow" role="status"></p><div class="role-buttons" aria-label="Explore a component"></div><h3 id="simpleRole"></h3><p id="simpleRelation"></p><p id="simpleObserved"></p><details><summary>What does this part believe?</summary><p id="simpleModel"></p><p>These are smoothed estimates of role viability. Its environment is represented by the other roles; each also carries a bounded model of their estimates. Estimates can lag behind reality.</p></details>';
 main.insertBefore(console,advanced);
 for(const key of ROLES){const b=document.createElement('button');b.textContent={protector:'Boundary',healer:'Food producer',child_A:'Snake A',child_B:'Snake B'}[key];b.dataset.role=key;b.onclick=()=>actions.select(key);console.querySelector('.role-buttons').append(b);}
 const input=document.createElement('section');input.className='wide simple-input';input.innerHTML='<h2>Try one change</h2><p>Choose an input, review its effect, then confirm. Nothing is applied until you confirm and the simulation advances.</p><div class="simple-actions" id="simpleInputs"></div>';
 for(const [label,kind] of [['Add support','support'],['Add pressure','stress'],['Add a signal','information']]){const b=document.createElement('button');b.textContent=label;b.onclick=()=>actions.input({label,kind,value:2});input.querySelector('#simpleInputs').append(b);}
 for(const id of ['inputPreview','applyInput','cancelInput','inputStatus','comparison'])input.append($(id));main.insertBefore(input,advanced);
 $('applyInput').textContent='Confirm input';$('cancelInput').textContent='Cancel';
 const extras=document.createElement('details');extras.innerHTML='<summary>Session options</summary>';const nav=document.querySelector('nav');for(const el of [...nav.children])if(!['run','step','vr'].includes(el.id))extras.append(el);nav.append(extras);
 $('attention').hidden=true;document.querySelector('header p').textContent='Observe · explore relationships · try a change';document.querySelector('header small').textContent='TAYOH / SIMPLE SYSTEMS LAB';
 return {update(s,p,key){const r=explainRole(s,key);$('simpleNow').textContent=p?.alert||`Tick ${s.tick} · ${s.agents.filter(a=>a.alive).length} snakes active · boundary ${s.systems?.integrity??'?'}/100 · ${s.material.reduce((a,b)=>a+b,0)} food available`;$('simpleRole').textContent=r.name;$('simpleRelation').textContent=r.relationship;$('simpleObserved').textContent=r.observed;$('simpleModel').textContent=`At tick ${r.tick}, ${r.name} estimates: ${r.model}.`;for(const b of console.querySelectorAll('[data-role]'))b.setAttribute('aria-pressed',String(b.dataset.role===key));}};
}
