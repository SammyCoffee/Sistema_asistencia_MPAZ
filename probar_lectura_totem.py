from procesar_lectura_totem import procesar_lectura_totem


codigo_totem = input("Ingrese el codigo del Tótem: ")
uid = input("Ingrese el UID de la tarjeta: ")

respuesta = procesar_lectura_totem(
    codigo_totem,
    uid
)

print("Resultado:", respuesta["resultado"])
print("Mensaje:", respuesta["mensaje"])

if "alumno" in respuesta:
    print("Alumno:", respuesta["alumno"])
    print("Curso:", respuesta["curso"])
    print("Fecha:", respuesta["fecha"])

if"hora" in respuesta:
    print("Hora:", respuesta["hora"])

print("LED:", respuesta["led"])
print("Buzzer:", respuesta["buzzer"])