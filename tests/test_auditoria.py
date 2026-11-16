"""Regresiones aisladas: nunca abre bases del repositorio ni del servidor."""
import csv
from contextlib import closing
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

# Valores exclusivamente ficticios, anteriores a importar Flask y sus módulos.
os.environ['MPAZ_SESSION_SECRET'] = 'solo-pruebas-sin-valor-en-produccion'
os.environ['MPAZ_API_KEY'] = 'api-ficticia-auditoria'
os.environ['MPAZ_DB_PATH'] = '/ruta-inexistente/pruebas-no-produccion.db'
import api
import base_datos as bd
import exportar_asistencias_csv as exportaciones
import respaldar_base_datos as respaldos
from calendario_administracion import guardar_jornada_escolar
from calendario_escolar import resolver_jornada_escolar
from procesar_lectura_totem import procesar_lectura_totem
from werkzeug.security import generate_password_hash

ROOT = Path(__file__).resolve().parents[1]
PASSWORD = 'Ficticia-auditoria-123'


class SistemaTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.ruta = Path(self.tmp.name) / 'ficticia.db'
        self.dbpatch = patch.object(bd, 'RUTA_BASE_DATOS', str(self.ruta))
        self.dbpatch.start()
        self.addCleanup(self.dbpatch.stop)
        bd.crear_tablas()
        self.con = bd.obtener_conexion()
        self.addCleanup(self.con.close)
        for archivo in sorted((ROOT / 'migraciones').glob('*.sql')):
            self.con.executescript(archivo.read_text())
        clave = generate_password_hash(PASSWORD)
        for ident, rol in [(1, 'administracion'), (2, 'direccion')]:
            self.con.execute('INSERT INTO seguimiento_operadores (id,nombre_completo,usuario,password_hash,rol) VALUES (?,?,?,?,?)',
                             (ident, 'Operador Ficticio', f'demo{ident}', clave, rol))
        for ident in (1, 2):
            self.con.execute("INSERT INTO usuarios (id,nombre_completo,usuario,password_hash,rol,fecha_creacion) VALUES (?,?,?,?,'profesor','2026-01-01')",
                             (ident, 'Docente Ficticio', f'profe{ident}', clave))
            # Identificador deliberadamente no es un RUT válido ni real.
            self.con.execute('INSERT INTO alumnos (id,rut,nombre_completo,curso) VALUES (?,?,?,?)',
                             (ident, f'DEMO-NO-RUT-{ident}', 'Estudiante Ficticio', f'{ident}A'))
        self.con.execute("INSERT INTO totems (id,codigo,nombre,ubicacion,fecha_registro) VALUES (1,'DEMO','Totem ficticio','Laboratorio','2026-01-01')")
        self.con.execute("INSERT INTO tarjetas (alumno_id,uid,estado,fecha_registro) VALUES (1,'AABBCCDD','activa','2026-01-01')")
        self.con.execute("INSERT INTO asignaturas (id,nombre) VALUES (1,'Demo')")
        self.con.execute("INSERT INTO profesores_cursos (id,profesor_id,curso,asignatura_id) VALUES (1,1,'1A',1),(2,2,'2A',1)")
        self.con.commit()
        api.app.config.update(TESTING=True)
        self.client = api.app.test_client()

    def login(self, rol='administracion'):
        usuario = 'demo1' if rol == 'administracion' else 'demo2'
        respuesta = self.client.post('/panel/login-individual', json={'usuario': usuario, 'password': PASSWORD})
        self.assertEqual(respuesta.status_code, 200)
        return self.client.get('/panel/csrf-token').json.get('csrf_token') if rol == 'administracion' else None

    def docente(self):
        self.assertEqual(self.client.post('/profesor/login', json={'usuario': 'profe1', 'password': PASSWORD}).status_code, 200)
        return self.client.get('/profesor/sesion').json['csrf_token']

    def test_estado_y_rutas_privadas(self):
        respuesta = self.client.get('/estado')
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json['sistema'], 'MPAZ RFID')
        self.assertEqual(respuesta.json['estado'], 'activo')
        for ruta in ['/alumnos', '/asistencias', '/panel/tarjetas', '/panel/totems', '/panel/seguimiento/casos', '/profesor/asignaciones']:
            with self.subTest(ruta=ruta):
                self.assertEqual(self.client.get(ruta).status_code, 401)
        self.assertEqual(self.client.get('/index.html').status_code, 302)
        self.assertEqual(self.client.get('/../../base_datos.py').status_code, 404)

    def test_administracion_direccion_y_csrf(self):
        token = self.login()
        self.assertEqual(self.client.get('/alumnos').status_code, 200)
        self.assertEqual(self.client.post('/panel/totems/registrar', json={}).status_code, 403)
        self.assertEqual(self.client.post('/panel/totems/registrar', json={}, headers={'X-CSRF-Token': token}).status_code, 400)
        self.login('direccion')
        self.assertEqual(self.client.get('/alumnos').status_code, 401)
        self.assertEqual(self.client.get('/panel/seguimiento/casos').status_code, 200)
        with self.client.session_transaction() as sesion:
            token = sesion['seguimiento_csrf']
        self.assertEqual(self.client.post('/panel/seguimiento/casos/1/contactos', json={'canal': 'telefonico'}, headers={'X-CSRF-Token': token}).status_code, 403)

    def test_sesion_antigua_y_operador_inactivo(self):
        with self.client.session_transaction() as sesion:
            sesion['panel_autorizado'] = True
        self.assertEqual(self.client.get('/alumnos').status_code, 401)
        self.login()
        self.con.execute("UPDATE seguimiento_operadores SET estado='inactivo' WHERE id=1")
        self.con.commit()
        self.assertEqual(self.client.get('/alumnos').status_code, 401)
        self.assertEqual(self.client.get('/seguimiento/operador/sesion').status_code, 401)
        self.assertEqual(self.client.post('/panel/login-individual', json={'usuario': 'demo1', 'password': PASSWORD}).status_code, 401)

    def test_docente_revocado(self):
        self.docente()
        self.con.execute("UPDATE usuarios SET estado='inactivo' WHERE id=1")
        self.con.commit()
        self.assertEqual(self.client.get('/profesor/sesion').status_code, 401)
        self.assertEqual(self.client.get('/profesor/seguimiento/casos').status_code, 401)

    def test_docente_idor_y_csrf(self):
        self.docente()
        self.assertEqual(self.client.get('/profesor/cursos/2A/alumnos').status_code, 403)
        self.assertEqual(self.client.post('/profesor/sesiones', json={}).status_code, 403)

    def test_logout_csrf(self):
        token = self.login()
        self.assertEqual(self.client.post('/panel/logout').status_code, 403)
        self.assertEqual(self.client.get('/panel/sesion').status_code, 200)
        self.assertEqual(self.client.post('/panel/logout', headers={'X-CSRF-Token': token}).status_code, 200)
        self.assertEqual(self.client.get('/panel/sesion').status_code, 401)
        token = self.docente()
        self.assertEqual(self.client.post('/profesor/logout').status_code, 403)
        self.assertEqual(self.client.post('/profesor/logout', headers={'X-CSRF-Token': token}).status_code, 200)
        self.assertEqual(self.client.get('/profesor/sesion').status_code, 401)

    def test_lectura_json_no_objeto(self):
        for valor in [[1], 'texto', 5, True]:
            with self.subTest(valor=valor):
                self.assertEqual(self.client.post('/lectura', json=valor, headers={'X-API-Key': api.API_KEY}).status_code, 400)

    def test_json_administrativo_no_objeto(self):
        token = self.login()
        for ruta in sorted(api.RUTAS_ADMIN_CSRF - {'/panel/logout'}):
            with self.subTest(ruta=ruta):
                self.assertEqual(self.client.post(ruta, json=[1], headers={'X-CSRF-Token': token}).status_code, 400)

    def test_cookie_y_cache(self):
        respuesta = self.client.post('/panel/login-individual', json={'usuario': 'demo1', 'password': PASSWORD}, base_url='https://localhost')
        cookie = respuesta.headers['Set-Cookie']
        self.assertIn('HttpOnly', cookie)
        self.assertIn('Secure', cookie)
        self.assertIn('SameSite=Lax', cookie)
        self.assertIn('no-store', self.client.get('/alumnos').headers.get('Cache-Control', ''))
        self.assertEqual(respuesta.headers.get('X-Content-Type-Options'), 'nosniff')
        self.assertEqual(respuesta.headers.get('X-Frame-Options'), 'SAMEORIGIN')

    def test_lectura_autorizacion_dispositivo(self):
        datos = {'codigo_totem': 'NO-EXISTE', 'uid': 'AABBCCDD', 'evento_id': 'demo-1'}
        self.assertEqual(self.client.post('/lectura', json=datos).status_code, 401)
        self.assertEqual(self.client.post('/lectura', json=datos, headers={'X-API-Key': api.API_KEY}).status_code, 403)
        self.con.execute("UPDATE totems SET estado='inactivo' WHERE id=1")
        self.con.commit()
        datos['codigo_totem'] = 'DEMO'
        self.assertEqual(self.client.post('/lectura', json=datos, headers={'X-API-Key': api.API_KEY}).status_code, 403)

    def test_rfid_antirrebote_idempotencia_y_salida(self):
        self.assertEqual(bd.guardar_asistencia(1, '2026-11-16', '08:00:00', 1, 'e1'), 'entrada_registrada')
        self.assertEqual(bd.guardar_asistencia(1, '2026-11-16', '08:00:40', 1, 'e1'), 'evento_repetido')
        self.assertEqual(bd.guardar_asistencia(1, '2026-11-16', '08:00:29', 1, 'e2'), 'lectura_repetida')
        self.assertEqual(bd.guardar_asistencia(1, '2026-11-16', '08:00:30', 1, 'e3'), 'salida_registrada')
        self.assertEqual(bd.guardar_asistencia(1, '2026-11-16', '09:00:00', 1, 'e3'), 'evento_repetido')
        self.assertEqual(bd.guardar_asistencia(1, '2026-11-16', '09:00:00', 1, 'e4'), 'jornada_completa')
        self.assertEqual(self.con.execute('SELECT totem_entrada_id,totem_salida_id,evento_entrada_id,evento_salida_id FROM asistencias').fetchone(), (1, 1, 'e1', 'e3'))

    def test_rfid_simultaneo(self):
        def lectura(_):
            return bd.guardar_asistencia(1, '2026-11-16', '08:00:00', 1, 'concurrente')
        with ThreadPoolExecutor(max_workers=4) as pool:
            resultados = list(pool.map(lectura, range(4)))
        self.assertEqual(resultados.count('entrada_registrada'), 1)
        self.assertEqual(resultados.count('evento_repetido'), 3)

    def test_tarjeta_bloqueada_y_alumno_inactivo(self):
        self.con.execute("UPDATE tarjetas SET estado='bloqueada'")
        self.con.commit()
        self.assertEqual(procesar_lectura_totem('DEMO', 'AABBCCDD', 'b1')['resultado'], 'tarjeta_bloqueada')
        self.con.execute("UPDATE tarjetas SET estado='activa'")
        self.con.execute("UPDATE alumnos SET estado='inactivo' WHERE id=1")
        self.con.commit()
        self.assertEqual(procesar_lectura_totem('DEMO', 'AABBCCDD', 'b2')['resultado'], 'alumno_inactivo')
        self.assertEqual(self.con.execute('SELECT count(*) FROM asistencias').fetchone()[0], 0)

    def test_cierre_automatico_y_cambio_dia(self):
        bd.guardar_asistencia(1, '2026-11-15', '08:00:00', 1, 'ayer')
        bd.guardar_asistencia(1, '2026-11-16', '08:00:00', 1, 'hoy')
        with patch.object(bd, 'ahora_chile', return_value=datetime(2026, 11, 16, 17, 0)):
            bd.cerrar_jornadas_pendientes()
        self.assertEqual(self.con.execute("SELECT count(*) FROM asistencias WHERE hora_salida='17:00:00' AND tipo_salida='automatica'").fetchone()[0], 2)

    def test_calendario_prioridad_y_auditoria(self):
        for curso, condicion in [(None, 'lectiva'), ('1A', 'suspendida')]:
            guardar_jornada_escolar(self.con, accion='crear', fecha='2026-11-16', curso=curso, condicion=condicion, motivo='Solo prueba ficticia')
        self.assertEqual(resolver_jornada_escolar(self.con, '2026-11-16', '1A')['condicion'], 'suspendida')
        self.assertEqual(resolver_jornada_escolar(self.con, '2026-11-16', '2A')['condicion'], 'lectiva')
        self.assertEqual(self.con.execute('SELECT count(*) FROM calendario_auditoria').fetchone()[0], 2)

    def test_logout_docente_csrf(self):
        token = self.docente()
        self.assertEqual(self.client.post('/profesor/logout').status_code, 403)
        self.assertEqual(self.client.get('/profesor/sesion').status_code, 200)
        self.assertEqual(self.client.post('/profesor/logout', headers={'X-CSRF-Token': token}).status_code, 200)

    def test_exportacion_nombre_unico(self):
        with patch.object(exportaciones, 'CARPETA_REPORTES', Path(self.tmp.name)), patch.object(exportaciones, 'ahora_chile', return_value=datetime(2026, 11, 16, 12, 0)):
            una, _ = exportaciones.exportar_asistencias()
            otra, _ = exportaciones.exportar_asistencias()
        self.assertNotEqual(una, otra)

    def test_exportacion_formula_y_nombres_unicos(self):
        self.con.execute("UPDATE alumnos SET nombre_completo='=1+1' WHERE id=1")
        self.con.commit()
        bd.guardar_asistencia(1, exportaciones.hoy_chile().strftime('%Y-%m-%d'), '08:00:00', 1, '=1+1')
        with patch.object(exportaciones, 'CARPETA_REPORTES', Path(self.tmp.name)):
            ruta, cantidad = exportaciones.exportar_asistencias()
            otra, _ = exportaciones.exportar_asistencias()
        self.assertEqual(cantidad, 1)
        with ruta.open(encoding='utf-8-sig') as archivo:
            filas = list(csv.reader(archivo, delimiter=';'))
        self.assertEqual(filas[1][2], "'=1+1")
        self.assertEqual(filas[1][10], "'=1+1")
        self.assertNotEqual(ruta, otra)

    def test_tarjetas_y_estados_administrativos(self):
        token = self.login()
        cabecera = {'X-CSRF-Token': token}
        datos = {'uid': '11223344'}
        self.assertEqual(self.client.post('/panel/tarjetas/registrar', json=datos, headers=cabecera).status_code, 201)
        self.assertEqual(self.client.post('/panel/tarjetas/registrar', json=datos, headers=cabecera).status_code, 409)
        self.assertEqual(bd.vincular_tarjeta(2, '11223344')['resultado'], 'vinculada')
        self.assertTrue(bd.bloquear_tarjeta('11223344'))
        self.assertEqual(bd.activar_tarjeta('11223344'), 'activada')
        self.assertFalse(bd.validar_rut_chileno('DEMO-NO-RUT'))
        respuesta = self.client.post('/panel/alumnos/registrar', json={'rut': 'DEMO-NO-RUT', 'nombre': 'Estudiante Ficticio', 'curso': '1A'}, headers=cabecera)
        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(respuesta.json['resultado'], 'rut_invalido')

    def test_docente_seguimiento_gestion_historial(self):
        self.con.execute("INSERT INTO sesiones_clase (id,asignacion_id,fecha,hora_inicio) VALUES (1,1,'2026-11-16','08:00')")
        self.con.execute("INSERT INTO asistencias_clase (sesion_clase_id,alumno_id,estado) VALUES (1,1,'no_presente')")
        self.con.commit()
        token = self.docente()
        caso = self.client.post('/profesor/seguimiento/casos', json={'alumno_id': 1, 'sesion_clase_id': 1, 'tipo': 'inasistencia', 'descripcion': 'Caso ficticio de prueba'}, headers={'X-CSRF-Token': token})
        self.assertEqual(caso.status_code, 201)
        ident = caso.json['caso_id']
        self.assertEqual(self.client.get(f'/profesor/seguimiento/casos/{ident}/historial').status_code, 200)
        self.client.post('/profesor/login', json={'usuario': 'profe2', 'password': PASSWORD})
        self.assertEqual(self.client.get(f'/profesor/seguimiento/casos/{ident}/historial').status_code, 403)
        self.login()
        with self.client.session_transaction() as sesion:
            token = sesion['seguimiento_csrf']
        base = f'/panel/seguimiento/casos/{ident}'
        self.assertEqual(self.client.post(base + '/mensajes', json={'mensaje': 'Ficticio'}).status_code, 403)
        for ruta, datos, codigo in [('/mensajes', {'mensaje': 'Respuesta ficticia'}, 201), ('/contactos', {'canal': 'telefonico', 'resultado': 'Prueba sin llamada real'}, 201), ('/estado', {'estado': 'resuelto'}, 200)]:
            self.assertEqual(self.client.post(base + ruta, json=datos, headers={'X-CSRF-Token': token}).status_code, codigo)
        historial = self.client.get(base + '/historial')
        self.assertEqual(historial.status_code, 200)
        self.assertEqual(historial.json['caso']['estado'], 'resuelto')
        self.assertEqual(len(historial.json['contactos']), 1)

    def test_sqlite_no_disponible(self):
        with patch.object(bd.sqlite3, 'connect', side_effect=sqlite3.OperationalError('detalle privado ficticio')):
            respuesta = self.client.post('/lectura', json={'codigo_totem': 'DEMO', 'uid': 'AABBCCDD', 'evento_id': 'error-db'}, headers={'X-API-Key': api.API_KEY})
        self.assertEqual(respuesta.status_code, 503)
        self.assertEqual(respuesta.json['resultado'], 'base_datos_no_disponible')
        self.assertNotIn('detalle privado', respuesta.get_data(as_text=True))

    def test_reenvio_sin_red(self):
        from urllib.error import URLError
        import reenviar_pendientes
        with patch.object(reenviar_pendientes.request, 'urlopen', side_effect=URLError('Red ficticia caída')):
            procesado, respuesta = reenviar_pendientes.enviar_pendiente({'evento_id': 'offline-demo'})
        self.assertFalse(procesado)
        self.assertEqual(respuesta['resultado'], 'sin_conexion')

    def test_exportacion_vacia(self):
        with patch.object(exportaciones, 'CARPETA_REPORTES', Path(self.tmp.name)):
            ruta, cantidad = exportaciones.exportar_asistencias()
        self.assertEqual(cantidad, 0)
        with ruta.open(encoding='utf-8-sig') as archivo:
            self.assertEqual(len(list(csv.reader(archivo, delimiter=';'))), 1)

    def test_respaldo_wal(self):
        self.con.execute('PRAGMA journal_mode=WAL')
        self.con.execute("UPDATE alumnos SET nombre_completo='Cambio en WAL' WHERE id=1")
        self.con.commit()
        with patch.object(respaldos, 'RUTA_BASE_DATOS', self.ruta), patch.object(respaldos, 'CARPETA_RESPALDOS', Path(self.tmp.name) / 'copias'):
            respaldos.respaldar_base_datos()
        copia = next((Path(self.tmp.name) / 'copias').glob('*.db'))
        with closing(sqlite3.connect(copia)) as con:
            self.assertEqual(con.execute('SELECT nombre_completo FROM alumnos WHERE id=1').fetchone()[0], 'Cambio en WAL')
            self.assertEqual(con.execute('PRAGMA integrity_check').fetchone()[0], 'ok')
            self.assertEqual(con.execute('PRAGMA foreign_key_check').fetchall(), [])


if __name__ == '__main__':
    unittest.main()
