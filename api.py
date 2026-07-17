from flask import Flask, jsonify, request

from procesar_lectura_totem import procesar_lectura_totem


app = Flask(__name__)


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

    if not isinstance(codigo_totem, str) or not isinstance(uid, str):
        return jsonify(
            {
                "resultado": "datos_invalidos",
                "mensaje": "El codigo del Tótem y el UID deben ser texto"
            }
        ), 400
    
    codigo_totem = codigo_totem.strip()
    uid = uid.strip()

    if not isinstance(codigo_totem, str) or not isinstance(uid, str):
        return jsonify(
            {
                "resultado": "datos_invalidos",
                "mensaje": "Falta el codigo del Tótem o el UID"
            }
        ), 400
    
    respuesta = procesar_lectura_totem(
        codigo_totem,
        uid

    )

    if respuesta["resultado"] in (
        "totem_no_autorizado",
        "totem_inactivo"
    ):
        return jsonify(respuesta), 403
    return jsonify(respuesta), 200

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )