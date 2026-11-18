# Evidencias de práctica profesional para revisión Capstone

Versión local candidata sobre `capstone/organizacion-evidencias`, base `48f4a4b3290bfb085e999908f6c4189eb7a97213`. No se crea commit ni se publica esta revisión.

Fuente privada: Informe final de Práctica Profesional de Samantha Tapia, Evaluación Sumativa 3. Actividades hasta el 30-10-2026, término del período 31-10-2026. El DOCX original y las figuras no seleccionadas permanecen fuera del repositorio; su integridad queda registrada en el manifiesto de práctica. El ZIP de origen tenía 33 archivos; su manifiesto verifica 32 y no se incluye a sí mismo.

## Cómo interpretar la evidencia

- **Física parcial:** E1 montaje; E2 lectura de prueba con HTTP 200 según fuente. No enlaza de forma transaccional un único evento hasta SQLite.
- **Aislada/simulada:** E3/E4/E8 y pruebas históricas F05; datos sintéticos y SQLite temporal. No se suman a las 61 pruebas de noviembre como si fueran nuevas ejecuciones.
- **Disponibilidad local:** E5; no equivale a HTTPS ni acceso externo o despliegue de la versión vigente.
- **Visual o documental:** E6/E7/E9–E18; las tablas de permisos se atribuyen a la fuente. Una pantalla no prueba persistencia o autorización por sí sola.
- **Pendiente:** correlación física integral, QA manual actual, despliegue escolar; calendario/seguimiento y edición posterior requieren pruebas en el código actual.

La fecha 15-11-2026 es un dato ficticio de simulación. Las cantidades de 8/9 alumnos, 4 tarjetas, 8 marcaciones o 105 tarjetas listadas pertenecen a momentos/conjuntos de prueba diferentes. Registrado significa estado asignado y no necesariamente presente. El contacto de seguimiento fue simulado.

La auditoría del 16-11-2026 es independiente: 61 métodos Python y tres scripts JS en entorno aislado, con cinco caracterizaciones de defectos/reglas aún abiertos. Esta integración documental no reejecuta la suite ni afirma merge en main.

## Matriz E1–E18

| Código | Figura(s) | Evidencia | Qué acredita | Límite | Uso recomendado |
|---|---|---|---|---|---|
| E1 | 1–2 | Fotografías de ESP32 y lector PN532 en mesa de trabajo | Montaje físico de banco de pruebas | No demuestra el flujo completo hasta SQLite | Fase 2 — Evidencias Sistema; vista física |
| E2 | 3 | Lectura de UID con respuesta HTTP 200 | Lectura física de prueba y respuesta del backend | No acredita por sí sola correlación con registro SQLite por evento_id | Informe 2.6; demostración RFID; vista de procesos |
| E3 | 4–5 | Consulta SQLite y evento repetido | Consulta de jornada y rechazo de duplicación en copia de prueba | No asociar automáticamente con la lectura física E2 | Informe 2.6; pruebas backend |
| E4 | 6–7 | Segunda lectura a 10 segundos y jornada completa | Reglas de antirrebote y salida simuladas | Datos ficticios y base temporal; no prueba física | Resultados y pruebas |
| E5 | 8 | Gunicorn y Nginx activos, /estado HTTP 200 local | Disponibilidad local del servicio web | No demuestra acceso externo, HTTPS ni operación productiva | Vista física; informe extenso |
| E6 | 9–11 | Panel administrativo, menú de reportes y archivo CSV | Interfaz de administración y evidencia visual de exportación CSV | Los contadores corresponden a datos de prueba; no equivale a XLSX/PDF | Resultados; presentación final |
| E7 | sin figura | Commit local 8b0dc28 en app.js y login.js | Trazabilidad histórica de corrección de interfaz | El documento indica que no se había verificado push a GitHub | Gestión del trabajo; anexos |
| E8 | tabla de la fuente | Tarjeta bloqueada, alumno inactivo, antirrebote y jornada | Resultados enumerados de software/SQLite temporal | Algunos casos no incluyen captura original de terminal | Pruebas backend; controles |
| E9 | 12–14 | Inicio docente, asignaciones 4.º B, sesiones y códigos HTTP | Portal docente y pruebas de permisos (401/200/403/400) | Capturas no equivalen a QA de la rama técnica del 16/11 | Semana 15; presentación; informe |
| E10 | 15–17 | Sesiones de 1.º A confirmadas y borradores parciales | Visualización de registros 5/5, 0/5, 2/5 | Registrado no equivale a presente; una captura estaba cargando | Flujos docentes; resultados |
| E11 | 18–19 | Búsqueda de alumno de prueba y formulario de edición | Consulta de ficha y carga de campos | No acredita guardado de cambios ni rechazo RFID desde tótem | Vista de escenarios; panel |
| E12 | 20–21 | Estados activo/inactivo y tarjeta bloqueada | Diferenciación de estado de estudiante y tarjeta en UI | No demuestra reactivación, desbloqueo ni lectura física | Modelo lógico; vistas de administración |
| E13 | 22–23 | Selección de portales y login docente rediseñado | Separación visual de accesos | Pruebas de autorización deben respaldarse por E9 u otras pruebas | Presentación final; interfaz |
| E14 | 24–25 | Dashboard administrativo y directorio de estudiantes | Navegación, indicadores y filtros | 9 alumnos, 4 tarjetas, 8 marcaciones son datos de una revisión, no matrícula escolar | Presentación; informe extenso |
| E15 | 26 | Inventario paginado con 105 tarjetas y filtros | Pantalla de inventario y acciones visibles | 105 listadas no significa 105 asignadas; revisar UIDs antes de publicar | Panel; gestión RFID |
| E16 | 27 | Calendario con excepción de horario ficticia | Prototipo visual de calendario | El guardado no estaba habilitado en el momento de la captura | Limitaciones; próximos pasos |
| E17 | 28 | Seguimiento escolar DEMO con observación e intervenciones | Vista demostrativa de historial | Contacto telefónico fue simulado; no se llamó al apoderado | Limitaciones; alcance |
| E18 | 29 | Sesión confirmada de 4.º B, modo solo lectura | Estado confirmado visible en interfaz | No acredita por sí sola rechazo en API de edición posterior | Semana 15; QA pendiente |

