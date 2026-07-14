import sqlite3

rut = input("Ingrese el rut del alumno: ")
nombre_completo = input("Ingrese el nombre completo del alumno: ")
curso = input("Ingrese el curso del alumno: ")
uid = input("Ingrese el uid del alumno: ")

rut = rut.strip()
nombre_completo = nombre_completo.strip()
curso = curso.strip().upper()
uid = uid.strip().replace(" ", "").upper()


conexion = sqlite3.connect("data/asistencia.db")
cursor = conexion.cursor()

try:
    if not rut or not nombre_completo or not curso or not uid:
        print("No se pudo agregar: todos los campos son obligatorios")
    
    else:
        cursor.execute(
            """
            INSERT INTO alumnos (rut, nombre_completo, curso, uid)
            VALUES (?,?,?,?)
            """,
            (rut, nombre_completo, curso, uid)

        )

        conexion.commit()
        
        print("Alumno agregado correctamente")
        print("Rut:", rut)
        print("Nombre:", nombre_completo)
        print("Curso:", curso)
        print("UID:", uid)
          
except sqlite3.IntegrityError:
    print("No se pudo agregar: el rut o el uid ya estan registrados" )

finally:
    conexion.close()