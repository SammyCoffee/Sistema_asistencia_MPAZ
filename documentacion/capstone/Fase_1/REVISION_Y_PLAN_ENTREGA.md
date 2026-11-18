# Revisión de evidencias — Fase 1 (APT122)

> Documento interno de trabajo. No reemplaza los archivos oficiales DOCX/PPTX ni constituye una calificación docente.
> Revisión basada en la tabla de evidencias de Fase 1 y en el contenido disponible del proyecto MPAZ RFID.

## Control de archivos

| Evidencia | Estado al 12-10-2026 | Próxima acción |
|---|---|---|
| 1.1 Autoevaluación de competencias (individual) | **Samantha Tapia:** DOCX subido; **Lucas Baeza:** no localizado | Revisar por docente el de Samantha y añadir el de Lucas cuando esté completo |
| 1.2 Diario de reflexión (individual) | **Samantha Tapia:** DOCX subido; **Lucas Baeza:** no localizado | Revisar por docente el de Samantha y añadir el de Lucas cuando esté completo |
| 1.3 Autoevaluación Fase 1 (individual) | Archivo existente y revisión documental realizada | Confirmar autoría, justificar niveles y relacionar con la guía 1.5 antes de guardar una versión individual definitiva |
| Presentación idea de proyecto (grupal) | **PPTX de revisión subido y verificado** en `Evidencias_Grupales/Presentacion_Idea_Proyecto/` | Validar los roles, cronograma y coherencia con la guía 1.5 antes de dar por definitiva la presentación |
| 1.4 Formativa Fase 1 (grupal) | **Solo borrador de apoyo localizado; no se identificó una heteroevaluación validada del docente en el repositorio** | Conservar el borrador diferenciado y adjuntar versión evaluada únicamente si la entrega el docente |
| 1.5 Guía Estudiante — Definición Proyecto APT (español) | **Word de cuatro páginas recibido y reubicado en Evidencias_Grupales** | Confirmar roles, validar calendario y contenido con el equipo/docente; el archivo sigue siendo una versión para revisión |
| 1.5 Guía en inglés (grupal) | Optativa | Incorporar únicamente si se realizó |

## Revisión del contenido hallado en la guía 1.5

**Situación de versiones:** el DOCX original previamente disponible presentaba las secciones 6 (Evidencias), 7 (Plan de trabajo) y 8 (Carta Gantt) vacías. **La nueva versión reconstruida para revisión ya completa las ocho secciones**, con seis evidencias previstas, ocho actividades en el plan y una Carta Gantt de 18 semanas. Esto **no equivale a aprobación docente ni a evidencia técnica ejecutada**.

La versión original describía aplicación móvil, alertas y controles futuros. La versión actual 1.5 ya limita el alcance a lo demostrable y excluye móvil nativo y alertas automáticas como funciones demostradas. Mantener coherencia con: lectura NFC/RFID con **ESP32 + PN532**, transmisión al servidor, **API Flask**, **base de datos SQLite**, **panel web** y **exportación de asistencias**. La autenticación del panel y la llave de la API se pueden documentar con pruebas. No declarar como implementadas características futuras no verificadas.

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

El original revisado contenía datos de identificación. La guía 1.5 actual reserva los RUT para la entrega privada; mantener ese criterio en futuras versiones públicas. Conservar una versión académica íntegra por el canal privado de entrega si el docente lo exige.

El repositorio ya contenía archivos `.db` históricos en `data/`; revisar si guardan registros de estudiantes. El `.gitignore` no elimina datos ya publicados ni del historial.

## Estado de esta revisión

- [x] Pautas y carpetas comparadas.
- [x] Guia 1.5 hallada entre archivos previos.
- [x] Partes incompletas y desajustes técnicos identificados.
- [x] Incorporar el DOCX oficial individual de Samantha Tapia para 1.1.
- [ ] Incorporar el DOCX oficial individual de Lucas Baeza para 1.1.
- [x] Incorporar el DOCX individual del diario de Samantha Tapia para 1.2.
- [ ] Incorporar el DOCX individual del diario de Lucas Baeza para 1.2.
- [x] Preparar un DOCX reconstruido de la guía 1.5 con las ocho secciones, revisado visualmente.
- [x] Subir y ubicar el DOCX 1.5 en `Evidencias_Grupales/`.
- [ ] Validar la asignación real de roles y semanas con el equipo/docente.
- [x] Incorporar la presentación grupal revisada al repositorio.
- [ ] Validar entre integrantes las responsabilidades y el cronograma de la presentación.
- [ ] Incorporar las entregas restantes a GitHub sin datos sensibles.
- [ ] Validar aceptación con docente.

## Revisión específica de evidencia 1.3 — Autoevaluación Fase 1

**Documento revisado:** `Evidencias_Individuales/1.3_APT122_AutoevaluacionFase1_MPAZ_RFID_Completada.docx`. Esta es una **revisión documental**, no una evaluación ni aprobación docente.

### Aspectos presentes
- Conserva la estructura de la pauta institucional y desarrolla una tabla de indicadores de calidad correspondientes a pruebas, gestión, bases de datos y desarrollo e integración de software.
- Aparecen seleccionados los indicadores 1 al 11 en «Completamente Logrado» y el indicador 12 de comunicación escrita en inglés en «Logrado», con nota explícita de verificación posterior.
- Añade un fundamento técnico sobre API Flask, base de datos SQLite, tótems, lectura de tarjetas, restricciones de duplicidad y panel web.
- El indicador de implantación de software 4.3 se identifica **en desarrollo**, lo que evita presentarlo como implementado por completo.

