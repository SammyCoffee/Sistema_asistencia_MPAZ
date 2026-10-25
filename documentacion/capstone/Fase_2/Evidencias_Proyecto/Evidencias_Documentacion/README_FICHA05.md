# Ficha de Avance 05 — Capstone MPAZ RFID

**Sección:** 003D  
**Estado:** Word, PNG, SVG, fuente DOT y representación Mermaid **subidos en esta rama**; revisión académica pendiente.

## Archivos disponibles en GitHub

- [Diagrama editable DOT](MPAZ_RFID_Ficha05_Diagrama_Actividades_UML.dot).
- [Vista de procesos UML con diagrama renderizable (Mermaid)](MPAZ_RFID_Ficha05_Diagrama_Actividades_UML.md).

## Archivos subidos el 23-10-2026

- [x] [Ficha de Avance 05 Word para revisión](Ficha_Avance_05_MPAZ_RFID_003D_PARA_REVISION.docx)
- [x] [Diagrama de actividades UML PNG](MPAZ_RFID_Ficha05_Diagrama_Actividades_UML.png)
- [x] [Diagrama de actividades UML SVG](MPAZ_RFID_Ficha05_Diagrama_Actividades_UML.svg)

Se conservaron las rutas internas del ZIP y todas las fichas anteriores. La carga no implica aprobación docente ni validación técnica adicional.

**Carpeta de destino:** `documentacion/capstone/Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/`

## Referencias disponibles

- [Ficha 04, conservada sin alterar](Ficha_Avance_04_MPAZ_RFID_FINAL.docx)
- [Casos de uso, flujo y arquitectura (PDF)](MPAZ_RFID_Diagramas_para_Profesor.pdf)
- [Evidencias técnicas del documento 2.4](../README_EVIDENCIAS_2.4.md)
- [Control de evidencias restantes](../PLAN_EVIDENCIAS_PENDIENTES.md)

## Precauciones académicas

La Ficha 05 mantiene **87,5 % como dato declarado en la Ficha 04**, sin afirmar que se ha confirmado un nuevo porcentaje. Ya existe la prueba correlacionada de una nueva asistencia SIMULADA con Flask.test_client y SQLite temporal; faltan el hardware físico, la exportación, el piloto y la validación del docente; las capturas del panel están subidas. No alterar la autoría histórica ni asignar firmas.

**No modificar código ni `main` ni fusionar ramas.**

## Nueva evidencia de terminal — 25-10-2026

**Disponible como transcripción del equipo:** [Prueba aislada de API y SQLite sin hardware](../Evidencias_Sistema_Aplicacion/F05_2026-10-25_PRUEBA_SIMULADA_API_SQLITE.md). La ejecución informa `entrada_registrada`, correlación del mismo `evento_id` (0→1), `evento_repetido` (1→1), rechazo de tótem inactivo (403), rechazo sin clave (401) y GET `/estado` (200). 

**Límite:** fue una simulación `Flask.test_client()` con BD temporal y versión local `d167c1c`, no una prueba física del ESP32 ni del servidor escolar; el Word actualizado del 25-10-2026 está disponible en la carga complementaria. No recalcular el 87,5 % de la Ficha 04 sin revisar F01–F09.

## Prueba F05 ejecutada por el equipo el 25/10/2026

- [x] [TXT original de terminal (contenido)](../Evidencias_Sistema_Aplicacion/F05_2026-10-25_PRUEBA_SIMULADA_TERMINAL_ORIGINAL.txt).
- [x] [Informe de resultados y alcance](../Evidencias_Sistema_Aplicacion/F05_2026-10-25_PRUEBA_SIMULADA_API_SQLITE.md).
- [x] [Script de prueba reutilizable](Material_de_Apoyo/Prueba_Ficha05_MPAZ_sin_hardware.py).
- [x] Word actualizado del 25/10/2026 subido; enlace en la carga complementaria. Word anterior conservado como borrador histórico.
- [x] Capturas DOCENTE_01/02/03 subidas; enlaces en la carga complementaria.

Alcance 7/7: GET /estado 200, lectura simulada HTTP 200 → SQLite 0→1 con evento_id correlacionado, evento_repetido 1→1, tótem inactivo 403, sin clave 401. **No significa validación física del ESP32 ni del PN532.**


## Carga complementaria Ficha 05 — 25-10-2026

Los cuatro archivos originales están subidos con sus nombres conservados:

- [x] [DOCENTE_01_Sesiones_Asistencia_1A_2026-10-22(1).png](https://github.com/SammyCoffee/Sistema_asistencia_MPAZ/blob/capstone/organizacion-evidencias/documentacion/capstone/Fase_2/Evidencias_Proyecto/Evidencias_Sistema_Aplicacion/DOCENTE_01_Sesiones_Asistencia_1A_2026-10-22(1).png)
- [x] [DOCENTE_02_Registro_Parcial_2_de_5_2026-10-22(1).png](https://github.com/SammyCoffee/Sistema_asistencia_MPAZ/blob/capstone/organizacion-evidencias/documentacion/capstone/Fase_2/Evidencias_Proyecto/Evidencias_Sistema_Aplicacion/DOCENTE_02_Registro_Parcial_2_de_5_2026-10-22(1).png)
- [x] [DOCENTE_03_Sesion_Confirmada_4B_2026-10-21(1).png](https://github.com/SammyCoffee/Sistema_asistencia_MPAZ/blob/capstone/organizacion-evidencias/documentacion/capstone/Fase_2/Evidencias_Proyecto/Evidencias_Sistema_Aplicacion/DOCENTE_03_Sesion_Confirmada_4B_2026-10-21(1).png)
- [x] [Ficha_Avance_05_MPAZ_RFID_003D_ACTUALIZADA_2026-10-25_PARA_ENTREGA(2).docx](https://github.com/SammyCoffee/Sistema_asistencia_MPAZ/blob/capstone/organizacion-evidencias/documentacion/capstone/Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Ficha_Avance_05_MPAZ_RFID_003D_ACTUALIZADA_2026-10-25_PARA_ENTREGA(2).docx)

La [Ficha 05 anterior](https://github.com/SammyCoffee/Sistema_asistencia_MPAZ/blob/capstone/organizacion-evidencias/documentacion/capstone/Fase_2/Evidencias_Proyecto/Evidencias_Documentacion/Ficha_Avance_05_MPAZ_RFID_003D_PARA_REVISION.docx) se conserva sin cambios como **borrador histórico**. El Word actualizado es la versión preparada para entrega; revisión y aprobación docente pendientes. Las capturas respaldan sesiones del panel docente, registro parcial 2 de 5 y sesión confirmada. No acreditan por sí solas login, persistencia tras recarga, exportación, piloto ni integración física completa.

El TXT original de terminal y su informe técnico se conservan en sus rutas existentes, sin duplicarlos. Se mantiene la distinción entre simulación API/SQLite y validación física ESP32/PN532; no se recalcula el porcentaje histórico de la Ficha 04.
