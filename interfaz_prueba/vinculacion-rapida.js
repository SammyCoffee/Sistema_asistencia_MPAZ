
/*
 * MPAZ RFID - Vinculación rápida
 *
 * Reutiliza el formulario existente.
 * No realiza operaciones POST automáticamente.
 */

(function () {
    "use strict";

    const formulario = document.getElementById(
        "formulario-vinculacion"
    );

    const selectAlumno = document.getElementById(
        "vinculacion-estudiante"
    );

    const selectTarjeta = document.getElementById(
        "vinculacion-tarjeta"
    );

    const mensaje = document.getElementById(
        "mensaje-vinculacion"
    );

    if (
        !formulario ||
        !selectAlumno ||
        !selectTarjeta ||
        !mensaje
    ) {
        console.error(
            "MPAZ: No se encontró el formulario de vinculación."
        );
        return;
    }

    function existeOpcion(select, valor) {
        return Array.from(select.options).some(function (opcion) {
            return opcion.value === valor;
        });
    }

    window.mpazAbrirVinculacionRapida = async function (seleccion) {

        const alumnoId = seleccion?.alumnoId;
        const uid = seleccion?.uid;

        if (!alumnoId && !uid) {
            return;
        }

        // Cambiar a la pantalla de Vinculación.
        window.location.hash = "#vinculacion";

        // Limpiar cualquier selección anterior.
        formulario.reset();

        mensaje.textContent =
            "Preparando vinculación RFID...";

        try {
            // Actualizar estudiantes y tarjetas disponibles
            // antes de aplicar la preselección.
            await cargarOpcionesVinculacion();

            if (alumnoId) {

                const valor = String(alumnoId);

                if (!existeOpcion(selectAlumno, valor)) {
                    mensaje.textContent =
                        "El estudiante no está habilitado para " +
                        "recibir otra tarjeta RFID. Comprueba su estado.";
                    return;
                }

                selectAlumno.value = valor;
                selectAlumno.dispatchEvent(
                    new Event("change", {bubbles: true})
                );

                mensaje.textContent =
                    "Estudiante seleccionado. " +
                    "Elige una tarjeta RFID disponible y confirma.";

                selectTarjeta.focus();

            } else {

                const valor = String(uid).trim().toUpperCase();

                if (!existeOpcion(selectTarjeta, valor)) {
                    mensaje.textContent =
                        "La tarjeta ya no está disponible " +
                        "para vinculación.";
                    return;
                }

                selectTarjeta.value = valor;
                selectTarjeta.dispatchEvent(
                    new Event("change", {bubbles: true})
                );

                mensaje.textContent =
                    "Tarjeta RFID seleccionada. " +
                    "Elige al estudiante y confirma.";

                selectAlumno.focus();
            }

        } catch (error) {

            console.error(
                "MPAZ: Error en vinculación rápida:",
                error
            );

            mensaje.textContent =
                "No fue posible preparar la vinculación.";
        }
    };
})();
