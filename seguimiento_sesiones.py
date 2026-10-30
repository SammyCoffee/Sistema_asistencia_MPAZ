
"""Autenticacion web individual para Seguimiento Escolar."""

import secrets

from flask import Blueprint, jsonify, request, session
from base_datos import obtener_conexion
from seguimiento_identidad import autenticar_operador

sesiones_bp = Blueprint("seguimiento_sesiones", __name__)

ROLES = {"administracion", "direccion"}


def operador_actual():
    """Obtiene la identidad vigente desde SQLite."""

    operador_id = session.get("seguimiento_operador_id")

    if type(operador_id) is not int or operador_id <= 0:
        return None

    con = obtener_conexion()

    try:
        fila = con.execute("""
            SELECT id, nombre_completo, usuario, rol
            FROM seguimiento_operadores
            WHERE id = ?
              AND estado = 'activo'
            LIMIT 1
        """, (operador_id,)).fetchone()

        if fila is None or fila[3] not in ROLES:
            return None

        return {
            "id": fila[0],
            "nombre": fila[1],
            "usuario": fila[2],
            "rol": fila[3]
        }

    finally:
        con.close()


def csrf_operador_valido():
    esperado = session.get("seguimiento_csrf")
    recibido = request.headers.get("X-CSRF-Token")

    return (
        isinstance(esperado, str)
        and isinstance(recibido, str)
        and bool(esperado)
        and secrets.compare_digest(esperado, recibido)
    )


@sesiones_bp.after_request
def sin_cache(respuesta):
    respuesta.headers["Cache-Control"] = "no-store"
    return respuesta


@sesiones_bp.post("/seguimiento/operador/login")
def iniciar_sesion_operador():

    if not request.is_json:
        return jsonify({
            "resultado": "datos_invalidos"
        }), 400

    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "resultado": "datos_invalidos"
        }), 400

    usuario = datos.get("usuario")
    password = datos.get("password")

    if (
        not isinstance(usuario, str)
        or not isinstance(password, str)
        or len(usuario) > 40
        or len(password) > 128
    ):
        return jsonify({
            "resultado": "datos_invalidos"
        }), 400

    resultado = autenticar_operador(usuario, password)

    if resultado.get("resultado") != "autenticado":
        return jsonify({
            "resultado": "credenciales_invalidas"
        }), 401

    session.clear()

    session["seguimiento_operador_id"] = resultado["id"]
    session["seguimiento_csrf"] = secrets.token_urlsafe(32)

    return jsonify({
        "resultado": "ok",
        "operador": {
            "id": resultado["id"],
            "nombre": resultado["nombre"],
            "rol": resultado["rol"]
        }
    }), 200


@sesiones_bp.get("/seguimiento/operador/sesion")
def consultar_sesion_operador():

    operador = operador_actual()

    if operador is None:
        return jsonify({
            "resultado": "no_autorizado"
        }), 401

    return jsonify({
        "resultado": "ok",
        "operador": operador,
        "csrf_token": session.get("seguimiento_csrf")
    }), 200


@sesiones_bp.post("/seguimiento/operador/logout")
def cerrar_sesion_operador():

    if operador_actual() is None:
        return jsonify({
            "resultado": "no_autorizado"
        }), 401

    if not csrf_operador_valido():
        return jsonify({
            "resultado": "csrf_invalido"
        }), 403

    session.clear()

    return jsonify({
        "resultado": "sesion_cerrada"
    }), 200
