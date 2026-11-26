"""Consulta administrativa de asistencia manual de clase."""
from contextlib import closing
from datetime import date
import sqlite3

from flask import Blueprint, jsonify, request, session

from base_datos import obtener_conexion
from seguimiento_sesiones import operador_actual

sesiones_clase_admin_bp = Blueprint("sesiones_clase_admin", __name__)
TAMANO_PAGINA = 50
ESTADOS = {"borrador", "confirmada", "anulada"}

# Los totales de marcas conservan también alumnos que cambiaron de curso.
# Solo los borradores tienen pendientes calculados contra la nómina actual.
CONSULTA = """
    SELECT sc.id AS sesion_id, sc.fecha, sc.hora_inicio, sc.estado,
           sc.fecha_confirmacion, sc.modalidad, UPPER(TRIM(pc.curso)) AS curso,
           a.nombre AS asignatura, u.nombre_completo AS profesor,
           (SELECT COUNT(*) FROM asistencias_clase ac
            WHERE ac.sesion_clase_id = sc.id AND ac.estado = 'presente') AS presentes,
           (SELECT COUNT(*) FROM asistencias_clase ac
            WHERE ac.sesion_clase_id = sc.id AND ac.estado = 'atrasado') AS atrasados,
           (SELECT COUNT(*) FROM asistencias_clase ac
            WHERE ac.sesion_clase_id = sc.id AND ac.estado = 'no_presente') AS no_presentes,
           CASE WHEN sc.estado = 'borrador' THEN (
               SELECT COUNT(*) FROM alumnos al
               WHERE al.estado = 'activo' AND UPPER(TRIM(al.curso)) = UPPER(TRIM(pc.curso))
                 AND NOT EXISTS (
                   SELECT 1 FROM asistencias_clase ac
                   WHERE ac.sesion_clase_id = sc.id AND ac.alumno_id = al.id
                 )
           ) WHEN sc.estado = 'confirmada' THEN 0 END AS pendientes
    FROM sesiones_clase sc
    JOIN profesores_cursos pc ON pc.id = sc.asignacion_id
    JOIN asignaturas a ON a.id = pc.asignatura_id
    JOIN usuarios u ON u.id = pc.profesor_id
"""


@sesiones_clase_admin_bp.before_request
def autorizar():
    operador = operador_actual()
    if operador is None:
        return jsonify(resultado="no_autorizado"), 401
    if operador["rol"] != "administracion" or session.get("panel_autorizado") is not True:
        return jsonify(resultado="acceso_denegado"), 403
    return None


@sesiones_clase_admin_bp.after_request
def evitar_cache(respuesta):
    respuesta.headers["Cache-Control"] = "no-store"
    return respuesta


@sesiones_clase_admin_bp.errorhandler(sqlite3.Error)
def error_consulta(error):
    return jsonify(resultado="servicio_no_disponible"), 503


def consultar(condiciones, valores, limite, desplazamiento=0):
    filtro = " WHERE " + " AND ".join(condiciones) if condiciones else ""
    orden = " ORDER BY sc.fecha DESC, sc.hora_inicio DESC, sc.id DESC"
    with closing(obtener_conexion()) as conexion:
        conexion.execute("PRAGMA query_only = ON")
        conexion.row_factory = sqlite3.Row
        return [
            dict(fila) for fila in conexion.execute(
                CONSULTA + filtro + orden + " LIMIT ? OFFSET ?",
                (*valores, limite, desplazamiento),
            )
        ]


@sesiones_clase_admin_bp.get("/panel/sesiones-docentes")
def listar_sesiones():
    condiciones = []
    valores = []
    filtros = {
        "fecha": ("sc.fecha = ?", 10),
        "curso": ("UPPER(TRIM(pc.curso)) = UPPER(?)", 20),
        "asignatura": ("a.nombre = ? COLLATE NOCASE", 100),
        "estado": ("sc.estado = ?", 15),
    }
    try:
        pagina = int(request.args.get("pagina", "1"))
        if not 1 <= pagina <= 1_000_000:
            raise ValueError
        for campo, (condicion, maximo) in filtros.items():
            valor = request.args.get(campo, "").strip()
            if not valor:
                continue
            if len(valor) > maximo:
                raise ValueError
            if campo == "fecha" and date.fromisoformat(valor).isoformat() != valor:
                raise ValueError
            if campo == "estado" and valor not in ESTADOS:
                raise ValueError
            condiciones.append(condicion)
            valores.append(valor)
    except ValueError:
        return jsonify(resultado="filtros_invalidos"), 400

    filas = consultar(condiciones, valores, TAMANO_PAGINA + 1, (pagina - 1) * TAMANO_PAGINA)
    return jsonify(
        resultado="ok", sesiones=filas[:TAMANO_PAGINA],
        pagina=pagina, hay_siguiente=len(filas) > TAMANO_PAGINA,
    )


@sesiones_clase_admin_bp.get("/panel/sesiones-docentes/<int:sesion_id>")
def detalle_sesion(sesion_id):
    # Límite de enteros de SQLite.
    if not 1 <= sesion_id <= 2**63 - 1:
        return jsonify(resultado="sesion_no_encontrada"), 404
    filas = consultar(["sc.id = ?"], [sesion_id], 1)
    if not filas:
        return jsonify(resultado="sesion_no_encontrada"), 404
    return jsonify(resultado="ok", sesion=filas[0])
