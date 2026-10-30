
"""Operaciones internas de seguimiento administrativo MPAZ RFID.

IMPORTANTE: Estas funciones no autentican usuarios por si solas.
La API debe comprobar sesion, rol y CSRF antes de invocarlas.
"""

from base_datos import obtener_conexion


ESTADOS = {"pendiente", "en_gestion", "resuelto"}
CANALES = {"telefonico", "presencial", "otro"}


def _id_valido(valor):
    return type(valor) is int and valor > 0


# MPAZ-AUTORES-758
def _rol_operador(con, operador_id):
    if not _id_valido(operador_id) or isinstance(operador_id, bool):
        return None

    fila = con.execute("""
        SELECT rol FROM seguimiento_operadores
        WHERE id = ? AND estado = 'activo'
        LIMIT 1
    """, (operador_id,)).fetchone()

    return fila[0] if fila else None


def _caso(con, caso_id):
    return con.execute("""
        SELECT id, estado, creado_por_rol, creado_por_usuario_id
        FROM seguimiento_casos
        WHERE id = ?
    """, (caso_id,)).fetchone()


def _avisar_docente(con, caso):
    if caso[2] == "docente" and caso[3] is not None:
        con.execute("""
            INSERT INTO seguimiento_avisos (
                caso_id, destinatario_rol, destinatario_usuario_id
            )
            VALUES (?, 'docente', ?)
        """, (caso[0], caso[3]))


def listar_casos_administracion(estado=None):
    """Lista interna de casos; requiere autorización en la API."""

    if estado is not None and estado not in ESTADOS:
        return {"resultado": "estado_invalido", "casos": []}

    con = obtener_conexion()

    try:
        filas = con.execute("""
            SELECT
                c.id, c.alumno_id, a.nombre_completo,
                c.curso, c.fecha_evento, c.tipo,
                c.estado, c.descripcion, c.creado_en
            FROM seguimiento_casos c
            JOIN alumnos a ON a.id = c.alumno_id
            WHERE (? IS NULL OR c.estado = ?)
            ORDER BY c.creado_en DESC, c.id DESC
            LIMIT 100
        """, (estado, estado)).fetchall()

        casos = [
            {
                "id": f[0],
                "alumno_id": f[1],
                "alumno": f[2],
                "curso": f[3],
                "fecha_evento": f[4],
                "tipo": f[5],
                "estado": f[6],
                "descripcion": f[7],
                "creado_en": f[8]
            }
            for f in filas
        ]

        return {"resultado": "ok", "casos": casos}

    finally:
        con.close()


def responder_caso_administracion(caso_id, mensaje, *, operador_id):
    """Añade una respuesta y notifica al docente creador."""

    if not _id_valido(caso_id):
        return {"resultado": "datos_invalidos"}

    if not isinstance(mensaje, str):
        return {"resultado": "mensaje_invalido"}

    mensaje = mensaje.strip()

    if not 1 <= len(mensaje) <= 1000:
        return {"resultado": "mensaje_invalido"}

    con = obtener_conexion()

    try:
        con.execute("BEGIN IMMEDIATE")
        rol = _rol_operador(con, operador_id)

        if rol not in ("administracion", "direccion"):
            return {"resultado": "operador_no_autorizado"}

        caso = _caso(con, caso_id)

        if caso is None:
            return {"resultado": "caso_no_existe"}

        if caso[1] == "resuelto":
            return {"resultado": "caso_resuelto"}

        cursor = con.execute("""
            INSERT INTO seguimiento_mensajes (
                caso_id, autor_rol, autor_operador_id, mensaje
            )
            VALUES (?, ?, ?, ?)
        """, (caso_id, rol, operador_id, mensaje))

        _avisar_docente(con, caso)
        con.commit()

        return {
            "resultado": "mensaje_registrado",
            "mensaje_id": cursor.lastrowid,
            "caso_id": caso_id
        }

    finally:
        con.close()


