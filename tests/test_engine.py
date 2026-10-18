import json
import unittest
from engine import World,index,inside,fold,boundary

class EngineTests(unittest.TestCase):
    def test_replay(self):
        a,b=World(7, snakes=1, systems=False),World(7, snakes=1, systems=False)
        for d in ['+y','+z','-x','-y','+z','+x']:
            self.assertEqual(a.step(d),b.step(d))
    def test_conservation_and_bounds(self):
        w=World(snakes=1, systems=False)
        for i in range(35):
            w.step(['+y','+z','-x','-y','-z','+x'][i%6], 'scan' if i%7==0 else None)
            self.assertEqual(sum(w.energy)+w.battery+w.heat,20060+w.input_energy)
            self.assertEqual(sum(w.material)+len(w.snake)+w.compost,83+w.spawned_material)
            self.assertTrue(all(e>=0 for e in w.energy))
            self.assertTrue(all(inside(p) for p in w.snake))
            self.assertEqual(len(w.snake),len(set(w.snake)))
    def test_flux_extreme(self):
        w=World(snakes=1, systems=False);w.energy=[0]*1000;w.energy[555]=10000
        w.step();self.assertTrue(all(e>=0 for e in w.energy));self.assertEqual(sum(w.energy)+w.battery+w.heat,10060+w.input_energy)
    def test_wall(self):
        w=World(snakes=1, systems=False);w.snake=[(9,4,4),(8,4,4)];w.step();self.assertFalse(w.alive);self.assertEqual(w.snake[0],(9,4,4))
    def test_shield_wall(self):
        w=World(snakes=1, systems=False);w.snake=[(9,4,4)];w.step(skill='shield');self.assertTrue(w.alive);self.assertEqual(w.snake[0],(9,4,4))
    def test_food_growth(self):
        w=World(snakes=1, systems=False);w.material[index((5,4,4))]=1;w.step();self.assertEqual(len(w.snake),4);self.assertEqual(w.score,1)
    def test_reverse_rejected(self):
        w=World(snakes=1, systems=False);w.step('-x');self.assertEqual(w.snake[0],(5,4,4))
    def test_expiry(self):
        w=World(snakes=1, systems=False);w.step('+y','scan')
        for d in ['+z','-x','-y','-z','+x']:w.step(d)
        self.assertIsNone(w.effect)
    def test_models_finite(self):
        w=World(snakes=1, systems=False);s=w.state();self.assertEqual(len(s['models']),4)
        for m in s['models'].values():
            self.assertEqual(len(m),4)
            for v in m.values():self.assertEqual(len(v['models']),4)
        self.assertLess(len(json.dumps(s['models'])),5000)
    def test_snapshot_not_alias(self):
        w=World(snakes=1, systems=False);s=w.state();s['energy'][0]=999;s['snake'][0]=(0,0,0);self.assertEqual(w.energy[0],20);self.assertEqual(w.snake[0],(4,4,4))
    def test_invalid_atomic(self):
        w=World(snakes=1, systems=False);s=w.state()
        with self.assertRaises(ValueError):w.step('wrong')
        self.assertEqual(s,w.state())
    def test_dead_noop(self):
        w=World(snakes=1, systems=False);w.alive=False;s=w.state();self.assertEqual(w.step(),s)
    def test_boundary_preimage(self):
        for x in range(10):
            for y in range(10):self.assertEqual(boundary((x,y)),2<=x<=7 and 2<=y<=7)
        self.assertEqual(fold((2,2)),fold((7,7)))
    def test_seed_difference(self):self.assertNotEqual(World(1, snakes=1, systems=False).material,World(2, snakes=1, systems=False).material)
if __name__=='__main__':unittest.main()
