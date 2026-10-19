"""Protector/healer/child coupling and explicit, replayable uncertainty adapter.

Game units and designed rules, not a calibrated model of an arbitrary real system.
"""
from instructions import interpret, describe
import copy
import hashlib
import random

class Systems:
    def __init__(self, world):
        self.rng=random.Random(world.seed ^ 0x50524F54)
        self.protector={'faces':[100]*6,'reserve':120,'heat':0,'consumed':0,'repaired':0}
        self.healer={'vitality':100,'reserve':80,'heat':0,'produced':80,'safe':True,'pollination':0}
        self.food={i:{'born':0,'expires':25+i%55,'kind':'regular'} for i,m in enumerate(world.material) if m}
        self.policies={'protector':'default','healer':'default','children':'default'}
        self.failed=False;self.pressure=0;self.novelty=0;self.pending=[];self.processed=[];self.models={};self.models_tick=0
        self.last_damage={'face':None,'amount':0,'cause':'unattributed external influence','uncertain':True}
        self.update_models(world)
    @property
    def integrity(self):return min(self.protector['faces'])
    @property
    def bank(self):return self.protector['reserve']+self.healer['reserve']
    @property
    def heat(self):return self.protector['heat']+self.healer['heat']
    @property
    def viable(self):return self.integrity>0 and self.healer['vitality']>0
    def validate_input(self, event):
        if not isinstance(event,dict):raise ValueError('Input must be an object')
        if event.get('kind')=='instruction':
            if set(event)-{'label','kind','text'}:raise ValueError('Unknown instruction field')
            rule=interpret(event.get('text'))
            return {'label':rule['text'],'kind':'instruction','text':rule['text']}
        if set(event)-{'label','kind','value','position'}:raise ValueError('Unknown input field')
        label=event.get('label','Experiment')
        if not isinstance(label,str) or not 1<=len(label)<=120:raise ValueError('Label must be 1–120 characters')
        kind=event.get('kind');value=event.get('value')
        if kind not in ('stress','support','information'):raise ValueError('Kind must be stress, support or information')
        if type(value) is not int or not 0<=value<=10:raise ValueError('Value must be an integer from 0 to 10')
        position=event.get('position')
        if position is None:
            i=int.from_bytes(hashlib.sha256(label.encode()).digest()[:4],'big')%1000
            position=[i%10,(i//10)%10,i//100]
        if not isinstance(position,list) or len(position)!=3 or any(type(v) is not int or not 0<=v<=9 for v in position):raise ValueError('Position must be three integer coordinates 0–9')
        return {'label':label,'kind':kind,'value':value,'position':position[:]}
    def queue(self,event):
        event=self.validate_input(event)
        if len(self.pending)>=64:raise ValueError('Input queue full (64 events)')
        self.pending.append(event);return event
    def spend(self,role,amount):
        used=min(amount,role['reserve']);role['reserve']-=used;role['heat']+=used;return used
    def start(self,w):
        for e in self.pending:
            if e['kind']=='instruction':
                rule=interpret(e['text'])
                if rule['role']=='all':self.policies={k:'default' for k in self.policies}
                else:self.policies[rule['role']]=rule['mode']
                self.processed.append({**copy.deepcopy(e),'applied_tick':w.tick,'policy':copy.deepcopy(rule)})
                continue
            x,y,z=e['position'];i=x+10*y+100*z;w.signal[i]=min(30,w.signal[i]+e['value']*3)
            if e['kind']=='stress':self.pressure=min(10,self.pressure+e['value'])
            elif e['kind']=='support':
                self.pressure=max(0,self.pressure-e['value'])
                gain=8*e['value'];self.protector['reserve']+=gain;w.input_energy+=gain
            else:self.novelty+=e['value']
            self.processed.append({**copy.deepcopy(e),'applied_tick':w.tick})
        self.pending=[];self.processed=self.processed[-32:]
        if w.tick%10==0:self.pressure=max(0,self.pressure-1)
        face=self.rng.randrange(6);damage=self.rng.randrange(4+self.pressure)
        self.protector['faces'][face]=max(0,self.protector['faces'][face]-damage)
        self.last_damage={'face':face,'amount':damage,'cause':'unattributed external influence','uncertain':True,
                          'envelope_max':3+self.pressure,'seeded':True}
        # Expiry happens before movement: a child must reach food before its deadline.
        for i,food in list(self.food.items()):
            if not w.material[i]:del self.food[i];continue
            if food['expires']<=w.tick:
                w.material[i]=0;del self.food[i];w.compost+=1;self.protector['consumed']+=1
                if food['kind']=='toxic':
                    self.spend(self.protector,6)
                    f=min(range(6),key=lambda j:self.protector['faces'][j]);self.protector['faces'][f]=max(0,self.protector['faces'][f]-2)
                else:
                    gain=18 if food['kind']=='enriched' else 12
                    self.protector['reserve']+=gain;w.input_energy+=gain
        if self.integrity==0:
            self.failed=True
            for a in w.agents:a.alive=False;a.events.append('Protector boundary failed')
    def child_food(self,w,i):
        food=self.food.pop(i,{'kind':'regular','born':w.tick,'expires':w.tick+1})
        if food['kind']=='toxic':
            loss=min(18,w.battery);w.battery-=loss;w.heat+=loss;w.events.append('Consumed toxic food')
            return False
        w.add_energy(12+min(3,w.score//20)+(6 if food['kind']=='enriched' else 0))
        # Child pays a reciprocal contribution, not an unaccounted energy bonus.
        gift=min(2,w.battery);w.battery-=gift;self.healer['reserve']+=gift;self.healer['pollination']+=gift
        belief=self.models.get(f'child_{w.agents[w._active].label}',{}).get('protector',{}).get('estimate',self.integrity)
        if belief<85:
            repair=min(1,w.battery);w.battery-=repair;self.protector['reserve']+=repair
        return True
    def finish(self,w):
        p=self.protector;h=self.healer
        # Boundary has healer-like repair and child-like observation/adaptation.
        self.spend(p,1)
        weakest=min(range(6),key=lambda j:p['faces'][j])
        child_beliefs=[v['estimate'] for k,v in self.models.get('protector',{}).items() if k.startswith('child_')]
        budget=4 if child_beliefs and min(child_beliefs)<30 else 3
        budget={'repair':5,'conserve':1}.get(self.policies['protector'],budget)
        repair=0 if self.failed else min(budget,100-p['faces'][weakest],p['reserve'])
        self.spend(p,repair);p['faces'][weakest]+=repair;p['repaired']+=repair
        child_safe=all(a.alive and a.battery>=8 for a in w.agents)
        model=self.models.get('healer',{}).get('protector',{}).get('estimate',self.integrity)
        threshold=65 if self.policies['healer']=='cautious' else 40
        h['safe']=not self.failed and self.integrity>=threshold and model>=threshold and child_safe
        if h['safe']:
            h['vitality']=min(100,h['vitality']+1)
            h['reserve']+=3;w.input_energy+=3  # external metabolic substrate, explicitly supplied
        else:h['vitality']=max(0,h['vitality']-2)
        self.spend(h,1)
        w.resources={i:r for i,r in w.resources.items() if r['expires']>w.tick}
        free=[i for i in range(1000) if not w.material[i] and i not in w.all_body() and i not in w.resources]
        if (self.policies['healer']!='cautious' or w.tick%3==0) and h['safe'] and h['vitality']>=20 and h['reserve']>=1 and sum(w.material)<80 and free:
            i=free[w.rng.randrange(len(free))];kind='regular'
            # New information changes available phenotypes, gated by boundary condition.
            if self.novelty>0:
                kind='toxic' if self.pressure>=5 or self.integrity<65 else 'enriched' if self.integrity>=85 else 'regular'
                self.novelty-=1
            elif self.pressure>=5 and w.tick%3==0:kind='toxic'
            elif self.integrity>=90 and w.tick%7==0:kind='enriched'
            self.spend(h,1);w.material[i]=1;w.spawned_material+=1;h['produced']+=1
            self.food[i]={'born':w.tick,'expires':w.tick+(30 if kind=='enriched' else 20 if kind=='toxic' else 45),'kind':kind}
        if self.integrity>=40 and h['vitality']>0:w.spawn_resources()
        self.update_models(w)
    def update_models(self,w):
        truth={'protector':self.integrity,'healer':self.healer['vitality'],
               **{f'child_{a.label}':max(0,min(100,a.battery*100//(100+10*min(5,a.score//20)))) if a.alive else 0 for a in w.agents}}
        old=copy.deepcopy(self.models)
        self.models={a:{b:{'estimate':(old.get(a,{}).get(b,{}).get('estimate',v)+v)//2,
                          'observed_tick':w.tick,'models':{c:old.get(b,{}).get(c,{}).get('estimate',q) for c,q in truth.items()}}
                       for b,v in truth.items()} for a in truth}
        self.models_tick=w.tick
    def snapshot(self):
        return {'failed':self.failed,'roles':{'protector':'Environment boundary','healer':'Food-producing process and its timed food','children':'Snakes A/B'},
                'protector':copy.deepcopy(self.protector),'integrity':self.integrity,'healer':copy.deepcopy(self.healer),
                'policies':self.policies.copy(),'policy_descriptions':{k:describe(k,v) for k,v in self.policies.items()},'pressure':self.pressure,'novelty':self.novelty,'last_damage':self.last_damage.copy(),
                'models':copy.deepcopy(self.models),'food':copy.deepcopy(self.food),
                'pending':copy.deepcopy(self.pending),'processed':copy.deepcopy(self.processed)}
    def output(self,w):
        return {'schema':'tayoh.system-output.v1','tick':w.tick,'interpretation':'Designed simulation outcomes; not calibrated real-world predictions',
                'purpose':w.purpose_observer.report(w),
                'protector_integrity':self.integrity,'healer_vitality':self.healer['vitality'],'safe_space':self.healer['safe'],
                'children':{a.label:{'alive':a.alive,'food_consumed':a.score,'battery':a.battery} for a in w.agents},
                'protector_food_consumed':self.protector['consumed'],'external_cause':'unknown within a seeded bounded envelope',
                'inputs_pending':len(self.pending),'applied_inputs':copy.deepcopy(self.processed),
                'next_question':'Which input, boundary condition or resource rule should be changed and compared in the next run?'}
