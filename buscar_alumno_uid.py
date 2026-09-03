from base_datos import obtener_conexion


def buscar_alumno_por_uid():
    uid_ingresado = input("Ingrese el UID de prueba: ")
    uid_ingresado = uid_ingresado.strip().replace(" ", "").upper()

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT
                alumnos.id,
                alumnos.rut,
                alumnos.nombre_completo,
                alumnos.curso,
                tarjetas.uid,
                tarjetas.estado
            FROM tarjetas
            INNER JOIN alumnos
                ON tarjetas.alumno_id = alumnos.id
            WHERE tarjetas.uid = ?
            LIMIT 1
            """,
            (uid_ingresado,)
        )

        alumno = cursor.fetchone()

        if alumno:
            print("Alumno encontrado")
            print("ID:", alumno[0])
            print("RUT:", alumno[1])
            print("Nombre:", alumno[2])
            print("Curso:", alumno[3])
            print("UID:", alumno[4])
            print("Estado:", alumno[5])
        else:
            print("No existe un alumno registrado con ese UID")
    finally:
        conexion.close()


if __name__ == "__main__":
    buscar_alumno_por_uid()
