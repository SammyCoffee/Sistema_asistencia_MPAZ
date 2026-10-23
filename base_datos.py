import sqlite3
from datetime import datetime
import os
import re

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

def validar_rut_chileno(rut):
    rut_limpio = (
        rut.replace(".", "")
        .replace("-", "")
        .strip()
        .upper()
    )

    if len(rut_limpio) < 2:
        return False

    cuerpo = rut_limpio[:-1]
    dv = rut_limpio[-1]

    if not cuerpo.isdigit():
        return False

    suma = 0
    multiplicador = 2

    for numero in reversed(cuerpo):
        suma += int(numero) * multiplicador
        multiplicador += 1

        if multiplicador > 7:
            multiplicador = 2

    resto = 11 - (suma % 11)

    if resto == 11:
        dv_calculado = "0"
    elif resto == 10:
        dv_calculado = "K"
    else:
        dv_calculado = str(resto)

    return dv == dv_calculado


def validar_nombre_estudiante(nombre):
    nombre = nombre.strip()

    if len(nombre) < 5:
        return False

    if not re.fullmatch(
        r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü' -]+",
        nombre
    ):
        return False

    palabras = nombre.split()

    return len(palabras) >= 2

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

    if not rut or not nombre_completo or not curso:
        return {
            "resultado": "datos_incompletos"
        }

    if curso not in CURSOS_VALIDOS:
        return {
            "resultado": "curso_invalido",
            "mensaje": "El curso seleccionado no es válido"
        }

    if not validar_rut_chileno(rut):
        return {
            "resultado": "rut_invalido",
            "mensaje": "El RUT ingresado no es válido"
        }

    if not validar_nombre_estudiante(nombre_completo):
        return {
            "resultado": "nombre_invalido",
            "mensaje": "Debes ingresar nombre y apellido válidos"
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
    if not validar_rut_chileno(rut):
        return {
            "resultado": "rut_invalido",
            "mensaje": "El RUT ingresado no es válido"
        }

    if not validar_nombre_estudiante(nombre_completo):
        return {
            "resultado": "nombre_invalido",
            "mensaje": "Debes ingresar nombre y apellido válidos"
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
    """
    Reactiva una tarjeta bloqueada si esta asignada
    a un estudiante activo.
    """
    if not isinstance(uid, str):
        return "uid_invalido"

    uid = uid.strip().replace(" ", "").upper()

    if not uid:
        return "uid_invalido"

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT t.id, t.estado, a.estado
            FROM tarjetas AS t
            LEFT JOIN alumnos AS a
                ON a.id = t.alumno_id
            WHERE t.uid = ?
            LIMIT 1
            """,
            (uid,)
        )

        tarjeta = cursor.fetchone()

        if tarjeta is None:
            return "tarjeta_no_existe"

        if tarjeta[1] != "bloqueada":
            return "tarjeta_no_bloqueada"

        if tarjeta[2] != "activo":
            return "alumno_no_autorizado"

        cursor.execute(
            """
            UPDATE tarjetas
            SET estado = 'activa',
                fecha_bloqueo = NULL
            WHERE id = ?
              AND estado = 'bloqueada'
            """,
            (tarjeta[0],)
        )

        if cursor.rowcount != 1:
            conexion.rollback()
            return "no_actualizada"

        conexion.commit()
        return "activada"

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


def registrar_usuario(nombre_completo, usuario, password, rol):
    import sqlite3
    from datetime import datetime
    from werkzeug.security import generate_password_hash

    if not all(isinstance(v, str) for v in
               (nombre_completo, usuario, password, rol)):
        return {"resultado": "datos_invalidos"}

    nombre_completo = nombre_completo.strip()
    usuario = usuario.strip().lower()
    rol = rol.strip().lower()

    if not nombre_completo or not usuario or not password:
        return {"resultado": "datos_incompletos"}

    if rol not in ("administrador", "profesor"):
        return {"resultado": "rol_invalido"}

    if len(password) < 8:
        return {"resultado": "password_demasiado_corto"}

    if len(password) > 15:
        return {"resultado": "password_demasiado_largo"}

    if len(usuario) > 50 or len(nombre_completo) > 150:
        return {"resultado": "datos_invalidos"}

    password_hash = generate_password_hash(password)

    fecha_creacion = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO usuarios (
                nombre_completo,
                usuario,
                password_hash,
                rol,
                estado,
                fecha_creacion
            )
            VALUES (?, ?, ?, ?, 'activo', ?)
            """,
            (
                nombre_completo,
                usuario,
                password_hash,
                rol,
                fecha_creacion
            )
        )

        conexion.commit()

        return {
            "resultado": "usuario_registrado",
            "id": cursor.lastrowid,
            "usuario": usuario,
            "rol": rol
        }

    except sqlite3.IntegrityError:
        conexion.rollback()

        return {
            "resultado": "usuario_duplicado"
        }

    finally:
        conexion.close()



def autenticar_usuario(usuario, password):
    from werkzeug.security import check_password_hash

    if not isinstance(usuario, str) or not isinstance(password, str):
        return {"resultado": "datos_invalidos"}

    usuario = usuario.strip().lower()

    if not usuario or not password:
        return {"resultado": "datos_incompletos"}

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT
                id,
                nombre_completo,
                usuario,
                password_hash,
                rol,
                estado
            FROM usuarios
            WHERE usuario = ?
            LIMIT 1
            """,
            (usuario,)
        )

        fila = cursor.fetchone()

        if not fila:
            return {"resultado": "credenciales_invalidas"}

        if fila[5] != "activo":
            return {"resultado": "usuario_inactivo"}

        if not check_password_hash(fila[3], password):
            return {"resultado": "credenciales_invalidas"}

        return {
            "resultado": "autenticado",
            "id": fila[0],
            "nombre_completo": fila[1],
            "usuario": fila[2],
            "rol": fila[4]
        }

    finally:
        conexion.close()



def asignar_profesor_curso(profesor_id, curso, asignatura_id):
    if not isinstance(profesor_id, int) or isinstance(profesor_id, bool):
        return {"resultado": "profesor_invalido"}

    if not isinstance(asignatura_id, int) or isinstance(asignatura_id, bool):
        return {"resultado": "asignatura_invalida"}

    if not isinstance(curso, str) or not curso.strip():
        return {"resultado": "curso_invalido"}

    curso = curso.strip().upper()

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT rol, estado
            FROM usuarios
            WHERE id = ?
            """,
            (profesor_id,)
        )

        profesor = cursor.fetchone()

        if not profesor or profesor[0] != "profesor":
            return {"resultado": "profesor_no_autorizado"}

        if profesor[1] != "activo":
            return {"resultado": "profesor_inactivo"}

        cursor.execute(
            """
            SELECT estado
            FROM asignaturas
            WHERE id = ?
            """,
            (asignatura_id,)
        )

        asignatura = cursor.fetchone()

        if not asignatura:
            return {"resultado": "asignatura_no_existe"}

        if asignatura[0] != "activo":
            return {"resultado": "asignatura_inactiva"}

        cursor.execute(
            """
            SELECT 1
            FROM alumnos
            WHERE UPPER(TRIM(curso)) = ?
              AND estado = 'activo'
            LIMIT 1
            """,
            (curso,)
        )

        if not cursor.fetchone():
            return {"resultado": "curso_sin_alumnos_activos"}

        cursor.execute(
            """
            SELECT id, estado
            FROM profesores_cursos
            WHERE profesor_id = ?
              AND curso = ?
              AND asignatura_id = ?
            """,
            (profesor_id, curso, asignatura_id)
        )

        existente = cursor.fetchone()

        if existente:
            if existente[1] == "activo":
                return {
                    "resultado": "asignacion_existente",
                    "id": existente[0]
                }

            cursor.execute(
                """
                UPDATE profesores_cursos
                SET estado = 'activo'
                WHERE id = ?
                """,
                (existente[0],)
            )

            conexion.commit()

            return {
                "resultado": "asignacion_reactivada",
                "id": existente[0]
            }

        cursor.execute(
            """
            INSERT INTO profesores_cursos
                (profesor_id, curso, asignatura_id, estado)
            VALUES (?, ?, ?, 'activo')
            """,
            (profesor_id, curso, asignatura_id)
        )

        conexion.commit()

        return {
            "resultado": "asignacion_creada",
            "id": cursor.lastrowid
        }

    finally:
        conexion.close()


