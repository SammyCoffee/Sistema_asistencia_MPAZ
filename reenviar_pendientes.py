import json
import os
from urllib import request
from urllib.error import HTTPError, URLError

from cola_pendientes import (
    cargar_pendientes,
    guardar_pendiente
)

API_KEY = os.getenv("MPAZ_API_KEY")

API_URL = os.getenv(

    "MPAZ_API_URL",
    "http://127.0.0.1:5000/lectura"
)

if not API_KEY:
    raise RuntimeError(
        "No se encontro la variable de entorno MPAZ_API_KEY"
    )

def enviar_pendiente(datos):
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

            return True, json.loads(contenido)
    
    except HTTPError as error:
        contenido = error.read().decode("utf-8")

        try:
            respuesta_error = json.loads(contenido)

        except json.JSONDecodeError:
            respuesta_error = {
            "resultado": "error_http",
            "mensaje": contenido,
            "codigo_http": error.code
            }
        return False, respuesta_error
    
    except URLError as error:
        return False, {
            "resultado": "sin_conexion",
            "mensaje": str(error.reason)
        }
if __name__ == "__main__":
    pendientes = cargar_pendientes()    

    if not pendientes:
        print("No existen lecturas pendientes")

    else:
        pendientes_restantes = []

        for pendiente in pendientes:
            print("-----------------------------")
            print(
                "Reenviando evento:",
                pendiente.get("evento_id")
            )

            procesada, respuesta = enviar_pendiente(
                pendiente
            )

            print(
                "Resultado:",
                respuesta.get("resultado")
            )

            print(
                "Mensaje:",
                respuesta.get("mensaje")
            )

            if procesada:
                print("Lectura retirada la cola")

            else:
                pendientes_restantes.append(
                    pendiente
                )

                print(
                    "La lectura continua pendiente"
                )

        guardar_pendiente(
            pendientes_restantes
        )        

        print("-----------------------------")
        print(
            "Pendientes restantes:",
            len(pendientes_restantes)
        )