## Comparación de las 29 figuras y decisión

Cuatro duplicados binarios exactos (F01/F02/F04/F05) y uno con píxeles idénticos pero contenedor distinto (F29). F15/F16 son equivalentes visuales a recursos docentes existentes; F03 es un registro distinto del mismo tipo que API_01. Las similitudes visuales no se presentan como igualdad SHA-256.

| Figura | Relación | Referencia existente | Decisión |
|---|---|---|---|
| F01 | Duplicado SHA-256 | [HARDWARE_02_Tarjeta_Prueba_PN532.jpeg](../Evidencias_Sistema_Aplicacion/HARDWARE_02_Tarjeta_Prueba_PN532.jpeg) | Reutilizar la fotografía existente; no crear otra copia gráfica. [Recurso revisado](../Evidencias_Sistema_Aplicacion/HARDWARE_02_Tarjeta_Prueba_PN532.jpeg). |
| F02 | Duplicado SHA-256 | [HARDWARE_01_ESP32_PN532_Montaje.jpeg](../Evidencias_Sistema_Aplicacion/HARDWARE_01_ESP32_PN532_Montaje.jpeg) | Copia sanitizada creada y verificada solo en revisión privada. No incorporada por duplicación binaria con histórico. |
| F03 | Equivalente funcional, distinto evento | [API_01_ESP32_Envio_Lectura_HTTP200.png](../Evidencias_Sistema_Aplicacion/API_01_ESP32_Envio_Lectura_HTTP200.png) | Seleccionada sanitizada: lectura física parcial HTTP 200. No demuestra registro correlacionado en SQLite. [Copia protegida](../Evidencias_Sistema_Aplicacion/Practica_2026-11-17/PRACTICA_F03_SANITIZADA_2026-11-17.png). |
| F04 | Duplicado SHA-256 | [BD_02_Consulta_Asistencia_Demo_2026-10-13.png](../Base_de_Datos/BD_02_Consulta_Asistencia_Demo_2026-10-13.png) | Copia sanitizada creada y verificada solo en revisión privada. No incorporada por duplicación binaria con histórico. |
| F05 | Duplicado SHA-256 | [API_02_Evento_Repetido_Sin_Duplicados.png](../Evidencias_Sistema_Aplicacion/API_02_Evento_Repetido_Sin_Duplicados.png) | Copia sanitizada creada y verificada solo en revisión privada. No incorporada por duplicación binaria con histórico. |
| F06 | Complemento nuevo de simulación | [F05_2026-10-25_PRUEBA_SIMULADA_API_SQLITE.md](../Evidencias_Sistema_Aplicacion/F05_2026-10-25_PRUEBA_SIMULADA_API_SQLITE.md) | Seleccionada: doble lectura con SQLite temporal; no contar como otra ejecución actual. [Recurso revisado](../Evidencias_Sistema_Aplicacion/Practica_2026-11-17/PRACTICA_F06_REVISADA_2026-11-17.png). |
| F07 | Complemento nuevo de simulación | [F05_2026-10-25_PRUEBA_SIMULADA_API_SQLITE.md](../Evidencias_Sistema_Aplicacion/F05_2026-10-25_PRUEBA_SIMULADA_API_SQLITE.md) | Seleccionada: salida/jornada completa simuladas; fecha de ensayo ficticia. [Recurso revisado](../Evidencias_Sistema_Aplicacion/Practica_2026-11-17/PRACTICA_F07_REVISADA_2026-11-17.png). |
| F08 | Nuevo respaldo de disponibilidad local | Sin recurso idéntico confirmado | Seleccionada: servicio y HTTP 200 local, sin HTTPS/acceso externo certificado. [Recurso revisado](../Evidencias_Sistema_Aplicacion/Practica_2026-11-17/PRACTICA_F08_REVISADA_2026-11-17.png). |
| F09 | Nuevo estado visual del panel | Sin recurso idéntico confirmado | Seleccionada: contadores de prueba de esa revisión; no matrícula real. [Recurso revisado](../Evidencias_Sistema_Aplicacion/Practica_2026-11-17/PRACTICA_F09_REVISADA_2026-11-17.png). |
| F10 | Complemento visual redundante con E6 | Sin recurso idéntico confirmado | No seleccionada: botones de reporte no acreditan generación ni descarga. |
| F11 | Nuevo respaldo visual de CSV | Sin recurso idéntico confirmado | Seleccionada sanitizada: CSV histórico con fechas/horas/tipo de salida conservados. No certifica exportación actual ni XLSX/PDF. [Copia protegida](../Evidencias_Sistema_Aplicacion/Practica_2026-11-17/PRACTICA_F11_SANITIZADA_2026-11-17.png). |
| F12 | Interfaz de acceso, complementaria a Ficha 05 | Sin recurso idéntico confirmado | No seleccionada: login sin credenciales; redundante con accesos revisados. |
| F13 | Complemento visual de asignaciones docentes | Sin recurso idéntico confirmado | No seleccionada: cuenta de prueba y opciones visibles no certifican permisos por sí solas. |
| F14 | Nuevo encuadre de estados docentes | [DOCENTE_03_Sesion_Confirmada_4B_2026-10-21(1).png](../Evidencias_Sistema_Aplicacion/DOCENTE_03_Sesion_Confirmada_4B_2026-10-21(1).png) | Seleccionada: ya contiene anonimización de origen; añade contexto de confirmada y borrador, sin probar bloqueo API. [Recurso revisado](../Evidencias_Sistema_Aplicacion/Practica_2026-11-17/PRACTICA_F14_REVISADA_2026-11-17.png). |
| F15 | Equivalencia visual de sesión | [DOCENTE_01_Sesiones_Asistencia_1A_2026-10-22(1).png](../Evidencias_Sistema_Aplicacion/DOCENTE_01_Sesiones_Asistencia_1A_2026-10-22(1).png) | No crear otra copia: mismos estados 5/5, 0/5 y horarios; registros no significan todos presentes. |
| F16 | Equivalencia visual de borrador | [DOCENTE_02_Registro_Parcial_2_de_5_2026-10-22(1).png](../Evidencias_Sistema_Aplicacion/DOCENTE_02_Registro_Parcial_2_de_5_2026-10-22(1).png) | No crear otra copia: borrador 2/5 equivalente; se conservan antecedentes de demostración ya incluidos en APT. |
| F17 | Diseño aún cargando | Sin recurso idéntico confirmado | No seleccionada: no acredita carga completa ni sesión terminada de verificar. |
| F18 | Nueva ficha visual, información de E11 | Sin recurso idéntico confirmado | Copia sanitizada creada y verificada solo en revisión privada. No incorporada por redundancia con el par de estados F20/F21. |
| F19 | Formulario de edición ilustrativo | Sin recurso idéntico confirmado | No seleccionada: la carga del formulario no demuestra guardado. |
| F20 | Estado de tarjeta/estudiante en UI | Sin recurso idéntico confirmado | Seleccionada sanitizada: estudiante de prueba activo y tarjeta bloqueada; no prueba ejecución de acciones. [Copia protegida](../Evidencias_Sistema_Aplicacion/Practica_2026-11-17/PRACTICA_F20_SANITIZADA_2026-11-17.png). |
| F21 | Estado de tarjeta/estudiante en UI | Sin recurso idéntico confirmado | Seleccionada sanitizada: estudiante de prueba inactivo y tarjeta bloqueada; no prueba reactivación. [Copia protegida](../Evidencias_Sistema_Aplicacion/Practica_2026-11-17/PRACTICA_F21_SANITIZADA_2026-11-17.png). |
| F22 | Nuevo diseño de portales | Sin recurso idéntico confirmado | Seleccionada: separación visual de accesos, sin certificar autorización. [Recurso revisado](../Evidencias_Sistema_Aplicacion/Practica_2026-11-17/PRACTICA_F22_REVISADA_2026-11-17.png). |
| F23 | Nuevo diseño del login | Sin recurso idéntico confirmado | No seleccionada: sin credenciales, pero redundante para la selección de figuras. |
| F24 | Nuevo dashboard de revisión | Sin recurso idéntico confirmado | Seleccionada: 9 estudiantes, 4 tarjetas y 8 marcaciones son datos de prueba, no población escolar. [Recurso revisado](../Evidencias_Sistema_Aplicacion/Practica_2026-11-17/PRACTICA_F24_REVISADA_2026-11-17.png). |
| F25 | Directorio complementario a E14 | Sin recurso idéntico confirmado | No seleccionada: identidades ya ocultas y filtros visuales; no acredita operaciones. |
| F26 | Nuevo inventario ilustrativo | Sin recurso idéntico confirmado | Seleccionada: UID/nombres ya ocultos en la fuente; 105 listadas no equivale a asignadas. [Recurso revisado](../Evidencias_Sistema_Aplicacion/Practica_2026-11-17/PRACTICA_F26_REVISADA_2026-11-17.png). |
| F27 | Nuevo prototipo de calendario | Sin recurso idéntico confirmado | Seleccionada: horario ficticio y guardado no habilitado; no prueba persistencia. [Recurso revisado](../Evidencias_Sistema_Aplicacion/Practica_2026-11-17/PRACTICA_F27_REVISADA_2026-11-17.png). |
| F28 | Nueva demostración de seguimiento | Sin recurso idéntico confirmado | Seleccionada: sin teléfono real; contacto declarado simulado, no llamada a apoderado. [Recurso revisado](../Evidencias_Sistema_Aplicacion/Practica_2026-11-17/PRACTICA_F28_REVISADA_2026-11-17.png). |
| F29 | Duplicado de píxeles, PNG con distinto hash | [DOCENTE_03_Sesion_Confirmada_4B_2026-10-21(1).png](../Evidencias_Sistema_Aplicacion/DOCENTE_03_Sesion_Confirmada_4B_2026-10-21(1).png) | No crear otro recurso: píxeles idénticos al histórico; solo lectura visible no demuestra rechazo por API. |

