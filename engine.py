"""Integer, fixed-tick, authoritative TAYOH simulation. Python 3.10+."""
from purpose import PurposeObserver
import copy
import hashlib
import json
import random
from collections import deque
from contextlib import contextmanager
from resources import CATALOG
from systems import Systems

N = 10
DIRECTIONS = {'+x': (1,0,0), '-x': (-1,0,0), '+y': (0,1,0), '-y': (0,-1,0), '+z': (0,0,1), '-z': (0,0,-1)}
PURPOSES = ('energy', 'material', 'information', 'snake')
def index(p):
    return p[0] + 10*p[1] + 100*p[2]
def inside(p):
    return all(0 <= v < N for v in p)
def fold(p):
    """Explicit many-to-one feature map; not a physical paper fold."""
    x,y = p
    return (max(abs(x-4.5), abs(y-4.5)), 0.0)
def boundary(p, radius=2.5):
    return fold(p)[0] <= radius

AGENT_FIELDS = ('snake','battery','heat','score','alive','direction','effect','effect_until',
                'models','buffs','visits','resource_memory','decision','events','opponent_model')

class Snake:
    def __init__(self, label, color, body, direction):
        self.label=label;self.color=color;self.snake=body;self.direction=direction
        self.battery=60;self.heat=0;self.score=0;self.alive=True
        self.effect=None;self.effect_until=0;self.models={};self.buffs={};self.visits=[0]*1000
        self.resource_memory={k:{'count':0,'battery_delta':0} for k in CATALOG}
        self.decision={'mode':'auto','reason':'Ready to forage alongside a competitor','target':None}
        self.events=[];self.opponent_model={}

class World:
    def __init__(self, seed=42, snakes=2, systems=True):
        if snakes not in (1,2):raise ValueError('One or two snakes supported')
        self.seed=seed;self.rng=random.Random(seed);self.tick=0;self._active=0
        self.agents=[Snake('A', '#6cf2b2',[(4,4,4),(3,4,4),(2,4,4)],'+x')]
        if snakes==2:self.agents.append(Snake('B','#6dbdff',[(5,6,5),(6,6,5),(7,6,5)],'-x'))
        self.energy=[20]*1000;self.signal=[0]*1000;self.material=[0]*1000
        occupied=self.all_body()
        for i in self.rng.sample([i for i in range(1000) if i not in occupied],80):self.material[i]=1
        self.history=[];self.input_energy=0;self.spawned_material=0;self.compost=0
        self.resources={};self.resource_clock=0;self.events=[]
        self.spawn_resources()
        for k in range(len(self.agents)):
            with self.as_agent(k):self.observe()
        self.sense_others()
        self.systems=Systems(self) if systems else None
        self.purpose_observer=PurposeObserver(self)
    @contextmanager
    def as_agent(self, number):
        previous=self._active;self._active=number
        try:yield
        finally:self._active=previous
    def all_body(self):
        return {index(p) for agent in self.agents for p in agent.snake}
    def other_body(self):
        return {p for k,agent in enumerate(self.agents) if k!=self._active for p in agent.snake}
    def sense_others(self):
        # Both observe the same tick. A shallow model-of-model summary stays finite.
        previous=[copy.deepcopy(a.opponent_model) for a in self.agents]
        for k,agent in enumerate(self.agents):
            agent.opponent_model={}
            for j,other in enumerate(self.agents):
                if k==j:continue
                head=other.snake[0];d=DIRECTIONS[other.direction]
                predicted=tuple(a+b for a,b in zip(head,d))
                agent.opponent_model[other.label]={
                    'observed_tick':self.tick,'head':head,'body':copy.deepcopy(other.snake),
                    'direction':other.direction,'battery':other.battery,'score':other.score,'alive':other.alive,
                    'predicted_head':predicted if inside(predicted) and other.alive else head,
                    'target':other.decision.get('target'),
                    'model_of_me':{name:{'head':model['head'],'predicted_head':model['predicted_head'],
                                         'observed_tick':model['observed_tick']}
                                   for name,model in previous[j].items() if name==agent.label}}
    def observe(self):
        # All ordered purpose pairs; level 2 stores bounded summaries, never cyclic objects.
        truth={'energy':sum(self.energy), 'material':sum(self.material), 'information':sum(self.signal), 'snake':self.battery}
        old=copy.deepcopy(self.models)
        self.models={a:{b:{'estimate':(old.get(a,{}).get(b,{}).get('estimate',truth[b])+truth[b])//2,
                           'observed_tick':self.tick,
                           'models':{c:old.get(b,{}).get(c,{}).get('estimate',truth[c]) for c in PURPOSES}}
                        for b in PURPOSES} for a in PURPOSES}
    @property
    def capacity(self):
        return 100+10*min(5,self.score//20)
    @property
    def metabolism(self):
        return 2+(len(self.snake)-3)//8 + (2 if 'capacitor' in self.buffs else 0) + (5 if 'overload' in self.buffs else 0)
    def add_energy(self, amount):
        # External resource energy enters the ledger; overflow becomes heat.
        self.input_energy+=amount
        stored=min(amount,max(0,self.capacity-self.battery))
        self.battery+=stored; self.heat+=amount-stored
    def spawn_resources(self):
        available=[i for i in range(1000) if not self.material[i] and i not in self.resources and i not in self.all_body()]
        kinds=list(CATALOG)
        while len(self.resources)<14 and available:
            i=available.pop(self.rng.randrange(len(available)))
            kind=kinds[self.resource_clock%len(kinds)]; self.resource_clock+=1
            self.resources[i]={'kind':kind,'expires':self.tick+100}
    def queue_input(self,event):
        if not self.systems:raise ValueError('Systems framework disabled')
        accepted=self.systems.queue(event)
        self.history.append({'op':'input','data':copy.deepcopy(accepted)})
        return self.state()
    def ecology(self):
        # Open system: a bounded environmental energy input and material supply.
        for j in range(10):
            i=(self.tick*37+j*97)%1000
            gain=min(4,max(0,40-self.energy[i])); self.energy[i]+=gain; self.input_energy+=gain
        if self.systems:
            self.systems.finish(self);return
        self.resources={i:r for i,r in self.resources.items() if r['expires']>self.tick}
        occupied=self.all_body()
        free=[i for i in range(1000) if not self.material[i] and i not in occupied and i not in self.resources]
        if sum(self.material)<80 and free:
            i=free[self.rng.randrange(len(free))];self.material[i]=1;self.spawned_material+=1
        self.spawn_resources()
    def utility(self, kind):
        deficit=max(0,self.capacity-self.battery)
        if kind=='toxin':return -1000
        if kind=='overload':return -1000  # delayed cost exceeds the maximum gain
        if kind=='capacitor':return min(30,deficit)-16-2*(len(self.snake)//8)
        if kind=='shield':return 9 if self.buffs.get('shield',0)<=self.tick+2 else -1
        if kind=='catalyst':
            # An energy model now affects the controller's resource preference.
            estimated=self.models.get('snake',{}).get('energy',{}).get('estimate')
            if estimated is None:estimated=sum(self.energy)
            return 10 if estimated>=4000 and 'harvest' not in self.buffs else -1
        if kind=='memory':return 5 if 'scan' not in self.buffs else -1
        if kind=='recycler':return min(12,max(0,len(self.snake)-6)*2)-2
        return -1000
    def plan(self):
        """Bounded BFS followed by utility ranking and a free-volume safety check.

        Static body obstacles are conservative. Only the immediately departing tail
        can be traversed. Replan every tick; do not assume a route is permanently safe.
        """
        head=self.snake[0];others=self.other_body();blocked=set(self.snake[1:-1])|others;reverse=tuple(-v for v in DIRECTIONS[self.direction])
        queue=deque([(head,0,None)]);seen={head};paths={}
        while queue:
            p,dist,first=queue.popleft()
            for name,d in DIRECTIONS.items():
                if dist==0 and d==reverse:continue
                q=tuple(a+b for a,b in zip(p,d));i=index(q) if inside(q) else -1
                if i<0 or q in seen or q in blocked:continue
                if dist==0 and any(tuple(model['predicted_head'])==q for model in self.opponent_model.values() if model['alive']):continue
                if q==self.snake[-1] and self.material[i]:continue
                if self.systems and self.systems.food.get(i,{}).get('kind')=='toxic':continue
                resource=self.resources.get(i)
                if resource and self.utility(resource['kind'])<=0:continue
                seen.add(q);move=first or name;paths[i]=(dist+1,move)
                queue.append((q,dist+1,move))
        candidates=[]
        for i,(distance,move) in paths.items():
            if self.material[i]:
                food=self.systems.food.get(i) if self.systems else None
                if food and (food['kind']=='toxic' or food['expires']-self.tick<distance):continue
                value=32+max(0,55-self.battery)  # food remains primary, especially under stress
                kind='food'
                if food and food['kind']=='enriched':value+=6
            elif i in self.resources:
                kind=self.resources[i]['kind'];value=self.utility(kind)
            else:continue
            if 'scan' in self.buffs and self.visits[i]==0:value+=3
            # Discount a contested target when the other snake appears closer.
            for model in self.opponent_model.values():
                if model['alive']:
                    pos=(i%10,(i//10)%10,i//100)
                    other_distance=sum(abs(a-b) for a,b in zip(pos,model['head']))
                    if other_distance<distance:value*=0.65
                    if model['target']==i:value*=0.8
            candidates.append((value/(distance+1),-distance,-i,move,i,kind))
        # Reject first moves that immediately strand a growing body.
        def volume(move):
            q=tuple(a+b for a,b in zip(head,DIRECTIONS[move]));i=index(q)
            obstacles=set(self.snake if self.material[i] else self.snake[:-1])|others;obstacles.discard(q)
            stack=[q];visited={q}
            while stack and len(visited)<len(self.snake)+6:
                p=stack.pop()
                for d in DIRECTIONS.values():
                    v=tuple(a+b for a,b in zip(p,d))
                    if inside(v) and v not in obstacles and v not in visited:
                        if self.systems and self.systems.food.get(index(v),{}).get('kind')=='toxic':continue
                        r=self.resources.get(index(v))
                        if r and self.utility(r['kind'])<=0:continue
                        visited.add(v);stack.append(v)
            return len(visited)
        safe={m:volume(m) for m in {v[1] for v in paths.values()}}
        ranked=sorted(candidates,reverse=True)
        for value,_,__,move,target,kind in ranked:
            if safe[move]>=len(self.snake)+2:
                reason=f'Seek {kind}: benefit/distance={value:.2f}; reachable space={safe[move]}'
                return move,{'mode':'auto','reason':reason,'target':target,'kind':kind,'direction':move}
        if safe:
            # Seek unvisited energy-bearing space if all useful resources are blocked.
            move=max(safe,key=lambda m:(safe[m],self.energy[index(tuple(a+b for a,b in zip(head,DIRECTIONS[m])))],
                                       -self.visits[index(tuple(a+b for a,b in zip(head,DIRECTIONS[m])))],-list(DIRECTIONS).index(m)))
            return move,{'mode':'auto','reason':'No safe resource route; preserve free space and seek energy','target':None,'direction':move}
        return self.direction,{'mode':'auto','reason':'Trapped: no safe direction; survival is not guaranteed','target':None,'direction':self.direction}
    def consume_resource(self, i):
        resource=self.resources.pop(i,None)
        if not resource:return
        kind=resource['kind'];before=self.battery
        if kind=='capacitor':self.add_energy(30);self.buffs['capacitor']=self.tick+8
        elif kind=='shield':self.buffs['shield']=self.tick+10
        elif kind=='catalyst':self.buffs['harvest']=self.tick+12
        elif kind=='memory':self.buffs['scan']=self.tick+16
        elif kind=='recycler':
            shed=min(3,max(0,len(self.snake)-3))
            if shed:self.snake=self.snake[:-shed];self.compost+=shed
        elif kind=='toxin':
            loss=min(25,self.battery);self.battery-=loss;self.heat+=loss
        elif kind=='overload':self.add_energy(40);self.buffs['overload']=self.tick+10
        memory=self.resource_memory[kind];memory['count']+=1;memory['battery_delta']+=self.battery-before
        self.events.append(f"Consumed {CATALOG[kind]['name']}")
    def step(self, direction=None, skill=None, auto=False):
        if direction is not None and direction not in DIRECTIONS:raise ValueError('Unknown direction')
        if skill not in (None,'shield','harvest','scan'):raise ValueError('Unknown skill')
        if type(auto) is not bool:raise ValueError('auto must be a boolean')
        if not any(a.alive for a in self.agents):return self.state()
        self.history.append({'direction':direction,'skill':skill,'auto':auto});self.tick+=1
        for agent in self.agents:
            agent.events=[];agent.buffs={k:t for k,t in agent.buffs.items() if t>self.tick}
        if self.systems:self.systems.start(self)
        self.sense_others()
        # Decide from the same pre-movement state; B is always autonomous.
        intents={};auto_modes={}
        for k,agent in enumerate(self.agents):
            if not agent.alive:continue
            with self.as_agent(k):
                automatic=auto or k>0;auto_modes[k]=automatic
                move=direction if k==0 else None;purchase=skill if k==0 else None
                if automatic:move,self.decision=self.plan();purchase=None
                else:self.decision={'mode':'manual','reason':'Player steering; competitor remains autonomous','target':None}
                if purchase and self.battery>=12:
                    self.battery-=12;self.heat+=12;self.buffs[purchase]=self.tick+5
                if move:
                    d=DIRECTIONS[move];previous=DIRECTIONS[self.direction]
                    if d!=tuple(-v for v in previous):self.direction=move
                intents[k]=tuple(a+b for a,b in zip(self.snake[0],DIRECTIONS[self.direction]))
        # Conservative body exclusion includes all opponent tails. Resolve shared
        # empty-cell claims by alternating right-of-way, not iteration order.
        allowed={};reasons={}
        for k,head in intents.items():
            with self.as_agent(k):
                grows=inside(head) and self.material[index(head)]==1
                occupied=set(self.snake if grows else self.snake[:-1])|self.other_body()
                allowed[k]=inside(head) and head not in occupied
                if not allowed[k]:reasons[k]='Body or wall blocked; yield'
        keys=list(intents)
        for x,k in enumerate(keys):
            for j in keys[x+1:]:
                if intents[k]==intents[j] and allowed[k] and allowed[j]:
                    winner=min((k,j),key=lambda n:(n-(self.tick%len(self.agents)))%len(self.agents))
                    loser=j if winner==k else k;allowed[loser]=False
                    reasons[loser]='Shared resource/cell claim; yield by alternating right-of-way'
        self.diffuse()
        self.signal=[max(0,s-1) for s in self.signal]
        for k,head in intents.items():
            with self.as_agent(k):
                if not allowed[k]:
                    if auto_modes[k] or reasons[k].startswith('Shared') or 'shield' in self.buffs:
                        self.events.append(reasons[k])
                    else:self.alive=False;self.events.append('Fatal collision')
                else:self.move_into(head)
                cost=min(self.battery,self.metabolism);self.battery-=cost;self.heat+=cost
                if self.battery<=0:self.alive=False
                self.effect=next(iter(self.buffs),None);self.effect_until=self.buffs.get(self.effect,0)
        self.ecology()
        for k in range(len(self.agents)):
            with self.as_agent(k):self.observe()
        self.purpose_observer.record(self)
        return self.state()
    def diffuse(self):
        delta=[0]*1000
        for z in range(10):
            for y in range(10):
                for x in range(10):
                    p=(x,y,z);i=index(p)
                    for axis in range(3):
                        q=list(p);q[axis]+=1
                        if inside(q):
                            j=index(q);diff=self.energy[i]-self.energy[j]
                            flux=(abs(diff)//12)*(1 if diff>=0 else -1)
                            delta[i]-=flux;delta[j]+=flux
        self.energy=[e+d for e,d in zip(self.energy,delta)]
    def move_into(self, head):
        grows=self.material[index(head)]==1
        self.snake.insert(0,head)
        if grows:
            self.material[index(head)]=0;self.score+=1
            if self.systems:self.systems.child_food(self,index(head))
            else:self.add_energy(12+min(3,self.score//20))
            self.events.append('Consumed food')
            if self.score%3==0:self.buffs['harvest']=self.tick+5
            if len(self.snake)>24:self.snake.pop();self.compost+=1
        else:self.snake.pop()
        i=index(head);self.consume_resource(i);self.visits[i]+=1
        gain=min(self.energy[i],8 if 'harvest' in self.buffs else 4,max(0,self.capacity-self.battery))
        self.energy[i]-=gain;self.battery+=gain
        self.signal[i]=30 if 'scan' in self.buffs else 10
    def agent_state(self, number):
        with self.as_agent(number):
            a=self.agents[number]
            return {'id':a.label,'color':a.color,'snake':copy.deepcopy(self.snake),
                    'battery':self.battery,'heat':self.heat,'score':self.score,'alive':self.alive,
                    'direction':self.direction,'effect':self.effect,'effect_until':self.effect_until,
                    'models':copy.deepcopy(self.models),'buffs':self.buffs.copy(),
                    'decision':copy.deepcopy(self.decision),'events':self.events[:],
                    'capacity':self.capacity,'metabolism':self.metabolism,'digestion':min(3,self.score//20),
                    'resource_memory':copy.deepcopy(self.resource_memory),
                    'resource_values':{k:self.utility(k) for k in CATALOG},
                    'opponent_model':copy.deepcopy(self.opponent_model)}
    def state(self):
        agents=[self.agent_state(k) for k in range(len(self.agents))]
        s={**agents[0],'version':4,'seed':self.seed,'tick':self.tick,'time':self.tick/5,
           'energy':self.energy[:],'material':self.material[:],'signal':self.signal[:],
           'alive':any(a.alive for a in self.agents),'agents':agents,
           'period_ms':max(150,500-5*max(a.score for a in self.agents)),
           'resources':copy.deepcopy(self.resources),'catalog':copy.deepcopy(CATALOG),
           'input_energy':self.input_energy,'spawned_material':self.spawned_material,'compost':self.compost,
           'systems':self.systems.snapshot() if self.systems else None,
           'output':self.systems.output(self) if self.systems else None,
           'purpose':self.purpose_observer.report(self),
           'system_energy':self.systems.bank+self.systems.heat if self.systems else 0,
           'initial_energy':20000+60*len(self.agents)+(200 if self.systems else 0),'initial_material':80+3*len(self.agents),
           'right_of_way':self.agents[(self.tick+1)%len(self.agents)].label}
        s['hash']=hashlib.sha256(json.dumps(s,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        return s

# Compatibility properties keep single-agent experiments concise. Simulation work
# enters an explicit agent context; shared fields never move between agents.
for _name in AGENT_FIELDS:
    setattr(World,_name,property(lambda self,n=_name:getattr(self.agents[self._active],n),
                                lambda self,value,n=_name:setattr(self.agents[self._active],n,value)))
