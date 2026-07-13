import sqlite3

conexion = sqlite3.connect("data/asistencia.db")
cursor = conexion.cursor()

cursor.execute(
    "SELECT id, rut, nombre_completo, curso, uid FROM alumnos"
    )

alumnos = cursor.fetchall()

for alumno in alumnos:
    print("ID: ", alumno[0],",rut:", alumno[1], ",nombre: ", alumno[2], ",curso:", alumno[3], ",uid  :", alumno[4])

conexion.close()    