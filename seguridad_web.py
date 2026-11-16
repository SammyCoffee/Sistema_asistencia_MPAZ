"""Límites y sesiones compartidos entre workers mediante SQLite.

No crea tablas ni modifica el esquema al importar/iniciar la aplicación.
No confía en X-Forwarded-For; la integración con el proxy debe revisarse aparte.
"""
import hashlib
import hmac
import math
import os
import secrets
import time
from contextlib import closing
from flask import current_app, g, jsonify, request, session
from base_datos import obtener_conexion
from werkzeug.security import check_password_hash

LOGINS = {
    '/panel/login-individual': 'operador',
    '/seguimiento/operador/login': 'operador',
    '/profesor/login': 'docente',
}
LOGOUTS = {'/panel/logout', '/profesor/logout', '/seguimiento/operador/logout'}
CAMPOS_IDENTIDAD = ('panel_autorizado', 'seguimiento_operador_id', 'profesor_id')


def comparar_tokens(esperado, recibido):
    """Comparación constante en bytes; entradas Unicode inválidas no provocan 500."""
    return (isinstance(esperado, str) and isinstance(recibido, str)
            and bool(esperado) and hmac.compare_digest(esperado.encode('utf-8'), recibido.encode('utf-8')))


def _firma(valor):
    return hmac.new(current_app.secret_key.encode('utf-8'), valor.encode('utf-8'), hashlib.sha256).hexdigest()


def limitar_login(tipo, usuario, direccion, ahora=None):
    """Reserva un intento atómico; cuenta por identidad y por IP, ventana de 5 min."""
    ahora = time.time() if ahora is None else ahora
    claves = [(_firma('ip:' + direccion), 200)]
    if isinstance(usuario, str) and len(usuario) <= 40:
        claves.append((_firma(tipo + ':' + usuario.strip().lower()), 10))
    with closing(obtener_conexion()) as con:
        try:
            con.execute('BEGIN IMMEDIATE')
            con.execute('DELETE FROM web_login_intentos WHERE expira <= ?', (ahora,))
            esperas = []
            for clave, limite in claves:
                fila = con.execute('SELECT cantidad, expira FROM web_login_intentos WHERE clave=?', (clave,)).fetchone()
                if fila and fila[0] >= limite:
                    esperas.append(fila[1] - ahora)
            if esperas:
                con.commit()
                return max(1, math.ceil(max(esperas)))
            for clave, _ in claves:
                con.execute('INSERT INTO web_login_intentos(clave,cantidad,expira) VALUES (?,1,?) '
                            'ON CONFLICT(clave) DO UPDATE SET cantidad=cantidad+1', (clave, ahora + 300))
            con.commit()
        except Exception:
            con.rollback()
            raise
    return 0


def _cuenta(con, tipo, ident):
    # Tabla seleccionada de constantes internas; ningún identificador SQL viene del cliente.
    if tipo == 'operador':
        return con.execute("SELECT password_hash,rol FROM seguimiento_operadores WHERE id=? AND estado='activo' AND rol IN ('administracion','direccion')", (ident,)).fetchone()
    if tipo == 'docente':
        return con.execute("SELECT password_hash,rol FROM usuarios WHERE id=? AND estado='activo' AND rol='profesor'", (ident,)).fetchone()
    return None


def revocar(token):
    if not isinstance(token, str):
        return
    with closing(obtener_conexion()) as con:
        con.execute('DELETE FROM web_sesiones WHERE token_hash=?', (_firma('sid:' + token),))
        con.commit()


def crear_sesion_web(tipo, ident, password):
    """Se llama únicamente después de autenticar y crear identidad en la cookie."""
    revocar(getattr(g, 'web_token_anterior', None))
    ahora = time.time()
    token = secrets.token_urlsafe(32)
    with closing(obtener_conexion()) as con:
        cuenta = _cuenta(con, tipo, ident)
        # Revalidar contra la credencial vigente: puede haber rotado desde el login.
        if cuenta is None or not check_password_hash(cuenta[0], password):
            session.clear()
            return False
        con.execute('DELETE FROM web_sesiones WHERE expira <= ?', (ahora,))
        con.execute('INSERT INTO web_sesiones VALUES (?,?,?,?,?,?,?)',
                    (_firma('sid:' + token), tipo, ident, _firma(cuenta[0] + ':' + cuenta[1]),
                     ahora, ahora, ahora + current_app.config['MPAZ_SESION_MAX_SEGUNDOS']))
        con.commit()
    session['web_sid'] = token
    session.permanent = False
    return True


def validar_sesion_web():
    token = session.get('web_sid')
    if not isinstance(token, str) or len(token) > 100:
        session.clear()
        return
    ahora = time.time()
    huella = _firma('sid:' + token)
    with closing(obtener_conexion()) as con:
        try:
            con.execute('BEGIN IMMEDIATE')
            fila = con.execute('SELECT tipo,identidad_id,credencial_firma,actividad,expira FROM web_sesiones WHERE token_hash=?', (huella,)).fetchone()
            cuenta = _cuenta(con, fila[0], fila[1]) if fila else None
            ident_cookie = session.get('profesor_id') if fila and fila[0] == 'docente' else session.get('seguimiento_operador_id')
            valida = bool(fila and cuenta and type(ident_cookie) is int and ident_cookie == fila[1]
                          and ahora < fila[4] and 0 <= ahora - fila[3] < current_app.config['MPAZ_SESION_INACTIVIDAD_SEGUNDOS']
                          and hmac.compare_digest(fila[2], _firma(cuenta[0] + ':' + cuenta[1])))
            if valida:
                con.execute('UPDATE web_sesiones SET actividad=? WHERE token_hash=?', (ahora, huella))
            else:
                con.execute('DELETE FROM web_sesiones WHERE token_hash=?', (huella,))
                session.clear()
            con.commit()
        except Exception:
            con.rollback()
            raise


def instalar_seguridad(app):
    for nombre, defecto in [('MPAZ_SESION_MAX_SEGUNDOS', 8 * 3600),
                             ('MPAZ_SESION_INACTIVIDAD_SEGUNDOS', 30 * 60)]:
        try:
            valor = int(os.getenv(nombre, str(defecto)))
            if valor <= 0:
                raise ValueError
        except ValueError as error:
            raise RuntimeError(f"{nombre} debe ser un entero positivo") from error
        app.config.setdefault(nombre, valor)

    @app.before_request
    def comprobar_seguridad_web():
        g.web_token_anterior = session.get('web_sid')
        if request.method == 'POST' and request.path in LOGINS:
            datos = request.get_json(silent=True)
            usuario = datos.get('usuario') if isinstance(datos, dict) else None
            espera = limitar_login(LOGINS[request.path], usuario, request.remote_addr or 'sin-direccion')
            if espera:
                respuesta = jsonify(resultado='demasiados_intentos', mensaje='Espera unos minutos antes de volver a intentar.')
                respuesta.status_code = 429
                respuesta.headers['Retry-After'] = str(espera)
                return respuesta
        elif any(campo in session for campo in CAMPOS_IDENTIDAD) or 'web_sid' in session:
            validar_sesion_web()

    @app.after_request
    def confirmar_logout(respuesta):
        if request.method == 'POST' and request.path in LOGOUTS and respuesta.status_code == 200:
            revocar(getattr(g, 'web_token_anterior', None))
            session.clear()
        return respuesta
