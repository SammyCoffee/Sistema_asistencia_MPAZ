


const campoBuscar = document.getElementById("buscar-estudiante");

const botonBuscar = document.getElementById("boton-buscar");

const resultadoEstudiante = 
    document.getElementById("resultado-estudiante");

let alumnosEncontrados = [];    

const totalAlertasInasistencia =
    document.getElementById(
        "total-alertas-inasistencia"
    );

    

const totalEstudiantes =
    document.getElementById("total-estudiantes");

const totalTarjetasActivas =
    document.getElementById("total-tarjetas-activas");

const botonReporteDiario =
    document.getElementById("reporte-diario");

const botonReporteSemanal =
    document.getElementById("reporte-semanal");

const botonReporteMensual =
    document.getElementById("reporte-mensual");

const botonReporteAnual =
    document.getElementById("reporte-anual");

const filtroCursoReporte =
    document.getElementById("filtro-curso-reporte");

const cuerpoAsistencias =
    document.getElementById("cuerpo-asistencias");

const totalAsistenciasHoy =
    document.getElementById("total-asistencias-hoy");

const botonCerrarSesion =
    document.getElementById("boton-cerrar-sesion");


botonCerrarSesion.addEventListener("click", async function() {

    console.log("Boton cerrar sesión detectado");

    const respuesta = await fetch("/panel/logout", {
        method: "POST"
    });

    if (respuesta.ok) {
        window.location.href = "/login.html";
    }
});


function descargarReporte(periodo) {

    const curso = filtroCursoReporte.value;

    console.log(
        "Descargando reporte:",
        periodo,
        "Curso:",
        curso || "Todos"
    );

    let url = "/asistencias/exportar/" + periodo;

    if (curso) {
        url += "?curso=" + encodeURIComponent(curso);
    }

    window.location.href = url;
}


botonReporteDiario.addEventListener("click", function() {
    descargarReporte("diario");
});


botonReporteSemanal.addEventListener("click", function() {
    descargarReporte("semanal");
});


botonReporteMensual.addEventListener("click", function() {
    descargarReporte("mensual");
});


botonReporteAnual.addEventListener("click", function() {
    descargarReporte("anual");
});


async function cargarResumenEstudiantes() {

    const respuesta = await fetch("/alumnos");

    if (!respuesta.ok) {
        console.error(
            "No se pudo cargar el resumen de estudiantes"
        );
        return;
    }

    const datos = await respuesta.json();

    const cursos = [
        ...new Set(
            datos.alumnos
                .map(function(alumno) {
                    return alumno.curso;
                })
                .filter(function(curso) {
                    return curso;
                })
        )
    ].sort();

    filtroCursoReporte.innerHTML =
        '<option value="">Todos los cursos</option>';

    cursos.forEach(function(curso) {

        const opcion =
            document.createElement("option");

        opcion.value = curso;
        opcion.textContent = curso;

        filtroCursoReporte.appendChild(opcion);

    });

    totalEstudiantes.textContent =
        datos.total;

    const tarjetasActivas =
        datos.alumnos.filter(function(alumno) {
            return (
                alumno.uid !== null &&
                alumno.estado_tarjeta === "activa"
            );
        }).length;

    totalTarjetasActivas.textContent =
        tarjetasActivas;
}


cargarResumenEstudiantes();

async function cargarAsistencias() {

    const respuesta = await fetch("/asistencias");
	
    if (!respuesta.ok) {
        console.error(
            "No se pudieron cargar las asistencias"
        );
        return;
    }

    const datos = await respuesta.json();

    console.log(
        "Asistencias recibidas:",
        datos.asistencias
    );

    const ahora = new Date();

const fechaHoy = [
    ahora.getFullYear(),
    String(ahora.getMonth() + 1).padStart(2, "0"),
    String(ahora.getDate()).padStart(2, "0")
].join("-");

const cantidadAsistenciasHoy =
    datos.asistencias.filter(function (asistencia) {
        return asistencia.fecha === fechaHoy;
    }).length;

totalAsistenciasHoy.textContent =
    cantidadAsistenciasHoy;    

    cuerpoAsistencias.innerHTML = "";

    if (datos.asistencias.length === 0) {

        cuerpoAsistencias.innerHTML = `
            <tr>
                <td colspan="6">
                    No hay asistencias registradas.
                </td>
            </tr>
        `;

        return;
    }

    datos.asistencias.forEach(function (asistencia) {

        const fila = document.createElement("tr");

        let tipoSalida = "Pendiente";

        if (asistencia.tipo_salida === "totem") {
            tipoSalida = "Tótem";
        }

        if (asistencia.tipo_salida === "automatica") {
            tipoSalida = "Automática";
        }

        const horaSalida =
            asistencia.hora_salida ?? "Pendiente";

        fila.innerHTML = `
            <td>${asistencia.fecha}</td>
            <td>${asistencia.nombre}</td>
            <td>${asistencia.curso}</td>
            <td>${asistencia.hora_entrada ?? "--"}</td>
            <td>${horaSalida}</td>
            <td>${tipoSalida}</td>
        `;

        cuerpoAsistencias.appendChild(fila);
    });
}


