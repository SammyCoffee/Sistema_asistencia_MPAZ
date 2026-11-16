# Reglas escolares: contradicciones reproducidas y decisiones pendientes

Estado: **reproducido mediante pruebas; no corregido automáticamente**. La aplicación mantiene sus reglas históricas, salvo que el reloj para nuevos registros ahora usa America/Santiago explícito.

## Evidencia

Los cinco métodos `test_caracteriza_*` de `tests/test_tiempo_calendario.py` pasan cuando reproducen el comportamiento actual. No son criterios de aceptación del cálculo de asistencia.

| Escenario ficticio | Comportamiento actual observado | Riesgo |
|---|---|---|
| Jornada general feriado/suspendida, con una lectura de otro alumno | Cuenta una inasistencia para alumno sin lectura | Penalizar un día no lectivo |
| Domingo con una lectura | Cuenta jornada para otros estudiantes | Computar día fuera del calendario acordado |
| Día lectivo sin lecturas en toda la escuela | Denominador cero | Ocultar una jornada completa; porcentaje no representativo |
| Jornada especial con entrada 10:00, lectura 09:00 | Aparece como atraso por umbral fijo 08:20 | Marcar atraso incorrectamente |
| Consulta semanal frente a CSV semanal en lunes 16-11 | Consulta: 16–22 noviembre; CSV: 10–16 noviembre | Periodos distintos bajo el mismo nombre |
| Entrada 18:00 y cierre posterior del mismo día | Salida automática 17:00 | Salida anterior a entrada |

`obtener_inasistencias` usa fechas distintas con registros RFID para toda la escuela, sin resolver jornada por curso. Los porcentajes derivados de ese denominador heredan el problema. La exportación CSV actual lista marcaciones; no implementa por sí sola el denominador lectivo ni corrige estos cálculos.

## Alternativas para autorización institucional

1. **Calendario como autoridad.** Para cada alumno/curso/fecha, resolver curso → general. Excluir feriados y suspensiones explícitas. Definir el tratamiento de días sin configurar y la fecha de inicio/baja/traslado de cada estudiante. No asumir que todo lunes–viernes es lectivo.
2. **Regla por defecto con excepciones.** Definir lunes–viernes como base solo si la escuela lo aprueba; aplicar feriados/suspensiones y habilitar sábados lectivos expresos. Requiere datos anuales completos y acuerdos sobre vacaciones, jornadas y fechas no configuradas.
3. **Transición conservadora.** Identificar jornadas sin configuración y presentar resultados como incompletos, sin afirmar un porcentaje oficial. No extrapolar silenciosamente desde lecturas de otras personas.

Para reportes: decidir si «semanal» significa semana calendario o últimos siete días y unificar nombres/rangos. No se cambió automáticamente ninguna de las dos convenciones.

Para atrasos: decidir si usar hora_entrada del calendario, tolerancia institucional y regla para falta de horario. Conservar las marcaciones originales y registrar la versión de la regla aplicada al cálculo.

Para cierre después de las 17:00: decidir entre impedir una nueva jornada, dejarla pendiente para revisión, aplicar hora efectiva de jornada especial o cerrar en un instante no anterior a la entrada. No elegir automáticamente ni modificar históricos.

## Criterios de aceptación propuestos

- Feriado/suspensión explícitos no generan inasistencia ni atraso.
- Denominador por curso/alumno, nunca determinado por lecturas de otro curso.
- Jornada lectiva completa sin lecturas sigue siendo visible; distinguir caída técnica de ausencia individual.
- Porcentaje con denominador cero se presenta como no calculable.
- Horarios especiales y cambio de día probados; salida nunca anterior a entrada.
- Reporte y panel usan la misma regla, versión y periodo.
- Tratar estado activo/baja/traslado según política histórica acordada, sin reescribir marcaciones.

Hasta la aprobación, no usar los cálculos actuales como informe oficial sin conciliación. Las cinco pruebas de caracterización deberán convertirse en pruebas de aceptación de la alternativa aprobada, no borrarse para aparentar conformidad.

## Zona horaria implementada

`reloj_escolar.py` utiliza `ZoneInfo('America/Santiago')` para crear nuevos valores civiles de fecha/hora, consultar el día actual, exportar y nombrar respaldos. Los metadatos SQLite con CURRENT_TIMESTAMP/datetime('now') conservan su semántica UTC. El frontend usa Intl con zona explícita para fechas/horas por defecto.

Pruebas cubren el retroceso 05-04-2026 03:00 UTC y el avance 06-09-2026 04:00 UTC, además de una fecha UTC que corresponde al día anterior en Chile. Referencia: [ZoneInfo Python 3.12](https://docs.python.org/3.12/library/zoneinfo.html).

No se modificaron valores históricos. Los campos antiguos TEXT no contienen offset/fold: no puede recuperarse automáticamente el instante UTC de horas repetidas durante DST. El antirrebote sigue calculándose con fecha/hora civil almacenada; lecturas durante la hora repetida o jornadas nocturnas necesitan una definición y esquema de instantes para garantizar ese caso. El firmware y el tratamiento del instante original de eventos offline quedan pendientes.
