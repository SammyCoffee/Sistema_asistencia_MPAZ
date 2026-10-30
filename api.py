from base_datos import obtener_detalle_sesion_clase_profesor
import os
import secrets

from flask import (Flask,jsonify,request,session,redirect,send_file)
from consultar_alumnos import obtener_alumnos, buscar_alumnos
from procesar_lectura_totem import procesar_lectura_totem
from base_datos import (
    autenticar_usuario,
    obtener_asignaciones_profesor,
    obtener_alumnos_curso_profesor,
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
from base_datos import obtener_sesiones_clase_profesor
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
def mostrar_inicio():
    return app.send_static_file("inicio.html")


@app.get("/seguimiento.html")
def mostrar_seguimiento_administrativo():

    from seguimiento_sesiones import operador_actual

    operador = operador_actual()

    permiso_panel = session.get("panel_autorizado") is True

    permiso_direccion = (
        operador is not None
        and operador["rol"] == "direccion"
    )

    if not (permiso_panel or permiso_direccion):
        return redirect("/login.html")

    respuesta = app.send_static_file("seguimiento.html")
    respuesta.headers["Cache-Control"] = "no-store"

    return respuesta


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


# MPAZ-CSRF-687
# Proteccion centralizada de operaciones administrativas.
# No interviene en /lectura ni en el portal docente.

RUTAS_ADMIN_CSRF = frozenset({
    "/panel/totems/registrar",
    "/panel/totems/estado",
    "/panel/alumnos/registrar",
    "/panel/alumnos/editar",
    "/panel/alumnos/estado",
    "/panel/tarjetas/registrar",
    "/panel/tarjetas/vincular",
    "/panel/tarjetas/extraviada",
    "/panel/tarjetas/asignar",
    "/panel/tarjetas/bloquear",
    "/panel/tarjetas/desbloquear",
})


@app.before_request
def proteger_escrituras_administrativas_csrf():

    if (
        request.method != "POST"
        or request.path not in RUTAS_ADMIN_CSRF
    ):
        return None

    if not session.get("panel_autorizado", False):
        return jsonify({
            "resultado": "no_autorizado",
            "mensaje": "Sesion administrativa requerida"
        }), 401

    token_sesion = session.get("panel_csrf")
    token_recibido = request.headers.get("X-CSRF-Token")

    if (
        not isinstance(token_sesion, str)
        or not isinstance(token_recibido, str)
        or not token_sesion
        or not token_recibido
        or not secrets.compare_digest(
            token_sesion, token_recibido
        )
    ):
        return jsonify({
            "resultado": "csrf_invalido",
            "mensaje": "Token CSRF ausente o invalido"
        }), 403

    return None


@app.get("/panel/csrf-token")
def obtener_token_administrativo():

    if not session.get("panel_autorizado", False):
        return jsonify({
            "resultado": "no_autorizado"
        }), 401

    token = session.get("panel_csrf")

    if not isinstance(token, str) or not token:
        token = secrets.token_urlsafe(32)
        session["panel_csrf"] = token

    respuesta = jsonify({
        "resultado": "ok",
        "csrf_token": token
    })

    respuesta.headers["Cache-Control"] = "no-store"

    return respuesta, 200


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

    # Evitar heredar identidades individuales anteriores.
    session.clear()

    session["panel_autorizado"] = True
    session["panel_csrf"] = secrets.token_urlsafe(32)

    return jsonify(
        {
            "resultado": "ok",
            "mensaje": "Sesion iniciada correctamente"
        }
    ), 200    

@app.post("/panel/login-individual")
def iniciar_sesion_panel_individual():

    from seguimiento_identidad import autenticar_operador

    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "resultado": "datos_invalidos"
        }), 400

    usuario = datos.get("usuario")
    password = datos.get("password")

    if (
        not isinstance(usuario, str)
        or not isinstance(password, str)
        or len(usuario) > 40
        or len(password) > 128
    ):
        return jsonify({
            "resultado": "datos_invalidos"
        }), 400

    resultado = autenticar_operador(usuario, password)

    if (
        resultado.get("resultado") != "autenticado"
        or resultado.get("rol") not in (
            "administracion", "direccion"
        )
    ):
        return jsonify({
            "resultado": "credenciales_invalidas"
        }), 401

    # Crear una sesion nueva con identidad individual.
    session.clear()

    if resultado["rol"] == "administracion":
        session["panel_autorizado"] = True
        session["panel_csrf"] = secrets.token_urlsafe(32)

    session["seguimiento_operador_id"] = resultado["id"]
    session["seguimiento_csrf"] = secrets.token_urlsafe(32)

    return jsonify({
        "resultado": "ok",
        "mensaje": "Sesion individual iniciada",
        "operador": {
            "nombre": resultado["nombre"],
            "rol": resultado["rol"]
        }
    }), 200


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
    session.pop("panel_csrf", None)

    # Cerrar también la identidad individual de seguimiento.
    session.pop("seguimiento_operador_id", None)
    session.pop("seguimiento_csrf", None)

    return jsonify(
        {
            "resultado": "ok",
            "mensaje": "Sesion cerrada correctamente"
        }
    ),200



