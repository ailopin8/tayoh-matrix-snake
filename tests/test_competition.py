import unittest
from engine import World,index,DIRECTIONS

class CompetitionTests(unittest.TestCase):
    def ledger(self,w):
        self.assertEqual(sum(w.energy)+sum(a.battery+a.heat for a in w.agents),20120+w.input_energy)
        self.assertEqual(sum(w.material)+sum(len(a.snake) for a in w.agents)+w.compost,86+w.spawned_material)
        bodies=[p for a in w.agents for p in a.snake]
        self.assertEqual(len(bodies),len(set(bodies)))
    def test_initial_separation_and_models(self):
        w=World(systems=False);self.ledger(w)
        for k,a in enumerate(w.agents):
            other=w.agents[1-k]
            self.assertEqual(a.opponent_model[other.label]['head'],other.snake[0])
        self.assertEqual(len(w.state()['agents']),2)
    def test_prediction_changes_route(self):
        w=World(systems=False);w.material=[0]*1000;w.resources={}
        w.agents[0].snake=[(3,4,4),(2,4,4),(1,4,4)]
        w.agents[1].snake=[(5,4,4),(6,4,4),(7,4,4)];w.agents[1].direction='-x'
        w.material[index((4,4,4))]=1;w.sense_others()
        move,decision=w.plan();self.assertNotEqual(move,'+x')
        w.agents[1].direction='+y';w.sense_others()
        move,decision=w.plan();self.assertEqual(move,'+x')
    def contest(self,tick):
        w=World(systems=False);w.tick=tick;w.material=[0]*1000;w.resources={}
        w.agents[0].snake=[(3,4,4),(2,4,4),(1,4,4)]
        w.agents[1].snake=[(5,4,4),(6,4,4),(7,4,4)];w.agents[1].direction='-x'
        w.material[index((4,4,4))]=1
        # Force two same-cell proposals to isolate the simultaneous resolver.
        w.plan=lambda:(w.direction,{'mode':'auto','reason':'Forced contest','target':index((4,4,4))})
        w.step(auto=True);return w
    def test_contest_single_consumption(self):
        w=self.contest(0)
        self.assertEqual([a.score for a in w.agents],[0,1])
        self.assertEqual(sum(a.score for a in w.agents),1)
        self.assertTrue(all(a.alive for a in w.agents))
        self.assertNotEqual(w.agents[0].snake[0],w.agents[1].snake[0])
    def test_alternating_priority(self):
        w=self.contest(1);self.assertEqual([a.score for a in w.agents],[1,0])
    def test_no_head_swap(self):
        w=World(systems=False);w.agents[0].snake=[(4,4,4),(3,4,4),(2,4,4)]
        w.agents[1].snake=[(5,4,4),(6,4,4),(7,4,4)];w.agents[1].direction='-x'
        w.plan=lambda:(w.direction,{'mode':'auto','reason':'Forced head swap','target':None})
        before=[a.snake[:] for a in w.agents];w.step(auto=True)
        self.assertEqual(before,[a.snake for a in w.agents]);self.assertTrue(all(a.alive for a in w.agents))
    def test_mutual_models_bounded_and_causal(self):
        w=World(systems=False);w.step(auto=True);w.step(auto=True)
        for a in w.agents:
            for model in a.opponent_model.values():
                self.assertIn(a.label,model['model_of_me'])
                self.assertNotIn('model_of_me',model['model_of_me'][a.label])
                self.assertEqual(model['observed_tick'],w.tick)
    def test_competition_replay(self):
        a,b=World(7, systems=False),World(7, systems=False)
        for _ in range(20):a.step(auto=True);b.step(auto=True)
        self.assertEqual(a.state(),b.state())
    def test_dual_endurance(self):
        w=World(42, systems=False)
        for _ in range(250):
            w.step(auto=True);self.ledger(w)
            self.assertTrue(all(a.alive for a in w.agents))
            self.assertTrue(all(0<a.battery<=150 for a in w.agents))
            for i in w.resources:self.assertNotIn(i,w.all_body());self.assertFalse(w.material[i])
        self.assertTrue(all(a.score>10 for a in w.agents))
    def test_survivor_continues(self):
        w=World(systems=False);w.agents[0].alive=False;old=w.agents[0].snake[:]
        w.step(auto=True);self.assertEqual(w.tick,1);self.assertEqual(w.agents[0].snake,old)
        self.assertTrue(w.state()['alive']);self.ledger(w)
    def test_model_snapshot_independent(self):
        w=World(systems=False);s=w.state();s['agents'][0]['opponent_model']['B']['body'].clear()
        self.assertEqual(len(w.agents[0].opponent_model['B']['body']),3)
if __name__=='__main__':unittest.main()
