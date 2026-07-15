import shutil
from datetime import datetime

from base_datos import obtener_conexion, crear_tablas

marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")

ruta_original = "data/asistencia.db"
ruta_respaldo = (
    f"data/asistencia_respaldo_tarjetas_{marca_tiempo}.db"
)

shutil.copy2(ruta_original,ruta_respaldo)


crear_tablas()

conexion = obtener_conexion()
cursor = conexion.cursor()

fecha_asignacion = datetime.now().strftime("%Y-%m-%d")

try:
    cursor.execute(
        """
        SELECT id, uid FROM alumnos WHERE uid IS NOT NULL
        """
    )
    
    alumnos = cursor.fetchall()
    
    tarjetas_copiadas = 0
    
    for alumno in alumnos:
        alumno_id = alumno[0]
        uid = alumno[1]
        
        if uid and uid.strip():
            uid = uid.strip().replace(" ","").upper()

            cursor.execute(
                """
                INSERT OR IGNORE
INTO tarjetas (
                    alumno_id,
                    uid,
                    estado,
                    fecha_asignacion     
                )                
                VALUES (?, ?, ?, ?)
                """,
                (
                    alumno_id,
                    uid,
                    "activa",
                    fecha_asignacion
                )
            )            
            tarjetas_copiadas += cursor.rowcount

    conexion.commit()
    
    print("Migracion  de tarjetas completada")
    print("Tarjetas copiadas", tarjetas_copiadas)
    print("Respaldo creado", ruta_respaldo)
    
finally:
    conexion.close()   