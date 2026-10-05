from datetime import date, datetime, timedelta
import math

from base_datos import obtener_conexion


HORA_LIMITE_ATRASO = "08:20:00"


def obtener_rango_periodo(
    periodo,
    fecha_referencia=None
):
    if fecha_referencia:
        referencia = datetime.strptime(
            fecha_referencia,
            "%Y-%m-%d"
        ).date()
    else:
        referencia = date.today()

    if periodo == "diario":
        inicio = referencia
        fin = referencia

    elif periodo == "semanal":
        inicio = referencia - timedelta(
            days=referencia.weekday()
        )

        fin = inicio + timedelta(days=6)

    elif periodo == "mensual":
        inicio = referencia.replace(day=1)

        if referencia.month == 12:
            siguiente_mes = referencia.replace(
                year=referencia.year + 1,
                month=1,
                day=1
            )
        else:
            siguiente_mes = referencia.replace(
                month=referencia.month + 1,
                day=1
            )

        fin = siguiente_mes - timedelta(days=1)

    else:
        raise ValueError(
            "Periodo no valido"
        )

    return (
        inicio.strftime("%Y-%m-%d"),
        fin.strftime("%Y-%m-%d")
    )


def obtener_asistencias():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT
                asistencias.id,
                alumnos.nombre_completo,
                alumnos.rut,
                alumnos.curso,
                asistencias.fecha,
                asistencias.hora_entrada,
                asistencias.hora_salida,
                asistencias.tipo_salida,
                totem_entrada.codigo,
                totem_salida.codigo,
                tarjetas.uid

            FROM asistencias

            INNER JOIN alumnos
                ON asistencias.alumno_id = alumnos.id

            LEFT JOIN totems AS totem_entrada
                ON asistencias.totem_entrada_id =
                   totem_entrada.id

            LEFT JOIN totems AS totem_salida
                ON asistencias.totem_salida_id =
                   totem_salida.id

            LEFT JOIN tarjetas
                ON tarjetas.alumno_id = alumnos.id
                AND tarjetas.estado = 'activa'

            ORDER BY
                asistencias.fecha DESC,
                asistencias.hora_entrada DESC
            """
        )

        return cursor.fetchall()

    finally:
        conexion.close()


def obtener_inasistencias(
    periodo="mensual",
    fecha_referencia=None
):
    fecha_inicio, fecha_fin = obtener_rango_periodo(
        periodo,
        fecha_referencia
    )

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            WITH fechas_registradas AS (
                SELECT DISTINCT fecha
                FROM asistencias
                WHERE fecha BETWEEN ? AND ?
            ),
            total_jornadas AS (
                SELECT COUNT(*) AS cantidad
                FROM fechas_registradas
            )

            SELECT
                alumnos.id,
                alumnos.nombre_completo,
                alumnos.curso,

                (
                    SELECT cantidad
                    FROM total_jornadas
                ) - COUNT(
                    DISTINCT asistencias.fecha
                ) AS inasistencias,

                (
                    SELECT cantidad
                    FROM total_jornadas
                ) AS jornadas_periodo

            FROM alumnos

            LEFT JOIN asistencias
                ON asistencias.alumno_id =
                   alumnos.id
                AND asistencias.fecha IN (
                    SELECT fecha
                    FROM fechas_registradas
                )

            GROUP BY
                alumnos.id,
                alumnos.nombre_completo,
                alumnos.curso

            ORDER BY
                inasistencias DESC,
                alumnos.curso,
                alumnos.nombre_completo
            """,
            (
                fecha_inicio,
                fecha_fin
            )
        )

        return cursor.fetchall()

    finally:
        conexion.close()


def obtener_atrasos(
    periodo="diario",
    fecha_referencia=None
):
    fecha_inicio, fecha_fin = obtener_rango_periodo(
        periodo,
        fecha_referencia
    )

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT
                asistencias.id,
                alumnos.nombre_completo,
                alumnos.curso,
                asistencias.fecha,
                asistencias.hora_entrada

            FROM asistencias

            INNER JOIN alumnos
                ON asistencias.alumno_id =
                   alumnos.id

            WHERE asistencias.fecha
                BETWEEN ? AND ?

              AND asistencias.hora_entrada
                IS NOT NULL

              AND asistencias.hora_entrada > ?

            ORDER BY
                asistencias.fecha DESC,
                asistencias.hora_entrada ASC
            """,
            (
                fecha_inicio,
                fecha_fin,
                HORA_LIMITE_ATRASO
            )
        )

        filas = cursor.fetchall()

        hora_limite = datetime.strptime(
            HORA_LIMITE_ATRASO,
            "%H:%M:%S"
        )

        atrasos = []

        for fila in filas:
            hora_entrada = datetime.strptime(
                fila[4],
                "%H:%M:%S"
            )

            segundos_atraso = (
                hora_entrada - hora_limite
            ).total_seconds()

            minutos_atraso = math.ceil(
                segundos_atraso / 60
            )

            atrasos.append(
                (
                    fila[0],
                    fila[1],
                    fila[2],
                    fila[3],
                    fila[4],
                    minutos_atraso
                )
            )

        return atrasos

    finally:
        conexion.close()


if __name__ == "__main__":
    registros = obtener_asistencias()

    print(
        "Registros de asistencia:",
        len(registros)
    )