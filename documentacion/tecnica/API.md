# API existente

Inventario de rutas consultadas en `api.py` y `sesiones_administracion.py` en la rama `feature/paso68h-sesiones-docentes-admin` (26-11-2026). No es una salida runtime de `app.url_map` ni sustituye las pruebas de autorización.

| Métodos | Ruta | Función |
|---|---|---|
| GET | `/` | `mostrar_inicio` |
| GET | `/<path:filename>` | `static` |
| GET | `/alumnos` | `consultar_alumnos_api` |
| GET | `/asistencias` | `consultar_asistencias_api` |
| GET | `/asistencias/exportar/<periodo>` | `exportar_asistencias_api` |
| GET | `/atrasos` | `consultar_atrasos_api` |
| GET | `/estado` | `consultar_estado` |
| GET | `/inasistencias` | `consultar_inasistencias_api` |
| GET | `/index.html` | `mostrar_panel` |
| POST | `/lectura` | `recibir_lectura` |
| POST | `/panel/alumnos/editar` | `editar_alumno_panel` |
| POST | `/panel/alumnos/estado` | `cambiar_estado_alumno_panel` |
| POST | `/panel/alumnos/registrar` | `registrar_alumno_panel` |
| GET | `/panel/calendario/jornada` | `consultar_jornada_escolar_panel` |
| POST | `/panel/calendario/jornadas/editar` | `editar_jornada_calendario_panel` |
| GET | `/panel/calendario/jornadas/historial` | `consultar_historial_calendario_panel` |
| POST | `/panel/calendario/jornadas/registrar` | `registrar_jornada_calendario_panel` |
| GET | `/panel/calendario/mes` | `consultar_calendario_mensual_panel` |
| GET | `/panel/calendario/token` | `obtener_token_calendario_panel` |
| GET | `/panel/csrf-token` | `obtener_token_administrativo` |
| POST | `/panel/login-individual` | `iniciar_sesion_panel_individual` |
| POST | `/panel/logout` | `cerrar_sesion_panel` |
| GET | `/panel/seguimiento/casos` | `seguimiento.listar_casos_panel_api` |
| POST | `/panel/seguimiento/casos/<int:caso_id>/contactos` | `seguimiento_gestiones.registrar_contacto` |
| POST | `/panel/seguimiento/casos/<int:caso_id>/estado` | `seguimiento_gestiones.actualizar_estado` |
| GET | `/panel/seguimiento/casos/<int:caso_id>/historial` | `seguimiento.historial_administrativo_api` |
| POST | `/panel/seguimiento/casos/<int:caso_id>/mensajes` | `seguimiento_gestiones.registrar_mensaje` |
| GET | `/panel/sesion` | `consultar_sesion_panel` |
| GET | `/panel/sesiones-docentes` | `sesiones_administracion.listar_sesiones` |
| GET | `/panel/sesiones-docentes/<int:sesion_id>` | `sesiones_administracion.detalle_sesion` |
| GET | `/panel/tarjetas` | `consultar_tarjetas_panel` |
| POST | `/panel/tarjetas/asignar` | `asignar_tarjeta_panel` |
| POST | `/panel/tarjetas/bloquear` | `bloquear_tarjeta_panel` |
| POST | `/panel/tarjetas/desbloquear` | `desbloquear_tarjeta_panel` |
| POST | `/panel/tarjetas/extraviada` | `marcar_tarjeta_extraviada_panel` |
| POST | `/panel/tarjetas/registrar` | `registrar_tarjeta_panel` |
| POST | `/panel/tarjetas/vincular` | `vincular_tarjeta_panel` |
| GET | `/panel/totems` | `consultar_totems_panel` |
| POST | `/panel/totems/estado` | `cambiar_estado_totem_panel` |
| POST | `/panel/totems/registrar` | `registrar_totem_panel` |
| GET | `/profesor/asignaciones` | `consultar_asignaciones_profesor` |
| GET | `/profesor/asignaciones/<int:asignacion_id>/sesiones` | `consultar_sesiones_clase_api` |
| GET | `/profesor/cursos/<curso>/alumnos` | `consultar_alumnos_curso_profesor` |
| GET | `/profesor/cursos/<curso>/asistencia` | `consultar_asistencia_curso_profesor` |
| POST | `/profesor/login` | `iniciar_sesion_profesor` |
| POST | `/profesor/logout` | `cerrar_sesion_profesor` |
| POST | `/profesor/seguimiento/casos` | `seguimiento.crear_caso_profesor_api` |
| GET | `/profesor/seguimiento/casos` | `seguimiento.listar_casos_profesor_api` |
| GET | `/profesor/seguimiento/casos/<int:caso_id>/historial` | `seguimiento.historial_profesor_api` |
| GET | `/profesor/sesion` | `consultar_sesion_profesor` |
| POST | `/profesor/sesiones` | `crear_sesion_clase_api` |
| GET | `/profesor/sesiones/<int:sesion_id>` | `consultar_detalle_sesion_clase_api` |
| POST | `/profesor/sesiones/<int:sesion_id>/asistencia` | `registrar_asistencia_clase_api` |
| POST | `/profesor/sesiones/<int:sesion_id>/confirmar` | `confirmar_sesion_clase_api` |
| GET | `/seguimiento.html` | `mostrar_seguimiento_administrativo` |
| POST | `/seguimiento/operador/login` | `seguimiento_sesiones.iniciar_sesion_operador` |
| POST | `/seguimiento/operador/logout` | `seguimiento_sesiones.cerrar_sesion_operador` |
| GET | `/seguimiento/operador/sesion` | `seguimiento_sesiones.consultar_sesion_operador` |

