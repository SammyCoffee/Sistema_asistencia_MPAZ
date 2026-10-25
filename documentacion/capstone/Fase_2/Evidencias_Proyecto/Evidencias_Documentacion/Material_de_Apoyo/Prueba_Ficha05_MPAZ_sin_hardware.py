#!/usr/bin/env python3
"""Prueba académica aislada para la Ficha de Avance 05 del Sistema MPAZ RFID.

Ejecutar desde la RAIZ del proyecto, con el .venv activado:
    python3 ~/Descargas/Prueba_Ficha05_MPAZ_sin_hardware.py

Usa flask.test_client + una BD SQLite en directorio TEMPORAL.
No hace peticiones a la API que está en ejecución ni cambia la BD real.
No requiere lectores ESP32/PN532 ni claves reales.
"""
from __future__ import annotations

import os
import sqlite3
import subprocess
import sys
import tempfile
import uuid
from datetime import datetime
from pathlib import Path


def salida(nombre: str, pasa: bool, detalle: str = "") -> None:
    marca = "OK" if pasa else "FALLÓ"
    print(f"[{marca}] {nombre}")
    if detalle:
        print(f"     {detalle}")
    if not pasa:
        raise RuntimeError(f"La verificación '{nombre}' no se superó")


def cuenta_asistencias(bd: Path) -> int:
    with sqlite3.connect(bd) as cx:
        return cx.execute("SELECT COUNT(*) FROM asistencias").fetchone()[0]


