"""Zona Chile y caracterización de reglas pendientes, sin alterar históricos."""
from datetime import datetime, timezone
import os
import time
import unittest
from unittest.mock import patch
import test_auditoria as fixtures
from reloj_escolar import ahora_chile
from calendario_administracion import guardar_jornada_escolar
from consultar_asistencia import obtener_inasistencias, obtener_atrasos
import consultar_asistencia
import registrar_asistencia


class TiempoCalendarioTest(unittest.TestCase):
    setUp = fixtures.SistemaTest.setUp

    def test_transiciones_chile_2026(self):
        casos = [
            ('2026-04-05T02:59:59+00:00', '2026-04-04T23:59:59-03:00'),
            ('2026-04-05T03:00:00+00:00', '2026-04-04T23:00:00-04:00'),
            ('2026-09-06T03:59:59+00:00', '2026-09-05T23:59:59-04:00'),
            ('2026-09-06T04:00:00+00:00', '2026-09-06T01:00:00-03:00'),
        ]
        for utc, civil in casos:
            with self.subTest(utc=utc):
                self.assertEqual(ahora_chile(datetime.fromisoformat(utc)).isoformat(), civil)
        with self.assertRaises(ValueError):
            ahora_chile(datetime(2026, 1, 1))

    def test_registro_y_consulta_independientes_de_tz_proceso(self):
        anterior = os.environ.get('TZ')
        os.environ['TZ'] = 'UTC'; time.tzset()
        try:
            instante = ahora_chile(datetime(2026, 11, 17, 1, 0, tzinfo=timezone.utc))
            with patch.object(registrar_asistencia, 'ahora_chile', return_value=instante), patch.object(fixtures.bd, 'ahora_chile', return_value=instante):
                respuesta = registrar_asistencia.procesar_asistencia('AABBCCDD', 1, 'zona-demo')
            self.assertEqual(respuesta['fecha'], '2026-11-16')
            self.assertEqual(respuesta['hora'], '22:00:00')
            with patch.object(consultar_asistencia, 'hoy_chile', return_value=instante.date()):
                self.assertEqual(consultar_asistencia.obtener_rango_periodo('diario'), ('2026-11-16','2026-11-16'))
        finally:
            if anterior is None: os.environ.pop('TZ', None)
            else: os.environ['TZ'] = anterior
            time.tzset()

    def test_caracteriza_inasistencia_en_dia_no_lectivo(self):
        # Caracterización de defecto existente: aprobado significa reproducido, NO corregido.
        for fecha, condicion in [('2026-11-16','feriado'),('2026-11-17','suspendida')]:
            guardar_jornada_escolar(self.con, accion='crear', fecha=fecha, condicion=condicion, motivo='Prueba ficticia no lectiva')
            fixtures.bd.guardar_asistencia(1, fecha, '08:00:00', 1, fecha)
            filas = obtener_inasistencias('diario', fecha)
            alumno_sin_lectura = next(f for f in filas if f[0] == 2)
            self.assertEqual(alumno_sin_lectura[3], 1)  # Riesgo documentado para decisión institucional.

    def test_caracteriza_fin_semana_y_dia_sin_lecturas(self):
        fixtures.bd.guardar_asistencia(1,'2026-11-15','08:00:00',1,'domingo')
        self.assertEqual(next(f for f in obtener_inasistencias('diario','2026-11-15') if f[0]==2)[3], 1)
        self.assertEqual(next(f for f in obtener_inasistencias('diario','2026-11-16') if f[0]==2)[4], 0)

    def test_caracteriza_atraso_jornada_especial(self):
        guardar_jornada_escolar(self.con, accion='crear', fecha='2026-11-16', condicion='horario_especial', hora_entrada='10:00', hora_salida='15:00', motivo='Prueba ficticia especial')
        fixtures.bd.guardar_asistencia(1,'2026-11-16','09:00:00',1,'especial')
        self.assertEqual(len(obtener_atrasos('diario','2026-11-16')),1)  # Aplica 08:20 fijo, no las 10:00.

    def test_caracteriza_cierre_entrada_despues_17(self):
        fixtures.bd.guardar_asistencia(1,'2026-11-16','18:00:00',1,'tarde')
        with patch.object(fixtures.bd,'ahora_chile',return_value=ahora_chile(datetime(2026,11,16,22,tzinfo=timezone.utc))):
            fixtures.bd.cerrar_jornadas_pendientes()
        entrada,salida=self.con.execute('SELECT hora_entrada,hora_salida FROM asistencias').fetchone()
        self.assertLess(salida,entrada)  # Defecto de regla existente, no resultado correcto para asistencia.

    def test_caracteriza_periodo_semanal_consulta_exportacion(self):
        import exportar_asistencias_csv
        consulta=consultar_asistencia.obtener_rango_periodo('semanal','2026-11-16')
        with patch.object(exportar_asistencias_csv,'hoy_chile',return_value=datetime(2026,11,16).date()):
            exportacion=exportar_asistencias_csv.obtener_rango_fechas('semanal')
        self.assertEqual(consulta,('2026-11-16','2026-11-22'))
        self.assertEqual(exportacion,('2026-11-10','2026-11-16'))
        self.assertNotEqual(consulta,exportacion)  # Decidir semana calendario vs últimos siete días.
