"""Verificación de enlaces de assets; no reemplaza navegador ni accesibilidad."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import unittest


class RecursosTest(unittest.TestCase):
    def test_scripts_y_estilos_locales_existen(self):
        raiz=Path(__file__).resolve().parents[1]/'interfaz_prueba'
        class Parser(HTMLParser):
            def __init__(self): super().__init__(); self.refs=[]
            def handle_starttag(self,tag,attrs):
                a=dict(attrs)
                if tag=='script' and 'src' in a: self.refs.append(a['src'])
                if tag=='link' and a.get('rel')=='stylesheet': self.refs.append(a['href'])
        for archivo in raiz.rglob('*.html'):
            parser=Parser(); parser.feed(archivo.read_text())
            for ref in parser.refs:
                url=urlsplit(ref)
                if url.scheme or url.netloc: continue
                target=raiz/url.path.lstrip('/') if url.path.startswith('/') else archivo.parent/url.path
                with self.subTest(archivo=archivo.name,recurso=ref):
                    self.assertTrue(target.is_file())
