import sqlite3

from base_datos import obtener_conexion


COLUMNAS_NUEVAS = {
    "hora_entrada": "TEXT",
    "hora_salida": "TEXT",
    "tipo_salida": "TEXT",
    "totem_entrada_id": "INTEGER",
    "totem_salida_id": "INTEGER",
    "evento_entrada_id": "TEXT",
    "evento_salida_id": "TEXT",
}


def obtener_columnas(cursor):
    cursor.execute(
        "PRAGMA table_info(asistencias)"
    )

    return {
        fila[1]
        for fila in cursor.fetchall()
    }


def migrar_asistencias():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        columnas_actuales = obtener_columnas(
            cursor
        )

        print("Columnas actuales:")
        print(sorted(columnas_actuales))
        print()

        for nombre, tipo in COLUMNAS_NUEVAS.items():

            if nombre in columnas_actuales:
                print(
                    f"{nombre}: ya existe"
                )
                continue

            cursor.execute(
                f"""
                ALTER TABLE asistencias
                ADD COLUMN {nombre} {tipo}
                """
            )

            print(
                f"{nombre}: agregada"
            )

        cursor.execute(
            """
            UPDATE asistencias
            SET hora_entrada = hora
            WHERE hora_entrada IS NULL
            """
        )

        cursor.execute(
            """
            UPDATE asistencias
            SET totem_entrada_id = totem_id
            WHERE totem_entrada_id IS NULL
            """
        )

        cursor.execute(
            """
            UPDATE asistencias
            SET evento_entrada_id = evento_id
            WHERE evento_entrada_id IS NULL
            """
        )

        cursor.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS
                indice_evento_entrada_asistencias
            ON asistencias(evento_entrada_id)
            """
        )

        cursor.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS
                indice_evento_salida_asistencias
            ON asistencias(evento_salida_id)
            """
        )

        cursor.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS
                indice_alumno_fecha_asistencias
            ON asistencias(alumno_id, fecha)
            """
        )

        conexion.commit()

        print()
        print(
            "Migracion completada correctamente"
        )

    except sqlite3.Error as error:

        conexion.rollback()

        print(
            "ERROR durante la migracion:"
        )
        print(error)

        raise

    finally:
        conexion.close()


if __name__ == "__main__":
    migrar_asistencias()
    