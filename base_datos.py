import sqlite3
from datetime import datetime
import os

CURSOS_VALIDOS = {
    "PK",
    "K",
    "1A",
    "1B",
    "2A",
    "2B",
    "3A",
    "3B",
    "4A",
    "4B",
    "5A",
    "5B",
    "6A",
    "6B",
    "7A",
    "7B",
    "8A",
    "8B",
}

RUTA_BASE_DATOS = os.getenv(
    "MPAZ_DB_PATH",
    "data/asistencia.db"
)


def obtener_conexion():
    conexion = sqlite3.connect(RUTA_BASE_DATOS)
    conexion.execute("PRAGMA foreign_keys = ON")

    return conexion

def guardar_alumno(
    rut,
    nombre_completo,
    curso,
    uid
):
    rut = rut.strip()
    nombre_completo = nombre_completo.strip()
    curso = curso.strip().upper()
    uid = uid.strip().replace(" ", "").upper()

    fecha_actual = datetime.now().strftime(
        "%Y-%m-%d"
    )

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO alumnos (
                rut,
                nombre_completo,
                curso,
                estado
            )
            VALUES (?, ?, ?, 'activo')
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
                fecha_registro,
                fecha_asignacion
            )
            VALUES (?, ?, 'activa', ?, ?)
            """,
            (
                alumno_id,
                uid,
                fecha_actual,
                fecha_actual
            )
        )

        conexion.commit()

        return True

    except sqlite3.IntegrityError:
        conexion.rollback()

        return False

    finally:
        conexion.close()


def registrar_alumno(
    rut,
    nombre_completo,
    curso
):
    rut = rut.strip()
    nombre_completo = nombre_completo.strip()
    curso = curso.strip().upper()

    if curso not in CURSOS_VALIDOS:
        return {
            "resultado": "curso_invalido",
            "mensaje": "El curso seleccionado no es válido"
        }
    
    if not rut or not nombre_completo or not curso:
        return {
            "resultado": "datos_incompletos"
        }

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO alumnos (
                rut,
                nombre_completo,
                curso,
                estado
            )
            VALUES (?, ?, ?, 'activo')
            """,
            (
                rut,
                nombre_completo,
                curso
            )
        )

        alumno_id = cursor.lastrowid

        conexion.commit()

        return {
            "resultado": "registrado",
            "id": alumno_id,
            "rut": rut,
            "nombre": nombre_completo,
            "curso": curso,
            "estado": "activo"
        }

    except sqlite3.IntegrityError:
        conexion.rollback()

        return {
            "resultado": "rut_repetido"
        }

    finally:
        conexion.close()


def editar_alumno(
    alumno_id,
    rut,
    nombre_completo,
    curso
):
    rut = rut.strip()
    nombre_completo = nombre_completo.strip()
    curso = curso.strip().upper()
    
    if curso not in CURSOS_VALIDOS:
        return {
            "resultado": "curso_invalido",
            "mensaje": "El curso seleccionado no es válido"
        }
    

    if not rut or not nombre_completo or not curso:
        return {
            "resultado": "datos_incompletos"
        }

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT id
            FROM alumnos
            WHERE id = ?
            LIMIT 1
            """,
            (alumno_id,)
        )

        alumno = cursor.fetchone()

        if not alumno:
            return {
                "resultado": "alumno_no_existe"
            }

        try:
            cursor.execute(
                """
                UPDATE alumnos
                SET
                    rut = ?,
                    nombre_completo = ?,
                    curso = ?
                WHERE id = ?
                """,
                (
                    rut,
                    nombre_completo,
                    curso,
                    alumno_id
                )
            )

        except sqlite3.IntegrityError:
            return {
                "resultado": "rut_repetido"
            }

        conexion.commit()

        return {
            "resultado": "actualizado",
            "id": alumno_id,
            "rut": rut,
            "nombre": nombre_completo,
            "curso": curso
        }

    finally:
        conexion.close()

def cambiar_estado_alumno(
    alumno_id,
    nuevo_estado
):
    nuevo_estado = nuevo_estado.strip().lower()

    if nuevo_estado not in (
        "activo",
        "inactivo"
    ):
        return {
            "resultado": "estado_invalido"
        }

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT
                id,
                nombre_completo
            FROM alumnos
            WHERE id = ?
            LIMIT 1
            """,
            (alumno_id,)
        )

        alumno = cursor.fetchone()

        if not alumno:
            return {
                "resultado": "alumno_no_existe"
            }

        if nuevo_estado == "inactivo":
            fecha_baja = datetime.now().strftime(
                "%Y-%m-%d"
            )
        else:
            fecha_baja = None

        cursor.execute(
            """
            UPDATE alumnos
            SET
                estado = ?,
                fecha_baja = ?
            WHERE id = ?
            """,
            (
                nuevo_estado,
                fecha_baja,
                alumno_id
            )
        )

        conexion.commit()

        return {
            "resultado": "actualizado",
            "id": alumno_id,
            "nombre": alumno[1],
            "estado": nuevo_estado,
            "fecha_baja": fecha_baja
        }

    finally:
        conexion.close()