def validar_csrf_profesor():
    """
    Valida el token CSRF enviado por un profesor autenticado.

    Debe utilizarse en las rutas docentes que modifican datos.
    """

    token_sesion = session.get("profesor_csrf")
    token_peticion = request.headers.get("X-CSRF-Token")

    if (
        not isinstance(token_sesion, str)
        or not isinstance(token_peticion, str)
        or not token_sesion
        or not token_peticion
    ):
        return False

    return secrets.compare_digest(
        token_sesion,
        token_peticion
    )


@app.post("/profesor/login")
def iniciar_sesion_profesor():
    datos = request.get_json(silent=True) or {}

    if not isinstance(datos, dict):
        return jsonify({
            "resultado": "datos_invalidos"
        }), 400

    usuario = datos.get("usuario", "")
    password = datos.get("password", "")

    resultado = autenticar_usuario(usuario, password)

    if resultado["resultado"] == "datos_invalidos":
        return jsonify({
            "resultado": "datos_invalidos"
        }), 400

    if resultado["resultado"] == "datos_incompletos":
        return jsonify({
            "resultado": "datos_incompletos"
        }), 400

    if resultado["resultado"] != "autenticado":
        return jsonify({
            "resultado": "credenciales_invalidas"
        }), 401

    if resultado["rol"] != "profesor":
        return jsonify({
            "resultado": "acceso_denegado"
        }), 403

    session.clear()

    session["profesor_id"] = resultado["id"]
    session["profesor_usuario"] = resultado["usuario"]
    session["profesor_nombre"] = resultado["nombre_completo"]
    session["profesor_rol"] = resultado["rol"]
    session["profesor_csrf"] = secrets.token_urlsafe(32)

    return jsonify({
        "resultado": "ok",
        "mensaje": "Sesion docente iniciada correctamente",
        "profesor": {
            "id": resultado["id"],
            "nombre": resultado["nombre_completo"],
            "usuario": resultado["usuario"],
            "rol": resultado["rol"]
        }
    }), 200


@app.get("/profesor/sesion")
def consultar_sesion_profesor():

    profesor_id = session.get("profesor_id")
    profesor_rol = session.get("profesor_rol")

    if not profesor_id or profesor_rol != "profesor":
        return jsonify({
            "resultado": "no_autorizado",
            "mensaje": "No existe una sesion docente activa"
        }), 401

    return jsonify({
        "resultado": "ok",
        "autorizado": True,
        "csrf_token": session.get("profesor_csrf"),
        "profesor": {
            "id": profesor_id,
            "usuario": session.get("profesor_usuario"),
            "nombre": session.get("profesor_nombre"),
            "rol": profesor_rol
        }
    }), 200


@app.post("/profesor/logout")
def cerrar_sesion_profesor():

    if (
        not session.get("profesor_id")
        or session.get("profesor_rol") != "profesor"
    ):
        return jsonify({
            "resultado": "no_autorizado",
            "mensaje": "No existe una sesion docente activa"
        }), 401

    session.pop("profesor_id", None)
    session.pop("profesor_usuario", None)
    session.pop("profesor_nombre", None)
    session.pop("profesor_rol", None)
    session.pop("profesor_csrf", None)

    return jsonify({
        "resultado": "ok",
        "mensaje": "Sesion docente cerrada correctamente"
    }), 200



