import os
import secrets

from flask import (Flask,jsonify,request,session,redirect,send_file)
from consultar_alumnos import obtener_alumnos, buscar_alumnos
from procesar_lectura_totem import procesar_lectura_totem
from base_datos import asignar_tarjeta_por_rut, bloquear_tarjeta
from consultar_asistencia import obtener_asistencias
from exportar_asistencias_csv import exportar_asistencias

app = Flask(
    __name__,
    static_folder="interfaz_prueba",
    static_url_path=""
    )

@app.get("/")
@app.get("/index.html")
def mostrar_panel():

    if not session.get("panel_autorizado", False):
        return redirect("/login.html")

    return app.send_static_file("index.html")


app.secret_key = os.getenv("MPAZ_SESSION_SECRET")

if not app.secret_key:
    raise RuntimeError(
        "No se encontro la variable de entorno MPAZ_SESSION_SECRET"
    )

API_KEY = os.getenv("MPAZ_API_KEY")
PANEL_PASSWORD = os.getenv("MPAZ_PANEL_PASSWORD")

if not API_KEY:
    raise RuntimeError(
        "No se encontro la variable de entorno MPAZ_API_KEY" 
    )

if not PANEL_PASSWORD:
    raise RuntimeError(
        "No se encontro la variable de entorno MPAZ_PANEL_PASSWORD"
    )

@app.post("/panel/login")
def iniciar_sesion_panel():
    datos = request.get_json(silent=True) or {}

    password = datos.get("password", "")

    if not isinstance(password, str):
        return jsonify(
            {
            "resultado": "datos_invalidos",
            "mensaje": "La contraseña no es valida"
            }        
        ), 400
    
    if not secrets.compare_digest(password, PANEL_PASSWORD):
        return jsonify(
            {
                "resultado": "no_autorizado",
                "mensaje": "Contraseña incorrecta"
            }
        ), 401

    session["panel_autorizado"] = True

    return jsonify(
        {
            "resultado": "ok",
            "mensaje": "Sesion iniciada correctamente"
        }
    ), 200    

@app.get("/panel/sesion")
def consultar_sesion_panel():

    if not session.get("panel_autorizado", False):
        return jsonify(
            {
                "resultado": "no_autorizado",
                "mensaje": "No hay una sesion activa"
            }
        ), 401

    return jsonify(
        {
            "resultado": "ok",
            "autorizado": True
        }
    ), 200

@app.post("/panel/logout")
def cerrar_sesion_panel():

    session.pop("panel_autorizado", None)

    return jsonify(
        {
            "resultado": "ok",
            "mensaje": "Sesion cerrada correctamente"
        }
    ),200

@app.get("/estado")
def consultar_estado():
    return jsonify(
        {
            "sistema": "MPAZ RFID",
            "estado": "activo",
            "mensaje": "API funcionando correctamente"
        }

    )

@app.get("/alumnos")
def consultar_alumnos_api():
    
    if not session.get("panel_autorizado", False):
        return jsonify(
            {
                "resultado": "no_autorizado",
                "mensaje": "Debes iniciar sesion en el panel"
            }
        ), 401

    termino = request.args.get("buscar", "").strip()

    if termino:
        alumnos = buscar_alumnos(termino)
    else:
        alumnos = obtener_alumnos()

    alumnos_json = []

    for alumno in alumnos:
        alumnos_json.append(
            {
                "id": alumno[0],
                "rut": alumno[1],
                "nombre": alumno[2],
                "curso": alumno[3],
                "uid": alumno[4],
                "estado_tarjeta": alumno[5]
            }
        )

    return jsonify(
        {
            "resultado": "ok",
            "total": len(alumnos),
            "alumnos": alumnos_json
        }
    ), 200    

