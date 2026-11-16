# Seguridad web — continuación 16-11-2026

Estado: **implementado y probado en desarrollo**, pendiente de revisión, migración autorizada y despliegue. No se modificaron credenciales ni datos de producción.

## Persistencia compartida entre workers

`seguridad_web.py` se instala antes de los validadores de identidad existentes. Usa SQLite mediante `obtener_conexion()` y requiere la migración aditiva `005_seguridad_web.sql`. No crea tablas al iniciar Flask. Si falta estructura, el acceso falla cerrado (503); no existe fallback a una cookie sin registro ni contador en memoria.

- `web_login_intentos`: claves HMAC, cantidad y expiración. No almacena usuario ni IP en claro.
- `web_sesiones`: HMAC del identificador aleatorio, tipo/ID de identidad, firma de la credencial/rol y tiempos UTC Unix. No almacena la contraseña ni el token sin transformar.
- Las operaciones de limitación y validación de sesión se serializan con `BEGIN IMMEDIATE`. Las conexiones se cierran. No se cambió el modo journal de ninguna base.

## Limitación de login

Aplica a `/panel/login-individual`, `/seguimiento/operador/login` y `/profesor/login`.

- Hasta 10 intentos por identidad/tipo en ventana fija de 300 segundos. Los dos accesos de operadores comparten contador, incluyendo Administración y Dirección.
- Hasta 200 intentos por IP en la misma ventana, para reducir rotación de nombres de usuario.
- Incluye intentos válidos e inválidos. Al exceder: 429 y `Retry-After`; los rechazos no alargan indefinidamente la ventana. Recuperación automática sin desbloqueo manual.
- Usuario normalizado con strip/lower antes de derivar la clave. Contadores almacenados en la misma SQLite visible por los workers. Una prueba lanza tres procesos y comprueba que solo 10 de 18 reservas se aceptan.
- Usa `request.remote_addr`, **no confía en X-Forwarded-For aportado por el cliente**. Una cabecera falsificada no evita el límite.

**Revisión previa a producción:** detrás de Nginx/Cloudflare, remote_addr puede ser el proxy. El límite por IP podría agrupar al establecimiento; probar el tráfico esperado y definir la cadena de proxies confiables antes de introducir ProxyFix o cambiar umbrales. No se alteró red ni proxy. El límite por cuenta funciona independientemente de esa IP. No sustituye monitorización, TLS ni protección del borde.

## Sesiones y revocación

Después de autenticar se vuelve a comprobar la contraseña contra la credencial vigente al emitir la sesión. Esto evita emitir una sesión con una contraseña que haya cambiado entre la autenticación inicial y la emisión.

Cada solicitud autenticada valida el registro persistente, el tipo/ID de identidad, la cuenta activa, su rol, la firma del hash vigente y la expiración. Los validadores administrativos/docentes anteriores siguen funcionando; no se retiraron controles.

- Cookies antiguas sin registro: identidad borrada, reautenticación requerida.
- Logout correcto con CSRF: elimina el registro del servidor y limpia la cookie; una copia anterior ya no obtiene acceso.
- Nuevo login en el mismo navegador: revoca la sesión anterior antes de emitir la nueva. Otros navegadores legítimos permanecen conectados salvo desactivación/cambio de credencial/rol/expiración.
- Cambio de hash de contraseña o rol: invalida las sesiones cuando vuelven a usarse. No se añadió un endpoint de cambio de contraseña; el sistema detecta cambios hechos por el procedimiento administrativo existente.
- Desactivación: acceso denegado y registro de esa sesión eliminado cuando se presenta.
- Cookie válida tras recargar o usar otro worker: recupera sesión si no fue revocada y sigue vigente.

Valores de desarrollo propuestos, sujetos a revisión antes de producción:

| Variable | Por defecto | Efecto |
|---|---|---|
| `MPAZ_SESION_MAX_SEGUNDOS` | 28800 (8 h) | Duración absoluta, aunque exista actividad |
| `MPAZ_SESION_INACTIVIDAD_SEGUNDOS` | 1800 (30 min) | Tiempo máximo entre solicitudes con sesión |

