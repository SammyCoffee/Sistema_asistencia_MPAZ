
"""Rutas protegidas de seguimiento escolar MPAZ RFID.

Etapa inicial: solicitudes docentes y consulta administrativa.
No habilita aun escritura administrativa sin identidad individual.
"""

import sqlite3
import secrets

from flask import Blueprint, jsonify, request, session

from seguimiento_sesiones import operador_actual

from seguimiento_escolar import (
    crear_caso_docente,
    listar_casos_docente,
)
from seguimiento_administracion import (
    consultar_historial_docente,
    listar_casos_administracion,
)

seguimiento_bp = Blueprint("seguimiento", __name__)


def _id_valido(valor):
    return type(valor) is int and valor > 0


def _json_valido():
    if not request.is_json:
        return None

    datos = request.get_json(silent=True)
    return datos if isinstance(datos, dict) else None


def _respuesta(datos, codigo=200):
    return jsonify(datos), codigo


@seguimiento_bp.before_request
def proteger_seguimiento():
    """Verifica la sesion y el token de las escrituras."""

    if request.path.startswith("/profesor/seguimiento/"):
        profesor_id = session.get("profesor_id")

        if (
            not _id_valido(profesor_id)
            or session.get("profesor_rol") != "profesor"
        ):
            return _respuesta({"resultado": "no_autorizado"}, 401)

        if request.method == "POST":
            esperado = session.get("profesor_csrf")
            recibido = request.headers.get("X-CSRF-Token")

            if (
                not isinstance(esperado, str)
                or not isinstance(recibido, str)
                or not esperado
                or not secrets.compare_digest(esperado, recibido)
            ):
                return _respuesta({"resultado": "csrf_invalido"}, 403)

    elif request.path.startswith("/panel/seguimiento/"):

        consulta_administrativa = (
            request.method == "GET"
            and request.endpoint in {
                "seguimiento.listar_casos_panel_api",
                "seguimiento.historial_administrativo_api"
            }
            and session.get("panel_autorizado") is True
        )

        if not consulta_administrativa and operador_actual() is None:
            return _respuesta({"resultado": "no_autorizado"}, 401)

    else:
        return _respuesta({"resultado": "ruta_no_autorizada"}, 403)


@seguimiento_bp.after_request
def evitar_cache(respuesta):
    respuesta.headers["Cache-Control"] = "no-store"
    return respuesta


@seguimiento_bp.errorhandler(sqlite3.OperationalError)
def error_base_datos(error):
    mensaje = str(error).lower()

    if "no such table" in mensaje:
        return _respuesta({
            "resultado": "seguimiento_no_preparado"
        }, 503)

    return _respuesta({
        "resultado": "base_datos_no_disponible"
    }, 503)


@seguimiento_bp.post("/profesor/seguimiento/casos")
def crear_caso_profesor_api():
    datos = _json_valido()

    if datos is None:
        return _respuesta({"resultado": "datos_invalidos"}, 400)

    alumno_id = datos.get("alumno_id")
    sesion_id = datos.get("sesion_clase_id")
    tipo = datos.get("tipo")
    descripcion = datos.get("descripcion")

    if not _id_valido(alumno_id) or not _id_valido(sesion_id):
        return _respuesta({"resultado": "datos_invalidos"}, 400)

    if not isinstance(tipo, str) or tipo not in (
        "inasistencia", "atraso"
    ):
        return _respuesta({"resultado": "tipo_invalido"}, 400)

    if (
        not isinstance(descripcion, str)
        or not 1 <= len(descripcion.strip()) <= 1000
    ):
        return _respuesta({"resultado": "descripcion_invalida"}, 400)

    resultado = crear_caso_docente(
        session["profesor_id"],
        alumno_id,
        sesion_id,
        tipo,
        descripcion
    )

    codigo = resultado.get("resultado")

    if codigo == "caso_creado":
        return _respuesta(resultado, 201)

    if codigo == "caso_existente":
        return _respuesta(resultado, 409)

    if codigo in ("no_autorizado", "alumno_no_autorizado"):
        return _respuesta(resultado, 403)

    if codigo == "asistencia_no_coincide":
        return _respuesta(resultado, 409)

    return _respuesta(resultado, 400)


@seguimiento_bp.get("/profesor/seguimiento/casos")
def listar_casos_profesor_api():
    resultado = listar_casos_docente(session["profesor_id"])
    return _respuesta(resultado)


@seguimiento_bp.get(
    "/profesor/seguimiento/casos/<int:caso_id>/historial"
)
def historial_profesor_api(caso_id):
    resultado = consultar_historial_docente(
        session["profesor_id"],
        caso_id
    )

    if resultado.get("resultado") == "ok":
        return _respuesta(resultado)

    return _respuesta(resultado, 403)


@seguimiento_bp.get("/panel/seguimiento/casos")
def listar_casos_panel_api():
    estado = request.args.get("estado") or None

    if estado is not None and estado not in (
        "pendiente", "en_gestion", "resuelto"
    ):
        return _respuesta({"resultado": "estado_invalido"}, 400)

    resultado = listar_casos_administracion(estado)
    return _respuesta(resultado)


# MPAZ-HISTORIAL-7613
from seguimiento_historial import (
    consultar_historial_operador,
    consultar_historial_panel
)


@seguimiento_bp.get(
    "/panel/seguimiento/casos/<int:caso_id>/historial"
)
def historial_administrativo_api(caso_id):

    operador = operador_actual()

    if operador is not None:
        resultado = consultar_historial_operador(
            operador["id"], caso_id
        )

    elif session.get("panel_autorizado") is True:
        resultado = consultar_historial_panel(caso_id)

    else:
        return _respuesta({"resultado": "no_autorizado"}, 401)

    estado = resultado.get("resultado")

    if estado == "ok":
        return _respuesta(resultado, 200)

    if estado == "caso_no_existe":
        return _respuesta(resultado, 404)

    if estado == "no_autorizado":
        return _respuesta(resultado, 403)

    return _respuesta(resultado, 400)
