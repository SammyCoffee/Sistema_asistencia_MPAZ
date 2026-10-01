from base_datos import validar_totem
from registrar_asistencia import procesar_asistencia


def procesar_lectura_totem(
    codigo_totem,
    uid,
    evento_id=None
):
    respuesta_totem = validar_totem(
        codigo_totem
    )

    resultado_totem = respuesta_totem.get(
        "resultado"
    )

    # ==========================================
    # TOTEM NO REGISTRADO
    # ==========================================

    if resultado_totem == "no_existe":
        return {
            "resultado": "totem_no_autorizado",
            "mensaje": "El tótem no está registrado",
            "totem": codigo_totem,
            "led": "rojo",
            "buzzer": "un_pitido_largo"
        }

    # ==========================================
    # TOTEM INACTIVO
    # ==========================================

    if resultado_totem == "inactivo":
        return {
            "resultado": "totem_inactivo",
            "mensaje": "El tótem está inactivo",
            "totem": respuesta_totem.get(
                "codigo",
                codigo_totem
            ),
            "led": "rojo",
            "buzzer": "un_pitido_largo"
        }

    totem_id = respuesta_totem.get("id")

    if (
        resultado_totem != "activo"
        or totem_id is None
    ):
        return {
            "resultado": "totem_no_autorizado",
            "mensaje": (
                "No fue posible validar el tótem"
            ),
            "totem": respuesta_totem.get(
                "codigo",
                codigo_totem
            ),
            "led": "rojo",
            "buzzer": "un_pitido_largo"
        }

    # ==========================================
    # PROCESAR TARJETA
    # ==========================================

    respuesta_asistencia = procesar_asistencia(
        uid,
        totem_id,
        evento_id
    )

    resultado_asistencia = (
        respuesta_asistencia.get("resultado")
    )

    # ==========================================
    # ENTRADA REGISTRADA
    # ==========================================

    if resultado_asistencia == "entrada_registrada":
        return {
            "resultado": "entrada_registrada",
            "mensaje": respuesta_asistencia["mensaje"],
            "totem": respuesta_totem["codigo"],
            "alumno": respuesta_asistencia["alumno"],
            "curso": respuesta_asistencia["curso"],
            "fecha": respuesta_asistencia["fecha"],
            "hora": respuesta_asistencia["hora"],
            "hora_entrada": respuesta_asistencia[
                "hora_entrada"
            ],
            "led": "verde",
            "buzzer": "un_pitido_corto"
        }

    # ==========================================
    # SALIDA REGISTRADA
    # ==========================================

    if resultado_asistencia == "salida_registrada":
        return {
            "resultado": "salida_registrada",
            "mensaje": respuesta_asistencia["mensaje"],
            "totem": respuesta_totem["codigo"],
            "alumno": respuesta_asistencia["alumno"],
            "curso": respuesta_asistencia["curso"],
            "fecha": respuesta_asistencia["fecha"],
            "hora": respuesta_asistencia["hora"],
            "hora_salida": respuesta_asistencia[
                "hora_salida"
            ],
            "led": "verde",
            "buzzer": "un_pitido_corto"
        }

    # ==========================================
    # RELECTURA MUY RAPIDA
    # ==========================================

    if resultado_asistencia == "lectura_repetida":
        return {
            "resultado": "lectura_repetida",
            "mensaje": respuesta_asistencia["mensaje"],
            "totem": respuesta_totem["codigo"],
            "alumno": respuesta_asistencia["alumno"],
            "curso": respuesta_asistencia["curso"],
            "fecha": respuesta_asistencia["fecha"],
            "hora": respuesta_asistencia["hora"],
            "led": "amarillo",
            "buzzer": "dos_pitidos_cortos"
        }

    # ==========================================
    # JORNADA YA COMPLETA
    # ==========================================

    if resultado_asistencia == "jornada_completa":
        return {
            "resultado": "jornada_completa",
            "mensaje": respuesta_asistencia["mensaje"],
            "totem": respuesta_totem["codigo"],
            "alumno": respuesta_asistencia["alumno"],
            "curso": respuesta_asistencia["curso"],
            "fecha": respuesta_asistencia["fecha"],
            "hora": respuesta_asistencia["hora"],
            "led": "amarillo",
            "buzzer": "dos_pitidos_cortos"
        }

    # ==========================================
    # EVENTO YA PROCESADO
    # ==========================================

    if resultado_asistencia == "evento_repetido":
        return {
            "resultado": "evento_repetido",
            "mensaje": respuesta_asistencia["mensaje"],
            "totem": respuesta_totem["codigo"],
            "alumno": respuesta_asistencia["alumno"],
            "curso": respuesta_asistencia["curso"],
            "fecha": respuesta_asistencia["fecha"],
            "hora": respuesta_asistencia["hora"],
            "led": "amarillo",
            "buzzer": "dos_pitidos_cortos"
        }

    # ==========================================
    # TARJETA BLOQUEADA
    # ==========================================

    if resultado_asistencia == "bloqueada":
        return {
            "resultado": "tarjeta_bloqueada",
            "mensaje": respuesta_asistencia["mensaje"],
            "totem": respuesta_totem["codigo"],
            "led": "rojo",
            "buzzer": "un_pitido_largo"
        }

    # ==========================================
    # ERROR INTERNO
    # ==========================================

    if resultado_asistencia == "error":
        return {
            "resultado": "error_interno",
            "mensaje": respuesta_asistencia["mensaje"],
            "totem": respuesta_totem["codigo"],
            "led": "rojo",
            "buzzer": "un_pitido_largo"
        }

    # ==========================================
    # TARJETA DESCONOCIDA
    # ==========================================

    return {
        "resultado": "tarjeta_desconocida",
        "mensaje": respuesta_asistencia["mensaje"],
        "totem": respuesta_totem["codigo"],
        "led": "rojo",
        "buzzer": "un_pitido_largo"
    }