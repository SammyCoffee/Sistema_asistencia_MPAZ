# Desarrollo local sin datos escolares

## Requisitos

Python 3.12 (versión objetivo del servidor), Git y las dependencias fijadas en `requirements.txt`. Node permite ejecutar la prueba JavaScript, pero no es dependencia de producción. Gunicorn es parte del despliegue existente; no está fijado en `requirements.txt`, pendiente de inventariar y fijar por separado.

La auditoría se ejecutó en Python 3.14.8 y Node 26.12.0; queda pendiente repetirla en Python 3.12. No se instalaron dependencias en el servidor.

```bash
git clone --branch integration/seguridad-seguimiento https://github.com/SammyCoffee/Sistema_asistencia_MPAZ.git
cd Sistema_asistencia_MPAZ
git status --short --branch
git switch -c desarrollo/nombre-del-cambio
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
node tests/test_interfaz.cjs
```

No copiar la base de producción ni abrir respaldos versionados. Las pruebas crean y eliminan únicamente sus carpetas temporales.

## Variables de entorno

| Variable | Uso | Desarrollo |
|---|---|---|
| `MPAZ_SESSION_SECRET` | Firma de cookies Flask; obligatoria | Generar valor exclusivo local; nunca versionarlo |
| `MPAZ_API_KEY` | Autenticación de `/lectura`; obligatoria | Valor ficticio local; no usar clave institucional |
| `MPAZ_DB_PATH` | Ruta SQLite | Usar ruta absoluta a base vacía fuera del repositorio |
| `MPAZ_COOKIE_SECURE` | Atributo Secure de cookie | Por defecto `1`; `0` únicamente para HTTP en localhost |
| `MPAZ_CALENDARIO_ESCRITURA_HABILITADA` | Habilita escrituras de jornadas | Deshabilitada por defecto; `si` solo en prueba aislada o mediante decisión institucional |
| `MPAZ_BACKUP_DIR` | Destino de copias verificadas | Ruta privada de pruebas; producción conserva destino `/srv/mpaz-data/backups/rfid` |
| `MPAZ_API_URL` | Clientes de simulación/reenvío | Consultar cada script: unos esperan base URL, otros URL completa `/lectura` |

`MPAZ_PANEL_PASSWORD` ya no se usa. No reintroducir el login compartido.

## Iniciar una base nueva y vacía

Elegir una carpeta privada nueva. Este ejemplo se detiene si el archivo ya existe; no usar rutas de la escuela.

```bash
export MPAZ_DB_PATH="$(mktemp -d /tmp/mpaz-desarrollo.XXXXXX)/ficticia.db"
export MPAZ_SESSION_SECRET="$(.venv/bin/python -c 'import secrets; print(secrets.token_hex(32))')"
export MPAZ_API_KEY="solo-simulacion-local"
export MPAZ_COOKIE_SECURE=0
.venv/bin/python - <<'PY'
from pathlib import Path
import base_datos as bd
ruta = Path(bd.RUTA_BASE_DATOS)
assert not ruta.exists(), 'Usar una base nueva; no modificar una existente'
bd.crear_tablas()
con = bd.obtener_conexion()
try:
    for archivo in sorted(Path('migraciones').glob('*.sql')):
        con.executescript(archivo.read_text())
finally:
    con.close()
PY
.venv/bin/flask --app api run --host 127.0.0.1 --port 5000
```

Este procedimiento crea estructura, no estudiantes ni operadores. Las cuentas ficticias y escenarios completos están definidos en `tests/test_auditoria.py`. No ejecutar `crear_base_demostracion.py` ni migradores históricos sobre una base existente sin revisar sus efectos.

## Verificación

```bash
.venv/bin/python -m unittest discover -s tests -v
node tests/test_interfaz.cjs
.venv/bin/python -m compileall -q -x '/(\.venv|\.git)/' .
git diff --check
```

La prueba JavaScript usa un DOM mínimo: no acredita contraste, diseño adaptable, navegación de teclado ni funcionamiento completo del navegador.
