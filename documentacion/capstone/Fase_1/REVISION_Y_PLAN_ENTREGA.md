# Revisión de evidencias — Fase 1 (APT122)

> Documento interno de trabajo. No reemplaza los archivos oficiales DOCX/PPTX ni constituye una calificación docente.
> Revisión basada en la tabla de evidencias de Fase 1 y en el contenido disponible del proyecto MPAZ RFID.

## Control de archivos

| Evidencia | Estado al 12-10-2026 | Próxima acción |
|---|---|---|
| 1.1 Autoevaluación de competencias (individual) | No localizada en el repositorio ni en la búsqueda de archivos disponibles | Conseguir plantilla oficial, completar individualmente y subir DOCX con Apellido_Nombre |
| 1.2 Diario de reflexión (individual) | No localizado | Completar individualmente y subir DOCX con Apellido_Nombre |
| 1.3 Autoevaluación Fase 1 (individual) | Archivo existente en `Evidencias_Individuales/` | Revisar autoría, contenido y nombre final antes de entregar |
| Presentación idea de proyecto (grupal) | No localizada en el repositorio | Añadir PPTX/PDF de la presentación ya trabajada |
| 1.4 Formativa Fase 1 (grupal) | Archivo existente en `Evidencias_Grupales/` | Verificar comentarios y aprobación del docente; el archivo actual es una propuesta para revisión |
| 1.5 Guía Estudiante — Definición Proyecto APT (español) | Localizada entre los archivos de trabajo anteriores, pero **no incorporada al repositorio** | Completar y corregir el DOCX original, quitar identificadores sensibles y subir versión revisada |
| 1.5 Guía en inglés (grupal) | Optativa | Incorporar únicamente si se realizó |

## Revisión del contenido hallado en la guía 1.5

Las secciones 1–5 cuentan con redacción preliminar. Las secciones **6 (Evidencias)**, **7 (Plan de trabajo)** y **8 (Carta Gantt)** aparecen como plantillas sin las respuestas ni asignaciones completas, por lo que aún **no se debe marcar la guía 1.5 como terminada**.

Además, el texto describe aplicación **web y móvil**, registro manual por docente, alertas automáticas y controles RBAC/encriptación como si fuesen parte del alcance. Antes de entregar, ajustarlo al producto que se pueda demostrar: lectura NFC/RFID con **ESP32 + PN532**, transmisión al servidor, **API Flask**, **base de datos SQLite**, **panel web** y **exportación de asistencias**. La autenticación del panel y la llave de la API se pueden documentar con pruebas. No declarar como implementadas características futuras no verificadas.

La distribución de roles debe reflejar el trabajo realizado: **integrante de software** (API, BD, panel web, pruebas y documentación de integración) e **integrante de hardware/IoT** (ESP32, lector PN532, firmware y montaje). Verificar nombres y responsabilidades reales con ambos integrantes.

### Propuesta para completar el apartado 6 — Evidencias

**IMPORTANTE:** la tabla es una **propuesta** y debe ajustarse a las evidencias **acordadas con el docente**.

| Tipo | Evidencia | Descripción | Justificación |
|---|---|---|---|
| Avance | Documento de arquitectura y flujo NFC/RFID | Diagrama de componentes, comunicación tótem–API–BD–panel y reglas de asistencia | Comprueba diseño y trazabilidad técnica |
| Avance | Diseño de la base de datos | Modelo de alumnos, tarjetas, asistencias y tótems; relaciones y reglas de unicidad | Evidencia modelamiento e integridad de datos |
| Avance | Prototipo de API y pruebas | Capturas y resultados de `GET /estado`, `POST /lectura` y validación de eventos duplicados | Permite verificar el incremento funcional |
| Final | Integración ESP32/PN532 con API | Lectura de tarjeta de prueba, envío de `UID` y `evento_id`, respuesta del servidor | Demuestra la integración software–hardware |
| Final | Panel web y reportes | Capturas con datos ficticios de login, visualización y exportación de asistencias | Evidencia gestión y consulta de información |
| Final | Pruebas y documentación técnica | Casos de prueba, resultados reproducibles, manual e instructivo | Aporta verificabilidad y continuidad del proyecto |

### Propuesta para completar el apartado 7 — Plan de trabajo

Las duraciones siguientes son **estimaciones orientativas**, no fechas oficiales de la asignatura.

| Competencia aplicada | Tarea | Actividades y recursos | Duración propuesta | Responsable | Observación |
|---|---|---|---|---|---|
| Ingeniería de requisitos | Levantar necesidades y alcance | Reuniones, definición de actores, reglas y backlog; procesador de texto/GitHub | 2 semanas | Ambos | Validar alcance con establecimiento y docente |
| Diseño de soluciones | Arquitectura y modelo de datos | Flujo NFC, API, tablas, restricciones; diagramas/SQLite | 2 semanas | Software, con revisión de Hardware | Mantener datos de prueba anonimizados |
| Desarrollo y datos | Programar BD y API | Flask, endpoints, validaciones, idempotencia; Python, SQLite, pruebas HTTP | 3 semanas | Software | No divulgar llaves ni BD productiva |
| Desarrollo de interfaces | Implementar panel web y reportes | Login, listado y filtros, exportación; HTML/CSS/JS, Python | 3 semanas | Software | Validar con perfiles institucionales |
| Integración IoT | Montar y programar tótem | ESP32, PN532, Wi-Fi, buzzer, emisión de lecturas | 3 semanas | Hardware/IoT | Probar conectividad y alimentación |
| Pruebas e integración | Conectar tótem y backend | Validar UIDs, tarjetas activas, tótem autorizado, reintentos y duplicados | 2 semanas | Ambos | Guardar evidencia sin datos reales |
| Gestión y documentación | Preparar informe y defensa | Capturas, resultados, limitaciones, presentación | 3 semanas | Ambos | Revisar rúbrica antes de entregar |

### Propuesta para completar el apartado 8 — Carta Gantt

**Solo propuesta para las 18 semanas que aparecen en la plantilla:** confirmar con el docente la distribución real de las fases y adaptar a la ejecución concreta.

| Actividad | Semanas orientativas |
|---|---|
| Definición de problema, objetivos, competencias y alcance | 1–2 |
| Arquitectura, requerimientos y modelado inicial | 3–4 |
| Desarrollo de base de datos y API | 5–7 |
| Desarrollo de panel web y reportes | 7–10 |
| Desarrollo de tótem ESP32/PN532 | 8–11 |
| Integración y pruebas con datos de demostración | 11–14 |
| Mejoras, validación técnica y evidencias | 15–16 |
| Informe final y presentación | 17–18 |

## Confidencialidad antes de subir la guía 1.5

El archivo localizado contiene **datos de identificación personal de integrantes del equipo**. No debe publicarse en este repositorio abierto sin revisar y retirar, cuando corresponda, números de identificación y otros datos privados. Conservar una versión académica íntegra por el canal privado de entrega si el docente lo exige.

El repositorio ya contenía archivos `.db` históricos en `data/`; revisar si guardan registros de estudiantes. El `.gitignore` no elimina datos ya publicados ni del historial.

## Estado de esta revisión

- [x] Pautas y carpetas comparadas.
- [x] Guia 1.5 hallada entre archivos previos.
- [x] Partes incompletas y desajustes técnicos identificados.
- [ ] Crear/revisar los DOCX oficiales 1.1 y 1.2.
- [ ] Completar/corregir el DOCX original 1.5 (no basta este Markdown).
- [ ] Verificar y añadir la presentación.
- [ ] Incorporar entregas a GitHub sin datos sensibles.
- [ ] Validar aceptación con docente.