def registrar_contacto_administracion(
    caso_id, canal, resultado, observacion=None, *, operador_id
):
    """Registra una gestión con apoderado sin justificar ausencias."""

    if not _id_valido(caso_id):
        return {"resultado": "datos_invalidos"}

    if canal not in CANALES:
        return {"resultado": "canal_invalido"}

    if not isinstance(resultado, str):
        return {"resultado": "resultado_invalido"}

    resultado = resultado.strip()

    if not 1 <= len(resultado) <= 400:
        return {"resultado": "resultado_invalido"}

    if observacion is not None:
        if not isinstance(observacion, str):
            return {"resultado": "observacion_invalida"}

        observacion = observacion.strip() or None

        if observacion is not None and len(observacion) > 500:
            return {"resultado": "observacion_invalida"}

    con = obtener_conexion()

    try:
        con.execute("BEGIN IMMEDIATE")

        if _rol_operador(con, operador_id) != "administracion":
            return {"resultado": "operador_no_autorizado"}

        caso = _caso(con, caso_id)

        if caso is None:
            return {"resultado": "caso_no_existe"}

        if caso[1] == "resuelto":
            return {"resultado": "caso_resuelto"}

        cursor = con.execute("""
            INSERT INTO seguimiento_contactos (
                caso_id, canal, resultado, observacion,
                registrado_por_operador_id
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            caso_id, canal, resultado, observacion, operador_id
        ))

        _avisar_docente(con, caso)
        con.commit()

        return {
            "resultado": "contacto_registrado",
            "contacto_id": cursor.lastrowid
        }

    finally:
        con.close()


def cambiar_estado_caso_administracion(caso_id, estado, *, operador_id):
    """Actualiza el estado del seguimiento, no la asistencia."""

    if not _id_valido(caso_id):
        return {"resultado": "datos_invalidos"}

    if estado not in ESTADOS:
        return {"resultado": "estado_invalido"}

    con = obtener_conexion()

    try:
        con.execute("BEGIN IMMEDIATE")
        rol = _rol_operador(con, operador_id)

        if rol not in ("administracion", "direccion"):
            return {"resultado": "operador_no_autorizado"}

        caso = _caso(con, caso_id)

        if caso is None:
            return {"resultado": "caso_no_existe"}

        if caso[1] == estado:
            return {"resultado": "sin_cambios", "estado": estado}

        con.execute("""
            UPDATE seguimiento_casos
            SET estado = ?,
                actualizado_en = datetime('now'),
                resuelto_en = CASE
                    WHEN ? = 'resuelto' THEN datetime('now')
                    ELSE NULL
                END
            WHERE id = ?
        """, (estado, estado, caso_id))

        con.execute("""
            INSERT INTO seguimiento_mensajes (
                caso_id, autor_rol, autor_operador_id, mensaje
            )
            VALUES (?, ?, ?, ?)
        """, (
            caso_id, rol, operador_id,
            f"Estado cambiado: {caso[1]} -> {estado}"
        ))

        _avisar_docente(con, caso)
        con.commit()

        return {
            "resultado": "estado_actualizado",
            "estado": estado
        }

    finally:
        con.close()


def consultar_historial_docente(profesor_id, caso_id):
    """Solo permite consultar casos de cursos asignados al docente."""

    if not _id_valido(profesor_id) or not _id_valido(caso_id):
        return {"resultado": "datos_invalidos"}

    con = obtener_conexion()

    try:
        caso = con.execute("""
            SELECT c.id, c.estado
            FROM seguimiento_casos c
            WHERE c.id = ?
              AND EXISTS (
                  SELECT 1
                  FROM profesores_cursos pc
                  JOIN usuarios u ON u.id = pc.profesor_id
                  WHERE pc.curso = c.curso
                    AND pc.profesor_id = ?
                    AND pc.estado = 'activo'
                    AND u.rol = 'profesor'
                    AND u.estado = 'activo'
              )
        """, (caso_id, profesor_id)).fetchone()

        if caso is None:
            return {"resultado": "no_autorizado"}

        mensajes = [
            {
                "id": f[0],
                "autor_rol": f[1],
                "mensaje": f[2],
                "fecha": f[3]
            }
            for f in con.execute("""
                SELECT id, autor_rol, mensaje, creado_en
                FROM seguimiento_mensajes
                WHERE caso_id = ?
                ORDER BY id
            """, (caso_id,))
        ]

        contactos = [
            {
                "id": f[0],
                "canal": f[1],
                "resultado": f[2],
                "observacion": f[3],
                "fecha": f[4]
            }
            for f in con.execute("""
                SELECT id, canal, resultado,
                       observacion, fecha_contacto
                FROM seguimiento_contactos
                WHERE caso_id = ?
                ORDER BY id
            """, (caso_id,))
        ]

        return {
            "resultado": "ok",
            "caso_id": caso_id,
            "estado": caso[1],
            "mensajes": mensajes,
            "contactos": contactos
        }

    finally:
        con.close()