def obtener_asignaciones_profesor(profesor_id):
    """
    Obtiene los cursos y asignaturas activos de un profesor.
    """

    if (
        not isinstance(profesor_id, int)
        or isinstance(profesor_id, bool)
        or profesor_id <= 0
    ):
        return {
            "resultado": "profesor_invalido",
            "asignaciones": []
        }

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT rol, estado
            FROM usuarios
            WHERE id = ?
            LIMIT 1
            """,
            (profesor_id,)
        )

        profesor = cursor.fetchone()

        if not profesor or profesor[0] != "profesor":
            return {
                "resultado": "profesor_no_autorizado",
                "asignaciones": []
            }

        if profesor[1] != "activo":
            return {
                "resultado": "profesor_inactivo",
                "asignaciones": []
            }

        cursor.execute(
            """
            SELECT
                pc.id,
                pc.curso,
                a.id,
                a.nombre
            FROM profesores_cursos pc
            INNER JOIN asignaturas a
                ON pc.asignatura_id = a.id
            WHERE pc.profesor_id = ?
              AND pc.estado = 'activo'
              AND a.estado = 'activo'
            ORDER BY pc.curso, a.nombre
            """,
            (profesor_id,)
        )

        asignaciones = []

        for fila in cursor.fetchall():
            asignaciones.append({
                "asignacion_id": fila[0],
                "curso": fila[1],
                "asignatura_id": fila[2],
                "asignatura": fila[3]
            })

        return {
            "resultado": "ok",
            "asignaciones": asignaciones
        }

    finally:
        conexion.close()

def crear_tablas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:


	        # ==========================================
        # USUARIOS DEL SISTEMA
        # ADMINISTRADORES Y PROFESORES
        # ==========================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                nombre_completo TEXT NOT NULL,

                usuario TEXT NOT NULL UNIQUE,

                password_hash TEXT NOT NULL,

                rol TEXT NOT NULL
                    CHECK (rol IN ('administrador', 'profesor')),

                estado TEXT NOT NULL DEFAULT 'activo'
                    CHECK (estado IN ('activo', 'inactivo')),

                fecha_creacion TEXT NOT NULL
            )
            """
        )
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
            CREATE TABLE IF NOT EXISTS asignaturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                estado TEXT NOT NULL DEFAULT 'activo'
                    CHECK (estado IN ('activo', 'inactivo'))
            )
            """
        )


        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS profesores_cursos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profesor_id INTEGER NOT NULL,
                curso TEXT NOT NULL,
                asignatura_id INTEGER NOT NULL,
                estado TEXT NOT NULL DEFAULT 'activo'
                    CHECK (estado IN ('activo', 'inactivo')),

                FOREIGN KEY (profesor_id)
                    REFERENCES usuarios(id),

                FOREIGN KEY (asignatura_id)
                    REFERENCES asignaturas(id),

                UNIQUE (profesor_id, curso, asignatura_id)
            )
            """
        )

        cursor.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS
                indice_alumno_fecha_asistencias
            ON asistencias(alumno_id, fecha)
            """
        )


        # ==========================================
        # SESIONES DE CONFIRMACION DOCENTE
        # ==========================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sesiones_clase (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                asignacion_id INTEGER NOT NULL,

                fecha TEXT NOT NULL,

                hora_inicio TEXT NOT NULL,

                modalidad TEXT NOT NULL DEFAULT 'por_clase'
                    CHECK (modalidad IN ('por_clase', 'diaria')),

                estado TEXT NOT NULL DEFAULT 'borrador'
                    CHECK (estado IN ('borrador', 'confirmada', 'anulada')),

                fecha_creacion TEXT NOT NULL
                    DEFAULT (datetime('now')),

                fecha_confirmacion TEXT,

                FOREIGN KEY (asignacion_id)
                    REFERENCES profesores_cursos(id),

                UNIQUE (
                    asignacion_id,
                    fecha,
                    modalidad,
                    hora_inicio
                )
            )
            """
        )

        # ==========================================
        # ASISTENCIAS CONFIRMADAS POR EL DOCENTE
        # ==========================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS asistencias_clase (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                sesion_clase_id INTEGER NOT NULL,

                alumno_id INTEGER NOT NULL,

                estado TEXT NOT NULL
                    CHECK (
                        estado IN (
                            'presente',
                            'atrasado',
                            'no_presente'
                        )
                    ),

                observacion TEXT,

                fecha_registro TEXT NOT NULL
                    DEFAULT (datetime('now')),

                FOREIGN KEY (sesion_clase_id)
                    REFERENCES sesiones_clase(id),

                FOREIGN KEY (alumno_id)
                    REFERENCES alumnos(id),

                UNIQUE (sesion_clase_id, alumno_id)
            )
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
                indice_sesiones_clase_fecha
            ON sesiones_clase(fecha, estado)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
                indice_asistencias_clase_alumno
            ON asistencias_clase(alumno_id)
            """
        )

        conexion.commit()

        print("Tablas creadas correctamente")
    finally:
        conexion.close()



def crear_sesion_clase_profesor(
    profesor_id,
    asignacion_id,
    fecha,
    hora_inicio
):
    """
    Crea o recupera una sesión de verificación docente.

    La sesión comienza en estado borrador.
    No modifica los registros de asistencia RFID.
    """

    from datetime import date as tipo_fecha
    from datetime import time as tipo_hora
    import sqlite3

    if (
        not isinstance(profesor_id, int)
        or isinstance(profesor_id, bool)
        or profesor_id <= 0
    ):
        return {"resultado": "profesor_invalido"}

    if (
        not isinstance(asignacion_id, int)
        or isinstance(asignacion_id, bool)
        or asignacion_id <= 0
    ):
        return {"resultado": "asignacion_invalida"}

    if not isinstance(fecha, str):
        return {"resultado": "fecha_invalida"}

    try:
        fecha_validada = tipo_fecha.fromisoformat(fecha)

        if fecha_validada.isoformat() != fecha:
            return {"resultado": "fecha_invalida"}

    except ValueError:
        return {"resultado": "fecha_invalida"}

    if not isinstance(hora_inicio, str):
        return {"resultado": "hora_invalida"}

    try:
        hora_validada = tipo_hora.fromisoformat(hora_inicio)

        hora_normalizada = hora_validada.strftime("%H:%M")

        if hora_normalizada != hora_inicio:
            return {"resultado": "hora_invalida"}

    except ValueError:
        return {"resultado": "hora_invalida"}

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT
                pc.id,
                pc.curso,
                a.nombre
            FROM profesores_cursos pc
            INNER JOIN usuarios u
                ON u.id = pc.profesor_id
            INNER JOIN asignaturas a
                ON a.id = pc.asignatura_id
            WHERE pc.id = ?
              AND pc.profesor_id = ?
              AND pc.estado = 'activo'
              AND u.rol = 'profesor'
              AND u.estado = 'activo'
              AND a.estado = 'activo'
            LIMIT 1
            """,
            (asignacion_id, profesor_id)
        )

        asignacion = cursor.fetchone()

        if asignacion is None:
            return {"resultado": "asignacion_no_autorizada"}

        cursor.execute(
            """
            SELECT id, estado
            FROM sesiones_clase
            WHERE asignacion_id = ?
              AND fecha = ?
              AND modalidad = 'por_clase'
              AND hora_inicio = ?
            LIMIT 1
            """,
            (
                asignacion_id,
                fecha,
                hora_inicio
            )
        )

        existente = cursor.fetchone()

        if existente is not None:
            return {
                "resultado": "sesion_existente",
                "sesion_id": existente[0],
                "estado": existente[1]
            }

        try:
            cursor.execute(
                """
                INSERT INTO sesiones_clase (
                    asignacion_id,
                    fecha,
                    hora_inicio,
                    modalidad,
                    estado
                )
                VALUES (?, ?, ?, 'por_clase', 'borrador')
                """,
                (
                    asignacion_id,
                    fecha,
                    hora_inicio
                )
            )

            conexion.commit()

            return {
                "resultado": "sesion_creada",
                "sesion_id": cursor.lastrowid,
                "estado": "borrador",
                "curso": asignacion[1],
                "asignatura": asignacion[2]
            }

        except sqlite3.IntegrityError:
            conexion.rollback()

            cursor.execute(
                """
                SELECT id, estado
                FROM sesiones_clase
                WHERE asignacion_id = ?
                  AND fecha = ?
                  AND modalidad = 'por_clase'
                  AND hora_inicio = ?
                LIMIT 1
                """,
                (
                    asignacion_id,
                    fecha,
                    hora_inicio
                )
            )

            existente = cursor.fetchone()

            if existente is None:
                raise

            return {
                "resultado": "sesion_existente",
                "sesion_id": existente[0],
                "estado": existente[1]
            }

    finally:
        conexion.close()


