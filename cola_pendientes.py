import json
from pathlib import Path


RUTA_PENDIENTES = Path("lecturas_pendientes.json")


def cargar_pendientes():
    if not RUTA_PENDIENTES.exists():
        return []
    
    try:
        contenido = RUTA_PENDIENTES.read_text(
            encoding="utf-8"
        )

        if not contenido.strip():
            return []
        
        return json.loads(contenido)
    
    except (json.JSONDecodeError, OSError):
        return []
    
def guardar_pendiente(pendientes):
    contenido = json.dumps(
        pendientes,
        ensure_ascii=False,
        indent=4
    )

    RUTA_PENDIENTES.write_text(
        contenido,
        encoding="utf-8"
    )

def agregar_pendiente(datos):
    pendientes = cargar_pendientes()
    pendientes.append(datos)
    guardar_pendiente(pendientes)
    

def eliminar_pendiente(evento_id):
    pendientes = cargar_pendientes()

    pendientes_restantes = []

    for pendiente in pendientes:
        if pendiente.get("evento_id") !=evento_id:
            pendientes_restantes.append(pendiente)

    guardar_pendiente(pendientes_restantes)            
        