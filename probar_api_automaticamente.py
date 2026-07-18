import json
import os
import sys
import urllib.error
import urllib.request


# ==================================================
# CONFIGURACIÓN
# ==================================================

API_BASE = os.getenv(
    "MPAZ_API_URL",
    "http://127.0.0.1:5000"
)

API_KEY = os.getenv(
    "MPAZ_API_KEY"
)


# ==================================================
# FUNCIÓN PARA ENVIAR PETICIONES A LA API
# ==================================================

def enviar_peticion(
    metodo,
    ruta,
    datos=None,
    incluir_clave=True
):
    url = f"{API_BASE}{ruta}"

    encabezados = {
        "Accept": "application/json"
    }

    # Agregamos la clave solo cuando la prueba lo requiere.
    if incluir_clave and API_KEY:
        encabezados["X-API-Key"] = API_KEY

    cuerpo = None

    if datos is not None:
        cuerpo = json.dumps(datos).encode(
            "utf-8"
        )

        encabezados["Content-Type"] = (
            "application/json"
        )

    solicitud = urllib.request.Request(
        url,
        data=cuerpo,
        headers=encabezados,
        method=metodo
    )

    try:
        with urllib.request.urlopen(
            solicitud,
            timeout=5
        ) as respuesta:
            contenido = respuesta.read().decode(
                "utf-8"
            )

            return (
                respuesta.status,
                convertir_respuesta(contenido)
            )

    except urllib.error.HTTPError as error:
        contenido = error.read().decode(
            "utf-8"
        )

        return (
            error.code,
            convertir_respuesta(contenido)
        )


# ==================================================
# INTENTA CONVERTIR LA RESPUESTA A JSON
# ==================================================

def convertir_respuesta(contenido):
    try:
        return json.loads(contenido)

    except json.JSONDecodeError:
        return {
            "respuesta_texto": contenido
        }


# ==================================================
# COMPARA EL RESULTADO REAL CON EL ESPERADO
# ==================================================

def comprobar_prueba(
    numero,
    nombre,
    estado_obtenido,
    estado_esperado,
    respuesta
):
    aprobado = (
        estado_obtenido == estado_esperado
    )

    simbolo = "✅" if aprobado else "❌"
    resultado = "APROBADA" if aprobado else "FALLIDA"

    print("")
    print(
        f"{simbolo} PRUEBA {numero}: {nombre}"
    )
    print(
        f"Resultado: {resultado}"
    )
    print(
        f"HTTP esperado: {estado_esperado}"
    )
    print(
        f"HTTP obtenido: {estado_obtenido}"
    )
    print(
        "Respuesta:",
        respuesta
    )

    return aprobado


# ==================================================
# EJECUCIÓN DE TODAS LAS PRUEBAS
# ==================================================

