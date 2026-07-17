import sqlite3
from datetime import datetime

RUTA_BASE_DATOS = "data/asistencia.db"


def obtener_conexion():
    conexion = sqlite3.connect(RUTA_BASE_DATOS)
    conexion.execute("PRAGMA foreign_keys = ON")
    
    return conexion
def guardar_alumno(rut, nombre_completo, curso, uid):
    fecha_asignacion = datetime.now().strftime("%Y-%m-%d")

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    
    try:
        cursor.execute(
                """
                INSERT INTO alumnos(
                    rut, 
                    nombre_completo, 
                    curso
                )
                VALUES (?, ?, ?)
                """,
                (
                    rut, 
                    nombre_completo, 
                    curso
                )
        )

        alumno_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO tarjetas (
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
        
        conexion.commit()
        
        return True
    
    except sqlite3.IntegrityError:
        conexion.rollback()

        return False
    
    finally:
        conexion.close()

def bloquear_tarjeta(uid):
    uid = uid.strip().replace(" ", "").upper()
    
    fecha_bloqueo = datetime.now().strftime("%Y-%m-%d")
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    try:
        cursor.execute(
            """
            UPDATE tarjetas
            SET estado = 'bloqueada',
                fecha_bloqueo = ?
            WHERE uid = ?
                AND estado = 'activa'
            """,
            (fecha_bloqueo, uid)
        )
        if cursor.rowcount == 0:
            return False
        
        conexion.commit()
        
        return True
    
    finally:
        conexion.close()

def asignar_tarjeta_por_rut(rut,uid):
    rut = rut.strip()
    uid = uid.strip().replace(" ","").upper()


    fecha_asignacion = datetime.now().strftime("%Y-%m-%d")


    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:

        cursor.execute(
            """
            SELECT id, nombre_completo, curso
            FROM alumnos
            WHERE rut = ?
            """,
            (rut,)
        )

        alumno = cursor.fetchone()

        if not alumno:
            return  {
                "resultado": "alumno_no_existe"
            }
        cursor.execute(
            """
            SELECT uid
            FROM tarjetas
            WHERE alumno_id = ?
                AND estado = 'activa'
            LIMIT 1
            """,
            (alumno[0],)    
        )        

        tarjeta_activa = cursor.fetchone()

        if tarjeta_activa:
            return{
                "resultado": "ya_tiene_tarjeta",
                "alumno": alumno[1],
                "uid": tarjeta_activa[0]
            }
        
        try:
            cursor.execute(
                """
               INSERT INTO tarjetas (
                alumno_id,
                uid,
                estado,
                fecha_asignacion
            )
                VALUES (?, ?, ?, ?)
                """,
            (
                    alumno[0],
                    uid,
                    "activa",
                    fecha_asignacion
                )
            )
        except sqlite3.IntegrityError:
            return {
                "resultado": "uid_repetido"
            }
        
        conexion.commit()

        return {
            "resultado": "asignada",
            "alumno": alumno[1],
            "curso": alumno[2],
            "uid": uid,
            "fecha": fecha_asignacion
        }
    finally:
        conexion.close()  
        
    
def buscar_alumno_por_uid(uid):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    try: 
        cursor.execute(
            """ 
            SELECT 
                alumnos.id,
                alumnos.nombre_completo,
                alumnos.curso,
                tarjetas.estado
            FROM tarjetas
            INNER JOIN alumnos
                ON tarjetas.alumno_id = alumnos.id
            WHERE tarjetas.uid = ?
            LIMIT 1
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

def guardar_totem(codigo, nombre, ubicacion):
    codigo = codigo.strip().upper()
    nombre = nombre.strip()
    ubicacion = ubicacion.strip()

    fecha_registro = datetime.now().strftime("%Y-%m-%d")

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO totems (
                codigo,
                nombre,
                ubicacion,
                estado,
                fecha_registro
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                codigo,
                nombre,
                ubicacion,
                "activo",
                fecha_registro
            )
        )

        conexion.commit()

        return {
            "resultado": "registrado",
            "codigo": codigo,
            "nombre": nombre,
            "ubicacion": ubicacion,
            "estado": "activo",
            "fecha_registro": fecha_registro
        }
    
    except sqlite3.IntegrityError:
        conexion.rollback()

        return {
            "resultado": "codigo_repetido"
        }
    finally:
        conexion.close
        
def validar_totem(codigo):
    codigo = codigo.strip().upper()

    momento_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conexion = obtener_conexion()
    cursor = conexion.cursor()


    try:
        cursor.execute(
            """
            SELECT
                id,
                codigo,
                nombre,
                ubicacion,
                estado
            FROM totems
            WHERE codigo = ?
            LIMIT 1    
            """,
            (codigo,)
        )        

        totem = cursor.fetchone()

        if not totem:
            return {
                "resultado": "no_existe",
                "codigo": codigo
            }    
            
        if totem[4] != "activo":
            return {
                "resultado": "inactivo",
                "codigo": totem[1],
                "nombre": totem[2]
            }

        cursor.execute(
            """
            UPDATE totems
            SET ultima_conexion = ?
            WHERE id = ?
            """,
            (
                momento_actual,
                totem[0]
            )
        )

        conexion.commit()

        return {
            "resultado": "activo",
            "id": totem[0],
            "codigo": totem[1],
            "nombre": totem[2],
            "ubicacion": totem[3],
            "ultima_conexion": momento_actual
        }
    
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
                curso TEXT NOT NULL
            )
            """
        )
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS 
        tarjetas (
                id INTEGER PRIMARY KEY 
        AUTOINCREMENT,
            alumno_id INTEGER NOT NULL,
            uid TEXT NOT NULL UNIQUE,
            estado TEXT NOT NULL DEFAULT 
        'activa',
            fecha_asignacion TEXT NOT 
        NULL,
            fecha_bloqueo TEXT,
            FOREIGN KEY (alumno_id) 
        REFERENCES alumnos(id)    
            )
            """
        )

        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS totems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT NOT NULL UNIQUE,
                nombre TEXT NOT NULL,
                ubicacion TEXT NOT NULL,
                estado TEXT NOT NULL DEFAULT 'activo',
                fecha_registro TEXT NOT NULL,
                ultima_conexion TEXT
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