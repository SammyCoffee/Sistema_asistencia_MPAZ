import json
import os
from http.client import HTTPException
from urllib import request
from urllib.error import HTTPError, URLError

from cola_pendientes import (
    cargar_pendientes,
    eliminar_pendiente
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
        with request.urlopen(solicitud, timeout=10) as respuesta:
            contenido = respuesta.read().decode("utf-8")

            datos_respuesta = json.loads(contenido)
            if (not isinstance(datos_respuesta, dict)
                or not isinstance(datos_respuesta.get("resultado"), str)):
                return False, {"resultado": "respuesta_invalida"}
            # HTTP 200 también transporta rechazos de negocio. Solo retirar
            # eventos registrados o atendidos por las reglas vigentes.
            confirmados = {
                "entrada_registrada", "salida_registrada", "evento_repetido",
                "lectura_repetida", "jornada_completa"
            }
            return datos_respuesta["resultado"] in confirmados, datos_respuesta
    
    except HTTPError as error:
        contenido = error.read().decode("utf-8", errors="replace")

        try:
            respuesta_error = json.loads(contenido)

        except json.JSONDecodeError:
            respuesta_error = {
            "resultado": "error_http",
            "mensaje": contenido,
            "codigo_http": error.code
            }
        return False, respuesta_error
    
    except (json.JSONDecodeError, UnicodeDecodeError):
        return False, {"resultado": "respuesta_invalida"}
    except (URLError, TimeoutError, ConnectionError, HTTPException):
        return False, {
            "resultado": "sin_conexion",
            "mensaje": "No fue posible completar el envío; se conserva el evento"
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
                eliminar_pendiente(pendiente.get("evento_id"))
                print("Lectura retirada la cola")

            else:
                pendientes_restantes.append(
                    pendiente
                )

                print(
                    "La lectura continua pendiente"
                )

        # No sobrescribir una instantánea: pueden haber llegado eventos nuevos.
        pendientes_restantes = cargar_pendientes()

        print("-----------------------------")
        print(
            "Pendientes restantes:",
            len(pendientes_restantes)
        )