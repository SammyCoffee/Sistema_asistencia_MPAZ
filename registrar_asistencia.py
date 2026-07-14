
from base_datos import buscar_alumno_por_uid, guardar_asistencia
from datetime import datetime
from lector_nfc import obtener_uid

uid_ingresado = obtener_uid()

alumno = buscar_alumno_por_uid(uid_ingresado)

if alumno:
    momento_actual = datetime.now()
    
    fecha = momento_actual.strftime("%Y-%m-%d")
    hora = momento_actual.strftime("%H:%M:%S")
    
    asistencia_guardada = guardar_asistencia(
        alumno[0],
        fecha,
        hora
    )
    if asistencia_guardada:
        print("Asistencia registrada correctamente")
        print("Alumno:", alumno[1])
        print("Curso:", alumno[2])
        print("Fecha:", fecha)
        print("Hora:", hora)
    else:
        print("La asistencia de este alumno ya fue registrada hoy")
        print("Alumno:", alumno[1])
        print("Curso:", alumno[2])
        print("Fecha:", fecha)
else:
    print("No existe un alumno con el UID ingresado")   
        
    