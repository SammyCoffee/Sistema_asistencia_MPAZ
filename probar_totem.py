from base_datos import validar_totem


codigo = input("Ingrese el codigo del Tótem: ")

respuesta = validar_totem(codigo)

if respuesta["resultado"] == "activo":
    print("Tótem validado correctamente")
    print("Codigo:", respuesta["codigo"])
    print("Nombre:", respuesta["nombre"])
    print("Ubicacion:", respuesta["ubicacion"])
    print("Ultima conexion:", respuesta["ultima_conexion"]
          
elif respuesta["resultado"] == "inactivo":
    print("El Tótem existe, pero no esta activo")
    print("Codigo:", respuesta["codigo"]
    print("Nombre:", respuesta["nombre])

elif respuesta["resultado"] == "no_existe"
print("No existe un Tótem registrado con ese codigo") 
