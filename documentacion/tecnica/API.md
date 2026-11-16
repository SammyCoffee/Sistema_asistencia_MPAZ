# API existente

Inventario generado desde `app.url_map` en la auditoría del 16-11-2026. No constituye prueba de autorización de cada ruta.

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

El esquema completo de entradas y errores de cada endpoint aún requiere formalización; consultar validaciones del código y pruebas. No se declara un contrato OpenAPI completo.
