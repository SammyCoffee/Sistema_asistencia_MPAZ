import sqlite3
from datetime import datetime
from lector_nfc import obtener_uid

uid_ingresado = obtener_uid()

conexion = sqlite3.connect("data/asistencia.db")
conexion.execute("PRAGMA foreign_keys = ON")

cursor = conexion.cursor()

try:
    cursor.execute(
        """
        SELECT id, nombre_completo,curso
        FROM alumnos
        WHERE uid = ?
        """,
        (uid_ingresado,)
    )
    alumno = cursor.fetchone()

    if alumno:
        momento_actual = datetime.now()

        fecha = momento_actual.strftime("%Y-%m-%d")
        hora = momento_actual.strftime("%H:%M:%S")

        cursor.execute(
            """

            SELECT id
            FROM asistencia
            WHERE alumno_id = ? AND fecha = ?
            """,
            (alumno[0], fecha)

       )
        
        asistencia_existente = cursor.fetchone()

        if asistencia_existente:
            print("la asistencia de este alumno ya fue registrada hoy")
            print("ALumno:", alumno[1])
            print("Curso:", alumno[2])
            print("Fecha:", fecha)

        else:
            cursor.execute(
                """
                INSERT INTO asistencia (alumno_id, fecha, hora)
                VALUES (?, ?, ?)
                """,
                (alumno[0], fecha, hora)
            )

            conexion.commit()

            print("Asistencia registrada correctamente")
            print("alumno: ", alumno[1])
            print("curso: ", alumno[2])
            print("Fecha: ", fecha)
            print("Hora: ", hora)

    else:
        print("no existe un alumno con el UID ingresado")

finally:
    conexion.close()    
