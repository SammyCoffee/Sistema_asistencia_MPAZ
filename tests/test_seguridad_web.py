"""Regresiones de autenticación y revocación, con cuentas ficticias."""
import unittest
from unittest.mock import patch
import test_auditoria as fixtures
api, bd, PASSWORD = fixtures.api, fixtures.bd, fixtures.PASSWORD


class SeguridadWebTest(unittest.TestCase):
    setUp = fixtures.SistemaTest.setUp
    login = fixtures.SistemaTest.login
    docente = fixtures.SistemaTest.docente

    def test_limite_login_compartido_operadores(self):
        for numero in range(10):
            ruta = '/panel/login-individual' if numero % 2 else '/seguimiento/operador/login'
            self.assertEqual(self.client.post(ruta, json={'usuario': 'demo1', 'password': 'incorrecta'}).status_code, 401)
        respuesta = self.client.post('/panel/login-individual', json={'usuario': 'demo1', 'password': PASSWORD})
        self.assertEqual(respuesta.status_code, 429)
        self.assertGreater(int(respuesta.headers['Retry-After']), 0)
        otra = api.app.test_client()
        self.assertEqual(otra.post('/seguimiento/operador/login', json={'usuario': 'DEMO1', 'password': PASSWORD}, headers={'X-Forwarded-For':'198.51.100.22'}).status_code, 429)
        # La cuenta distinta sigue disponible: no bloqueo permanente ni global.
        self.assertEqual(otra.post('/panel/login-individual', json={'usuario': 'demo2', 'password': PASSWORD}).status_code, 200)

    def test_limite_docente(self):
        for _ in range(10):
            self.client.post('/profesor/login', json={'usuario': 'profe1', 'password': 'incorrecta'})
        self.assertEqual(self.client.post('/profesor/login', json={'usuario': 'profe1', 'password': PASSWORD}).status_code, 429)

    def test_cookie_copiada_despues_logout(self):
        for tipo in ('administracion', 'direccion', 'docente'):
            with self.subTest(tipo=tipo):
                if tipo == 'docente':
                    token = self.docente(); logout = '/profesor/logout'; privada = '/profesor/sesion'
                else:
                    token = self.login(tipo); logout = '/panel/logout'; privada = '/panel/sesion'
                    if tipo == 'direccion':
                        privada = '/seguimiento/operador/sesion'; logout = '/seguimiento/operador/logout'
                        token = self.client.get(privada).json['csrf_token']
                cookie = self.client.get_cookie('session').value
                activa = api.app.test_client(); activa.set_cookie('session', cookie)
                self.assertEqual(activa.get(privada).status_code, 200)
                self.assertEqual(self.client.post(logout, headers={'X-CSRF-Token': token}).status_code, 200)
                copiada = api.app.test_client(); copiada.set_cookie('session', cookie)
                self.assertEqual(copiada.get(privada).status_code, 401)

    def test_cambio_password_revoca_copia(self):
        for tipo, tabla, privada in [('administracion', 'seguimiento_operadores', '/panel/sesion'), ('docente', 'usuarios', '/profesor/sesion')]:
            with self.subTest(tipo=tipo):
                self.docente() if tipo == 'docente' else self.login()
                cookie = self.client.get_cookie('session').value
                self.con.execute(f"UPDATE {tabla} SET password_hash='hash-ficticio-cambiado' WHERE id=1")
                self.con.commit()
                copiada = api.app.test_client(); copiada.set_cookie('session', cookie)
                self.assertEqual(copiada.get(privada).status_code, 401)

    def test_cookie_antigua_con_identidad(self):
        with self.client.session_transaction() as s:
            s['panel_autorizado'] = True
            s['seguimiento_operador_id'] = 1
        self.assertEqual(self.client.get('/alumnos').status_code, 401)

    def test_nuevo_login_revoca_sesion_anterior_mismo_navegador(self):
        self.login()
        cookie = self.client.get_cookie('session').value
        self.docente()
        copiada = api.app.test_client(); copiada.set_cookie('session', cookie)
        self.assertEqual(copiada.get('/alumnos').status_code, 401)

    def test_expiracion_inactividad_y_absoluta(self):
        for avance in (1800, 8 * 3600):
            with self.subTest(avance=avance), patch('seguridad_web.time.time', return_value=100000):
                self.login()
                cookie = self.client.get_cookie('session').value
            with patch('seguridad_web.time.time', return_value=100000 + avance):
                copiada = api.app.test_client(); copiada.set_cookie('session', cookie)
                self.assertEqual(copiada.get('/alumnos').status_code, 401)

    def test_limite_se_recupera(self):
        with patch('seguridad_web.time.time', return_value=100000):
            for _ in range(10):
                self.client.post('/profesor/login', json={'usuario': 'profe1', 'password': 'incorrecta'})
            self.assertEqual(self.client.post('/profesor/login', json={'usuario': 'profe1', 'password': PASSWORD}).status_code, 429)
        with patch('seguridad_web.time.time', return_value=100301):
            self.assertEqual(self.client.post('/profesor/login', json={'usuario': 'profe1', 'password': PASSWORD}).status_code, 200)

    def test_limite_entre_procesos(self):
        import subprocess, sys
        codigo = '''import sys; import base_datos as bd; import api
from seguridad_web import limitar_login
bd.RUTA_BASE_DATOS=sys.argv[1]
with api.app.app_context():
    resultados=[limitar_login('operador','demo1','ip-ficticia',100000) for _ in range(6)]
print(sum(x == 0 for x in resultados))
'''
        procesos = [subprocess.Popen([sys.executable, '-c', codigo, str(self.ruta)], stdout=subprocess.PIPE, text=True) for _ in range(3)]
        aceptados = 0
        for proceso in procesos:
            salida, _ = proceso.communicate(timeout=15)
            self.assertEqual(proceso.returncode, 0)
            aceptados += int(salida.strip())
        self.assertEqual(aceptados, 10)

    def test_login_direccion_inactiva(self):
        self.login('direccion')
        self.con.execute("UPDATE seguimiento_operadores SET estado='inactivo' WHERE id=2")
        self.con.commit()
        self.assertEqual(self.client.get('/panel/seguimiento/casos').status_code, 401)
        self.assertEqual(self.client.post('/seguimiento/operador/login', json={'usuario':'demo2','password':PASSWORD}).status_code, 401)

    def test_expiracion_absoluta_aunque_haya_actividad(self):
        with patch.dict(api.app.config, {'MPAZ_SESION_MAX_SEGUNDOS':60, 'MPAZ_SESION_INACTIVIDAD_SEGUNDOS':40}):
            with patch('seguridad_web.time.time', return_value=100000):
                self.login()
            for segundos, codigo in [(30,200),(59,200),(60,401)]:
                with patch('seguridad_web.time.time', return_value=100000+segundos):
                    self.assertEqual(self.client.get('/alumnos').status_code,codigo)

    def test_migracion_repetible_y_fallo_cerrado(self):
        archivo=fixtures.ROOT/'migraciones/005_seguridad_web.sql'
        for _ in range(2):
            self.con.executescript(archivo.read_text())
        self.assertEqual(self.con.execute('SELECT count(*) FROM alumnos').fetchone()[0],2)
        self.con.execute('DROP TABLE web_login_intentos')  # Exclusivamente base temporal de prueba.
        self.con.commit()
        respuesta=self.client.post('/panel/login-individual',json={'usuario':'demo1','password':PASSWORD})
        self.assertEqual(respuesta.status_code,503)
        self.assertNotIn('no such table',respuesta.get_data(as_text=True))

    def test_limite_ip_para_rotacion_de_usuarios(self):
        for numero in range(200):
            respuesta=self.client.post('/profesor/login',json={'usuario':f'ficticio{numero}','password':'incorrecta'})
            self.assertEqual(respuesta.status_code,401)
        respuesta=self.client.post('/profesor/login',json={'usuario':'profe1','password':PASSWORD},headers={'X-Forwarded-For':'198.51.100.23'})
        self.assertEqual(respuesta.status_code,429)

    def test_password_cambiada_entre_autenticacion_y_emision(self):
        from werkzeug.security import generate_password_hash
        import seguimiento_identidad
        for tipo in ('operador','docente'):
            tabla='seguimiento_operadores' if tipo=='operador' else 'usuarios'
            original=seguimiento_identidad.autenticar_operador if tipo=='operador' else api.autenticar_usuario
            def autenticar_y_rotar(usuario,password):
                resultado=original(usuario,password)
                self.con.execute(f'UPDATE {tabla} SET password_hash=? WHERE id=1',(generate_password_hash('Nueva-ficticia-456'),))
                self.con.commit()
                return resultado
            destino='seguimiento_identidad.autenticar_operador' if tipo=='operador' else 'api.autenticar_usuario'
            ruta='/panel/login-individual' if tipo=='operador' else '/profesor/login'
            with self.subTest(tipo=tipo), patch(destino,side_effect=autenticar_y_rotar):
                respuesta=self.client.post(ruta,json={'usuario':'demo1' if tipo=='operador' else 'profe1','password':PASSWORD})
            self.assertEqual(respuesta.status_code,401)
