
/* INVENTARIO RFID MPAZ */

(function () {
    "use strict";

    const tabla = document.getElementById("tabla-tarjetas");

    const buscar = document.getElementById("mpaz-rfid-buscar");
    const estado = document.getElementById("mpaz-rfid-estado");
    const curso = document.getElementById("mpaz-rfid-curso");

    const anterior = document.getElementById("mpaz-rfid-anterior");
    const siguiente = document.getElementById("mpaz-rfid-siguiente");
    const paginaTexto = document.getElementById("mpaz-rfid-pagina");
    const mensaje = document.getElementById("mpaz-rfid-mensaje");

    if (!tabla || !buscar || !estado || !curso) {
        return;
    }

    let tarjetas = [];
    let pagina = 1;

    const porPagina = 10;

    function actualizarResumen() {
        const cantidades = {
            activa: 0,
            disponible: 0,
            bloqueada: 0,
            extraviada: 0
        };

        tarjetas.forEach(function (tarjeta) {
            if (Object.prototype.hasOwnProperty.call(
                cantidades, tarjeta.estado
            )) {
                cantidades[tarjeta.estado]++;
            }
        });

        const valores = {
            "mpaz-rfid-total": tarjetas.length,
            "mpaz-rfid-activas": cantidades.activa,
            "mpaz-rfid-disponibles": cantidades.disponible,
            "mpaz-rfid-bloqueadas": cantidades.bloqueada,
            "mpaz-rfid-extraviadas": cantidades.extraviada
        };

        Object.entries(valores).forEach(function ([id, valor]) {
            document.getElementById(id).textContent = valor;
        });
    }

    function actualizarEstadosVisuales() {
        const filas = Array.from(tabla.querySelectorAll("tr"));

        tarjetas.forEach(function (tarjeta, indice) {
            const fila = filas[indice];

            if (!fila || fila.cells.length < 2) {
                return;
            }

            const celda = fila.cells[1];

            const indicador = document.createElement("span");
            indicador.className = "mpaz-estado-rfid";

            if ([
                "activa",
                "disponible",
                "bloqueada",
                "extraviada"
            ].includes(tarjeta.estado)) {
                indicador.classList.add(tarjeta.estado);
            }

            indicador.textContent = tarjeta.estado || "Sin estado";
            celda.replaceChildren(indicador);
        });
    }

    function mostrar() {
        const texto = buscar.value.trim().toLocaleLowerCase("es-CL");

        const filas = Array.from(tabla.querySelectorAll("tr"));

        const indices = tarjetas.map(function (tarjeta, indice) {
            const uid = String(tarjeta.uid || "")
                .toLocaleLowerCase("es-CL");

            const alumno = String(tarjeta.alumno || "")
                .toLocaleLowerCase("es-CL");

            const coincideTexto = !texto
                || uid.includes(texto)
                || alumno.includes(texto);

            const coincideEstado = !estado.value
                || tarjeta.estado === estado.value;

            const coincideCurso = !curso.value
                || tarjeta.curso === curso.value;

            return coincideTexto && coincideEstado && coincideCurso
                ? indice
                : -1;
        }).filter(indice => indice !== -1);

        const totalPaginas = Math.max(
            1,
            Math.ceil(indices.length / porPagina)
        );

        pagina = Math.min(pagina, totalPaginas);

        const desde = (pagina - 1) * porPagina;

        const visibles = new Set(
            indices.slice(desde, desde + porPagina)
        );

        filas.forEach(function (fila, indice) {
            if (tarjetas.length > 0) {
                fila.hidden = !visibles.has(indice);
            }
        });

        paginaTexto.textContent =
            "Página " + pagina + " de " + totalPaginas
            + " · " + indices.length + " tarjetas";

        anterior.disabled = pagina === 1;
        siguiente.disabled = pagina === totalPaginas;

        if (tarjetas.length > 0 && indices.length === 0) {
            mensaje.textContent =
                "No se encontraron tarjetas con estos filtros.";
        } else {
            mensaje.textContent = "";
        }
    }


    // MPAZ-ACCIONES-633
    // Acciones administrativas sobre las tarjetas RFID.

    function instalarAccionesTarjetas() {

        const filas = Array.from(
            tabla.querySelectorAll("tr")
        );

        tarjetas.forEach(function (tarjeta, indice) {

            const fila = filas[indice];

            if (!fila || fila.cells.length !== 6) {
                return;
            }

            const celdaAcciones = fila.cells[5];

            // Limpiar botones agregados previamente.
            celdaAcciones.querySelectorAll(
                ".mpaz-accion-rfid"
            ).forEach(function (boton) {
                boton.remove();
            });

            let accion = null;
            let texto = null;

            if (tarjeta.estado === "activa") {
                accion = "bloquear";
                texto = "Bloquear";
            }

            if (tarjeta.estado === "bloqueada") {
                accion = "desbloquear";
                texto = "Desbloquear";
            }

            if (tarjeta.estado === "disponible") {

                celdaAcciones.textContent = "";

                const botonVincular = document.createElement("button");

                botonVincular.type = "button";
                botonVincular.className = "mpaz-vinculacion-rapida";
                botonVincular.textContent = "Vincular";

                botonVincular.addEventListener("click", function () {
                    if (
                        typeof window.mpazAbrirVinculacionRapida
                        === "function"
                    ) {
                        window.mpazAbrirVinculacionRapida({
                            uid: tarjeta.uid
                        });
                    }
                });

                celdaAcciones.appendChild(botonVincular);
                return;
            }

            if (!accion) {
                return;
            }

            if (celdaAcciones.textContent.trim() === "-") {
                celdaAcciones.textContent = "";
            }

            const boton = document.createElement("button");

            boton.type = "button";
            boton.textContent = texto;

            boton.className =
                "mpaz-accion-rfid mpaz-accion-" + accion;

            boton.dataset.uid = tarjeta.uid;
            boton.dataset.accion = accion;

            celdaAcciones.appendChild(boton);
        });
    }

    tabla.addEventListener("click", async function (evento) {

        const boton = evento.target.closest(
            ".mpaz-accion-rfid"
        );

        if (!boton || !tabla.contains(boton)) {
            return;
        }

        if (boton.disabled) {
            return;
        }

        const uid = boton.dataset.uid;
        const accion = boton.dataset.accion;

        if (
            !uid ||
            !["bloquear", "desbloquear"].includes(accion)
        ) {
            return;
        }

        const tarjetaActual = tarjetas.find(
            tarjeta => tarjeta.uid === uid
        );

        const estadoRequerido = accion === "bloquear"
            ? "activa"
            : "bloqueada";

        if (
            !tarjetaActual ||
            tarjetaActual.estado !== estadoRequerido
        ) {
            alert(
                "El estado de la tarjeta cambió. " +
                "Actualiza el inventario."
            );
            return;
        }

        const verbo = accion === "bloquear"
            ? "bloquear"
            : "desbloquear";

        if (!confirm(
            "¿Seguro que deseas " + verbo +
            " la tarjeta " + uid + "?"
        )) {
            return;
        }

        const endpoint = accion === "bloquear"
            ? "/panel/tarjetas/bloquear"
            : "/panel/tarjetas/desbloquear";

        const resultadoEsperado = accion === "bloquear"
            ? "bloqueada"
            : "activada";

        boton.disabled = true;

        try {

            const respuesta = await fetch(endpoint, {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({uid})
            });

            const datos = await respuesta.json();

            if (
                !respuesta.ok ||
                datos.resultado !== resultadoEsperado
            ) {

                if (datos.resultado === "alumno_no_autorizado") {
                    alert(
                        "No se puede desbloquear la tarjeta " +
                        "porque el estudiante asociado no está activo."
                    );
                } else {
                    alert(
                        datos.mensaje ||
                        "No se pudo completar la operación RFID."
                    );
                }

                return;
            }

            await cargarTarjetas();
            await cargarOpcionesVinculacion();
            await cargarResumenEstudiantes();

            alert(
                accion === "bloquear"
                    ? "Tarjeta RFID bloqueada correctamente."
                    : "Tarjeta RFID desbloqueada correctamente."
            );

        } catch (error) {

            console.error(
                "Error administrativo RFID:",
                error
            );

            alert(
                "No fue posible completar la operación. " +
                "Comprueba la conexión con el servidor."
            );

        } finally {
            boton.disabled = false;
        }
    });

    function actualizarInventario(registros) {
        tarjetas = Array.isArray(registros)
            ? registros.slice()
            : [];

        const seleccionado = curso.value;

        const cursos = [...new Set(
            tarjetas.map(t => t.curso).filter(Boolean)
        )].sort(new Intl.Collator("es-CL", {
            numeric: true
        }).compare);

        curso.replaceChildren(new Option("Todos", ""));

        cursos.forEach(function (nombreCurso) {
            curso.add(new Option(nombreCurso, nombreCurso));
        });

        curso.value = cursos.includes(seleccionado)
            ? seleccionado
            : "";

        actualizarResumen();
        actualizarEstadosVisuales();
        instalarAccionesTarjetas();
        mostrar();
    }

    [buscar, estado, curso].forEach(function (control) {
        control.addEventListener("input", function () {
            pagina = 1;
            mostrar();
        });
    });

    anterior.addEventListener("click", function () {
        if (pagina > 1) {
            pagina--;
            mostrar();
        }
    });

    siguiente.addEventListener("click", function () {
        pagina++;
        mostrar();
    });

    window.actualizarInventarioMPAZ = actualizarInventario;
})();