def registrar_asistencia_clase_profesor(
    profesor_id,
    sesion_id,
    alumno_id,
    estado,
    observacion=None
):
    """
    Registra o actualiza la asistencia de un estudiante
    dentro de una sesión docente en estado borrador.

    No modifica la asistencia registrada por RFID.
    """

    import sqlite3

    for valor, nombre_campo in (
        (profesor_id, "profesor"),
        (sesion_id, "sesion"),
        (alumno_id, "alumno")
    ):
        if (
            not isinstance(valor, int)
            or isinstance(valor, bool)
            or valor <= 0
        ):
            return {
                "resultado": f"{nombre_campo}_invalido"
            }

    estados_permitidos = (
        "presente",
        "atrasado",
        "no_presente"
    )

    if estado not in estados_permitidos:
        return {"resultado": "estado_invalido"}

    if observacion is not None:
        if not isinstance(observacion, str):
            return {"resultado": "observacion_invalida"}

        observacion = observacion.strip()

        if len(observacion) > 500:
            return {"resultado": "observacion_demasiado_larga"}

        if not observacion:
            observacion = None

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        # Bloquear escrituras concurrentes durante la validación.
        cursor.execute("BEGIN IMMEDIATE")

        cursor.execute(
            """
            SELECT
                sc.id,
                sc.estado,
                pc.curso
            FROM sesiones_clase sc
            INNER JOIN profesores_cursos pc
                ON pc.id = sc.asignacion_id
            INNER JOIN usuarios u
                ON u.id = pc.profesor_id
            INNER JOIN asignaturas a
                ON a.id = pc.asignatura_id
            WHERE sc.id = ?
              AND pc.profesor_id = ?
              AND pc.estado = 'activo'
              AND u.rol = 'profesor'
              AND u.estado = 'activo'
              AND a.estado = 'activo'
            LIMIT 1
            """,
            (sesion_id, profesor_id)
        )

        sesion = cursor.fetchone()

        if sesion is None:
            return {"resultado": "sesion_no_autorizada"}

        if sesion[1] != "borrador":
            return {
                "resultado": "sesion_no_editable",
                "estado_sesion": sesion[1]
            }

        curso = sesion[2]

        cursor.execute(
            """
            SELECT id
            FROM alumnos
            WHERE id = ?
              AND curso = ?
              AND estado = 'activo'
            LIMIT 1
            """,
            (alumno_id, curso)
        )

        if cursor.fetchone() is None:
            return {"resultado": "alumno_no_autorizado"}

        cursor.execute(
            """
            INSERT INTO asistencias_clase (
                sesion_clase_id,
                alumno_id,
                estado,
                observacion
            )
            VALUES (?, ?, ?, ?)
            ON CONFLICT(sesion_clase_id, alumno_id)
            DO UPDATE SET
                estado = excluded.estado,
                observacion = excluded.observacion,
                fecha_registro = datetime('now')
            """,
            (
                sesion_id,
                alumno_id,
                estado,
                observacion
            )
        )

        conexion.commit()

        return {
            "resultado": "asistencia_guardada",
            "sesion_id": sesion_id,
            "alumno_id": alumno_id,
            "estado": estado
        }

    except sqlite3.IntegrityError:
        conexion.rollback()
        return {"resultado": "error_integridad"}

    finally:
        conexion.close()


