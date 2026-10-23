# CU-01 · Registrar asistencia con tarjeta RFID — Vista de procesos UML

**Proyecto:** Sistema MPAZ RFID · **Ficha 05** · Sección **003D**  
**Estado:** esquema documental para revisión del equipo y docente; no es una prueba de ejecución.

```mermaid
flowchart TD
    START((Inicio))
    A01["A01 · Estudiante acerca tarjeta RFID al PN532"]
    A02["A02 · ESP32 / PN532 lee UID"]
    A03["A03 · ESP32 genera evento_id"]
    A04["A04 · ESP32 envía POST /lectura con JSON y X-API-KEY"]
    A05["A05 · API Flask comprueba clave y campos"]
    D01{"¿Clave y datos válidos?"}
    A06["A06 · Backend valida tótem"]
    D02{"¿Tótem autorizado y activo?"}
    A07["A07 · Backend consulta tarjeta y alumno"]
    D03{"¿Tarjeta y alumno autorizados?"}
    A08["A08 · Backend comprueba evento_id"]
    D04{"¿Evento ya procesado?"}
    A09["A09 · Backend aplica reglas de entrada / salida"]
    A10["A10 · SQLite registra según reglas"]
    A11["A11 · API devuelve JSON de resultado"]
    A12["A12 · ESP32 emite señal y queda disponible"]
    A13["A13 · API rechaza lectura con motivo"]
    A14["A14 · API responde evento_repetido sin insertar"]
    END((Fin))
    START --> A01 --> A02 --> A03 --> A04 --> A05 --> D01
    D01 -- Sí --> A06 --> D02
    D01 -- No --> A13 --> END
    D02 -- Sí --> A07 --> D03
    D02 -- No --> A13
    D03 -- Sí --> A08 --> D04
    D03 -- No --> A13
    D04 -- No --> A09 --> A10 --> A11 --> A12 --> END
    D04 -- Sí --> A14 --> END
    style A13 fill:#ffe8e8,stroke:#b0474e
    style A14 fill:#ffe8e8,stroke:#b0474e
    style A10 fill:#fff1d5,stroke:#a77a24
```

## Correspondencia con la ficha

- **Vista de escenarios (+1):** CU-01 · Estudiante registra asistencia presentando tarjeta ante el tótem.
- **Vista de procesos:** A01–A14, validaciones, caminos alternativos y responsables lógicos.
- **Componentes:** PN532/ESP32, API Flask, validaciones del backend, SQLite.
- **Condiciones de validación:** clave API y campos, tótem activo, tarjeta/alumno autorizado y evento no procesado.
- **Limitaciones:** un diagrama no demuestra que el recorrido completo se probó; falta correlacionar una nueva lectura con su registro persistido.

**Fuente editable DOT:** [Abrir .dot](MPAZ_RFID_Ficha05_Diagrama_Actividades_UML.dot). La [versión PNG](MPAZ_RFID_Ficha05_Diagrama_Actividades_UML.png), el [SVG](MPAZ_RFID_Ficha05_Diagrama_Actividades_UML.svg) y la [Ficha 05 Word](Ficha_Avance_05_MPAZ_RFID_003D_PARA_REVISION.docx) están subidos en la misma carpeta desde el 23-10-2026; pendientes de revisión académica.