cargarAsistencias();

function obtenerEstadoInasistencia(cantidad, periodo) {

    if (periodo === "diario") {

        if (cantidad >= 1) {
            return {
                texto: "Inasistente",
                clase: "inasistencias-rojo",
                alerta: true
            };
        }

        return {
            texto: "Normal",
            clase: "inasistencias-verde",
            alerta: false
        };
    }


    if (periodo === "semanal") {

        if (cantidad >= 3) {
            return {
                texto: "Alerta",
                clase: "inasistencias-rojo",
                alerta: true
            };
        }

        if (cantidad >= 1) {
            return {
                texto: "Observación",
                clase: "inasistencias-amarillo",
                alerta: false
            };
        }

        return {
            texto: "Normal",
            clase: "inasistencias-verde",
            alerta: false
        };
    }


    if (cantidad >= 13) {
        return {
            texto: "Crítico",
            clase: "inasistencias-rojo",
            alerta: true
        };
    }

    if (cantidad >= 6) {
        return {
            texto: "Alerta",
            clase: "inasistencias-amarillo",
            alerta: true
        };
    }

    return {
        texto: "Normal",
        clase: "inasistencias-verde",
        alerta: false
    };
}


function obtenerFechaActual() {

    const ahora = new Date();

    return [
        ahora.getFullYear(),
        String(ahora.getMonth() + 1).padStart(2, "0"),
        String(ahora.getDate()).padStart(2, "0")
    ].join("-");
}


const tablaInasistencias =
    document.getElementById("tabla-inasistencias");

const periodoInasistencias =
    document.getElementById("periodo-inasistencias");

const fechaInasistencias =
    document.getElementById("fecha-inasistencias");

const botonFiltrarInasistencias =
    document.getElementById("boton-filtrar-inasistencias");

const resumenInasistencias =
    document.getElementById("resumen-inasistencias");


const tablaAtrasos =
    document.getElementById("tabla-atrasos");

const periodoAtrasos =
    document.getElementById("periodo-atrasos");

const fechaAtrasos =
    document.getElementById("fecha-atrasos");

const botonFiltrarAtrasos =
    document.getElementById("boton-filtrar-atrasos");

const resumenAtrasos =
    document.getElementById("resumen-atrasos");


fechaInasistencias.value =
    obtenerFechaActual();

fechaAtrasos.value =
    obtenerFechaActual();


async function cargarInasistencias() {

    const periodo =
        periodoInasistencias.value;

    const fecha =
        fechaInasistencias.value;

    let url =
        `/inasistencias?periodo=${encodeURIComponent(periodo)}`;

    if (fecha) {
        url += `&fecha=${encodeURIComponent(fecha)}`;
    }

    const respuesta = await fetch(url);

    if (!respuesta.ok) {
        console.error(
            "No se pudieron cargar las inasistencias"
        );
        return;
    }

    const datos = await respuesta.json();

    tablaInasistencias.innerHTML = "";

    let cantidadAlertas = 0;

    let jornadasPeriodo = 0;

    if (datos.inasistencias.length > 0) {
        jornadasPeriodo =
            datos.inasistencias[0].jornadas_periodo;
    }

    datos.inasistencias.forEach(function (alumno) {

        const cantidad =
            alumno.inasistencias;

        const estado =
            obtenerEstadoInasistencia(
                cantidad,
                periodo
            );

        if (estado.alerta) {
            cantidadAlertas++;
        }

        const fila =
            document.createElement("tr");

        fila.innerHTML = `
            <td>${alumno.nombre}</td>
            <td>${alumno.curso}</td>
            <td>${cantidad}</td>
            <td>${alumno.jornadas_periodo}</td>
            <td>
                <span class="${estado.clase}">
                    ${estado.texto}
                </span>
            </td>
        `;

        tablaInasistencias.appendChild(fila);
    });

    resumenInasistencias.textContent =
        `Jornadas consideradas: ${jornadasPeriodo}`;

    totalAlertasInasistencia.textContent =
        cantidadAlertas;
}


