from base_datos import obtener_conexion

def obtener_alumnos():
    conexion = obtener_conexion()
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

    conexion.close()  

    return alumnos

def buscar_alumnos(termino):
    termino = termino.strip()

    if not termino:
        return []

    conexion = obtener_conexion()
    cursor = conexion.cursor()  

    patron_busqueda = f"%{termino}%"  

if __name__ == "__main__":
    alumnos = obtener_alumnos()

    for alumno in alumnos:
        print("ID: ", alumno[0],",rut:", alumno[1], ",nombre: ", alumno[2], ",curso:", alumno[3], ",uid  :", alumno[4])

  