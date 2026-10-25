# Ficha 05 — Resultado de pruebas simuladas API + SQLite (sin hardware)

**Proyecto:** Sistema MPAZ RFID · **Sección:** 003D · **Fecha/hora informada:** 2026-10-25 09:32:36 (hora del equipo de ejecución).  
**Versión Git local indicada por la prueba:** `d167c1c`. **Medio:** Python, `Flask.test_client()` y una base de datos SQLite **temporal**, eliminada al finalizar.  
**Origen de esta evidencia:** transcripción de terminal compartida por el equipo el 25-10-2026. **No se ejecutó de forma independiente desde este repositorio** ni se adjuntó todavía el TXT original generado con `tee`.

> **Alcance:** se prueba el procesamiento del backend con UID y tótem ficticios. **No prueba una lectura física PN532, transmisión Wi-Fi del ESP32, despliegue real, login/panel, exportación Excel ni piloto escolar.** El porcentaje de 87,5 % de la Ficha 04 no se modifica automáticamente.

## Resultados observados

| Verificación | Resultado que devolvió el programa | Estado informado |
|---|---|---|
| Crear SQLite temporal | «Tablas creadas correctamente» y `[OK] Esquema de prueba creado` | Aprobada |
| GET `/estado` | HTTP 200 | Aprobada |
| POST `/lectura` con evento nuevo | HTTP 200, `entrada_registrada`, 09:32:36 | Aprobada |
| Correlación del mismo evento en SQLite | Antes: **0** registros; después: **1**; mismo `evento_id` | Aprobada |
| Reenvío idéntico | `evento_repetido`, registros **1 → 1** | Aprobada |
| Tótem desactivado | HTTP 403, `totem_inactivo`, sin nueva escritura | Aprobada |
| Petición sin clave API | HTTP 401, `no_autorizado`, sin nueva escritura | Aprobada |

**Identificadores exclusivamente ficticios:** tótem `TOTEM-F05-SIMULADO`, UID `F05A1B2C`, evento `F05-PRUEBA-5247DE3F908C`.  
**Fila SQLite transcrita:** `('2026-10-25', '09:32:36', 'F05-PRUEBA-5247DE3F908C', 'F05-PRUEBA-5247DE3F908C')`.

La transcripción informa que la base escolar real **no fue utilizada**. El script usa `tempfile.TemporaryDirectory`, fija `MPAZ_DB_PATH` antes de importar los módulos y llama a `api.app.test_client()`; por tanto, la simulación no requiere el servicio remoto ni hardware físico.

## Referencias y trazabilidad

- [Script reproducible utilizado](../Evidencias_Documentacion/Material_de_Apoyo/Prueba_Ficha05_MPAZ_sin_hardware.py).
- [Ficha de avance 05](../Evidencias_Documentacion/Ficha_Avance_05_MPAZ_RFID_003D_PARA_REVISION.docx).
- [Diagrama de actividades UML](../Evidencias_Documentacion/MPAZ_RFID_Ficha05_Diagrama_Actividades_UML.md).
- Código utilizado por el script: `api.py`, `procesar_lectura_totem.py`, `base_datos.py`, `registrar_asistencia.py`.
- La evidencia se relaciona con el flujo de **validación → registro → respuesta y error** de CU-01, **sin involucrar el sensor físico**.

## Próximos respaldos

- [ ] Adjuntar el **TXT original** `prueba_terminal_f05.txt` generado en `~/pruebas_mpaz/evidencias_ficha05/`, después de comprobar que no contenga secretos.
- [ ] Incorporar esta evidencia al Word oficial de la Ficha 05 con fecha, versión `d167c1c` y referencia a la simulación.
- [ ] Probar una lectura real del PN532/ESP32 contra la API y correlacionar con SQLite cuando se cuente con el equipo físico.
- [ ] Confirmar responsables, semana académica, porcentaje actualizado y observación docente.
