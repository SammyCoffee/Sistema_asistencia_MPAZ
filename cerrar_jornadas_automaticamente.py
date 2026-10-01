from base_datos import cerrar_jornadas_pendientes


def main():
    resultado = cerrar_jornadas_pendientes()

    print("Cierre automatico de jornadas")
    print("-----------------------------")
    print("Fecha:", resultado["fecha"])
    print(
        "Jornadas anteriores cerradas:",
        resultado["jornadas_anteriores"]
    )
    print(
        "Jornadas de hoy cerradas:",
        resultado["jornadas_hoy"]
    )


if __name__ == "__main__":
    main()