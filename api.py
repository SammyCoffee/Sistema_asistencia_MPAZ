import os
import secrets

from flask import (Flask,jsonify,request,session,redirect,send_file)
from consultar_alumnos import obtener_alumnos, buscar_alumnos
from procesar_lectura_totem import procesar_lectura_totem
from base_datos import (
    asignar_tarjeta_por_rut,
    bloquear_tarjeta,
    obtener_totems,
    guardar_totem,
    cambiar_estado_totem,
    registrar_alumno,
    editar_alumno,
    cambiar_estado_alumno,
    obtener_tarjetas,
    registrar_tarjeta,
    vincular_tarjeta,
    marcar_tarjeta_extraviada
)
from consultar_asistencia import (
    obtener_asistencias,
    obtener_inasistencias,
    obtener_atrasos
)
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
    
@app.get("/panel/totems")
def consultar_totems_panel():

    if not session.get("panel_autorizado", False):
        return jsonify(
            {
                "resultado": "no_autorizado",
                "mensaje": "Debes iniciar sesion en el panel"
            }
        ), 401

    totems = obtener_totems()

    return jsonify(
        {
            "resultado": "ok",
            "total": len(totems),
            "totems": totems
        }
    ), 200

@app.post("/panel/totems/registrar")
def registrar_totem_panel():

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

    codigo = datos.get("codigo", "")
    nombre = datos.get("nombre", "")
    ubicacion = datos.get("ubicacion", "")

    if (
        not isinstance(codigo, str)
        or not isinstance(nombre, str)
        or not isinstance(ubicacion, str)
    ):
        return jsonify(
            {
                "resultado": "datos_invalidos",
                "mensaje": "Los datos del totem deben ser texto"
            }
        ), 400

    codigo = codigo.strip()
    nombre = nombre.strip()
    ubicacion = ubicacion.strip()

    if not codigo or not nombre or not ubicacion:
        return jsonify(
            {
                "resultado": "datos_incompletos",
                "mensaje": "Codigo, nombre y ubicacion son obligatorios"
            }
        ), 400

    respuesta = guardar_totem(
        codigo,
        nombre,
        ubicacion
    )

    if respuesta["resultado"] == "codigo_repetido":
        return jsonify(respuesta), 409

    if respuesta["resultado"] == "registrado":
        return jsonify(respuesta), 201

    return jsonify(
        {
            "resultado": "error_interno",
            "mensaje": "No se pudo registrar el totem"
        }
    ), 500


@app.post("/panel/totems/estado")
def cambiar_estado_totem_panel():

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

    codigo = datos.get("codigo", "")
    estado = datos.get("estado", "")

    if not isinstance(codigo, str) or not isinstance(estado, str):
        return jsonify(
            {
                "resultado": "datos_invalidos",
                "mensaje": "El codigo y el estado deben ser texto"
            }
        ), 400

    codigo = codigo.strip()
    estado = estado.strip()

    if not codigo or not estado:
        return jsonify(
            {
                "resultado": "datos_incompletos",
                "mensaje": "Falta el codigo o el estado"
            }
        ), 400

    respuesta = cambiar_estado_totem(
        codigo,
        estado
    )

    resultado = respuesta.get("resultado")

    if resultado == "estado_invalido":
        return jsonify(respuesta), 400

    if resultado == "no_existe":
        return jsonify(respuesta), 404

    if resultado == "actualizado":
        return jsonify(respuesta), 200

    return jsonify(
        {
            "resultado": "error_interno",
            "mensaje": "No se pudo cambiar el estado del totem"
        }
    ), 500

@app.post("/panel/alumnos/registrar")
def registrar_alumno_panel():

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
    nombre = datos.get("nombre", "")
    curso = datos.get("curso", "")

    if (
        not isinstance(rut, str)
        or not isinstance(nombre, str)
        or not isinstance(curso, str)
    ):
        return jsonify(
            {
                "resultado": "datos_invalidos",
                "mensaje": "RUT, nombre y curso deben ser texto"
            }
        ), 400

    rut = rut.strip()
    nombre = nombre.strip()
    curso = curso.strip()

    if not rut or not nombre or not curso:
        return jsonify(
            {
                "resultado": "datos_incompletos",
                "mensaje": "RUT, nombre y curso son obligatorios"
            }
        ), 400

    respuesta = registrar_alumno(
        rut,
        nombre,
        curso
    )

    resultado = respuesta.get("resultado")

    if resultado == "rut_repetido":
        return jsonify(respuesta), 409

    if resultado == "datos_incompletos":
        return jsonify(respuesta), 400

    if resultado == "curso_invalido":
        return jsonify(respuesta), 400

    if resultado == "rut_invalido":
        return jsonify(respuesta), 400

    if resultado == "nombre_invalido":
        return jsonify(respuesta), 400

    if resultado == "registrado":
        return jsonify(respuesta), 201

    return jsonify(
        {
            "resultado": "error_interno",
            "mensaje": "No se pudo registrar el alumno"
        }
    ), 500
