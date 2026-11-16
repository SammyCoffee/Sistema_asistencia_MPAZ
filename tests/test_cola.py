"""Durabilidad de cola solo en carpetas temporales ficticias."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
import runpy
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import cola_pendientes as cola


class ColaTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.ruta = Path(self.tmp.name) / 'pendientes.json'
        parche = patch.object(cola, 'RUTA_PENDIENTES', self.ruta)
        parche.start()
        self.addCleanup(parche.stop)

    def test_corrupcion_no_sobrescribe(self):
        original = '{incompleto'
        self.ruta.write_text(original)
        with self.assertRaises(ValueError):
            cola.agregar_pendiente({'evento_id': 'nuevo-ficticio'})
        self.assertEqual(self.ruta.read_text(), original)

    def test_interrupcion_escritura_conserva_original(self):
        cola.guardar_pendiente([{'evento_id': 'anterior'}])
        original = self.ruta.read_bytes()
        with patch('os.replace', side_effect=OSError('fallo simulado')):
            with self.assertRaises(OSError):
                cola.agregar_pendiente({'evento_id': 'nuevo'})
        self.assertEqual(self.ruta.read_bytes(), original)

    def test_altas_simultaneas(self):
        def alta(numero):
            cola.agregar_pendiente({'evento_id': f'ficticio-{numero}'})
        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(alta, range(30)))
        pendientes = cola.cargar_pendientes()
        self.assertEqual(len(pendientes), 30)
        self.assertEqual(len({p['evento_id'] for p in pendientes}), 30)
        cola.eliminar_pendiente('ficticio-0')
        self.assertEqual(len(cola.cargar_pendientes()), 29)

    def test_reenvio_conserva_eventos_nuevos(self):
        cola.guardar_pendiente([{'evento_id': 'anterior'}])
        class Respuesta:
            def __enter__(self):
                cola.agregar_pendiente({'evento_id': 'nuevo'})
                return self
            def __exit__(self, *args):
                pass
            def read(self):
                return b'{"resultado":"entrada_registrada"}'
        with patch.dict(os.environ, {'MPAZ_API_KEY': 'solo-ficticia'}), patch('urllib.request.urlopen', return_value=Respuesta()):
            runpy.run_path(str(Path(cola.__file__).with_name('reenviar_pendientes.py')), run_name='__main__')
        self.assertEqual(cola.cargar_pendientes(), [{'evento_id': 'nuevo'}])

    def test_procesos_simultaneos(self):
        codigo = (
            'import sys; from pathlib import Path; import cola_pendientes as c; '
            'c.RUTA_PENDIENTES=Path(sys.argv[1]); '
            '[c.agregar_pendiente({"evento_id":sys.argv[2]+str(i)}) for i in range(10)]'
        )
        procesos = [subprocess.Popen([sys.executable, '-c', codigo, str(self.ruta), str(numero)]) for numero in range(3)]
        for proceso in procesos:
            self.assertEqual(proceso.wait(timeout=10), 0)
        self.assertEqual(len(cola.cargar_pendientes()), 30)

    def test_timeout_de_reenvio_conserva_evento(self):
        with patch.dict(os.environ, {'MPAZ_API_KEY':'solo-ficticia'}):
            import reenviar_pendientes
        cola.agregar_pendiente({'evento_id':'timeout-ficticio'})
        with patch.object(reenviar_pendientes.request,'urlopen',side_effect=TimeoutError('Simulado')) as solicitud:
            procesado,respuesta=reenviar_pendientes.enviar_pendiente({'evento_id':'timeout-ficticio'})
        self.assertFalse(procesado)
        self.assertEqual(respuesta['resultado'],'sin_conexion')
        self.assertEqual(solicitud.call_args.kwargs['timeout'],10)
        self.assertEqual(len(cola.cargar_pendientes()),1)
