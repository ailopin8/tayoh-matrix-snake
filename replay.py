"""Usage: python3 replay.py downloaded-replay.json"""
import json
import sys
from engine import World
if __name__=='__main__':
    with open(sys.argv[1]) as f: log=json.load(f)
    w=World(log['seed'],snakes=log.get('snakes',2),systems=log.get('systems',True))
    for a in log['actions']:
        if a.get('op')=='input':w.queue_input(a['data'])
        else:w.step(a.get('direction'),a.get('skill'),a.get('auto',False))
    print(w.state()['hash'])
