# Revisión académica y carga documental del 09 de noviembre de 2026

Proyecto Sistema MPAZ RFID: Plataforma Inteligente de Asistencia Escolar. Duoc UC Maipú, Ingeniería en Informática, Capstone APT122, sección 003D. Samantha Tapia: software y documentación; Lucas Baeza: hardware y firmware, según distribución informada por el equipo.

Los seis adjuntos se incorporan con los nombres solicitados, retirando únicamente los sufijos de descarga (1)/(2). Su contenido binario original se conserva. Los dos formularios son documentos distintos: Vista Lógica describe entidades y relaciones; Vista de Desarrollo describe módulos, dependencias e integración. Tres nuevas versiones corrigen referencias y terminología; ninguna sustituye ni elimina el original. Todos están disponibles para revisión académica; no se presume aprobación, firma ni evaluación docente.

## Archivos y versiones

| Documento | Original conservado | Versión corregida | Estado |
|---|---|---|---|
| Vista Lógica | [Abrir archivo](Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/MPAZ_RFID_Formulario_Vista_Logica_003D_PARA_REVISION.docx) | [Revisión 09-11-2026](Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/MPAZ_RFID_Formulario_Vista_Logica_003D_REVISION_2026-11-09.docx) | Para revisión académica |
| Vista de Desarrollo | [Abrir archivo](Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/MPAZ_RFID_Formulario_Vista_Desarrollo_003D_PARA_REVISION.docx) | [Revisión 09-11-2026](Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/MPAZ_RFID_Formulario_Vista_Desarrollo_003D_REVISION_2026-11-09.docx) | Para revisión académica |
| Informe Final 2.6 | [Abrir archivo](Fase_2/Evidencias_Grupales/2.6_Informe_Final_Fase2_MPAZ_RFID_003D_BORRADOR_PARA_REVISION.docx) | [Revisión 09-11-2026](Fase_2/Evidencias_Grupales/2.6_Informe_Final_Fase2_MPAZ_RFID_003D_BORRADOR_REVISION_2026-11-09.docx) | Para revisión académica |
| Presentación Fase 2 | [Abrir archivo](Fase_2/Evidencias_Proyecto/Presentacion_Proyecto/MPAZ_Fase2_Presentacion.pptx) | Original sin cambios | Para revisión académica |
| Diario 3.1 de Samantha | [Abrir archivo](Fase_3/Evidencias_Individuales/MPAZ_RFID_Diario_Reflexion_3_1_Samantha_Tapia_PARA_REVISION.docx) | Original sin cambios | Para revisión académica |
| Presentación Final Capstone | [Abrir archivo](Fase_3/Evidencias_Grupales/MPAZ_RFID_Presentacion_Final_Capstone_003D_PARA_REVISION.pptx) | Original sin cambios | Para revisión académica |

## Fuentes y método

- Rama documental inicial: `capstone/organizacion-evidencias@462e3533d07223a766a5c1a1c2322fc5c0525908`.
- Código consultado en modo de solo lectura: `main@2cbb1088236415bad627d676cc2ff766aa5ea7f3`. No se actualiza main ni se traslada código a la rama documental.
- Referencia histórica de los adjuntos: `909f2e9`. Se contrastaron `api.py`, `base_datos.py`, `registrar_asistencia.py`, `procesar_lectura_totem.py`, consultas, exportador CSV y dependencias. La referencia histórica no contiene las tablas y rutas docentes que sí están en la versión actual consultada; se corrige en las nuevas versiones.
- [Informe de conformidad del 04-11-2026](INFORME_CONFORMIDAD_DUOC_2026-11-04.md), conservado como registro histórico.
- [Fichas 02–06 y anexos existentes](Fase_2/Evidencias_Proyecto/Fichas_de_Iteracion/README.md): lectura de 04, 05 actualizada y 06, sin editar sus contenidos ni recalcular el avance histórico 87,5 %.
- [Resultados de simulación F05](Fase_2/Evidencias_Proyecto/Evidencias_Sistema_Aplicacion/F05_2026-10-25_PRUEBA_SIMULADA_API_SQLITE.md) y [transcripción original](Fase_2/Evidencias_Proyecto/Evidencias_Sistema_Aplicacion/F05_2026-10-25_PRUEBA_SIMULADA_TERMINAL_ORIGINAL.txt).

No se ejecutaron pruebas nuevas del sistema ni se abrieron bases escolares. La revisión de código es estática; las pruebas citadas son resultados históricos aportados por el equipo.

## Apertura e integridad visual

