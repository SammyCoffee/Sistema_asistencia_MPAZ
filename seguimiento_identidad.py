
"""Identidad individual de funcionarios MPAZ RFID."""

import re
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from base_datos import obtener_conexion

ROLES = {"administracion", "direccion"}

def crear_operador(nombre, usuario, contrasena, rol):
    """Uso interno: la API debera autorizar esta operacion."""
    if not all(isinstance(x, str) for x in
               (nombre, usuario, contrasena, rol)):
        return {"resultado": "datos_invalidos"}

    nombre = nombre.strip()
    usuario = usuario.strip().lower()

    if (not 5 <= len(nombre) <= 100
        or not re.fullmatch(r"[a-z0-9._-]{4,40}", usuario)
        or not 12 <= len(contrasena) <= 128
        or rol not in ROLES):
        return {"resultado": "datos_invalidos"}

    clave_hash = generate_password_hash(
        contrasena, method="scrypt"
    )

    con = obtener_conexion()
    try:
        cursor = con.execute("""
            INSERT INTO seguimiento_operadores
            (nombre_completo, usuario, password_hash, rol)
            VALUES (?, ?, ?, ?)
        """, (nombre, usuario, clave_hash, rol))
        con.commit()
        return {
            "resultado": "operador_creado",
            "id": cursor.lastrowid,
            "usuario": usuario,
            "rol": rol
        }
    except sqlite3.IntegrityError:
        con.rollback()
        return {"resultado": "usuario_existente"}
    finally:
        con.close()


def autenticar_operador(usuario, contrasena):
    """Comprueba credenciales sin exponer el hash."""
    error = {"resultado": "credenciales_invalidas"}

    if not isinstance(usuario, str) or not isinstance(contrasena, str):
        return error

    usuario = usuario.strip().lower()

    if not re.fullmatch(r"[a-z0-9._-]{4,40}", usuario):
        return error

    con = obtener_conexion()
    try:
        fila = con.execute("""
            SELECT id, nombre_completo, usuario,
                   password_hash, rol, estado
            FROM seguimiento_operadores
            WHERE usuario = ? COLLATE NOCASE
            LIMIT 1
        """, (usuario,)).fetchone()

        if fila is None or fila[5] != "activo":
            return error

        if fila[4] not in ROLES:
            return error

        if not check_password_hash(fila[3], contrasena):
            return error

        return {
            "resultado": "autenticado",
            "id": fila[0],
            "nombre": fila[1],
            "usuario": fila[2],
            "rol": fila[4]
        }
    finally:
        con.close()
