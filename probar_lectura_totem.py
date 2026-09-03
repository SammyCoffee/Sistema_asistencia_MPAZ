import uuid
from datetime import datetime

from procesar_lectura_totem import procesar_lectura_totem


def crear_evento_id(codigo_totem):
    codigo_totem = codigo_totem.strip().upper()
    fecha_hora = datetime.now().strftime("%Y%m%d-%H%M%S")
    codigo_aleatorio = uuid.uuid4().hex[:8].upper()

    return f"{codigo_totem}-{fecha_hora}-{codigo_aleatorio}"


def main():
    codigo_totem = input("Ingrese el código del tótem: ")
    uid = input("Ingrese el UID de la tarjeta: ")
    evento_id = crear_evento_id(codigo_totem)

    respuesta = procesar_lectura_totem(
        codigo_totem,
        uid,
        evento_id
    )

    print("Evento ID:", evento_id)
    print("Resultado:", respuesta.get("resultado"))
    print("Mensaje:", respuesta.get("mensaje"))

    if respuesta.get("alumno") is not None:
        print("Alumno:", respuesta.get("alumno"))
        print("Curso:", respuesta.get("curso"))
        print("Fecha:", respuesta.get("fecha"))

    if respuesta.get("hora") is not None:
        print("Hora:", respuesta.get("hora"))

    print("LED:", respuesta.get("led", "sin_indicacion"))
    print("Buzzer:", respuesta.get("buzzer", "sin_indicacion"))


if __name__ == "__main__":
    main()
