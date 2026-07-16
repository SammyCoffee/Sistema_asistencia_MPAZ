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
    
    conexion.execute("PRAGMA foreing_keys = OFF")

    cursor.execute("BEGIN")

    

    cursor.execute(
        """

        """
    )