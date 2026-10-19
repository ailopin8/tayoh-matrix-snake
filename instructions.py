"""Deterministic, bounded language-to-policy adapter. Never executes user code."""
import re
RECIPES = {
 'repair': ('protector','repair','Help the boundary repair more damage','Spend up to 5 reserve units repairing each tick; reserve can run out sooner.'),
 'conserve': ('protector','conserve','Help the boundary conserve its energy','Limit repair to 1 reserve unit per tick; damage may accumulate faster.'),
 'cautious': ('healer','cautious','Make the food producer more cautious','Require boundary integrity at least 65 (was 40); produce at most every 3 ticks. Food may become scarcer.'),
 'normal_food': ('healer','default','Restore normal food production','Restore boundary threshold 40 and production opportunity every tick; all other safety checks remain.'),
 'cooperate': ('children','cooperate','Make the snakes give each other more space','Discount food targets nearer the other snake by 65%, and shared targets by 50%; both snakes still need food.'),
 'compete': ('children','compete','Make the snakes compete more strongly','Discount nearer-opponent targets by only 10% and do not discount shared targets; collision avoidance still applies.'),
 'restore': ('all','default','Restore the original rules','Restore original repair, production and competition policies; this does not reset the world or replenish reserves.')}
def interpret(text):
    if not isinstance(text,str) or not 1 <= len(text.strip()) <= 240:
        raise ValueError('Write an instruction of 1–240 characters.')
    normalized = re.sub(r'[^a-z0-9 ]','',text.lower()).strip()
    normalized = ' '.join(normalized.split())
    for key,(role,mode,phrase,effect) in RECIPES.items():
        if normalized in (key.replace('_',''),phrase.lower()):
            return {'recipe':key,'role':role,'mode':mode,'text':phrase,'effect':effect,
                    'scope':'Bounded rule selection; not arbitrary code generation'}
    raise ValueError('Instruction not recognized. Choose one of the example instructions; free-form algorithm generation is not enabled.')

def describe(role,mode):
    if mode=='default':return 'Original rules'
    return next((r[2] for r in RECIPES.values() if r[0]==role and r[1]==mode),'Original rules')
