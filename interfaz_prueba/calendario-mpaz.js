
/* MPAZ-CALENDARIO-6571 */

(function () {
    "use strict";

    const calendario = document.getElementById(
        "mpaz-cal-cuadricula"
    );

    if (!calendario) return;

    const titulo = document.getElementById("mpaz-cal-mes");
    const campoFecha = document.getElementById("mpaz-cal-fecha");
    const textoFecha = document.getElementById(
        "mpaz-cal-fecha-texto"
    );

    const selectorCurso = document.getElementById(
        "mpaz-cal-curso"
    );

    const selectorAlcance = document.getElementById(
        "mpaz-cal-alcance"
    );

    const cursos = [
        "PK", "K",
        "1A", "1B", "2A", "2B",
        "3A", "3B", "4A", "4B",
        "5A", "5B", "6A", "6B",
        "7A", "7B", "8A", "8B"
    ];

    cursos.forEach(function (curso) {
        selectorCurso.add(new Option(curso, curso));
        selectorAlcance.add(new Option(curso, curso));
    });

    // Integrar con el selector general del panel.
    document.querySelectorAll("select").forEach(function (control) {
        const opciones = Array.from(
            control.options,
            opcion => opcion.value
        );

        if (
            opciones.includes("reportes") &&
            !opciones.includes("calendario")
        ) {
            control.add(
                new Option("Calendario escolar", "calendario")
            );
        }
    });

    const hoy = new Date();
    let anio = hoy.getFullYear();
    let mes = hoy.getMonth();

    const fechaISO = function (a, m, d) {
        return [
            a,
            String(m + 1).padStart(2, "0"),
            String(d).padStart(2, "0")
        ].join("-");
    };

    let seleccionada = fechaISO(
        anio, mes, hoy.getDate()
    );

    const formatoMes = new Intl.DateTimeFormat(
        "es-CL",
        {month: "long", year: "numeric"}
    );

    const formatoFecha = new Intl.DateTimeFormat(
        "es-CL",
        {day: "numeric", month: "long", year: "numeric"}
    );

    function seleccionar(fecha) {
        seleccionada = fecha;
        campoFecha.value = fecha;

        const [a, m, d] = fecha.split("-").map(Number);

        textoFecha.textContent = formatoFecha.format(
            new Date(a, m - 1, d)
        );

        dibujar();
        actualizarDetalle();
    }

    function dibujar() {
        const primero = new Date(anio, mes, 1);
        const ultimo = new Date(anio, mes + 1, 0);

        titulo.textContent = formatoMes.format(primero);

        const espacios = (primero.getDay() + 6) % 7;
        const total = Math.ceil(
            (espacios + ultimo.getDate()) / 7
        ) * 7;

        calendario.replaceChildren();

        for (let posicion = 0; posicion < total; posicion++) {
            const dia = posicion - espacios + 1;

            if (dia < 1 || dia > ultimo.getDate()) {
                calendario.appendChild(
                    document.createElement("span")
                );
                continue;
            }

            const fecha = fechaISO(anio, mes, dia);
            const boton = document.createElement("button");

            boton.dataset.fecha = fecha;

            boton.type = "button";
            boton.className = "mpaz-cal-dia";

            const numero = document.createElement("strong");
            numero.textContent = dia;

            const estado = document.createElement("small");
            const jornada = jornadasMes.get(fecha);

            if (!datosMesCargados) {
                estado.textContent = "Consultando...";
                boton.classList.add("estado-consultando");

            } else if (jornada) {
                estado.textContent =
                    etiquetas[jornada.condicion]
                    || "Estado desconocido";

                boton.classList.add(
                    "estado-" + jornada.condicion
                );

            } else {
                estado.textContent = "Sin configurar";
                boton.classList.add(
                    "estado-sin_configurar"
                );
            }

            boton.append(numero, estado);

            if (fecha === seleccionada) {
                boton.classList.add("seleccionado");
            }

            if (
                fecha === fechaISO(
                    hoy.getFullYear(),
                    hoy.getMonth(),
                    hoy.getDate()
                )
            ) {
                boton.classList.add("es-hoy");
            }

            boton.setAttribute(
                "aria-label",
                "Seleccionar " + formatoFecha.format(
                    new Date(anio, mes, dia)
                )
            );

            boton.addEventListener("click", function () {
                seleccionar(fecha);
            });

            calendario.appendChild(boton);
        }
    }

    document.getElementById(
        "mpaz-cal-anterior"
    ).addEventListener("click", function () {
        const fecha = new Date(anio, mes - 1, 1);
        anio = fecha.getFullYear();
        mes = fecha.getMonth();
        seleccionar(fechaISO(anio, mes, 1));
        cargarMes();
    });

    document.getElementById(
        "mpaz-cal-siguiente"
    ).addEventListener("click", function () {
        const fecha = new Date(anio, mes + 1, 1);
        anio = fecha.getFullYear();
        mes = fecha.getMonth();
        seleccionar(fechaISO(anio, mes, 1));
        cargarMes();
    });

    document.getElementById(
        "mpaz-cal-hoy"
    ).addEventListener("click", function () {
        anio = hoy.getFullYear();
        mes = hoy.getMonth();

        seleccionar(
            fechaISO(anio, mes, hoy.getDate())
        );

        cargarMes();
    });

    campoFecha.addEventListener("change", function () {
        if (!campoFecha.value) return;

        const [a, m] = campoFecha.value
            .split("-")
            .map(Number);

        anio = a;
        mes = m - 1;
        seleccionar(campoFecha.value);
        cargarMes();
    });

    selectorCurso.addEventListener("change", function () {
        selectorAlcance.value = selectorCurso.value;
        cargarMes();
    });

    // Seguridad: sin operaciones POST en este paso.
    document.getElementById(
        "mpaz-cal-guardar"
    ).disabled = true;

    document.getElementById(
        "mpaz-cal-formulario"
    ).addEventListener("submit", function (evento) {
        evento.preventDefault();
    });


    // MPAZ-CALENDARIO-660
    // Consultas exclusivamente de lectura.

    const etiquetas = {
        lectiva: "Lectiva",
        suspendida: "Suspendida",
        feriado: "Feriado",
        reducida: "Reducida",
        horario_especial: "Horario especial"
    };

    const estadoConsulta = document.getElementById(
        "mpaz-cal-estado-consulta"
    );

    const detalleJornada = document.getElementById(
        "mpaz-cal-detalle-jornada"
    );

    const historialContenido = document.getElementById(
        "mpaz-cal-historial-contenido"
    );

    const condicionCampo = document.getElementById(
        "mpaz-cal-condicion"
    );

    const entradaCampo = document.getElementById(
        "mpaz-cal-entrada"
    );

    const salidaCampo = document.getElementById(
        "mpaz-cal-salida"
    );

    const motivoCampo = document.getElementById(
        "mpaz-cal-motivo"
    );

    let jornadasMes = new Map();
    let datosMesCargados = false;
    let numeroConsulta = 0;
    let numeroHistorial = 0;

    function mesActual() {
        return (
            String(anio).padStart(4, "0") + "-" +
            String(mes + 1).padStart(2, "0")
        );
    }

    function textoSeguro(elemento, contenido) {
        elemento.textContent = String(contenido ?? "");
    }

    function limpiarFormulario() {
        condicionCampo.value = "lectiva";
        entradaCampo.value = "";
        salidaCampo.value = "";
        motivoCampo.value = "";
        selectorAlcance.value = selectorCurso.value;
    }

    function actualizarDetalle() {
        const consultaHistorial = ++numeroHistorial;

        const estaEnMes = seleccionada.startsWith(
            mesActual() + "-"
        );

        historialContenido.replaceChildren();

        if (!estaEnMes) {
            textoSeguro(
                detalleJornada,
                "Selecciona una fecha del mes visible."
            );

            textoSeguro(
                historialContenido,
                "Selecciona una fecha del mes."
            );

            return;
        }

        if (!datosMesCargados) {
            textoSeguro(
                detalleJornada,
                "Consultando configuración..."
            );

            textoSeguro(
                historialContenido,
                "Esperando datos del calendario..."
            );

            return;
        }

        const jornada = jornadasMes.get(seleccionada);

        if (!jornada) {
            limpiarFormulario();

            textoSeguro(
                detalleJornada,
                "Sin configurar. Todavía no existe " +
                "una jornada registrada para esta fecha " +
                "y el alcance consultado."
            );

            textoSeguro(
                historialContenido,
                "No existe un registro de jornada " +
                "para consultar su historial."
            );

            return;
        }

        const etiqueta = etiquetas[jornada.condicion]
            || jornada.condicion;

        // Mostrar los datos guardados, sin habilitar guardado.
        condicionCampo.value = jornada.condicion;
        entradaCampo.value = jornada.hora_entrada || "";
        salidaCampo.value = jornada.hora_salida || "";
        motivoCampo.value = jornada.motivo || "";

        selectorAlcance.value =
            jornada.alcance === "curso"
            ? selectorCurso.value
            : "";

        detalleJornada.replaceChildren();

        const titulo = document.createElement("strong");
        titulo.textContent = etiqueta;

        const alcance = document.createElement("p");
        alcance.textContent =
            "Alcance aplicado: " +
            (
                jornada.alcance === "curso"
                ? "Excepción de " + selectorCurso.value
                : "Configuración general de la escuela"
            );

        const motivo = document.createElement("p");
        motivo.textContent =
            "Motivo: " + (jornada.motivo || "Sin motivo");

        detalleJornada.append(titulo, alcance, motivo);

        const cursoHistorial =
            jornada.alcance === "curso"
            ? selectorCurso.value
            : "";

        consultarHistorial(
            seleccionada,
            cursoHistorial,
            consultaHistorial
        );
    }


    // MPAZ-CALENDARIO-669

    function fechaHistorialChile(valor) {
        if (typeof valor !== "string" || !valor.trim()) {
            return "Sin fecha";
        }

        // SQLite CURRENT_TIMESTAMP genera fecha UTC.
        // Ejemplo: 2026-10-27 00:52:09
        const patronUTC =
            /^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$/;

        if (!patronUTC.test(valor)) {
            return valor + " (zona horaria no verificada)";
        }

        const instante = new Date(
            valor.replace(" ", "T") + "Z"
        );

        if (Number.isNaN(instante.getTime())) {
            return valor + " (fecha no válida)";
        }

        const formato = new Intl.DateTimeFormat(
            "es-CL",
            {
                timeZone: "America/Santiago",
                day: "2-digit",
                month: "2-digit",
                year: "numeric",
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit",
                hourCycle: "h23"
            }
        );

        return formato.format(instante) + " (Chile)";
    }

    function valorHistorial(campo, valor) {
        if (valor === null || valor === undefined ||
            valor === "") {
            return "Sin definir";
        }

        if (campo === "condicion") {
            return etiquetas[valor] || String(valor);
        }

        return String(valor);
    }

    function agregarCambiosHistorial(bloque, item) {
        const anterior = item.anterior || {};
        const nuevo = item.nuevo || {};

        const campos = [
            ["Condición", "condicion"],
            ["Entrada", "hora_entrada"],
            ["Salida", "hora_salida"],
            ["Motivo", "motivo"]
        ];

        let diferencias = 0;

        campos.forEach(function (elemento) {
            const etiqueta = elemento[0];
            const campo = elemento[1];

            const valorAnterior = anterior[campo] ?? null;
            const valorNuevo = nuevo[campo] ?? null;

            // Para ediciones, mostrar solamente lo que cambió.
            if (
                item.accion === "editar" &&
                valorAnterior === valorNuevo
            ) {
                return;
            }

            // Para creaciones, omitir campos sin información.
            if (
                item.accion === "crear" &&
                (valorNuevo === null || valorNuevo === "")
            ) {
                return;
            }

            const linea = document.createElement("p");

            const nombre = document.createElement("strong");
            nombre.textContent = etiqueta + ": ";

            const detalle = document.createElement("span");

            if (item.accion === "crear") {
                detalle.textContent = valorHistorial(
                    campo, valorNuevo
                );
            } else {
                detalle.textContent =
                    valorHistorial(campo, valorAnterior) +
                    " → " +
                    valorHistorial(campo, valorNuevo);
            }

            linea.append(nombre, detalle);
            bloque.appendChild(linea);

            diferencias++;
        });

        if (diferencias === 0) {
            const nota = document.createElement("p");
            nota.textContent =
                "Sin diferencias en los campos disponibles.";

            bloque.appendChild(nota);
        }
    }

    async function consultarHistorial(
        fecha,
        curso,
        solicitud
    ) {
        textoSeguro(
            historialContenido,
            "Consultando historial..."
        );

        const parametros = new URLSearchParams({
            fecha: fecha,
            curso: curso
        });

        try {
            const respuesta = await fetch(
                "/panel/calendario/jornadas/historial?" +
                parametros.toString(),
                {
                    credentials: "same-origin",
                    cache: "no-store"
                }
            );

            if (solicitud !== numeroHistorial) {
                return;
            }

            if (respuesta.status === 404) {
                textoSeguro(
                    historialContenido,
                    "No existe un historial para este alcance."
                );
                return;
            }

            if (!respuesta.ok) {
                throw new Error(
                    "HTTP " + respuesta.status
                );
            }

            const datos = await respuesta.json();

            if (!Array.isArray(datos.historial)) {
                throw new Error(
                    "Respuesta de historial incorrecta"
                );
            }

            historialContenido.replaceChildren();

            if (!datos.historial.length) {
                textoSeguro(
                    historialContenido,
                    "La jornada no tiene cambios registrados."
                );
                return;
            }

            datos.historial.forEach(function (item) {
                const bloque = document.createElement("div");
                bloque.className = "mpaz-cal-historial-item";

                const titulo = document.createElement("strong");

                titulo.textContent =
                    (item.accion === "crear"
                        ? "Creación"
                        : "Modificación") +
                    " · " +
                    fechaHistorialChile(item.registrado_en);


                // Mostrar diferencias de condición, horario y motivo.
                // MPAZ-CALENDARIO-6701
                // Conservar titulo, accion y fecha local.
                bloque.appendChild(titulo);
                agregarCambiosHistorial(bloque, item);

                const actor = document.createElement("p");
                actor.textContent =
                    "Origen: " +
                    (item.actor || "No identificado");

                bloque.appendChild(actor);
                historialContenido.appendChild(bloque);
            });

            if (datos.historial_limitado) {
                const aviso = document.createElement("p");
                aviso.textContent =
                    "Se muestran solamente los 100 " +
                    "cambios más recientes.";

                historialContenido.appendChild(aviso);
            }

        } catch (error) {
            if (solicitud !== numeroHistorial) {
                return;
            }

            textoSeguro(
                historialContenido,
                "No fue posible consultar el historial."
            );

            console.error(
                "MPAZ: Error consultando historial:",
                error
            );
        }
    }

    async function cargarMes() {
        const solicitud = ++numeroConsulta;
        const mesSolicitado = mesActual();

        datosMesCargados = false;
        jornadasMes = new Map();

        textoSeguro(
            estadoConsulta,
            "Consultando jornadas de " +
            mesSolicitado + "..."
        );

        dibujar();
        actualizarDetalle();

        const parametros = new URLSearchParams({
            mes: mesSolicitado,
            curso: selectorCurso.value
        });

        try {
            const respuesta = await fetch(
                "/panel/calendario/mes?" +
                parametros.toString(),
                {
                    credentials: "same-origin",
                    cache: "no-store"
                }
            );

            if (!respuesta.ok) {
                throw new Error(
                    "HTTP " + respuesta.status
                );
            }

            const datos = await respuesta.json();

            if (
                datos.resultado !== "ok" ||
                !Array.isArray(datos.jornadas)
            ) {
                throw new Error(
                    "Respuesta mensual inválida"
                );
            }

            // Evitar que una respuesta antigua
            // sobrescriba un mes recién seleccionado.
            if (solicitud !== numeroConsulta) {
                return;
            }

            const jornadas = new Map();

            datos.jornadas.forEach(function (jornada) {
                if (
                    jornada &&
                    typeof jornada.fecha === "string" &&
                    jornada.fecha.startsWith(
                        mesSolicitado + "-"
                    ) &&
                    etiquetas[jornada.condicion]
                ) {
                    jornadas.set(
                        jornada.fecha,
                        jornada
                    );
                }
            });

            jornadasMes = jornadas;
            datosMesCargados = true;

            textoSeguro(
                estadoConsulta,
                jornadas.size
                    ? (
                        "Consulta completada: " +
                        jornadas.size +
                        " fechas configuradas. " +
                        "Las demás permanecen sin configurar."
                    )
                    : (
                        "No existen jornadas configuradas " +
                        "para este mes y alcance. " +
                        "No se asume que estén suspendidas."
                    )
            );

            dibujar();
            actualizarDetalle();

        } catch (error) {
            if (solicitud !== numeroConsulta) {
                return;
            }

            datosMesCargados = false;
            jornadasMes = new Map();

            textoSeguro(
                estadoConsulta,
                "No fue posible consultar el calendario. " +
                "Comprueba tu sesión de pruebas."
            );

            textoSeguro(
                detalleJornada,
                "La información del calendario " +
                "no está disponible."
            );

            textoSeguro(
                historialContenido,
                "Historial no disponible."
            );

            dibujar();

            console.error(
                "MPAZ: Error consultando calendario:",
                error
            );
        }
    }

    seleccionar(seleccionada);
    cargarMes();

    window.dispatchEvent(new Event("hashchange"));
})();
