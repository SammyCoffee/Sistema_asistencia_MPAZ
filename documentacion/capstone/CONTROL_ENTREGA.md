# Control de Entrega Documental — Capstone MPAZ RFID (17-11-2026)

**Ubicación preparada:** `documentacion/capstone/` (rutas relativas al repositorio)
**Rama técnica de referencia:** `audit/seguridad-continuidad-20261116` (`4268d50`) — *sin modificaciones*
**Rama documental de referencia:** `capstone/organizacion-evidencias` (`fc1aeea`) — *sin modificaciones*

---

## 1. Inventario y Control de Entregables Generados

| Documento | Ruta relativa | Versión | Fuentes utilizadas | Cambios realizados | Evidencias de respaldo | Pendientes de confirmación | Estado |
|---|---|---|---|---|---|---|---|
| Vista Lógica 4+1 (Word + SVG/PNG) | `Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/MPAZ_RFID_Vista_Logica_003D_ACTUALIZADA_2026-11-17.docx` | v2026-11-17 | `Anexo Modelo 4+1(1).pdf`, `base_datos.py`, `migraciones/001..005`, `BASE_DATOS.md` | Incorpora tablas `001`–`005` (`web_sesiones`, `web_login_intentos`, calendario, seguimiento) y reglas de idempotencia/antirrebote | `005_seguridad_web.sql`, 61 tests Python `OK` | Aplicar `005` en producción | Listo para revisión |
| Vista de Desarrollo 4+1 (Word + SVG/PNG) | `Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/MPAZ_RFID_Vista_Desarrollo_003D_ACTUALIZADA_2026-11-17.docx` | v2026-11-17 | `Anexo Modelo 4+1(1).pdf`, `INVENTARIO_CODIGO.md`, `api.py`, `seguridad_web.py` | Actualiza 54 rutas Flask, `seguridad_web.py`, `reloj_escolar.py`, `dom-seguro.js` y blueprints `seguimiento_*` | `INVENTARIO_CODIGO.md`, `test_dom_seguro.cjs` | Confirmar autoría histórica F02/F04 | Listo para revisión |
| Vista de Procesos 4+1 (Word + SVG/PNG) | `Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/MPAZ_RFID_Vista_Procesos_003D_2026-11-17.docx` | v2026-11-17 | `Anexo Modelo 4+1(1).pdf`, `ARQUITECTURA.md`, `registrar_asistencia.py`, `reenviar_pendientes.py` | Unifica flujo `POST /lectura`, `BEGIN IMMEDIATE`, antirrebote `< 30 s`, sesiones/CSRF y timeout de reenvío 10 s | `test_api_flujos.py`, `test_cola.py` | Prueba de carrera desactivación vs lectura | Listo para revisión |
| Vista Física 4+1 (Word + SVG/PNG) | `Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/MPAZ_RFID_Vista_Fisica_003D_2026-11-17.docx` | v2026-11-17 | `Anexo Modelo 4+1(1).pdf`, `AUDITORIA_CONTINUACION_20261116.md` | Diferencia entorno demo aislado, prototipo ESP32/PN532 y despliegue escolar propuesto (HTTPS/Gunicorn) | `F05_2026-10-25...txt`, suite 61+3 | Prueba física PN532→ESP32→API y despliegue escolar | Listo para revisión |
| Vista de Escenarios 4+1 (Word + SVG/PNG) | `Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Vistas_4mas1/MPAZ_RFID_Vista_Escenarios_003D_2026-11-17.docx` | v2026-11-17 | `Anexo Modelo 4+1(1).pdf`, `ARQUITECTURA.md`, `api.py` | Consolida 4 actores y matriz de permisos real (Tótem, Docente, Administración, Dirección) | `test_permisos_crud.py`, `test_seguridad_web.py` | Validación en navegador (`QA_MANUAL.md`) | Listo para revisión |
| Cronograma 18 Semanas (Excel + PNG) | `Fase_2/Evidencias_Proyecto/Cronograma/MPAZ_RFID_Cronograma_18_Semanas.xlsx` + `cronograma_18_semanas_slide7.png` | v2026-11-17 | `Ejemplo Agil Ganntt(1).xlsx`, Fichas `02`–`06`, commits `main` y `audit/...` | Mapea 10 hitos en 18 semanas con hoja `Resumen` (`COUNTA`/`COUNTIF`) sin porcentajes inventados | Fichas `02`–`06`, `git log` | Localizar Ficha 01 y validar calendario oficial | Listo para revisión |
| Informe Final 2.6 Oficial (Word) | `Fase_2/Evidencias_Grupales/2.6_Informe_Final_MPAZ_RFID_003D_OFICIAL_2026-11-17.docx` | v2026-11-17 | `2.6_GuiaEstudiante_Fase 2_Informe Final Proyecto APT.docx`, borrador `2026-11-09`, `audit/...` | Migrado a plantilla oficial de 6 apartados; actualiza pruebas (7/7 vs 61+3) y conserva `$1.758.000 CLP` estimado | `REVISION_ACADEMICA_2026-11-09.md`, suite 61+3 | Áreas de desempeño, competencias y sección 6 personal | Borrador avanzado (con marcadores) |
| Informe Extenso 20 Apartados (Word) | `Fase_2/Evidencias_Grupales/MPAZ_RFID_Informe_Extenso_20_Apartados_003D_2026-11-17.docx` | v2026-11-17 | `Guia_Informe_APT_Completa.pdf`, `Plantilla_Formal_Proyecto_APT.docx` | Generado por separado sobre plantilla formal de 20 apartados, alineado con 4+1, Ficha 06 y `audit/...` | Ficha 06, 4+1, suite 61+3 | Apartados 14, 15 (malla) y 18 (reflexiones) | Borrador avanzado (con marcadores) |
| Presentación Final 14 Diapositivas (PPTX) | `Fase_3/Evidencias_Grupales/MPAZ_RFID_Presentacion_Final_Capstone_003D_2026-11-17.pptx` | v2026-11-17 | `Formato Presentación final(1).pptx`, borrador `PARA_REVISION.pptx`, diagramas y Gantt nuevos | Corrige slide 4 (rechazo duplicados), actualiza slides 7 (Gantt), 8 (Arquitectura), 9 (BD 001–005) y 12 (61+3 + 7/7) | Previews PNG en `05_Evidencias_y_Control/previews/` | Revisión visual final por equipo | Listo para revisión |
| Bitácora Semana 15 (Word) | `Fase_2/Evidencias_Proyecto/Evidencias_Sistema_Aplicacion/Bitacora_Semana_15_MPAZ_RFID_003D_2026-11-17.docx` | v2026-11-17 | `Bitacora_Semana_15_Capstone_2026.docx`, `test_permisos_crud.py`, `test_seguridad_web.py` | Completa tabla de verificación de roles/permisos/salidas con resultados simulados y marca pendientes físicos/QA | Suite 61 Python + 3 JS `OK` | Código de grupo definitivo; prueba física PN532 | Listo para revisión |

