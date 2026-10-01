from base_datos import obtener_conexion


def obtener_asistencias():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT
                asistencias.id,
                alumnos.nombre_completo,
                alumnos.rut,
                alumnos.curso,
                asistencias.fecha,
                asistencias.hora_entrada,
                asistencias.hora_salida,
                asistencias.tipo_salida,
                totem_entrada.codigo,
                totem_salida.codigo,
                tarjetas.uid

            FROM asistencias

            INNER JOIN alumnos
                ON asistencias.alumno_id = alumnos.id

            LEFT JOIN totems AS totem_entrada
                ON asistencias.totem_entrada_id =
                   totem_entrada.id

            LEFT JOIN totems AS totem_salida
                ON asistencias.totem_salida_id =
                   totem_salida.id

            LEFT JOIN tarjetas
                ON tarjetas.alumno_id = alumnos.id
                AND tarjetas.estado = 'activa'

            ORDER BY
                asistencias.fecha DESC,
                asistencias.hora_entrada DESC
            """
        )

        return cursor.fetchall()

    finally:
        conexion.close()
        
def obtener_inasistencias():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            WITH fechas_registradas AS (
                SELECT DISTINCT fecha
                FROM asistencias
            ),
            total_jornadas AS (
                SELECT COUNT(*) AS cantidad
                FROM fechas_registradas
            )

            SELECT
                alumnos.id,
                alumnos.nombre_completo,
                alumnos.curso,
                (
                    SELECT cantidad
                    FROM total_jornadas
                ) - COUNT(DISTINCT asistencias.fecha)
                    AS inasistencias

            FROM alumnos

            LEFT JOIN asistencias
                ON asistencias.alumno_id = alumnos.id
                AND asistencias.fecha IN (
                    SELECT fecha
                    FROM fechas_registradas
                )

            GROUP BY
                alumnos.id,
                alumnos.nombre_completo,
                alumnos.curso

            ORDER BY
                inasistencias DESC,
                alumnos.curso,
                alumnos.nombre_completo
            """
        )

        return cursor.fetchall()

    finally:
        conexion.close()        


if __name__ == "__main__":
    registros = obtener_asistencias()

    if registros:
        print("REGISTROS DE ASISTENCIA")
        print("-------------------------")

        for registro in registros:
            print("ID:", registro[0])
            print("Nombre:", registro[1])
            print("RUT:", registro[2])
            print("Curso:", registro[3])
            print("Fecha:", registro[4])
            print("Hora:", registro[5])
            print("Tótem:", registro[6])
            print("Evento:", registro[7])
            print("UID:", registro[8])
            print("-------------------------")

    else:
        print("No hay registros de asistencia disponibles.")