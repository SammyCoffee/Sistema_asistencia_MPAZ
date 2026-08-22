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
            tarjetas.uid,
            tarjetas.estado
        FROM alumnos
        LEFT JOIN tarjetas
            ON tarjetas.id = (
                SELECT t2.id
                FROM tarjetas AS t2
                WHERE t2.alumno_id = alumnos.id
                ORDER BY
                    CASE WHEN t2.estado = 'activa' THEN 0 ELSE 1 END,
                    t2.id DESC
                LIMIT 1
            )
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
            tarjetas.uid,
            tarjetas.estado
        FROM alumnos
        LEFT JOIN tarjetas
            ON tarjetas.id = (
                SELECT t2.id
                FROM tarjetas AS t2
                WHERE t2.alumno_id = alumnos.id
                ORDER BY
                    CASE WHEN t2.estado = 'activa' THEN 0 ELSE 1 END,
                    t2.id DESC
                LIMIT 1
            )
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