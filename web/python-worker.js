// Pinned, self-hosted Pyodide: no JavaScript port or second simulation model.
const ready=(async()=>{
  importScripts('./vendor/pyodide/pyodide.js');
  const py=await loadPyodide({indexURL:new URL('./vendor/pyodide/',self.location.href).href});
  for(const file of ['engine.py','systems.py','resources.py']){
    const r=await fetch(new URL('./py/'+file,self.location.href).href+'?v='+(new URL(self.location.href).searchParams.get('v')||'local'));if(!r.ok)throw Error('Missing simulation source: '+file);
    py.FS.writeFile('/home/pyodide/'+file,await r.text());
  }
  py.runPython(`
import sys, json
sys.path.insert(0, '/home/pyodide')
from engine import World
world = World(42)
def dispatch(message):
    global world
    path = message['path']
    body = message.get('body') or {}
    if path == '/api/state': return world.state()
    if path == '/api/output': return world.systems.output(world)
    if path == '/api/replay':
        return {'version':4, 'runtime':'pyodide-0.27.7', 'systems':True, 'seed':world.seed, 'snakes':len(world.agents), 'actions':world.history}
    if path == '/api/reset':
        seed=body.get('seed',42)
        if type(seed) is not int: raise ValueError('Seed must be an integer')
        world=World(seed)
        return world.state()
    if path in ('/api/step','/api/input'):
        if body.get('tick') != world.tick: raise ValueError('Stale tick; refresh state')
        if path == '/api/input': return world.queue_input(body.get('input'))
        return world.step(body.get('direction'),body.get('skill'),body.get('auto',False))
    raise ValueError('Unknown operation')
`);
  return py;
})();
// A single serialized command queue includes initialization and every mutation.
let queue=Promise.resolve();
self.onmessage=e=>{queue=queue.then(async()=>{try{const py=await ready;py.globals.set('_request_json',JSON.stringify(e.data));const result=JSON.parse(py.runPython('json.dumps(dispatch(json.loads(_request_json)))'));self.postMessage({id:e.data.id,result});}catch(error){self.postMessage({id:e.data.id,error:String(error.message||error)});}});};
