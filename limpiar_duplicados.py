import sqlite3
import shutil

shutil.copy2(
    "data/asistencia.db",
    "data/asistencia_respaldo.db"
)

conexion = sqlite3.connect("data/asistencia.db")
cursor = conexion.cursor()

try:
    cursor.execute(
        """
        DELETE FROM asistencia
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM asistencia
            GROUP BY alumno_id, fecha
        )
        """)
    
    registros_eliminados = cursor.rowcount
    

    conexion.commit()
    print("limpieza completada correctamente")
    print("Registros duplicados eliminados:", registros_eliminados)
    print("respaldo  creado: data/asistencia_respaldo.db")

finally:
    conexion.close()
    