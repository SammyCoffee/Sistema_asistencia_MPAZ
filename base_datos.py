import sqlite3

RUTA_BASE_DATOS = "data/asistencia.db"


def obtener_conexion():
    conexion = sqlite3.connect(RUTA_BASE_DATOS)
    conexion.execute("PRAGMA foreign_keys = ON")
    
    return conexion
def guardar_alumno(rut, nombre_completo, curso, uid):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    
    try:
        cursor.execute(
                """
                INSERT INTO alumnos(rut, nombre_completo, curso, uid)
                VALUES (?, ?, ?, ?)
                """,
                (rut, nombre_completo, curso, uid)
        )
        
        conexion.commit()
        
        return True
    except sqlite3.IntegrityError:
        return False
    
    finally:
        conexion.close()
    
def buscar_alumno_por_uid(uid):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    try: 
        cursor.execute(
            """ 
            SELECT id,nombre_completo,curso
            FROM alumnos
            WHERE uid = ?
            """,
            (uid,)
        )
        
        
        alumno = cursor.fetchone()
        return alumno
    
    finally:
        conexion.close()

def guardar_asistencia(alumno_id, fecha, hora): 
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    try:        
        cursor.execute(
            """ 
            SELECT id
            FROM asistencias
            WHERE alumno_id = ? AND fecha= ?
            """,
            (alumno_id, fecha)
        )
        asistencias_existente = cursor.fetchone()
        
        if asistencias_existente:
            return False
        
        
        cursor.execute(
                """INSERT INTO asistencias (alumno_id, fecha,hora)
                    VALUES (?, ?, ?)
                    """,
                    (alumno_id, fecha, hora )
                    
        )
        
        conexion.commit()
        
        return True
    
    finally:
        conexion.close()
        

def crear_tablas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS alumnos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rut TEXT NOT NULL UNIQUE,
                nombre_completo TEXT NOT NULL,
                curso TEXT NOT NULL,
                uid TEXT NOT NULL UNIQUE
            )
            """
        )
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS asistencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alumno_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                hora TEXT NOT NULL,
                FOREIGN KEY (alumno_id) REFERENCES alumnos(id)
            )
            """
        )
        conexion.commit()
        
        print("Tablas creadas correctamente")
    finally:
        conexion.close()    
if __name__ == "__main__":
    crear_tablas()  