@app.get("/asistencias")
def consultar_asistencias_api():

    if not session.get("panel_autorizado", False):
        return jsonify(
            {
                "resultado": "no_autorizado",
                "mensaje": "Debes iniciar sesion en el panel"
            }
        ), 401

    registros = obtener_asistencias()

    asistencias_json = []

    for registro in registros:
        asistencias_json.append(
            {
                "id": registro[0],
                "nombre": registro[1],
                "rut": registro[2],
                "curso": registro[3],
                "fecha": registro[4],
                "hora": registro[5],
                "totem": registro[6],
                "evento_id": registro[7],
                "uid": registro[8],
                "resultado": "registrada"
            }
        )

    return jsonify(
        {
            "resultado": "ok",
            "total": len(asistencias_json),
            "asistencias": asistencias_json
        }
    ), 200

@app.get("/asistencias/exportar/<periodo>")
def exportar_asistencias_api(periodo):

    if not session.get("panel_autorizado", False):
        return jsonify(
            {
                "resultado": "no_autorizado",
                "mensaje": "Debes iniciar sesion en el panel"
            }
        ), 401

    if periodo not in (
        "diario",
        "semanal",
        "mensual"
    ):
        return jsonify(
            {
                "resultado": "periodo_invalido",
                "mensaje": "El periodo solicitado no es valido"
            }
        ), 400

    ruta_reporte, cantidad = exportar_asistencias(periodo)

    return send_file(
        ruta_reporte,
        as_attachment=True,
        download_name=ruta_reporte.name,
        mimetype="text/csv"
    )
@app.post("/panel/tarjetas/asignar")
def asignar_tarjeta_panel():

    if not session.get("panel_autorizado", False):
        return jsonify(
            {
                "resultado": "no_autorizado",
                "mensaje": "Debes iniciar sesion en el panel"
            }
        ), 401

    datos = request.get_json(silent=True)

    if not datos:
        return jsonify(
            {
                "resultado": "solicitud_invalida",
                "mensaje": "Debes enviar los datos en formato JSON"
            }
        ), 400

    rut = datos.get("rut", "")
    uid = datos.get("uid", "")

    if not isinstance(rut, str) or not isinstance(uid, str):
        return jsonify(
            {
                "resultado": "datos_invalidos",
                "mensaje": "El RUT y la UID deben ser texto"
            }
        ), 400

    rut = rut.strip()
    uid = uid.strip()

    if not rut or not uid:
        return jsonify(
            {
                "resultado": "datos_incompletos",
                "mensaje": "Falta el RUT o la UID de la tarjeta"
            }
        ), 400

    respuesta = asignar_tarjeta_por_rut(rut, uid)

    resultado = respuesta.get("resultado")

    if resultado == "alumno_no_existe":
        return jsonify(respuesta), 404

    if resultado in (
        "ya_tiene_tarjeta",
        "uid_repetido"
    ):
        return jsonify(respuesta), 409

    if resultado == "asignada":
        return jsonify(respuesta), 200

    return jsonify(
        {
            "resultado": "error_interno",
            "mensaje": "No se pudo procesar la asignacion"
        }
    ), 500    

@app.post("/panel/tarjetas/bloquear")
def bloquear_tarjeta_panel():

    if not session.get("panel_autorizado", False):
        return jsonify(
            {
                "resultado": "no_autorizado",
                "mensaje": "Debes iniciar sesion en el panel"
            }
        ), 401

    datos = request.get_json(silent=True)

    if not datos:
        return jsonify(
            {
                "resultado": "solicitud_invalida",
                "mensaje": "Debes enviar los datos en formato JSON"
            }
        ), 400

    uid = datos.get("uid", "")

    if not isinstance(uid, str):
        return jsonify(
            {
                "resultado": "datos_invalidos",
                "mensaje": "La UID debe ser texto"
            }
        ), 400

    uid = uid.strip()

    if not uid:
        return jsonify(
            {
                "resultado": "datos_incompletos",
                "mensaje": "Falta la UID de la tarjeta"
            }
        ), 400

    bloqueada = bloquear_tarjeta(uid)

    if not bloqueada:
        return jsonify(
            {
                "resultado": "no_bloqueada",
                "mensaje": "La tarjeta no existe o ya estaba bloqueada"
            }
        ), 404

    return jsonify(
        {
            "resultado": "bloqueada",
            "uid": uid.upper(),
            "mensaje": "Tarjeta bloqueada correctamente"
        }
    ), 200

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