| Archivo | Comprobación | Resultado y límite |
|---|---|---|
| Vista Lógica | Paquete OOXML íntegro, XML y relaciones internas; apertura/renderizado | 3 páginas, 3 imágenes/diagramas, tablas y 7 apartados conservados |
| Vista de Desarrollo | Mismas comprobaciones | 4 páginas, 2 diagramas, tablas y 8 apartados conservados; tabla de módulos continúa en página 2 |
| Informe 2.6 | Mismas comprobaciones | 9 páginas, 4 imágenes, tablas, referencias y anexos conservados |
| Presentación Fase 2 | OOXML y renderizado completo | 15 diapositivas, fotografías/capturas y diagramas visibles |
| Diario 3.1 | OOXML y renderizado completo | 3 páginas, 8 apartados; redacción individual en primera persona intacta |
| Presentación Final | OOXML y renderizado completo | 14 diapositivas, capturas y diagramas visibles |

Se abrió cada archivo mediante LibreOffice en modo sin interfaz y se inspeccionaron las páginas/diapositivas renderizadas. No se afirma haber abierto los archivos en Microsoft Word o PowerPoint. Los diagramas docentes en formato panorámico y las capturas contienen texto pequeño: conviene ampliar al exponer o consultar el anexo fuente. No se observó pérdida de medios ni recorte que impida leer los contenidos principales. Los originales mantienen su diseño. Los PDF/PNG temporales de revisión no se cargan como anexos duplicados.

## Correcciones en nuevas versiones

| Documento | Cambio justificado | Conservación |
|---|---|---|
| Vista Lógica | Sustituye referencia `909f2e9` por `2cbb108`, versión que respalda tablas y rutas docentes; precisa que comparar entorno local/despliegue sigue pendiente | Solo cambia texto en `word/document.xml`; imágenes, estilos y demás partes intactos |
| Vista de Desarrollo | Misma corrección de versión; cambia «anticlonado lógico por evento» por «control de duplicados por evento» | La idempotencia no demuestra resistencia a clonación de tarjetas; no se declara esa propiedad |
| Informe 2.6 | Actualiza referencia de código y el pendiente «producción posterior» de las presentaciones a «archivos disponibles para revisión» | Conserva el estado de borrador, costos, pruebas, limitaciones y autoría |

La reflexión individual se conserva literalmente. Samantha debe validar las expresiones personales antes de presentarlas como declaración propia; no se añaden experiencias ni comentarios docentes.

## Contraste técnico y económico

| Tema | Evidencia disponible | Estado preciso |
|---|---|---|
| ESP32 + PN532, API Flask, SQLite | Código, fotos y diagramas | Arquitectura coherente; lectura física nueva correlacionada aún pendiente |
| Administración | Rutas de alumnos, tarjetas y tótems en `api.py`; interfaz HTML/JS | Implementación estática identificada; matriz funcional completa sin verificar |
| Docentes | Rutas `/profesor`, usuarios, asignaciones, sesiones y asistencias de clase; capturas DOCENTE_01–03 | Backend presente y estados visuales demostrados; login, recarga y permisos completos pendientes |
| Entrada y duplicado | F05: 0→1 y 1→1 con mismo evento_id | Verificado mediante simulación histórica, sin ESP32 conectado |
| Disponibilidad y autorización | F05: GET /estado 200, tótem inactivo 403, petición sin clave 401 | Casos simulados concretos; no certifican seguridad integral |
| Tarjeta bloqueada, alumno inactivo, antirrebote y cierre | Lógica en código; ventana de 30 segundos y cierre a las 17:00 | Implementados; falta matriz de resultados reproducibles para declararlos aprobados |
| Reportes | `exportar_asistencias_csv.py`, ruta con MIME `text/csv` | CSV en código; descarga/apertura sin evidencia final. PDF/XLSX no acreditados |
| PostgreSQL | Propuesta de evolución | Migración no acreditada |
| Implementación estimada | Ficha 06 | $930.000 CLP |
| Operación/desarrollo, 3 meses | Ficha 06 | $828.000 CLP, incluye $554.400 por 360 h globales |
| Total estimado | Suma de las dos categorías | $1.758.000 CLP; no equivale a desembolso real auditado |
| Beneficio de tiempo | Supuestos Ficha 06: 3–5 h actuales y 0,5–1 h proyectadas | 2–4,5 h/día potenciales; no medidas en piloto. 190 días/año es supuesto |
| VAN/TIR y remuneraciones | Ficha 06 distingue escenario económico y caja | No se afirman indicadores financieros concluyentes ni ahorro salarial directo |

Las siete comprobaciones F05 incluyen la creación de la base temporal y seis comprobaciones de API/persistencia. La diapositiva 8 de Fase 2 enumera las seis últimas; «7/7» se entiende únicamente con ese alcance, no como siete pruebas de hardware ni porcentaje de cobertura total.

