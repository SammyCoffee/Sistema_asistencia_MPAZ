
from datetime import datetime
from pathlib import Path
import sqlite3

# ==================================================
# BASE DE DATOS DE DEMOSTRACIÓN
# No contiene información real de estudiantes.
# ==================================================

RUTA_BASE_DEMO = Path(
    "data/asistencia_demo.db"
)


def crear_base_demostracion():
    # Creamos la carpeta data si no existe.
    RUTA_BASE_DEMO.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Si ya existe una demostración anterior,
    # la reemplazamos por una nueva.
    if RUTA_BASE_DEMO.exists():
        RUTA_BASE_DEMO.unlink()

    conexion = sqlite3.connect(
        RUTA_BASE_DEMO
    )

    cursor = conexion.cursor()

    cursor.execute(
        "PRAGMA foreign_keys = ON"
    )

    try:
        # ==========================================
        # TABLA DE ALUMNOS
        # ==========================================
        cursor.execute(
            """
            CREATE TABLE alumnos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rut TEXT NOT NULL UNIQUE,
                nombre_completo TEXT NOT NULL,
                curso TEXT NOT NULL
            )
            """
        )

        # ==========================================
        # TABLA DE TÓTEMS
        # ==========================================
        cursor.execute(
            """
            CREATE TABLE totems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT NOT NULL UNIQUE,
                nombre TEXT NOT NULL,
                ubicacion TEXT,
                fecha_registro TEXT NOT NULL,
                ultima_conexion TEXT,
                estado TEXT NOT NULL DEFAULT 'activo'
            )
            """
        )

        # ==========================================
        # TABLA DE TARJETAS RFID
        # ==========================================
        cursor.execute(
            """
            CREATE TABLE tarjetas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alumno_id INTEGER NOT NULL,
                uid TEXT NOT NULL UNIQUE,
                estado TEXT NOT NULL DEFAULT 'activa',
                fecha_asignacion TEXT NOT NULL,
                fecha_bloqueo TEXT,
                FOREIGN KEY (alumno_id)
                    REFERENCES alumnos(id)
            )
            """
        )

        # ==========================================
        # TABLA DE ASISTENCIAS
        # ==========================================
        cursor.execute(
            """
            CREATE TABLE asistencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alumno_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                hora TEXT NOT NULL,
                totem_id INTEGER,
                evento_id TEXT,
                FOREIGN KEY (alumno_id)
                    REFERENCES alumnos(id),
                FOREIGN KEY (totem_id)
                    REFERENCES totems(id)
            )
            """
        )

        # Evita registrar dos veces el mismo evento.
        cursor.execute(
            """
            CREATE UNIQUE INDEX
            indice_evento_id
            ON asistencias(evento_id)
            WHERE evento_id IS NOT NULL
            """
        )

        fecha_actual = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # ==========================================
        # TÓTEM FICTICIO
        # ==========================================
        cursor.execute(
            """
            INSERT INTO totems (
                codigo,
                nombre,
                ubicacion,
                fecha_registro,
                estado
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                "MPAZ-DEMO-01",
                "Tótem de demostración",
                "Entrada ficticia",
                fecha_actual,
                "activo"
            )
        )

        # ==========================================
        # ESTUDIANTES FICTICIOS
        # ==========================================
        estudiantes_demo = [
            (
                "11111111-1",
                "Estudiante Demo Uno",
                "1A"
            ),
            (
                "22222222-2",
                "Estudiante Demo Dos",
                "2A"
            ),
            (
                "33333333-3",
                "Estudiante Demo Tres",
                "3B"
            ),
            (
                "44444444-4",
                "Estudiante Demo Cuatro",
                "4B"
            )
        ]

        cursor.executemany(
            """
            INSERT INTO alumnos (
                rut,
                nombre_completo,
                curso
            )
            VALUES (?, ?, ?)
            """,
            estudiantes_demo
        )

        # ==========================================
        # TARJETAS FICTICIAS
        # ==========================================
        tarjetas_demo = [
            (
                1,
                "A1B2C3D4",
                "activa",
                fecha_actual
            ),
            (
                2,
                "B1C2D3E4",
                "activa",
                fecha_actual
            ),
            (
                3,
                "C1D2E3F4",
                "activa",
                fecha_actual
            ),
            (
                4,
                "D1E2F3A4",
                "activa",
                fecha_actual
            )
        ]

        cursor.executemany(
            """
            INSERT INTO tarjetas (
                alumno_id,
                uid,
                estado,
                fecha_asignacion
            )
            VALUES (?, ?, ?, ?)
            """,
            tarjetas_demo
        )

        conexion.commit()

    except Exception as error:
        conexion.rollback()

        print(
            "Ocurrió un error al crear "
            "la base de demostración"
        )
        print(error)

        conexion.close()
        return

    conexion.close()

    print(
        "Base de demostración creada correctamente"
    )
    print(
        "Archivo:",
        RUTA_BASE_DEMO
    )
    print("Estudiantes ficticios: 4")
    print("Tarjetas ficticias: 4")
    print("Tótems ficticios: 1")
    print("")
    print(
        "La base real data/asistencia.db "
        "NO fue modificada."
    )


if __name__ == "__main__":
    crear_base_demostracion()