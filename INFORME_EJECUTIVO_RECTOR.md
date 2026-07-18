# Informe Ejecutivo  
# Sistema MPAZ RFID: Plataforma Inteligente de Asistencia Escolar

**Establecimiento:** Escuela Escritora Marcela Paz de San Bernardo  
**Proyecto impulsado por:** Equipo directivo y Centro de Innovación Escolar Marcela Paz  
**Estado:** Desarrollo funcional y etapa de integración con hardware

---

## 1. Presentación

El Sistema MPAZ RFID es una iniciativa de modernización tecnológica destinada a mejorar el registro de ingreso y asistencia de los estudiantes de la Escuela Escritora Marcela Paz.

El sistema utiliza tarjetas RFID personales, lectores instalados en tótems de acceso y una plataforma central que registra automáticamente la fecha y la hora de ingreso de cada estudiante.

Su implementación busca disminuir los registros manuales, mejorar la disponibilidad de la información y facilitar la generación de reportes para la gestión escolar.

## 2. Problema que busca resolver

El registro manual de asistencia puede requerir tiempo, generar errores de transcripción y dificultar la consulta rápida de información histórica.

El proyecto propone una solución que permita:

- Registrar el ingreso de estudiantes de manera rápida.
- Centralizar la información en una base de datos.
- Evitar registros duplicados.
- Identificar tarjetas bloqueadas o desconocidas.
- Generar reportes diarios, semanales, mensuales y anuales.
- Disponer de información organizada para la gestión interna.

## 3. Funcionamiento general

Cada estudiante contará con una tarjeta RFID vinculada a su registro institucional.

Al acercar la tarjeta al tótem:

1. El lector reconoce el identificador de la tarjeta.
2. El tótem envía la lectura al servidor.
3. El servidor valida al estudiante, la tarjeta y el dispositivo.
4. Se registra la fecha y hora del ingreso.
5. El tótem entrega una señal visual y sonora.

Las señales serán:

- Luz verde: asistencia registrada.
- Luz amarilla: asistencia ya registrada.
- Luz roja: tarjeta bloqueada, desconocida o dispositivo no autorizado.
- Buzzer: confirmación sonora según el resultado.

## 4. Arquitectura del sistema

```text
Tarjeta RFID del estudiante
            ↓
Lector PN532
            ↓
ESP32 DevKit V1
            ↓
Red WiFi institucional
            ↓
API segura en servidor Linux
            ↓
Base de datos de asistencia
            ↓
Consultas y reportes escolares
## 6. Beneficios esperados

La implementación del Sistema MPAZ RFID permitirá:

- Reducir el tiempo destinado al registro manual.
- Disminuir errores de digitación y duplicidad.
- Consultar rápidamente la asistencia por estudiante, curso o fecha.
- Facilitar la elaboración de reportes internos.
- Mejorar la trazabilidad de los ingresos.
- Apoyar la modernización tecnológica del establecimiento.
- Contar con una plataforma adaptable a futuras necesidades.

El sistema también permitirá que la escuela mantenga el control de sus propios datos y pueda realizar respaldos periódicos.

## 7. Seguridad y protección de la información

El sistema considera distintas medidas de seguridad:

- La API utiliza una clave privada para autorizar las comunicaciones.
- Solo los tótems registrados y activos pueden enviar lecturas.
- Las tarjetas bloqueadas no pueden registrar asistencia.
- La información real de los estudiantes no se almacena en GitHub.
- La base de datos y los respaldos se mantienen en medios privados.
- Las lecturas repetidas se identifican mediante un código único.
- Las pruebas técnicas utilizan estudiantes ficticios.
- Los respaldos permiten recuperar el sistema ante errores.

La información de estudiantes, tarjetas y asistencias deberá ser administrada únicamente por personal autorizado del establecimiento.

## 8. Riesgos y medidas de mitigación

### Pérdida de conexión a Internet o a la red local

**Riesgo:** el tótem podría no comunicarse temporalmente con el servidor.

**Mitigación:** las lecturas pueden almacenarse de manera local y reenviarse cuando se recupere la conexión.

### Pérdida o daño de una tarjeta

**Riesgo:** un estudiante podría quedar temporalmente sin poder registrar su ingreso.

**Mitigación:** la tarjeta puede bloquearse y posteriormente asignarse una nueva.

### Lecturas duplicadas

**Riesgo:** una tarjeta puede acercarse más de una vez durante el mismo ingreso.

**Mitigación:** el servidor permite solo una asistencia por estudiante durante el mismo día.

### Envío repetido de una lectura pendiente

**Riesgo:** un evento podría enviarse nuevamente después de una interrupción de red.

**Mitigación:** cada lectura posee un identificador único que evita registrar el mismo evento dos veces.

### Acceso no autorizado

**Riesgo:** un dispositivo externo podría intentar enviar información al servidor.

**Mitigación:** la API exige una clave privada y valida que el tótem esté registrado y activo.

### Pérdida o daño de la base de datos

**Riesgo:** una falla del equipo podría afectar la información almacenada.

**Mitigación:** el sistema dispone de procedimientos para crear respaldos periódicos y restaurar la base de datos.

### Corte de energía

**Riesgo:** el tótem o el servidor podrían apagarse inesperadamente.

**Mitigación:** se recomienda utilizar alimentación estable, protectores eléctricos y respaldos regulares.

## 9. Etapas pendientes

Para completar la implementación se deberán realizar las siguientes actividades:

1. Montar físicamente el ESP32, lector PN532, LEDs y buzzer.
2. Programar la comunicación del ESP32 con la API.
3. Conectar el tótem a la red institucional.
4. Registrar los tótems físicos en el servidor.
5. Adquirir y numerar las tarjetas RFID.
6. Asociar cada tarjeta con un estudiante.
7. Realizar pruebas controladas en el acceso de la escuela.
8. Capacitar al personal responsable.
9. Definir una política institucional de respaldos.
10. Iniciar una etapa piloto antes de la puesta en funcionamiento general.

## 10. Conclusión

El Sistema MPAZ RFID presenta una solución funcional y adaptable para modernizar el registro de asistencia de la Escuela Escritora Marcela Paz.

La plataforma de software ya permite validar dispositivos, administrar estudiantes y tarjetas, evitar duplicados, registrar asistencias y generar reportes.

La siguiente etapa corresponde a la integración con el hardware físico y a la realización de un piloto controlado dentro del establecimiento.

El proyecto busca apoyar la gestión escolar mediante una herramienta tecnológica propia, segura y desarrollada de acuerdo con las necesidades de la comunidad educativa.
