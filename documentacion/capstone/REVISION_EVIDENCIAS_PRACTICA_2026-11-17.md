# Protección e integración de evidencias de práctica 17-11-2026

## Resultado preparado

Ocho imágenes sanitizadas con Pillow, sin edición generativa. Se seleccionan F03/F11/F20/F21 para aportar lectura física parcial, CSV histórico y estados diferenciados de estudiante/tarjeta. F02/F04/F05/F18 se conservaron sanitizadas solo en la revisión privada por duplicación/redundancia. Los ocho originales no sanitizados y el informe de práctica permanecen fuera de esta carga.

Se mantienen las diez imágenes ya revisadas y la fotografía F01 reutilizada. La carpeta preparada contiene catorce imágenes nuevas; su inserción en distintos documentos no cuenta como nuevas pruebas independientes. Se conservan las 18 evidencias y 29 figuras en la matriz de trazabilidad.

Todos los 122 archivos que existían en el commit base permanecen byte por byte iguales. Solo se agregan versiones candidatas y controles nuevos bajo documentacion/capstone/. No se alteran los nueve documentos consolidados anteriores ni sus índices/hashes. El XLSX y los diagramas originales permanecen intactos.

## Seguridad y fuente

Rama capstone/organizacion-evidencias; HEAD 48f4a4b3290bfb085e999908f6c4189eb7a97213. El remoto coincidía antes de la integración. Sparse checkout académico sin cambios. Sin staging, commit, push, merge o rebase. No se modificaron main, rama técnica, código, firmware ni bases; no hubo acceso al servidor escolar. La consulta técnica fue solo de texto y estado Git; no se leyeron bases para deducir el estado actual de tarjetas.

ZIP original: 33 archivos inspeccionados sin traversal/enlaces simbólicos y con CRC correcto. Manifiesto de origen: 32 huellas verificadas, más la huella del propio JSON en el manifiesto local. Los originales se preservan externamente y no se copian a documentos, notas o medios Office nuevos.

## Trazabilidad y diferencia de pruebas

- E1/E2: montaje y lectura física parcial ESP32/PN532 con HTTP 200. La respuesta no demuestra por sí sola una fila SQLite correlacionada por evento_id.
- E3/E4/E8: simulaciones con SQLite temporal y datos sintéticos. La fecha 15-11-2026 es ficticia.
- E5: disponibilidad local histórica por Gunicorn/Nginx; no HTTPS ni despliegue actual certificado.
- E6/E9/E10/E18: CSV y capturas históricas del panel/portal docente. Registrado no significa necesariamente presente. Las tablas de permisos se atribuyen a la fuente; UI de solo lectura no prueba rechazo posterior por API.
- E16/E17: calendario cuyo guardado no estaba habilitado y seguimiento DEMO con contacto simulado. No se llamó a un apoderado.
- Integración física completa, QA manual actual y despliegue escolar pendientes. Las cantidades visibles son conjuntos de prueba de distintos momentos, no matrícula institucional.
- Auditoría del 16-11 independiente de la práctica finalizada en octubre: 61 métodos Python y tres scripts JS en entorno aislado; cinco caracterizaciones de defectos/reglas abiertos. No se reejecuta la suite ni se afirma fusión en main.

Los ocho Word incluyen una nota común que distingue todos estos niveles. La presentación los distribuye entre alcance, tecnologías, demostración y resultados, manteniendo catorce láminas. Las reflexiones y competencias pendientes siguen identificadas; el antecedente de Samantha no completa la reflexión de Lucas ni ratifica el perfil oficial.

## Archivos documentales candidatos

| Archivo nuevo para revisión | Páginas/diapositivas PDF |
|---|---|
| [2.6_Informe_Final_MPAZ_RFID_003D_OFICIAL_PRACTICA_REVISION_2026-11-17.docx](Fase_2/Evidencias_Grupales/Historial_Borradores/2.6_Informe_Final_MPAZ_RFID_003D_OFICIAL_PRACTICA_REVISION_2026-11-17.docx) | 9 |
| [MPAZ_RFID_Informe_Extenso_20_Apartados_003D_PRACTICA_REVISION_2026-11-17.docx](Fase_2/Evidencias_Grupales/Material_de_Apoyo/MPAZ_RFID_Informe_Extenso_20_Apartados_003D_PRACTICA_REVISION_2026-11-17.docx) | 14 |
| [MPAZ_RFID_Vista_Desarrollo_003D_ACTUALIZADA_PRACTICA_REVISION_2026-11-17.docx](Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/MPAZ_RFID_Vista_Desarrollo_003D_ACTUALIZADA_PRACTICA_REVISION_2026-11-17.docx) | 3 |
| [MPAZ_RFID_Vista_Escenarios_003D_PRACTICA_REVISION_2026-11-17.docx](Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/MPAZ_RFID_Vista_Escenarios_003D_PRACTICA_REVISION_2026-11-17.docx) | 3 |
| [MPAZ_RFID_Vista_Fisica_003D_PRACTICA_REVISION_2026-11-17.docx](Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/MPAZ_RFID_Vista_Fisica_003D_PRACTICA_REVISION_2026-11-17.docx) | 5 |
| [MPAZ_RFID_Vista_Logica_003D_ACTUALIZADA_PRACTICA_REVISION_2026-11-17.docx](Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/MPAZ_RFID_Vista_Logica_003D_ACTUALIZADA_PRACTICA_REVISION_2026-11-17.docx) | 4 |
| [MPAZ_RFID_Vista_Procesos_003D_PRACTICA_REVISION_2026-11-17.docx](Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/MPAZ_RFID_Vista_Procesos_003D_PRACTICA_REVISION_2026-11-17.docx) | 4 |
| [Bitacora_Semana_15_MPAZ_RFID_003D_PRACTICA_REVISION_2026-11-17.docx](Fase_2/Evidencias_Proyecto/Evidencias_Sistema_Aplicacion/Bitacora_Semana_15_MPAZ_RFID_003D_PRACTICA_REVISION_2026-11-17.docx) | 4 |
| [MPAZ_RFID_Presentacion_Final_Capstone_003D_PRACTICA_REVISION_2026-11-17.pptx](Fase_3/Evidencias_Grupales/MPAZ_RFID_Presentacion_Final_Capstone_003D_PRACTICA_REVISION_2026-11-17.pptx) | 14 |

