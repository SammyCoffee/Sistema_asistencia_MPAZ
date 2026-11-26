"""Recorrido del paso 65 con SQLite temporal y cuentas ficticias."""
import sqlite3
import unittest
from unittest.mock import patch

import test_auditoria as fixtures

RUTA = "/panel/sesiones-docentes"
FECHA = "2026-11-25"


class SesionesDocentesTest(unittest.TestCase):
    setUp = fixtures.SistemaTest.setUp
    login = fixtures.SistemaTest.login
    docente = fixtures.SistemaTest.docente

    def preparar_cursos(self):
        self.con.executescript("""
            UPDATE profesores_cursos SET curso = ' 4°b ' WHERE id = 1;
            UPDATE alumnos SET curso = '4°B' WHERE id = 1;
            INSERT INTO alumnos (id, rut, nombre_completo, curso)
                VALUES (3, 'DEMO-NO-RUT-3', 'Estudiante ficticio tres', ' 4°b ');
            INSERT INTO asignaturas (id, nombre, estado) VALUES (2, 'Inactiva', 'inactivo');
            INSERT INTO profesores_cursos (id, profesor_id, curso, asignatura_id, estado)
                VALUES (3, 2, '5A', 1, 'activo'), (4, 1, '6A', 1, 'inactivo'),
                       (5, 1, '7A', 2, 'activo'), (6, 1, '4B', 1, 'inactivo');
        """)

    def crear(self, cabecera, hora="09:05", asignacion=1):
        return self.client.post("/profesor/sesiones", headers=cabecera, json={
            "asignacion_id": asignacion, "fecha": FECHA, "hora_inicio": hora,
        })

    def test_selector_y_nomina_restringidos(self):
        self.preparar_cursos()
        self.docente()
        asignaciones = self.client.get("/profesor/asignaciones").json["asignaciones"]
        self.assertEqual([(a["asignacion_id"], a["curso"]) for a in asignaciones], [(1, "4°B")])
        self.assertEqual(self.client.get("/profesor/cursos/4°b/alumnos").json["total"], 2)
        for curso in ("4B", "6A", "7A", "2A"):
            with self.subTest(curso=curso):
                self.assertEqual(self.client.get(f"/profesor/cursos/{curso}/alumnos").status_code, 403)

        self.client.post("/profesor/login", json={"usuario": "profe2", "password": fixtures.PASSWORD})
        asignaciones = self.client.get("/profesor/asignaciones").json["asignaciones"]
        self.assertEqual([a["curso"] for a in asignaciones], ["2A", "5A"])
        self.assertEqual(self.client.get("/profesor/cursos/2A/alumnos").json["total"], 1)
        self.assertEqual(self.client.get("/profesor/cursos/5A/alumnos").json["total"], 0)
        cabecera = {"X-CSRF-Token": self.client.get("/profesor/sesion").json["csrf_token"]}
        id_vacia = self.crear(cabecera, asignacion=3).json["sesion_id"]
        vacia = self.client.post(f"/profesor/sesiones/{id_vacia}/confirmar", headers=cabecera)
        self.assertEqual((vacia.status_code, vacia.json["resultado"]), (409, "curso_sin_alumnos"))

    def test_flujo_completo_con_reintentos_y_detalle_historico(self):
        self.preparar_cursos()
        fixtures.bd.guardar_asistencia(1, FECHA, "08:00:00", 1, "paso65-rfid")
        rfid_original = self.con.execute("SELECT * FROM asistencias").fetchall()
        self.assertEqual(len(rfid_original), 1)
        cabecera = {"X-CSRF-Token": self.docente()}
        self.assertEqual(self.crear({}).json["resultado"], "csrf_invalido")
        self.assertEqual(self.crear(cabecera, asignacion=4).status_code, 403)
        alta = self.crear(cabecera)
        self.assertEqual((alta.status_code, alta.json["estado"]), (201, "borrador"))
        ident = alta.json["sesion_id"]
        base = f"/profesor/sesiones/{ident}"
        reenvio = self.crear(cabecera)
        self.assertEqual((reenvio.status_code, reenvio.json["sesion_id"]), (200, ident))
        self.assertEqual(self.client.get(base).json["sesion"]["pendientes"], 2)

        def marcar(alumno, estado):
            return self.client.post(base + "/asistencia", headers=cabecera, json={
                "alumno_id": alumno, "estado": estado,
            })

        self.assertEqual(marcar(1, "presente").status_code, 200)
        self.assertEqual(marcar(2, "presente").status_code, 403)
        incompleta = self.client.post(base + "/confirmar", headers=cabecera)
        self.assertEqual((incompleta.status_code, incompleta.json["pendientes"]), (409, 1))
        self.assertEqual(self.client.get(RUTA).status_code, 401)

        admin = fixtures.api.app.test_client()
        acceso = admin.post("/panel/login-individual", json={"usuario": "demo1", "password": fixtures.PASSWORD})
        self.assertEqual(acceso.status_code, 200)
        listado = admin.get(RUTA, query_string={"fecha": FECHA, "curso": " 4°b ", "asignatura": "Demo", "estado": "borrador"})
        self.assertEqual(listado.status_code, 200)
        self.assertEqual(listado.headers["Cache-Control"], "no-store")
        self.assertEqual([(s["sesion_id"], s["pendientes"]) for s in listado.json["sesiones"]], [(ident, 1)])

        self.con.execute("UPDATE asistencias_clase SET fecha_registro = '2026-11-25 12:06:00'")
        self.con.commit()
        self.assertEqual(marcar(1, "presente").status_code, 200)
        self.assertEqual(self.con.execute("SELECT fecha_registro FROM asistencias_clase").fetchone()[0],
                         "2026-11-25 12:06:00")
        self.assertEqual(marcar(3, "atrasado").status_code, 200)
        self.assertEqual(self.client.post(base + "/confirmar", headers=cabecera).status_code, 200)
        self.assertEqual(marcar(3, "no_presente").status_code, 409)
        self.assertEqual(self.con.execute("SELECT count(*) FROM asistencias_clase").fetchone()[0], 2)
        self.assertEqual(self.con.execute("SELECT * FROM asistencias").fetchall(), rfid_original)

        # Cambios ficticios posteriores a la clase. La consulta histórica conserva las marcas.
        self.con.execute("UPDATE alumnos SET curso = '9C' WHERE id = 3")
        self.con.execute("UPDATE alumnos SET curso = '4°B' WHERE id = 2")
        self.con.commit()
        detalle_docente = self.client.get(base).json
        self.assertEqual({a["alumno_id"] for a in detalle_docente["alumnos"]}, {1, 3})
        self.assertEqual(detalle_docente["sesion"]["pendientes"], 0)
        self.con.execute("UPDATE profesores_cursos SET estado = 'inactivo' WHERE id = 1")
        self.con.commit()
        datos = admin.get(f"{RUTA}/{ident}").json["sesion"]
        self.assertEqual(datos["profesor"], "Docente Ficticio")
        self.assertEqual(datos["estado"], "confirmada")
        self.assertEqual((datos["presentes"], datos["atrasados"], datos["no_presentes"], datos["pendientes"]), (1, 1, 0, 0))
        self.assertNotIn("alumnos", datos)
        self.assertNotIn("observacion", datos)
        self.assertEqual(admin.get(RUTA + "?estado=borrador").json["sesiones"], [])
        self.assertEqual(admin.get(RUTA + "?estado=confirmada").json["sesiones"], [datos])

    def test_permiso_filtros_y_fallo_del_servicio(self):
        self.assertEqual(self.client.get(RUTA).status_code, 401)
        self.assertGreaterEqual(self.client.post("/panel/login", json={"password": fixtures.PASSWORD}).status_code, 400)
        with self.client.session_transaction() as sesion:
            sesion["panel_autorizado"] = True
        self.assertEqual(self.client.get(RUTA + "/1").status_code, 401)
        self.login("direccion")
        self.assertEqual(self.client.get(RUTA).status_code, 403)
        self.assertEqual(self.client.get(RUTA + "/1").status_code, 403)
        self.login()
        for filtro in ("fecha=2026-11-31", "estado=incorrecto", "pagina=0"):
            self.assertEqual(self.client.get(RUTA + "?" + filtro).status_code, 400)
        self.assertEqual(self.client.get(RUTA + "/999").status_code, 404)
        self.assertEqual(self.client.get(RUTA).json["sesiones"], [])
        with patch("sesiones_administracion.consultar", side_effect=sqlite3.OperationalError):
            self.assertEqual(self.client.get(RUTA).json["resultado"], "servicio_no_disponible")
            self.assertEqual(self.client.get(RUTA).status_code, 503)
        self.con.execute("UPDATE seguimiento_operadores SET estado = 'inactivo' WHERE id = 1")
        self.con.commit()
        self.assertEqual(self.client.get(RUTA).status_code, 401)
