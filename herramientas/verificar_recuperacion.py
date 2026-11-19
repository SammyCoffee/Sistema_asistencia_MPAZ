"""Complemento: timeout real y liberación de transacciones después de un timeout."""
import argparse
from contextlib import closing
from concurrent.futures import ThreadPoolExecutor
import json
import socket
import sqlite3
import sys
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from carga_rfid import Ensayo

p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--gunicorn',required=True);p.add_argument('--salida',required=True);a=p.parse_args();a.repeticiones=1;a.disco=True
Path(a.salida).mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory(prefix='mpaz-complemento-ficticio-',dir=a.salida) as tmp:
 e=Ensayo(a,tmp);e.servidor(3)
 try:
  for n in [10,50,100]:
   e.reset();datos=[e.payload(i) for i in range(1,n+1)]
   for d in datos:e.cola.agregar_pendiente(d)
   estado={'respuestas':0};lock=threading.Lock()
   class Demorada(BaseHTTPRequestHandler):
    def do_POST(self):
     d=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
     r=e.http(d)
     assert r['resultado']=='entrada_registrada'
     with lock:estado['respuestas']+=1
     time.sleep(.25)
     try:self.send_response(200);self.end_headers();self.wfile.write(b'{}')
     except OSError:pass
    def log_message(self,*args):pass
   ThreadingHTTPServer.request_queue_size=256
   proxy=ThreadingHTTPServer(('127.0.0.1',0),Demorada);hilo=threading.Thread(target=proxy.serve_forever);hilo.start()
   def timeout(d):
    import urllib.request,urllib.error
    req=urllib.request.Request(f'http://127.0.0.1:{proxy.server_port}',data=json.dumps(d).encode(),headers={'Content-Type':'application/json'})
    try:
     urllib.request.build_opener(urllib.request.ProxyHandler({})).open(req,timeout=.05)
     raise AssertionError('Se esperaba timeout')
    except (TimeoutError,urllib.error.URLError):return True
   with ThreadPoolExecutor(max_workers=n) as pool:assert all(pool.map(timeout,datos))
   limite=time.monotonic()+30
   while estado['respuestas']<n:
    assert time.monotonic()<limite;time.sleep(.01)
   proxy.shutdown();proxy.server_close();hilo.join()
   assert len(e.filas())==n and len(e.cola.cargar_pendientes())==n
   for d in e.cola.cargar_pendientes():
    ok,r=e.reenvio.enviar_pendiente(d);assert ok and r['resultado']=='evento_repetido';e.cola.eliminar_pendiente(d['evento_id'])
   assert len(e.filas())==n and not e.cola.cargar_pendientes()
   with closing(sqlite3.connect(e.db,timeout=.05)) as con:
    t=time.perf_counter();con.execute('BEGIN IMMEDIATE');espera=time.perf_counter()-t;con.rollback()
   if n==10:e.bloqueo(10,3,1,5.5)
   fila={'n':n,'timeout_cliente_ms':50,'demora_respuesta_ms':250,'commit_confirmado_en_proxy':estado['respuestas'],'filas':len(e.filas()),'pendientes':0,'lock_post_recuperacion_ms':espera*1000}
   with open(a.salida+'/complemento.jsonl','a') as out:out.write(json.dumps(fila)+'\n')
   print('TIMEOUT_RECUPERADO',json.dumps(fila),flush=True)
  errores=Path(str(e.trace)+'.errores').read_text().splitlines()
  assert errores and all(json.loads(x)['error']=='database is locked' for x in errores)
  Path(a.salida+'/errores_sqlite.json').write_text(json.dumps([json.loads(x) for x in errores],indent=2))
 finally:e.parar()