@app.post("/profesor/sesiones")
def crear_sesion_clase_api():
    """
    Crea una sesión de asistencia docente para una
    asignación autorizada del profesor autenticado.
    """

    from base_datos import crear_sesion_clase_profesor

    profesor_id = session.get("profesor_id")
    profesor_rol = session.get("profesor_rol")

    if (
        not isinstance(profesor_id, int)
        or isinstance(profesor_id, bool)
        or profesor_id <= 0
        or profesor_rol != "profesor"
    ):
        return jsonify({
            "resultado": "no_autorizado",
            "mensaje": "Debe iniciar sesion como profesor"
        }), 401

    if not validar_csrf_profesor():
        return jsonify({
            "resultado": "csrf_invalido",
            "mensaje": "Token de seguridad invalido o ausente"
        }), 403

    if not request.is_json:
        return jsonify({
            "resultado": "datos_invalidos",
            "mensaje": "Debe enviar datos JSON"
        }), 400

    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "resultado": "datos_invalidos",
            "mensaje": "El contenido JSON no es valido"
        }), 400

    asignacion_id = datos.get("asignacion_id")
    fecha = datos.get("fecha")
    hora_inicio = datos.get("hora_inicio")

    resultado = crear_sesion_clase_profesor(
        profesor_id,
        asignacion_id,
        fecha,
        hora_inicio
    )

    codigo = resultado.get("resultado")

    if codigo == "sesion_creada":
        return jsonify(resultado), 201

    if codigo == "sesion_existente":
        return jsonify(resultado), 200

    if codigo in (
        "profesor_invalido",
        "asignacion_invalida",
        "fecha_invalida",
        "hora_invalida"
    ):
        return jsonify(resultado), 400

    if codigo in (
        "asignacion_no_autorizada",
        "profesor_no_autorizado"
    ):
        return jsonify({
            "resultado": "acceso_denegado",
            "mensaje": "No tiene autorizacion para esta asignacion"
        }), 403

    return jsonify({
        "resultado": "error_creacion",
        "mensaje": "No fue posible crear la sesion"
    }), 500



@app.post("/profesor/sesiones/<int:sesion_id>/asistencia")
def registrar_asistencia_clase_api(sesion_id):
    """
    Registra o corrige la asistencia de un estudiante
    en una sesión docente que permanezca en borrador.
    """

    from base_datos import registrar_asistencia_clase_profesor

    profesor_id = session.get("profesor_id")
    profesor_rol = session.get("profesor_rol")

    if (
        not isinstance(profesor_id, int)
        or isinstance(profesor_id, bool)
        or profesor_id <= 0
        or profesor_rol != "profesor"
    ):
        return jsonify({
            "resultado": "no_autorizado",
            "mensaje": "Debe iniciar sesion como profesor"
        }), 401

    if not validar_csrf_profesor():
        return jsonify({
            "resultado": "csrf_invalido",
            "mensaje": "Token de seguridad invalido o ausente"
        }), 403

    if not request.is_json:
        return jsonify({
            "resultado": "datos_invalidos",
            "mensaje": "Debe enviar datos JSON"
        }), 400

    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "resultado": "datos_invalidos",
            "mensaje": "El contenido JSON no es valido"
        }), 400

    alumno_id = datos.get("alumno_id")
    estado = datos.get("estado")
    observacion = datos.get("observacion")

    if (
        observacion is not None
        and (
            not isinstance(observacion, str)
            or len(observacion) > 500
        )
    ):
        return jsonify({
            "resultado": "observacion_invalida",
            "mensaje": "La observacion debe ser texto de maximo 500 caracteres"
        }), 400

    resultado = registrar_asistencia_clase_profesor(
        profesor_id,
        sesion_id,
        alumno_id,
        estado,
        observacion
    )

    codigo = resultado.get("resultado")

    if codigo == "asistencia_guardada":
        return jsonify(resultado), 200

    if codigo in (
        "profesor_invalido",
        "sesion_invalida",
        "alumno_invalido",
        "estado_invalido",
        "observacion_invalida"
    ):
        return jsonify(resultado), 400

    if codigo in (
        "sesion_no_autorizada",
        "alumno_no_autorizado",
        "profesor_no_autorizado"
    ):
        return jsonify({
            "resultado": "acceso_denegado",
            "mensaje": "No tiene autorizacion para esta operacion"
        }), 403

    if codigo == "sesion_no_editable":
        return jsonify({
            "resultado": "sesion_no_editable",
            "mensaje": "La sesion ya no permite modificaciones"
        }), 409

    if codigo == "error_integridad":
        return jsonify({
            "resultado": "error_integridad",
            "mensaje": "No fue posible guardar la asistencia"
        }), 409

    return jsonify({
        "resultado": "error_registro",
        "mensaje": "No fue posible registrar la asistencia"
    }), 500



