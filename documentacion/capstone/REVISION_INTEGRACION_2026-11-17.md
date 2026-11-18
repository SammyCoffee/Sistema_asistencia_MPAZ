# Revisión final de integración documental 17-11-2026

Estado: preparado para un único commit documental, sujeto a autorización expresa. Sin commit, push ni git add. La condición de preparación documental no equivale a cierre académico ni aprobación docente.

## Alcance y seguridad

Repositorio académico: `SammyCoffee/Sistema_asistencia_MPAZ`. Rama activa `capstone/organizacion-evidencias`, HEAD `fc1aeea453927e26ff352d5db5437b11eab5f628`. La consulta remota de la revisión inicial coincidió con ese SHA; debe repetirse antes del commit/push autorizado. Sparse checkout `/documentacion/capstone/` sin cambios. El árbol inicial de la integración estaba limpio; las modificaciones actuales pertenecen a esta integración y su corrección. No se detectaron documentos históricos modificados.

Todos los cambios quedan dentro de `documentacion/capstone/`. No se modificaron código, firmware, dependencias, bases de datos, main ni la rama técnica. No se ejecutaron merge, rebase, reset, commit ni push. La corrección final utiliza solamente documentos y evidencias locales; los renders y scripts temporales no se incorporan a Git.

## Fuente y trazabilidad

ZIP original de Antigravity: `MPAZ_Capstone_Entrega_Consolidada_2026-11-17.zip`, 23 archivos. Inspección previa de rutas y CRC correcta, extracción inicial en carpeta temporal externa al repositorio. Las 22 huellas originales del manifiesto coincidían; se calculó además la del manifiesto. No hubo colisiones de rutas ni duplicados por SHA-256 contra los archivos académicos existentes. Las revisiones nuevas se distinguen de los originales históricos sin renombrarlos ni eliminarlos.

SHA-256 ZIP original: `e4346fd9bdb42a10f57f88da07fa52ca468234e7226b593ff0b86db0ca210e29`.

SHA-256 manifiesto original del ZIP: `fa1ac2d22fb8ab67707654ecb8a17a2587b07582c3863d02b6daf9fddad2cf1a`.

SHA-256 guía APT consultada: `cbd82122c564e6420af9a16d0f1308582d93be91cc5122789ed17d75712d4185`. Fuente: `Guia_Informe_APT_Completa.pdf` del material docente Sem15. No se inventó autor docente ni fecha de publicación de la guía.

El manifiesto ahora describe los bytes corregidos. [Índice SHA-256](SHA256_ENTREGA_2026-11-17.txt): cubre 34 archivos preparados o modificados, incluido el manifiesto, control, informe y README; se excluye únicamente el propio índice para evitar autorreferencia. Verificación desde esta carpeta: `sha256sum -c SHA256_ENTREGA_2026-11-17.txt`.

## Correcciones aplicadas

- Informe extenso: portada con título completo, Duoc UC Maipú, carrera, asignatura, sección, integrantes y fecha 2026. Docente por confirmar. Eliminados marcadores genéricos de plantilla y tabla de contenido desactualizada; veinte encabezados numerados conservados. Resumen de 154 palabras. Se añadieron alcance, limitaciones de la comparación comercial, justificación de capas, capturas existentes en 11 y 17, conclusión general, bibliografía y anexos relativos. No se añaden mediciones, horarios, sprints ni vivencias personales sin respaldo.
- Cinco Word 4+1: diagramas ampliados, páginas dedicadas, leyendas junto a imágenes. Desarrollo, Física y Procesos en A3 horizontal para diagramas; Escenarios y Lógica en página vertical. Tabla de Desarrollo conservada en una página. Los bytes de todos los medios incrustados se compararon con el ZIP original y coinciden; SVG y PNG externos intactos.
- Cronograma: áreas de impresión explícitas, orientación horizontal, salto entre tabla y Gantt y columna Actividad repetida; texto ajustado y filas más altas. Exporta tres páginas: dos A3 para cronograma y una A4 para Resumen, frente a siete iniciales. Todas las celdas y las tres fórmulas conservan exactamente su XML de contenido original; no se guardó una conversión Calc sobre el original.
- Informe 2.6, extenso, cinco vistas y bitácora: nota explícita de 61 métodos Python y tres scripts JS en entorno aislado; cinco caracterizaciones pendientes y ausencia de certificación de finalización funcional. Se mantienen los siete controles históricos de octubre como evidencia separada.
- Presentación: diapositiva 4 aclara rechazo de duplicados; diapositiva 12 identifica las cinco caracterizaciones abiertas y los pendientes. Se mantienen 14 diapositivas.
- Control, manifiesto, índices y README actualizados para describir la versión corregida.

