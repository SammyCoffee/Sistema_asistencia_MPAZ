from collections import Counter, defaultdict
from pathlib import Path

from openpyxl import load_workbook


RUTA_EXCEL = Path(
    "datos_privados/REGISTRO DATOS.xlsx"
)

RUTA_INFORME = Path(
    "datos_privado/revision_estudiantes.txt"
)
NOMBRE_HOJA = "ESTUDIANTE"

def limpiar_texto(valor)
    if valor is None:
        return ""
    
    return " ".join(
        str(valor).strip().split()
    )

def normalizar_rut(rut):
    rut = limpiar_texto(rut).upper()

    rut = (
        rut.replace(".", "")
        .replace(".", "")
        .replace(" ", "")
    )

    if len(rut) < 2:
        return ""
    
    cuerpo = rut[:-1]
    digito_verificador = rut[-1]


    if not cuerpo.isdigit():
        return ""
    
    if not (
        digito_verificador.isdigit()
        or digito_verificador == "K"
    ):
        return ""