def ejecutar_pruebas():
    if not API_KEY:
        print(
            "ERROR: no se encontró MPAZ_API_KEY."
        )
        print(
            "Ejecuta primero:"
        )
        print(
            "source .mpaz_api_key"
        )

        sys.exit(1)

    resultados = []

    print(
        "PRUEBAS AUTOMÁTICAS DE LA API MPAZ RFID"
    )
    print("=" * 55)
    print(
        "Servidor:",
        API_BASE
    )

    try:
        # ==========================================
        # PRUEBA 1
        # Consultar el estado sin utilizar clave.
        # Debe ser una ruta pública.
        # ==========================================

        estado, respuesta = enviar_peticion(
            metodo="GET",
            ruta="/estado",
            incluir_clave=False
        )

        resultados.append(
            comprobar_prueba(
                numero=1,
                nombre="Estado público de la API",
                estado_obtenido=estado,
                estado_esperado=200,
                respuesta=respuesta
            )
        )

        # ==========================================
        # PRUEBA 2
        # Intentar registrar sin clave de API.
        # La API debe rechazar la petición.
        # ==========================================

        estado, respuesta = enviar_peticion(
            metodo="POST",
            ruta="/lectura",
            datos={
                "codigo_totem": "MPAZ-DEMO-01",
                "uid": "A1B2C3D4",
                "evento_id": "TEST-SIN-CLAVE"
            },
            incluir_clave=False
        )

        resultados.append(
            comprobar_prueba(
                numero=2,
                nombre="Lectura sin clave",
                estado_obtenido=estado,
                estado_esperado=401,
                respuesta=respuesta
            )
        )

        # ==========================================
        # PRUEBA 3
        # Enviar un JSON vacío.
        # Debe indicar datos incompletos.
        # ==========================================

        estado, respuesta = enviar_peticion(
            metodo="POST",
            ruta="/lectura",
            datos={}
        )

        resultados.append(
            comprobar_prueba(
                numero=3,
                nombre="JSON vacío",
                estado_obtenido=estado,
                estado_esperado=400,
                respuesta=respuesta
            )
        )

        # ==========================================
        # PRUEBA 4
        # Enviar una lectura sin evento_id.
        # Debe rechazarla por falta de información.
        # ==========================================

        estado, respuesta = enviar_peticion(
            metodo="POST",
            ruta="/lectura",
            datos={
                "codigo_totem": "MPAZ-DEMO-01",
                "uid": "A1B2C3D4"
            }
        )

        resultados.append(
            comprobar_prueba(
                numero=4,
                nombre="Lectura sin evento_id",
                estado_obtenido=estado,
                estado_esperado=400,
                respuesta=respuesta
            )
        )

        # ==========================================
        # PRUEBA 5
        # Enviar el UID como número.
        # La API debe exigir texto.
        # ==========================================

        estado, respuesta = enviar_peticion(
            metodo="POST",
            ruta="/lectura",
            datos={
                "codigo_totem": "MPAZ-DEMO-01",
                "uid": 12345678,
                "evento_id": "TEST-UID-NUMERICO"
            }
        )

        resultados.append(
            comprobar_prueba(
                numero=5,
                nombre="UID con tipo incorrecto",
                estado_obtenido=estado,
                estado_esperado=400,
                respuesta=respuesta
            )
        )

        # ==========================================
        # PRUEBA 6
        # Utilizar un tótem que no está registrado.
        # Debe rechazarlo sin provocar error 500.
        # ==========================================

        estado, respuesta = enviar_peticion(
            metodo="POST",
            ruta="/lectura",
            datos={
                "codigo_totem": "TOTEM-INEXISTENTE",
                "uid": "A1B2C3D4",
                "evento_id": "TEST-TOTEM-DESCONOCIDO"
            }
        )

        resultados.append(
            comprobar_prueba(
                numero=6,
                nombre="Tótem no autorizado",
                estado_obtenido=estado,
                estado_esperado=403,
                respuesta=respuesta
            )
        )

    except urllib.error.URLError as error:
        print("")
        print(
            "No fue posible conectarse con la API."
        )
        print(
            "Detalle:",
            error
        )
        print("")
        print(
            "Comprueba que api.py esté funcionando."
        )

        sys.exit(1)

    # ==============================================
    # RESUMEN FINAL
    # ==============================================

    aprobadas = sum(resultados)
    total = len(resultados)
    fallidas = total - aprobadas

    print("")
    print("=" * 55)
    print("RESUMEN")
    print("=" * 55)
    print(
        "Pruebas ejecutadas:",
        total
    )
    print(
        "Pruebas aprobadas:",
        aprobadas
    )
    print(
        "Pruebas fallidas:",
        fallidas
    )

    if fallidas == 0:
        print("")
        print(
            "✅ Todas las pruebas fueron aprobadas."
        )
        sys.exit(0)

    print("")
    print(
        "❌ Existen pruebas que debemos revisar."
    )
    sys.exit(1)


if __name__ == "__main__":
    ejecutar_pruebas()