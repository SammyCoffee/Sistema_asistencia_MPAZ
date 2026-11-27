"""Prueba Chromium local sobre el mismo fixture ficticio del paso 68AK."""
from threading import Thread

from werkzeug.serving import make_server

from navegador_paso65 import esperar, navegador
from test_paso68ak import FECHA, Paso68AKTest, fixtures


def comprobar(web, base):
    def js(script, *args):
        return web("/execute/sync", {"script": script, "args": args})

    def campo(selector, valor):
        js("""
            const campo = document.querySelector(arguments[0]);
            campo.value = arguments[1];
            for (const evento of ['input', 'change']) {
                campo.dispatchEvent(new Event(evento, {bubbles: true}));
            }
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
            const nodo = document.querySelector(arguments[0]);
            return Boolean(nodo?.getClientRects().length && nodo.textContent.includes(arguments[1]));
        """, selector, texto))

    def entrar(ruta, usuario, boton, destino):
        web("/url", {"url": base + ruta})
        campo("#usuario", usuario)
        campo("#password", fixtures.PASSWORD)
        pulsar(boton)
        esperar(lambda: destino in web("/url"))

    entrar("/profesor/login.html", "profe1", "#boton-ingresar", "/profesor/panel.html")
    esperar(lambda: js("return document.querySelector('#selector-curso')?.options.length === 2;"))
    campo("#selector-curso", "1A")
    campo("#selector-asignatura", "1")
    pulsar("#boton-gestionar-clase")
    campo("#fecha-sesion-clase", FECHA)
    campo("#hora-sesion-clase", "09:05")
    pulsar("#boton-crear-sesion-clase")
    contiene("#pendientes-clase", "20")
    for alumno in (1, 3, 4):
        pulsar(f'.casilla-asistencia-masiva[value="{alumno}"]')
    pulsar("#boton-masivo-presentes")
    contiene("#pendientes-clase", "17")

    completar = "#boton-completar-pendientes"
    confirmar = "#boton-confirmar-sesion-clase"
    js("window.confirm = mensaje => { window.ultimoDialogo = mensaje; return false; };")
    pulsar(completar)
    assert "17 estudiantes pendientes" in js("return window.ultimoDialogo;")
    assert js("return document.querySelector('#pendientes-clase').textContent;") == "17"
    assert js("return document.querySelector(arguments[0]).disabled;", confirmar)

    js("window.confirm = () => true;")
    pulsar(completar)
    contiene("#mensaje-gestion-clase", "Estudiantes marcados como no presentes: 17")
    contiene("#pendientes-clase", "0")
    assert js("return document.querySelectorAll('.estado-presente').length;") == 3
    assert js("return document.querySelectorAll('.estado-no_presente').length;") == 17
    pulsar(confirmar)
    contiene("#mensaje-gestion-clase", "Asistencia confirmada correctamente")
    assert js("return document.querySelector(arguments[0]).disabled;", completar)

    entrar("/login.html", "demo1", "#login-form button[type=submit]", "/index.html")
    pulsar('.mpaz-accesos a[href="#sesiones-docentes"]')
    pulsar('#filtros-sesiones-docentes button[type="submit"]')
    contiene("#filas-sesiones-docentes", "Confirmada")
    assert js("""
        return Array.from(document.querySelector('#filas-sesiones-docentes tr').cells)
            .slice(5, 10).map(celda => celda.textContent);
    """) == ["Confirmada", "3", "0", "17", "0"]

    web("/url", {"url": base + "/index.html#asistencias"})
    contiene("#asistencias h2", "Jornadas RFID")
    esperar(lambda: js("return [...document.querySelector('#mpaz-asis-curso').options].some(o => o.value === '2A');"))
    assert js("return document.querySelector('#mpaz-asis-ingresos').textContent;") == "1"
    campo("#mpaz-asis-curso", "2A")
    contiene("#mpaz-asis-mensaje", "Este curso aún no tiene marcaciones de acceso RFID.")
    campo("#mpaz-asis-curso", "ADMIN")
    contiene("#cuerpo-asistencias tr:not([hidden])", "ADMIN · Prueba RFID")
    assert js("return document.querySelector('.mpaz-resumen-asistencias').hidden;")


def main():
    caso = Paso68AKTest()
    caso.setUp()
    try:
        caso.preparar_clase()
        caso.con.execute("INSERT INTO alumnos (id,rut,nombre_completo,curso) VALUES (22,'DEMO-NO-RUT-22','Cuenta ficticia','ADMIN')")
        caso.con.commit()
        fixtures.bd.guardar_asistencia(22, FECHA, "18:00:00", 1, "prueba-navegador-admin")
        original = caso.con.execute("SELECT * FROM asistencias").fetchall()
        fixtures.api.app.config.update(SESSION_COOKIE_SECURE=False)
        servidor = make_server("127.0.0.1", 0, fixtures.api.app, threaded=True)
        hilo = Thread(target=servidor.serve_forever, daemon=True)
        hilo.start()
        try:
            with navegador() as web:
                comprobar(web, f"http://127.0.0.1:{servidor.server_port}")
            assert caso.con.execute("SELECT * FROM asistencias").fetchall() == original
        finally:
            servidor.shutdown()
            servidor.server_close()
            hilo.join()
    finally:
        caso.doCleanups()
    print("Chromium: confirmación explícita, sesión de 20, listado administrativo y filtros RFID verificados.")


if __name__ == "__main__":
    main()
