from base_datos import asignar_tarjeta_por_rut


def main():
    rut = input("Ingrese el RUT del alumno: ")
    uid = input("Ingrese el UID de la tarjeta nueva: ")

    respuesta = asignar_tarjeta_por_rut(rut, uid)
    resultado = respuesta.get("resultado")

    if resultado == "asignada":
        print("Tarjeta asignada correctamente")
        print("Alumno:", respuesta["alumno"])
        print("Curso:", respuesta["curso"])
        print("UID nuevo:", respuesta["uid"])
        print("Fecha:", respuesta["fecha"])

    elif resultado == "alumno_no_existe":
        print("No existe un alumno registrado con ese RUT")

    elif resultado == "ya_tiene_tarjeta":
        print("El alumno ya tiene una tarjeta activa")
        print("Alumno:", respuesta["alumno"])
        print("UID activo:", respuesta["uid"])

    elif resultado == "uid_repetido":
        print("El UID ingresado ya está registrado")

    else:
        print("No se pudo procesar la asignación de la tarjeta")
        print("Resultado inesperado:", resultado)


if __name__ == "__main__":
    main()
