def obtener_uid():
    uid = input("Ingrese el UID del NFC: ")
    uid = uid.strip().replace(" ", "").upper()
    
    return uid