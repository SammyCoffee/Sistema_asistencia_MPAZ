import sqlite3

conexion = sqlite3.connect("data/asistencia.db")


cursor = conexion.cursor()

cursor.execute(""" 
 CREATE TABLE IF NOT EXISTS alumnos (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               rut TEXT NOT NULL UNIQUE,
               nombre_completo TEXT NOT NULL,curso TEXT NOT NULL,uid TEXT NOT NULL UNIQUE
               )
               """             )

conexion.commit()

print("tabla de alumnos creada correctamente")

conexion.close()