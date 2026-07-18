import csv
from datetime import datetime
from pathlib import Path

from base_datos import obtener_conexion


CARPETAS_REPORTES = Path("reportes")

def exportar_asistencias():
    CARPETAS_REPORTES.mkdir(exist_ok=True)

    marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")

    ruta_reporte = (
        CARPETAS_REPORTES
        / F"asistencias_{marca_tiempo}.csv"
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

            ORDER BY
                asistencias.fecha,
                asistencias.hora        
            """
        )

        registros = cursor.fetchall()

    finally:
        conexion.close()

    with ruta_reporte.open(
        mode="w",
        encoding="utf-8-sig",
        newline=""
    )as archivo:
        escritor = csv.writer(
            archivo,
            delimiter=";"
        )

        escritor.writerow(
            [
                "ID asistencia",
                "RUT",
                "Nombre_completo",
                "Curso",
                "Fecha",
                "Hora",
                "Tótem",
                "Evento_ID"
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

if __name__ ==  "__main__":
    ruta, cantidad = exportar_asistencias()

    print("Reporte creada correctamente")
    print("Archivo:", ruta)
    print("Asistencias exportadas:", cantidad) 