#!/usr/bin/env python3
"""Loopback-only dashboard and classifier; intentionally no authentication for local use."""
import argparse,json
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
from src.core import load_model,classify
p=argparse.ArgumentParser();p.add_argument('--out',default='output');p.add_argument('--port',type=int,default=8765);a=p.parse_args();model=load_model()
class Handler(BaseHTTPRequestHandler):
    def respond(self,status,body,kind='application/json'):
        self.send_response(status);self.send_header('Content-Type',kind+'; charset=utf-8');self.send_header('Content-Length',str(len(body)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(body)
    def do_GET(self):
        if self.path in ('/','/dashboard.html'):
            path=Path(a.out)/'dashboard.html'
            if not path.is_file():return self.respond(404,b'{"error":"Run python run.py first"}')
            return self.respond(200,path.read_bytes(),'text/html')
        self.respond(404,b'{"error":"Not found"}')
    def do_POST(self):
        if self.path!='/api/classify':return self.respond(404,b'{"error":"Not found"}')
        try:
            n=int(self.headers.get('Content-Length','0'))
            if not 0<n<=16000:raise ValueError('Message too large or empty')
            body=json.loads(self.rfile.read(n));message=body.get('message')
            if not isinstance(message,str):raise ValueError('message must be a string')
            self.respond(200,json.dumps(classify(message,model)).encode())
        except (ValueError,TypeError,json.JSONDecodeError) as e:self.respond(400,json.dumps({'error':str(e)}).encode())
print(f'Open http://127.0.0.1:{a.port} (Ctrl+C to stop)',flush=True)
ThreadingHTTPServer(('127.0.0.1',a.port),Handler).serve_forever()
