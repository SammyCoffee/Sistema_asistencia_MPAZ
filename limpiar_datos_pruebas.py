from base_datos import obtener_conexion


FRASE_CONFIRMACION = "BORRAR DATOS DE PRUEBA"


def tabla_existe(cursor, nombre_tabla):
    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name = ?
        """,
        (nombre_tabla,)
    )

    return cursor.fetchone() is not None

def contar_registros(cursor, tabla):
    cursor.execute(
        f"SELECT COUNT(*) FROM {tabla}"
    )

    return cursor.fetchone()[0]

def limpiar_datos_prueba():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    tablas_a_limpiar = [
        "asistencias",
        "asistencia",
        "tarjetas",
        "alumnos"
    ]

    tablas_existentes = [
        tabla
        for tabla in tablas_a_limpiar
        if tabla_existe(cursor, tabla)
    ]

    print ("DATOS ACTUALES")
    print ("=" * 40)

    for tabla in tablas_existentes:
        cantidad = contar_registros(
            cursor,
            tabla
        )

        print(f"{tabla}: {cantidad}")

    print("")
    print(
        "Los totems y su configuracion se conservaran."
    )
    print(
        "Se eliminaran alumnos, tarjetas y asistencias."
    )    
    print("")
    print(
        "Escribe exactamente esta frase para continuar:"
    )
    print(FRASE_CONFIRMACION)

    confirmacion = input("> ").strip()

    if confirmacion != FRASE_CONFIRMACION:
        print("Operacion cancelada")
        conexion.close()
        return
    try:
        if tabla_existe(cursor, "asistencias"):
            cursor.execute(
                "DELETE FROM asistencias"
            )
        if tabla_existe(cursor, "asistencia"):
            cursor.execute(
                "DELETE FROM asistencia"
            )
        if tabla_existe(cursor, "tarjetas"):
            cursor.execute(
                "DELETE FROM tarjetas"
            )        

        if tabla_existe(cursor, "alumnos"):
            cursor.execute(
                "DELETE FROM alumnos"
            )

        if tabla_existe(cursor, "sqlite_sequence"):
            cursor.execute(
                """
                DELETE FROM sqlite_sequence
                WHERE name IN (
                    'alumnos',
                    'tarjetas',
                    'asistencias',
                    'asistencia'
                )
                """
            )
        conexion.commit()

    except  Exception as error:
        conexion.rollback()

        print("Ocurrio un error")
        print(error)    

        conexion.close()
        return
    
    print("")
    print("Limpieza completada correctamente")
    print("=" * 40)

    for tabla in tablas_existentes:
        cantidad = contar_registros(
            cursor,
            tabla
        )

        print(f"{tabla}: {cantidad}")

    if tabla_existe(cursor, "totems"):
        cantidad_totems = contar_registros(
            cursor,
            "totems"
        )

        print(
            f"Tótems conservados: {cantidad_totems}"
        )    

    conexion.close()

if __name__ == "__main__":
    limpiar_datos_prueba()
