"""Prueba Chromium local. Ejecutar con PYTHONPATH=. y una carpeta para capturas."""
from base64 import b64decode
from contextlib import contextmanager
import json
from pathlib import Path
from subprocess import DEVNULL, Popen
import sys
from threading import Thread
from time import monotonic, sleep
from urllib.error import URLError
from urllib.request import Request, urlopen

from werkzeug.serving import make_server

from test_sesiones_docentes import SesionesDocentesTest
import test_auditoria as fixtures


def esperar(condicion):
    hasta = monotonic() + 12
    while monotonic() < hasta:
        if condicion():
            return
        sleep(0.1)
    raise AssertionError("El navegador no llegó al estado esperado")


@contextmanager
def navegador():
    with Popen(["chromedriver", "--port=9515", "--allowed-ips=127.0.0.1"],
               stdout=DEVNULL, stderr=DEVNULL) as proceso:
        cliente = "http://127.0.0.1:9515"

        def enviar(ruta, datos=None, metodo=None):
            cuerpo = None if datos is None else json.dumps(datos).encode()
            peticion = Request(cliente + ruta, data=cuerpo, method=metodo,
                                headers={"Content-Type": "application/json"})
            with urlopen(peticion, timeout=20) as respuesta:
                return json.load(respuesta)["value"]

        def listo():
            try:
                return enviar("/status")["ready"]
            except URLError:
                return False

        try:
            esperar(listo)
            sesion = enviar("/session", {"capabilities": {"alwaysMatch": {
                "browserName": "chrome",
                "goog:chromeOptions": {"binary": "/usr/bin/chromium", "args": [
                    "--headless=new", "--no-sandbox", "--disable-dev-shm-usage",
                    "--disable-background-networking", "--no-proxy-server",
                    "--window-size=1440,1100",
                ]},
            }}})["sessionId"]
            try:
                yield lambda ruta, datos=None: enviar(f"/session/{sesion}{ruta}", datos)
            finally:
                enviar(f"/session/{sesion}", metodo="DELETE")
        finally:
            proceso.terminate()