@app.post("/profesor/sesiones/<int:sesion_id>/confirmar")
def confirmar_sesion_clase_api(sesion_id):
    """
    Confirma una sesión de asistencia docente cuando
    todos los estudiantes activos están verificados.
    """

    from base_datos import confirmar_sesion_clase_profesor

    profesor_id = session.get("profesor_id")
    profesor_rol = session.get("profesor_rol")

    if (
        not isinstance(profesor_id, int)
        or isinstance(profesor_id, bool)
        or profesor_id <= 0
        or profesor_rol != "profesor"
    ):
        return jsonify({
            "resultado": "no_autorizado",
            "mensaje": "Debe iniciar sesion como profesor"
        }), 401

    if not validar_csrf_profesor():
        return jsonify({
            "resultado": "csrf_invalido",
            "mensaje": "Token de seguridad invalido o ausente"
        }), 403

    resultado = confirmar_sesion_clase_profesor(
        profesor_id,
        sesion_id
    )

    codigo = resultado.get("resultado")

    if codigo == "sesion_confirmada":
        return jsonify(resultado), 200

    if codigo in (
        "profesor_invalido",
        "sesion_invalida"
    ):
        return jsonify(resultado), 400

    if codigo in (
        "sesion_no_autorizada",
        "profesor_no_autorizado"
    ):
        return jsonify({
            "resultado": "acceso_denegado",
            "mensaje": "No tiene autorizacion para esta sesion"
        }), 403

    if codigo == "asistencia_incompleta":
        return jsonify(resultado), 409

    if codigo in (
        "sesion_no_editable",
        "sesion_ya_confirmada",
        "sesion_no_confirmable",
        "curso_sin_alumnos"
    ):
        return jsonify(resultado), 409

    return jsonify({
        "resultado": "error_confirmacion",
        "mensaje": "No fue posible confirmar la sesion"
    }), 500



@app.get("/profesor/asignaciones/<int:asignacion_id>/sesiones")
def consultar_sesiones_clase_api(asignacion_id):
    """
    Consulta sesiones de una asignación docente autorizada.
    """

    profesor_id = session.get("profesor_id")
    profesor_rol = session.get("profesor_rol")

    if profesor_id is None or profesor_rol != "profesor":
        return jsonify({
            "resultado": "no_autenticado",
            "mensaje": "Debe iniciar sesión como profesor"
        }), 401

    if asignacion_id <= 0:
        return jsonify({
            "resultado": "asignacion_invalida"
        }), 400

    resultado = obtener_sesiones_clase_profesor(
        profesor_id,
        asignacion_id
    )

    codigo_resultado = resultado.get("resultado")

    if codigo_resultado == "ok":
        return jsonify(resultado), 200

    if codigo_resultado in (
        "profesor_invalido",
        "asignacion_invalida"
    ):
        return jsonify(resultado), 400

    if codigo_resultado in (
        "profesor_no_autorizado",
        "profesor_inactivo",
        "asignacion_no_autorizada"
    ):
        return jsonify(resultado), 403

    return jsonify({
        "resultado": "error_consulta",
        "mensaje": "No fue posible consultar las sesiones"
    }), 500



