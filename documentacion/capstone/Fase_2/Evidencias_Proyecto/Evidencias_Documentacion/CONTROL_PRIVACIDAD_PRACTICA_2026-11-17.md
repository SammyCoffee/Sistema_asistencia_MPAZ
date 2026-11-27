# Control de privacidad de evidencias de práctica

## Autorización y resultado

El usuario autorizó máscaras opacas con Pillow o ImageMagick y prohibió edición generativa. Se utilizó Pillow: ocho copias sanitizadas, cuatro seleccionadas para la preparación documental y cuatro conservadas solo en revisión privada. Los archivos originales, el ZIP y el DOCX de práctica permanecen intactos y no se añaden a Git.

Las 29 figuras fueron inspeccionadas individualmente. Se mantiene la matriz de 18 evidencias y 29 figuras. Ya no hay una elección de método pendiente: la autorización está recibida y aplicada. El commit y la publicación siguen sin autorización.

## Prueba de ocultación

- Salida PNG aplanada y sin metadatos heredados, EXIF, miniaturas, capas o nombres identificadores. Los nombres usan solamente F02/F03/etc. y la fecha.
- Rectángulos negros con opacidad total. No se usa desenfoque, una máscara de Word ni reconstrucción generativa de texto.
- Comparación exacta entre el original decodificado y la salida: cero píxeles cambiados fuera de la unión de rectángulos. En JPEG la referencia es la imagen decodificada, conservada sin una nueva compresión con pérdida.
- Todas las zonas ocultas contienen solo negro; si hay alfa, es 255. El PNG publicado no conserva el contenido sustituido en canales ocultos. La revisión visual se hizo sobre las salidas guardadas, no sobre una capa de previsualización.
- HTTP 200, conteos antes/después, consultas SQL, fechas, horas, tipos de salida, «Sin tótem» y estados activo/inactivo/bloqueada se preservan. No se cambian resultados de pruebas.
- La ocultación protege la copia: no elimina datos ya disponibles en versiones históricas. Las ocho originales no sanitizadas están excluidas de nuevos archivos/medios Office.

## Ocho copias y selección

| Figura | Zonas ocultas | Destino |
|---|---|---|
| F02 | Anotaciones visibles y tenues de la tarjeta; etiqueta identificadora de componente del fondo. | Solo revisión privada; duplicado/redundante |
| F03 | UID, identificador del evento y valores identificadores del tótem/UID/evento en el JSON enviado. HTTP 200 y respuesta no sensible conservados. | [Incorporada](../Evidencias_Sistema_Aplicacion/Practica_2026-11-17/PRACTICA_F03_SANITIZADA_2026-11-17.png) |
| F04 | Usuario/host del prompt de terminal; consulta SQL, rutas públicas y resultado intactos. | Solo revisión privada; duplicado/redundante |
| F05 | Usuario/host del prompt de terminal; resultado y conteos intactos. | Solo revisión privada; duplicado/redundante |
| F11 | Valores de tótem/eventos por fila, remanente de campos personales ya ocultos y minimapa que reproduce esos datos. Fechas/horas/tipo de salida conservados. | [Incorporada](../Evidencias_Sistema_Aplicacion/Practica_2026-11-17/PRACTICA_F11_SANITIZADA_2026-11-17.png) |
| F18 | Valor UID de la ficha; nombre explícito de prueba y estado de tarjeta conservados. | Solo revisión privada; duplicado/redundante |
| F20 | Valor del identificador RFID de prueba; estado estudiante/tarjeta conservado. | [Incorporada](../Evidencias_Sistema_Aplicacion/Practica_2026-11-17/PRACTICA_F20_SANITIZADA_2026-11-17.png) |
| F21 | Valor del identificador RFID de prueba; estado estudiante/tarjeta conservado. | [Incorporada](../Evidencias_Sistema_Aplicacion/Practica_2026-11-17/PRACTICA_F21_SANITIZADA_2026-11-17.png) |

## Resto de figuras

F06/F07/F08/F09/F14/F22/F24/F26/F27/F28 permanecen como copias revisadas sin identificadores sensibles visibles o con anonimización ya hecha en la fuente. F01 reutiliza el recurso histórico revisado. F10/F12/F13/F15/F16/F17/F19/F23/F25/F29 no se añaden como archivos gráficos: son redundantes, equivalentes o no aportan una validación nueva. Las reproducciones docentes ya presentes en APT son demostraciones declaradas, sin UID visible.

Los originales API_01 y HARDWARE_01 permanecen intactos. La recomendación separada clasifica el UID de API_01 como reportado en una prueba y su estado actual como desconocido; F18 muestra «bloqueada» solo históricamente. La anotación de HARDWARE_01 no se vinculó de forma fiable a un UID completo. Si corresponden a tarjetas activas, existe riesgo condicional de suplantación de lecturas, sin demostrar que haya ocurrido.

No se accedió al servidor ni se leyeron/modificaron bases. La confirmación privada de estado vigente corresponde al responsable autorizado. No se confunde una tarjeta física de prueba con un identificador ficticio o permanentemente revocado.

[Registro técnico de máscaras y hashes](../../../REGISTRO_SANITIZACION_PRACTICA_2026-11-17.json) · [Recomendación de históricos](../../../RECOMENDACION_HISTORICOS_PRIVACIDAD_2026-11-17.md).