@app.post("/panel/alumnos/editar")
def editar_alumno_panel():

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

    alumno_id = datos.get("id")
    rut = datos.get("rut", "")
    nombre = datos.get("nombre", "")
    curso = datos.get("curso", "")

    if not isinstance(alumno_id, int):
        return jsonify(
            {
                "resultado": "datos_invalidos",
                "mensaje": "El ID del alumno debe ser numerico"
            }
        ), 400

    if (
        not isinstance(rut, str)
        or not isinstance(nombre, str)
        or not isinstance(curso, str)
    ):
        return jsonify(
            {
                "resultado": "datos_invalidos",
                "mensaje": "RUT, nombre y curso deben ser texto"
            }
        ), 400

    rut = rut.strip()
    nombre = nombre.strip()
    curso = curso.strip()

    if not rut or not nombre or not curso:
        return jsonify(
            {
                "resultado": "datos_incompletos",
                "mensaje": "RUT, nombre y curso son obligatorios"
            }
        ), 400

    respuesta = editar_alumno(
        alumno_id,
        rut,
        nombre,
        curso
    )

    resultado = respuesta.get("resultado")

    if resultado == "alumno_no_existe":
        return jsonify(respuesta), 404

    if resultado == "rut_repetido":
        return jsonify(respuesta), 409

    if resultado == "datos_incompletos":
        return jsonify(respuesta), 400

    if resultado == "curso_invalido":
        return jsonify(respuesta), 400

    if resultado == "rut_invalido":
        return jsonify(respuesta), 400

    if resultado == "nombre_invalido":
        return jsonify(respuesta), 400

    if resultado == "actualizado":
        return jsonify(respuesta), 200

    return jsonify(
        {
            "resultado": "error_interno",
            "mensaje": "No se pudo editar el alumno"
        }
    ), 500
@app.post("/panel/alumnos/estado")
def cambiar_estado_alumno_panel():

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

    alumno_id = datos.get("id")
    estado = datos.get("estado", "")

    if not isinstance(alumno_id, int):
        return jsonify(
            {
                "resultado": "datos_invalidos",
                "mensaje": "El ID del alumno debe ser numerico"
            }
        ), 400

    if not isinstance(estado, str):
        return jsonify(
            {
                "resultado": "datos_invalidos",
                "mensaje": "El estado debe ser texto"
            }
        ), 400

    estado = estado.strip().lower()

    if not estado:
        return jsonify(
            {
                "resultado": "datos_incompletos",
                "mensaje": "Falta el estado del alumno"
            }
        ), 400

    respuesta = cambiar_estado_alumno(
        alumno_id,
        estado
    )

    resultado = respuesta.get("resultado")

    if resultado == "alumno_no_existe":
        return jsonify(respuesta), 404

    if resultado == "estado_invalido":
        return jsonify(respuesta), 400

    if resultado == "actualizado":
        return jsonify(respuesta), 200

    return jsonify(
        {
            "resultado": "error_interno",
            "mensaje": "No se pudo cambiar el estado del alumno"
        }
    ), 500
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
            "estado_alumno": alumno[4],
            "fecha_baja": alumno[5],
            "uid": alumno[6],
            "estado_tarjeta": alumno[7]
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
                "hora_entrada": registro[5],
                "hora_salida": registro[6],
                "tipo_salida": registro[7],
                "totem_entrada": registro[8],
                "totem_salida": registro[9],
                "uid": registro[10]
            }
        )

    return jsonify(
        {
            "resultado": "ok",
            "total": len(asistencias_json),
            "asistencias": asistencias_json
        }
    ), 200


@app.get("/inasistencias")
def consultar_inasistencias_api():

    if not session.get("panel_autorizado", False):
        return jsonify(
            {
                "resultado": "no_autorizado",
                "mensaje": "Debes iniciar sesion en el panel"
            }
        ), 401

    periodo = request.args.get(
        "periodo",
        "mensual"
    ).strip().lower()

    fecha_referencia = request.args.get(
        "fecha",
        ""
    ).strip()

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

    if not fecha_referencia:
        fecha_referencia = None

    try:
        registros = obtener_inasistencias(
            periodo,
            fecha_referencia
        )

    except ValueError:
        return jsonify(
            {
                "resultado": "fecha_invalida",
                "mensaje": "La fecha debe usar formato YYYY-MM-DD"
            }
        ), 400

    inasistencias_json = []

    for registro in registros:
        inasistencias_json.append(
            {
                "id": registro[0],
                "nombre": registro[1],
                "curso": registro[2],
                "inasistencias": registro[3],
                "jornadas_periodo": registro[4]
            }
        )

    return jsonify(
        {
            "resultado": "ok",
            "periodo": periodo,
            "total": len(inasistencias_json),
            "inasistencias": inasistencias_json
        }
    ), 200