def obtener_tarjetas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT
                tarjetas.id,
                tarjetas.uid,
                tarjetas.estado,
                tarjetas.fecha_registro,
                tarjetas.fecha_asignacion,
                tarjetas.fecha_bloqueo,
                tarjetas.fecha_extravio,
                alumnos.id,
                alumnos.nombre_completo,
                alumnos.curso
            FROM tarjetas

            LEFT JOIN alumnos
                ON tarjetas.alumno_id = alumnos.id

            ORDER BY
                CASE tarjetas.estado
                    WHEN 'activa' THEN 1
                    WHEN 'disponible' THEN 2
                    WHEN 'bloqueada' THEN 3
                    WHEN 'extraviada' THEN 4
                    ELSE 5
                END,
                tarjetas.id ASC
            """
        )

        filas = cursor.fetchall()

        tarjetas = []

        for fila in filas:
            tarjetas.append(
                {
                    "id": fila[0],
                    "uid": fila[1],
                    "estado": fila[2],
                    "fecha_registro": fila[3],
                    "fecha_asignacion": fila[4],
                    "fecha_bloqueo": fila[5],
                    "fecha_extravio": fila[6],
                    "alumno_id": fila[7],
                    "alumno": fila[8],
                    "curso": fila[9]
                }
            )

        return tarjetas

    finally:
        conexion.close()
def registrar_tarjeta(
    uid
):
    uid = uid.strip().replace(" ", "").upper()

    if not uid:
        return {
            "resultado": "datos_incompletos"
        }

    fecha_registro = datetime.now().strftime(
        "%Y-%m-%d"
    )

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO tarjetas (
                alumno_id,
                uid,
                estado,
                fecha_registro,
                fecha_asignacion,
                fecha_bloqueo,
                fecha_extravio
            )
            VALUES (
                NULL,
                ?,
                'disponible',
                ?,
                NULL,
                NULL,
                NULL
            )
            """,
            (
                uid,
                fecha_registro
            )
        )

        tarjeta_id = cursor.lastrowid

        conexion.commit()

        return {
            "resultado": "registrada",
            "id": tarjeta_id,
            "uid": uid,
            "estado": "disponible",
            "fecha_registro": fecha_registro
        }

    except sqlite3.IntegrityError:
        conexion.rollback()

        return {
            "resultado": "uid_repetido"
        }

    finally:
        conexion.close()