@app.get("/profesor/sesiones/<int:sesion_id>")
def consultar_detalle_sesion_clase_api(sesion_id):
    """
    Consulta el detalle de una sesión docente autorizada.
    No modifica datos RFID ni registros de asistencia.
    """

    profesor_id = session.get("profesor_id")
    profesor_rol = session.get("profesor_rol")

    if profesor_id is None or profesor_rol != "profesor":
        return jsonify({
            "resultado": "no_autenticado",
            "mensaje": "Debe iniciar sesión como profesor"
        }), 401

    if sesion_id <= 0:
        return jsonify({
            "resultado": "sesion_invalido"
        }), 400

    resultado = obtener_detalle_sesion_clase_profesor(
        profesor_id,
        sesion_id
    )

    codigo_resultado = resultado.get("resultado")

    if codigo_resultado == "ok":
        return jsonify(resultado), 200

    if codigo_resultado in (
        "profesor_invalido",
        "sesion_invalido"
    ):
        return jsonify(resultado), 400

    if codigo_resultado == "sesion_no_autorizada":
        return jsonify(resultado), 403

    return jsonify({
        "resultado": "error_consulta",
        "mensaje": "No fue posible consultar la sesión"
    }), 500


@app.get("/profesor/asignaciones")
def consultar_asignaciones_profesor():

    profesor_id = session.get("profesor_id")
    profesor_rol = session.get("profesor_rol")

    if not profesor_id or profesor_rol != "profesor":
        return jsonify({
            "resultado": "no_autorizado",
            "mensaje": "Debe iniciar sesion como profesor"
        }), 401

    resultado = obtener_asignaciones_profesor(profesor_id)

    if resultado["resultado"] != "ok":
        return jsonify({
            "resultado": "acceso_denegado",
            "mensaje": "Profesor no autorizado o inactivo"
        }), 403

    return jsonify(resultado), 200


@app.get("/profesor/cursos/<curso>/alumnos")
def consultar_alumnos_curso_profesor(curso):

    profesor_id = session.get("profesor_id")
    profesor_rol = session.get("profesor_rol")

    if (
        not isinstance(profesor_id, int)
        or isinstance(profesor_id, bool)
        or profesor_id <= 0
        or profesor_rol != "profesor"
    ):
        return jsonify({
            "resultado": "no_autorizado",
            "mensaje": "Debe iniciar sesion como profesor"
        }), 401

    if not curso.strip() or len(curso.strip()) > 20:
        return jsonify({
            "resultado": "curso_invalido",
            "mensaje": "El curso solicitado no es valido"
        }), 400

    resultado = obtener_alumnos_curso_profesor(
        profesor_id,
        curso
    )

    if resultado["resultado"] == "ok":
        return jsonify(resultado), 200

    if resultado["resultado"] == "curso_invalido":
        return jsonify({
            "resultado": "curso_invalido",
            "mensaje": "El curso solicitado no es valido"
        }), 400

    return jsonify({
        "resultado": "acceso_denegado",
        "mensaje": "No tiene autorizacion para consultar este curso"
    }), 403


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

@app.post("/panel/tarjetas/desbloquear")
def desbloquear_tarjeta_panel():

    if not session.get("panel_autorizado", False):
        return jsonify({
            "resultado": "no_autorizado",
            "mensaje": "Debe iniciar sesion como administrador"
        }), 401

    if not request.is_json:
        return jsonify({
            "resultado": "datos_invalidos"
        }), 400

    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "resultado": "datos_invalidos"
        }), 400

    uid = datos.get("uid")

    if not isinstance(uid, str) or not uid.strip():
        return jsonify({
            "resultado": "uid_invalido"
        }), 400

    from base_datos import activar_tarjeta

    resultado = activar_tarjeta(uid)

    if resultado == "activada":
        return jsonify({
            "resultado": "activada",
            "mensaje": "Tarjeta desbloqueada correctamente"
        }), 200

    if resultado == "tarjeta_no_existe":
        return jsonify({"resultado": resultado}), 404

    if resultado in (
        "tarjeta_no_bloqueada",
        "alumno_no_autorizado",
        "otra_tarjeta_activa",
        "no_actualizada"
    ):
        return jsonify({"resultado": resultado}), 409

    return jsonify({"resultado": "uid_invalido"}), 400


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



