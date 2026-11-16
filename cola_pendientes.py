"""Cola local de simuladores: escritura atómica y exclusión entre procesos Linux."""
from contextlib import contextmanager
import fcntl
import json
import os
from pathlib import Path
import tempfile
from threading import RLock

RUTA_PENDIENTES = Path("lecturas_pendientes.json")
_BLOQUEO_HILOS = RLock()


@contextmanager
def _bloquear():
    # El archivo de lock es estable: no eliminarlo al liberar el bloqueo.
    with _BLOQUEO_HILOS:
        descriptor = os.open(str(RUTA_PENDIENTES) + ".lock", os.O_CREAT | os.O_RDWR, 0o600)
        with os.fdopen(descriptor, "a") as archivo:
            fcntl.flock(archivo, fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(archivo, fcntl.LOCK_UN)


def _validar(pendientes):
    if not isinstance(pendientes, list) or not all(isinstance(p, dict) for p in pendientes):
        raise ValueError("La cola debe contener una lista de eventos; conservar el archivo para revisión")


def _leer():
    if not RUTA_PENDIENTES.exists():
        return []
    # Una cola ilegible o corrupta no equivale a una cola vacía.
    pendientes = json.loads(RUTA_PENDIENTES.read_text(encoding="utf-8"))
    _validar(pendientes)
    return pendientes


def _guardar(pendientes):
    _validar(pendientes)
    temporal = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=RUTA_PENDIENTES.parent,
                                         prefix=RUTA_PENDIENTES.name + ".", suffix=".tmp",
                                         delete=False) as archivo:
            temporal = Path(archivo.name)
            json.dump(pendientes, archivo, ensure_ascii=False, indent=4)
            archivo.flush()
            os.fsync(archivo.fileno())
        os.replace(temporal, RUTA_PENDIENTES)
    finally:
        if temporal is not None and temporal.exists():
            temporal.unlink()  # Solo el temporal creado por esta operación.


def cargar_pendientes():
    with _bloquear():
        return _leer()


def guardar_pendiente(pendientes):
    """Reemplazo explícito de lista; no usar para confirmar snapshots enviados."""
    with _bloquear():
        _guardar(pendientes)


def agregar_pendiente(datos):
    if not isinstance(datos, dict):
        raise ValueError("Evento inválido")
    with _bloquear():
        pendientes = _leer()
        pendientes.append(datos)
        _guardar(pendientes)


def eliminar_pendiente(evento_id):
    with _bloquear():
        _guardar([p for p in _leer() if p.get("evento_id") != evento_id])
