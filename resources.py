"""Explicit, inspectable resource rules; no hidden randomness in consumption."""
CATALOG = {
    'capacitor': {'name':'Capacitor', 'symbol':'⚡', 'color':'#ffe073', 'effect':'Stores up to 30 GU; elevated metabolism (+2/tick) for 8 ticks.', 'class':'situational'},
    'shield': {'name':'Shield crystal', 'symbol':'◇', 'color':'#7ee8ff', 'effect':'Absorbs wall/body collision attempts for 10 ticks; no wall crossing.', 'class':'beneficial'},
    'catalyst': {'name':'Harvest catalyst', 'symbol':'✦', 'color':'#ffa85e', 'effect':'Harvests up to 8 GU/cell for 12 ticks instead of 4.', 'class':'situational'},
    'memory': {'name':'Memory spore', 'symbol':'◎', 'color':'#ce9fff', 'effect':'Longer trail (30); exploratory preference for unvisited cells for 16 ticks.', 'class':'situational'},
    'recycler': {'name':'Recycler enzyme', 'symbol':'♻', 'color':'#70f0ac', 'effect':'Sheds up to 3 tail segments into compost and reduces metabolic burden.', 'class':'situational'},
    'toxin': {'name':'Toxin', 'symbol':'×', 'color':'#ff6885', 'effect':'Transfers up to 25 battery GU to heat immediately.', 'class':'detrimental'},
    'overload': {'name':'Overload seed', 'symbol':'!', 'color':'#ff7054', 'effect':'Adds up to 40 GU but drains 5 GU/tick for 10 ticks; usually net harmful.', 'class':'detrimental'},
}
