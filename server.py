"""Local development service: no dependencies; one shared world, serialized actions."""
import argparse
import json
import threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from engine import World
from instructions import interpret
ROOT=Path(__file__).parent/'web'
world=World(); lock=threading.Lock()
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw): super().__init__(*a,directory=str(ROOT),**kw)
    def log_message(self,format,*args):
        if len(args)>1 and str(args[1]) in ('200','304'):return
        super().log_message(format,*args)
    def respond(self,data,status=200):
        body=json.dumps(data).encode(); self.send_response(status)
        self.send_header('Content-Type','application/json'); self.send_header('Cache-Control','no-store')
        self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        if self.path=='/api/state':
            with lock: self.respond(world.state())
        elif self.path=='/api/output':
            with lock:self.respond(world.systems.output(world) if world.systems else {'error':'Framework disabled'})
        elif self.path=='/api/replay':
            with lock: self.respond({'version':4,'systems':bool(world.systems),'seed':world.seed,'snakes':len(world.agents),'actions':world.history})
        else: super().do_GET()
    def do_POST(self):
        global world
        try:
            length=int(self.headers.get('Content-Length',0))
            if not 0 < length <= 4096: raise ValueError('Invalid request size')
            body=json.loads(self.rfile.read(length))
            with lock:
                if self.path=='/api/interpret':return self.respond(interpret(body.get('text')))
                if self.path=='/api/reset':
                    seed=body.get('seed',42)
                    if type(seed) is not int: raise ValueError('Seed must be an integer')
                    world=World(seed)
                elif self.path=='/api/input':
                    if body.get('tick')!=world.tick:return self.respond({'error':'Stale tick; refresh state'},409)
                    world.queue_input(body.get('input'))
                elif self.path=='/api/step':
                    if body.get('tick')!=world.tick: return self.respond({'error':'Stale tick; refresh state'},409)
                    world.step(body.get('direction'),body.get('skill'),body.get('auto',False))
                else: return self.respond({'error':'Not found'},404)
                self.respond(world.state())
        except (ValueError,TypeError,AttributeError) as exc: self.respond({'error':str(exc)},400)
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--host',default='127.0.0.1'); p.add_argument('--port',type=int,default=8765)
    a=p.parse_args(); print(f'TAYOH: http://{a.host}:{a.port}',flush=True)
    ThreadingHTTPServer((a.host,a.port),Handler).serve_forever()
