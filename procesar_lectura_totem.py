from base_datos import validar_totem
from registrar_asistencia import procesar_asistencia


def procesar_lectura_totem(codigo_totem, uid, evento_id=None):
    respuesta_totem = validar_totem(codigo_totem)

    if respuesta_totem["resultado"] == "no existe":
        return {
            "resultado": "totem_no_autorizado",
            "mensaje": "El Tótem no esta registrado",
            "led": "rojo",
            "buzzer": "un_pitido_largo"
        }
    if respuesta_totem["resultado"] == "inactivo":
        return {
            "resultado": "totem_inactivo",
            "mensaje": "El Tómen no esta activo",
            "led": "rojo",
            "buzzer": "un_pitido_largo"
        }
    respuesta_asistencia = procesar_asistencia(
        uid, 
        respuesta_totem["id"],
        evento_id
        )

    if respuesta_asistencia["resultado"] == "registrada":
        return {
            "resultado": "registrada",
            "mensaje": respuesta_asistencia["mensaje"],
            "totem": respuesta_totem["codigo"],
            "alumno": respuesta_asistencia["alumno"],
            "curso": respuesta_asistencia["curso"],
            "fecha": respuesta_asistencia["fecha"],
            "hora": respuesta_asistencia["hora"],
            "led": "verde",
            "buzzer": "un_pitido_corto"
        }
    if respuesta_asistencia["resultado"] == "duplicada":
        return{
            "resultado": "duplicada",
            "mensaje": respuesta_asistencia["mensaje"],
            "totem": respuesta_totem["codigo"],
            "alumno": respuesta_asistencia["alumno"],
            "curso": respuesta_asistencia["curso"],
            "fecha": respuesta_asistencia["fecha"],
            "led": "amarillo",
            "buzzer": "dos_pitidos_cortos"
        }
    
    if respuesta_asistencia["resultado"] == "evento_repetido":
        return{
            "resultado": "evento_repetido",
            "mensaje": respuesta_asistencia["mensaje"],
            "totem": respuesta_totem["codigo"],
            "alumno": respuesta_asistencia["alumno"],
            "curso": respuesta_asistencia["curso"],
            "fecha": respuesta_asistencia["fecha"],
            "led": "amarillo",
            "buzzer": "dos_pitidos_cortos"
        }
    
    if respuesta_asistencia["resultado"] == "bloqueda":
        return{
            "resultado": "tarjeta_bloqueada",
            "mensaje": respuesta_asistencia["mensaje"],
            "totem": respuesta_totem["codigo"],
            "led": "rojo",
            "buzzer": "un_pitido_largo"
        }
    
    return {
        "resultado": "tarjeta_desconocida",
        "mensaje": respuesta_asistencia["mensaje"],
        "totem": respuesta_totem["codigo"],
        "led": "rojo",
        "buzzer": "pitido_largo"

     }