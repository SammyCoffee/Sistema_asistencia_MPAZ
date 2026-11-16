# Arquitectura existente y permisos

## Organización

- Raíz: backend Flask, acceso SQLite, utilitarios CLI, simuladores y migradores históricos.
- `interfaz_prueba/`: portada, administración, hojas de estilo y scripts por módulo; subcarpeta `profesor/` para portal docente.
- `migraciones/`: cuatro migraciones SQL, calendario (001), auditoría (002), seguimiento (003), operadores (004).
- `data/`: ubicación histórica de SQLite y seis respaldos ya rastreados; no utilizar para pruebas.
- `documentacion/capstone/`: evidencias académicas; no modificadas.
- `tests/`: pruebas nuevas con unittest y prueba JavaScript aislada.

## Dependencias entre módulos

`api.py` crea Flask y registra `seguimiento_api`, `seguimiento_sesiones` y `seguimiento_gestiones_api`. Las consultas y escrituras se delegan a `base_datos`, `consultar_alumnos`, `consultar_asistencia`, `calendario_*` y `seguimiento_*`.

`procesar_lectura_totem` valida el dispositivo; `registrar_asistencia.procesar_asistencia` cierra jornadas pendientes, comprueba tarjeta y alumno, y llama a `base_datos.guardar_asistencia`. Esa escritura serializa mediante `BEGIN IMMEDIATE` y consulta evento previo en tres columnas. La autorización de tarjeta y estudiante ocurre antes de esa transacción; falta probar cambios de estado simultáneos con la lectura.

`cerrar_jornadas_automaticamente.py` llama al cierre de jornadas; no se confirmó su programación como timer/cron. El mismo cierre también se invoca al procesar tarjetas. No deducir que ocurre puntualmente a las 17:00 si no hay lecturas ni programación externa.

`exportar_asistencias_csv` consulta SQLite y guarda un CSV privado en `reportes/`. `respaldar_base_datos` utiliza la API de respaldo SQLite y verifica integridad y referencias en la copia. No automatiza retención ni recuperación.

`cola_pendientes.py` conserva eventos locales mediante bloqueo Linux y escritura atómica. `reenviar_pendientes.py` confirma individualmente los eventos procesados, sin sobrescribir altas concurrentes. Una cola corrupta provoca error y conserva el archivo para revisión. Esta cola corresponde a scripts Python, no demuestra el almacenamiento offline del ESP32.

## Matriz de permisos observada

| Operación | Anónimo | Docente activo | Administración activa | Dirección activa |
|---|---|---|---|---|
| Portada, login, `/estado` | Sí | Sí | Sí | Sí |
| `/lectura` | Solo con clave API y tótem autorizado | Clave requerida | Clave requerida | Clave requerida |
| Panel, alumnos, tarjetas, tótems, reportes | No | No | Sí | No |
| Jornadas de calendario | No | No | Consulta; escritura con habilitación y CSRF | No |
| Sesiones y alumnos docentes | No | Cursos/asignaciones propios | No por sesión administrativa | No |
| Crear caso docente | No | Sesión propia y asistencia coincidente | Sin endpoint equivalente verificado | Sin endpoint equivalente verificado |
| Listar/historial de seguimiento | No | Cursos asignados | Sí | Sí |
| Mensajes y estados de seguimiento | No | Sin endpoint de escritura equivalente | Sí, CSRF | Sí, CSRF |
| Registrar contacto con apoderado | No | No | Sí, CSRF | No |

Las identidades administrativas se almacenan en `seguimiento_operadores`. El rol `administrador` de la tabla histórica `usuarios` no equivale a `administracion` y no habilita el login individual del panel.

Se revalida la cuenta administrativa activa y, en esta rama, la cuenta docente activa. Las cookies Flask son firmadas, no un almacén central de sesiones: logout elimina la cookie del cliente, pero no revoca una copia robada de esa cookie. Revocación por dispositivo/contraseña requiere diseño adicional.

Las páginas estáticas no son una frontera de datos: algunos HTML docentes pueden descargarse sin sesión, pero las API deben proteger cada dato. `/index.html` y `/seguimiento.html` tienen control explícito. No se comprobó exhaustivamente cada variante de ruta estática.

## Reglas temporales y limitaciones

- Antirrebote: menos de 30 segundos desde la entrada; a los 30 segundos permite salida.
- Una entrada y una salida por alumno y fecha.
- Cierre automático de pendientes a las 17:00, incluidos días anteriores.
- El código usa `datetime.now()`/`date.today()` sin `ZoneInfo`: depende de la zona del proceso. No se validó horario de verano de Chile.
- Primera lectura después de las 17:00 puede crear entrada posterior a la hora que utilizará un cierre ulterior; requiere decisión institucional antes de cambiar la regla.
- Calendario resuelve prioridad curso → general, pero las inasistencias se calculan a partir de fechas con registros RFID y los atrasos usan 08:20 fijo. No hay integración completa entre ambas reglas.

## Mantenibilidad

`api.py`, `base_datos.py` y `app.js` concentran varias responsabilidades. Los scripts CLI duplican acciones del panel y algunos migradores ejecutan escrituras al importarse. `main.py` solo imprime un saludo. No se eliminó código por inferir que está sin uso.

El catálogo de cursos se repite en Python/JavaScript; hay validaciones de RUT en más de un módulo. `README_INSTALACION.md` anterior contenía instrucciones truncadas de Git y copia de datos: se reemplazó por instalación ficticia aislada. El manual histórico y comentarios sobre login compartido requieren actualización posterior; no son especificación vigente.
