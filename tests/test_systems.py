import copy
import unittest
from engine import World,index

class SystemsTests(unittest.TestCase):
    def ledger(self,w):
        s=w.systems
        self.assertEqual(sum(w.energy)+sum(a.battery+a.heat for a in w.agents)+s.bank+s.heat,20000+60*len(w.agents)+200+w.input_energy)
        self.assertEqual(sum(w.material)+sum(len(a.snake) for a in w.agents)+w.compost,80+3*len(w.agents)+w.spawned_material)
    def test_roles_initialized(self):
        w=World();self.assertEqual(w.systems.integrity,100);self.assertEqual(len(w.systems.food),80);self.ledger(w)
        self.assertEqual(set(w.systems.models),{'protector','healer','child_A','child_B'})
    def test_expired_food_feeds_protector(self):
        w=World();i=next(iter(w.systems.food));w.systems.food[i]['expires']=1
        w.step(auto=True);self.assertEqual(w.systems.protector['consumed'],1);self.assertEqual(w.material[i],0);self.ledger(w)
    def test_child_consumption_and_reciprocity(self):
        w=World(snakes=1);i=index((5,4,4));w.material[i]=1
        w.systems.food[i]={'born':0,'expires':50,'kind':'regular'}
        reserve=w.systems.healer['reserve'];w.step('+x')
        self.assertEqual(w.score,1);self.assertEqual(w.systems.healer['pollination'],2)
        self.assertNotIn(i,w.systems.food);self.assertGreater(w.systems.healer['reserve'],reserve)
    def test_unsafe_healer_pauses(self):
        w=World();w.systems.protector['faces']=[30]*6
        n=w.spawned_material;w.step(auto=True)
        self.assertFalse(w.systems.healer['safe']);self.assertEqual(n,w.spawned_material);self.ledger(w)
    def test_child_safety_gates_healer(self):
        w=World();w.agents[1].alive=False;w.step(auto=True)
        self.assertFalse(w.systems.healer['safe'])
    def test_support_and_information_mapping(self):
        w=World();w.queue_input({'label':'Supply','kind':'support','value':5,'position':[1,2,3]})
        w.queue_input({'label':'Novel','kind':'information','value':2,'position':[1,2,3]})
        self.assertEqual(w.systems.pressure,0);self.assertEqual(len(w.systems.pending),2)
        w.step(auto=True);self.assertEqual(len(w.systems.pending),0)
        self.assertEqual(w.systems.processed[0]['position'],[1,2,3]);self.assertGreaterEqual(w.signal[321],0)
        self.assertIn('enriched',[f['kind'] for f in w.systems.food.values()]);self.ledger(w)
    def test_stress_creates_toxic_food(self):
        w=World();w.queue_input({'label':'Unknown shock','kind':'stress','value':10})
        w.queue_input({'label':'New phenotype','kind':'information','value':3})
        w.step(auto=True)
        # Force a free production slot so the phenotype can be expressed.
        i=next(iter(w.systems.food));w.systems.food[i]['expires']=w.tick+1
        w.step(auto=True)
        self.assertIn('toxic',[f['kind'] for f in w.systems.food.values()]);self.ledger(w)
    def test_reach_food_before_deadline(self):
        w=World(snakes=1);w.material=[0]*1000;w.resources={};w.systems.food={}
        i=index((5,4,4));w.material[i]=1
        w.systems.food[i]={'born':0,'expires':2,'kind':'regular'}
        w.step(auto=True);self.assertEqual(w.score,1)
        self.assertEqual(w.snake[0],(5,4,4))
    def test_toxic_food_not_used_as_transit(self):
        w=World(snakes=1);w.material=[0]*1000;w.resources={};w.systems.food={}
        i=index((5,4,4));j=index((6,4,4));w.material[i]=w.material[j]=1
        w.systems.food[i]={'born':0,'expires':40,'kind':'toxic'};w.systems.food[j]={'born':0,'expires':40,'kind':'regular'}
        self.assertNotEqual(w.plan()[0],'+x')
    def test_invalid_input_atomic(self):
        w=World();before=w.state()
        for event in ({'label':'bad','kind':'stress','value':11},{'label':'bad','kind':'stress','value':True},{'label':'bad','kind':'support','value':2,'position':[-1,0,0]}):
            with self.assertRaises(ValueError):w.queue_input(event)
            self.assertEqual(before,w.state())
    def test_deterministic_input_replay(self):
        a,b=World(7),World(7)
        a.queue_input({'label':'External event','kind':'stress','value':3})
        for _ in range(20):a.step(auto=True)
        for action in a.history:
            if action.get('op')=='input':b.queue_input(action['data'])
            else:b.step(**action)
        self.assertEqual(a.state(),b.state());self.ledger(a)
    def test_models_are_finite_and_used(self):
        w=World();w.systems.models['healer']['protector']['estimate']=0
        w.step(auto=True);self.assertFalse(w.systems.healer['safe'])
        for role,models in w.systems.models.items():
            for model in models.values():self.assertEqual(len(model['models']),4)
    def test_failure_propagates(self):
        w=World();w.systems.protector['faces']=[0]*6;w.step(auto=True)
        self.assertTrue(all(not a.alive for a in w.agents));self.assertFalse(w.state()['alive']);self.ledger(w)
    def test_endurance_accounting_and_food_metadata(self):
        w=World()
        for _ in range(180):
            w.step(auto=True);self.ledger(w)
            self.assertEqual(set(w.systems.food),{i for i,m in enumerate(w.material) if m})
            self.assertTrue(all(0<=h<=100 for h in w.systems.protector['faces']))
            bodies=[p for a in w.agents for p in a.snake];self.assertEqual(len(bodies),len(set(bodies)))
        self.assertGreater(w.systems.protector['consumed'],0)
        self.assertGreater(w.systems.healer['pollination'],0)
    def test_snapshot_independent(self):
        w=World();s=w.state();s['systems']['protector']['faces'][0]=0
        self.assertEqual(w.systems.protector['faces'][0],100)
if __name__=='__main__':unittest.main()