async function cargarAtrasos() {

    const periodo =
        periodoAtrasos.value;

    const fecha =
        fechaAtrasos.value;

    let url =
        `/atrasos?periodo=${encodeURIComponent(periodo)}`;

    if (fecha) {
        url += `&fecha=${encodeURIComponent(fecha)}`;
    }

    const respuesta = await fetch(url);

    if (!respuesta.ok) {
        console.error(
            "No se pudieron cargar los atrasos"
        );
        return;
    }

    const datos = await respuesta.json();

    tablaAtrasos.innerHTML = "";

    if (datos.atrasos.length === 0) {

        tablaAtrasos.innerHTML = `
            <tr>
                <td colspan="5">
                    No hay atrasos registrados
                    para el período seleccionado.
                </td>
            </tr>
        `;

        resumenAtrasos.textContent =
            "Total de atrasos: 0";

        return;
    }

    datos.atrasos.forEach(function (atraso) {

        const fila =
            document.createElement("tr");

        fila.innerHTML = `
            <td>${atraso.fecha}</td>
            <td>${atraso.nombre}</td>
            <td>${atraso.curso}</td>
            <td>${atraso.hora_entrada}</td>
            <td>${atraso.minutos_atraso} min</td>
        `;

        tablaAtrasos.appendChild(fila);
    });

    resumenAtrasos.textContent =
        `Total de atrasos: ${datos.total}`;
}


botonFiltrarInasistencias.addEventListener(
    "click",
    cargarInasistencias
);


botonFiltrarAtrasos.addEventListener(
    "click",
    cargarAtrasos
);


cargarInasistencias();
cargarAtrasos();


async function actualizarPanel() {

    await cargarResumenEstudiantes();
    await cargarAsistencias();
    await cargarInasistencias();
    await cargarAtrasos();
}


setInterval(
    actualizarPanel,
    10000
);


// ==========================================
// ADMINISTRACIÓN DE ESTUDIANTES
// ==========================================

const formularioEstudiante =
    document.getElementById("formulario-estudiante");

const campoEstudianteId =
    document.getElementById("estudiante-id");

const campoEstudianteRut =
    document.getElementById("estudiante-rut");

const campoEstudianteNombre =
    document.getElementById("estudiante-nombre");

const campoEstudianteCurso =
    document.getElementById("estudiante-curso");

const mensajeEstudiante =
    document.getElementById("mensaje-estudiante");

const tituloFormularioEstudiante =
    document.getElementById("titulo-formulario-estudiante");

const botonCancelarEdicionEstudiante =
    document.getElementById(
        "boton-cancelar-edicion-estudiante"
    );
const formularioTarjeta =
    document.getElementById("formulario-tarjeta");

const campoTarjetaUid =
    document.getElementById("tarjeta-uid");

const mensajeTarjeta =
    document.getElementById("mensaje-tarjeta");

const tablaTarjetas =
    document.getElementById("tabla-tarjetas");
const formularioVinculacion =
    document.getElementById("formulario-vinculacion");

const selectVinculacionEstudiante =
    document.getElementById("vinculacion-estudiante");

const selectVinculacionTarjeta =
    document.getElementById("vinculacion-tarjeta");

const mensajeVinculacion =
    document.getElementById("mensaje-vinculacion");
