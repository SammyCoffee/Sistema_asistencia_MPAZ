"""Flujos API aislados adicionales: no son llamadas al servidor escolar."""
from datetime import datetime, timezone
from unittest.mock import patch
import unittest
import test_auditoria as fixtures
from reloj_escolar import ahora_chile
import registrar_asistencia
import exportar_asistencias_csv


class ApiFlujosTest(unittest.TestCase):
    setUp=fixtures.SistemaTest.setUp
    login=fixtures.SistemaTest.login

    def test_lectura_api_entrada_reintento_salida(self):
        datos={'codigo_totem':'DEMO','uid':'aa bb cc dd','evento_id':'api-e1'}
        cab={'X-API-Key':fixtures.api.API_KEY}
        for instante, evento, esperado in [('2026-11-16T11:00:00+00:00','api-e1','entrada_registrada'), ('2026-11-16T11:00:10+00:00','api-e1','evento_repetido'), ('2026-11-16T11:00:30+00:00','api-e2','salida_registrada')]:
            datos['evento_id']=evento
            reloj=ahora_chile(datetime.fromisoformat(instante))
            with patch.object(registrar_asistencia,'ahora_chile',return_value=reloj), patch.object(fixtures.bd,'ahora_chile',return_value=reloj):
                respuesta=self.client.post('/lectura',json=datos,headers=cab)
            self.assertEqual(respuesta.status_code,200)
            self.assertEqual(respuesta.json['resultado'],esperado)
        self.assertEqual(self.con.execute('SELECT fecha,hora_entrada,hora_salida,totem_entrada_id,totem_salida_id FROM asistencias').fetchone(),('2026-11-16','08:00:00','08:00:30',1,1))

    def test_exportacion_http_y_filtro_curso(self):
        self.login()
        hoy=exportar_asistencias_csv.hoy_chile().isoformat()
        fixtures.bd.guardar_asistencia(1,hoy,'08:00:00',1,'exportacion')
        with patch.object(exportar_asistencias_csv,'CARPETA_REPORTES', fixtures.Path(self.tmp.name)):
            respuesta=self.client.get('/asistencias/exportar/diario?curso=2A')
            try:
                self.assertEqual(respuesta.status_code,200)
                self.assertEqual(respuesta.mimetype,'text/csv')
                self.assertIn('attachment',respuesta.headers['Content-Disposition'])
                texto=respuesta.get_data().decode('utf-8-sig')
                self.assertEqual(len(texto.splitlines()),1)
            finally:
                respuesta.close()

    def test_calendario_api_habilitacion_csrf_actor(self):
        self.login()
        datos={'fecha':'2026-11-16','condicion':'suspendida','motivo':'Solo prueba ficticia'}
        ruta='/panel/calendario/jornadas/registrar'
        self.assertEqual(self.client.post(ruta,json=datos).status_code,403)
        with patch.dict('os.environ',{'MPAZ_CALENDARIO_ESCRITURA_HABILITADA':'si'}):
            self.assertEqual(self.client.post(ruta,json=datos).status_code,403)
            token=self.client.get('/panel/calendario/token').json['csrf_token']
            respuesta=self.client.post(ruta,json=datos,headers={'X-CSRF-Token':token})
        self.assertEqual(respuesta.status_code,201)
        self.assertEqual(self.con.execute('SELECT count(*) FROM calendario_jornadas').fetchone()[0],1)
        self.assertEqual(self.con.execute('SELECT actor FROM calendario_auditoria').fetchone()[0],'operador:1')
