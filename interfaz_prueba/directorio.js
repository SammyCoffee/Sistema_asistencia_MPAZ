
/* Directorio general de estudiantes MPAZ */

(function () {
    "use strict";

    const buscar = document.getElementById("mpaz-directorio-buscar");
    const curso = document.getElementById("mpaz-directorio-curso");
    const estado = document.getElementById("mpaz-directorio-estado");
    const rfid = document.getElementById("mpaz-directorio-rfid");
    const filas = document.getElementById("mpaz-directorio-filas");
    const total = document.getElementById("mpaz-directorio-total");
    const paginaTexto = document.getElementById("mpaz-directorio-pagina");
    const mensaje = document.getElementById("mpaz-directorio-mensaje");
    const anterior = document.getElementById("mpaz-directorio-anterior");
    const siguiente = document.getElementById("mpaz-directorio-siguiente");

    if (!filas) return;

    let alumnos = [];
    let pagina = 1;
    const porPagina = 10;

    const comparador = new Intl.Collator("es-CL", {
        numeric: true,
        sensitivity: "base"
    });

    function crearCelda(fila, valor) {
        const td = document.createElement("td");
        td.textContent = String(valor ?? "-");
        fila.appendChild(td);
        return td;
    }

    function crearEstado(fila, valor) {
        const td = document.createElement("td");
        const etiqueta = document.createElement("span");
        const texto = valor || "Sin tarjeta";

        etiqueta.textContent = texto;
        etiqueta.className = "mpaz-estado " +
            (valor || "sin-tarjeta").toLowerCase();

        td.appendChild(etiqueta);
        fila.appendChild(td);
    }

    function mostrar() {
        const texto = buscar.value.trim().toLocaleLowerCase("es-CL");

        const filtrados = alumnos.filter(function (a) {
            const nombre = String(a.nombre || "").toLocaleLowerCase("es-CL");
            const rut = String(a.rut || "").toLocaleLowerCase("es-CL");

            if (texto && !nombre.includes(texto) && !rut.includes(texto)) {
                return false;
            }

            if (curso.value && a.curso !== curso.value) return false;

            if (estado.value && a.estado_alumno !== estado.value) {
                return false;
            }

            if (rfid.value === "sin") return !a.uid;

            if (rfid.value && a.estado_tarjeta !== rfid.value) {
                return false;
            }

            return true;
        });

        const paginas = Math.max(1, Math.ceil(filtrados.length / porPagina));
        pagina = Math.min(pagina, paginas);

        const inicio = (pagina - 1) * porPagina;
        const visibles = filtrados.slice(inicio, inicio + porPagina);

        filas.replaceChildren();
        total.textContent = filtrados.length;
        paginaTexto.textContent = "Página " + pagina + " de " + paginas;

        anterior.disabled = pagina <= 1;
        siguiente.disabled = pagina >= paginas;

        if (!visibles.length) {
            const tr = document.createElement("tr");
            const td = crearCelda(tr, "No hay estudiantes para estos filtros.");
            td.colSpan = 5;
            filas.appendChild(tr);
            return;
        }

        visibles.forEach(function (alumno) {
            const tr = document.createElement("tr");

            crearCelda(tr, alumno.nombre);
            crearCelda(tr, alumno.curso);
            crearEstado(tr, alumno.estado_alumno);
            crearEstado(tr, alumno.uid ? alumno.estado_tarjeta : null);

            const td = document.createElement("td");
            const boton = document.createElement("button");

            boton.type = "button";
            boton.textContent = "Ver ficha";

            boton.addEventListener("click", function () {
                // Reutilizar la ficha administrativa existente.
                alumnosEncontrados = alumnos;
                // MPAZ-FICHA-642
                resultadoEstudiante.hidden = false;
                mostrarFichaEstudiante(alumno);

                document.getElementById("resultado-estudiante")
                    .scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });
            });

            td.appendChild(boton);

            // Vinculación rápida para estudiantes activos
            // que todavía no tienen una tarjeta RFID activa.
            if (
                alumno.estado_alumno === "activo" &&
                alumno.estado_tarjeta !== "activa"
            ) {
                const botonVincular = document.createElement("button");

                botonVincular.type = "button";
                botonVincular.className = "mpaz-vinculacion-rapida";

                botonVincular.textContent = alumno.uid
                    ? "Asignar reemplazo"
                    : "Asignar RFID";

                botonVincular.addEventListener("click", function () {
                    if (
                        typeof window.mpazAbrirVinculacionRapida
                        === "function"
                    ) {
                        window.mpazAbrirVinculacionRapida({
                            alumnoId: alumno.id
                        });
                    }
                });

                td.appendChild(botonVincular);
            }

            tr.appendChild(td);
            filas.appendChild(tr);
        });
    }

    async function cargarDirectorio() {
        try {
            const respuesta = await fetch("/alumnos", {
                credentials: "same-origin",
                cache: "no-store"
            });

            if (!respuesta.ok) {
                throw new Error("HTTP " + respuesta.status);
            }

            const datos = await respuesta.json();

            if (!Array.isArray(datos.alumnos)) {
                throw new Error("Respuesta de estudiantes inválida");
            }

            alumnos = datos.alumnos.slice().sort(function (a, b) {
                return comparador.compare(a.nombre || "", b.nombre || "");
            });

            const cursoSeleccionado = curso.value;

            const cursos = [...new Set(
                alumnos.map(a => a.curso).filter(Boolean)
            )].sort(comparador.compare);

            curso.replaceChildren(new Option("Todos", ""));

            cursos.forEach(function (nombreCurso) {
                curso.add(new Option(nombreCurso, nombreCurso));
            });

            curso.value = cursos.includes(cursoSeleccionado)
                ? cursoSeleccionado : "";

            mensaje.textContent = "";
            mostrar();

        } catch (error) {
            console.error("Directorio MPAZ:", error);
            mensaje.textContent =
                "No fue posible cargar el directorio de estudiantes.";
        }
    }

    [buscar, curso, estado, rfid].forEach(function (elemento) {
        elemento.addEventListener("input", function () {
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

    window.actualizarDirectorioMPAZ = cargarDirectorio;
    cargarDirectorio();
})();
