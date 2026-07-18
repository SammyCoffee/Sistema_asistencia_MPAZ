from collections import Counter
from datetime import datetime
from pathlib import Path

from base_datos import obtener_conexion
from revisar_excel_estudiantes import (
    normalizar_rut,
    rut_es_valido
)

from simular_importacion_estudiantes import (
    leer_estudiantes_excel
)

RUTA_EXCEL = Path(
    "datos_privados/REGISTRO DATOS.xlsx"
)

CARPETA_RESPALDOS = Path(
    "respaldos"
)

CARPETA_INFORMES = Path(
    "datos_privados"
)

def existe_respaldo():
    respaldos = list(
        CARPETA_RESPALDOS.glob(
            "asistencia_*.db"
        )
    )
    return len(respaldos) > 0

def obtener_ruts_existentes(cursor):
    cursor.execute(
        """
        SELECT rut
        FROM alumnos
        """
    )    

    registros = cursor.fetchall()

    ruts_existentes = set()

    for registro in registros:
        rut = normalizar_rut(
            registro[0]
        )

        if rut:
            ruts_existentes.add(rut)

    return ruts_existentes

def clasificar_estudiantes(
        estudiantes,
        ruts_existentes
):
    ruts_excel = Counter(
        estudiante["rut"]
        for estudiante in estudiantes
        if estudiante["rut"]
    )        

    estudiantes_aptos = []
    estudiantes_omitidos = []

    for estudiante in estudiantes:
        motivos = []

        rut = estudiante["rut"]
        nombre = estudiante["nombre_completo"]
        curso = estudiante["curso"]


        if not rut:
            motivos.append(
                "RUT vacio o con formato incorrecto"
            )

        else:
            if not rut_es_valido(rut):
                motivos.append(
                    "RUT con digito verificador invalido"
                )
            if ruts_excel[rut] > 1:
                motivos.append(
                    "RUT repetido dentro del Excel"
                )

            if rut in ruts_existentes:
                motivos.append(
                    "El estudiante ya existe en SQLite"

                )

        if not nombre:
            motivos.append(
                "Nombre incompleto"
            )

        if not curso:
            motivos.append(
                "Curso Vacio"
            )
        if motivos:
            estudiantes_omitidos.append(
                {
                    **estudiante,
                    "motivos": motivos
                }
            )                   
        else:
            estudiantes_aptos.append(
                estudiante
            )
    return (
        estudiantes_aptos,
        estudiantes_omitidos
    )

def guardar_informe(
        leidos,
        importados,
        omitidos,
        total_base_datos
):

        CARPETA_INFORMES.mkdir(
            parents=True,
            exist_ok=True
        )

        marca_tiempo = datetime.now().strftime(
            "%Y%m%d-%H%M%S"
        )

        ruta_informe = CARPETA_INFORMES / (
            f"resultado_importacion_{marca_tiempo}.txt"
        )        

        lineas = [
            "RESULTADO DE IMPORTACION DE ESTUDIANTES"
            "=" * 50,
            f"Registros leidos del Excel: {leidos}",
            f"Estudiantes importados: {importados}",
            f"Registros omitidos: {omitidos}",
            f"Total de alumnos en SQLite: {total_base_datos}",
            "Tarjetas RFID asignadas: 0",
            "",
            "Los registros omitidos permanecen fuera de SQLite.",
            "Las tarjetas RFID deberan asignarse posteriormente"


        ]

        ruta_informe.write_text(
            "\n".join(lineas),
            encoding="utf-8"
        )

        return ruta_informe

def importar_estudiantes():
    if not RUTA_EXCEL.exists():
        print("No se encontro el Excel:")
        print(RUTA_EXCEL)
        return
    
    if not existe_respaldo():
        print(
            "importacion cancelada: "
            "no existe un respaldo de la base de datos."
        )
        return
    estudiantes = leer_estudiantes_excel()

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try: 
        ruts_existentes = obtener_ruts_existentes(
            cursor
        )

        (
            estudiantes_aptos,
            estudiantes_omitidos
        ) = clasificar_estudiantes(
            estudiantes,
            ruts_existentes
        )

        print("IMPORTACION DE ESTUDIANTES")
        print("=" * 40)
        print(
            "Registrados leidos:",
            len(estudiantes)
        )
        print(
            "Aptos para importar:",
            len(estudiantes_aptos)
        )
        print(
            "Omitidos:",
            len(estudiantes_omitidos)
        )
        print(
            "Alumnos actuales en SQLite:",
            len(ruts_existentes)
        )
        print("")
        print(
            "Las tarjetas RFID no seran creadas."
        )

        if not estudiantes_aptos:
            print(
                "No existen estudiantes nuevos "
                "para importar."
            )
            conexion.close()
            return
        
        frase_confirmacion = (
            f"IMPORTAR "
            f"{len(estudiantes_aptos)} "

            f"ESTUDIANTES"
        )

        print("")
        print(
                "Escribe exactamente esta frase "
                "para continuar:"
        )
        print(frase_confirmacion)

        confirmacion = input(">").strip()

        if confirmacion != frase_confirmacion:
            print("Importacion cancelada")
            conexion.close()
            return
        
        datos_para_insertar = [
            (
                estudiante["rut"],
                estudiante["nombre_completo"],
                estudiante["curso"]
            )
            for estudiante in estudiantes_aptos
        ]

        cursor.execute(
            "BEGIN IMMEDIATE"
        )

        cursor.executemany(
            """
            INSERT INTO alumnos (
            rut,
            nombre_completo,
            curso
            
        )
        Values (?, ?, ?)
        """,
        datos_para_insertar

        )

        conexion.commit()


        cursor.execute(
                """
                SELECT COUNT(*)
                FROM alumnos
                """   
        )

        total_base_datos = cursor.fetchone()[0]

    except Exception as error:
        conexion.rollback()


        print("Ocurrio un error durante la importacion")
        print(error)
        print(
            "Los cambios fueron cancelados."
        )

        conexion.close()
        return
    
    conexion.close()

    ruta_informe = guardar_informe(
        leidos=len(estudiantes_aptos),
        importados=len(estudiantes_aptos),
        omitidos=len(estudiantes_omitidos),
        total_base_datos=total_base_datos
    )

    print("")
    print("Importacion completada correctamente")
    print("=" * 40)
    print(
        "Estudiantes importados:",
        len(estudiantes_aptos)
    )
    print(
        "Registrados omitidos:",
        len(estudiantes_omitidos)
    )
    print(
        "Total de alumnos en SQLite:",
        total_base_datos
    )
    print(
        "Tarjetas RFID asignadas: 0"
    )
    print(
        "Informe privado:",
        ruta_informe
    )

if __name__ == "__main__":
    importar_estudiantes()
