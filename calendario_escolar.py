
"""
Sistema MPAZ RFID
Consulta de jornadas escolares.

No modifica registros ni determina
inasistencias por sí misma.
"""

import re
from datetime import date

CURSOS_VALIDOS = {
    "PK", "K",
    "1A", "1B", "2A", "2B",
    "3A", "3B", "4A", "4B",
    "5A", "5B", "6A", "6B",
    "7A", "7B", "8A", "8B"
}


def validar_fecha_escolar(fecha):
    """Valida una fecha real YYYY-MM-DD."""

    if not isinstance(fecha, str):
        raise ValueError("fecha_invalida")

    if not re.fullmatch(
        "[0-9]{4}-[0-9]{2}-[0-9]{2}",
        fecha
    ):
        raise ValueError("fecha_invalida")

    try:
        date.fromisoformat(fecha)
    except ValueError as error:
        raise ValueError("fecha_invalida") from error

    return fecha


def validar_curso_escolar(curso):
    """Comprueba que el curso esté en el catálogo escolar."""

    if not isinstance(curso, str):
        raise ValueError("curso_invalido")

    curso = curso.strip().upper()

    if curso not in CURSOS_VALIDOS:
        raise ValueError("curso_invalido")

    return curso


def resolver_jornada_escolar(conexion, fecha, curso):
    """
    Consulta la jornada correspondiente.

    Prioridad:
    1. Configuración específica del curso.
    2. Configuración general.
    3. Fecha sin configurar.

    Recibe una conexión SQLite explícita.
    No modifica la base de datos.
    """

    fecha = validar_fecha_escolar(fecha)
    curso = validar_curso_escolar(curso)

    cursor = conexion.execute(
        """
        SELECT
            id,
            fecha,
            curso,
            condicion,
            hora_entrada,
            hora_salida,
            motivo
        FROM calendario_jornadas
        WHERE fecha = ?
          AND (curso = ? OR curso IS NULL)
        ORDER BY
            CASE
                WHEN curso = ? THEN 0
                ELSE 1
            END
        LIMIT 1
        """,
        (fecha, curso, curso)
    )

    jornada = cursor.fetchone()

    if jornada is None:
        return {
            "resultado": "sin_configurar",
            "fecha": fecha,
            "curso": curso,
            "condicion": None,
            "alcance": None,
            "hora_entrada": None,
            "hora_salida": None,
            "motivo": None
        }

    return {
        "resultado": "configurada",
        "id": jornada[0],
        "fecha": jornada[1],
        "curso": curso,
        "condicion": jornada[3],
        "alcance": (
            "curso"
            if jornada[2] is not None
            else "general"
        ),
        "hora_entrada": jornada[4],
        "hora_salida": jornada[5],
        "motivo": jornada[6]
    }