## Versiones candidatas de los documentos

Las nueve versiones publicadas de referencia se conservan sin modificar. Se proponen las siguientes copias para revisión académica, sin promoverlas aún sobre las anteriores:

| Documento de referencia | Nueva versión candidata |
|---|---|
| [2.6_Informe_Final_MPAZ_RFID_003D_OFICIAL_2026-11-17.docx](../../Evidencias_Grupales/Historial_Borradores/2.6_Informe_Final_MPAZ_RFID_003D_OFICIAL_2026-11-17.docx) | [2.6_Informe_Final_MPAZ_RFID_003D_OFICIAL_PRACTICA_REVISION_2026-11-17.docx](../../Evidencias_Grupales/Historial_Borradores/2.6_Informe_Final_MPAZ_RFID_003D_OFICIAL_PRACTICA_REVISION_2026-11-17.docx) |
| [MPAZ_RFID_Informe_Extenso_20_Apartados_003D_2026-11-17.docx](../../Evidencias_Grupales/Material_de_Apoyo/MPAZ_RFID_Informe_Extenso_20_Apartados_003D_2026-11-17.docx) | [MPAZ_RFID_Informe_Extenso_20_Apartados_003D_PRACTICA_REVISION_2026-11-17.docx](../../Evidencias_Grupales/Material_de_Apoyo/MPAZ_RFID_Informe_Extenso_20_Apartados_003D_PRACTICA_REVISION_2026-11-17.docx) |
| [MPAZ_RFID_Vista_Desarrollo_003D_ACTUALIZADA_2026-11-17.docx](Vistas_4mas1/MPAZ_RFID_Vista_Desarrollo_003D_ACTUALIZADA_2026-11-17.docx) | [MPAZ_RFID_Vista_Desarrollo_003D_ACTUALIZADA_PRACTICA_REVISION_2026-11-17.docx](Vistas_4mas1/MPAZ_RFID_Vista_Desarrollo_003D_ACTUALIZADA_PRACTICA_REVISION_2026-11-17.docx) |
| [MPAZ_RFID_Vista_Escenarios_003D_2026-11-17.docx](Vistas_4mas1/MPAZ_RFID_Vista_Escenarios_003D_2026-11-17.docx) | [MPAZ_RFID_Vista_Escenarios_003D_PRACTICA_REVISION_2026-11-17.docx](Vistas_4mas1/MPAZ_RFID_Vista_Escenarios_003D_PRACTICA_REVISION_2026-11-17.docx) |
| [MPAZ_RFID_Vista_Fisica_003D_2026-11-17.docx](Vistas_4mas1/MPAZ_RFID_Vista_Fisica_003D_2026-11-17.docx) | [MPAZ_RFID_Vista_Fisica_003D_PRACTICA_REVISION_2026-11-17.docx](Vistas_4mas1/MPAZ_RFID_Vista_Fisica_003D_PRACTICA_REVISION_2026-11-17.docx) |
| [MPAZ_RFID_Vista_Logica_003D_ACTUALIZADA_2026-11-17.docx](Vistas_4mas1/MPAZ_RFID_Vista_Logica_003D_ACTUALIZADA_2026-11-17.docx) | [MPAZ_RFID_Vista_Logica_003D_ACTUALIZADA_PRACTICA_REVISION_2026-11-17.docx](Vistas_4mas1/MPAZ_RFID_Vista_Logica_003D_ACTUALIZADA_PRACTICA_REVISION_2026-11-17.docx) |
| [MPAZ_RFID_Vista_Procesos_003D_2026-11-17.docx](Vistas_4mas1/MPAZ_RFID_Vista_Procesos_003D_2026-11-17.docx) | [MPAZ_RFID_Vista_Procesos_003D_PRACTICA_REVISION_2026-11-17.docx](Vistas_4mas1/MPAZ_RFID_Vista_Procesos_003D_PRACTICA_REVISION_2026-11-17.docx) |
| [Bitacora_Semana_15_MPAZ_RFID_003D_2026-11-17.docx](../Evidencias_Sistema_Aplicacion/Bitacora_Semana_15_MPAZ_RFID_003D_2026-11-17.docx) | [Bitacora_Semana_15_MPAZ_RFID_003D_PRACTICA_REVISION_2026-11-17.docx](../Evidencias_Sistema_Aplicacion/Bitacora_Semana_15_MPAZ_RFID_003D_PRACTICA_REVISION_2026-11-17.docx) |
| [MPAZ_RFID_Presentacion_Final_Capstone_003D_2026-11-17.pptx](../../../Fase_3/Evidencias_Grupales/MPAZ_RFID_Presentacion_Final_Capstone_003D_2026-11-17.pptx) | [MPAZ_RFID_Presentacion_Final_Capstone_003D_PRACTICA_REVISION_2026-11-17.pptx](../../../Fase_3/Evidencias_Grupales/MPAZ_RFID_Presentacion_Final_Capstone_003D_PRACTICA_REVISION_2026-11-17.pptx) |

