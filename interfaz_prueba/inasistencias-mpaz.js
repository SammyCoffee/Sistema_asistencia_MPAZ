
/* MPAZ-INASISTENCIAS-648 */

(function () {
    "use strict";

    const cuerpo = document.getElementById(
        "tabla-inasistencias"
    );

    const buscar = document.getElementById(
        "mpaz-ina-buscar"
    );

    const curso = document.getElementById(
        "mpaz-ina-curso"
    );

    const estado = document.getElementById(
        "mpaz-ina-estado"
    );

    const anterior = document.getElementById(
        "mpaz-ina-anterior"
    );

    const siguiente = document.getElementById(
        "mpaz-ina-siguiente"
    );

    const paginaTexto = document.getElementById(
        "mpaz-ina-pagina"
    );

    const resumen = document.getElementById(
        "resumen-inasistencias"
    );

    const mensaje = document.getElementById(
        "mpaz-ina-mensaje"
    );

    if (!cuerpo || !buscar || !curso || !estado) {
        return;
    }

    let registros = [];
    let jornadas = 0;
    let pagina = 1;

    const porPagina = 10;

    function normalizar(texto) {
        return String(texto || "")
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .toLocaleLowerCase("es-CL")
            .trim();
    }

    function numeroSeguro(valor) {
        const numero = Number(valor);

        return Number.isFinite(numero)
            ? Math.max(0, Math.trunc(numero))
            : 0;
    }

    function clasificar(registro) {
        if (jornadas === 0) {
            return {
                codigo: "sin_datos",
                texto: "Sin fechas base"
            };
        }

        if (registro.ausencias === 0) {
            return {
                codigo: "completo",
                texto: "Con registros en todas las fechas"
            };
        }

        if (registro.ausencias >= jornadas) {
            return {
                codigo: "sin",
                texto: "Sin marcaciones"
            };
        }

        return {
            codigo: "parcial",
            texto: "Marcaciones parciales"
        };
    }

    function celda(fila, contenido) {
        const td = document.createElement("td");
        td.textContent = String(contenido ?? "-");
        fila.appendChild(td);
        return td;
    }

    function indicador(id, valor) {
        document.getElementById(id).textContent = valor;
    }

    function mostrar() {
        const texto = normalizar(buscar.value);

        const filtrados = registros.filter(function (registro) {
            if (
                texto &&
                !normalizar(registro.nombre).includes(texto)
            ) {
                return false;
            }

            if (curso.value && registro.curso !== curso.value) {
                return false;
            }

            if (
                estado.value &&
                clasificar(registro).codigo !== estado.value
            ) {
                return false;
            }

            return true;
        });

        const sinMarcaciones = filtrados.filter(function (r) {
            return jornadas > 0 && r.ausencias >= jornadas;
        }).length;

        const casosPorRevisar = filtrados.filter(function (r) {
            return jornadas > 0 && r.ausencias > 0;
        }).length;

        indicador("mpaz-ina-estudiantes", filtrados.length);
        indicador("mpaz-ina-jornadas", jornadas);
        indicador("mpaz-ina-sin-marcaciones", sinMarcaciones);
        indicador("mpaz-ina-revisar", casosPorRevisar);

        // El resumen principal también queda identificado
        // como una revisión preliminar, no como faltas oficiales.
        const alertaPrincipal = document.getElementById(
            "total-alertas-inasistencia"
        );

        if (alertaPrincipal) {
            alertaPrincipal.textContent = registros.filter(function (r) {
                return jornadas > 0 && r.ausencias > 0;
            }).length;
        }

        resumen.textContent =
            "Fechas base con registros RFID: " + jornadas;

        const paginas = Math.max(
            1,
            Math.ceil(filtrados.length / porPagina)
        );

        pagina = Math.min(pagina, paginas);

        const inicio = (pagina - 1) * porPagina;
        const visibles = filtrados.slice(
            inicio,
            inicio + porPagina
        );

        cuerpo.replaceChildren();

        if (visibles.length === 0) {
            const fila = document.createElement("tr");
            const td = celda(
                fila,
                "No hay estudiantes para estos filtros."
            );

            td.colSpan = 5;
            cuerpo.appendChild(fila);
        }

        visibles.forEach(function (registro) {
            const fila = document.createElement("tr");
            const situacion = clasificar(registro);

            celda(fila, registro.nombre);
            celda(fila, registro.curso);
            celda(fila, registro.ausencias);
            celda(fila, jornadas);

            const estadoCelda = document.createElement("td");
            const etiqueta = document.createElement("span");

            etiqueta.className =
                "mpaz-situacion " + situacion.codigo;

            etiqueta.textContent = situacion.texto;

            estadoCelda.appendChild(etiqueta);
            fila.appendChild(estadoCelda);

            cuerpo.appendChild(fila);
        });

        paginaTexto.textContent =
            "Página " + pagina + " de " + paginas +
            " · " + filtrados.length + " estudiantes";

        anterior.disabled = pagina <= 1;
        siguiente.disabled = pagina >= paginas;

        mensaje.textContent = jornadas === 0
            ? "No existen fechas base con registros RFID " +
              "para el período consultado."
            : "";
    }

    window.mpazRenderInasistencias = function (datos) {
        if (!Array.isArray(datos.inasistencias)) {
            mensaje.textContent =
                "La respuesta del servidor no es válida.";
            return;
        }

        const lista = datos.inasistencias;

        jornadas = lista.length
            ? numeroSeguro(lista[0].jornadas_periodo)
            : 0;

        registros = lista.map(function (alumno) {
            return {
                nombre: String(alumno.nombre || ""),
                curso: String(alumno.curso || ""),
                ausencias: Math.min(
                    jornadas,
                    numeroSeguro(alumno.inasistencias)
                )
            };
        });

        const cursoActual = curso.value;

        const cursos = [...new Set(
            registros.map(r => r.curso).filter(Boolean)
        )].sort(
            new Intl.Collator("es-CL", {numeric: true}).compare
        );

        curso.replaceChildren(
            new Option("Todos los cursos", "")
        );

        cursos.forEach(function (nombre) {
            curso.add(new Option(nombre, nombre));
        });

        if (cursos.includes(cursoActual)) {
            curso.value = cursoActual;
        }

        pagina = 1;
        mostrar();
    };

    [buscar, curso, estado].forEach(function (control) {
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

    // Inicializar desde la API existente.
    if (typeof cargarInasistencias === "function") {
        cargarInasistencias();
    }
})();