## Contratos y autorización

- `/estado`: público; comprueba disponibilidad de la aplicación, no integridad de SQLite ni salud del lector.
- `/lectura`: POST JSON con `codigo_totem`, `uid`, `evento_id` de tipo texto y no vacíos; cabecera `X-API-Key`. 401 sin clave válida; 400 JSON inválido; 403 dispositivo no autorizado/inactivo; 200 para resultados de negocio, incluidos rechazos de tarjeta. No asumir que todo 200 es asistencia registrada.
- `/panel/login-individual`: JSON `usuario`, `password`; 200 válido; 401 inválido/inactivo; Dirección obtiene identidad de Seguimiento, sin acceso al panel general.
- `/profesor/login`: JSON `usuario`, `password`; cuenta activa de rol profesor.
- Sesiones mediante cookies firmadas. Las escrituras requieren `X-CSRF-Token` según dominio: panel, profesor, calendario o seguimiento. Consultar token en el endpoint correspondiente; no son intercambiables.
- `/panel/calendario/jornadas/*`: escritura deshabilitada salvo `MPAZ_CALENDARIO_ESCRITURA_HABILITADA=si`; además exige sesión administrativa y token de calendario.
- `/asistencias/exportar/<periodo>`: sesión administrativa; periodos diario, semanal, mensual, anual; CSV UTF-8 BOM, separador punto y coma. No existe exportador PDF/XLSX en esta API.

## Sesiones docentes y consulta administrativa

La asistencia de aula se guarda en `sesiones_clase` y `asistencias_clase`; es independiente de la tabla `asistencias` usada por el flujo RFID. Las operaciones de sesión docente no modifican las marcas RFID.

### Docencia

- `GET /profesor/asignaciones`: devuelve asignaciones activas del profesor autenticado.
- `GET /profesor/asignaciones/<int:asignacion_id>/sesiones`: lista sesiones de una asignación autorizada.
- `POST /profesor/sesiones`: JSON con `asignacion_id`, `fecha` y `hora_inicio`. Devuelve 201 al crear y 200 si recupera una sesión existente con la misma clave única.
- `GET /profesor/sesiones/<int:sesion_id>`: devuelve sesión y marcas. En borrador incluye la nómina activa del curso; los estudiantes sin marca aparecen como `sin_verificar`.
- `POST /profesor/sesiones/<int:sesion_id>/asistencia`: JSON con `alumno_id`, `estado` (`presente`, `atrasado`, `no_presente`) y `observacion` opcional de hasta 500 caracteres.
- `POST /profesor/sesiones/<int:sesion_id>/confirmar`: confirma únicamente cuando todos los estudiantes activos del curso tienen marca.

Las rutas POST docentes requieren sesión de profesor y `X-CSRF-Token` docente. La API comprueba en el servidor la asignación, sesión y pertenencia del estudiante al curso. Entre las respuestas de negocio se encuentran 401 (sin sesión), 403 (sin permiso/CSRF), 400 (datos inválidos), 409 (sesión incompleta o no editable) y 500 (error no recuperable). La creación existente responde 200; la nueva, 201.

### Administración: consulta de sesiones

- `GET /panel/sesiones-docentes`: exige operador activo de rol `administracion` y panel autorizado. Admite `fecha`, `curso`, `asignatura`, `estado` y `pagina`; la página contiene hasta 50 filas.
- `GET /panel/sesiones-docentes/<int:sesion_id>`: devuelve el resumen de una sesión o 404 si no existe.

Los estados de filtro son `borrador`, `confirmada` y `anulada`. El listado devuelve conteos de presentes, atrasados, no presentes y pendientes. Los pendientes se calculan para borradores; una sesión confirmada devuelve cero. La consulta no devuelve nombres ni observaciones individuales y ejecuta SQLite en modo `query_only`. Dirección no tiene permiso para este blueprint. Las respuestas llevan `Cache-Control: no-store`.

El detalle de flujo, permisos, estados, límites y pruebas está en [SESIONES_DOCENTES.md](SESIONES_DOCENTES.md). No existe una ruta API de anulación en esta rama y no se declara una especificación OpenAPI completa.

El esquema completo de entradas y errores de cada endpoint aún requiere formalización; consultar validaciones del código y pruebas. No se declara un contrato OpenAPI completo.

## Cambios de la continuación

Los tres logins pueden responder **429** con Retry-After; límites en SEGURIDAD_WEB.md. Las sesiones requieren registro SQLite vigente, expiran por inactividad/límite absoluto y se revocan al cerrar sesión o cambiar credencial/rol. Cookies antiguas requieren nuevo login. Falta de tablas de seguridad o error operativo: 503 sin detalles internos. Los permisos y rutas del inventario se conservan.

El calendario ahora registra el actor del servidor como `operador:<id>`; no acepta un actor suministrado por el cliente. Los tokens Unicode inválidos se rechazan sin excepción y canal/estado JSON de tipo incorrecto devuelve 400.
