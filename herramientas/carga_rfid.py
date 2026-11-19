"""Ensayo local RFID reproducible. Solo loopback y datos temporales ficticios.
Ejecutar con Python del proyecto, --repo RUTA --gunicorn RUTA --salida RUTA.
No cambia journal, timeouts ni reglas del producto.
"""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
import http.client
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import math
import os
from pathlib import Path
import shutil
import socket
import sqlite3
import statistics
import subprocess
import sys
import tempfile
import threading
import time
from urllib import request, error

WRAPPER = '''import json,os,time,sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo
from flask import request,g,has_request_context
import api,base_datos,registrar_asistencia
app=api.app
@app.errorhandler(sqlite3.OperationalError)
def error_sql(error):
    fd=os.open(os.environ['CARGA_TRACE']+'.errores',os.O_WRONLY|os.O_APPEND|os.O_CREAT,0o600)
    os.write(fd,(json.dumps({'tipo':type(error).__name__,'error':str(error)})+'\\n').encode());os.close(fd)
    return api.base_datos_no_disponible(error)
clock=lambda:datetime.fromisoformat(open(os.environ['CARGA_CLOCK']).read()).replace(tzinfo=ZoneInfo('America/Santiago'))
base_datos.ahora_chile=clock
registrar_asistencia.ahora_chile=clock
original=sqlite3.connect
class Cursor(sqlite3.Cursor):
    def execute(self,sql,*a,**kw):
        t=time.perf_counter()
        try:return super().execute(sql,*a,**kw)
        finally:
            if has_request_context() and hasattr(g,'escrituras') and sql.strip().split()[0].upper() in {'BEGIN','UPDATE','INSERT','DELETE'}:g.escrituras.append(time.perf_counter()-t)
class Con(sqlite3.Connection):
    def cursor(self,*a,**kw):return super().cursor(*a,**dict(kw,factory=Cursor))
    def execute(self,sql,*a,**kw):
        if sql=='BEGIN IMMEDIATE':
            t=time.perf_counter()
            try: return super().execute(sql,*a,**kw)
            finally:
                if hasattr(g,'locks'):g.locks.append(time.perf_counter()-t)
        return super().execute(sql,*a,**kw)
sqlite3.connect=lambda *a,**kw:original(*a,**dict(kw,factory=Con))
@app.before_request
def inicio():
    g.t=time.perf_counter();g.locks=[];g.escrituras=[]
@app.after_request
def fin(r):
    if request.path=='/lectura':
        d=request.get_json(silent=True) or {}
        fila={'evento':d.get('evento_id'),'uid':d.get('uid'),'pid':os.getpid(),'status':r.status_code,'resultado':(r.get_json(silent=True) or {}).get('resultado'),'segundos':time.perf_counter()-g.t,'locks':g.locks,'escrituras':g.escrituras}
        fd=os.open(os.environ['CARGA_TRACE'],os.O_WRONLY|os.O_APPEND|os.O_CREAT,0o600)
        os.write(fd,(json.dumps(fila)+'\\n').encode());os.close(fd)
    return r
'''

def percentil(xs,p):
    return sorted(xs)[max(0,math.ceil(len(xs)*p)-1)] if xs else 0

