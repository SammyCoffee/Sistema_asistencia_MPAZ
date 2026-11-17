# Recomendación de protección de históricos

Estado: revisión documental local. No se modificó, sobrescribió ni eliminó ningún histórico; sin servidor escolar ni lectura de bases de datos.

## API_01_ESP32_Envio_Lectura_HTTP200.png

La inspección privada confirma que el UID visible (alias UID-H1, valor no reproducido en este informe) coincide con F03 de la práctica. La fuente presenta esa lectura como una tarjeta de prueba. F18 muestra visualmente el mismo identificador asociado a un alumno rotulado de prueba y una tarjeta «bloqueada». Ese estado es una captura histórica y no prueba el bloqueo efectivo actual ni el rechazo por API. No se certifica que el UID sea ficticio, que no se haya reutilizado, que siga bloqueado o que esté fuera del inventario operativo.

La búsqueda literal en texto Git rastreado de los dos checkouts no encontró una referencia que permita verificar su vigencia. No se consultaron archivos SQLite, cuentas del servidor ni registros de producción. La clasificación sustentada es: **UID reportado en prueba física parcial; estado actual desconocido**. La comparación F18 es visual; OCR de esa ficha no se usa como prueba concluyente.

**Riesgo condicional si la tarjeta está activa:** el identificador seguiría disponible en el archivo y su historia pública. Si alguien reproduce un identificador aceptado por el lector/sistema, podría originar lecturas asociadas a esa tarjeta, sujeto a los demás controles. No se ha probado ni afirmado una suplantación. Conocer el UID no acredita acceso a la clave API ni a una sesión: la ruta de lectura también valida clave del tótem y estados, según el código de consulta. La captura no permite certificar la seguridad de toda la cadena.

Recomendación específica:

1. El responsable autorizado debe cotejar privadamente UID-H1 con el inventario vigente y confirmar asignación, uso y bloqueo efectivo. Este documento no reproduce el valor; se consulta el original privado.
2. Si está activa o vinculada a una persona, priorizar su bloqueo/desvinculación y, si procede, emitir otra tarjeta con el procedimiento institucional autorizado. No se ejecutó ninguna acción de ese tipo en esta tarea.
3. En una futura carga autorizada, usar una variante sanitizada para la vista pública actual de API_01 y revisar sus reproducciones en documentos antiguos. Una copia sanitizada no borra la versión previamente publicada ni sus objetos Git. No declarar saneado el historial.
4. Mantener los originales como respaldo privado y acordar por separado cualquier tratamiento de visibilidad/historia que corresponda. No se propone un reset ni una reescritura automática.

## HARDWARE_01_ESP32_PN532_Montaje.jpeg

Es duplicado binario de F02. Se observa una anotación manuscrita y trazos tenues sobre la tarjeta, además de una etiqueta identificadora de un componente del fondo. El contexto es un montaje de prueba; no se pudo leer de forma fiable un UID completo de la anotación ni vincularlo con certeza a UID-H1. Tampoco se verificó el uso actual de esa tarjeta. No debe clasificarse como ficticia o inactiva por la sola fotografía.

Si la anotación corresponde a una tarjeta activa, existe el mismo riesgo condicional de exposición de su identificador. El responsable deberá identificar la tarjeta desde el original privado antes de decidir si procede bloquearla o sustituirla.

Se creó y verificó una copia sanitizada F02 en la revisión privada: oculta anotaciones/etiqueta y conserva los demás píxeles. Puede servir como candidata para proteger una vista pública futura de HARDWARE_01, previa autorización, sin sobrescribir ahora el histórico. No se añade a esta carga por duplicación: F01 ya ilustra el montaje sin esa anotación.

## Conclusión operativa

No se confirmó exposición de una clave API ni uso actual de las tarjetas; tampoco se puede certificar riesgo nulo. La nueva preparación evita añadir los identificadores, pero no elimina la exposición histórica. Se puede revisar y autorizar el siguiente commit estrictamente documental con copias sanitizadas; mantener abierta la comprobación privada de vigencia, prioritariamente antes de uso escolar de esas tarjetas. No se realizaron commit, push ni operaciones sobre tarjetas o bases.
