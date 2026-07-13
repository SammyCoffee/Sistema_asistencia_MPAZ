import sqlite3

conexion = sqlite3.connect("data/asistencia.db")
cursor = conexion.cursor()

try:
    cursor.execute(
        """
        SELECT
            asistencia.id,
            alumnos.nombre_completo,
            alumnos.rut,
            alumnos.curso,
            asistencia.fecha,
            asistencia.hora
        FROM asistencia
        INNER JOIN alumnos
            ON asistencia.alumno_id = alumnos.id
         ORDER BY asistencia.fecha DESC, asistencia.hora DESC
        """ 

    )

    registros = cursor.fetchall()

    if registros:
        print("RESGISTROS DE ASISTENCIA")
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
        