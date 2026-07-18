import shutil
import sqlite3
from datetime import datetime


ruta_base_datos = "data/asistencia.db"

marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")

ruta_respaldo = (
    f"data/asistencia_respaldo_evento_id{marca_tiempo}.db"
    
)

shutil.copy2(ruta_base_datos, ruta_respaldo)

conexion = sqlite3.connect(ruta_base_datos)
cursor = conexion.cursor()

try:

    cursor.execute("PRAGMA table_info(asistencias)")

    columnas = cursor.fetchall()
    nombres_columnas = []

    for columna in columnas:
        nombres_columnas.append(columna[1])

    if "evento_id" not in nombres_columnas:
        cursor.execute(
            """
            ALTER TABLE asistencias
            ADD COLUMN evento_id TEXT
            """
        )    

        print("Columna evento_id agregada correctamente")
    
    else:
        print("La columna evento_id ya existe")

    cursor.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS
        indice_evento_id_asistencias
        ON asistencias(evento_id)
        """
    )

    conexion.commit()

    print("Proteccion contra eventos repetidos creada")
    print("Respaldo creado:", ruta_respaldo)

except Exception as error:
    conexion.rollback()

    print("No se pudo completar la migracion")
    print("Error:", error)

finally:
    conexion.close()                