---

## 2. Revisión de `0 Detalles F2 Sem 12.pdf` (Fase 2 Parte 1 y Parte 2)

Extraído desde `MPAZ_Profesor_Nuevos_Sem15_y_Sem12_20261117.zip` (`02_REFERENCIA_PREVIA/0 Detalles F2 Sem 12.pdf`, 7 páginas) en `/home/witch4coffee/Work/MPAZ_Material_Profesor/0 Detalles F2 Sem 12.pdf`:

| Requisito de Semana 12 (`0 Detalles F2 Sem 12.pdf`) | Estado en MPAZ RFID | Evidencia / Brecha |
|---|---|---|
| **Parte 1 (Avance, 20%, Sem. 5–9):** Informe de avance (`2.4`) + resumen, objetivos/metodología ajustados y evidencias | **Cumplido para revisión** (evaluación docente pendiente) | `2.4_..._ANEXOS_VERIFICABLES_REVISION.docx` + Fichas 02–05; falta `PLANILLA DE EVALUACION AVANCE FASE 2.xlsx` |
| **Parte 2 (Final, 30%, Sem. 10–15):** Informe final (`2.6`) con 6 apartados + presentación | **Cumplido en estructura oficial** (campos personales pendientes) | `2.6_Informe_Final_MPAZ_RFID_003D_OFICIAL_2026-11-17.docx` + `MPAZ_Fase2_Presentacion.pptx`; falta completar apartado 6 personal y `PLANILLA DE EVALUACION FINAL FASE 2.xlsx` |
| **Checklist Fase 1 (Sem. 07):** `1.1`, `1.2`, `1.3`, `1.4`, `1.5`, Presentación | **Parcialmente cubierto** | Samantha `1.1`–`1.2` y grupales `1.4`–`1.5` disponibles; faltan individuales de Lucas y `1.3` por validar |
| **Checklist Fase 2 — Individual:** `Apellido_Nombre_2.1_APT122_DiarioReflexionFase2.docx` | **Parcialmente cubierto** | Existe `2.1_..._BORRADOR_GRUPAL.docx`; validar con docente si exige archivo individual por integrante |
| **Checklist Fase 2 — Proyecto:** Presentación, Documentación, Sistema/Aplicación y Base de Datos | **Cumplido (simulado) / Requiere nueva evidencia física** | 5 vistas 4+1, Cronograma, Ficha 06, 61+3 tests OK; falta **prueba física PN532→ESP32→API→SQLite** y **QA visual en navegador** |
| **Disponibilidad en Git público** según cronograma | **Pendiente de carga autorizada** | Documentos actualizados listos en `MPAZ_Capstone_Trabajo_2026-11-17/` para subir cuando autorices |

