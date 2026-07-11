import sqlite3

conexion= sqlite3.connect("data/asistencia.db")
cursor=conexion.cursor()

rut="12.345678-9"
nombre_completo="Juan Perez"
curso="1A"
uid="123456789"

try:
    cursor.execute(
        """
        INSERT INTO alumnos (rut, nombre_completo, curso, uid)
        VALUES (?,?,?,?)
        """,
        (rut, nombre_completo, curso, uid)

    )

    conexion.commit()
    print("Alumno agregado correctamente")

except sqlite3.IntegrityError:
    print("No se pudo agregar: el rut o el uid ya estan registrados" )

finally:
    conexion.close()