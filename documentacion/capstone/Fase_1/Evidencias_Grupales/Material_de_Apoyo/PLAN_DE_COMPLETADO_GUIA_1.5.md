# Guía 1.5 — Propuesta de desarrollo de los apartados 6, 7 y 8

> **Documento auxiliar de trabajo.** Este archivo Markdown NO sustituye al DOCX `1.5_GuiaEstudiante_Fase 1_Definicion Proyecto APT.docx`, cuya versión revisada se debe verificar y subir por separado. Las evidencias y el calendario deben validarse con el docente. Se omiten RUT y datos personales privados por tratarse de un repositorio público.

**Proyecto:** Sistema MPAZ RFID — Plataforma Inteligente de Asistencia Escolar.

**Alcance revisado:** ESP32 + PN532 → API Flask (`POST /lectura`, `GET /estado`) → SQLite → panel web y exportación de registros. No presentar aplicación móvil nativa, RBAC, cifrado completo ni alertas automáticas como funciones implementadas sin pruebas.

## 6. Evidencias del Proyecto APT

| Tipo | Nombre | Descripción | Justificación |
|---|---|---|---|
| Avance | Requisitos y arquitectura | Flujos, reglas de negocio, actores y diagrama ESP32–API–BD–panel | Evidencia el análisis y las decisiones técnicas |
| Avance | Diseño de datos | Entidades alumnos, tarjetas, tótems y asistencias y sus restricciones | Demuestra modelado e integridad |
| Avance | API y pruebas funcionales | Resultados de `GET /estado`, `POST /lectura`, autorizaciones y `evento_id` | Demuestra el servicio y la prevención de duplicados |
| Final | Integración RFID | Prueba con ESP32/PN532, datos ficticios y respuestas del servidor | Verifica comunicación física y lógica |
| Final | Panel y reportes | Capturas de acceso, consulta y exportación con datos ficticios | Ilustra el beneficio para administración |
| Final | Pruebas y documentación | Casos de prueba, incidencias, manual técnico, informe y presentación | Da trazabilidad y reproducibilidad |

## 7. Plan de trabajo

| Competencia/área | Actividad | Recursos y tareas | Semanas propuestas | Responsable propuesto | Observaciones |
|---|---|---|---|---|---|
| Requisitos y gestión | Levantar alcance | Reuniones, actores, reglas y criterios de aceptación | 1–2 | Ambos | Validar necesidades del colegio |
| Arquitectura y datos | Diseñar modelo | Diagramas, API y esquema SQLite | 2–4 | Samantha; Lucas apoya IoT | Usar datos de prueba |
| Desarrollo de software | Programar API y BD | Python, Flask, SQLite, validaciones y eventos | 4–8 | Samantha | Probar rechazos y duplicados |
| Desarrollo de interfaz | Crear panel y reportes | HTML, CSS, JS, Flask; filtros y exportación | 6–10 | Samantha | No exponer datos reales |
| Integración IoT | Desarrollar tótem | ESP32, PN532, Wi-Fi, buzzer y lecturas | 6–11 | Lucas | Verificar conectividad y fuente |
| Integración de sistemas | Conectar componentes | Envío UID/evento_id y validación de respuestas | 10–13 | Ambos | Guardar pruebas reproducibles |
| Calidad y seguridad | Pruebas y ajustes | Casos positivos y negativos, autenticación, fallos | 12–16 | Ambos | No inventar métricas |
| Documentación | Informe y defensa | Manual técnico, evidencias y presentación | 16–18 | Ambos | Ajustar a la rúbrica |

**Validación pendiente:** comprobar la asignación real de responsabilidades, la duración y las evidencias aceptadas por el docente. Las semanas son un ejemplo de planificación, **no fechas efectivamente ejecutadas**.

## 8. Carta Gantt de 18 semanas

Leyenda: ■ actividad planificada. División ilustrativa: **Fase 1** semanas 1–6, **Fase 2** semanas 7–12, **Fase 3** semanas 13–18. El calendario oficial puede ser distinto.

| Actividad | Semanas previstas |
|---|---|
| Requisitos y definición | 1–2 |
| Arquitectura y datos | 2–4 |
| API y base de datos | 4–8 |
| Panel web y reportes | 6–10 |
| Tótem ESP32/PN532 | 6–11 |
| Integración completa | 10–13 |
| Pruebas y correcciones | 12–16 |
| Documentación y defensa | 16–18 |

### Control para la entrega

- [x] Propuesta escrita para completar los apartados 6–8.
- [x] Descripción acotada a la solución NFC/RFID documentada.
- [ ] Confirmación de responsabilidades y semanas con el equipo/docente.
- [x] Revisar los ocho apartados exigidos frente a la plantilla original (la versión de Word es reconstruida y no reproduce literalmente el diseño institucional).
- [ ] Revisar concordancia con la autoevaluación 1.3 (en especial indicadores 7, 8 y 12).
- [ ] Subir `1.5_GuiaEstudiante_Fase_1_Definicion_Proyecto_APT_PARA_REVISION.docx` a `Evidencias_Grupales/` (documento preparado sin RUT; pendiente de validación y subida).
