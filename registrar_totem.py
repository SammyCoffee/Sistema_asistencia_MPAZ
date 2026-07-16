from base_datos import guardar_totem


codigo = input("Ingrese el codigo del Tótem: ")
nombre = input("Ingrese el nombre del Tótem: ")
ubicacion = input("Ingrese la ubicacion del Tótem: ")


codigo = codigo.strip()
nombre = nombre.strip()
ubicacion = ubicacion.strip()

if not codigo or not nombre or not ubicacion:
    print("No se pudo registrar: todos los campos son obligatorios")

else:
    respuesta = guardar_totem(
        codigo,
        nombre,
        ubicacion
    )

    if respuesta["resultado"] == "registrado":
        print("Tótem registrado correctamente")
        print("Codigo:", respuesta["codigo"])
        print("Nombre:", respuesta["nombre"])
        print("Ubicacion:", respuesta["ubicacion"])
        print("Estado:", respuesta["estado"])
        print("Fecha de registro:", respuesta["fecha_registro"])

    elif respuesta["resultado"] == "codigo_repetido":
        print ("No se pudo registrar: el codigo del Tótem ya existe")    