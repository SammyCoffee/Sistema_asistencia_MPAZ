
"""Seguimiento escolar MPAZ RFID.

Etapa inicial: casos docentes por inasistencia o atraso.
No modifica las marcaciones RFID.
"""

from base_datos import obtener_conexion


ESTADOS_POR_TIPO = {
    "inasistencia": "no_presente",
    "atraso": "atrasado",
}


def _id_valido(valor):
    return type(valor) is int and valor > 0


def crear_caso_docente(
    profesor_id,
    alumno_id,
    sesion_clase_id,
    tipo,
    descripcion
):
    """Abre un caso de seguimiento validando permisos y asistencia."""

    if not all(
        _id_valido(valor)
        for valor in (profesor_id, alumno_id, sesion_clase_id)
    ):
        return {"resultado": "datos_invalidos"}

    if tipo not in ESTADOS_POR_TIPO:
        return {"resultado": "tipo_invalido"}

    if not isinstance(descripcion, str):
        return {"resultado": "descripcion_invalida"}

    descripcion = descripcion.strip()

    if not 1 <= len(descripcion) <= 1000:
        return {"resultado": "descripcion_invalida"}

    con = obtener_conexion()

    try:
        con.execute("BEGIN IMMEDIATE")

        sesion = con.execute("""
            SELECT sc.fecha, pc.curso
            FROM sesiones_clase sc
            JOIN profesores_cursos pc
                ON pc.id = sc.asignacion_id
            JOIN usuarios u
                ON u.id = pc.profesor_id
            JOIN asignaturas asig
                ON asig.id = pc.asignatura_id
            WHERE sc.id = ?
              AND pc.profesor_id = ?
              AND pc.estado = 'activo'
              AND u.rol = 'profesor'
              AND u.estado = 'activo'
              AND asig.estado = 'activo'
              AND sc.estado != 'anulada'
            LIMIT 1
        """, (sesion_clase_id, profesor_id)).fetchone()

        if sesion is None:
            return {"resultado": "no_autorizado"}

        fecha, curso = sesion

        alumno = con.execute("""
            SELECT id
            FROM alumnos
            WHERE id = ?
              AND curso = ?
              AND estado = 'activo'
            LIMIT 1
        """, (alumno_id, curso)).fetchone()

        if alumno is None:
            return {"resultado": "alumno_no_autorizado"}

        asistencia = con.execute("""
            SELECT estado
            FROM asistencias_clase
            WHERE sesion_clase_id = ?
              AND alumno_id = ?
            LIMIT 1
        """, (sesion_clase_id, alumno_id)).fetchone()

        if (
            asistencia is None
            or asistencia[0] != ESTADOS_POR_TIPO[tipo]
        ):
            return {"resultado": "asistencia_no_coincide"}

        existente = con.execute("""
            SELECT id
            FROM seguimiento_casos
            WHERE alumno_id = ?
              AND sesion_clase_id = ?
              AND tipo = ?
            LIMIT 1
        """, (alumno_id, sesion_clase_id, tipo)).fetchone()

        if existente:
            return {
                "resultado": "caso_existente",
                "caso_id": existente[0]
            }

        cursor = con.execute("""
            INSERT INTO seguimiento_casos (
                alumno_id,
                sesion_clase_id,
                curso,
                fecha_evento,
                tipo,
                descripcion,
                creado_por_rol,
                creado_por_usuario_id
            )
            VALUES (?, ?, ?, ?, ?, ?, 'docente', ?)
        """, (
            alumno_id,
            sesion_clase_id,
            curso,
            fecha,
            tipo,
            descripcion,
            profesor_id
        ))

        caso_id = cursor.lastrowid

        con.execute("""
            INSERT INTO seguimiento_avisos (
                caso_id,
                destinatario_rol
            )
            VALUES (?, 'administracion')
        """, (caso_id,))

        con.commit()

        return {
            "resultado": "caso_creado",
            "caso_id": caso_id,
            "estado": "pendiente",
            "aviso": "administracion"
        }

    finally:
        con.close()


def listar_casos_docente(profesor_id):
    """Consulta casos de cursos actualmente asignados al profesor."""

    if not _id_valido(profesor_id):
        return {"resultado": "datos_invalidos", "casos": []}

    con = obtener_conexion()

    try:
        filas = con.execute("""
            SELECT
                c.id,
                c.alumno_id,
                a.nombre_completo,
                c.curso,
                c.fecha_evento,
                c.tipo,
                c.estado,
                c.descripcion,
                c.creado_en
            FROM seguimiento_casos c
            JOIN alumnos a
                ON a.id = c.alumno_id
            WHERE EXISTS (
                SELECT 1
                FROM profesores_cursos pc
                JOIN usuarios u
                    ON u.id = pc.profesor_id
                WHERE pc.curso = c.curso
                  AND pc.profesor_id = ?
                  AND pc.estado = 'activo'
                  AND u.rol = 'profesor'
                  AND u.estado = 'activo'
            )
            ORDER BY c.creado_en DESC, c.id DESC
            LIMIT 50
        """, (profesor_id,)).fetchall()

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
