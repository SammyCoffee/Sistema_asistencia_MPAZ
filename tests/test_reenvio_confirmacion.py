"""Confirmación funcional y pérdida de respuesta, con cola ficticia temporal."""
from http.client import RemoteDisconnected
import json
import os
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
import cola_pendientes as cola


class ReenvioConfirmacionTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        p=patch.object(cola,'RUTA_PENDIENTES',Path(self.tmp.name)/'ficticia.json')
        p.start(); self.addCleanup(p.stop)
        with patch.dict(os.environ,{'MPAZ_API_KEY':'solo-ficticia-carga'}):
            import reenviar_pendientes
        self.mod=reenviar_pendientes
        cola.agregar_pendiente({'evento_id':'ficticio-carga'})

    def respuesta(self, contenido):
        class Respuesta:
            def __enter__(self): return self
            def __exit__(self,*args): pass
            def read(self): return contenido
        return Respuesta()

    def test_http200_no_confirma_error_o_rechazo(self):
        for resultado in ['error_interno','tarjeta_bloqueada','alumno_inactivo','tarjeta_desconocida','desconocido']:
            with self.subTest(resultado=resultado), patch.object(self.mod.request,'urlopen',return_value=self.respuesta(json.dumps({'resultado':resultado}).encode())):
                procesado,respuesta=self.mod.enviar_pendiente({'evento_id':'ficticio-carga'})
                self.assertFalse(procesado)
                self.assertEqual(respuesta['resultado'],resultado)
        self.assertEqual(len(cola.cargar_pendientes()),1)

    def test_confirmacion_funcional_y_reglas_terminales(self):
        for resultado in ['entrada_registrada','salida_registrada','evento_repetido','lectura_repetida','jornada_completa']:
            with self.subTest(resultado=resultado), patch.object(self.mod.request,'urlopen',return_value=self.respuesta(json.dumps({'resultado':resultado}).encode())):
                self.assertTrue(self.mod.enviar_pendiente({'evento_id':'ficticio-carga'})[0])

    def test_respuesta_cortada_conserva_evento(self):
        with patch.object(self.mod.request,'urlopen',side_effect=RemoteDisconnected('Fallo ficticio tras commit')):
            procesado,respuesta=self.mod.enviar_pendiente({'evento_id':'ficticio-carga'})
        self.assertFalse(procesado)
        self.assertEqual(respuesta['resultado'],'sin_conexion')
        self.assertEqual(len(cola.cargar_pendientes()),1)

    def test_respuesta_invalida_conserva_evento(self):
        for contenido in [b'{cortado', b'[]', b'null', b'{}', b'\xff']:
            with self.subTest(contenido=contenido), patch.object(self.mod.request,'urlopen',return_value=self.respuesta(contenido)):
                procesado,respuesta=self.mod.enviar_pendiente({'evento_id':'ficticio-carga'})
                self.assertFalse(procesado)
                self.assertEqual(respuesta['resultado'],'respuesta_invalida')
        self.assertEqual(len(cola.cargar_pendientes()),1)