@app.get("/atrasos")
def consultar_atrasos_api():

    if not session.get("panel_autorizado", False):
        return jsonify(
            {
                "resultado": "no_autorizado",
                "mensaje": "Debes iniciar sesion en el panel"
            }
        ), 401

    periodo = request.args.get(
        "periodo",
        "diario"
    ).strip().lower()

    fecha_referencia = request.args.get(
        "fecha",
        ""
    ).strip()

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

    if not fecha_referencia:
        fecha_referencia = None

    try:
        registros = obtener_atrasos(
            periodo,
            fecha_referencia
        )

    except ValueError:
        return jsonify(
            {
                "resultado": "fecha_invalida",
                "mensaje": "La fecha debe usar formato YYYY-MM-DD"
            }
        ), 400

    atrasos_json = []

    for registro in registros:
        atrasos_json.append(
            {
                "id": registro[0],
                "nombre": registro[1],
                "curso": registro[2],
                "fecha": registro[3],
                "hora_entrada": registro[4],
                "minutos_atraso": registro[5]
            }
        )

    return jsonify(
        {
            "resultado": "ok",
            "periodo": periodo,
            "total": len(atrasos_json),
            "atrasos": atrasos_json
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
        "mensual",
        "anual"
    ):
        return jsonify(
            {
                "resultado": "periodo_invalido",
                "mensaje": "El periodo solicitado no es valido"
            }
        ), 400
    
    curso = request.args.get("curso", "").strip()

    if not curso:
         curso = None
    
    ruta_reporte, cantidad = exportar_asistencias(
	periodo,
	curso=curso
	)

    return send_file(
        ruta_reporte,
        as_attachment=True,
        download_name=ruta_reporte.name,
        mimetype="text/csv"
    )
@app.get("/panel/tarjetas")
def consultar_tarjetas_panel():

    if not session.get("panel_autorizado", False):
        return jsonify(
            {
                "resultado": "no_autorizado",
                "mensaje": "Debes iniciar sesion en el panel"
            }
        ), 401

    tarjetas = obtener_tarjetas()

    return jsonify(
        {
            "resultado": "ok",
            "total": len(tarjetas),
            "tarjetas": tarjetas
        }
    ), 200
@app.post("/panel/tarjetas/registrar")
def registrar_tarjeta_panel():

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

    respuesta = registrar_tarjeta(
        uid
    )

    resultado = respuesta.get("resultado")

    if resultado == "uid_repetido":
        return jsonify(respuesta), 409

    if resultado == "datos_incompletos":
        return jsonify(respuesta), 400

    if resultado == "registrada":
        return jsonify(respuesta), 201

    return jsonify(
        {
            "resultado": "error_interno",
            "mensaje": "No se pudo registrar la tarjeta"
        }
    ), 500
@app.post("/panel/tarjetas/vincular")
def vincular_tarjeta_panel():

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

    alumno_id = datos.get("alumno_id")
    uid = datos.get("uid", "")

    if not isinstance(alumno_id, int):
        return jsonify(
            {
                "resultado": "datos_invalidos",
                "mensaje": "El ID del alumno debe ser numerico"
            }
        ), 400

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

    respuesta = vincular_tarjeta(
        alumno_id,
        uid
    )

    resultado = respuesta.get("resultado")

    if resultado == "alumno_no_existe":
        return jsonify(respuesta), 404

    if resultado == "tarjeta_no_existe":
        return jsonify(respuesta), 404

    if resultado == "alumno_inactivo":
        return jsonify(respuesta), 409

    if resultado in (
        "ya_tiene_tarjeta",
        "tarjeta_no_disponible"
    ):
        return jsonify(respuesta), 409

    if resultado == "vinculada":
        return jsonify(respuesta), 200

    return jsonify(
        {
            "resultado": "error_interno",
            "mensaje": "No se pudo vincular la tarjeta"
        }
    ), 500
@app.post("/panel/tarjetas/extraviada")
def marcar_tarjeta_extraviada_panel():

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

    respuesta = marcar_tarjeta_extraviada(
        uid
    )

    resultado = respuesta.get("resultado")

    if resultado == "tarjeta_no_existe":
        return jsonify(respuesta), 404

    if resultado == "ya_extraviada":
        return jsonify(respuesta), 409

    if resultado == "extraviada":
        return jsonify(respuesta), 200

    return jsonify(
        {
            "resultado": "error_interno",
            "mensaje": "No se pudo marcar la tarjeta como extraviada"
        }
    ), 500
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