def vincular_tarjeta(
    alumno_id,
    uid
):
    uid = uid.strip().replace(" ", "").upper()

    fecha_asignacion = datetime.now().strftime(
        "%Y-%m-%d"
    )

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        # ==========================================
        # 1. COMPROBAR QUE EL ALUMNO EXISTA
        # ==========================================

        cursor.execute(
            """
            SELECT
                id,
                nombre_completo,
                curso,
                estado
            FROM alumnos
            WHERE id = ?
            LIMIT 1
            """,
            (alumno_id,)
        )

        alumno = cursor.fetchone()

        if not alumno:
            return {
                "resultado": "alumno_no_existe"
            }

        # ==========================================
        # 2. EL ALUMNO DEBE ESTAR ACTIVO
        # ==========================================

        if alumno[3] != "activo":
            return {
                "resultado": "alumno_inactivo"
            }

        # ==========================================
        # 3. VERIFICAR QUE NO TENGA TARJETA ACTIVA
        # ==========================================

        cursor.execute(
            """
            SELECT uid
            FROM tarjetas
            WHERE alumno_id = ?
              AND estado = 'activa'
            LIMIT 1
            """,
            (alumno_id,)
        )

        tarjeta_actual = cursor.fetchone()

        if tarjeta_actual:
            return {
                "resultado": "ya_tiene_tarjeta",
                "uid": tarjeta_actual[0]
            }

        # ==========================================
        # 4. BUSCAR LA TARJETA
        # ==========================================

        cursor.execute(
            """
            SELECT
                id,
                estado,
                alumno_id
            FROM tarjetas
            WHERE uid = ?
            LIMIT 1
            """,
            (uid,)
        )

        tarjeta = cursor.fetchone()

        if not tarjeta:
            return {
                "resultado": "tarjeta_no_existe"
            }

        # ==========================================
        # 5. DEBE ESTAR DISPONIBLE
        # ==========================================

        if tarjeta[1] != "disponible":
            return {
                "resultado": "tarjeta_no_disponible",
                "estado": tarjeta[1]
            }

        # ==========================================
        # 6. VINCULAR
        # ==========================================

        cursor.execute(
            """
            UPDATE tarjetas
            SET
                alumno_id = ?,
                estado = 'activa',
                fecha_asignacion = ?,
                fecha_bloqueo = NULL,
                fecha_extravio = NULL
            WHERE id = ?
            """,
            (
                alumno_id,
                fecha_asignacion,
                tarjeta[0]
            )
        )

        conexion.commit()

        return {
            "resultado": "vinculada",
            "alumno_id": alumno_id,
            "alumno": alumno[1],
            "curso": alumno[2],
            "uid": uid,
            "estado": "activa",
            "fecha_asignacion": fecha_asignacion
        }

    finally:
        conexion.close()
def marcar_tarjeta_extraviada(
    uid
):
    uid = uid.strip().replace(" ", "").upper()

    fecha_extravio = datetime.now().strftime(
        "%Y-%m-%d"
    )

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT
                id,
                alumno_id,
                estado
            FROM tarjetas
            WHERE uid = ?
            LIMIT 1
            """,
            (uid,)
        )

        tarjeta = cursor.fetchone()

        if not tarjeta:
            return {
                "resultado": "tarjeta_no_existe"
            }

        if tarjeta[2] == "extraviada":
            return {
                "resultado": "ya_extraviada"
            }

        cursor.execute(
            """
            UPDATE tarjetas
            SET
                estado = 'extraviada',
                fecha_extravio = ?
            WHERE id = ?
            """,
            (
                fecha_extravio,
                tarjeta[0]
            )
        )

        conexion.commit()

        return {
            "resultado": "extraviada",
            "id": tarjeta[0],
            "alumno_id": tarjeta[1],
            "uid": uid,
            "estado": "extraviada",
            "fecha_extravio": fecha_extravio
        }

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
                tarjetas.estado,
                alumnos.estado
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
                curso TEXT NOT NULL,
                estado TEXT NOT NULL DEFAULT 'activo',
                fecha_baja TEXT
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tarjetas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                alumno_id INTEGER,

                uid TEXT NOT NULL UNIQUE,

                estado TEXT NOT NULL
                DEFAULT 'disponible',

                fecha_registro TEXT NOT NULL,

                fecha_asignacion TEXT,

                fecha_bloqueo TEXT,

                fecha_extravio TEXT,

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