## Cotejo de los veinte apartados con la guía

| Apartado | Evidencia o ajuste | Estado |
|---|---|---|
| 1 Resumen | Problema, solución, tecnologías, resultados y límites; 154 palabras | Revisado |
| 2 Introducción | Contexto, alcance y público objetivo | Revisado |
| 3 Problema | Afectados y consecuencias; estimación temporal identificada | Revisado |
| 4 Objetivos | Objetivo general y cinco específicos | Revisado |
| 5 Valor | Costos y tiempo proyectados, sin beneficio medido | Revisado |
| 6 Mercado y contexto | Alternativa manual y brecha; sin comparativa comercial inventada | Revisado con límite de evidencia |
| 7 Metodología | Incremental, fichas, gestión temporal, herramientas | Revisado; calendario oficial pendiente |
| 8 Stack | Hardware, backend, frontend y persistencia | Revisado |
| 9 Patrón | Separación en capas justificada; 4+1 identificado como modelo de vistas | Revisado |
| 10 Casos de uso | Lista de casos principales y acciones | Revisado |
| 11 Mockups | Captura funcional existente, distinguida de wireframe previo | Revisado; no se inventan mockups |
| 12 Evidencias | Ensayos históricos, auditoría aislada y referencias | Revisado |
| 13 Roles | Responsabilidades respaldadas; atribución histórica y horarios por ratificar | Revisado con pendientes |
| 14 Áreas | Marcador según Plan de Estudio oficial | Pendiente del equipo/docente |
| 15 Competencias | Marcador según Perfil de Egreso | Pendiente del equipo/docente |
| 16 Economía | Estimación Ficha 06; sin gasto o ahorro salarial certificado | Revisado |
| 17 Resultados | Escenarios ejercidos, límites y captura histórica | Revisado |
| 18 Conclusiones | Conclusión general y cumplimiento parcial; reflexión personal reservada | Pendiente de cada integrante |
| 19 Bibliografía | Referencias simples a guía y documentación existente | Revisado |
| 20 Anexos | Rutas relativas a archivos reales y enlace GitHub | Revisado |

## Revisión visual y estructural

Los ocho Word, el Excel y la presentación se abrieron y renderizaron con LibreOffice; páginas convertidas a PNG con Poppler. Se revisaron las páginas de los documentos afectados y en detalle los diagramas ampliados, el cronograma, portada y diapositivas 4/12. No se observaron recortes ni superposiciones en los elementos corregidos. Se conservan espacios propios de páginas dedicadas a figuras. Estas comprobaciones documentales no equivalen al QA manual de la aplicación.

Se utilizó LibreOffice y Poppler directamente: el helper render_docx.py no disponía de pdf2image en este entorno. La verificación se hizo sobre el render real, no solo sobre extracción de texto.

| Archivo | Páginas/diapositivas PDF |
|---|---|
| 2.6_Informe_Final_MPAZ_RFID_003D_OFICIAL_2026-11-17 | 4 |
| Bitacora_Semana_15_MPAZ_RFID_003D_2026-11-17 | 3 |
| MPAZ_RFID_Cronograma_18_Semanas | 3 |
| MPAZ_RFID_Informe_Extenso_20_Apartados_003D_2026-11-17 | 6 |
| MPAZ_RFID_Presentacion_Final_Capstone_003D_2026-11-17 | 14 |
| MPAZ_RFID_Vista_Desarrollo_003D_ACTUALIZADA_2026-11-17 | 2 |
| MPAZ_RFID_Vista_Escenarios_003D_2026-11-17 | 2 |
| MPAZ_RFID_Vista_Fisica_003D_2026-11-17 | 2 |
| MPAZ_RFID_Vista_Logica_003D_ACTUALIZADA_2026-11-17 | 2 |
| MPAZ_RFID_Vista_Procesos_003D_2026-11-17 | 2 |

Excel: resumen calculado al convertir a PDF, valores 10 actividades, 5 simuladas, 2 parciales/en curso y 18 semanas. Fórmulas COUNTA/COUNTIF conservadas; sin errores visibles. La impresión requiere respetar A3 para las dos páginas del cronograma, evitando reducirlas a A4 automáticamente.

Office: CRC y XML válidos; sin macros, objetos incrustados ni relaciones externas nuevas. Cinco SVG renderizados y seis PNG verificados en la revisión inicial, idénticos tras esta corrección. Rutas de anexos relativas verificadas en disco; el enlace técnico fija el commit de auditoría y no implica merge ni publicación del paquete corregido.