def comprobar(web, base, salida):
    def js(script, *args):
        return web("/execute/sync", {"script": script, "args": args})

    def campo(selector, valor):
        js("""
            const campo = document.querySelector(arguments[0]);
            campo.value = arguments[1];
            campo.dispatchEvent(new Event('change', {bubbles: true}));
        """, selector, valor)

    def pulsar(selector):
        assert js("""
            const boton = document.querySelector(arguments[0]);
            if (!boton || boton.disabled || !boton.getClientRects().length) return false;
            boton.click();
            return true;
        """, selector), selector

    def contiene(selector, texto):
        esperar(lambda: js("""
            const campo = document.querySelector(arguments[0]);
            return Boolean(campo?.getClientRects().length && campo.textContent.includes(arguments[1]));
        """, selector, texto))

    def captura(nombre):
        (salida / nombre).write_bytes(b64decode(web("/screenshot")))

    def entrar(ruta, usuario, boton):
        web("/url", {"url": base + ruta})
        campo("#usuario", usuario)
        campo("#password", fixtures.PASSWORD)
        pulsar(boton)
        esperar(lambda: "/panel.html" in web("/url") or "/index.html" in web("/url"))

    entrar("/profesor/login.html", "profe1", "#boton-ingresar")
    esperar(lambda: js("return document.querySelector('#selector-curso')?.options.length === 2;"))
    assert js("return document.querySelector('#selector-curso option:last-child').value;") == "4°B"
    campo("#selector-curso", "4°B")
    campo("#selector-asignatura", "1")
    pulsar("#boton-gestionar-clase")
    campo("#fecha-sesion-clase", "2026-11-25")
    campo("#hora-sesion-clase", "09:05")
    mensaje = "#mensaje-gestion-clase"

    js("""
        const original = window.fetch;
        let fallo = true;
        window.fetch = (ruta, opciones) => {
            if (fallo && ruta === '/profesor/sesiones' && opciones.method === 'POST') {
                fallo = false;
                return original(ruta, {...opciones, headers: {...opciones.headers, 'X-CSRF-Token': 'vencido'}});
            }
            return original(ruta, opciones);
        };
    """)
    pulsar("#boton-crear-sesion-clase")
    contiene(mensaje, "La validación de seguridad venció")

    # El historial falla una vez tras guardar. Un reintento recupera el mismo borrador.
    js("""
        const original = window.fetch;
        let fallo = true;
        window.fetch = (ruta, opciones) => {
            if (fallo && String(ruta).includes('/profesor/asignaciones/1/sesiones')) {
                fallo = false;
                return Promise.reject(new TypeError('Red ficticia'));
            }
            return original(ruta, opciones);
        };
    """)
    pulsar("#boton-crear-sesion-clase")
    contiene(mensaje, "No se pudo actualizar el historial")
    pulsar("#boton-crear-sesion-clase")
    contiene(mensaje, "Se recuperó el borrador existente")
    contiene("#pendientes-clase", "2")
    contiene("#lista-asistencia-clase", "Pendiente de marcar")
    assert js("return document.querySelector('#boton-confirmar-sesion-clase').disabled;")

    # Una pérdida de red deja una marca por reintentar.
    js("""
        const original = window.fetch;
        let fallo = true;
        window.fetch = (ruta, opciones) => {
            if (fallo && String(ruta).endsWith('/asistencia')
                && JSON.parse(opciones.body).alumno_id === 3) {
                fallo = false;
                return Promise.reject(new TypeError('Red ficticia'));
            }
            return original(ruta, opciones);
        };
    """)
    pulsar("#seleccionar-todos-asistencia")
    pulsar("#boton-masivo-presentes")
    contiene(mensaje, "Quedó 1 marca seleccionada")
    contiene("#pendientes-clase", "1")
    captura("docente-borrador-parcial.png")
    pulsar("#boton-masivo-presentes")
    contiene("#pendientes-clase", "0")
    contiene(mensaje, "Guardados con confirmación del servidor: 1 de 1")
    js("window.confirm = () => true;")
    pulsar("#boton-confirmar-sesion-clase")
    contiene(mensaje, "Asistencia confirmada correctamente")
    captura("docente-confirmada.png")

    # En el mismo navegador, Administración obtiene su propia sesión individual.
    entrar("/login.html", "demo1", "#login-form button[type=submit]")
    pulsar('.mpaz-accesos a[href="#sesiones-docentes"]')
    contiene("#filas-sesiones-docentes", "Confirmada")
    campo('#filtros-sesiones-docentes [name="estado"]', "borrador")
    pulsar('#filtros-sesiones-docentes button[type="submit"]')
    contiene("#mensaje-sesiones-docentes", "No hay sesiones docentes")
    campo('#filtros-sesiones-docentes [name="estado"]', "confirmada")
    pulsar('#filtros-sesiones-docentes button[type="submit"]')
    contiene("#filas-sesiones-docentes", "4°B")
    pulsar("#filas-sesiones-docentes button")
    contiene("#datos-detalle-docente", "Docente Ficticio")
    assert js("""
        const detalle = document.querySelector('#datos-detalle-docente');
        return [...detalle.querySelectorAll('dt')].some(
            dt => dt.textContent === 'Presentes' && dt.nextElementSibling.textContent === '2'
        ) && !detalle.textContent.includes('Estudiante ficticio');
    """)
    captura("administracion-detalle.png")

    js("""
        const original = window.fetch;
        window.fetch = (ruta, opciones) => String(ruta).startsWith('/panel/sesiones-docentes')
            ? Promise.resolve(new Response('{}', {status: 503})) : original(ruta, opciones);
    """)
    pulsar('#filtros-sesiones-docentes button[type="submit"]')
    contiene("#mensaje-sesiones-docentes", "no está disponible")

    web("/url", {"url": base + "/profesor/panel.html"})
    esperar(lambda: "expirada=1" in web("/url"))
    contiene("#mensaje-login", "La sesión docente expiró")
    entrar("/profesor/login.html", "profe2", "#boton-ingresar")
    esperar(lambda: js("return document.querySelector('#selector-curso')?.options.length === 3;"))
    assert js("return [...document.querySelector('#selector-curso').options].slice(1).map(o => o.value);") == ["2A", "5A"]


def main():
    salida = Path(sys.argv[1]).resolve()
    salida.mkdir(parents=True, exist_ok=True)
    caso = SesionesDocentesTest()
    caso.setUp()
    try:
        caso.preparar_cursos()
        fixtures.bd.guardar_asistencia(1, "2026-11-25", "08:00:00", 1, "navegador-rfid")
        original = caso.con.execute("SELECT * FROM asistencias").fetchall()
        assert len(original) == 1
        fixtures.api.app.config.update(SESSION_COOKIE_SECURE=False)
        servidor = make_server("127.0.0.1", 0, fixtures.api.app, threaded=True)
        hilo = Thread(target=servidor.serve_forever, daemon=True)
        hilo.start()
        try:
            with navegador() as web:
                comprobar(web, f"http://127.0.0.1:{servidor.server_port}", salida)
            assert caso.con.execute("SELECT estado FROM sesiones_clase").fetchall() == [("confirmada",)]
            assert caso.con.execute("SELECT count(*) FROM asistencias_clase").fetchone() == (2,)
            assert caso.con.execute("SELECT * FROM asistencias").fetchall() == original
        finally:
            servidor.shutdown()
            servidor.server_close()
            hilo.join()
    finally:
        caso.doCleanups()
    print("Chromium: flujo docente y administrativo, fallos y recuperación verificados.")


if __name__ == "__main__":
    main()
