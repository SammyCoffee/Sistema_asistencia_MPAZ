# Plan de evidencias técnicas — pendientes de recopilación

**Proyecto:** Sistema MPAZ RFID · Capstone APT122  
**Estado:** organización preparada; **ningún pantallazo técnico se marca como realizado o entregado**.

Esta lista corresponde a evidencia de ejecución que se recogerá **paso a paso**. No es necesario capturarla ni subirla ahora. El código y las fichas de avance que ya están en el repositorio **no cuentan automáticamente** como capturas o pruebas documentadas.

| N.º | Estado | Nombre de archivo sugerido | Qué demostrar | Carpeta de destino |
|---|---|---|---|---|
| 01 | [ ] Pendiente | `01_Arquitectura_Sistema.png` | Diagrama ESP32–PN532–Wi-Fi–API–SQLite–panel | `Evidencias_Documentacion/` |
| 02 | [ ] Pendiente | `02_Base_Datos_SQLite.png` | Esquema/tablas con datos de demostración | `Base_de_Datos/` |
| 03 | [ ] Pendiente | `03_API_Flask_Estado.png` | Resultado real de `GET /estado` | `Evidencias_Sistema_Aplicacion/` |
| 04 | [ ] Pendiente | `04_Asistencia_Registrada.png` | Respuesta exitosa a lectura con tarjeta ficticia | `Evidencias_Sistema_Aplicacion/` |
| 05 | [ ] Pendiente | `05_Control_Duplicados.png` | Rechazo de asistencia duplicada o evento repetido | `Evidencias_Sistema_Aplicacion/` |
| 06 | [ ] Pendiente | `06_Login_Panel.png` | Pantalla de acceso sin credenciales | `Evidencias_Sistema_Aplicacion/` |
| 07 | [ ] Pendiente | `07_Panel_Asistencias.png` | Vista de asistencias con registros ficticios | `Evidencias_Sistema_Aplicacion/` |
| 08 | [ ] Pendiente | `08_Reporte_Excel.png` | Reporte exportado y abierto con datos ficticios | `Evidencias_Sistema_Aplicacion/` |
| 09 | [ ] Pendiente | `09_Totem_ESP32.jpg` y `09_Lectura_PN532.png` | Montaje real y lectura de tarjeta de prueba | `Evidencias_Sistema_Aplicacion/` |
| 10 | [ ] Pendiente | `10_Integracion_Completa.png` | Recepción desde el tótem y registro en el servidor | `Evidencias_Sistema_Aplicacion/` |

## Criterios para aceptar cada evidencia

1. La funcionalidad debe haberse probado realmente; una captura no debe hacer pasar un componente incompleto por terminado.
2. Utilizar **exclusivamente datos de demostración** y ocultar identificadores de estudiantes, credenciales, tokens, claves y direcciones internas sensibles.
3. Conservar la captura original y añadir, cuando sea útil, una breve nota con el objetivo, el resultado esperado y el resultado observado.
4. Revisar con el docente qué capturas exige formalmente la pauta; la lista anterior es una **propuesta de respaldo técnico**, no una sustitución de la rúbrica.
5. Marcar cada casilla únicamente una vez verificada la evidencia y subido el archivo a su carpeta.

## Relación con la Fase 1

La guía 1.5 incluye la **planificación** de las evidencias. La ejecución documentada (capturas y pruebas) se guardará en la **Fase 2** conforme esté disponible. No duplicar imágenes entre fases si basta con una referencia.

## Paso siguiente (cuando se retome)

Comenzar con `02_Base_Datos_SQLite.png` usando la base de demostración y después continuar con la API, el panel y la integración de hardware. Por ahora **todo permanece pendiente**.
