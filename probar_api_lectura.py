import json
from urllib import request
from urllib.error import HTTPError, URLError


datos = {
        "codigo_totem": "mpaz-entrada-01",
        "uid": "11 22 33 44"
}

cuerpo = json.dumps(datos).encode("utf-8")

solicitud = request.Request(
    "http://127.0.0.1:5000/lectura",
    data=cuerpo,
    headers={
        "Content-Type": "application/json"
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

    print("Codigo HTTP:", error.code)
    print("Respuesta del  servidor:")
    print(contenido)

except HTTPError as error:
    contenido = error.read().decode("utf-8")

    print("Código HTTP:", error.code)
    print("Respuesta del servidor:")
    print(contenido)

except URLError as error:
    print("No fue posible conectarse con la API")
    print("Detalle del error:", error.reason)            