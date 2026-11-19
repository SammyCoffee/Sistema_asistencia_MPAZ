"""Migración 005 contra código/esquema d0d2c80 y datos exclusivamente ficticios.

Gunicorn opcional: MPAZ_TEST_GUNICORN_PATH=/tmp/mpaz-migracion005-gunicorn
No extrae bases históricas, no usa red externa ni configuración escolar.
"""
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
import json
import os
from pathlib import Path
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
from urllib import request, error

import test_auditoria as fixtures

ROOT = fixtures.ROOT
SQL = (ROOT / 'migraciones/005_seguridad_web.sql').read_text()
BASE = 'd0d2c807710066fc41f5fe1922f4452c258b8270'


def snapshot(con, tablas):
    return {t: con.execute('SELECT * FROM "' + t + '" ORDER BY rowid').fetchall() for t in tablas}


def esquema(con):
    return con.execute('SELECT type,name,tbl_name,sql FROM sqlite_master ORDER BY type,name').fetchall()


class Migracion005Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.codigo = tempfile.TemporaryDirectory(prefix='mpaz-codigo-d0d2c80-')
        cls.addClassCleanup(cls.codigo.cleanup)
        cls.anterior = Path(cls.codigo.name)
        nombres = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE], cwd=ROOT, text=True).splitlines()
        # Lista permitida de fuentes: nunca materializar .db, secretos o respaldos.
        for nombre in nombres:
            if Path(nombre).suffix not in {'.py', '.sql'}:
                continue
            destino = cls.anterior / nombre
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_bytes(subprocess.check_output(['git', 'show', f'{BASE}:{nombre}'], cwd=ROOT))
        cls.clave = fixtures.generate_password_hash(fixtures.PASSWORD)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='mpaz-m005-ficticia-')
        self.addCleanup(self.tmp.cleanup)
        self.ruta = Path(self.tmp.name) / 'ficticia.db'
        self.entorno = dict(os.environ, MPAZ_DB_PATH=str(self.ruta),
                            MPAZ_SESSION_SECRET='m005-secreto-ficticio-local',
                            MPAZ_API_KEY='m005-api-ficticia', PYTHONDONTWRITEBYTECODE='1')
        self.entorno.pop('PYTHONPATH', None)
        codigo = """from pathlib import Path
import base_datos as bd
bd.crear_tablas()
con=bd.obtener_conexion()
for archivo in sorted(Path('migraciones').glob('*.sql')):
    con.executescript(archivo.read_text())
con.close()
"""
        subprocess.run([sys.executable, '-c', codigo], cwd=self.anterior, env=self.entorno,
                       check=True, capture_output=True, text=True, timeout=20)
        self.con = sqlite3.connect(self.ruta)
        self.addCleanup(self.con.close)
        self.con.execute('PRAGMA foreign_keys=ON')
        self.con.executemany('INSERT INTO seguimiento_operadores(id,nombre_completo,usuario,password_hash,rol) VALUES (?,?,?,?,?)',
                             [(1, 'Administracion Ficticia', 'demo1', self.clave, 'administracion'),
                              (2, 'Direccion Ficticia', 'demo2', self.clave, 'direccion')])
        self.con.execute("INSERT INTO usuarios VALUES (1,'Docente Ficticio','profe1',?,'profesor','activo','2026-01-01')", (self.clave,))
        self.con.executemany('INSERT INTO alumnos VALUES (?,?,?,?,?,?)',
                             [(1,'DEMO-NO-RUT-1','Estudiante Ficticio Uno','1A','activo',None),
                              (2,'DEMO-NO-RUT-2','Estudiante Ficticio Dos','1A','inactivo','2026-10-01')])
        self.con.executemany('INSERT INTO tarjetas VALUES (?,?,?,?,?,?,?,?)',
                             [(1,1,'FICTICIA-001','activa','2026-01-01','2026-01-02',None,None),
                              (2,2,'FICTICIA-002','bloqueada','2026-01-01','2026-01-02','2026-10-01',None)])
        self.con.execute("INSERT INTO totems(id,codigo,nombre,ubicacion,fecha_registro) VALUES (1,'DEMO','Totem Ficticio','Laboratorio','2026-01-01')")
        self.con.execute("INSERT INTO asistencias VALUES (1,1,'2026-11-16','08:00:00',1,'ficticio-original','08:00:00','16:00:00','manual',1,1,'ficticio-entrada','ficticio-salida')")
        self.con.execute("INSERT INTO asignaturas VALUES (1,'Asignatura Ficticia','activo')")
        self.con.execute("INSERT INTO profesores_cursos VALUES (1,1,'1A',1,'activo')")
        self.con.execute("INSERT INTO sesiones_clase VALUES (1,1,'2026-11-16','08:00','por_clase','confirmada','2026-11-16 08:00','2026-11-16 09:00')")
        self.con.execute("INSERT INTO asistencias_clase VALUES (1,1,1,'presente','Observacion ficticia','2026-11-16 09:00')")
        self.con.execute("INSERT INTO calendario_jornadas(id,fecha,condicion,motivo) VALUES (1,'2026-11-16','lectiva','Ficticio')")
        self.con.execute("INSERT INTO calendario_eventos(id,fecha,titulo) VALUES (1,'2026-11-16','Evento ficticio')")
        self.con.execute("INSERT INTO calendario_auditoria(id,jornada_id,accion,valor_nuevo) VALUES (1,1,'crear','{}')")
        self.con.execute("INSERT INTO seguimiento_casos(id,alumno_id,sesion_clase_id,curso,fecha_evento,tipo,descripcion,creado_por_rol,creado_por_usuario_id,creado_por_operador_id) VALUES (1,1,1,'1A','2026-11-16','otro','Caso ficticio','docente',1,1)")
        self.con.execute("INSERT INTO seguimiento_mensajes(id,caso_id,autor_rol,autor_usuario_id,mensaje,autor_operador_id) VALUES (1,1,'administracion',1,'Mensaje ficticio',1)")
        self.con.execute("INSERT INTO seguimiento_contactos(id,caso_id,canal,resultado,registrado_por_usuario_id,registrado_por_operador_id) VALUES (1,1,'otro','Ficticio',1,1)")
        self.con.execute("INSERT INTO seguimiento_avisos(id,caso_id,destinatario_rol,destinatario_usuario_id,destinatario_operador_id) VALUES (1,1,'direccion',1,2)")
        self.con.commit()
        self.tablas = [r[0] for r in self.con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        self.antes = snapshot(self.con, self.tablas)
        self.esquema_antes = esquema(self.con)
        self.assertEqual(self.con.execute('PRAGMA foreign_key_check').fetchall(), [])
        self.dbpatch = patch.object(fixtures.bd, 'RUTA_BASE_DATOS', str(self.ruta))
        self.dbpatch.start()
        self.addCleanup(self.dbpatch.stop)

    def comprobar_conservacion(self):
        self.assertEqual(snapshot(self.con, self.tablas), self.antes)
        for objeto in self.esquema_antes:
            self.assertIn(objeto, esquema(self.con))
        self.assertEqual(self.con.execute('PRAGMA integrity_check').fetchall(), [('ok',)])
        self.assertEqual(self.con.execute('PRAGMA foreign_key_check').fetchall(), [])

    def test_estructura_y_conservacion_desde_d0d2c80(self):
        self.assertNotIn('web_sesiones', self.tablas)
        self.con.executescript(SQL)
        nuevos = set(esquema(self.con)) - set(self.esquema_antes)
        self.assertEqual({(r[0],r[1]) for r in nuevos}, {
            ('table','web_login_intentos'), ('table','web_sesiones'),
            ('index','idx_web_intentos_expira'), ('index','idx_web_sesiones_expira'),
            ('index','sqlite_autoindex_web_login_intentos_1'), ('index','sqlite_autoindex_web_sesiones_1')})
        self.assertEqual([r[1] for r in self.con.execute('PRAGMA table_info(web_sesiones)')],
                         ['token_hash','tipo','identidad_id','credencial_firma','creada','actividad','expira'])
        self.comprobar_conservacion()

    def test_segunda_aplicacion_conserva_incluso_seguridad(self):
        self.con.executescript(SQL)
        self.con.execute("INSERT INTO web_login_intentos VALUES ('hash-ficticio',7,9999999999)")
        self.con.execute("INSERT INTO web_sesiones VALUES ('token-ficticio','operador',1,'firma-ficticia',1,2,9999999999)")
        self.con.commit()
        antes = snapshot(self.con, self.tablas + ['web_login_intentos','web_sesiones'])
        ddl = esquema(self.con)
        self.con.executescript(SQL)
        self.assertEqual(snapshot(self.con, list(antes)), antes)
        self.assertEqual(esquema(self.con), ddl)
        self.comprobar_conservacion()

    def test_fallo_intermedio_requiere_rollback(self):
        # Conflicto ficticio de namespace: el índice no puede ocupar nombre de tabla.
        self.con.execute('CREATE TABLE idx_web_sesiones_expira (ficticio TEXT)')
        self.con.commit()
        previo = esquema(self.con)
        with self.assertRaises(sqlite3.OperationalError):
            self.con.executescript(SQL)
        self.assertTrue(self.con.in_transaction)
        self.con.rollback()
        self.assertEqual(esquema(self.con), previo)
        self.comprobar_conservacion()

    def test_bloqueo_escritura_no_deja_esquema_parcial(self):
        with closing(sqlite3.connect(self.ruta, timeout=0.05)) as otra:
            otra.execute('BEGIN IMMEDIATE')
            self.con.execute('PRAGMA busy_timeout=50')
            with self.assertRaisesRegex(sqlite3.OperationalError, 'locked'):
                self.con.executescript(SQL)
            self.assertFalse(self.con.in_transaction)
            otra.rollback()
        self.assertEqual(esquema(self.con), self.esquema_antes)
        self.con.executescript(SQL)
        self.comprobar_conservacion()

    def test_if_not_exists_no_valida_esquema_preexistente(self):
        self.con.execute('CREATE TABLE web_sesiones(token_hash TEXT, expira REAL)')
        self.con.commit()
        self.con.executescript(SQL)  # SQLite acepta esta tabla incompatible sin repararla.
        self.assertEqual(len(self.con.execute('PRAGMA table_info(web_sesiones)').fetchall()), 2)
        cliente = fixtures.api.app.test_client()
        respuesta = cliente.post('/panel/login-individual', json={'usuario':'demo1','password':fixtures.PASSWORD})
        self.assertEqual(respuesta.status_code, 503)
        self.assertEqual(self.con.execute('SELECT count(*) FROM web_sesiones').fetchone()[0], 0)
        self.comprobar_conservacion()

    def test_restricciones_de_seguridad(self):
        self.con.executescript(SQL)
        for sql in ["INSERT INTO web_login_intentos VALUES ('ficticio',-1,1)",
                    "INSERT INTO web_sesiones VALUES ('ficticio','administrador',1,'firma',1,1,2)",
                    "INSERT INTO web_sesiones VALUES ('ficticio','docente',NULL,'firma',1,1,2)"]:
            with self.subTest(sql=sql), self.assertRaises(sqlite3.IntegrityError):
                self.con.execute(sql)
            self.con.rollback()
        self.comprobar_conservacion()

    def test_sesiones_tres_roles_sobre_base_migrada(self):
        self.con.executescript(SQL)
        for usuario, login, privada, logout in [
            ('demo1','/panel/login-individual','/panel/sesion','/panel/logout'),
            ('demo2','/seguimiento/operador/login','/seguimiento/operador/sesion','/seguimiento/operador/logout'),
            ('profe1','/profesor/login','/profesor/sesion','/profesor/logout')]:
            with self.subTest(usuario=usuario):
                cliente = fixtures.api.app.test_client()
                self.assertEqual(cliente.post(login,json={'usuario':usuario,'password':fixtures.PASSWORD}).status_code, 200)
                cookie = cliente.get_cookie('session').value
                otro = fixtures.api.app.test_client(); otro.set_cookie('session',cookie)
                self.assertEqual(otro.get(privada).status_code, 200)
                token = cliente.get('/panel/csrf-token').json['csrf_token'] if usuario=='demo1' else cliente.get(privada).json['csrf_token']
                if usuario == 'demo2':
                    self.assertEqual(cliente.get('/alumnos').status_code,401)
                if usuario == 'profe1':
                    self.assertEqual(cliente.get('/profesor/cursos/1A/alumnos').status_code,200)
                self.assertEqual(cliente.post(logout,headers={'X-CSRF-Token':token}).status_code,200)
                self.assertEqual(otro.get(privada).status_code,401)
        self.assertEqual(self.con.execute('SELECT count(*) FROM web_sesiones').fetchone()[0],0)
        self.comprobar_conservacion()

    def test_actividad_concurrente_no_revoca_sesion_valida(self):
        import seguridad_web
        self.con.executescript(SQL)
        reloj = [time.time()]
        with patch('seguridad_web.time.time', side_effect=lambda: reloj[0]):
            cliente = fixtures.api.app.test_client()
            self.assertEqual(cliente.post('/panel/login-individual', json={
                'usuario':'demo1','password':fixtures.PASSWORD}).status_code, 200)
        inicio = reloj[0]
        conectar = seguridad_web.obtener_conexion

        class ConexionConEspera:
            def __init__(self):
                self.real = conectar()
            def execute(self, sql, *args):
                if sql == 'BEGIN IMMEDIATE':
                    # Otro worker confirma actividad durante la espera del lock.
                    with closing(sqlite3.connect(self_ruta)) as otra:
                        otra.execute('UPDATE web_sesiones SET actividad=?', (inicio + 1,))
                        otra.commit()
                    reloj[0] = inicio + 2
                return self.real.execute(sql, *args)
            def __getattr__(self, nombre):
                return getattr(self.real, nombre)

        self_ruta = self.ruta
        with patch('seguridad_web.obtener_conexion', side_effect=ConexionConEspera), patch(
                'seguridad_web.time.time', side_effect=lambda: reloj[0]):
            self.assertEqual(cliente.get('/panel/sesion').status_code, 200)
        self.assertEqual(self.con.execute('SELECT actividad FROM web_sesiones').fetchone()[0], inicio + 2)
        self.comprobar_conservacion()

    def test_codigo_anterior_sobre_base_migrada_y_riesgo_replay(self):
        self.con.executescript(SQL)
        codigo = """import json, api
app=api.app
c=app.test_client()
resultados=[]
for usuario,login,privada,logout in [('demo1','/panel/login-individual','/panel/sesion','/panel/logout'),('profe1','/profesor/login','/profesor/sesion','/profesor/logout')]:
    assert c.post(login,json={'usuario':usuario,'password':%r}).status_code==200
    cookie=c.get_cookie('session').value
    assert c.get(privada).status_code==200
    assert c.post(logout).status_code==200
    copia=app.test_client(); copia.set_cookie('session',cookie)
    resultados.append(copia.get(privada).status_code)
print(json.dumps(resultados))
""" % fixtures.PASSWORD
        salida = subprocess.run([sys.executable,'-c',codigo],cwd=self.anterior,env=self.entorno,
                                text=True,capture_output=True,check=True,timeout=20)
        self.assertEqual(json.loads(salida.stdout), [200,200])
        self.assertEqual(self.con.execute('SELECT count(*) FROM web_sesiones').fetchone()[0],0)
        self.comprobar_conservacion()

    @unittest.skipUnless(os.getenv('MPAZ_TEST_GUNICORN_PATH'), 'Gunicorn de ensayo no solicitado; ver informe')
    def test_gunicorn_workers_y_preload(self):
        self.con.executescript(SQL)
        self.entorno['PYTHONPATH'] = os.environ['MPAZ_TEST_GUNICORN_PATH']
        # Wrapper solo temporal: permite identificar el PID que realmente atendió.
        (Path(self.tmp.name)/'mpaz_worker.py').write_text('''from api import app
import os
@app.after_request
def pid_prueba(respuesta):
    respuesta.headers['X-MPAZ-Test-Pid']=str(os.getpid())
    return respuesta
''')
        self.entorno['PYTHONPATH'] += os.pathsep + self.tmp.name + os.pathsep + str(ROOT)
        def http(puerto, ruta, datos=None, cookie=None, csrf=None):
            cab = {'Content-Type':'application/json'}
            if cookie: cab['Cookie']=cookie
            if csrf: cab['X-CSRF-Token']=csrf
            req=request.Request(f'http://127.0.0.1:{puerto}'+ruta,
                                data=json.dumps(datos).encode() if datos is not None else None,headers=cab)
            try:
                respuesta=request.urlopen(req,timeout=15)
            except error.HTTPError as exc:
                respuesta=exc
            with respuesta:
                return respuesta.status, respuesta.headers, json.loads(respuesta.read())
        for workers,preload in [(2,False),(3,True)]:
            with self.subTest(workers=workers,preload=preload):
                self.con.execute('DELETE FROM web_login_intentos'); self.con.execute('DELETE FROM web_sesiones'); self.con.commit()
                with socket.socket() as sock:
                    sock.bind(('127.0.0.1',0)); puerto=sock.getsockname()[1]
                cmd=[sys.executable,'-m','gunicorn','--bind',f'127.0.0.1:{puerto}','--workers',str(workers),'--worker-class','sync','--timeout','30','mpaz_worker:app']
                if preload: cmd.append('--preload')
                with tempfile.TemporaryFile(mode='w+') as log:
                    proceso=subprocess.Popen(cmd,cwd=ROOT,env=self.entorno,stdout=log,stderr=log)
                    try:
                        limite=time.monotonic()+15
                        while True:
                            try:
                                self.assertEqual(http(puerto,'/estado')[0],200); break
                            except (OSError, error.URLError):
                                if proceso.poll() is not None or time.monotonic()>limite:
                                    log.seek(0); self.fail(log.read())
                                time.sleep(0.05)
                        for usuario,login,privada,logout in [
                            ('demo1','/panel/login-individual','/panel/sesion','/panel/logout'),
                            ('profe1','/profesor/login','/profesor/sesion','/profesor/logout')]:
                            estado,cab,_=http(puerto,login,{'usuario':usuario,'password':fixtures.PASSWORD})
                            self.assertEqual(estado,200)
                            cookie=cab['Set-Cookie'].split(';',1)[0]
                            with ThreadPoolExecutor(max_workers=workers*2) as pool:
                                respuestas=list(pool.map(lambda _:http(puerto,privada,cookie=cookie),range(36)))
                            self.assertEqual({r[0] for r in respuestas},{200})
                            pids={r[1]['X-MPAZ-Test-Pid'] for r in respuestas}
                            self.assertEqual(len(pids),workers)
                            token=http(puerto,'/panel/csrf-token' if usuario=='demo1' else privada,cookie=cookie)[2]['csrf_token']
                            self.assertEqual(http(puerto,logout,{},cookie,token)[0],200)
                            with ThreadPoolExecutor(max_workers=workers*2) as pool:
                                rechazadas=list(pool.map(lambda _:http(puerto,privada,cookie=cookie),range(18)))
                            self.assertEqual({r[0] for r in rechazadas},{401})
                            print(f'Gunicorn: workers={workers}, preload={preload}, {usuario}: 36 accesos OK en {len(pids)} PIDs; 18 replays rechazados')
                        self.con.execute('DELETE FROM web_login_intentos'); self.con.commit()
                        with ThreadPoolExecutor(max_workers=workers*2) as pool:
                            intentos=list(pool.map(lambda _:http(puerto,'/profesor/login',{'usuario':'profe1','password':'incorrecta'}),range(18)))
                        self.assertEqual(sorted(r[0] for r in intentos),[401]*10+[429]*8)
                        self.assertTrue(all(int(r[1]['Retry-After'])>0 for r in intentos if r[0]==429))
                        self.assertEqual(self.con.execute('SELECT max(cantidad) FROM web_login_intentos').fetchone()[0],10)
                        print(f'Gunicorn: workers={workers}, preload={preload}: 10 intentos admitidos, 8 bloqueados; sin 500/503')
                    finally:
                        proceso.terminate()
                        try: proceso.wait(timeout=10)
                        except subprocess.TimeoutExpired:
                            proceso.kill(); proceso.wait(timeout=5)
                self.comprobar_conservacion()