@app.route(
    "/profesor/cursos/<curso>/asistencia",
    methods=["GET"]
)
def consultar_asistencia_curso_profesor(curso):
    """
    Permite consultar la asistencia RFID de un curso
    únicamente a profesores autorizados.
    """
    from base_datos import obtener_asistencia_curso_profesor

    profesor_id = session.get("profesor_id")
    profesor_rol = session.get("profesor_rol")

    if (
        not isinstance(profesor_id, int)
        or isinstance(profesor_id, bool)
        or profesor_id <= 0
        or profesor_rol != "profesor"
    ):
        return jsonify({
            "resultado": "no_autorizado",
            "mensaje": "Debe iniciar sesion como profesor"
        }), 401

    if not curso.strip() or len(curso.strip()) > 20:
        return jsonify({
            "resultado": "curso_invalido",
            "mensaje": "El curso solicitado no es valido"
        }), 400

    fecha = request.args.get("fecha")

    if not fecha:
        return jsonify({
            "resultado": "fecha_invalida",
            "mensaje": "Debe indicar una fecha valida"
        }), 400

    resultado = obtener_asistencia_curso_profesor(
        profesor_id,
        curso,
        fecha
    )

    if resultado["resultado"] == "ok":
        return jsonify(resultado), 200

    if resultado["resultado"] in (
        "curso_invalido",
        "fecha_invalida"
    ):
        return jsonify({
            "resultado": resultado["resultado"],
            "mensaje": "Los parametros solicitados no son validos"
        }), 400

    return jsonify({
        "resultado": "acceso_denegado",
        "mensaje": "No tiene autorizacion para consultar este curso"
    }), 403


@app.get("/panel/calendario/jornada")
def consultar_jornada_escolar_panel():
    """
    Consulta administrativa de una jornada escolar.

    No crea ni modifica registros.
    """

    import sqlite3

    from calendario_escolar import (
        resolver_jornada_escolar,
        validar_fecha_escolar,
        validar_curso_escolar
    )

    from base_datos import obtener_conexion

    if not session.get("panel_autorizado", False):
        return jsonify({
            "resultado": "no_autorizado",
            "mensaje": "Debe iniciar sesion como administrador"
        }), 401

    fecha = request.args.get("fecha", "")
    curso = request.args.get("curso", "")

    try:
        fecha = validar_fecha_escolar(fecha)
        curso = validar_curso_escolar(curso)

    except ValueError as error:
        codigo = str(error)

        return jsonify({
            "resultado": codigo,
            "mensaje": (
                "La fecha o el curso solicitado no es valido"
            )
        }), 400

    try:
        conexion = obtener_conexion()

        try:
            jornada = resolver_jornada_escolar(
                conexion,
                fecha,
                curso
            )

        finally:
            conexion.close()

    except sqlite3.OperationalError as error:

        if "no such table: calendario_jornadas" in str(error):
            return jsonify({
                "resultado": "calendario_no_preparado",
                "mensaje": (
                    "La estructura del calendario escolar "
                    "todavia no esta instalada"
                )
            }), 503

        raise

    return jsonify({
        "resultado": "ok",
        "jornada": jornada
    }), 200



# ==========================================
# MPAZ - ADMINISTRACION DEL CALENDARIO
# ==========================================

@app.get("/panel/calendario/token")
def obtener_token_calendario_panel():

    if not session.get("panel_autorizado", False):
        return jsonify({
            "resultado": "no_autorizado"
        }), 401

    session["calendario_csrf"] = secrets.token_urlsafe(32)

    respuesta = jsonify({
        "resultado": "ok",
        "csrf_token": session["calendario_csrf"]
    })

    respuesta.headers["Cache-Control"] = "no-store"
    return respuesta, 200


