import os
import json
from urllib import request
from urllib.error import HTTPError, URLError

API_KEY = os.getenv("MPAZ_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "No se encontro la variable de entorno MPAZ_API_KEY"
    )



datos = {
        "codigo_totem": "mpaz-entrada-01",
        "uid": "123456789",
        "evento_id": "EVENTO-JUAN-001"
}

cuerpo = json.dumps(datos).encode("utf-8")

url_api = "http://127.0.0.1:5000/lectura"


solicitud = request.Request(
    url_api,
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

        print("Código HTTP:", respuesta.status)
        print("Respuesta del servidor:")
        print(contenido)

except HTTPError as error:
    contenido = error.read().decode("utf-8")

    print("Código HTTP:", error.code)
    print("Respuesta del servidor:")
    print(contenido)

except URLError as error:
    print("No fue posible conectarse con la API")
    print("Detalle del error:", error.reason)            