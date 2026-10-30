
/* MPAZ-VINCULACION-640 */

(function () {
    "use strict";

    const buscar = document.getElementById(
        "mpaz-buscar-alumno-vincular"
    );

    const resultados = document.getElementById(
        "mpaz-resultados-vinculacion"
    );

    const alumno = document.getElementById(
        "vinculacion-estudiante"
    );

    const tarjeta = document.getElementById(
        "vinculacion-tarjeta"
    );

    const resumen = document.getElementById(
        "mpaz-resumen-vinculacion"
    );

    if (!buscar || !resultados || !alumno || !tarjeta || !resumen) {
        return;
    }

    function normalizar(texto) {
        return String(texto || "")
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .toLocaleLowerCase("es-CL")
            .trim();
    }

    function actualizarResumen() {
        const opcionAlumno = alumno.selectedOptions[0];
        const opcionTarjeta = tarjeta.selectedOptions[0];

        const nombre = alumno.value && opcionAlumno
            ? opcionAlumno.textContent.trim()
            : null;

        const uid = tarjeta.value && opcionTarjeta
            ? opcionTarjeta.textContent.trim()
            : null;

        if (nombre && uid) {
            resumen.textContent =
                "Estudiante: " + nombre +
                " | Tarjeta RFID: " + uid +
                ". Revisa los datos antes de confirmar.";

        } else if (nombre) {
            resumen.textContent =
                "Estudiante seleccionado: " + nombre +
                ". Falta elegir una tarjeta disponible.";

        } else if (uid) {
            resumen.textContent =
                "Tarjeta seleccionada: " + uid +
                ". Falta elegir un estudiante.";

        } else {
            resumen.textContent =
                "Selecciona un estudiante y una tarjeta RFID.";
        }
    }

    function mostrarCoincidencias() {
        const texto = normalizar(buscar.value);

        resultados.replaceChildren();

        if (texto.length < 2) {
            resultados.hidden = true;
            return;
        }

        const coincidencias = Array.from(alumno.options)
            .filter(function (opcion) {
                return opcion.value &&
                    normalizar(opcion.textContent).includes(texto);
            })
            .slice(0, 8);

        if (!coincidencias.length) {
            const aviso = document.createElement("p");
            aviso.textContent =
                "No se encontraron estudiantes habilitados.";
            resultados.appendChild(aviso);
        }

        coincidencias.forEach(function (opcion) {
            const boton = document.createElement("button");

            boton.type = "button";
            boton.textContent = opcion.textContent.trim();

            boton.addEventListener("click", function () {
                alumno.value = opcion.value;

                alumno.dispatchEvent(
                    new Event("change", {bubbles: true})
                );

                buscar.value = opcion.textContent.trim();
                resultados.hidden = true;
                tarjeta.focus();
            });

            resultados.appendChild(boton);
        });

        resultados.hidden = false;
    }

    buscar.addEventListener(
        "input",
        mostrarCoincidencias
    );

    alumno.addEventListener(
        "change",
        actualizarResumen
    );

    tarjeta.addEventListener(
        "change",
        actualizarResumen
    );

    // El formulario original actualiza sus opciones desde
    // la API. Reflejar cambios sin interferir con ellas.
    const observador = new MutationObserver(function () {
        actualizarResumen();

        if (!resultados.hidden) {
            mostrarCoincidencias();
        }
    });

    [alumno, tarjeta].forEach(function (select) {
        observador.observe(select, {
            childList: true,
            subtree: true
        });
    });

    actualizarResumen();
})();
