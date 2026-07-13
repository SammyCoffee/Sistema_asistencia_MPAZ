import sqlite3

uid_ingresado = input("Ingrese el UID de prueba:  ")
uid_ingresado = uid_ingresado.strip().upper()

conexion = sqlite3.connect("data/asistencia.db")
cursor = conexion.cursor()

cursor.execute(
    """

    SELECT id, rut, nombre_completo, curso, uid
    FROM alumnos
    WHERE uid = ?
    """,
    (uid_ingresado,)

)

alumno = cursor.fetchone()

if alumno:
    print("Alumno encontrado")
    print("ID:",  alumno[0])
    print("RUT:", alumno[1])
    print("Nombre:", alumno[2])
    print("Curso:", alumno[3])
    print("UID:", alumno[4])

else: 
    print("no existe un alumno registrado con ese UID")

conexion.close()
