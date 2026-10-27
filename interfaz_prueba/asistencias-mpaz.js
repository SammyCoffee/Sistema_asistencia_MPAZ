
/* MPAZ-ASISTENCIAS-645 */

(function () {
    "use strict";

    const cuerpo = document.getElementById(
        "cuerpo-asistencias"
    );

    const buscar = document.getElementById(
        "mpaz-asis-buscar"
    );

    const fecha = document.getElementById(
        "mpaz-asis-fecha"
    );

    const curso = document.getElementById(
        "mpaz-asis-curso"
    );

    const limpiar = document.getElementById(
        "mpaz-asis-limpiar"
    );

    const anterior = document.getElementById(
        "mpaz-asis-anterior"
    );

    const siguiente = document.getElementById(
        "mpaz-asis-siguiente"
    );

    const paginaTexto = document.getElementById(
        "mpaz-asis-pagina"
    );

    const mensaje = document.getElementById(
        "mpaz-asis-mensaje"
    );

    if (!cuerpo || !buscar || !fecha || !curso) {
        return;
    }

    let pagina = 1;
    const porPagina = 10;

    function normalizar(texto) {
        return String(texto || "")
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .toLocaleLowerCase("es-CL")
            .trim();
    }

    function registros() {
        return Array.from(cuerpo.querySelectorAll("tr"))
            .filter(function (fila) {
                return fila.cells.length === 6;
            })
            .map(function (fila) {
                const celdas = fila.cells;

                return {
                    fila: fila,
                    fecha: celdas[0].textContent.trim(),
                    estudiante: celdas[1].textContent.trim(),
                    curso: celdas[2].textContent.trim(),
                    entrada: celdas[3].textContent.trim(),
                    salida: celdas[4].textContent.trim(),
                    tipo: celdas[5].textContent.trim()
                };
            });
    }

    function actualizarCursos(datos) {
        const seleccionado = curso.value;

        const cursos = [...new Set(
            datos.map(d => d.curso).filter(Boolean)
        )].sort(
            new Intl.Collator("es-CL", {numeric: true}).compare
        );

        curso.replaceChildren(
            new Option("Todos los cursos", "")
        );

        cursos.forEach(function (nombre) {
            curso.add(new Option(nombre, nombre));
        });

        if (cursos.includes(seleccionado)) {
            curso.value = seleccionado;
        }
    }

    function actualizarIndicadores(datos) {
        const totalEntradas = datos.filter(
            d => d.entrada && d.entrada !== "--"
        ).length;

        const salidasTotem = datos.filter(
            d => d.tipo === "Tótem"
        ).length;

        const salidasAutomaticas = datos.filter(
            d => d.tipo === "Automática"
        ).length;

        const salidasPendientes = datos.filter(
            d => d.tipo === "Pendiente"
        ).length;

        const valores = {
            "mpaz-asis-ingresos": totalEntradas,
            "mpaz-asis-salidas": salidasTotem,
            "mpaz-asis-automaticas": salidasAutomaticas,
            "mpaz-asis-pendientes": salidasPendientes
        };

        Object.entries(valores).forEach(function ([id, valor]) {
            document.getElementById(id).textContent = valor;
        });
    }

    function mostrar() {
        const datos = registros();

        const texto = normalizar(buscar.value);

        const filtrados = datos.filter(function (d) {
            if (texto && !normalizar(d.estudiante).includes(texto)) {
                return false;
            }

            if (fecha.value && d.fecha !== fecha.value) {
                return false;
            }

            if (curso.value && d.curso !== curso.value) {
                return false;
            }

            return true;
        });

        actualizarIndicadores(filtrados);

        const totalPaginas = Math.max(
            1,
            Math.ceil(filtrados.length / porPagina)
        );

        pagina = Math.min(pagina, totalPaginas);

        const inicio = (pagina - 1) * porPagina;

        const visibles = new Set(
            filtrados.slice(inicio, inicio + porPagina)
                .map(d => d.fila)
        );

        datos.forEach(function (d) {
            d.fila.hidden = !visibles.has(d.fila);
        });

        paginaTexto.textContent =
            "Página " + pagina + " de " + totalPaginas +
            " · " + filtrados.length + " registros";

        anterior.disabled = pagina <= 1;
        siguiente.disabled = pagina >= totalPaginas;

        mensaje.textContent = filtrados.length
            ? ""
            : "No se encontraron registros de asistencia " +
              "para los filtros seleccionados.";
    }

    function actualizar() {
        actualizarCursos(registros());
        mostrar();
    }

    [buscar, fecha, curso].forEach(function (elemento) {
        elemento.addEventListener("input", function () {
            pagina = 1;
            mostrar();
        });
    });

    limpiar.addEventListener("click", function () {
        buscar.value = "";
        fecha.value = "";
        curso.value = "";
        pagina = 1;
        mostrar();
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

    // El panel original actualiza las asistencias
    // periódicamente. Reaplicar filtros y paginación
    // después de esas actualizaciones.
    const observador = new MutationObserver(actualizar);

    observador.observe(cuerpo, {
        childList: true
    });

    actualizar();
})();
