# Comprobación visual reproducible con datos ficticios

Estado: **la validación visual sigue pendiente**. El intento del 16-11-2026 no pudo acceder al navegador. La rama contiene además una automatización Chromium para el flujo docente/administrativo; no se encontró evidencia de que se haya ejecutado después del commit de integración `054075b05fe192d4dcda6ee6a993d067d381a1fe`. No marcarla como aprobada hasta guardar el resultado y las capturas.

## Preparación local

Usar Python 3.12, dependencias de requirements y la rama de auditoría. No cargar .env escolar ni copiar bases del servidor.

```bash
python3.12 -m venv /tmp/mpaz-venv312
/tmp/mpaz-venv312/bin/python -m pip install -r requirements.txt
/tmp/mpaz-venv312/bin/python herramientas/vista_previa_auditoria.py
```

Abrir http://127.0.0.1:8765. El script usa el fixture de pruebas, crea estructura y datos temporales, y fuerza cookie sin Secure únicamente en esa vista HTTP local. No ejecuta migraciones sobre archivos existentes ni utiliza el servidor escolar.

Cuentas ficticias: `demo1` (Administración), `demo2` (Dirección), `profe1`/`profe2` (docentes de cursos distintos). La contraseña ficticia común está definida como `PASSWORD` en `tests/test_auditoria.py`. No introducir contraseñas institucionales. Al finalizar, Ctrl+C; el fixture cierra conexiones y elimina solo su directorio temporal.

## Automatización Chromium disponible

Archivo: `tests/navegador_paso65.py`. Este script levanta Flask con el fixture temporal de `tests/test_sesiones_docentes.py`, inicia Chromium en modo headless y usa exclusivamente cuentas y datos ficticios. No utiliza la base del servidor escolar ni la URL de producción.

Requisitos:

- Python 3.12 y dependencias de `requirements.txt` instaladas en `.venv`.
- Chromium disponible en `/usr/bin/chromium`.
- `chromedriver` disponible en PATH y compatible con Chromium.
- Puerto local 9515 libre.
- Carpeta de salida nueva para las capturas.

Ejecución desde la raíz del repositorio:

```bash
mkdir -p /tmp/mpaz-capturas-sesiones
.venv/bin/python tests/navegador_paso65.py /tmp/mpaz-capturas-sesiones
```

El recorrido automatizado comprueba, entre otros puntos, el inicio de sesión docente, selección de asignación, creación/recuperación de borrador, pendientes, reintento tras fallo de red, guardado de marcas, confirmación, consulta administrativa, filtros, detalle sin nombres de estudiantes, respuesta 503, expiración de sesión y acceso de un segundo profesor a sus propias asignaciones. Al final compara la tabla RFID `asistencias` con su contenido inicial para verificar que el flujo de aula no la haya modificado.

El script está configurado para escritorio (ventana 1440×1100). **No sustituye** las pruebas manuales de tablet/móvil, teclado, foco, contraste ni lector de pantalla. La existencia del archivo tampoco acredita que se haya ejecutado: conservar la salida de consola y las capturas, registrar navegador/versión y fecha, y solo entonces marcar los puntos correspondientes.

## Matriz manual

Repetir con escritorio 1440×900, tablet 768×1024 y móvil 390×844. Registrar navegador/versión, tamaño, resultado y captura ficticia cuando corresponda. No marcar aprobado sin ejecutar.

1. Portada y login: logo, azul/dorado/blanco, etiquetas y foco visibles. Credenciales incorrectas muestran error legible; 429 informa espera y no obliga a recargar sin contexto.
2. Administración: login demo1, directorio, ficha, tarjetas, tótems y tablas vacías/con datos. Formularios conservan valores ante error; mensajes explican éxito/fallo. Verificar filtros y descarga CSV ficticia.
3. Docencia: login profe1, curso 1A, creación/verificación/confirmación de clase. Curso 2A y sesión de profe2 deben ser rechazados por API, incluso con identificadores cambiados.
4. Seguimiento: abrir caso ficticio desde docencia y gestionarlo con demo1; comprobar mensajes, contacto, estado e historial. demo2 puede consultar/responder/cambiar estado, pero no registrar contacto ni abrir panel administrativo.
5. Preferencias en cada portal: claro/oscuro, compacto, texto ampliado y reducción de movimiento. Recargar y cambiar de módulo: preferencias deben persistir en el mismo navegador. Sin localStorage, la visita sigue funcionando.
6. Teclado: Tab/Shift+Tab/Enter/Espacio/Escape; orden lógico, foco visible y menús cerrables. Formularios y tablas accesibles sin ratón.
7. Móvil: no texto recortado ni controles superpuestos; tablas con desplazamiento utilizable, botones alcanzables y mensajes legibles. Comprobar contraste visual y medirlo con herramienta adecuada.
8. Fecha/hora: con navegador/sistema en UTC y otra zona, valores por defecto siguen America/Santiago. No alterar fechas de registros existentes.
9. Sesión: logout en cada rol y recarga de página protegida; no debe volver a mostrar datos desde caché. Tras inactividad/expiración debe pedir login con mensaje comprensible. Nunca utilizar cookies de producción para esta comprobación.
10. XSS ficticio: campos/observaciones que contengan `<img src=x onerror=alert(1)>` se muestran como texto, sin ejecutar. No hacerlo sobre datos reales.

La escritura de calendario está deshabilitada por defecto incluso en la vista. Para ejercitarla en esta base ficticia, reiniciar la vista con `MPAZ_CALENDARIO_ESCRITURA_HABILITADA=si`; no copiar ese ajuste a producción. La prueba API automatizada ya comprueba habilitación, CSRF y actor, pero no la presentación visual.
