"""Bounded behavioral evidence; describes outcomes, never infers hidden intention."""
from collections import deque

class PurposeObserver:
    window = 32  # at most 31 logical tick transitions

    def __init__(self, world):
        self.samples = deque(maxlen=self.window)
        self.record(world)

    def record(self, world):
        s = world.systems
        self.samples.append({'tick': world.tick,
            'integrity': s.integrity if s else None,
            'produced': s.healer['produced'] if s else 0,
            'repaired': s.protector['repaired'] if s else 0,
            'expired': s.protector['consumed'] if s else 0,
            'safe': s.healer['safe'] if s else False,
            'children': {a.label: {'food': a.score, 'battery': a.battery,
                'alive': a.alive} for a in world.agents}})

    def report(self, world):
        first, last = self.samples[0], self.samples[-1]
        ticks = last['tick'] - first['tick']
        roles = []
        def role(name, declared, rules, observed, evidence, gap, lens):
            roles.append({'role': name, 'declared': declared, 'rules': rules,
                'observed': observed if ticks else 'Awaiting behavior evidence',
                'evidence': evidence, 'gap': bool(ticks and gap), 'lens': lens})
        if world.systems:
            loss = first['integrity'] - last['integrity']
            role('protector', 'Maintain a viable shared boundary',
                 'Spend reserve repairing weakest face; reclaim expired food',
                 'Boundary declining despite repair' if loss >= 10 else 'Boundary maintained or fluctuating',
                 {'integrity_change': -loss, 'repair_units': last['repaired']-first['repaired'],
                  'expired_food_consumed': last['expired']-first['expired']}, loss >= 10, 'boundary')
            produced = last['produced'] - first['produced']
            unsafe = sum(not s['safe'] for s in list(self.samples)[1:])
            role('healer', 'Supply food while preserving safe production',
                 'Produce only when safety, reserve, capacity and free-cell conditions permit',
                 f'Produced {produced} food; unsafe on {unsafe} observed ticks',
                 {'food_produced': produced, 'unsafe_ticks': unsafe}, unsafe >= 5, 'material')
        for label, child in last['children'].items():
            old = first['children'][label]
            food, battery = child['food']-old['food'], child['battery']-old['battery']
            role('child_'+label, 'Stay viable while sharing a bounded resource pool',
                 'A follows autonomy toggle or player; B forages; both obey collision and energy rules',
                 f'Consumed {food} food; battery change {battery:+d}; '+('viable' if child['alive'] else 'inactive'),
                 {'food_consumed': food, 'battery_change': battery, 'alive': child['alive']},
                 not child['alive'] or (battery <= -15 and food == 0), 'material')
        gaps = [r for r in roles if r['gap']]
        focus = gaps[0] if gaps else None
        return {'schema': 'tayoh.purpose-evidence.v1', 'from_tick': first['tick'],
            'to_tick': last['tick'], 'transitions': ticks, 'capacity': self.window,
            'interpretation': 'Observed outcomes under current rules and inputs; not proof of intention or isolated causation',
            'roles': roles, 'attention': {'focus': focus['role'] if focus else 'relationships',
                'lens': focus['lens'] if focus else 'relationships',
                'reason': (focus['role']+': '+focus['observed']) if focus else 'No configured purpose-gap threshold crossed'}}
