from base_datos import obtener_conexion


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
                asistencias.hora,
                totems.codigo,
                asistencias.evento_id
            FROM asistencias
            INNER JOIN alumnos
                ON asistencias.alumno_id = alumnos.id
            LEFT JOIN totems
                ON asistencias.totem_id = totems.id
            ORDER BY
                asistencias.fecha DESC,
                asistencias.hora DESC
            """
        )

        return cursor.fetchall()

    finally:
        conexion.close()


if __name__ == "__main__":
    registros = obtener_asistencias()

    if registros:
        print("REGISTROS DE ASISTENCIA")
        print("-------------------------")

        for registro in registros:
            print("ID:", registro[0])
            print("Nombre:", registro[1])
            print("RUT:", registro[2])
            print("Curso:", registro[3])
            print("Fecha:", registro[4])
            print("Hora:", registro[5])
            print("Tótem:", registro[6])
            print("Evento:", registro[7])
            print("-------------------------")

    else:
        print("No hay registros de asistencia disponibles.")