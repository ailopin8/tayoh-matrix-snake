import unittest
from engine import World, index
from instructions import interpret, RECIPES

class InstructionTests(unittest.TestCase):
    def test_all_recipes_and_keywords_are_deterministic(self):
        for key,r in RECIPES.items():
            self.assertEqual(interpret(key),interpret(r[2]))
            self.assertEqual(interpret('  '+r[2].upper()+'! '),interpret(key))

    def test_reject_without_mutation(self):
        w=World();before=w.state()
        for text in ('do anything','import os',None,'x'*241):
            with self.assertRaises(ValueError):w.queue_input({'kind':'instruction','text':text})
        self.assertEqual(w.state(),before)

    def test_confirm_queues_and_next_tick_applies_and_restore(self):
        w=World();w.queue_input({'kind':'instruction','text':'repair'})
        self.assertEqual(w.systems.policies['protector'],'default')
        w.step(auto=True);self.assertEqual(w.systems.policies['protector'],'repair')
        self.assertEqual(w.systems.processed[-1]['applied_tick'],1)
        w.queue_input({'kind':'instruction','text':'restore'});w.step(auto=True)
        self.assertTrue(all(v=='default' for v in w.systems.policies.values()))

    def test_protector_actual_repair_changes(self):
        worlds=[]
        for key in ('repair','conserve'):
            w=World();w.systems.protector['faces']=[70]*6
            w.queue_input({'kind':'instruction','text':key});w.step(auto=True);worlds.append(w)
        self.assertEqual(worlds[0].systems.protector['repaired'],5)
        self.assertEqual(worlds[1].systems.protector['repaired'],1)
        self.assertLess(worlds[0].systems.protector['reserve'],worlds[1].systems.protector['reserve'])

    def test_healer_actual_production_changes(self):
        counts=[]
        for key in ('normal_food','cautious'):
            w=World();w.material=[0]*1000;w.systems.food={};w.compost+=80
            w.queue_input({'kind':'instruction','text':key})
            for _ in range(3):w.step(auto=True)
            counts.append(w.systems.healer['produced']-80)
        self.assertEqual(counts,[3,1])

    def test_child_policy_changes_actual_target_choice(self):
        w=World();w.material=[0]*1000;w.resources={};w.systems.food={}
        contested=index((5,4,4));other=index((4,4,6))
        w.material[contested]=w.material[other]=1
        w.agents[0].opponent_model={'B':{'alive':True,'head':[5,6,5],'predicted_head':[5,5,5],'target':contested}}
        w.systems.policies['children']='compete';competitive=w.plan()[1]['target']
        w.systems.policies['children']='cooperate';cooperative=w.plan()[1]['target']
        self.assertEqual(competitive,contested);self.assertEqual(cooperative,other)

    def test_replay_and_energy_material_conservation(self):
        w=World(7)
        for key in ('repair','cautious','cooperate','restore'):
            w.queue_input({'kind':'instruction','text':key})
            for _ in range(3):w.step(auto=True)
        r=World(7)
        for action in w.history:
            if action.get('op')=='input':r.queue_input(action['data'])
            else:r.step(**action)
        self.assertEqual(w.state(),r.state())
        s=w.state()
        energy=sum(w.energy)+sum(a.battery+a.heat for a in w.agents)+w.systems.bank+w.systems.heat
        self.assertEqual(energy,s['initial_energy']+w.input_energy)
        self.assertEqual(sum(w.material)+sum(len(a.snake) for a in w.agents)+w.compost,s['initial_material']+w.spawned_material)
