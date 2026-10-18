import json
import threading
import unittest
import urllib.request
import urllib.error
from http.server import ThreadingHTTPServer
import server
from engine import World
class HTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.http=ThreadingHTTPServer(('127.0.0.1',0),server.Handler)
        cls.thread=threading.Thread(target=cls.http.serve_forever,daemon=True);cls.thread.start()
        cls.base='http://127.0.0.1:'+str(cls.http.server_port)
    @classmethod
    def tearDownClass(cls):cls.http.shutdown();cls.http.server_close();cls.thread.join()
    def call(self,path,body=None):
        req=urllib.request.Request(self.base+path,data=None if body is None else json.dumps(body).encode(),headers={'Content-Type':'application/json'})
        try:
            with urllib.request.urlopen(req) as r:return r.status,json.load(r)
        except urllib.error.HTTPError as e:return e.code,json.load(e)
    def setUp(self):self.call('/api/reset',{'seed':42})
    def test_state_step_replay(self):
        _,s=self.call('/api/state');self.assertEqual(s['tick'],0)
        _,s=self.call('/api/step',{'tick':0,'direction':'+y','skill':'scan'})
        _,log=self.call('/api/replay');w=World(log['seed'])
        for a in log['actions']:w.step(**a)
        self.assertEqual(s['hash'],w.state()['hash'])
    def test_auto_http_replay(self):
        _,s=self.call('/api/step',{'tick':0,'auto':True})
        self.assertEqual(s['decision']['mode'],'auto')
        _,log=self.call('/api/replay');w=World(log['seed'])
        for a in log['actions']:w.step(**a)
        self.assertEqual(s['hash'],w.state()['hash'])
    def test_input_output_and_replay(self):
        code,s=self.call('/api/input',{'tick':0,'input':{'label':'Experiment','kind':'stress','value':3}})
        self.assertEqual(code,200);self.assertEqual(len(s['systems']['pending']),1)
        _,s=self.call('/api/step',{'tick':0,'auto':True})
        _,out=self.call('/api/output');self.assertEqual(out['applied_inputs'][0]['label'],'Experiment')
        _,log=self.call('/api/replay');w=World(log['seed'])
        for a in log['actions']:
            if a.get('op')=='input':w.queue_input(a['data'])
            else:w.step(**a)
        self.assertEqual(s['hash'],w.state()['hash'])
    def test_input_invalid(self):
        code,_=self.call('/api/input',{'tick':0,'input':{'label':'bad','kind':'stress','value':100}})
        self.assertEqual(code,400);self.assertEqual(self.call('/api/state')[1]['tick'],0)
    def test_stale_action(self):
        self.call('/api/step',{'tick':0});status,_=self.call('/api/step',{'tick':0})
        self.assertEqual(status,409);self.assertEqual(self.call('/api/state')[1]['tick'],1)
    def test_invalid(self):
        self.assertEqual(self.call('/api/step',{'tick':0,'direction':'bad'})[0],400)
        self.assertEqual(self.call('/api/state')[1]['tick'],0)
    def test_static(self):
        with urllib.request.urlopen(self.base+'/') as r:self.assertIn(b'Matrix Snake',r.read())