def main() -> int:
    proyecto = Path.cwd().resolve()
    requeridos = ("api.py", "base_datos.py", "procesar_lectura_totem.py")
    if not all((proyecto / f).is_file() for f in requeridos):
        print("ERROR: debes situarte primero en la carpeta del proyecto MPAZ RFID.")
        print(f"Carpeta actual: {proyecto}")
        print("Ejemplo: cd ~/Proyectos/Sistema_asistencia_MPAZ")
        return 1

    sys.path.insert(0, str(proyecto))
    version = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=proyecto,
                             capture_output=True, text=True, check=False)
    print("=" * 71)
    print("FICHA 05 | PRUEBA SIMULADA SIN ESP32 | SOLO DATOS FICTICIOS")
    print("=" * 71)
    print("Momento:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("Versión Git:", version.stdout.strip() if version.returncode == 0 else "No disponible")
    print("Método: Flask test_client (sin conexión al servidor real)")
    print("Base escolar real: NO SE UTILIZA")

    with tempfile.TemporaryDirectory(prefix="mpaz_ficha05_aislada_") as temp:
        bd = Path(temp) / "solo_demostracion.db"
        # Fijar estas variables ANTES de importar api.py y base_datos.py.
        os.environ["MPAZ_DB_PATH"] = str(bd)
        os.environ["MPAZ_API_KEY"] = "CLAVE_DEMO_FICHA05_SOLO_TEST_CLIENT"
        os.environ["MPAZ_PANEL_PASSWORD"] = "PANEL_DEMO_FICHA05"
        os.environ["MPAZ_SESSION_SECRET"] = "SESION_DEMO_FICHA05_NO_REAL"

        # Si en alguna versión el proyecto cambia, nunca se debe usar la BD real.
        assert bd.is_absolute() and bd != (proyecto / "data" / "asistencia.db").resolve()

        import base_datos  # noqa: PLC0415
        base_datos.crear_tablas()
        salida("Esquema de prueba creado", bd.is_file(), "Solo se creó un archivo SQLite temporal")

        uid = "F05A1B2C"
        codigo_totem = "TOTEM-F05-SIMULADO"
        evento_id = "F05-PRUEBA-" + uuid.uuid4().hex[:12].upper()
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        with sqlite3.connect(bd) as cx:
            cx.execute("PRAGMA foreign_keys = ON")
            cx.execute("INSERT INTO alumnos (rut,nombre_completo,curso,estado) VALUES (?,?,?,?)",
                       ("ID_FICTICIO_F05", "Estudiante Demo Ficha Cinco", "1A", "activo"))
            alumno_id = cx.execute("SELECT id FROM alumnos WHERE rut = ?",
                                   ("ID_FICTICIO_F05",)).fetchone()[0]
            cx.execute("INSERT INTO tarjetas (alumno_id,uid,estado,fecha_registro,fecha_asignacion) "
                       "VALUES (?,?,?,?,?)", (alumno_id, uid, "activa", fecha_hoy, fecha_hoy))
            cx.execute("INSERT INTO totems (codigo,nombre,ubicacion,estado,fecha_registro) "
                       "VALUES (?,?,?,?,?)",
                       (codigo_totem, "Tótem simulado Ficha 05", "Laboratorio ficticio", "activo", fecha_hoy))

        import api  # noqa: PLC0415
        cliente = api.app.test_client()
        encabezados = {"X-API-KEY": os.environ["MPAZ_API_KEY"]}
        datos = {"codigo_totem": codigo_totem, "uid": uid, "evento_id": evento_id}

        print("\n[1] Comprobación GET /estado")
        r = cliente.get("/estado")
        salida("GET /estado", r.status_code == 200, f"HTTP={r.status_code}")

        print("\n[2] Estado antes de la nueva entrada")
        inicial = cuenta_asistencias(bd)
        print("Registros antes:", inicial)
        print("Evento enviado:", evento_id)
        print("UID ficticio:", uid)
        print("Tótem ficticio:", codigo_totem)

        print("\n[3] POST /lectura (nueva entrada simulada)")
        r = cliente.post("/lectura", json=datos, headers=encabezados)
        cuerpo = r.get_json(silent=True) or {}
        print("HTTP:", r.status_code)
        print("Resultado:", cuerpo.get("resultado"))
        print("Hora registrada:", cuerpo.get("hora"))
        salida("Entrada registrada", r.status_code == 200 and cuerpo.get("resultado") == "entrada_registrada")

        print("\n[4] Correlación con la escritura SQLite (MISMO evento_id)")
        with sqlite3.connect(bd) as cx:
            fila = cx.execute("SELECT fecha,hora_entrada,evento_id,evento_entrada_id "
                              "FROM asistencias WHERE evento_id=? OR evento_entrada_id=? LIMIT 1",
                              (evento_id, evento_id)).fetchone()
            ahora = cx.execute("SELECT COUNT(*) FROM asistencias").fetchone()[0]
        print("Registro SQLite:", fila)
        print("Registros después:", ahora)
        salida("Mismo evento encontrado en SQLite",
               bool(fila) and evento_id in (fila[2], fila[3]) and ahora == inicial + 1)

        print("\n[5] Reenvío del mismo evento: no debe duplicar")
        r = cliente.post("/lectura", json=datos, headers=encabezados)
        resp = r.get_json(silent=True) or {}
        tras_repetido = cuenta_asistencias(bd)
        print("Resultado:", resp.get("resultado"))
        print("Registros antes/después:", ahora, "/", tras_repetido)
        salida("Idempotencia evento_repetido",
               resp.get("resultado") == "evento_repetido" and tras_repetido == ahora)

        print("\n[6] Validación de tótem desactivado")
        with sqlite3.connect(bd) as cx:
            cx.execute("UPDATE totems SET estado='inactivo' WHERE codigo=?", (codigo_totem,))
        bloqueado = dict(datos, evento_id="F05-INACTIVO-"+uuid.uuid4().hex[:8].upper())
        r = cliente.post("/lectura", json=bloqueado, headers=encabezados)
        resp = r.get_json(silent=True) or {}
        print("HTTP:", r.status_code, "| Resultado:", resp.get("resultado"))
        salida("Tótem inactivo rechazado sin escritura",
               r.status_code == 403 and resp.get("resultado") == "totem_inactivo"
               and cuenta_asistencias(bd) == ahora)

        print("\n[7] Validación de solicitud SIN clave API")
        r = cliente.post("/lectura", json=dict(datos, evento_id="F05-SINCLAVE"))
        resp = r.get_json(silent=True) or {}
        print("HTTP:", r.status_code, "| Resultado:", resp.get("resultado"))
        salida("Solicitud sin clave rechazada sin escritura",
               r.status_code == 401 and resp.get("resultado") == "no_autorizado"
               and cuenta_asistencias(bd) == ahora)

        print("\n" + "=" * 71)
        print("PRUEBAS SIMULADAS APROBADAS EN EL CÓDIGO DEL PROYECTO")
        print("Lectura: simulada por HTTP/Flask; NO capturada por ESP32 físico")
        print("Base de datos: TEMPORAL y DE PRUEBA; se elimina al finalizar")
        print("No demuestra: piloto escolar, lector PN532 físico, exportación o despliegue real")
        print("=" * 71)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print("\nERROR: la prueba se detuvo, sin utilizar la base real.")
        print(f"Tipo: {type(exc).__name__}; detalle: {exc}")
        print("Envíame una captura de este error para ajustar la prueba a tu versión.")
        sys.exit(1)