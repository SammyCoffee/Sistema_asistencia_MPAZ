import sqlite3
from datetime import datetime

from base_datos import RUTA_BASE_DATOS


def columna_existe(cursor, tabla, columna):
    cursor.execute(
        f"PRAGMA table_info({tabla})"
    )

    columnas = [
        fila[1]
        for fila in cursor.fetchall()
    ]

    return columna in columnas


def migrar():
    conexion = sqlite3.connect(
        RUTA_BASE_DATOS
    )

    cursor = conexion.cursor()

    fecha_actual = datetime.now().strftime(
        "%Y-%m-%d"
    )

    try:
        conexion.execute(
            "PRAGMA foreign_keys = OFF"
        )

        conexion.execute(
            "BEGIN"
        )

        # ==========================================
        # 1. AMPLIAR TABLA ALUMNOS
        # ==========================================

        if not columna_existe(
            cursor,
            "alumnos",
            "estado"
        ):
            cursor.execute(
                """
                ALTER TABLE alumnos
                ADD COLUMN estado TEXT
                NOT NULL DEFAULT 'activo'
                """
            )

        if not columna_existe(
            cursor,
            "alumnos",
            "fecha_baja"
        ):
            cursor.execute(
                """
                ALTER TABLE alumnos
                ADD COLUMN fecha_baja TEXT
                """
            )

        # ==========================================
        # 2. RECONSTRUIR TABLA TARJETAS
        # ==========================================

        cursor.execute(
            """
            ALTER TABLE tarjetas
            RENAME TO tarjetas_anterior
            """
        )

        cursor.execute(
            """
            CREATE TABLE tarjetas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                alumno_id INTEGER,

                uid TEXT NOT NULL UNIQUE,

                estado TEXT
                NOT NULL DEFAULT 'disponible',

                fecha_registro TEXT NOT NULL,

                fecha_asignacion TEXT,

                fecha_bloqueo TEXT,

                fecha_extravio TEXT,

                FOREIGN KEY (alumno_id)
                    REFERENCES alumnos(id)
            )
            """
        )

        cursor.execute(
            """
            INSERT INTO tarjetas (
                id,
                alumno_id,
                uid,
                estado,
                fecha_registro,
                fecha_asignacion,
                fecha_bloqueo,
                fecha_extravio
            )

            SELECT
                id,
                alumno_id,
                uid,
                estado,
                COALESCE(
                    fecha_asignacion,
                    ?
                ),
                fecha_asignacion,
                fecha_bloqueo,
                NULL
            FROM tarjetas_anterior
            """,
            (
                fecha_actual,
            )
        )

        cursor.execute(
            """
            DROP TABLE tarjetas_anterior
            """
        )

        conexion.commit()

        print(
            "Migracion de administracion "
            "completada correctamente"
        )

    except Exception:
        conexion.rollback()
        raise

    finally:
        conexion.execute(
            "PRAGMA foreign_keys = ON"
        )

        conexion.close()


if __name__ == "__main__":
    migrar()