def confirmar_sesion_clase_profesor(profesor_id, sesion_id):
    """
    Confirma una sesión docente cuando todos los estudiantes
    activos del curso tienen un registro de asistencia.

    No modifica los registros de asistencia RFID.
    """

    for valor, campo in (
        (profesor_id, "profesor"),
        (sesion_id, "sesion")
    ):
        if (
            not isinstance(valor, int)
            or isinstance(valor, bool)
            or valor <= 0
        ):
            return {"resultado": f"{campo}_invalido"}

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        # Evita modificaciones concurrentes durante la confirmación.
        cursor.execute("BEGIN IMMEDIATE")

        cursor.execute(
            """
            SELECT
                sc.estado,
                pc.curso
            FROM sesiones_clase sc
            INNER JOIN profesores_cursos pc
                ON pc.id = sc.asignacion_id
            INNER JOIN usuarios u
                ON u.id = pc.profesor_id
            INNER JOIN asignaturas a
                ON a.id = pc.asignatura_id
            WHERE sc.id = ?
              AND pc.profesor_id = ?
              AND pc.estado = 'activo'
              AND u.rol = 'profesor'
              AND u.estado = 'activo'
              AND a.estado = 'activo'
            LIMIT 1
            """,
            (sesion_id, profesor_id)
        )

        sesion = cursor.fetchone()

        if sesion is None:
            return {"resultado": "sesion_no_autorizada"}

        estado_sesion, curso = sesion

        if estado_sesion != "borrador":
            return {
                "resultado": "sesion_no_confirmable",
                "estado_sesion": estado_sesion
            }

        # Contar estudiantes activos del curso.
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM alumnos
            WHERE curso = ?
              AND estado = 'activo'
            """,
            (curso,)
        )

        total_alumnos = cursor.fetchone()[0]

        if total_alumnos == 0:
            return {"resultado": "curso_sin_alumnos"}

        # Contar estudiantes activos con asistencia registrada.
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM asistencias_clase ac
            INNER JOIN alumnos al
                ON al.id = ac.alumno_id
            WHERE ac.sesion_clase_id = ?
              AND al.curso = ?
              AND al.estado = 'activo'
            """,
            (sesion_id, curso)
        )

        total_registrados = cursor.fetchone()[0]

        pendientes = total_alumnos - total_registrados

        if pendientes > 0:
            return {
                "resultado": "asistencia_incompleta",
                "total_alumnos": total_alumnos,
                "registrados": total_registrados,
                "pendientes": pendientes
            }

        # Confirmar definitivamente la sesión.
        cursor.execute(
            """
            UPDATE sesiones_clase
            SET estado = 'confirmada',
                fecha_confirmacion = datetime('now')
            WHERE id = ?
              AND estado = 'borrador'
            """,
            (sesion_id,)
        )

        if cursor.rowcount != 1:
            conexion.rollback()
            return {"resultado": "error_confirmacion"}

        conexion.commit()

        return {
            "resultado": "sesion_confirmada",
            "sesion_id": sesion_id,
            "total_alumnos": total_alumnos,
            "registrados": total_registrados,
            "pendientes": 0
        }

    finally:
        conexion.close()


