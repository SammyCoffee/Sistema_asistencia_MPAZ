"""Compara las regresiones actuales con d0d2c80 sin copiar bases ni secretos.

Ejecutar desde la raíz con .venv/bin/python tests/reproducir_base.py.
Los fallos en la referencia son esperados: este comando no es la suite de CI.
"""
from pathlib import Path
import shutil
import subprocess
import tempfile
repo=Path.cwd()
with tempfile.TemporaryDirectory() as carpeta:
    dest=Path(carpeta)
    archivos=subprocess.check_output(['git','ls-tree','-r','--name-only','d0d2c80'],text=True).splitlines()
    for nombre in archivos:
        if Path(nombre).suffix not in {'.py','.js','.html','.css','.sql'}:
            continue
        archivo=dest/nombre
        archivo.parent.mkdir(parents=True,exist_ok=True)
        archivo.write_bytes(subprocess.check_output(['git','show',f'd0d2c80:{nombre}']))
    shutil.copytree(repo/'tests',dest/'tests',ignore=shutil.ignore_patterns('__pycache__'))
    for etiqueta,cmd in [('python',[str(repo/'.venv/bin/python'),'-m','unittest','discover','-s','tests','-v']),('js',['node','tests/test_interfaz.cjs'])]:
        resultado=subprocess.run(cmd,cwd=dest,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        Path(f'/tmp/mpaz-baseline-final-{etiqueta}.log').write_text(resultado.stdout)
        print(etiqueta, 'salida',resultado.returncode)
        for linea in resultado.stdout.splitlines():
            if linea.startswith(('Ran ','FAILED','FAIL:','ERROR:')): print(linea)
