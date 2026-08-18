import sqlite3

conexion = sqlite3.connect("data/asistencia.db")
cursor = conexion.cursor()

cursor.execute(
    """
    SELECT 
    alumnos.id,
    alumnos.rut, 
    alumnos.nombre_completo,
    alumnos.curso,
    tarjetas.uid
    FROM alumnos LEFT JOIN tarjetas
        ON tarjetas.alumno_id = alumnos.id
        """
    )

alumnos = cursor.fetchall()

for alumno in alumnos:
    print("ID: ", alumno[0],",rut:", alumno[1], ",nombre: ", alumno[2], ",curso:", alumno[3], ",uid  :", alumno[4])

conexion.close()    