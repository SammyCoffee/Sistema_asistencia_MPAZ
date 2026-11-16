from reloj_escolar import ahora_chile
from datetime import datetime
from pathlib import Path
import os
import sqlite3
from uuid import uuid4


RUTA_BASE_DATOS = Path(
    os.getenv("MPAZ_DB_PATH", "data/asistencia.db")
)

CARPETA_RESPALDOS = Path(
    os.getenv("MPAZ_BACKUP_DIR", "/srv/mpaz-data/backups/rfid")
)


def respaldar_base_datos():
    if not RUTA_BASE_DATOS.exists():
        print("No se encontro la base ded datos:")
        print(RUTA_BASE_DATOS)
        return
    
    CARPETA_RESPALDOS.mkdir(
        parents=True,
        exist_ok=True
    )

    marca_tiempo = ahora_chile().strftime(
        "%Y%m%d_%H%M%S"
    )

    nombre_respaldo = (
        f"asistencia_{marca_tiempo}_{uuid4().hex}.db"
    )

    ruta_respaldo = (
        CARPETA_RESPALDOS
        / nombre_respaldo
    )

    # Reserva un archivo privado y único; nunca sobrescribe un respaldo.
    descriptor = os.open(ruta_respaldo, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(descriptor)
    origen = sqlite3.connect(RUTA_BASE_DATOS.resolve().as_uri() + "?mode=ro", uri=True)
    destino = sqlite3.connect(ruta_respaldo)
    try:
        origen.backup(destino)
        if destino.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise RuntimeError("El respaldo no superó la verificación de integridad")
        if destino.execute("PRAGMA foreign_key_check").fetchall():
            raise RuntimeError("El respaldo contiene referencias inconsistentes")
    finally:
        destino.close()
        origen.close()

    print("Respaldo creado correctamente")
    print("Base original:", RUTA_BASE_DATOS)
    print("Copia creada:", ruta_respaldo)
    return ruta_respaldo

if __name__ == "__main__":
    respaldar_base_datos()    