## Privacidad y pendientes

Se conservan diez imágenes revisadas previamente y se añaden cuatro sanitizadas (F03/F11/F20/F21); F01 se reutiliza sin duplicar el archivo. Se generaron ocho copias sanitizadas con Pillow autorizado: F02/F04/F05/F18 quedan solo en revisión privada por duplicación/redundancia. Los originales no sanitizados permanecen fuera de esta preparación. Máscaras negras opacas, PNG sin metadatos; igualdad exacta de todos los píxeles fuera de las máscaras verificada.

La reflexión de práctica es de Samantha: puede servir de antecedente sujeto a su validación y adaptación; no completa la reflexión de Lucas ni ratifica las competencias oficiales. Las discrepancias históricas de autoría F02/F04 continúan pendientes.

[Control de privacidad](CONTROL_PRIVACIDAD_PRACTICA_2026-11-17.md) · [Informe de revisión](../../../REVISION_EVIDENCIAS_PRACTICA_2026-11-17.md) · [Huellas de la revisión](../../../SHA256_PRACTICA_2026-11-17.txt).

[Registro de las ocho sanitizaciones](../../../REGISTRO_SANITIZACION_PRACTICA_2026-11-17.json) · [Recomendación específica para históricos](../../../RECOMENDACION_HISTORICOS_PRIVACIDAD_2026-11-17.md).