def procesar_jornada_calendario_panel(accion):

    import sqlite3

    from base_datos import obtener_conexion
    from calendario_administracion import guardar_jornada_escolar

    if not session.get("panel_autorizado", False):
        return jsonify({
            "resultado": "no_autorizado"
        }), 401


    # MPAZ - PASO 665
    # Bloqueo de escritura del lado del servidor.
    # Deshabilitado por defecto.

    if (
        os.getenv(
            "MPAZ_CALENDARIO_ESCRITURA_HABILITADA",
            ""
        ).strip().lower() != "si"
    ):
        return jsonify({
            "resultado": "calendario_escritura_deshabilitada",
            "mensaje": (
                "La administracion del calendario "
                "no esta habilitada en este entorno"
            )
        }), 403

    token_sesion = session.get("calendario_csrf")
    token_recibido = request.headers.get("X-CSRF-Token")

    if (
        not isinstance(token_sesion, str)
        or not isinstance(token_recibido, str)
        or not token_sesion
        or not secrets.compare_digest(
            token_sesion, token_recibido
        )
    ):
        return jsonify({
            "resultado": "csrf_invalido",
            "mensaje": "Token de seguridad ausente o invalido"
        }), 403

    if not request.is_json:
        return jsonify({
            "resultado": "datos_invalidos"
        }), 400

    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "resultado": "datos_invalidos"
        }), 400

    curso = datos.get("curso")

    # Un alcance general se representa como NULL.
    if curso == "":
        curso = None

    conexion = None

    try:
        conexion = obtener_conexion()

        resultado = guardar_jornada_escolar(
            conexion,
            accion=accion,
            fecha=datos.get("fecha"),
            curso=curso,
            condicion=datos.get("condicion"),
            motivo=datos.get("motivo"),
            hora_entrada=datos.get("hora_entrada"),
            hora_salida=datos.get("hora_salida")
        )

    except ValueError as error:
        return jsonify({
            "resultado": str(error),
            "mensaje": "Datos de jornada invalidos"
        }), 400

    except sqlite3.IntegrityError:
        return jsonify({
            "resultado": "conflicto_registro"
        }), 409

    except sqlite3.OperationalError as error:

        if "no such table" in str(error).lower():
            return jsonify({
                "resultado": "calendario_no_preparado",
                "mensaje": "Faltan estructuras del calendario"
            }), 503

        return jsonify({
            "resultado": "base_datos_no_disponible"
        }), 503

    finally:
        if conexion is not None:
            conexion.close()

    codigo = resultado.get("resultado")

    if codigo == "creada":
        return jsonify(resultado), 201

    if codigo == "actualizada":
        return jsonify(resultado), 200

    if codigo == "sin_cambios":
        return jsonify(resultado), 200

    if codigo == "ya_existe":
        return jsonify(resultado), 409

    if codigo == "no_existe":
        return jsonify(resultado), 404

    return jsonify({
        "resultado": "error_interno"
    }), 500


@app.post("/panel/calendario/jornadas/registrar")
def registrar_jornada_calendario_panel():
    return procesar_jornada_calendario_panel("crear")


@app.post("/panel/calendario/jornadas/editar")
def editar_jornada_calendario_panel():
    return procesar_jornada_calendario_panel("editar")



# ====================================================
# MPAZ RFID - CONSULTAS DEL CALENDARIO ESCOLAR
# ====================================================

@app.get("/panel/calendario/mes")
def consultar_calendario_mensual_panel():

    import re
    import sqlite3
    from datetime import date

    from base_datos import obtener_conexion
    from calendario_escolar import validar_curso_escolar

    if not session.get("panel_autorizado", False):
        return jsonify({
            "resultado": "no_autorizado"
        }), 401

    mes = request.args.get("mes", "")
    curso = request.args.get("curso", "").strip()

    if not re.fullmatch(
        "[0-9]{4}-(0[1-9]|1[0-2])", mes
    ):
        return jsonify({
            "resultado": "mes_invalido"
        }), 400

    try:
        date.fromisoformat(mes + "-01")

        if curso:
            curso = validar_curso_escolar(curso)
        else:
            curso = None

    except ValueError:
        return jsonify({
            "resultado": "parametros_invalidos"
        }), 400

    # Consultar solamente el mes solicitado.
    inicio = mes + "-01"

    anio = int(mes[:4])
    numero_mes = int(mes[5:7])

    if numero_mes == 12:
        if anio == 9999:
            fin = "9999-13-01"
        else:
            fin = f"{anio + 1:04d}-01-01"
    else:
        fin = f"{anio:04d}-{numero_mes + 1:02d}-01"

    if curso is None:
        consulta = """
            SELECT id, fecha, curso, condicion,
                   hora_entrada, hora_salida, motivo
            FROM calendario_jornadas
            WHERE fecha >= ?
              AND fecha < ?
              AND curso IS NULL
            ORDER BY fecha
        """
        parametros = (inicio, fin)

    else:
        consulta = """
            SELECT id, fecha, curso, condicion,
                   hora_entrada, hora_salida, motivo
            FROM calendario_jornadas
            WHERE fecha >= ?
              AND fecha < ?
              AND (curso IS NULL OR curso = ?)
            ORDER BY fecha,
                CASE
                    WHEN curso IS NULL THEN 0
                    ELSE 1
                END
        """
        parametros = (inicio, fin, curso)

    conexion = None

    try:
        conexion = obtener_conexion()
        registros = conexion.execute(
            consulta, parametros
        ).fetchall()

    except sqlite3.OperationalError as error:
        if "no such table" in str(error).lower():
            return jsonify({
                "resultado": "calendario_no_preparado"
            }), 503

        return jsonify({
            "resultado": "base_datos_no_disponible"
        }), 503

    finally:
        if conexion is not None:
            conexion.close()

    por_fecha = {}

    for fila in registros:
        por_fecha[fila[1]] = {
            "id": fila[0],
            "fecha": fila[1],
            "curso": curso,
            "condicion": fila[3],
            "alcance": (
                "curso" if fila[2] is not None
                else "general"
            ),
            "hora_entrada": fila[4],
            "hora_salida": fila[5],
            "motivo": fila[6]
        }

    jornadas = list(por_fecha.values())

    respuesta = jsonify({
        "resultado": "ok",
        "mes": mes,
        "curso": curso,
        "total": len(jornadas),
        "jornadas": jornadas
    })

    respuesta.headers["Cache-Control"] = "no-store"
    return respuesta, 200


