
"""Rutas de gestion administrativa de Seguimiento Escolar."""

import sqlite3

from flask import Blueprint, jsonify, request, g

from seguimiento_sesiones import (
    operador_actual,
    csrf_operador_valido
)

from seguimiento_administracion import (
    responder_caso_administracion,
    registrar_contacto_administracion,
    cambiar_estado_caso_administracion
)

gestiones_bp = Blueprint("seguimiento_gestiones", __name__)


def responder(datos, codigo=200):
    return jsonify(datos), codigo


@gestiones_bp.before_request
def proteger_gestiones():

    operador = operador_actual()

    if operador is None:
        return responder({"resultado": "no_autorizado"}, 401)

    if not csrf_operador_valido():
        return responder({"resultado": "csrf_invalido"}, 403)

    g.operador_seguimiento = operador


@gestiones_bp.after_request
def evitar_cache(respuesta):
    respuesta.headers["Cache-Control"] = "no-store"
    return respuesta


@gestiones_bp.errorhandler(sqlite3.OperationalError)
def error_sqlite(error):
    return responder({
        "resultado": "base_datos_no_disponible"
    }, 503)


def datos_json():
    if not request.is_json:
        return None

    datos = request.get_json(silent=True)

    return datos if isinstance(datos, dict) else None


def resultado_http(resultado, exito, codigo_exito=200):
    estado = resultado.get("resultado")

    if estado == exito:
        return responder(resultado, codigo_exito)

    if estado == "operador_no_autorizado":
        return responder(resultado, 403)

    if estado == "caso_no_existe":
        return responder(resultado, 404)

    if estado in ("caso_resuelto", "sin_cambios"):
        return responder(resultado, 409)

    return responder(resultado, 400)


@gestiones_bp.post(
    "/panel/seguimiento/casos/<int:caso_id>/mensajes"
)
def registrar_mensaje(caso_id):

    datos = datos_json()

    if datos is None:
        return responder({"resultado": "datos_invalidos"}, 400)

    resultado = responder_caso_administracion(
        caso_id,
        datos.get("mensaje"),
        operador_id=g.operador_seguimiento["id"]
    )

    return resultado_http(resultado, "mensaje_registrado", 201)


@gestiones_bp.post(
    "/panel/seguimiento/casos/<int:caso_id>/contactos"
)
def registrar_contacto(caso_id):

    datos = datos_json()

    if datos is None:
        return responder({"resultado": "datos_invalidos"}, 400)

    if g.operador_seguimiento["rol"] != "administracion":
        return responder({
            "resultado": "operador_no_autorizado"
        }, 403)

    resultado = registrar_contacto_administracion(
        caso_id,
        datos.get("canal"),
        datos.get("resultado"),
        datos.get("observacion"),
        operador_id=g.operador_seguimiento["id"]
    )

    return resultado_http(resultado, "contacto_registrado", 201)


@gestiones_bp.post(
    "/panel/seguimiento/casos/<int:caso_id>/estado"
)
def actualizar_estado(caso_id):

    datos = datos_json()

    if datos is None:
        return responder({"resultado": "datos_invalidos"}, 400)

    resultado = cambiar_estado_caso_administracion(
        caso_id,
        datos.get("estado"),
        operador_id=g.operador_seguimiento["id"]
    )

    return resultado_http(resultado, "estado_actualizado")
