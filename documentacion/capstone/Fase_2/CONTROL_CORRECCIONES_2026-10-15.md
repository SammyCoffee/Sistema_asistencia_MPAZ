# Control de correcciones y decisiones — Capstone MPAZ RFID

**Fecha de revisión:** 15-10-2026 · **Rama:** `capstone/organizacion-evidencias` · **Alcance:** documentación, no software.

> Este control registra situaciones reales del repositorio. Una corrección documental no equivale a evaluación aprobada ni sustituye la decisión personal de cada integrante.

| Observación | Estado actual | Acción o límite |
|---|---|---|
| Enlace roto del apoyo 1.1 | **Corregido en revisión anterior** | Los enlaces relativos al código y a la revisión de Fase 1 apuntan a sus destinos. |
| Guía 1.5 con secciones 6–8 supuestamente vacías | **Resuelto** | La versión Word actual incluye evidencias, plan y Gantt. Esa falta correspondía al original; confirmar fechas y responsables. |
| Texto antiguo sobre evidencias de 2.4 | **Corregido parcialmente en archivos actuales** | Se incorporaron anexos A1–A3 y B1–B3; se describen seis imágenes técnicas. Siguen pendientes otras pruebas, incluido el piloto. |
| Respuestas 2.2 con referencias anteriores a las imágenes | **Actualizadas** | Las hojas y notas de apoyo identifican seis imágenes disponibles; los formularios oficiales personales siguen pendientes. |
| Reparto de trabajo discrepante | **Documentado, aún por ratificar** | En la distribución descrita por Samantha: software/API/SQLite/panel/documentación principalmente Samantha; ESP32/PN532/montaje principalmente Lucas. Las fichas de avance 02 y 04 también atribuyen algunas tareas de software a Lucas. **No reescribir hechos históricos ni asignar autoría sin consulta a ambos**. |
| Formato e inglés | **Borrador bilingüe preparado; cumplimiento no confirmado** | Abstract español/inglés y borradores de conclusión/reflexión de Samantha disponibles [aquí](Evidencias_Grupales/Material_de_Apoyo/ANEXO_BILINGUE_MPAZ_RFID.md). Confirmar con docente si van dentro de 1.5/2.4 o en informe técnico complementario. Lucas redacta y valida sus textos. |
| 1.1 y 1.2 de Lucas | **Pendientes** | No hay formularios individuales localizados. No sustituirlos por los de Samantha. |
| Autoevaluación 1.3 | **Por confirmar** | Autoría individual y selección de niveles, especialmente el indicador de inglés. |
| Autoevaluación 2.2 | **Pendiente** | Hoja de apoyo y propuesta disponibles para Samantha; ella debe decidir su autoevaluación oficial y Lucas la suya. |
| Evaluaciones de docente 1.4 y 2.3, planillas | **Pendientes** | No atribuir calificaciones ni firmas del profesor. |
| Cierre 2.6 / presentación final | **Pendientes** | Entregables de cierre; confirmar calendario docente. |

## Evidencias técnicas: qué sí se tiene

- Dos PDF de arquitectura/casos de uso y siete vistas previas de diagramas.
- Capturas de tablas SQLite y consulta de un alumno **ficticio** con entrada y salida.
- Monitor serie ESP32 con lectura y respuesta HTTP 200: **comunicación, no inserción de nueva asistencia**.
- Prueba `evento_repetido`: siete registros antes y siete después, en **copia de pruebas**.
- Fotografías del ESP32, PN532 y tarjeta de prueba.

## Evidencias técnicas todavía no demostradas por estas imágenes

- Correlación de una **nueva asistencia** desde tarjeta → evento API → registro SQLite.
- Capturas del login y panel web con datos ficticios.
- Exportación y apertura de reporte.
- Piloto controlado y validación de extremo a extremo.
- Dominio, HTTPS y perfiles docentes, que figuran como objetivos posteriores.

## Para el profesor

1. ¿Exige portada, índice, abstract español/inglés y conclusiones/reflexión individuales en inglés **dentro** de las guías 1.5/2.4, o acepta un informe técnico separado?
2. ¿Para 2.1 se entrega una única reflexión grupal aunque el directorio esté en evidencias individuales?
3. ¿Qué cronograma y responsables oficiales deben quedar en 1.5 y 2.4?

Estas preguntas no deben resolverse inventando criterios académicos.
