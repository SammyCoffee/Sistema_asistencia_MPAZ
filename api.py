import os
import secrets

from flask import Flask, jsonify, request

from procesar_lectura_totem import procesar_lectura_totem


app = Flask(__name__)

API_KEY = os.getenv("MPAZ_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "No se encontro la variable de entorno MPAZ_API_KEY" 
    )


@app.get("/estado")
def consultar_estado():
    return jsonify(
        {
            "sistema": "MPAZ RFID",
            "estado": "activo",
            "mensaje": "API funcionando correctamente"
        }

    )

@app.post("/lectura")
def recibir_lectura():
    clave_recibida = request.headers.get("X-API-KEY", "")
    
    
    if not secrets.compare_digest(clave_recibida, API_KEY):
        return jsonify(
            {
            "resultado": "no_autorizado",
            "mensaje": "La clave de acceso no es valida"
            }
        ), 401


    datos = request.get_json(silent=True)

    if not datos:
        return jsonify(
            {
                "resultado": "solicitud_invalida",
                "mensaje": "Debe enviar informacion en formato JSON"
            }
        ), 400
    
    codigo_totem = datos.get("codigo_totem", "")
    uid = datos.get("uid", "")
    evento_id = datos.get("evento_id", "")

    if (

     not isinstance(codigo_totem, str)
       or not isinstance(uid, str)
       or not isinstance(evento_id, str)

    ):
        return jsonify(
            {
                "resultado": "datos_invalidos",
                "mensaje": (
                "El codigo del Tótem, el UID " 
                "y el  evento deben ser texto"
                )
            }
        ), 400
    
    codigo_totem = codigo_totem.strip()
    uid = uid.strip()
    evento_id = evento_id.strip()

    if not codigo_totem or not uid or not evento_id: 
        return jsonify(
            {
                "resultado": "datos_incompletos",
                "mensaje": (
                    "Falta el codigo del Tótem," 
                    "el UID o el evento"
                )
            }
        ), 400
    
    respuesta = procesar_lectura_totem(
        codigo_totem,
        uid,
        evento_id

    )

    resultado = respuesta.get("resultado")

    if not resultado:
        return jsonify(
            {
                "resultado": "error_interno",
                "mensaje": ("La respuesta interna no contiene " 
                "un resultado valido"
                )
            }
        ), 500

    if resultado in (
        "totem_no_autorizado",
        "totem_inactivo"
    ):
        return jsonify(respuesta), 403
    
    return jsonify(respuesta), 200

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )