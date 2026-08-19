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
        FROM alumnos
        LEFT JOIN tarjetas
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

    cursor.execute(
        """
        SELECT
            alumnos.id,
            alumnos.rut,
            alumnos.nombre_completo,
            alumnos.curso,
            tarjetas.uid
        FROM alumnos
        LEFT JOIN tarjetas
            ON tarjetas.alumno_id = alumnos.id
        WHERE alumnos.nombre_completo LIKE ?
            OR alumnos.rut LIKE ?
            OR alumnos.curso LIKE ?
        LIMIT 20
        """,
        (
            patron_busqueda,
            patron_busqueda,
            patron_busqueda
        )
    )

    alumnos = cursor.fetchall()

    conexion.close()

    return alumnos


if __name__ == "__main__":
    alumnos = obtener_alumnos()

    print(
        "Cantidad de alumnos:",
        len(alumnos)
    )