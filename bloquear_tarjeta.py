from base_datos import bloquear_tarjeta


uid = input("ingrese el UID de la tarjeta que desea bloquear: ")

tarjeta_bloqueada = bloquear_tarjeta(uid)

if tarjeta_bloqueada:
    print("Tarjeta bloqueada correctamente")
    
else:
    print("no se encontro una tarjeta activa con ese UID")
        
