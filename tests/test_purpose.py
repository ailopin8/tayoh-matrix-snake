import unittest
from engine import World

class PurposeTests(unittest.TestCase):
    def test_initial_report_has_no_inferred_behavior(self):
        w=World();p=w.state()['purpose']
        self.assertEqual(p['transitions'],0)
        self.assertEqual(len(p['roles']),4)
        self.assertTrue(all(r['observed']=='Awaiting behavior evidence' and not r['gap'] for r in p['roles']))

    def test_snapshot_is_read_only_and_export_matches(self):
        w=World();w.step(auto=True)
        before=w.state()
        self.assertEqual(before,w.state())
        self.assertEqual(before['purpose'],before['output']['purpose'])
        before['purpose']['roles'][0]['evidence']['integrity_change']=999
        self.assertNotEqual(w.state()['purpose']['roles'][0]['evidence']['integrity_change'],999)

    def test_replay_and_window_are_deterministic(self):
        a,b=World(5),World(5)
        for _ in range(40):a.step(auto=True);b.step(auto=True)
        self.assertEqual(a.state(),b.state())
        p=a.state()['purpose']
        self.assertLessEqual(len(a.purpose_observer.samples),32)
        self.assertEqual(p['transitions'],p['to_tick']-p['from_tick'])
        self.assertLessEqual(p['transitions'],31)
        self.assertEqual(World(5).state()['purpose']['transitions'],0)

    def test_threshold_and_evidence_report_actual_deltas(self):
        w=World();w.tick=1;w.systems.protector['faces'][0]=89
        w.agents[0].battery-=16
        w.purpose_observer.record(w)
        p=w.state()['purpose'];r={r['role']:r for r in p['roles']}
        self.assertTrue(r['protector']['gap'])
        self.assertEqual(r['protector']['evidence']['integrity_change'],-11)
        self.assertTrue(r['child_A']['gap'])
        self.assertEqual(p['attention']['focus'],'protector')

    def test_no_framework_and_single_child(self):
        w=World(snakes=1,systems=False);w.step(auto=True)
        self.assertEqual([r['role'] for r in w.state()['purpose']['roles']],['child_A'])