class Ensayo:
    def __init__(self,args,tmp):
        self.args=args; self.tmp=Path(tmp); self.repo=Path(args.repo).resolve()
        sys.path.insert(0,str(self.repo)); sys.path.insert(0,str(self.repo/'tests'))
        import test_auditoria as f
        self.f=f
        self.db=self.tmp/'ficticia.db'; self.template=self.tmp/'plantilla.db'
        self.trace=self.tmp/'trace.jsonl'; self.clock=self.tmp/'reloj.txt'
        self.clock.write_text('2026-11-19T08:00:00'); self.trace.touch()
        f.bd.RUTA_BASE_DATOS=str(self.template);f.bd.crear_tablas()
        with closing(sqlite3.connect(self.template)) as con:
            for p in sorted((self.repo/'migraciones').glob('*.sql')):con.executescript(p.read_text())
            for i in range(1,202):
                con.execute('INSERT INTO alumnos(id,rut,nombre_completo,curso,estado) VALUES (?,?,?,?,?)',(i,f'FICTICIO-NO-RUT-{i}','Estudiante Ficticio','1A','inactivo' if i==201 else 'activo'))
                con.execute("INSERT INTO tarjetas(alumno_id,uid,estado,fecha_registro) VALUES (?,?,?,'2026-01-01')",(i,f'FICTICIA{i:04}','bloqueada' if i==200 else 'activa'))
            con.execute("INSERT INTO totems(id,codigo,nombre,ubicacion,fecha_registro) VALUES (1,'DEMO','Totem Ficticio','Laboratorio','2026-01-01')")
            con.execute("INSERT INTO seguimiento_operadores(id,nombre_completo,usuario,password_hash,rol) VALUES (1,'Operador Ficticio','demo1',?,'administracion')",(f.generate_password_hash(f.PASSWORD),))
            con.commit()
        (self.tmp/'worker_carga.py').write_text(WRAPPER)
        self.env={k:v for k,v in os.environ.items() if not k.startswith('MPAZ_') and k.lower() not in {'http_proxy','https_proxy','all_proxy'}}
        self.env.update(MPAZ_DB_PATH=str(self.db),MPAZ_SESSION_SECRET='carga-secreto-solo-ficticio',MPAZ_API_KEY='carga-api-solo-ficticia',PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=os.pathsep.join([args.gunicorn,str(self.tmp),str(self.repo)]),CARGA_CLOCK=str(self.clock),CARGA_TRACE=str(self.trace))
        os.environ['MPAZ_API_KEY']='carga-api-solo-ficticia'
        import reenviar_pendientes as reenvio, cola_pendientes as cola
        self.reenvio=reenvio; self.cola=cola;reenvio.API_KEY=self.env['MPAZ_API_KEY']
        self.opener=request.build_opener(request.ProxyHandler({}))
        self.reset()
        self.resultados=[]
        ThreadingHTTPServer.request_queue_size=256

    def reset(self):
        shutil.copyfile(self.template,self.db)
        self.trace.write_text('');self.clock.write_text('2026-11-19T08:00:00')
        self.cola.RUTA_PENDIENTES=self.tmp/'cola.json'
        self.cola.guardar_pendiente([])

    def http(self,d,ruta='/lectura',cookie=None,timeout=20):
        t=time.perf_counter(); cab={'Content-Type':'application/json','X-API-Key':self.env['MPAZ_API_KEY']}
        if cookie:cab['Cookie']=cookie
        req=request.Request(f'http://127.0.0.1:{self.port}'+ruta,data=json.dumps(d).encode() if d is not None else None,headers=cab)
        try:
            try:r=self.opener.open(req,timeout=timeout)
            except error.HTTPError as e:r=e
            with r:status=r.status; datos=json.loads(r.read()); cookie=r.headers.get('Set-Cookie')
            return {'status':status,'resultado':datos.get('resultado'),'ms':(time.perf_counter()-t)*1000,'cookie':cookie}
        except (OSError,error.URLError,http.client.HTTPException) as e:
            return {'status':0,'resultado':type(e).__name__,'ms':(time.perf_counter()-t)*1000}

    def payload(self,i,e=None):
        return {'codigo_totem':'DEMO','uid':f'FICTICIA{i:04}','evento_id':e or f'ficticio-{i}'}

    def rafaga(self,datos):
        barrera=threading.Barrier(len(datos)); inicios=[]
        def uno(d):
            barrera.wait(timeout=20);inicios.append(time.perf_counter());return self.http(d)
        t=time.perf_counter()
        with ThreadPoolExecutor(max_workers=len(datos)) as pool:res=list(pool.map(uno,datos))
        return res,time.perf_counter()-t,(max(inicios)-min(inicios))*1000

    def filas(self):
        with closing(sqlite3.connect(self.db)) as con:
            assert con.execute('PRAGMA integrity_check').fetchall()==[('ok',)]
            assert not con.execute('PRAGMA foreign_key_check').fetchall()
            con.execute('BEGIN IMMEDIATE');con.rollback()
            return con.execute('SELECT alumno_id,fecha,hora_entrada,hora_salida,totem_entrada_id,totem_salida_id,evento_entrada_id,evento_salida_id FROM asistencias ORDER BY alumno_id').fetchall()

    def registro(self,esc,n,w,rep,res,total,disp=0,esperado=None):
        filas=self.filas(); trace=[json.loads(l) for l in self.trace.read_text().splitlines()]
        if esperado is not None:assert Counter(r['resultado'] for r in res)==Counter(esperado), (esc,Counter(r['resultado'] for r in res),esperado)
        entradas={r[6]:r for r in filas};salidas={r[7]:r for r in filas if r[7]}
        # Cada aceptación funcional registrada debe existir realmente en SQLite.
        for x in trace:
            if x['resultado']=='entrada_registrada':assert x['evento'] in entradas and entradas[x['evento']][0]==int(x['uid'][8:])
            if x['resultado']=='salida_registrada':assert x['evento'] in salidas
        assert all(r[1]=='2026-11-19' and r[2]=='08:00:00' and r[4]==1 for r in filas)
        locks=[l*1000 for x in trace for l in x['locks']]
        escrituras=[l*1000 for x in trace for l in x.get('escrituras',[])]
        ms=[r['ms'] for r in res]
        fila={'escenario':esc,'n':n,'workers':w,'repeticion':rep,'enviadas':len(res),'recibidas':len(trace),'resultados':dict(Counter(r['resultado'] for r in res)),'http':dict(Counter(str(r['status']) for r in res)),'filas':len(filas),'salidas':len(salidas),'pendientes':len(self.cola.cargar_pendientes()),'media_ms':statistics.mean(ms) if ms else 0,'p95_ms':percentil(ms,.95),'p99_ms':percentil(ms,.99),'total_s':total,'dispersion_ms':disp,'lock_p95_ms':percentil(locks,.95),'lock_max_ms':max(locks,default=0),'escritura_max_ms':max(escrituras,default=0),'pids':len(set(x['pid'] for x in trace)),'conciliado':True}
        fila['latencia_origen']='servidor' if esc in {'reenvio_dos_procesos','altas_durante_reenvio'} else 'cliente'
        with open(self.args.salida+'/muestras.jsonl','a') as muestras:
            muestras.write(json.dumps({'escenario':esc,'n':n,'workers':w,'repeticion':rep,'cliente':[{'ms':r['ms'],'status':r['status'],'resultado':r['resultado']} for r in res],'servidor':trace})+'\n')
        self.resultados.append(fila)
        with open(self.args.salida+'/resultados.jsonl','a') as out:out.write(json.dumps(fila)+'\n')
        return filas

    def servidor(self,w):
        s=socket.socket();s.bind(('127.0.0.1',0));self.port=s.getsockname()[1];s.close()
        self.log=open(self.args.salida+f'/gunicorn-{w}.log','w')
        self.proc=subprocess.Popen([sys.executable,'-m','gunicorn','--bind',f'127.0.0.1:{self.port}','--workers',str(w),'--worker-class','sync','--timeout','30','--no-control-socket','worker_carga:app'],cwd=self.repo,env=self.env,stdout=self.log,stderr=self.log)
        for _ in range(200):
            if self.proc.poll() is not None:raise RuntimeError('Gunicorn no arrancó')
            if self.http(None,'/estado')['status']==200:break
            time.sleep(.05)
        else:raise RuntimeError('Gunicorn timeout')
        self.reenvio.API_URL=f'http://127.0.0.1:{self.port}/lectura'

    def parar(self):
        self.proc.terminate()
        try:self.proc.wait(timeout=10)
        except subprocess.TimeoutExpired:self.proc.kill();self.proc.wait(timeout=5)
        self.log.close()

    def basicos(self,n,w,rep):
        for esc in ['unicos','duplicados','mezcla','antirrebote','salida','rechazos','mixto']:
            self.reset();datos=[self.payload(i) for i in range(1,n+1)]
            if esc=='duplicados':datos=[self.payload(1)]*n
            if esc=='mezcla':datos=[self.payload(i//2+1) for i in range(n)]
            if esc=='antirrebote':datos=[self.payload(1,f'ficticio-{i}') for i in range(n)]
            if esc=='salida':
                pre,_,_=self.rafaga(datos);assert all(r['resultado']=='entrada_registrada' for r in pre)
                self.trace.write_text('');self.clock.write_text('2026-11-19T08:01:00');datos=[self.payload(i,f'salida-{i}') for i in range(1,n+1)]
            if esc=='rechazos':
                datos=[]
                tipos=['tarjeta_bloqueada','alumno_inactivo','totem_no_autorizado']
                for i in range(n):
                    d=self.payload(200 if i%3==0 else 201 if i%3==1 else 1,f'rechazo-{i}')
                    if i%3==2:d['codigo_totem']='TOTEM-FICTICIO-NO-AUTORIZADO'
                    datos.append(d)
            if esc=='mixto':
                login=self.http({'usuario':'demo1','password':self.f.PASSWORD},'/panel/login-individual')
                assert login['status']==200
                cookie=login['cookie'].split(';')[0]
                with ThreadPoolExecutor(max_workers=1) as pool:
                    futuro=pool.submit(lambda:[self.http(None,'/panel/sesion',cookie=cookie) for _ in range(n)])
                    res,total,disp=self.rafaga(datos);sesiones=futuro.result()
                assert all(r['status']==200 for r in sesiones)
            else:res,total,disp=self.rafaga(datos)
            esp=['entrada_registrada']*n
            if esc=='duplicados':esp=['entrada_registrada']+['evento_repetido']*(n-1)
            if esc=='mezcla':esp=['entrada_registrada']*(n//2)+['evento_repetido']*(n//2)
            if esc=='antirrebote':esp=['entrada_registrada']+['lectura_repetida']*(n-1)
            if esc=='salida':esp=['salida_registrada']*n
            if esc=='rechazos':esp=[tipos[i%3] for i in range(n)]
            filas=self.registro(esc,n,w,rep,res,total,disp,esp)
            assert len(filas)==(0 if esc=='rechazos' else 1 if esc in {'duplicados','antirrebote'} else n//2 if esc=='mezcla' else n)
            assert all((r[3]=='08:01:00' and r[5]==1) if esc=='salida' else r[3] is None for r in filas)

    def bloqueo(self,n,w,rep,seg):
        self.reset();datos=[self.payload(i) for i in range(1,n+1)]
        listo=threading.Event()
        def bloquear():
            with closing(sqlite3.connect(self.db)) as con:
                con.execute('BEGIN IMMEDIATE');listo.set();time.sleep(seg);con.rollback()
        hilo=threading.Thread(target=bloquear);hilo.start();listo.wait()
        res,total,disp=self.rafaga(datos);hilo.join()
        filas=self.registro('bloqueo_corto' if seg<5 else 'bloqueo_largo',n,w,rep,res,total,disp)
        assert all(r['status'] in {200,503} for r in res)
        fallidos=[d for d,r in zip(datos,res) if r['status']==503]
        assert len(filas)==n-len(fallidos)
        for d in fallidos:self.cola.agregar_pendiente(d)
        self.trace.write_text('');t=time.perf_counter();reintentos=[]
        for d in self.cola.cargar_pendientes():
            t0=time.perf_counter();ok,r=self.reenvio.enviar_pendiente(d);assert ok;self.cola.eliminar_pendiente(d['evento_id']);reintentos.append({'status':200,'resultado':r['resultado'],'ms':(time.perf_counter()-t0)*1000})
        assert len(self.filas())==n and not self.cola.cargar_pendientes()
        self.registro('recuperacion_bloqueo',n,w,rep,reintentos,time.perf_counter()-t)

    def conexiones(self,n,w,rep):
        for esc in ['desconexion','respuesta_perdida','reenvio_dos_procesos','rechazo_pendiente']:
            self.reset();datos=[self.payload(i) for i in range(1,n+1)]
            for d in datos:self.cola.agregar_pendiente(d)
            if esc=='rechazo_pendiente':
                with closing(sqlite3.connect(self.db)) as con:con.execute("UPDATE tarjetas SET estado='bloqueada' WHERE alumno_id<=?",(n,));con.commit()
            t=time.perf_counter();res=[]
            def intento(d):
                t0=time.perf_counter();ok,r=self.reenvio.enviar_pendiente(d)
                return {'status':200 if ok else 0,'resultado':r['resultado'],'ms':(time.perf_counter()-t0)*1000}
            if esc=='desconexion':
                s=socket.socket();s.bind(('127.0.0.1',0));puerto=s.getsockname()[1] # reservado pero sin listen: rechazo real
                original=self.reenvio.API_URL;self.reenvio.API_URL=f'http://127.0.0.1:{puerto}/lectura'
                try:
                    with ThreadPoolExecutor(max_workers=n) as pool:res=list(pool.map(intento,datos))
                    assert all(x['resultado']=='sin_conexion' for x in res)
                    assert not self.filas() and len(self.cola.cargar_pendientes())==n
                finally:self.reenvio.API_URL=original;s.close()
            if esc=='respuesta_perdida':
                ensayo=self
                class Perdida(BaseHTTPRequestHandler):
                    def do_POST(self):
                        d=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                        r=ensayo.http(d);assert r['resultado']=='entrada_registrada'
                        self.close_connection=True # Sin encabezados después del commit real.
                    def log_message(self,*a):pass
                proxy=ThreadingHTTPServer(('127.0.0.1',0),Perdida);hilo=threading.Thread(target=proxy.serve_forever);hilo.start()
                original=self.reenvio.API_URL;self.reenvio.API_URL=f'http://127.0.0.1:{proxy.server_port}/lectura'
                try:
                    with ThreadPoolExecutor(max_workers=n) as pool:res=list(pool.map(intento,datos))
                    assert all(x['status']==0 for x in res)
                    assert len(self.filas())==n and len(self.cola.cargar_pendientes())==n
                finally:self.reenvio.API_URL=original;proxy.shutdown();proxy.server_close();hilo.join()
            if esc=='reenvio_dos_procesos':
                codigo="""import os,sys,time,json
from pathlib import Path
import cola_pendientes as c,reenviar_pendientes as r
c.RUTA_PENDIENTES=Path(sys.argv[1])
while not Path(sys.argv[2]).exists():time.sleep(.005)
for d in c.cargar_pendientes():
    ok,res=r.enviar_pendiente(d)
    if ok:c.eliminar_pendiente(d['evento_id'])
"""
                gate=self.tmp/'gate';gate.unlink(missing_ok=True)
                env=dict(self.env,MPAZ_API_URL=self.reenvio.API_URL)
                ps=[subprocess.Popen([sys.executable,'-c',codigo,str(self.cola.RUTA_PENDIENTES),str(gate)],cwd=self.repo,env=env) for _ in range(2)]
                gate.touch()
                for p in ps:assert p.wait(timeout=60)==0
            else:
                def reenviar(d):
                    t0=time.perf_counter();ok,r=self.reenvio.enviar_pendiente(d)
                    if ok:self.cola.eliminar_pendiente(d['evento_id'])
                    return {'status':200,'resultado':r['resultado'],'ms':(time.perf_counter()-t0)*1000}
                with ThreadPoolExecutor(max_workers=n) as pool:res+=list(pool.map(reenviar,datos))
            if esc=='reenvio_dos_procesos':
                res=[{'status':x['status'],'resultado':x['resultado'],'ms':x['segundos']*1000} for x in map(json.loads,self.trace.read_text().splitlines())]
            if esc=='rechazo_pendiente':assert not self.filas() and len(self.cola.cargar_pendientes())==n
            else:assert len(self.filas())==n and not self.cola.cargar_pendientes()
            self.registro(esc,n,w,rep,res,time.perf_counter()-t)

    def altas_y_timeout(self,n,w):
        self.reset()
        with closing(sqlite3.connect(self.db)) as con:
            con.execute("UPDATE tarjetas SET estado='activa' WHERE alumno_id=200");con.commit()
        iniciales=[self.payload(i) for i in range(1,n+1)]
        nuevas=[self.payload(i) for i in range(n+1,2*n+1)]
        for d in iniciales:self.cola.agregar_pendiente(d)
        codigo="""import sys,time
from pathlib import Path
import cola_pendientes as c,reenviar_pendientes as r
c.RUTA_PENDIENTES=Path(sys.argv[1]);lote=c.cargar_pendientes()
Path(sys.argv[3]).touch()
while not Path(sys.argv[2]).exists():time.sleep(.005)
for d in lote:
    ok,res=r.enviar_pendiente(d)
    if ok:c.eliminar_pendiente(d['evento_id'])
"""
        gate=self.tmp/'gate-altas';gate.unlink(missing_ok=True)
        env=dict(self.env,MPAZ_API_URL=self.reenvio.API_URL)
        ready=[self.tmp/f'ready-{i}' for i in range(2)]
        for p in ready:p.unlink(missing_ok=True)
        ps=[subprocess.Popen([sys.executable,'-c',codigo,str(self.cola.RUTA_PENDIENTES),str(gate),str(r)],cwd=self.repo,env=env) for r in ready]
        limite=time.monotonic()+20
        while not all(p.exists() for p in ready):
            assert time.monotonic()<limite;time.sleep(.01)
        t=time.perf_counter();gate.touch()
        for d in nuevas:self.cola.agregar_pendiente(d)
        for p in ps:assert p.wait(timeout=60)==0
        assert {d['evento_id'] for d in self.cola.cargar_pendientes()}=={d['evento_id'] for d in nuevas}
        assert len(self.filas())==n
        for d in self.cola.cargar_pendientes():
            ok,r=self.reenvio.enviar_pendiente(d);assert ok;self.cola.eliminar_pendiente(d['evento_id'])
        assert len(self.filas())==2*n and not self.cola.cargar_pendientes()
        trace=list(map(json.loads,self.trace.read_text().splitlines()))
        res=[{'status':x['status'],'resultado':x['resultado'],'ms':x['segundos']*1000} for x in trace]
        self.registro('altas_durante_reenvio',n,w,1,res,time.perf_counter()-t)

    def ejecutar(self):
        for w in [1,2,3]:
            self.servidor(w)
            try:
                self.reset();assert self.http(self.payload(1))['resultado']=='entrada_registrada';assert len(self.filas())==1
                for n in [10,50,100]:
                    for rep in range(1,self.args.repeticiones+1):
                        self.basicos(n,w,rep);self.bloqueo(n,w,rep,.2);self.conexiones(n,w,rep)
                        print(f'OK workers={w} n={n} repeticion={rep}',flush=True)
                    self.bloqueo(n,w,0,5.5)
                    if self.args.disco:self.altas_y_timeout(n,w)
            finally:self.parar()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--gunicorn',required=True);p.add_argument('--salida',required=True);p.add_argument('--repeticiones',type=int,default=5);p.add_argument('--disco',action='store_true');a=p.parse_args()
    if not __debug__:p.error('Ejecutar sin optimizacion: las conciliaciones usan assert')
    if (Path(a.salida)/'resultados.jsonl').exists():p.error('Elegir una salida nueva; no mezclar ejecuciones')
    Path(a.salida).mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='mpaz-carga-ficticia-',dir=a.salida if a.disco else None) as tmp:
        e=Ensayo(a,tmp)
        with closing(sqlite3.connect(e.template)) as con:
            meta={'python':sys.version,'sqlite':sqlite3.sqlite_version,'cpu_logicas':os.cpu_count(),'journal':con.execute('PRAGMA journal_mode').fetchone()[0],'busy_timeout_ms':con.execute('PRAGMA busy_timeout').fetchone()[0],'synchronous':con.execute('PRAGMA synchronous').fetchone()[0],'workers':[1,2,3],'repeticiones':a.repeticiones,'filesystem':subprocess.check_output(['stat','-f','-c','%T',tmp],text=True).strip()}
        Path(a.salida+'/entorno.json').write_text(json.dumps(meta,indent=2))
        e.ejecutar()