## Límites académicos y técnicos conservados

La evidencia 61+3 proviene de `audit/seguridad-continuidad-20261116`, commit `4268d50`; no se reejecutó la suite técnica en esta tarea. Cinco métodos caracterizan defectos o reglas institucionales abiertos. No se afirma que la rama esté fusionada en main, ni se declara aprobado el conjunto de funcionalidades.

Pendientes: prueba física correlacionada PN532→ESP32→API→SQLite, QA manual en navegador, carga operativa, migración 005 productiva, despliegue y piloto escolar. También competencias y áreas oficiales, grupo definitivo, autoría F02/F04, calendario/Ficha 01, reflexiones individuales, nombre docente, evidencias individuales de Lucas y pauta 3.1. Las capturas son demostraciones históricas, sin certificar impacto real.

## Inventario preparado y huellas originales de documentos corregidos

Los enlaces siguientes apuntan a los 23 archivos del paquete en sus destinos. La huella vigente está en el manifiesto y el índice SHA-256. Las huellas de origen permiten distinguir las correcciones del paquete recibido.

| Archivo | Relación con la versión anterior | SHA-256 original si fue corregido |
|---|---|---|
| [CONTROL_ENTREGA.md](CONTROL_ENTREGA.md) | CONTROL_ENTREGAS_FASE_2.md | `8185ea64f8779a73015928956f4d3d1410612013b07c2a99879aa6f5f84b6adb` |
| [Fase_2/Evidencias_Grupales/2.6_Informe_Final_MPAZ_RFID_003D_OFICIAL_2026-11-17.docx](Fase_2/Evidencias_Grupales/Historial_Borradores/2.6_Informe_Final_MPAZ_RFID_003D_OFICIAL_2026-11-17.docx) | 2.6_Informe_Final_Fase2_MPAZ_RFID_003D_BORRADOR_REVISION_2026-11-09.docx | `11d176a0df59687cbd09677ad685d2b59d5804c3358093b876135bf8661e62e0` |
| [Fase_2/Evidencias_Grupales/MPAZ_RFID_Informe_Extenso_20_Apartados_003D_2026-11-17.docx](Fase_2/Evidencias_Grupales/Material_de_Apoyo/MPAZ_RFID_Informe_Extenso_20_Apartados_003D_2026-11-17.docx) | Documento nuevo separado del 2.6 oficial | `eeb590137be586d10460d22913b63c33c599c48d651186be84ce4bee2d75bc9a` |
| [Fase_2/Evidencias_Proyecto/Cronograma/MPAZ_RFID_Cronograma_18_Semanas.xlsx](Fase_2/Evidencias_Proyecto/Cronograma/MPAZ_RFID_Cronograma_18_Semanas.xlsx) | Cronograma orientativo Slide 7 | `77264383aa86d36a90dbe792f22f363cd15b53a976d24886c84e994e07712aaa` |
| [Fase_2/Evidencias_Proyecto/Cronograma/cronograma_18_semanas_slide7.png](Fase_2/Evidencias_Proyecto/Cronograma/cronograma_18_semanas_slide7.png) | Slide 7 previa | Sin cambios respecto del ZIP |
| [Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/MPAZ_RFID_Vista_Desarrollo_003D_ACTUALIZADA_2026-11-17.docx](Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/MPAZ_RFID_Vista_Desarrollo_003D_ACTUALIZADA_2026-11-17.docx) | MPAZ_RFID_Formulario_Vista_Desarrollo_003D_REVISION_2026-11-09.docx | `590e839085442adaba30112a7eb3d6f50071c1329157886c429ae2e8e90011e1` |
| [Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/MPAZ_RFID_Vista_Escenarios_003D_2026-11-17.docx](Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/MPAZ_RFID_Vista_Escenarios_003D_2026-11-17.docx) | MPAZ_RFID_Diagramas_para_Profesor.pdf (pág. 1) | `aa9ae1ba5b24d3b99ecffc0a9272122dd7d171e020d9f88f171b840d015b55eb` |
| [Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/MPAZ_RFID_Vista_Fisica_003D_2026-11-17.docx](Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/MPAZ_RFID_Vista_Fisica_003D_2026-11-17.docx) | MPAZ_RFID_Diagramas_para_Profesor.pdf (pág. 3) | `573ad22513796467dfa573878957ce928188a806aa71651002b01a9d5cc31003` |
| [Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/MPAZ_RFID_Vista_Logica_003D_ACTUALIZADA_2026-11-17.docx](Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/MPAZ_RFID_Vista_Logica_003D_ACTUALIZADA_2026-11-17.docx) | MPAZ_RFID_Formulario_Vista_Logica_003D_REVISION_2026-11-09.docx | `2899378cc520f27bbc63f41d6627ee6f88eaba1b932f8bbaa62a23e6327d69ad` |
| [Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/MPAZ_RFID_Vista_Procesos_003D_2026-11-17.docx](Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/MPAZ_RFID_Vista_Procesos_003D_2026-11-17.docx) | MPAZ_RFID_Ficha05_Diagrama_Actividades_UML.* | `6fe4b398c53bf34fef835272947c7092eda8f1c81d900fc44da74824c3555037` |
| [Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/diagramas/vista_desarrollo_modulos.png](Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/diagramas/vista_desarrollo_modulos.png) | Diagramas previos 09-11-2026 | Sin cambios respecto del ZIP |
| [Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/diagramas/vista_desarrollo_modulos.svg](Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/diagramas/vista_desarrollo_modulos.svg) | Diagramas previos 09-11-2026 | Sin cambios respecto del ZIP |
| [Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/diagramas/vista_escenarios_casos_uso.png](Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/diagramas/vista_escenarios_casos_uso.png) | Diagramas previos 09-11-2026 | Sin cambios respecto del ZIP |
| [Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/diagramas/vista_escenarios_casos_uso.svg](Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/diagramas/vista_escenarios_casos_uso.svg) | Diagramas previos 09-11-2026 | Sin cambios respecto del ZIP |
| [Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/diagramas/vista_fisica_despliegue.png](Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/diagramas/vista_fisica_despliegue.png) | Diagramas previos 09-11-2026 | Sin cambios respecto del ZIP |
| [Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/diagramas/vista_fisica_despliegue.svg](Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/diagramas/vista_fisica_despliegue.svg) | Diagramas previos 09-11-2026 | Sin cambios respecto del ZIP |
| [Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/diagramas/vista_logica_entidades.png](Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/diagramas/vista_logica_entidades.png) | Diagramas previos 09-11-2026 | Sin cambios respecto del ZIP |
| [Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/diagramas/vista_logica_entidades.svg](Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/diagramas/vista_logica_entidades.svg) | Diagramas previos 09-11-2026 | Sin cambios respecto del ZIP |
| [Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/diagramas/vista_procesos_flujo.png](Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/diagramas/vista_procesos_flujo.png) | Diagramas previos 09-11-2026 | Sin cambios respecto del ZIP |
| [Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/diagramas/vista_procesos_flujo.svg](Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/diagramas/vista_procesos_flujo.svg) | Diagramas previos 09-11-2026 | Sin cambios respecto del ZIP |
| [Fase_2/Evidencias_Proyecto/Evidencias_Sistema_Aplicacion/Bitacora_Semana_15_MPAZ_RFID_003D_2026-11-17.docx](Fase_2/Evidencias_Proyecto/Evidencias_Sistema_Aplicacion/Bitacora_Semana_15_MPAZ_RFID_003D_2026-11-17.docx) | Plantilla Semana 15 del profesor | `0a22426e0644dcbc83738f87efd2748ef42e3199dfaefced7ca996ed2b5970b7` |
| [Fase_3/Evidencias_Grupales/MPAZ_RFID_Presentacion_Final_Capstone_003D_2026-11-17.pptx](Fase_3/Evidencias_Grupales/MPAZ_RFID_Presentacion_Final_Capstone_003D_2026-11-17.pptx) | MPAZ_RFID_Presentacion_Final_Capstone_003D_PARA_REVISION.pptx | `e4a5a361eaac5deaa4145e2c3dfd0992295bf1042d0ddabd895a090c9e85fec0` |
| [MANIFIESTO_ENTREGA.md](MANIFIESTO_ENTREGA.md) | Manifiesto de la entrega | `fa1ac2d22fb8ab67707654ecb8a17a2587b07582c3863d02b6daf9fddad2cf1a` |

## Verificación final previa a autorización

35 rutas preparadas respecto de HEAD: 26 nuevas y nueve README históricos actualizados. Ningún archivo eliminado; todos los documentos históricos binarios conservan sus huellas. Índice de Git vacío. Todos los cambios están bajo `documentacion/capstone/`.

`git diff --check`: correcto. Índice de SHA-256: 34/34 correcto. Tabla del manifiesto: 22/22 coincide; el manifiesto se verifica por el índice. No se incorporan claves, credenciales, bases escolares ni archivos de entorno. La detección estática inicial no encontró claves privadas, tokens GitHub/AWS, correos o RUT con puntos; la revisión actual no introduce datos personales reales nuevos.

Listo para autorizar un único commit documental. La autorización de commit y push sigue pendiente; detener trabajo después de las comprobaciones.
