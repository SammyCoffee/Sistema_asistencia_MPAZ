from base_datos import obtener_conexion



conexion = obtener_conexion()
cursor = conexion.cursor()

try:

    cursor.execute("PRAGMA table_info(totems)")

    columnas = cursor.fetchall()
    nombres_columnas = []

    for columna in columnas:
        nombres_columnas.append(columna[1])

    if "estado" in nombres_columnas:
        print("La columna estado ya existe")

    else: 
        cursor.execute(
            """
            ALTER TABLE totems
            ADD COLUMN estado TEXT NOT NULL DEFAULT 'activo'    
            """
        )    

        conexion.commit()

        print("Columna estado agregado correctamente")


finally:
    conexion.close()   