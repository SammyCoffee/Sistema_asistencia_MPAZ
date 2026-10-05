from base_datos import (
    buscar_alumno_por_uid,
    guardar_asistencia,
    cerrar_jornadas_pendientes
)
from datetime import datetime
from lector_nfc import obtener_uid


def procesar_asistencia(uid, totem_id=None, evento_id=None):
    uid = uid.strip().replace(" ", "").upper()

    cerrar_jornadas_pendientes()

    alumno = buscar_alumno_por_uid(uid)

    if not alumno:
        return {
            "resultado": "no_registrada",
            "mensaje": "No existe un alumno con el UID ingresado",
            "uid": uid
        }

    if alumno[3] != "activa":
        return {
            "resultado": "bloqueada",
            "mensaje": "La tarjeta está bloqueada",
            "uid": uid
        }

    if alumno[4] != "activo":
        return {
        "resultado": "alumno_inactivo",
        "mensaje": "El alumno se encuentra inactivo",
        "uid": uid
        }

    momento_actual = datetime.now()

    fecha = momento_actual.strftime("%Y-%m-%d")
    hora = momento_actual.strftime("%H:%M:%S")

    resultado_guardado = guardar_asistencia(
        alumno[0],
        fecha,
        hora,
        totem_id,
        evento_id
    )

    # ==========================================
    # ENTRADA
    # ==========================================

    if resultado_guardado == "entrada_registrada":
        return {
            "resultado": "entrada_registrada",
            "mensaje": "Entrada registrada correctamente",
            "alumno": alumno[1],
            "curso": alumno[2],
            "fecha": fecha,
            "hora": hora,
            "hora_entrada": hora,
            "hora_salida": None
        }

    # ==========================================
    # SALIDA
    # ==========================================

    if resultado_guardado == "salida_registrada":
        return {
            "resultado": "salida_registrada",
            "mensaje": "Salida registrada correctamente",
            "alumno": alumno[1],
            "curso": alumno[2],
            "fecha": fecha,
            "hora": hora,
            "hora_salida": hora
        }

    # ==========================================
    # DOBLE LECTURA MUY RAPIDA
    # ==========================================

    if resultado_guardado == "lectura_repetida":
        return {
            "resultado": "lectura_repetida",
            "mensaje": (
                "Lectura ignorada para evitar "
                "una salida accidental"
            ),
            "alumno": alumno[1],
            "curso": alumno[2],
            "fecha": fecha,
            "hora": hora
        }

    # ==========================================
    # JORNADA YA CERRADA
    # ==========================================

    if resultado_guardado == "jornada_completa":
        return {
            "resultado": "jornada_completa",
            "mensaje": (
                "El alumno ya tiene entrada "
                "y salida registradas hoy"
            ),
            "alumno": alumno[1],
            "curso": alumno[2],
            "fecha": fecha,
            "hora": hora
        }

    # ==========================================
    # EVENTO YA PROCESADO
    # ==========================================

    if resultado_guardado == "evento_repetido":
        return {
            "resultado": "evento_repetido",
            "mensaje": (
                "Este evento ya fue procesado "
                "anteriormente"
            ),
            "alumno": alumno[1],
            "curso": alumno[2],
            "fecha": fecha,
            "hora": hora
        }

    return {
        "resultado": "error",
        "mensaje": "No fue posible procesar la asistencia",
        "alumno": alumno[1],
        "curso": alumno[2],
        "fecha": fecha,
        "hora": hora
    }


if __name__ == "__main__":
    uid_ingresado = obtener_uid()

    respuesta = procesar_asistencia(uid_ingresado)

    print(respuesta["mensaje"])

    if respuesta["resultado"] in ("registrada", "duplicada"):
        print("Alumno:", respuesta["alumno"])
        print("Curso:", respuesta["curso"])
        print("Fecha:", respuesta["fecha"])

        if respuesta["resultado"] == "registrada":
            print("Hora:", respuesta["hora"])