## Estructura académica y formatos oficiales

Las tres fases conservan sus carpetas de evidencias individuales y grupales. Fase 2 mantiene además documentación, sistema/aplicación, base de datos, fichas y presentación del proyecto. `Vistas_4mas1` se incorpora dentro de documentación. Las fichas 02, 03, 04, ambas versiones 05, la 06 y sus anexos se conservan sin cambios. La Ficha 01 continúa sin localizar en el inventario de la rama documental.

La plantilla oficial 2.6, la pauta oficial 3.1 y el formato original de presentación final Duoc no se localizaron en las rutas inventariadas de esta rama ni entre los seis adjuntos; tampoco se encontró el formato final en el árbol documental de main. Por ello no se certifica correspondencia literal con preguntas, orden ni campos oficiales. La imagen institucional Duoc y los 14 slides no prueban cumplimiento de la pauta.

Orden observado de presentación final: portada; integrantes; descripción; objetivos; alcance/limitaciones; metodología; cronograma; arquitectura; modelo de datos; tecnologías; demostración; resultados; obstáculos/aprendizajes; preguntas. Cotejo con orden oficial: pendiente de disponer del original.

## Pendientes para cierre

- Obtener las plantillas oficiales 2.6 y 3.1 y el formato original de presentación final; adaptar y validar con docente. Los seis documentos siguen para revisión.
- Confirmar código de grupo, cronograma orientativo de 18 semanas y datos académicos exigidos.
- Validar personalmente el diario de Samantha; diario de Lucas pendiente.
- Resolver con el equipo las atribuciones históricas de software a Lucas en fichas 02/04, sin reescribir originales. La distribución informada para esta carga no resuelve retrospectivamente esa discrepancia.
- Localizar Ficha 01 y evidencias individuales faltantes de Lucas; autoevaluaciones y evaluaciones oficiales pendientes según controles históricos.
- Hacer prueba PN532→ESP32→API→nueva fila SQLite correlacionada; después piloto controlado.
- Completar login, persistencia tras recarga, permisos, CSV abierto, concurrencia, disponibilidad, TLS y respaldos en entorno autorizado con datos ficticios.
- Medir la línea base administrativa y el beneficio real; confirmar días lectivos, horas y costos efectivamente pagados antes de conclusiones financieras.
- Mejoras editoriales para futura versión de las presentaciones: en Fase 2/4 Python 3.12 corresponde a entorno informado, no a versión demostrada por lectura de código; en Fase 2/14 el diario ya está disponible pero falta validación. En Final/4 «registrar ... duplicados» debe explicarse como detectar/rechazar duplicados. No se interpreta como aprobación funcional ni se altera el original.

## Alcance de seguridad y conservación

Solo se incorporan documentos académicos y se actualizan índices/controles. No se añaden bases de datos, credenciales ni archivos de código. La revisión de textos y medios adjuntos no identificó datos escolares reales ni claves publicadas: las pantallas se presentan como DEMO. Los identificadores del evento F05 son ficticios. No se eliminan evidencias, no se renombran carpetas previas ni el repositorio, no se fusionan ramas ni se cierra el PR existente.

## Huellas de los originales incorporados

| Archivo recibido | SHA-256 de contenido conservado |
|---|---|
| `MPAZ_RFID_Formulario_Vista_Logica_003D_PARA_REVISION(1).docx` | `720d3b7552650a26059e6e12d9c6a894ec94eb03aac96979beafbf07783dc045` |
| `MPAZ_RFID_Formulario_Vista_Desarrollo_003D_PARA_REVISION(1).docx` | `183649ce71be199e3951a8a9eea5b12c8fe6f272bdce98b7e5b38e0f8d3a47f3` |
| `2.6_Informe_Final_Fase2_MPAZ_RFID_003D_BORRADOR_PARA_REVISION(2).docx` | `f7334a1375f7b357bc7b37f40c6edea446b68ea48ac6d1ac0e4fbe5e53b7adfe` |
| `MPAZ_Fase2_Presentacion(2).pptx` | `8eb07ef1eb243d4778e2829f2475c48e6666e38a3ff934957a16528d86d0256c` |
| `MPAZ_RFID_Diario_Reflexion_3_1_Samantha_Tapia_PARA_REVISION(1).docx` | `3e7a7d85dfe2bb0cfa3a2e2c2fc5a4d0ecf1249b7179bb1dd305a1ab1c1e504d` |
| `MPAZ_RFID_Presentacion_Final_Capstone_003D_PARA_REVISION(1).pptx` | `356b3ce26f99465c80f636ed3ec8cd98585e3ca71b2523a2e4dad754d125de76` |
