import shutil
import sqlite3
from datetime import datetime


ruta_base_datos = "data/asistencia.db"

marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")

ruta_respaldo = (
    f"data/asistencia_respaldo_totem_id_{marca_tiempo}.db"
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

    if "totem_id" in nombres_columnas:
        print("La columna totem_id ya existe")

    else:
        cursor.execute(
            """
            ALTER TABLE asistencias
            ADD COLUMN totem_id INTEGER
            REFERENCES totems(id)
            """
        )

        conexion.commit()

        print("Columna totem_id agregada correctamente")
    print("Respaldo creado:", ruta_respaldo)

finally:
    conexion.close()