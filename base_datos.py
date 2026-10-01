import sqlite3
from datetime import datetime
import os

RUTA_BASE_DATOS = os.getenv(
    "MPAZ_DB_PATH",
    "data/asistencia.db"
)


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

def activar_tarjeta(uid):
    uid = uid.strip().replace(" ", "").upper()

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            UPDATE tarjetas
            SET estado = 'activa',
                fecha_bloqueo = NULL
            WHERE uid = ?
                AND estado = 'bloqueada'
            """,
            (uid,)
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

def guardar_asistencia(
    alumno_id,
    fecha,
    hora,
    totem_id=None,
    evento_id=None
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        # Evita que dos procesos modifiquen la misma
        # jornada al mismo tiempo.
        conexion.execute("BEGIN IMMEDIATE")

        # ==========================================
        # 1. COMPROBAR EVENTO REPETIDO
        # ==========================================

        if evento_id:
            cursor.execute(
                """
                SELECT id
                FROM asistencias
                WHERE evento_id = ?
                   OR evento_entrada_id = ?
                   OR evento_salida_id = ?
                LIMIT 1
                """,
                (
                    evento_id,
                    evento_id,
                    evento_id
                )
            )

            if cursor.fetchone():
                conexion.rollback()
                return "evento_repetido"

        # ==========================================
        # 2. BUSCAR JORNADA DEL ALUMNO HOY
        # ==========================================

        cursor.execute(
            """
            SELECT
                id,
                hora_entrada,
                hora_salida
            FROM asistencias
            WHERE alumno_id = ?
              AND fecha = ?
            LIMIT 1
            """,
            (
                alumno_id,
                fecha
            )
        )

        jornada = cursor.fetchone()

        # ==========================================
        # 3. NO EXISTE JORNADA:
        #    PRIMERA LECTURA = ENTRADA
        # ==========================================

        if not jornada:
            cursor.execute(
                """
                INSERT INTO asistencias (
                    alumno_id,
                    fecha,
                    hora,
                    totem_id,
                    evento_id,
                    hora_entrada,
                    hora_salida,
                    tipo_salida,
                    totem_entrada_id,
                    totem_salida_id,
                    evento_entrada_id,
                    evento_salida_id
                )
                VALUES (
                    ?, ?, ?, ?, ?,
                    ?, NULL, NULL,
                    ?, NULL,
                    ?, NULL
                )
                """,
                (
                    alumno_id,
                    fecha,
                    hora,
                    totem_id,
                    evento_id,
                    hora,
                    totem_id,
                    evento_id
                )
            )

            conexion.commit()

            return "entrada_registrada"

        jornada_id = jornada[0]
        hora_entrada = jornada[1]
        hora_salida = jornada[2]

        # ==========================================
        # 4. LA JORNADA YA TIENE SALIDA
        # ==========================================

        if hora_salida:
            conexion.rollback()
            return "jornada_completa"

        # ==========================================
        # 5. EVITAR DOBLE LECTURA ACCIDENTAL
        # ==========================================

        momento_entrada = datetime.strptime(
            f"{fecha} {hora_entrada}",
            "%Y-%m-%d %H:%M:%S"
        )

        momento_actual = datetime.strptime(
            f"{fecha} {hora}",
            "%Y-%m-%d %H:%M:%S"
        )

        segundos_transcurridos = (
            momento_actual - momento_entrada
        ).total_seconds()

        if segundos_transcurridos < 30:
            conexion.rollback()
            return "lectura_repetida"

        # ==========================================
        # 6. SEGUNDA LECTURA = SALIDA
        # ==========================================

        cursor.execute(
            """
            UPDATE asistencias
            SET
                hora_salida = ?,
                tipo_salida = 'totem',
                totem_salida_id = ?,
                evento_salida_id = ?
            WHERE id = ?
            """,
            (
                hora,
                totem_id,
                evento_id,
                jornada_id
            )
        )

        conexion.commit()

        return "salida_registrada"

    except Exception:
        conexion.rollback()
        raise

    finally:
        conexion.close()


def cerrar_jornadas_pendientes():
    momento_actual = datetime.now()

    fecha_hoy = momento_actual.strftime("%Y-%m-%d")
    hora_actual = momento_actual.strftime("%H:%M:%S")

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        conexion.execute("BEGIN IMMEDIATE")

        # ==========================================
        # 1. CERRAR JORNADAS DE DIAS ANTERIORES
        # ==========================================

        cursor.execute(
            """
            UPDATE asistencias
            SET
                hora_salida = '17:00:00',
                tipo_salida = 'automatica'
            WHERE fecha < ?
              AND hora_entrada IS NOT NULL
              AND hora_salida IS NULL
            """,
            (fecha_hoy,)
        )

        jornadas_anteriores = cursor.rowcount

        jornadas_hoy = 0

        # ==========================================
        # 2. SI YA SON LAS 17:00,
        #    CERRAR JORNADAS DEL DIA ACTUAL
        # ==========================================

        if hora_actual >= "17:00:00":

            cursor.execute(
                """
                UPDATE asistencias
                SET
                    hora_salida = '17:00:00',
                    tipo_salida = 'automatica'
                WHERE fecha = ?
                  AND hora_entrada IS NOT NULL
                  AND hora_salida IS NULL
                """,
                (fecha_hoy,)
            )

            jornadas_hoy = cursor.rowcount

        conexion.commit()

        return {
            "resultado": "ok",
            "fecha": fecha_hoy,
            "jornadas_anteriores": jornadas_anteriores,
            "jornadas_hoy": jornadas_hoy
        }

    except Exception:
        conexion.rollback()
        raise

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
        conexion.close()

def cambiar_estado_totem(codigo, nuevo_estado):
    codigo = codigo.strip().upper()
    nuevo_estado = nuevo_estado.strip().lower()

    if nuevo_estado not in ("activo", "inactivo"):
        return {
            "resultado": "estado_invalido"
        }

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT id
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

        cursor.execute(
            """
            UPDATE totems
            SET estado = ?
            WHERE id = ?
            """,
            (
                nuevo_estado,
                totem[0]
            )
        )

        conexion.commit()

        return {
            "resultado": "actualizado",
            "codigo": codigo,
            "estado": nuevo_estado
        }

    finally:
        conexion.close()



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


def obtener_totems():

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
                estado,
                fecha_registro,
                ultima_conexion
            FROM totems
            ORDER BY id ASC
            """
        )

        filas = cursor.fetchall()

        totems = []

        for fila in filas:
            totems.append(
                {
                    "id": fila[0],
                    "codigo": fila[1],
                    "nombre": fila[2],
                    "ubicacion": fila[3],
                    "estado": fila[4],
                    "fecha_registro": fila[5],
                    "ultima_conexion": fila[6]
                }
            )

        return totems

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
                totem_id INTEGER,
                evento_id TEXT,

                hora_entrada TEXT,
                hora_salida TEXT,
                tipo_salida TEXT,

                totem_entrada_id INTEGER,
                totem_salida_id INTEGER,

                evento_entrada_id TEXT,
                evento_salida_id TEXT,

                FOREIGN KEY (alumno_id)
                    REFERENCES alumnos(id),

                FOREIGN KEY (totem_id)
                    REFERENCES totems(id),

                FOREIGN KEY (totem_entrada_id)
                    REFERENCES totems(id),

                FOREIGN KEY (totem_salida_id)
                    REFERENCES totems(id)
            )
            """
        )

        cursor.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS
                indice_evento_id_asistencias
            ON asistencias(evento_id)
            """
        )

        cursor.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS
                indice_evento_entrada_asistencias
            ON asistencias(evento_entrada_id)
            """
        )

        cursor.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS
                indice_evento_salida_asistencias
            ON asistencias(evento_salida_id)
            """
        )

        cursor.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS
                indice_alumno_fecha_asistencias
            ON asistencias(alumno_id, fecha)
            """
        )

        conexion.commit()

        print("Tablas creadas correctamente")
    finally:
        conexion.close()
if __name__ == "__main__":
    crear_tablas()
