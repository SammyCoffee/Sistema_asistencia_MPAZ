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

La Ficha 05 mantiene **87,5 % como dato declarado en la Ficha 04**, sin afirmar que se ha confirmado un nuevo porcentaje. Falta la prueba correlacionada de una nueva asistencia, las capturas del panel y la exportación, el piloto y la validación del docente. No alterar la autoría histórica ni asignar firmas.

**No modificar código ni `main` ni fusionar ramas.**

## Nueva evidencia de terminal — 25-10-2026

**Disponible como transcripción del equipo:** [Prueba aislada de API y SQLite sin hardware](../Evidencias_Sistema_Aplicacion/F05_2026-10-25_PRUEBA_SIMULADA_API_SQLITE.md). La ejecución informa `entrada_registrada`, correlación del mismo `evento_id` (0→1), `evento_repetido` (1→1), rechazo de tótem inactivo (403), rechazo sin clave (401) y GET `/estado` (200). 

**Límite:** fue una simulación `Flask.test_client()` con BD temporal y versión local `d167c1c`, no una prueba física del ESP32 ni del servidor escolar; la Ficha 05 Word sigue pendiente de incorporar esta referencia. No recalcular el 87,5 % de la Ficha 04 sin revisar F01–F09.
