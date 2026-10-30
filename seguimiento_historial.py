
"""Consulta protegida del historial de Seguimiento Escolar."""

from base_datos import obtener_conexion


ROLES = ("administracion", "direccion")


def consultar_historial_operador(operador_id, caso_id):
    """Consulta un caso y sus intervenciones.

    La API debe obtener operador_id de la sesion autenticada.
    """

    if (
        type(operador_id) is not int
        or operador_id <= 0
        or type(caso_id) is not int
        or caso_id <= 0
    ):
        return {"resultado": "datos_invalidos"}

    con = obtener_conexion()

    try:
        operador = con.execute("""
            SELECT id, rol
            FROM seguimiento_operadores
            WHERE id = ?
              AND estado = 'activo'
            LIMIT 1
        """, (operador_id,)).fetchone()

        if operador is None or operador[1] not in ROLES:
            return {"resultado": "no_autorizado"}

        return _consultar_historial_conexion(con, caso_id)

    finally:
        con.close()


def _consultar_historial_conexion(con, caso_id):
    fila = con.execute("""
        SELECT
            c.id,
            c.alumno_id,
            a.nombre_completo,
            c.curso,
            c.fecha_evento,
            c.tipo,
            c.estado,
            c.descripcion,
            c.creado_en,
            c.actualizado_en,
            c.resuelto_en,
            c.creado_por_rol,
            COALESCE(u.nombre_completo, op.nombre_completo)
        FROM seguimiento_casos c
        JOIN alumnos a ON a.id = c.alumno_id
        LEFT JOIN usuarios u
            ON u.id = c.creado_por_usuario_id
        LEFT JOIN seguimiento_operadores op
            ON op.id = c.creado_por_operador_id
        WHERE c.id = ?
    """, (caso_id,)).fetchone()

    if fila is None:
        return {"resultado": "caso_no_existe"}

    caso = {
        "id": fila[0],
        "alumno_id": fila[1],
        "alumno": fila[2],
        "curso": fila[3],
        "fecha_evento": fila[4],
        "tipo": fila[5],
        "estado": fila[6],
        "descripcion": fila[7],
        "creado_en": fila[8],
        "actualizado_en": fila[9],
        "resuelto_en": fila[10],
        "creado_por_rol": fila[11],
        "creado_por": fila[12] or fila[11]
    }

    filas_mensajes = con.execute("""
        SELECT
            m.id,
            m.autor_rol,
            COALESCE(
                op.nombre_completo,
                u.nombre_completo,
                m.autor_rol
            ),
            m.mensaje,
            m.creado_en
        FROM seguimiento_mensajes m
        LEFT JOIN seguimiento_operadores op
            ON op.id = m.autor_operador_id
        LEFT JOIN usuarios u
            ON u.id = m.autor_usuario_id
        WHERE m.caso_id = ?
        ORDER BY m.id DESC
        LIMIT 201
    """, (caso_id,)).fetchall()

    filas_contactos = con.execute("""
        SELECT
            ct.id,
            ct.canal,
            ct.resultado,
            ct.observacion,
            ct.fecha_contacto,
            COALESCE(
                op.nombre_completo,
                u.nombre_completo,
                'Administracion'
            )
        FROM seguimiento_contactos ct
        LEFT JOIN seguimiento_operadores op
            ON op.id = ct.registrado_por_operador_id
        LEFT JOIN usuarios u
            ON u.id = ct.registrado_por_usuario_id
        WHERE ct.caso_id = ?
        ORDER BY ct.id DESC
        LIMIT 101
    """, (caso_id,)).fetchall()

    mensajes = [
        {
            "id": f[0],
            "autor_rol": f[1],
            "autor": f[2],
            "mensaje": f[3],
            "fecha": f[4]
        }
        for f in reversed(filas_mensajes[:200])
    ]

    contactos = [
        {
            "id": f[0],
            "canal": f[1],
            "resultado": f[2],
            "observacion": f[3],
            "fecha": f[4],
            "responsable": f[5]
        }
        for f in reversed(filas_contactos[:100])
    ]

    return {
        "resultado": "ok",
        "caso": caso,
        "mensajes": mensajes,
        "contactos": contactos,
        "historial_parcial": (
            len(filas_mensajes) > 200
            or len(filas_contactos) > 100
        )
    }


def consultar_historial_panel(caso_id):
    """Consulta interna; la ruta Flask debe validar la sesión."""

    if type(caso_id) is not int or caso_id <= 0:
        return {"resultado": "datos_invalidos"}

    con = obtener_conexion()

    try:
        return _consultar_historial_conexion(con, caso_id)
    finally:
        con.close()
