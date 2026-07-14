from base_datos import guardar_alumno

rut = input("Ingrese el rut del alumno: ")
nombre_completo = input("Ingrese el nombre completo del alumno: ")
curso = input("Ingrese el curso del alumno: ")
uid = input("Ingrese el uid del alumno: ")

rut = rut.strip()
nombre_completo = nombre_completo.strip()
curso = curso.strip().upper()
uid = uid.strip().replace(" ", "").upper()

if not rut or not nombre_completo or not curso or not uid:
    print("no se pudo agregar: todos los campos son obligatorios")

else:
    alumno_guardado = guardar_alumno(
        rut,
        nombre_completo,
        curso,
        uid
    )    
    
    if alumno_guardado:
        print("alumno agregado correctamente")
        print("RUT:", rut)
        print("Nombre:", nombre_completo)
        print("Curso:", curso)
        print("UID:", uid)
    else:
        print("No se pudo agregar: el RUT o el UID ya estan registrados")    
        
