from datetime import datetime
from pathlib import Path
import shutil


RUTA_BASE_DATOS = Path(
    "data/asistencia.db"
)

CARPETA_RESPALDOS = Path(
    "respaldos"
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

    marca_tiempo = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    nombre_respaldo = (
        f"asistencia_{marca_tiempo}.db"
    )

    ruta_respaldo = (
        CARPETA_RESPALDOS
        / nombre_respaldo
    )

    shutil.copy2(
        RUTA_BASE_DATOS,
        ruta_respaldo
    )

    print("Respaldo creado correctamente")
    print("Base original:", RUTA_BASE_DATOS)
    print("Copia creada:", ruta_respaldo)

if __name__ == "__main__":
    respaldar_base_datos()    