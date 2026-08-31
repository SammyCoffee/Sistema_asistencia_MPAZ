import csv
from datetime import date, datetime, timedelta
from pathlib import Path

from base_datos import obtener_conexion


CARPETA_REPORTES = Path("reportes")


def obtener_rango_fechas(periodo):
    hoy = date.today()

    if periodo == "diario":
        fecha_desde = hoy
        fecha_hasta = hoy

    elif periodo == "semanal":
        fecha_desde = hoy - timedelta(days=6)
        fecha_hasta = hoy

    elif periodo == "mensual":
        fecha_desde = hoy.replace(day=1)
        fecha_hasta = hoy

    else:
        raise ValueError("Periodo de reporte no valido")

    return (
        fecha_desde.strftime("%Y-%m-%d"),
        fecha_hasta.strftime("%Y-%m-%d")
    )


def exportar_asistencias(periodo="diario"):
    CARPETA_REPORTES.mkdir(exist_ok=True)

    fecha_desde, fecha_hasta = obtener_rango_fechas(periodo)

    marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")

    ruta_reporte = (
        CARPETA_REPORTES
        / f"asistencias_{periodo}_{marca_tiempo}.csv"
    )

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT
                asistencias.id,
                alumnos.rut,
                alumnos.nombre_completo,
                alumnos.curso,
                asistencias.fecha,
                asistencias.hora,
                totems.codigo,
                asistencias.evento_id
            FROM asistencias

            INNER JOIN alumnos
                ON asistencias.alumno_id = alumnos.id

            LEFT JOIN totems
                ON asistencias.totem_id = totems.id

            WHERE asistencias.fecha BETWEEN ? AND ?

            ORDER BY
                asistencias.fecha,
                asistencias.hora
            """,
            (
                fecha_desde,
                fecha_hasta
            )
        )

        registros = cursor.fetchall()

    finally:
        conexion.close()

    with ruta_reporte.open(
        mode="w",
        encoding="utf-8-sig",
        newline=""
    ) as archivo:

        escritor = csv.writer(
            archivo,
            delimiter=";"
        )

        escritor.writerow(
            [
                "ID asistencia",
                "RUT",
                "Nombre completo",
                "Curso",
                "Fecha",
                "Hora",
                "Tótem",
                "Evento ID"
            ]
        )

        for registro in registros:
            escritor.writerow(
                [
                    registro[0],
                    registro[1],
                    registro[2],
                    registro[3],
                    registro[4],
                    registro[5],
                    registro[6] or "Registro manual",
                    registro[7] or "Sin evento"
                ]
            )

    return ruta_reporte, len(registros)


if __name__ == "__main__":
    ruta, cantidad = exportar_asistencias("diario")

    print("Reporte creado correctamente")
    print("Archivo:", ruta)
    print("Asistencias exportadas:", cantidad)