El Informe 2.6 y el extenso APT incorporan F03/F11 protegidas. Física incorpora F03; Lógica incorpora el par F20/F21; Procesos, Escenarios, Desarrollo y Bitácora actualizan sus referencias y límites. La presentación sustituye las imágenes centrales de la demostración por F03/F11 sanitizadas. Los diagramas 4+1 se conservan con sus bytes, dimensiones y páginas dedicadas; las capturas ilustran la evidencia sin redefinir la arquitectura.

## Ocultación y selección

Las máscaras son rectángulos negros opacos, guardados en PNG aplanado sin metadatos. La comparación exacta verifica cero cambios fuera de las zonas registradas. Se conservan HTTP 200, conteos, consulta/resultados SQL, fechas, horas, tipo de salida, «Sin tótem» y estados. No se usa desenfoque ni una capa recuperable de Word. Los píxeles sustituidos no están presentes en la copia; esto no elimina información que ya existiera en Git.

[Control de privacidad](Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/CONTROL_PRIVACIDAD_PRACTICA_2026-11-17.md) · [Registro de las ocho máscaras](REGISTRO_SANITIZACION_PRACTICA_2026-11-17.json).

## Riesgos de los dos históricos

API_01 contiene un UID coincidente con F03, reportado como tarjeta de prueba. F18 lo muestra visualmente como bloqueado en un momento histórico; no se verificó su estado vigente ni su desvinculación de una persona. HARDWARE_01 es el original de F02; la anotación no permite identificar de forma fiable un UID completo ni confirmar si es la misma tarjeta.

**Si cualquiera de esas tarjetas está activa, la exposición puede facilitar suplantación de lecturas bajo las condiciones descritas en la recomendación.** No se confirmó una suplantación, ni exposición de clave API, ni uso vigente. Se recomienda cotejo privado autorizado y, si corresponde, bloqueo/desvinculación y reemplazo. No se ejecutó ninguna acción operativa.

[Recomendación específica de protección](RECOMENDACION_HISTORICOS_PRIVACIDAD_2026-11-17.md). Los históricos no fueron sobrescritos. Una variante pública nueva no haría desaparecer las versiones anteriores: no se certifica saneamiento completo del historial ni se reescribe Git.

## Verificaciones finales

Nueve documentos abiertos/renderizados con LibreOffice; PDFs convertidos a PNG para revisión. PPTX: 14 láminas; APT: 20 apartados. Office validado por CRC/XML; diagramas originales comparados por contenido incrustado; PNG sanitizadas verificadas como aplanadas y sin metadatos, con igualdad exacta de píxeles fuera de máscaras. No se incorporan los originales privados ni figuras no sanitizadas con UID.

Los hashes de origen, de documentos y de copias protegidas están en [manifiesto](MANIFIESTO_PRACTICA_2026-11-17.json) y [SHA-256](SHA256_PRACTICA_2026-11-17.txt); el propio índice no se autoincluye y se añade la fotografía reutilizada. Las 34 huellas de la entrega consolidada anterior siguen verificando. Los textos nuevos se comprueban también contra /dev/null, porque git diff --check por sí solo no inspecciona archivos no rastreados.

## Recomendación para el siguiente paso

Se puede proceder al siguiente commit estrictamente documental cuando el usuario lo autorice, tras repetir estado remoto/local. La selección nueva está protegida y los pendientes académicos y técnicos siguen explícitos. Mantener abierta la revisión privada del uso actual de las tarjetas históricas; esta preparación no autoriza publicar ni operar sobre tarjetas, bases o servidor.

No se hizo commit ni push. La autorización para enmascarar imágenes fue aplicada; la publicación sigue pendiente.

Las capturas sanitizadas de terminal y CSV se ampliaron en páginas A3 horizontales de los informes y de la vista Física; sus PNG originales protegidas permanecen idénticas.


Resultado final verificado: 31 archivos nuevos, cero cambios en los 122 preexistentes; 31/31 huellas de preparación, 34/34 de la entrega anterior y 32/32 de fuente correctas. Ocho máscaras opacas verificadas, cuatro copias seleccionadas; cero cambios de píxeles fuera de las zonas sensibles. OCR complementario sin coincidencias de los identificadores protegidos en las ocho salidas. Comprobaciones CRC/XML, matriz 18/29, 20 apartados APT, 14 diapositivas y referencias correctas. git diff --check y comprobación de textos nuevos sin staging correctos. HEAD 48f4a4b y rama documental sin cambios; no se hizo commit ni push.