botonCancelarEdicionEstudiante.addEventListener(
    "click",
    function () {

        formularioEstudiante.reset();

        campoEstudianteId.value = "";

        tituloFormularioEstudiante.textContent =
            "Nuevo estudiante";

        botonCancelarEdicionEstudiante.hidden =
            true;

        mensajeEstudiante.textContent =
            "Edición cancelada.";
    }
);
formularioEstudiante.addEventListener(
    "submit",
    async function (evento) {

        evento.preventDefault();

        const id =
            campoEstudianteId.value.trim();

        const rut =
            campoEstudianteRut.value.trim();

        const nombre =
            campoEstudianteNombre.value.trim();

        const curso =
            campoEstudianteCurso.value
                .trim()
                .toUpperCase();

        if (
            rut === "" ||
            nombre === "" ||
            curso === ""
        ) {
            mensajeEstudiante.textContent =
                "Debes completar todos los campos.";

            return;
        }


        const editando =
            id !== "";

        const url = editando
            ? "/panel/alumnos/editar"
            : "/panel/alumnos/registrar";


        const datosEnviar = {
            rut: rut,
            nombre: nombre,
            curso: curso
        };


        if (editando) {
            datosEnviar.id =
                Number(id);
        }


        mensajeEstudiante.textContent =
            editando
                ? "Guardando cambios..."
                : "Guardando estudiante...";


        try {

            const respuesta = await fetch(
                url,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(
                        datosEnviar
                    )
                }
            );


            const datos =
                await respuesta.json();


            console.log(
                "Respuesta estudiante:",
                datos
            );


            if (
                datos.resultado === "registrado" ||
                datos.resultado === "actualizado"
            ) {

                mensajeEstudiante.textContent =
                    editando
                        ? "Estudiante actualizado correctamente."
                        : "Estudiante registrado correctamente.";


                formularioEstudiante.reset();

                campoEstudianteId.value = "";

                tituloFormularioEstudiante.textContent =
                    "Nuevo estudiante";

                botonCancelarEdicionEstudiante.hidden =
                    true;


                await cargarResumenEstudiantes();

                return;
            }


            if (
                datos.resultado ===
                "rut_repetido"
            ) {

                mensajeEstudiante.textContent =
                    "Ya existe un estudiante con ese RUT.";

                return;
            }

            if (
                    datos.resultado ===
                    "curso_invalido"
                ) {
                    mensajeEstudiante.textContent =
                        "Debes seleccionar un curso válido.";

                    return;
                }


            if (
                datos.resultado ===
                "alumno_no_existe"
            ) {

                mensajeEstudiante.textContent =
                    "El estudiante ya no existe.";

                return;
            }


            mensajeEstudiante.textContent =
                datos.mensaje ??
                "No se pudo guardar el estudiante.";


        } catch (error) {

            console.error(
                "Error al guardar estudiante:",
                error
            );

            mensajeEstudiante.textContent =
                "Error de comunicación con el servidor.";
        }
    }
);
async function cargarTarjetas() {

    const respuesta = await fetch(
        "/panel/tarjetas"
    );

    if (!respuesta.ok) {

        console.error(
            "No se pudieron cargar las tarjetas RFID"
        );

        return;
    }

    const datos =
        await respuesta.json();

    tablaTarjetas.innerHTML = "";

    if (datos.tarjetas.length === 0) {

        tablaTarjetas.innerHTML = `
            <tr>
                <td colspan="6">
                    No hay tarjetas RFID registradas.
                </td>
            </tr>
        `;

        return;
    }

    datos.tarjetas.forEach(function (tarjeta) {

        const fila =
            document.createElement("tr");

        const celdaUid =
            document.createElement("td");

        const celdaEstado =
            document.createElement("td");

        const celdaAlumno =
            document.createElement("td");

        const celdaCurso =
            document.createElement("td");

        const celdaFecha =
            document.createElement("td");

        const celdaAcciones =
            document.createElement("td");


        celdaUid.textContent =
            tarjeta.uid;

        celdaEstado.textContent =
            tarjeta.estado;

        celdaAlumno.textContent =
            tarjeta.alumno ??
            "Sin estudiante";

        celdaCurso.textContent =
            tarjeta.curso ??
            "-";

        celdaFecha.textContent =
            tarjeta.fecha_registro ??
            "-";

        if (tarjeta.estado === "activa") {

    const botonExtraviada =
        document.createElement("button");

    botonExtraviada.type =
        "button";

    botonExtraviada.className =
        "boton-tarjeta-extraviada";

    botonExtraviada.dataset.uid =
        tarjeta.uid;

    botonExtraviada.textContent =
        "Marcar extraviada";

    celdaAcciones.appendChild(
        botonExtraviada
    );

} else {

    celdaAcciones.textContent =
        "-";
}


        fila.appendChild(celdaUid);
        fila.appendChild(celdaEstado);
        fila.appendChild(celdaAlumno);
        fila.appendChild(celdaCurso);
        fila.appendChild(celdaFecha);
        fila.appendChild(celdaAcciones);

        tablaTarjetas.appendChild(fila);
    });
}
async function cargarOpcionesVinculacion() {

    try {

        const respuestaAlumnos =
            await fetch("/alumnos");

        const respuestaTarjetas =
            await fetch("/panel/tarjetas");

        if (
            !respuestaAlumnos.ok ||
            !respuestaTarjetas.ok
        ) {
            console.error(
                "No se pudieron cargar las opciones de vinculación"
            );

            return;
        }

        const datosAlumnos =
            await respuestaAlumnos.json();

        const datosTarjetas =
            await respuestaTarjetas.json();


        selectVinculacionEstudiante.innerHTML = `
            <option value="">
                Selecciona un estudiante
            </option>
        `;

        selectVinculacionTarjeta.innerHTML = `
            <option value="">
                Selecciona una tarjeta
            </option>
        `;


        const alumnosDisponibles =
            datosAlumnos.alumnos.filter(function (alumno) {

                return (
                    alumno.estado_alumno === "activo" &&
                    alumno.estado_tarjeta !== "activa"
                );
            });


        alumnosDisponibles.forEach(function (alumno) {

            const opcion =
                document.createElement("option");

            opcion.value =
                alumno.id;

            opcion.textContent =
                `${alumno.nombre} - ${alumno.curso} - ${alumno.rut}`;

            selectVinculacionEstudiante.appendChild(
                opcion
            );
        });


        const tarjetasDisponibles =
            datosTarjetas.tarjetas.filter(function (tarjeta) {

                return tarjeta.estado === "disponible";
            });


        tarjetasDisponibles.forEach(function (tarjeta) {

            const opcion =
                document.createElement("option");

            opcion.value =
                tarjeta.uid;

            opcion.textContent =
                tarjeta.uid;

            selectVinculacionTarjeta.appendChild(
                opcion
            );
        });

    } catch (error) {

        console.error(
            "Error cargando vinculación:",
            error
        );
    }
}
tablaTarjetas.addEventListener(
    "click",
    async function (evento) {

        if (
            !evento.target.classList.contains(
                "boton-tarjeta-extraviada"
            )
        ) {
            return;
        }

        const uid =
            evento.target.dataset.uid;

        const confirmar = confirm(
            `¿Seguro que deseas marcar la tarjeta ${uid} como extraviada?`
        );

        if (!confirmar) {
            return;
        }

        try {

            const respuesta = await fetch(
                "/panel/tarjetas/extraviada",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        uid: uid
                    })
                }
            );

            const datos =
                await respuesta.json();

            console.log(
                "Tarjeta extraviada:",
                datos
            );

            if (
                datos.resultado ===
                "extraviada"
            ) {

                alert(
                    "Tarjeta marcada como extraviada correctamente."
                );

                await cargarTarjetas();

                await cargarOpcionesVinculacion();

                await cargarResumenEstudiantes();

                return;
            }

            if (
                datos.resultado ===
                "ya_extraviada"
            ) {

                alert(
                    "La tarjeta ya estaba marcada como extraviada."
                );

                return;
            }

            alert(
                datos.mensaje ??
                "No se pudo marcar la tarjeta como extraviada."
            );

        } catch (error) {

            console.error(
                "Error al marcar tarjeta extraviada:",
                error
            );

            alert(
                "Error de comunicación con el servidor."
            );
        }
    }
);
cargarTarjetas();
cargarOpcionesVinculacion();
formularioVinculacion.addEventListener(
    "submit",
    async function (evento) {

        evento.preventDefault();

        const alumnoId =
            Number(selectVinculacionEstudiante.value);

        const uid =
            selectVinculacionTarjeta.value
                .trim()
                .toUpperCase();


        if (!alumnoId || uid === "") {

            mensajeVinculacion.textContent =
                "Debes seleccionar un estudiante y una tarjeta.";

            return;
        }


        mensajeVinculacion.textContent =
            "Vinculando tarjeta...";


        try {

            const respuesta = await fetch(
                "/panel/tarjetas/vincular",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        alumno_id: alumnoId,
                        uid: uid
                    })
                }
            );


            const datos =
                await respuesta.json();


            console.log(
                "Vinculación de tarjeta:",
                datos
            );


            if (
                datos.resultado ===
                "vinculada"
            ) {

                mensajeVinculacion.textContent =
                    "Tarjeta vinculada correctamente.";

                formularioVinculacion.reset();


                await cargarTarjetas();

                await cargarOpcionesVinculacion();

                await cargarResumenEstudiantes();

                return;
            }


            if (
                datos.resultado ===
                "ya_tiene_tarjeta"
            ) {

                mensajeVinculacion.textContent =
                    "El estudiante ya tiene una tarjeta activa.";

                return;
            }


            if (
                datos.resultado ===
                "tarjeta_no_disponible"
            ) {

                mensajeVinculacion.textContent =
                    "La tarjeta seleccionada ya no está disponible.";

                await cargarOpcionesVinculacion();

                return;
            }


            if (
                datos.resultado ===
                "alumno_inactivo"
            ) {

                mensajeVinculacion.textContent =
                    "No se puede vincular una tarjeta a un estudiante inactivo.";

                return;
            }


            if (
                datos.resultado ===
                "tarjeta_no_existe"
            ) {

                mensajeVinculacion.textContent =
                    "La tarjeta ya no existe en el sistema.";

                return;
            }


            if (
                datos.resultado ===
                "alumno_no_existe"
            ) {

                mensajeVinculacion.textContent =
                    "El estudiante ya no existe.";

                return;
            }


            mensajeVinculacion.textContent =
                datos.mensaje ??
                "No se pudo vincular la tarjeta.";


        } catch (error) {

            console.error(
                "Error al vincular tarjeta:",
                error
            );

            mensajeVinculacion.textContent =
                "Error de comunicación con el servidor.";
        }
    }
);
formularioTarjeta.addEventListener(
    "submit",
    async function (evento) {

        evento.preventDefault();

        const uid =
            campoTarjetaUid.value
                .trim()
                .replace(/\s/g, "")
                .toUpperCase();

        if (uid === "") {

            mensajeTarjeta.textContent =
                "Debes ingresar una UID.";

            return;
        }

        mensajeTarjeta.textContent =
            "Registrando tarjeta...";

        try {

            const respuesta = await fetch(
                "/panel/tarjetas/registrar",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        uid: uid
                    })
                }
            );

            const datos =
                await respuesta.json();

            console.log(
                "Registro de tarjeta:",
                datos
            );

            if (
                datos.resultado ===
                "registrada"
            ) {

                mensajeTarjeta.textContent =
                    "Tarjeta registrada correctamente.";

                formularioTarjeta.reset();

                await cargarTarjetas();

                await cargarOpcionesVinculacion();

                return;
            }

            if (
                datos.resultado ===
                "uid_repetido"
            ) {

                mensajeTarjeta.textContent =
                    "Esta UID ya está registrada.";

                return;
            }

            mensajeTarjeta.textContent =
                datos.mensaje ??
                "No se pudo registrar la tarjeta.";

        } catch (error) {

            console.error(
                "Error al registrar tarjeta:",
                error
            );

            mensajeTarjeta.textContent =
                "Error de comunicación con el servidor.";
        }
    }
);

