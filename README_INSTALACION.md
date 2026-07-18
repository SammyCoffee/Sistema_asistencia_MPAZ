# Instalación del Sistema MPAZ RFID

Esta guía permite instalar el proyecto en un computador nuevo sin compartir información privada de estudiantes ni claves reales.

## Requisitos

- Ubuntu o Linux Mint
- Python 3
- Git
- Visual Studio Code
- Conexión a Internet para instalar dependencias

## Archivos privados

Los siguientes archivos no se descargan desde GitHub:

- `.mpaz_api_key`
- `data/asistencia.db`
- `datos_privados/`
- `respaldos/`
- `reportes/`

Estos elementos deben trasladarse mediante un medio privado y seguro.

## 1. Descargar el proyecto

Abre una terminal y ejecuta:

```bash
git clone https://github.com/SammyCoffee/Sistema_asistencia_MPAZ.git



git add README_INSTALACION.md
git commit -m "Agrega guia de instalacion y traslado"
git push

git clone
crear .venv
instalar requirements.txt
crear la clave privada
copiar la base de datos de forma segura
iniciar api.py


