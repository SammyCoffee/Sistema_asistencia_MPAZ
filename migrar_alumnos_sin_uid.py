import shutil
import sqlite3
from datetime import datetime

ruta_base_datos = "data/asistencia.db"

marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")

ruta_respaldo = (
    f"data/asistencia_respaldo_sin_uid{marca_tiempo}.db"
)

shutil.copy2(ruta_base_datos, ruta_respaldo)

conexion = sqlite3.connect(ruta_base_datos)
cursor = conexion.cursor()

try:
        
    conexion.execute("PRAGMA foreign_keys = OFF")

    cursor.execute("BEGIN")

    cursor.execute("DROP TABLE IF EXISTS alumnos_nuevos")

    cursor.execute(
            """
            CREATE TABLE alumnos_nuevo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rut TEXT NOT NULL UNIQUE,
            nombre_completo TEXT NOT NULL,
            curso TEXT NOT NULL
            )
            """
        )

    cursor.execute(
            """
            INSERT INTO alumnos_nuevo(
                id,
                rut,
                nombre_completo,
                curso
            )
            SELECT
                id,
                rut,
                nombre_completo,
                curso
            FROM alumnos     
            """
    )

    cursor.execute("DROP TABLE alumnos")

    cursor.execute(
        """
        ALTER TABLE alumnos_nuevo
        RENAME TO alumnos    
        """ 
    )

    conexion.commit()

    print("Migracion completada correctamente")
    print("La columna antigua UID fue eliminada de alumnos")
    print("Respaldo creado:", ruta_respaldo)

except Exception as error:
    conexion.rollback()

    print("No se pudo completar la migracion")
    print("Error:" error)

finally:
    conexion.close()    

