"""Flujos docente y RFID con SQLite temporal y cuentas ficticias."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import sqlite3
import unittest
from unittest.mock import patch

import test_auditoria as fixtures
from consultar_asistencia import obtener_atrasos, obtener_inasistencias

FECHA = "2026-11-25"
LISTADO = "/panel/sesiones-docentes"


class Paso68AKTest(unittest.TestCase):
    setUp = fixtures.SistemaTest.setUp
    docente = fixtures.SistemaTest.docente
    login = fixtures.SistemaTest.login

    def preparar_clase(self):
        self.con.executemany(
            "INSERT INTO alumnos (id,rut,nombre_completo,curso) VALUES (?,?,?,'1A')",
            ((i, f"DEMO-NO-RUT-{i}", f"Estudiante ficticio {i}") for i in range(3, 22)),
        )
        self.con.commit()
        fixtures.bd.guardar_asistencia(1, FECHA, "08:00:00", 1, "paso68ak-rfid")

    def crear(self):
        respuesta = self.client.post("/profesor/sesiones", headers=self.cabecera, json={
            "asignacion_id": 1, "fecha": FECHA, "hora_inicio": "09:05",
        })
        self.assertEqual(respuesta.status_code, 201)
        return f"/profesor/sesiones/{respuesta.json['sesion_id']}"

    def marcar(self, base, alumno, estado):
        return self.client.post(base + "/asistencia", headers=self.cabecera, json={
            "alumno_id": alumno, "estado": estado,
        })

    def test_flujo_20_estudiantes_y_actualizacion_administrativa(self):
        self.preparar_clase()
        original = self.con.execute("SELECT * FROM asistencias").fetchall()
        self.cabecera = {"X-CSRF-Token": self.docente()}
        base = self.crear()
        self.assertEqual(self.client.get(base).json["sesion"]["pendientes"], 20)
        self.assertEqual(self.con.execute("SELECT count(*) FROM asistencias_clase").fetchone(), (0,))
        for alumno in (1, 3, 4):
            self.assertEqual(self.marcar(base, alumno, "presente").status_code, 200)

        admin = fixtures.api.app.test_client()
        self.assertEqual(admin.post("/panel/login-individual", json={
            "usuario": "demo1", "password": fixtures.PASSWORD,
        }).status_code, 200)
        self.assertEqual(admin.get(LISTADO).json["sesiones"][0]["pendientes"], 17)
        self.assertEqual(self.client.get(LISTADO).status_code, 401)

        ruta = base + "/completar-pendientes"
        datos = {"alumnos_pendientes": list(range(5, 22))}
        self.assertEqual(self.client.post(ruta, json=datos).json["resultado"], "csrf_invalido")
        otro = fixtures.api.app.test_client()
        otro.post("/profesor/login", json={"usuario": "profe2", "password": fixtures.PASSWORD})
        token = otro.get("/profesor/sesion").json["csrf_token"]
        self.assertEqual(otro.post(ruta, json=datos, headers={"X-CSRF-Token": token}).status_code, 403)

        respuesta = self.client.post(ruta, json=datos, headers=self.cabecera)
        self.assertEqual((respuesta.status_code, respuesta.json["marcados"]), (200, 17))
        reenvio = self.client.post(ruta, json=datos, headers=self.cabecera)
        self.assertEqual((reenvio.status_code, reenvio.json["marcados"]), (200, 0))
        detalle = self.client.get(base).json
        self.assertEqual(detalle["sesion"]["pendientes"], 0)
        self.assertEqual({a["alumno_id"]: a["estado"] for a in detalle["alumnos"]}, {
            **dict.fromkeys((1, 3, 4), "presente"),
            **dict.fromkeys(range(5, 22), "no_presente"),
        })

        self.assertEqual(self.client.post(base + "/confirmar", headers=self.cabecera).status_code, 200)
        listado = admin.get(LISTADO)
        self.assertEqual(listado.headers["Cache-Control"], "no-store")
        sesion, = listado.json["sesiones"]
        claves = ("estado", "presentes", "atrasados", "no_presentes", "pendientes")
        self.assertEqual(tuple(sesion[c] for c in claves), ("confirmada", 3, 0, 17, 0))
        self.assertEqual(admin.get(f"{LISTADO}/{sesion['sesion_id']}").json["sesion"], sesion)
        self.assertEqual(self.client.post(ruta, json=datos, headers=self.cabecera).status_code, 409)
        self.assertEqual(self.marcar(base, 1, "no_presente").status_code, 409)
        self.assertEqual(self.con.execute("SELECT * FROM asistencias").fetchall(), original)

    def test_concurrencia_nomina_desactualizada_y_rollback(self):
        self.preparar_clase()
        self.cabecera = {"X-CSRF-Token": self.docente()}
        base = self.crear()
        ruta = base + "/completar-pendientes"
        antiguos = {"alumnos_pendientes": [1, *range(3, 22)]}
        self.assertEqual(self.marcar(base, 1, "atrasado").status_code, 200)
        respuesta = self.client.post(ruta, json=antiguos, headers=self.cabecera)
        self.assertEqual((respuesta.status_code, respuesta.json["resultado"]), (409, "pendientes_cambiaron"))

        def enviar(cliente):
            return cliente.post(ruta, json={"alumnos_pendientes": list(range(3, 22))}, headers=self.cabecera)

        self.con.executescript("""
            CREATE TRIGGER fallo_ficticio BEFORE INSERT ON asistencias_clase
            WHEN NEW.alumno_id = 4
            BEGIN
                SELECT RAISE(ABORT, 'fallo ficticio');
            END;
        """)
        self.assertEqual(enviar(self.client).json["resultado"], "error_integridad")
        self.assertEqual(self.con.execute(
            "SELECT alumno_id, estado FROM asistencias_clase"
        ).fetchall(), [(1, "atrasado")])
        self.con.execute("DROP TRIGGER fallo_ficticio")
        with patch("api.completar_pendientes_clase_profesor", side_effect=sqlite3.OperationalError):
            self.assertEqual(enviar(self.client).status_code, 503)

        cookie = self.client.get_cookie(fixtures.api.app.config["SESSION_COOKIE_NAME"])
        clientes = [fixtures.api.app.test_client() for _ in range(4)]
        for cliente in clientes:
            cliente.set_cookie(cookie.key, cookie.value)
        with ThreadPoolExecutor(max_workers=4) as pool:
            respuestas = list(pool.map(enviar, clientes))
        self.assertEqual(sorted((r.status_code, r.json["marcados"]) for r in respuestas),
                         [(200, 0), (200, 0), (200, 0), (200, 19)])
        self.assertEqual(self.con.execute("""
            SELECT estado, count(*) FROM asistencias_clase GROUP BY estado ORDER BY estado
        """).fetchall(), [("atrasado", 1), ("no_presente", 19)])

    def test_catalogo_rfid_y_jornadas_de_prueba(self):
        self.con.execute("UPDATE alumnos SET curso = ' admin ' WHERE id = 2")
        self.con.commit()
        fixtures.bd.guardar_asistencia(2, FECHA, "18:00:00", 1, "prueba-admin")
        self.login()
        datos = self.client.get("/asistencias").json
        self.assertIn("1A", datos["cursos_matricula"])
        self.assertIn("2A", datos["cursos_matricula"])
        self.assertNotIn("ADMIN", datos["cursos_matricula"])
        prueba, = datos["asistencias"]
        self.assertTrue(prueba["es_prueba"])
        self.assertEqual(obtener_atrasos(fecha_referencia=FECHA), [])
        self.assertEqual([(fila[2], fila[4]) for fila in obtener_inasistencias(fecha_referencia=FECHA)], [("1A", 0)])

        with patch.object(fixtures.exportaciones, "CARPETA_REPORTES", self.ruta.parent):
            with patch.object(fixtures.exportaciones, "hoy_chile", return_value=datetime.fromisoformat(FECHA).date()):
                _, cantidad = fixtures.exportaciones.exportar_asistencias()
        self.assertEqual(cantidad, 0)
        self.assertEqual(self.con.execute("SELECT count(*) FROM asistencias").fetchone(), (1,))

    def test_cierres_tardios_y_conservacion_de_jornadas_cerradas(self):
        for alumno, fecha, hora in (
            (1, "2026-11-23", "18:12:34"), (1, "2026-11-24", "19:05:00"),
            (1, FECHA, "18:02:01"), (2, FECHA, "18:40:00"),
        ):
            fixtures.bd.guardar_asistencia(alumno, fecha, hora, 1, f"{alumno}-{fecha}")
        self.con.execute("""
            UPDATE asistencias SET hora_salida = '17:00:00', tipo_salida = 'automatica'
            WHERE fecha = '2026-11-24'
        """)
        self.con.commit()

        with patch.object(fixtures.bd, "ahora_chile", return_value=datetime(2026, 11, 25, 18, 20)):
            resultado = fixtures.bd.cerrar_jornadas_pendientes()
            repetido = fixtures.bd.cerrar_jornadas_pendientes()
        self.assertEqual((resultado["jornadas_anteriores"], resultado["jornadas_hoy"]), (1, 1))
        self.assertEqual((repetido["jornadas_anteriores"], repetido["jornadas_hoy"]), (0, 0))
        self.assertEqual(self.con.execute("""
            SELECT hora_salida, tipo_salida, totem_salida_id, evento_salida_id
            FROM asistencias ORDER BY fecha, alumno_id
        """).fetchall(), [
            ("18:12:34", "automatica", None, None),
            ("17:00:00", "automatica", None, None),
            ("18:02:01", "automatica", None, None),
            (None, None, None, None),
        ])
