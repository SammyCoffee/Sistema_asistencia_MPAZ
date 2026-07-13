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


cursor.execute(""" 
 CREATE TABLE IF NOT EXISTS asistencia (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               alumno_id INTEGER NOT NULL,
               fecha TEXT NOT NULL,
               hora TEXT NOT NULL,
               FOREIGN KEY (alumno_id) REFERENCES alumnos(id)
               )
               """             )
conexion.commit()

print("tablas creadas correctamente")

conexion.close()