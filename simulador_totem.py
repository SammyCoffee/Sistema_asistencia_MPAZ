import json
import os
import uuid
from datetime import datetime
from urllib import request
from urllib.error import HTTPError, URLError
from cola_pendientes import agregar_pendiente


API_KEY = os.getenv("MPAZ_API_KEY")

API_URL = os.getenv(
    "MPAZ_API_URL",
    "http://127.0.0.1:5000/lectura"
)

CODIGO_TOTEM = os.getenv(
    "CODIGO_TOTEM",
    "MPAZ-ENTRADA-01"
)

if not API_KEY:
    raise RuntimeError(
        "No se encontro la variable de entorno MPAZ_API_KEY"
    )

def crear_evento_id():
    fecha_hora = datetime.now().strftime("%Y%m%d-%H%M%S")
    codigo_aleatorio = uuid.uuid4().hex[:8].upper()

    return (
        f"{CODIGO_TOTEM}-"
        F"{fecha_hora}-"
        f"{codigo_aleatorio}"
    )
def enviar_lectura(uid):
    uid = uid.strip()

    if not uid:
        return {
            "resultado": "uid_vacio",
            "mensaje": "Debe ingresar un UID"
        }
    
    datos = {
        "codigo_totem": CODIGO_TOTEM,
        "uid": uid,
        "evento_id": crear_evento_id()
    }

    cuerpo = json.dumps(datos).encode("utf-8")

    solicitud = request.Request(
        API_URL,
        data=cuerpo,
        headers={
            "Content-Type": "application/json",
            "X-API-Key": API_KEY
        },
        method="POST"
        
    )

    try: 
        with request.urlopen(solicitud) as respuesta:
            contenido = respuesta.read().decode("utf-8")

            return json.loads(contenido)
        
    except HTTPError as error:
        contenido = error.read().decode("utf-8")

        try:

            return json.loads(contenido)
        
        except json.JSONDecodeError:
            return {
                "resultado": "error_http",
                "mensaje": contenido,
                "codigo_http": error.code
            }
        
    except URLError as error:
        agregar_pendiente(datos)
        
        return {
            "resultado": "sin_conexion",
            "mensaje": str(error.reason),
            "evento_id": datos["evento_id"],
            "guardada_pendiente": True
        }    

if __name__ == "__main__":
    uid = input("Ingrese el UID de la targeta: ")

    respuesta = enviar_lectura(uid)

    print("Resultado:", respuesta.get("resultado"))
    print("Mensaje:", respuesta.get("mensaje"))

    if respuesta.get("guardada_pendiente"):
        print("Lectura guardada para enviarla mas tarde")
        print("Evento:", respuesta.get("evento_id"))

    if "alumno" in respuesta:
        print("Alumno:", respuesta["alumno"])
        print("Curso:", respuesta["curso"])

    print("LED:", respuesta.get("led", "sin_indicacion"))
    print("Buzzer:", respuesta.get("buzzer", "sin_indicacion"))    
    