from base_datos import asignar_tarjeta_por_rut

rut = input("Ingrese el RUT del alumno: ")
uid = input("Ingrese el UID de la tarjeta nueva: ")

respuesta = asignar_tarjeta_por_rut(rut, uid)

if respuesta["resultado"] == "asignada":
    print("tarjeta asignada correctamente")
    print("alumno:", respuesta["alumno"])
    print("Curso:", respuesta["curso"])
    print("UID nueco:", respuesta["uid"])
    print("Fecha:", respuesta["fecha"])

elif respuesta["resultado"] == "alumno_no_existe":
    print("no existe un alumno registrado con ese RUT")

elif respuesta["resultado"] == "ya_tiene_tarjeta":
    print("El alumno ya tiene una tarjeta activa")
    print("Alumno:", respuesta["alumno"])
    print("UID activo", respuesta["uid"])

elif respuesta["resultado"] == "uid_registrado":
    print("El UID ingresado ya esta registrado ")    