import unittest
from engine import World,index
from resources import CATALOG

class AutonomyTests(unittest.TestCase):
    def empty(self):
        w=World(snakes=1, systems=False);w.material=[0]*1000;w.resources={};return w
    def test_seek_and_consume(self):
        w=self.empty();w.material[index((5,4,4))]=1;w.step(auto=True)
        self.assertEqual(w.snake[0],(5,4,4));self.assertEqual(w.score,1);self.assertEqual(w.decision['kind'],'food')
    def test_avoid_known_harm(self):
        w=self.empty();w.material[index((6,4,4))]=1;w.resources[index((5,4,4))]={'kind':'toxin','expires':100}
        direction,decision=w.plan();self.assertNotEqual(direction,'+x');self.assertEqual(decision['kind'],'food')
    def test_state_dependent_value(self):
        w=World(snakes=1, systems=False);w.battery=w.capacity;self.assertLess(w.utility('capacitor'),0)
        w.battery=10;self.assertGreater(w.utility('capacitor'),0);self.assertLess(w.utility('overload'),0)
    def test_resource_effects(self):
        for kind in CATALOG:
            w=self.empty();i=index((5,4,4));w.resources[i]={'kind':kind,'expires':100};w.step('+x')
            self.assertEqual(w.resource_memory[kind]['count'],1)
            self.assertEqual(sum(w.energy)+w.battery+w.heat,20060+w.input_energy)
        w=self.empty();w.resources[index((5,4,4))]={'kind':'toxin','expires':100};w.step('+x');self.assertLess(w.battery,60)
    def test_regrowth_supply(self):
        w=World(snakes=1, systems=False);i=next(i for i,v in enumerate(w.material) if v);w.material[i]=0;w.step(auto=True)
        self.assertEqual(w.spawned_material,1);self.assertEqual(sum(w.material),80-w.score)
    def test_body_cap_and_compost(self):
        w=self.empty();w.snake=[(x,0,0) for x in range(9,-1,-1)]+[(x,0,1) for x in range(10)]+[(x,0,2) for x in range(4)]
        w.material[index((9,1,0))]=1;w.step('+y');self.assertEqual(len(w.snake),24);self.assertEqual(w.compost,1)
    def test_resource_expiry_and_no_overlap(self):
        w=World(snakes=1, systems=False);w.resources[0]={'kind':'toxin','expires':1};w.step(auto=True)
        self.assertTrue(all(r['expires']>w.tick for r in w.resources.values()))
        self.assertTrue(all(not w.material[i] and i not in map(index,w.snake) for i in w.resources))
    def test_autonomous_replay(self):
        a,b=World(42, snakes=1, systems=False),World(42, snakes=1, systems=False)
        for _ in range(30):a.step(auto=True);b.step(auto=True)
        self.assertEqual(a.state(),b.state())
    def test_finite_endurance(self):
        w=World(42, snakes=1, systems=False)
        for _ in range(250):
            w.step(auto=True);self.assertTrue(w.alive)
            self.assertEqual(sum(w.energy)+w.battery+w.heat,20060+w.input_energy)
            self.assertEqual(sum(w.material)+len(w.snake)+w.compost,83+w.spawned_material)
            self.assertEqual(len(set(w.snake)),len(w.snake));self.assertTrue(0<w.battery<=w.capacity)
        self.assertGreater(w.score,20);self.assertLessEqual(len(w.snake),24)
    def test_auto_type_atomicity(self):
        w=World(snakes=1, systems=False);before=w.state()
        with self.assertRaises(ValueError):w.step(auto='yes')
        self.assertEqual(before,w.state())
if __name__=='__main__':unittest.main()
