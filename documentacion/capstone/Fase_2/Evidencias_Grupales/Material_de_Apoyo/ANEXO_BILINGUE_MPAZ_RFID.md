# Anexo bilingüe — texto de apoyo para revisar (NO entrega oficial)

**Proyecto:** Sistema MPAZ RFID · **Fases 1 y 2** · **Estado:** borrador complementario.

Este material no acredita el cumplimiento de la rúbrica. El docente debe confirmar **en qué documento** deben integrarse los abstracts y las secciones personales de inglés.

## Resumen / Abstract en español

El Sistema MPAZ RFID aborda la necesidad de registrar y consultar la asistencia escolar de manera más ordenada. La solución desarrollada combina tarjetas RFID, un lector PN532 conectado a un ESP32, una API en Python/Flask, una base de datos SQLite y un panel web de gestión. El tótem captura un identificador UID y transmite una lectura con identificador de evento a la API, que comprueba la autorización del dispositivo, el estado de la tarjeta y las reglas de asistencia antes de responder. La documentación disponible acredita el diseño, las tablas principales de SQLite, una consulta con datos de demostración, comunicación ESP32–servidor y una prueba de idempotencia en una copia de base de datos sin duplicar registros. Estas evidencias representan un avance técnico documentado, pero aún se deben completar las pruebas correlacionadas de nueva asistencia, la validación de interfaz y exportación, el piloto escolar y la revisión docente. El dominio público, HTTPS y los permisos diferenciados de docentes se mantienen como funciones previstas.

## Abstract in English

The MPAZ RFID System addresses the need for a more organized way to record and review school attendance. The solution combines RFID cards, a PN532 reader connected to an ESP32 board, a Python/Flask API, an SQLite database, and a web administration panel. The device reads a card UID and sends it with a unique event identifier to the API. The server checks device authorization, card status, and attendance rules before returning a response. Available documentation supports the system design, the main SQLite tables, a query using demonstration data, ESP32-to-server communication, and an idempotency test performed on a test database without creating duplicate records. These results show documented technical progress, but they do not prove complete deployment. Additional evidence is needed for a newly registered attendance event traced end to end, panel access and data exports, a controlled school pilot, and academic review. Public-domain access, HTTPS, and separate teacher permissions remain planned features.

## Individual conclusion — Samantha Tapia (draft to review)

During the MPAZ RFID project, I focused mainly on the software components of the attendance platform, including the Flask API, the SQLite database, and the web interface. I learned that a working endpoint is not enough to guarantee a reliable school system: the project also needs clear validation rules, evidence of successful and rejected events, and careful handling of student data. The available tests helped us identify how the server responds to RFID readings and how repeated events can be handled without creating extra records. However, I still need to strengthen the documentation of complete end-to-end tests and deployment. This experience has helped me connect software development, data modeling, testing, and teamwork with an actual need at the school.

## Individual reflection — Samantha Tapia (draft to review)

One of the main challenges was coordinating the software with the ESP32 and PN532 hardware while keeping the system rules consistent. I also recognized the importance of organizing evidence while development is still in progress, rather than leaving screenshots and test records until the end. My next priority is to work with my teammate to confirm the responsibilities and timeline, gather reproducible demonstrations with test data, and improve the clarity of our technical report. I consider this project an opportunity to grow as a software developer and to practice a responsible approach to information systems used in education.

## Contribution and status of Lucas Baeza

**Pendiente:** Lucas debe redactar o validar sus propias conclusiones y reflexiones en inglés de acuerdo con su participación real. No se redactan ni firman afirmaciones en su nombre.

## Pendientes de formato

- [ ] Confirmar con el docente si estos apartados corresponden al documento 1.5, 2.4 o un informe complementario.
- [ ] Samantha valida y personaliza sus textos individuales.
- [ ] Lucas redacta/valida su conclusión y reflexión individuales.
- [ ] Incorporar portada, índice, bibliografía y formato exigido por la pauta final.
- [ ] No marcar como «Logrado» indicadores de inglés sin comprobar la entrega efectiva.