botonBuscar.addEventListener("click", async function () {

    const textoBuscado = campoBuscar.value.trim();

    if (textoBuscado === "") {

        resultadoEstudiante.innerHTML =
            "Escribe un nombre, RUT o curso antes de buscar";

        return;
    }

    const respuestaBusqueda = await fetch(
        `/alumnos?buscar=${encodeURIComponent(textoBuscado)}`
    );

    const datosBusqueda = await respuestaBusqueda.json();

    console.log(
        "Busqueda real:",
        datosBusqueda.resultado,
        datosBusqueda.total
    );

    const alumnosReales = datosBusqueda.alumnos;

    alumnosEncontrados = alumnosReales;

    console.log(
        "Alumnos reales recibidos:",
        alumnosReales.length
    );

    if (alumnosReales.length === 0) {

        resultadoEstudiante.innerHTML =
            "No se encontraron estudiantes";

        return;
    }

const listaResultados = alumnosReales.map(function (alumno) {

    return `
        <div>
            <p>
                <strong>${alumno.nombre}</strong>
                - ${alumno.curso}
            </p>

            <button
                type="button"
                class="boton-ver-alumno"
                data-id="${alumno.id}"
            >
                Ver ficha
            </button>
        </div>
    `;

}).join("");

resultadoEstudiante.innerHTML = listaResultados;

});

