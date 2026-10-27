
"""
MPAZ RFID - Administracion de jornadas escolares.

Recibe una conexion SQLite explicita.
Registra cambios y auditoria en una misma transaccion.

La identidad individual del administrador no esta
disponible con el sistema actual de login compartido.
"""

import json
import re

from calendario_escolar import (
    validar_fecha_escolar,
    validar_curso_escolar
)

CONDICIONES = {
    "lectiva",
    "suspendida",
    "feriado",
    "reducida",
    "horario_especial"
}


def validar_hora_escolar(hora):
    if hora is None:
        return None

    if not isinstance(hora, str):
        raise ValueError("hora_invalida")

    if not re.fullmatch(
        r"(?:[01][0-9]|2[0-3]):[0-5][0-9]",
        hora
    ):
        raise ValueError("hora_invalida")

    return hora


def guardar_jornada_escolar(
    conexion,
    *,
    accion,
    fecha,
    curso=None,
    condicion,
    motivo,
    hora_entrada=None,
    hora_salida=None
):
    """
    Crea o edita una configuracion de jornada.

    La funcion no crea tablas ni abre otra conexion.
    La auditoria se guarda junto con la operacion.
    """

    if accion not in ("crear", "editar"):
        raise ValueError("accion_invalida")

    fecha = validar_fecha_escolar(fecha)

    if curso is not None:
        curso = validar_curso_escolar(curso)

    if (
        not isinstance(condicion, str)
        or condicion not in CONDICIONES
    ):
        raise ValueError("condicion_invalida")

    if not isinstance(motivo, str):
        raise ValueError("motivo_invalido")

    motivo = motivo.strip()

    if not 8 <= len(motivo) <= 300:
        raise ValueError("motivo_invalido")

    entrada = validar_hora_escolar(hora_entrada)
    salida = validar_hora_escolar(hora_salida)

    if condicion in ("suspendida", "feriado"):
        if entrada is not None or salida is not None:
            raise ValueError("horario_no_permitido")

    if condicion == "feriado" and curso is not None:
        raise ValueError("feriado_debe_ser_general")

    if condicion in ("reducida", "horario_especial"):
        if entrada is None or salida is None:
            raise ValueError("horario_obligatorio")

    if (entrada is None) != (salida is None):
        raise ValueError("horario_incompleto")

    if entrada is not None and entrada >= salida:
        raise ValueError("rango_horario_invalido")

    nuevo = {
        "fecha": fecha,
        "curso": curso,
        "condicion": condicion,
        "hora_entrada": entrada,
        "hora_salida": salida,
        "motivo": motivo
    }

    columnas = (
        "fecha",
        "curso",
        "condicion",
        "hora_entrada",
        "hora_salida",
        "motivo"
    )

    try:
        conexion.execute("BEGIN IMMEDIATE")

        fila = conexion.execute(
            """
            SELECT
                id, fecha, curso, condicion,
                hora_entrada, hora_salida, motivo
            FROM calendario_jornadas
            WHERE fecha = ?
              AND curso IS ?
            LIMIT 1
            """,
            (fecha, curso)
        ).fetchone()

        anterior = None

        if fila is not None:
            anterior = dict(zip(columnas, fila[1:]))

        if accion == "crear":

            if fila is not None:
                conexion.rollback()
                return {"resultado": "ya_existe"}

            cursor = conexion.execute(
                """
                INSERT INTO calendario_jornadas (
                    fecha, curso, condicion,
                    hora_entrada, hora_salida, motivo
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    fecha, curso, condicion,
                    entrada, salida, motivo
                )
            )

            jornada_id = cursor.lastrowid

        else:

            if fila is None:
                conexion.rollback()
                return {"resultado": "no_existe"}

            if anterior == nuevo:
                conexion.rollback()
                return {"resultado": "sin_cambios"}

            jornada_id = fila[0]

            conexion.execute(
                """
                UPDATE calendario_jornadas
                SET condicion = ?,
                    hora_entrada = ?,
                    hora_salida = ?,
                    motivo = ?,
                    actualizado_en = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    condicion, entrada,
                    salida, motivo, jornada_id
                )
            )

        conexion.execute(
            """
            INSERT INTO calendario_auditoria (
                jornada_id,
                accion,
                valor_anterior,
                valor_nuevo,
                actor
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                jornada_id,
                accion,
                (
                    json.dumps(anterior, ensure_ascii=False)
                    if anterior is not None
                    else None
                ),
                json.dumps(nuevo, ensure_ascii=False),
                "panel_administrativo"
            )
        )

        conexion.commit()

        return {
            "resultado": (
                "creada" if accion == "crear"
                else "actualizada"
            ),
            "jornada_id": jornada_id
        }

    except Exception:
        conexion.rollback()
        raise
