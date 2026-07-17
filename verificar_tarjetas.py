from base_datos import obtener_conexion


conexion = obtener_conexion()
cursor = conexion.cursor()


try:
    cursor.execute(
        """
        SELECT
            tarjetas.uid,
            alumnos.nombre_completo,
            tarjetas.estado
        FROM tarjetas
        INNER JOIN alumnos
            ON tarjetas.alumno_id = alumnos.id
        ORDER BY alumnos.id, tarjetas.id
        """
    )

    tarjetas = cursor.fetchall()

    if tarjetas:
        print("TARJETAS REGISTRADAS")
        print("--------------------")

        for tarjeta in tarjetas:
            print("UID:", tarjeta[0])
            print("Alumno:", tarjeta[1])
            print("Estado:", tarjeta[2])
            print("------------------")
    else:
        print("No existen tarjetas registradas")
finally:
    conexion.close()