### Correcciones o verificaciones antes de la entrega
1. **Autoría individual:** el documento no identifica claramente a la estudiante dentro de los apartados revisados. Confirmar autor/a y agregar identificación compatible con el formulario; solo entonces renombrar con `Apellido_Nombre_1.3_APT122_AutoevaluacionFase1.docx`.
2. **Indicadores 7 y 8:** están marcados como «Completamente Logrado» respecto del plan de trabajo y las evidencias. La guía 1.5 actual ya completa las secciones 6 (evidencias), 7 (plan) y 8 (Gantt). La observación de apartados vacíos corresponde a la versión original y está resuelta; resta confirmar coherencia, responsables y calendario antes de ratificar la valoración personal.
3. **Indicador 12:** aparece como «Logrado» (60 %) con instrucción «verificar versión final en inglés». Confirmar si el informe de definición realmente contiene abstract en ambos idiomas, conclusiones individuales en inglés y reflexión en inglés, tal como prescribe la pauta; si no, ajustar autoevaluación y trabajo base.
4. **Indicadores 9 a 11:** antes de asignar puntaje máximo, comprobar las normas de citas, el formato disciplinario y que los indicadores de calidad estén respaldados documentalmente. No basta con que la rúbrica diga «seleccionado».
5. **Fundamentación final:** es útil, pero funciona como síntesis de la implementación y **no reemplaza** el informe o guía de definición del proyecto.
6. **Redacción temporal:** revisar la frase «la implantación física completa ... continúa como incremento posterior» para que describa el estado real a la fecha de entrega; no afirmar funcionalidades no probadas.

**Estado provisional:** presente y cumplimentada, pero **pendiente de validar coherencia y autoría antes de considerarla lista**. No modificar la autoevaluación del estudiante sin que la persona confirme su propio juicio.

## Revisión específica de evidencia 1.4 — Formativa Fase 1

**Archivos contrastados:** `1.4_APT122_FormativaFase1.docx` (pauta oficial sin selecciones) y `Evidencias_Grupales/1.4_APT122_FormativaFase1_MPAZ_RFID_Preparada.docx` (borrador existente en GitHub). El documento de GitHub lleva una advertencia explícita: «BORRADOR DE APOYO PARA REVISIÓN DOCENTE — Las selecciones propuestas no reemplazan la heteroevaluación del/la docente».

### Qué dice la pauta oficial

- **Agente evaluativo: heteroevaluación.** La pauta declara que **el/la docente** debe aplicarla en la semana 2 y revisar la primera parte de la Definición del Proyecto APT.
- Contempla **cinco indicadores**, con ponderaciones 12 %, 15 %, 10 %, 13 % y 50 %.
- Su resultado orienta una **recomendación del docente** entre: cumple las condiciones, cumple algunas y requiere modificaciones, o no cumple.
- Es una evaluación **formativa, de ponderación 0 %**, según la propia pauta, pero no por ello podemos sustituir su valoración oficial.
- Solicita formato técnico con portada, índice, abstract español/inglés, desarrollo, conclusiones individuales en inglés y reflexión en inglés, según el texto de instrucciones de la pauta.

### Resultado de la revisión del archivo del repositorio

- Está presente un **borrador de ocho páginas**; la plantilla de referencia sin completar tiene siete.
- El borrador marca propuestas en nivel más alto para varios indicadores y sugiere la opción «cumple las condiciones»; **esto no constituye una decisión tomada por el docente**.
- Los indicadores de calidad 1.1–4.2 se presentan como «evidencia disponible», mientras 4.3 se señala en desarrollo; debe verificarse su respaldo en el material de la entrega.
- Incluye un anexo técnico útil del proyecto, pero es **material de apoyo**, no una rúbrica recibida tras la corrección del docente.

### Acciones de organización

- [x] Conservar el archivo original del borrador en el repositorio sin alterar sus selecciones.
- [x] Identificarlo en el índice como **borrador**, no como heteroevaluación oficial terminada.
- [ ] Incorporar la pauta evaluada por el docente, si existe o cuando la entregue, sin modificar sus valoraciones.
- [ ] Comprobar concordancia entre los cinco indicadores y la primera parte del informe/guía 1.5.
- [ ] No considerar cerrada la evaluación 1.4 hasta contar con una versión válida.

**Conclusión:** la Fase 2 ya contiene evidencias técnicas parciales; la evidencia 1.4 permanece **pendiente de validación docente**.

## Pendientes de cierre documental

- 1.1 y 1.2 de Lucas: no disponibles en esta rama.
- 1.3: confirmar autoría individual y niveles; el nivel de inglés no se ratifica sin los apartados correspondientes.
- 1.4: incorporar evaluación del docente cuando esté disponible.
- 1.5 y presentación: confirmar responsables y calendario; las secciones 6–8 de la guía ya están completas.
- Formato e inglés: la pauta pide abstract español/inglés, conclusiones individuales y reflexión en inglés. No se localizaron esos apartados en la guía 1.5 actual. Confirmar con el docente si van en un informe complementario. La traducción íntegra optativa no elimina esos requisitos por sí sola.