## 3. Materiales del profesor aún no disponibles

- `Pauta del Diario de Reflexión 3.1`: no incluida en los paquetes revisados.

---

## 4. Verificaciones de integridad realizadas

- **Word (`.docx`):** 8 / 8 archivos generados abiertos y validados con `python-docx`.
- **PowerPoint (`.pptx`):** `MPAZ_RFID_Presentacion_Final_Capstone_003D_2026-11-17.pptx` validado con `python-pptx` (14 diapositivas, 20 imágenes) y revisado visualmente vía LibreOffice + `pdftoppm` (`05_Evidencias_y_Control/previews/`).
- **Excel (`.xlsx`):** `MPAZ_RFID_Cronograma_18_Semanas.xlsx` validado con `openpyxl` (2 hojas, 3 fórmulas `COUNTA`/`COUNTIF`).
- **Diagramas (`.dot` / `.svg` / `.png`):** 5 vistas 4+1 + 1 Gantt generados y verificados.

## Corrección final anterior al commit

Este control fue actualizado después de la revisión del paquete original. Los hashes vigentes se consultan en MANIFIESTO_ENTREGA.md y SHA256_ENTREGA_2026-11-17.txt; el ZIP fuente se conserva intacto fuera del repositorio. Las verificaciones de la sección 4 describen la generación original. La nueva revisión y su paginación están en REVISION_INTEGRACION_2026-11-17.md.

Portada y veinte apartados del informe extenso cotejados con Guia_Informe_APT_Completa.pdf; referencias relativas, bibliografía y capturas históricas identificadas. Se mantienen pendientes docente, competencias, áreas oficiales, grupo y reflexiones personales. Los cinco Word 4+1 tienen páginas dedicadas a diagramas; SVG/PNG y medios incrustados conservan su contenido.

Las 61 pruebas son métodos Python y los tres programas son scripts JavaScript ejecutados en entorno aislado. Cinco métodos caracterizan defectos o reglas institucionales abiertas; un resultado OK no certifica finalización funcional. Prueba física PN532/ESP32, QA manual, migración productiva, despliegue y piloto escolar pendientes. No se afirma merge en main. Presentación: redacción de duplicados y nota de alcance corregidas.

Cronograma: impresión horizontal, áreas explícitas y repetición de actividad; dos páginas A3 para tabla y Gantt y una A4 para Resumen. Celdas, fórmulas, actividades, fechas y evidencias se conservan. No se hizo commit ni push.