resultadoEstudiante.addEventListener("click", async function (evento) {


    if (evento.target.classList.contains("boton-ver-alumno")) {

        const idAlumno = Number(evento.target.dataset.id);

        console.log("ID del alumno seleccionado:", idAlumno);

        const alumnoSeleccionado = alumnosEncontrados.find(function (alumno){

            return alumno.id === idAlumno;
        });

        console.log(
            "Alumno encontrado:",
            Boolean(alumnoSeleccionado)
        );

        console.log("Datos completos del alumno:", alumnoSeleccionado);
        
        if (alumnoSeleccionado) {

            resultadoEstudiante.innerHTML = `
            <div class="ficha-estudiante">
            
            <h3>${alumnoSeleccionado.nombre}</h3>
            
            <p>
            
            <strong>Curso:</strong>
            ${alumnoSeleccionado.curso}
            
            </p>

            <p>

            <strong>RUT:</strong>
            ${alumnoSeleccionado.rut}

            </p>

            <p>

            <strong>Tarjeta RFID:</strong>
            ${alumnoSeleccionado.uid ?? "Sin tarjeta asignada"}

            </p>

            <p>
            <strong>Estado tarjeta:</strong>
                ${alumnoSeleccionado.estado_tarjeta ?? "Sin tarjeta"}
            </p>

            <p>
            <strong>Estado del estudiante:</strong>
            ${alumnoSeleccionado.estado_alumno}
            </p>

            <button
            type="button"
            class="boton-editar-estudiante"
            data-id="${alumnoSeleccionado.id}"
            >
            Editar estudiante
            </button>

            ${alumnoSeleccionado.estado_alumno === "activo" ? `
            <button
                    type="button"
                    class="boton-desactivar-estudiante"
                    data-id="${alumnoSeleccionado.id}"
                >
                    Dar de baja
                </button>
            ` : `
                <button
                    type="button"
                    class="boton-reactivar-estudiante"
                    data-id="${alumnoSeleccionado.id}"
                >
                    Reactivar estudiante
                </button>
            `}


             ${alumnoSeleccionado.estado_tarjeta === "activa" ? `
                 <button
                        type="button"
                        class="boton-bloquear-tarjeta-real"
                        data-id="${alumnoSeleccionado.id}"
                >
                        Bloquear tarjeta
                </button>
            ` : ""}


              

            <button
                type="button"
                class="boton-volver-resultados"
            >
                Volver a resultados
            </button>        
            
         </div>
            
            `;
        }

        return;
    }
    if (evento.target.classList.contains("boton-editar-estudiante")) {

    const idAlumno =
        Number(evento.target.dataset.id);

    const alumnoSeleccionado =
        alumnosEncontrados.find(function (alumno) {

            return alumno.id === idAlumno;
        });

    if (!alumnoSeleccionado) {

        alert(
            "No se pudo encontrar al estudiante."
        );

        return;
    }

    campoEstudianteId.value =
        alumnoSeleccionado.id;

    campoEstudianteRut.value =
        alumnoSeleccionado.rut;

    campoEstudianteNombre.value =
        alumnoSeleccionado.nombre;

    campoEstudianteCurso.value =
        alumnoSeleccionado.curso;

    tituloFormularioEstudiante.textContent =
        "Editar estudiante";

    botonCancelarEdicionEstudiante.hidden =
        false;

    mensajeEstudiante.textContent =
        "Editando estudiante seleccionado.";

    document
        .getElementById("estudiantes")
        .scrollIntoView({
            behavior: "smooth"
        });

    return;}
    if (
    evento.target.classList.contains(
        "boton-desactivar-estudiante"
    ) ||
    evento.target.classList.contains(
        "boton-reactivar-estudiante"
    )
) {

    const idAlumno =
        Number(evento.target.dataset.id);

    const alumnoSeleccionado =
        alumnosEncontrados.find(function (alumno) {

            return alumno.id === idAlumno;
        });

    if (!alumnoSeleccionado) {

        alert(
            "No se pudo encontrar al estudiante."
        );

        return;
    }


    const nuevoEstado =
        alumnoSeleccionado.estado_alumno === "activo"
            ? "inactivo"
            : "activo";


    const accion =
        nuevoEstado === "inactivo"
            ? "dar de baja"
            : "reactivar";


    const confirmar = confirm(
        `¿Seguro que deseas ${accion} a ${alumnoSeleccionado.nombre}?`
    );

    if (!confirmar) {
        return;
    }


    try {

        const respuesta = await fetch(
            "/panel/alumnos/estado",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    id: idAlumno,
                    estado: nuevoEstado
                })
            }
        );


        const datos =
            await respuesta.json();


        console.log(
            "Cambio de estado de estudiante:",
            datos
        );


        if (
            datos.resultado ===
            "actualizado"
        ) {

            alumnoSeleccionado.estado_alumno =
                datos.estado;

            alumnoSeleccionado.fecha_baja =
                datos.fecha_baja;


            alert(
                nuevoEstado === "inactivo"
                    ? "Estudiante dado de baja correctamente."
                    : "Estudiante reactivado correctamente."
            );


            resultadoEstudiante.innerHTML = `
                <div class="ficha-estudiante">

                    <h3>
                        ${alumnoSeleccionado.nombre}
                    </h3>

                    <p>
                        <strong>Curso:</strong>
                        ${alumnoSeleccionado.curso}
                    </p>

                    <p>
                        <strong>RUT:</strong>
                        ${alumnoSeleccionado.rut}
                    </p>

                    <p>
                        <strong>Tarjeta RFID:</strong>
                        ${alumnoSeleccionado.uid ?? "Sin tarjeta asignada"}
                    </p>

                    <p>
                        <strong>Estado tarjeta:</strong>
                        ${alumnoSeleccionado.estado_tarjeta ?? "Sin tarjeta"}
                    </p>

                    <p>
                        <strong>Estado del estudiante:</strong>
                        ${alumnoSeleccionado.estado_alumno}
                    </p>

                    <button
                        type="button"
                        class="boton-editar-estudiante"
                        data-id="${alumnoSeleccionado.id}"
                    >
                        Editar estudiante
                    </button>

                    ${
                        alumnoSeleccionado.estado_alumno === "activo"
                            ? `
                                <button
                                    type="button"
                                    class="boton-desactivar-estudiante"
                                    data-id="${alumnoSeleccionado.id}"
                                >
                                    Dar de baja
                                </button>
                            `
                            : `
                                <button
                                    type="button"
                                    class="boton-reactivar-estudiante"
                                    data-id="${alumnoSeleccionado.id}"
                                >
                                    Reactivar estudiante
                                </button>
                            `
                    }

                    <button
                        type="button"
                        class="boton-volver-resultados"
                    >
                        Volver a resultados
                    </button>

                </div>
            `;

            await cargarResumenEstudiantes();

            return;
        }


        alert(
            datos.mensaje ??
            "No se pudo cambiar el estado del estudiante."
        );


    } catch (error) {

        console.error(
            "Error al cambiar estado del estudiante:",
            error
        );

        alert(
            "Error de comunicación con el servidor."
        );
    }

    return;
}
    if (evento.target.classList.contains("boton-volver-resultados")) {

        const listaResultados = alumnosEncontrados.map(function (alumno) {

            return `
                <div>
                    <p>
                        <strong>${alumno.nombre}</strong>
                        - ${alumno.curso}
                    </p>

                    <button
                        type="button"
                        class="boton-ver-alumno"
                        data-id="${alumno.id}"
                    >
                        Ver ficha
                    </button>
                </div>
            `;

        }).join("");

        resultadoEstudiante.innerHTML = listaResultados;

        return;
    }


        if (evento.target.classList.contains("boton-bloquear-tarjeta-real")) {

    const idAlumno = Number(evento.target.dataset.id);

    const alumnoSeleccionado = alumnosEncontrados.find(function (alumno) {
        return alumno.id === idAlumno;
    });

    if (!alumnoSeleccionado) {
        alert("No se pudo encontrar al estudiante.");
        return;
    }

    if (!alumnoSeleccionado.uid) {
        alert("El estudiante no tiene una tarjeta RFID.");
        return;
    }

    const confirmarBloqueo = confirm(
        `¿Seguro que deseas bloquear la tarjeta ${alumnoSeleccionado.uid}?`
    );

    if (!confirmarBloqueo) {
        return;
    }

    const respuesta = await fetch(
        "/panel/tarjetas/bloquear",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                uid: alumnoSeleccionado.uid
            })
        }
    );

    const datos = await respuesta.json();

    console.log(
        "Respuesta bloqueo de tarjeta:",
        datos
    );

    if (datos.resultado === "bloqueada") {

        alert("Tarjeta RFID bloqueada correctamente.");

        alumnoSeleccionado.estado_tarjeta = "bloqueada";

        await cargarTarjetas();

        await cargarOpcionesVinculacion();

        await cargarResumenEstudiantes();

       resultadoEstudiante.innerHTML = `
    <div class="ficha-estudiante">

        <h3>${alumnoSeleccionado.nombre}</h3>

        <p>
            <strong>Curso:</strong>
            ${alumnoSeleccionado.curso}
        </p>

        <p>
            <strong>RUT:</strong>
            ${alumnoSeleccionado.rut}
        </p>

        <p>
            <strong>Tarjeta RFID:</strong>
            ${alumnoSeleccionado.uid}
        </p>

        <p>
            <strong>Estado:</strong>
            ${alumnoSeleccionado.estado_tarjeta}
        </p>

        <button
            type="button"
            class="boton-volver-resultados"
        >
            Volver a resultados
        </button>

    </div>
`;
    return;
    }

    alert(
        datos.mensaje ?? "No se pudo bloquear la tarjeta RFID."
    );

    return;
    }

    

            
        
            
        });