Ambas deben ser enteros positivos. Se mide actividad HTTP, no pulsaciones humanas: un polling puede mantener actividad. Las solicitudes ya autorizadas y en curso no se cancelan retroactivamente al hacer logout. Las filas expiradas se purgan al iniciar sesión y al validar su propio token; no hay tarea nueva de mantenimiento. El control añade lecturas/escrituras SQLite por solicitud autenticada: falta medición de carga representativa.

Se conservan Secure/HttpOnly/SameSite=Lax y CSRF de la primera auditoría. Los tokens se comparan en bytes UTF-8 para rechazar entradas Unicode incorrectas sin TypeError/500. Los cuerpos anidados inválidos en canal/estado de seguimiento devuelven 400.

## Matriz de autorización

La [matriz existente](ARQUITECTURA.md) permanece vigente. El registro persistente no concede permisos nuevos.

| Identidad | Panel/estudiantes/tarjetas/tótems/exportaciones | Docencia | Seguimiento |
|---|---|---|---|
| Administración activa | Sí, con CSRF para escritura | No mediante sesión administrativa | Casos, historial, mensajes, estado, contactos |
| Dirección activa | No | No | Casos, historial, mensajes y estado; sin contactos |
| Docente activo | No | Asignaciones/sesiones/alumnos autorizados | Casos/historial de cursos asignados; creación validada |
| Anónimo/inactivo/sesión revocada | No | No | No |

Pruebas IDOR ejercen asignación ajena, sesión ajena (lectura/escritura/confirmación), estudiante de otro curso e historial de seguimiento. Se comprueba en el backend y se verifican filas en SQLite. Los administradores tienen alcance institucional: no se inventaron restricciones por curso para ese rol. No se cambió quién puede ver casos compartidos por docentes de un mismo curso.

## XSS: inventario de sumideros

| Lugar | Datos | Tratamiento verificado |
|---|---|---|
| `app.js` tablas de asistencia y atrasos | Nombre, curso, fechas y horas | `MPAZDom.celdas`, nodos td con textContent |
| `app.js` resultado de búsqueda | Nombre/curso/ID | `resultadoAlumno`, createElement/textContent/dataset |
| `app.js` análisis por curso | Curso, porcentajes y recuentos | `resumenCurso`, nodos de texto; clases desde constantes |
| `app.js` ficha | Nombre/RUT/UID/estado/ID | Escape de campos antes de interpolar; corrección anterior conservada |
| `app.js` otros innerHTML | Limpieza, opciones y mensajes fijos | Literales sin datos dinámicos; conservados |
| `identidad-mpaz.js` innerHTML | Icono/texto de tema | Dos cadenas constantes elegidas por booleano; conservado |
| Tarjetas/directorio/tótems | Campos de API | createElement/textContent/dataset; sin HTML dinámico encontrado en otros scripts |
| Seguimiento/docente | Descripciones, mensajes, contactos, observaciones e historiales | Construcción de elementos con textContent; inspección estática, pruebas de datos y permisos; sin navegador disponible |
| Exportación | Texto CSV | Neutralización de fórmulas anterior conservada y probada; no es HTML |

La búsqueda de outerHTML, insertAdjacentHTML, document.write, eval/new Function y setters de handlers/URL no encontró otros sumideros de esas clases. Se retiraron logs de arrays completos de asistencias y de la ficha seleccionada. Las pruebas de DOM usan payloads HTML y comprueban nodos/texto/dataset. No prueban todos los navegadores ni sustituyen una política CSP y QA visual.

## Límites de esta entrega

No se implementó MFA, recuperación de contraseña, cambio de contraseña web, CSP completa ni un sistema externo de monitorización. Falta evaluación de carga, cadena de proxy confiable, más fuzzing de entradas, normalización/unicidad histórica de RUT y revisión visual real. La seguridad de sistema operativo, secretos reales y configuración de producción no se inspeccionó en esta continuación.
