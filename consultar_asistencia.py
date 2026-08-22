import sqlite3

conexion = sqlite3.connect("data/asistencia.db")
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
            asistencias.hora
        FROM asistencias
        INNER JOIN alumnos
            ON asistencias.alumno_id = alumnos.id
        ORDER BY asistencias.fecha DESC, asistencias.hora DESC
        """
    )

    registros = cursor.fetchall()

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
            print("-------------------------")
    else:
        print("No hay registros de asistencia disponibles.")

finally:
    conexion.close()