# BORRADOR — 1.1 Autoevaluación de competencias Fase 1

> **No corresponde a la plantilla oficial** de Duoc UC. Este documento solo ofrece una propuesta de respuestas personales para copiar/adaptar al formulario APT122 cuando esté disponible. No incluye puntajes ni calificaciones.
>
> **Carácter:** evidencia individual. Debe ser revisada y ajustada por la persona que la presenta.

**Estudiante:** [Apellido y nombre]  
**Carrera:** Ingeniería en Informática — Duoc UC  
**Proyecto:** Sistema MPAZ RFID: Plataforma Inteligente de Asistencia Escolar  
**Fecha:** [Completar]

## Propósito

Presento una reflexión individual sobre las competencias que he puesto en práctica durante la definición y el desarrollo inicial del Sistema MPAZ RFID. La finalidad es reconocer mis avances, las evidencias que los respaldan y las habilidades que debo seguir fortaleciendo.

## Contexto de mi participación

Participo en un proyecto de asistencia escolar que conecta la lectura de tarjetas NFC/RFID con un servidor y una plataforma web. Mi trabajo se concentra principalmente en el software: diseño de base de datos, desarrollo de la API, lógica de registro, interfaz administrativa, pruebas y documentación de integración. La parte física del tótem ESP32 y el lector PN532 se desarrolla de manera coordinada con el otro integrante del equipo.

## Competencias y reflexión personal

### 1. Análisis de necesidades y requisitos

**Lo que he aplicado:** He identificado la necesidad del establecimiento de contar con registros de asistencia más ordenados y oportunos. A partir de ella, he definido reglas como autorización del tótem, validación de tarjetas y prevención de registros duplicados.

**Aspecto por mejorar:** Debo documentar de manera más formal los requisitos, los criterios de aceptación y la validación de cada necesidad con los futuros usuarios.

### 2. Modelamiento y gestión de datos

**Lo que he aplicado:** He trabajado en la estructura de una base de datos SQLite con entidades para estudiantes, tarjetas, tótems y asistencias. He aplicado relaciones y restricciones para organizar los registros y mantener consistencia en el sistema.

**Aspecto por mejorar:** Quiero fortalecer la documentación del modelo, la preparación de datos de demostración y los procedimientos de respaldo y recuperación.

### 3. Desarrollo de software y servicios

**Lo que he aplicado:** He desarrollado y probado componentes en Python y Flask, incluyendo endpoints como `/estado` y `/lectura`, validaciones del registro y un panel web básico. Esto me ha permitido integrar lógica de negocio y acceso a información desde una misma solución.

**Aspecto por mejorar:** Debo mejorar la modularidad, la gestión de errores, la documentación de la API y la facilidad de despliegue del sistema.

### 4. Pruebas y aseguramiento de calidad

**Lo que he aplicado:** He realizado verificaciones de lectura simulada, registro de asistencias, tarjetas activas o bloqueadas y control de eventos repetidos. Estas pruebas me han servido para detectar fallos antes de usar el sistema en condiciones reales.

**Aspecto por mejorar:** Necesito ordenar mejor los casos de prueba, automatizar verificaciones y guardar evidencias reproducibles de los resultados.

### 5. Seguridad y responsabilidad en el manejo de datos

**Lo que he aplicado:** He considerado mecanismos como autenticación del panel y clave de acceso para solicitudes a la API. Comprendo que los registros escolares requieren un tratamiento cuidadoso por incluir información de estudiantes.

**Aspecto por mejorar:** Debo continuar revisando los permisos, la protección de credenciales, el control de acceso y la publicación de datos ficticios o anonimizados en evidencias académicas.

### 6. Trabajo en equipo y gestión de avances

**Lo que he aplicado:** He coordinado el diseño del software con las necesidades de integración del ESP32/PN532, considerando el formato de las lecturas, la comunicación con la API y el funcionamiento general del tótem.

**Aspecto por mejorar:** Necesito registrar con mayor claridad los acuerdos, las responsabilidades de cada integrante, los cambios y las entregas de cada iteración.

## Balance individual de la Fase 1

Considero que mi principal fortaleza es relacionar una necesidad concreta del establecimiento con una solución técnica que combina programación, bases de datos y servicios web. El desarrollo me ha exigido aprender mediante pruebas, corregir errores y documentar decisiones. Al mismo tiempo, reconozco que todavía debo consolidar la planificación formal, la documentación y las pruebas sistemáticas para convertir el prototipo en una herramienta confiable y sostenible.

## Compromisos de mejora

- Elaborar una matriz breve que conecte requisitos, componentes implementados y casos de prueba.
- Actualizar la documentación técnica y los diagramas de base de datos y arquitectura.
- Realizar y registrar pruebas de integración con el tótem utilizando exclusivamente datos de demostración.
- Revisar con el equipo y el docente las prioridades, responsabilidades y pendientes de las siguientes etapas.

## Para finalizar el documento oficial

- [ ] Conseguir el formulario `Apellido_Nombre_1.1_APT122_AutoevaluacionCompetenciasFase1.docx`.
- [ ] Verificar los criterios y la escala de autoevaluación oficiales.
- [ ] Completar el nombre y la fecha de entrega por el canal correspondiente.
- [ ] Ajustar las afirmaciones de primera persona a la participación real de quien firma.
- [ ] No subir RUT, teléfonos, datos reales de alumnos ni otros identificadores sensibles a este repositorio público.
- [ ] Subir versión oficial revisada a `Evidencias_Individuales/` solo cuando corresponda.

### Referencias al proyecto

- [API Flask](../../../../api.py)
- [Base de datos](../../../../base_datos.py)
- [Panel web](../../../../interfaz_prueba/)
- [Documentación de Fase 1](../REVISION_Y_PLAN_ENTREGA.md)
