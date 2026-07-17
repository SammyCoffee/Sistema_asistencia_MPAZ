from base_datos import buscar_alumno_por_uid, guardar_asistencia
from datetime import datetime
from lector_nfc import obtener_uid

def procesar_asistencia(uid):
    uid = uid.strip().replace(" ","").upper()
    
    alumno = buscar_alumno_por_uid(uid)
    
    if not alumno:    
        return{
            "resultado": "no_registrada",
            "mensaje": "No existe un alumno con el uid ingresado",
            "uid": uid
        }
    if alumno[3] != "activa":
        return {
            "resultado": "bloqueada",
            "mensaje":"La tarjeta esta bloqueada",
            "uid": uid
        }    
    momento_actual = datetime.now()
    
    fecha = momento_actual.strftime("%Y-%m-%d")
    hora = momento_actual.strftime("%H:%M:%S")
    
    asistencia_guardada = guardar_asistencia(
        alumno[0],
        fecha,
        hora
    )
    
    if asistencia_guardada:
        resultado = "registrada"
        mensaje = "Asistencia registrada correctamente"
    
    else:
        resultado = "duplicada"
        mensaje = "La asistencia de este alumno ya fue registrada hoy"
    
    return {
        "resultado": resultado,
        "mensaje": mensaje,
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
        print("Curso", respuesta["curso"])
        print("Fecha:", respuesta["fecha"])
    
        if respuesta["resultado"] == "registrada":
            print("Hora:", respuesta["hora"])
        
        

    