def obtener_sesiones_clase_profesor(profesor_id, asignacion_id):
    """
    Consulta las sesiones de una asignación autorizada.

    Los estudiantes sin registro se consideran pendientes
    de verificación, nunca ausentes automáticamente.

    No modifica datos RFID ni registros docentes.
    """

    if (
        not isinstance(profesor_id, int)
        or isinstance(profesor_id, bool)
        or profesor_id <= 0
    ):
        return {
            "resultado": "profesor_invalido",
            "sesiones": []
        }

    if (
        not isinstance(asignacion_id, int)
        or isinstance(asignacion_id, bool)
        or asignacion_id <= 0
    ):
        return {
            "resultado": "asignacion_invalida",
            "sesiones": []
        }

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        # Verificar profesor y asignación activa.
        cursor.execute(
            """
            SELECT
                pc.curso,
                a.nombre
            FROM profesores_cursos pc
            INNER JOIN usuarios u
                ON u.id = pc.profesor_id
            INNER JOIN asignaturas a
                ON a.id = pc.asignatura_id
            WHERE pc.id = ?
              AND pc.profesor_id = ?
              AND pc.estado = 'activo'
              AND u.rol = 'profesor'
              AND u.estado = 'activo'
              AND a.estado = 'activo'
            LIMIT 1
            """,
            (asignacion_id, profesor_id)
        )

        asignacion = cursor.fetchone()

        if asignacion is None:
            return {
                "resultado": "asignacion_no_autorizada",
                "sesiones": []
            }

        curso, asignatura = asignacion

        # Contar estudiantes activos del curso.
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM alumnos
            WHERE curso = ?
              AND estado = 'activo'
            """,
            (curso,)
        )

        total_alumnos = cursor.fetchone()[0]

        # Consultar sesiones de la asignación.
        cursor.execute(
            """
            SELECT
                sc.id,
                sc.fecha,
                sc.hora_inicio,
                sc.modalidad,
                sc.estado,
                sc.fecha_creacion,
                sc.fecha_confirmacion,
                (
                    SELECT COUNT(*)
                    FROM asistencias_clase ac
                    INNER JOIN alumnos al
                        ON al.id = ac.alumno_id
                    WHERE ac.sesion_clase_id = sc.id
                      AND al.curso = ?
                      AND al.estado = 'activo'
                ) AS registrados
            FROM sesiones_clase sc
            WHERE sc.asignacion_id = ?
            ORDER BY
                sc.fecha DESC,
                sc.hora_inicio DESC,
                sc.id DESC
            """,
            (curso, asignacion_id)
        )

        sesiones = []

        for fila in cursor.fetchall():
            registrados = fila[7]

            sesiones.append({
                "sesion_id": fila[0],
                "asignacion_id": asignacion_id,
                "curso": curso,
                "asignatura": asignatura,
                "fecha": fila[1],
                "hora_inicio": fila[2],
                "modalidad": fila[3],
                "estado": fila[4],
                "fecha_creacion": fila[5],
                "fecha_confirmacion": fila[6],
                "total_alumnos": total_alumnos,
                "registrados": registrados,
                "pendientes": max(
                    total_alumnos - registrados,
                    0
                )
            })

        return {
            "resultado": "ok",
            "asignacion_id": asignacion_id,
            "curso": curso,
            "asignatura": asignatura,
            "total_sesiones": len(sesiones),
            "sesiones": sesiones
        }

    finally:
        conexion.close()



def obtener_detalle_sesion_clase_profesor(profesor_id, sesion_id):
    """
    Consulta una sesión docente y la asistencia individual.

    Los estudiantes sin registro se muestran como
    'sin_verificar', sin modificar la base de datos.

    No modifica los registros RFID.
    """

    for valor, campo in (
        (profesor_id, "profesor"),
        (sesion_id, "sesion")
    ):
        if (
            not isinstance(valor, int)
            or isinstance(valor, bool)
            or valor <= 0
        ):
            return {
                "resultado": f"{campo}_invalido",
                "alumnos": []
            }

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        # Verificar que la sesión pertenezca al profesor.
        cursor.execute(
            """
            SELECT
                sc.id,
                sc.asignacion_id,
                pc.curso,
                a.nombre,
                sc.fecha,
                sc.hora_inicio,
                sc.modalidad,
                sc.estado,
                sc.fecha_creacion,
                sc.fecha_confirmacion
            FROM sesiones_clase sc
            INNER JOIN profesores_cursos pc
                ON pc.id = sc.asignacion_id
            INNER JOIN usuarios u
                ON u.id = pc.profesor_id
            INNER JOIN asignaturas a
                ON a.id = pc.asignatura_id
            WHERE sc.id = ?
              AND pc.profesor_id = ?
              AND pc.estado = 'activo'
              AND u.rol = 'profesor'
              AND u.estado = 'activo'
              AND a.estado = 'activo'
            LIMIT 1
            """,
            (sesion_id, profesor_id)
        )

        sesion = cursor.fetchone()

        if sesion is None:
            return {
                "resultado": "sesion_no_autorizada",
                "alumnos": []
            }

        curso = sesion[2]

        # LEFT JOIN conserva estudiantes sin asistencia.
        cursor.execute(
            """
            SELECT
                al.id,
                al.nombre_completo,
                al.curso,
                ac.estado,
                ac.observacion,
                ac.fecha_registro
            FROM alumnos al
            LEFT JOIN asistencias_clase ac
                ON ac.alumno_id = al.id
               AND ac.sesion_clase_id = ?
            WHERE al.curso = ?
              AND al.estado = 'activo'
            ORDER BY
                al.nombre_completo ASC,
                al.id ASC
            """,
            (sesion_id, curso)
        )

        alumnos = []

        for fila in cursor.fetchall():
            estado = (
                fila[3]
                if fila[3] is not None
                else "sin_verificar"
            )

            alumnos.append({
                "alumno_id": fila[0],
                "nombre": fila[1],
                "curso": fila[2],
                "estado": estado,
                "observacion": fila[4],
                "fecha_registro": fila[5]
            })

        registrados = sum(
            alumno["estado"] != "sin_verificar"
            for alumno in alumnos
        )

        total_alumnos = len(alumnos)

        return {
            "resultado": "ok",
            "sesion": {
                "sesion_id": sesion[0],
                "asignacion_id": sesion[1],
                "curso": sesion[2],
                "asignatura": sesion[3],
                "fecha": sesion[4],
                "hora_inicio": sesion[5],
                "modalidad": sesion[6],
                "estado": sesion[7],
                "fecha_creacion": sesion[8],
                "fecha_confirmacion": sesion[9],
                "total_alumnos": total_alumnos,
                "registrados": registrados,
                "pendientes": total_alumnos - registrados
            },
            "alumnos": alumnos
        }

    finally:
        conexion.close()


def obtener_alumnos_curso_profesor(profesor_id, curso):
    """
    Obtiene los estudiantes activos de un curso
    únicamente si el profesor tiene autorización.
    """

    if (
        not isinstance(profesor_id, int)
        or isinstance(profesor_id, bool)
        or profesor_id <= 0
    ):
        return {
            "resultado": "profesor_invalido",
            "alumnos": []
        }

    if not isinstance(curso, str) or not curso.strip():
        return {
            "resultado": "curso_invalido",
            "alumnos": []
        }

    curso = curso.strip().upper()

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        # Verificar que el profesor exista y esté activo.
        cursor.execute(
            """
            SELECT id
            FROM usuarios
            WHERE id = ?
              AND rol = 'profesor'
              AND estado = 'activo'
            LIMIT 1
            """,
            (profesor_id,)
        )

        if cursor.fetchone() is None:
            return {
                "resultado": "profesor_no_autorizado",
                "alumnos": []
            }

        # Comprobar que tenga asignado el curso.
        cursor.execute(
            """
            SELECT 1
            FROM profesores_cursos pc
            INNER JOIN asignaturas a
                ON a.id = pc.asignatura_id
            WHERE pc.profesor_id = ?
              AND pc.curso = ?
              AND pc.estado = 'activo'
              AND a.estado = 'activo'
            LIMIT 1
            """,
            (profesor_id, curso)
        )

        if cursor.fetchone() is None:
            return {
                "resultado": "curso_no_autorizado",
                "alumnos": []
            }

        # Consultar solamente los estudiantes activos.
        cursor.execute(
            """
            SELECT
                id,
                nombre_completo,
                curso
            FROM alumnos
            WHERE curso = ?
              AND estado = 'activo'
            ORDER BY nombre_completo ASC
            """,
            (curso,)
        )

        alumnos = [
            {
                "id": fila[0],
                "nombre": fila[1],
                "curso": fila[2]
            }
            for fila in cursor.fetchall()
        ]

        return {
            "resultado": "ok",
            "curso": curso,
            "total": len(alumnos),
            "alumnos": alumnos
        }

    finally:
        conexion.close()


if __name__ == "__main__":
    crear_tablas()


def obtener_asistencia_curso_profesor(profesor_id, curso, fecha):
    """
    Consulta la asistencia RFID de un curso en una fecha,
    verificando previamente los permisos del profesor.
    """
    from datetime import date as tipo_fecha

    if (
        not isinstance(profesor_id, int)
        or isinstance(profesor_id, bool)
        or profesor_id <= 0
    ):
        return {
            "resultado": "profesor_invalido",
            "estudiantes": []
        }

    if not isinstance(curso, str) or not curso.strip():
        return {
            "resultado": "curso_invalido",
            "estudiantes": []
        }

    curso = curso.strip().upper()

    if len(curso) > 20:
        return {
            "resultado": "curso_invalido",
            "estudiantes": []
        }

    if not isinstance(fecha, str):
        return {
            "resultado": "fecha_invalida",
            "estudiantes": []
        }

    try:
        fecha_validada = tipo_fecha.fromisoformat(fecha)

        if fecha_validada.isoformat() != fecha:
            raise ValueError("Formato de fecha incorrecto")

    except ValueError:
        return {
            "resultado": "fecha_invalida",
            "estudiantes": []
        }

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT id
            FROM usuarios
            WHERE id = ?
              AND rol = 'profesor'
              AND estado = 'activo'
            LIMIT 1
            """,
            (profesor_id,)
        )

        if cursor.fetchone() is None:
            return {
                "resultado": "profesor_no_autorizado",
                "estudiantes": []
            }

        cursor.execute(
            """
            SELECT 1
            FROM profesores_cursos pc
            INNER JOIN asignaturas a
                ON a.id = pc.asignatura_id
            WHERE pc.profesor_id = ?
              AND pc.curso = ?
              AND pc.estado = 'activo'
              AND a.estado = 'activo'
            LIMIT 1
            """,
            (profesor_id, curso)
        )

        if cursor.fetchone() is None:
            return {
                "resultado": "curso_no_autorizado",
                "estudiantes": []
            }

        cursor.execute(
            """
            SELECT
                al.id,
                al.nombre_completo,
                COALESCE(
                    (
                        SELECT MIN(
                            COALESCE(a.hora_entrada, a.hora)
                        )
                        FROM asistencias a
                        WHERE a.alumno_id = al.id
                          AND a.fecha = ?
                    ),
                    NULL
                ) AS hora_entrada,
                (
                    SELECT MAX(a.hora_salida)
                    FROM asistencias a
                    WHERE a.alumno_id = al.id
                      AND a.fecha = ?
                ) AS hora_salida
            FROM alumnos al
            WHERE al.curso = ?
              AND al.estado = 'activo'
            ORDER BY al.nombre_completo ASC, al.id ASC
            """,
            (fecha, fecha, curso)
        )

        estudiantes = []

        for fila in cursor.fetchall():
            hora_entrada = fila[2]
            hora_salida = fila[3]

            estudiantes.append({
                "id": fila[0],
                "nombre": fila[1],
                "hora_entrada": hora_entrada,
                "hora_salida": hora_salida,
                "estado": (
                    "ingreso_registrado"
                    if hora_entrada is not None
                    else "sin_registro"
                )
            })

        ingresos = sum(
            estudiante["estado"] == "ingreso_registrado"
            for estudiante in estudiantes
        )

        return {
            "resultado": "ok",
            "curso": curso,
            "fecha": fecha,
            "total_estudiantes": len(estudiantes),
            "ingresos_registrados": ingresos,
            "sin_registro": len(estudiantes) - ingresos,
            "estudiantes": estudiantes
        }

    finally:
        conexion.close()