@app.get("/panel/calendario/jornadas/historial")
def consultar_historial_calendario_panel():

    import json
    import sqlite3

    from base_datos import obtener_conexion
    from calendario_escolar import (
        validar_fecha_escolar,
        validar_curso_escolar
    )

    if not session.get("panel_autorizado", False):
        return jsonify({
            "resultado": "no_autorizado"
        }), 401

    fecha = request.args.get("fecha", "")
    curso = request.args.get("curso", "").strip()

    try:
        fecha = validar_fecha_escolar(fecha)

        if curso:
            curso = validar_curso_escolar(curso)
        else:
            curso = None

    except ValueError:
        return jsonify({
            "resultado": "parametros_invalidos"
        }), 400

    conexion = None

    try:
        conexion = obtener_conexion()

        jornada = conexion.execute(
            """
            SELECT id
            FROM calendario_jornadas
            WHERE fecha = ?
              AND curso IS ?
            LIMIT 1
            """,
            (fecha, curso)
        ).fetchone()

        if jornada is None:
            return jsonify({
                "resultado": "jornada_no_encontrada"
            }), 404

        jornada_id = jornada[0]

        total = conexion.execute(
            """
            SELECT COUNT(*)
            FROM calendario_auditoria
            WHERE jornada_id = ?
            """,
            (jornada_id,)
        ).fetchone()[0]

        filas = conexion.execute(
            """
            SELECT id, accion, valor_anterior,
                   valor_nuevo, actor, registrado_en
            FROM calendario_auditoria
            WHERE jornada_id = ?
            ORDER BY id DESC
            LIMIT 100
            """,
            (jornada_id,)
        ).fetchall()

    except sqlite3.OperationalError as error:
        if "no such table" in str(error).lower():
            return jsonify({
                "resultado": "calendario_no_preparado"
            }), 503

        return jsonify({
            "resultado": "base_datos_no_disponible"
        }), 503

    finally:
        if conexion is not None:
            conexion.close()

    historial = []

    for fila in filas:
        historial.append({
            "id": fila[0],
            "accion": fila[1],
            "anterior": (
                json.loads(fila[2])
                if fila[2] is not None
                else None
            ),
            "nuevo": json.loads(fila[3]),
            "actor": fila[4],
            "registrado_en": fila[5]
        })

    respuesta = jsonify({
        "resultado": "ok",
        "jornada_id": jornada_id,
        "fecha": fecha,
        "curso": curso,
        "total_cambios": total,
        "historial_limitado": total > len(historial),
        "historial": historial
    })

    respuesta.headers["Cache-Control"] = "no-store"
    return respuesta, 200


# MPAZ SEGUIMIENTO 755: rutas protegidas.
from seguimiento_api import seguimiento_bp
app.register_blueprint(seguimiento_bp)

# MPAZ-SEGUIMIENTO-7593
from seguimiento_sesiones import sesiones_bp
app.register_blueprint(sesiones_bp)

# MPAZ-SEGUIMIENTO-7602
from seguimiento_gestiones_api import gestiones_bp
app.register_blueprint(gestiones_bp)



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
