# Manual Técnico — Sistema MPAZ RFID

## 1. Descripción general

El Sistema MPAZ RFID es una plataforma de registro de asistencia escolar mediante tarjetas RFID.

Cada estudiante utiliza una tarjeta personal. El tótem instalado en la entrada lee el UID de la tarjeta y envía la información a una API desarrollada en Python con Flask.

El servidor valida:

- Que el tótem esté registrado y activo.
- Que la tarjeta exista y esté activa.
- Que la tarjeta esté asociada a un estudiante.
- Que el estudiante no haya registrado asistencia previamente durante el mismo día.
- Que el mismo evento no sea procesado más de una vez.

## 2. Arquitectura general

```text
Tarjeta RFID
      ↓
Lector PN532
      ↓
ESP32 DevKit V1
      ↓ WiFi / HTTP
API Flask
      ↓
Base de datos SQLite
      ↓
Reportes de asistencia
## 6. Comunicación entre el ESP32 y la API

El ESP32 debe enviar una petición HTTP de tipo:

```text
POST /lectura
```

Dirección de ejemplo:

```text
http://IP_DEL_SERVIDOR:5000/lectura
```

La petición debe incluir esta cabecera:

```text
X-API-Key: CLAVE_PRIVADA
```

El contenido debe enviarse en formato JSON:

```json
{
  "codigo_totem": "MPAZ-ENTRADA-01",
  "uid": "A1B2C3D4",
  "evento_id": "MPAZ-ENTRADA-01-20260718-080000-ABC123"
}
```

### Significado de los campos

- `codigo_totem`: identifica el dispositivo que realizó la lectura.
- `uid`: identificador leído desde la tarjeta RFID.
- `evento_id`: identificador único de la lectura.

El `evento_id` permite reenviar una lectura sin registrarla dos veces.

## 7. Respuestas visuales y sonoras

### Asistencia registrada

```text
Resultado: registrada
LED: verde
Buzzer: un_pitido_corto
```

### Asistencia ya registrada durante el día

```text
Resultado: duplicada
LED: amarillo
Buzzer: dos_pitidos_cortos
```

### Evento recibido anteriormente

```text
Resultado: evento_repetido
LED: amarillo
Buzzer: dos_pitidos_cortos
```

### Tarjeta bloqueada

```text
Resultado: tarjeta_bloqueada
LED: rojo
Buzzer: un_pitido_largo
```

### Tarjeta desconocida

```text
Resultado: tarjeta_desconocida
LED: rojo
Buzzer: un_pitido_largo
```

### Tótem no autorizado o inactivo

```text
Resultado: totem_no_autorizado o totem_inactivo
LED: rojo
Buzzer: un_pitido_largo
```

## 8. Funcionamiento sin conexión

Si el tótem no logra comunicarse con la API, la lectura puede guardarse temporalmente en:

```text
lecturas_pendientes.json
```

El archivo se administra mediante:

```text
cola_pendientes.py
```

Para reenviar las lecturas cuando vuelva la conexión:

```bash
python3 reenviar_pendientes.py
```

Cada lectura conserva su `evento_id`, evitando duplicados en el servidor.

## 9. Pruebas con datos ficticios

Crear la base de demostración:

```bash
python3 crear_base_demostracion.py
```

Seleccionarla temporalmente:

```bash
export MPAZ_DB_PATH='data/asistencia_demo.db'
```

Seleccionar el tótem ficticio:

```bash
export CODIGO_TOTEM='MPAZ-DEMO-01'
```

Iniciar la API:

```bash
source .venv/bin/activate
source .mpaz_api_key
python3 api.py
```

En otra terminal, probar una tarjeta ficticia:

```bash
python3 simulador_totem.py
```

UID de prueba:

```text
B1C2D3E4
```

Para volver a la base real:

```bash
unset MPAZ_DB_PATH
unset CODIGO_TOTEM
```

## 10. Pruebas automáticas

Con la API de demostración activa, ejecutar:

```bash
python3 probar_api_automaticamente.py
```

El resultado esperado es:

```text
Pruebas ejecutadas: 6
Pruebas aprobadas: 6
Pruebas fallidas: 0
```

Las pruebas comprueban:

1. Estado público de la API.
2. Rechazo de una lectura sin clave.
3. Rechazo de un JSON vacío.
4. Rechazo de una lectura sin `evento_id`.
5. Rechazo de un UID con tipo incorrecto.
6. Rechazo controlado de un tótem no autorizado.
