


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
            <strong>Estado:</strong>
                ${alumnoSeleccionado.estado_tarjeta ?? "Sin tarjeta"}
            </p>


            ${alumnoSeleccionado.uid === null ? `
                <button
                    type="button"
                    class="boton-asignar-tarjeta"
                    data-id="${alumnoSeleccionado.id}"
                >
                    Asignar tarjeta RFID
                </button>
            ` : ""}

             ${alumnoSeleccionado.estado_tarjeta === "activa" ? `
                 <button
                        type="button"
                        class="boton-bloquear-tarjeta-real"
                        data-id="${alumnoSeleccionado.id}"
                >
                        Bloquear tarjeta
                </button>
            ` : ""}

            ${alumnoSeleccionado.estado_tarjeta === "bloqueada" ? `
                <button
                    type="button"
                    class="boton-reemplazar-tarjeta-real"
                    data-id="${alumnoSeleccionado.id}"
                >
                    Reemplazar tarjeta RFID
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

    if (evento.target.classList.contains("boton-asignar-tarjeta")) {

    const idAlumno = Number(evento.target.dataset.id);

    const alumnoSeleccionado = alumnosEncontrados.find(function (alumno) {
        return alumno.id === idAlumno;
    });

    if (!alumnoSeleccionado) {
        alert("No se pudo encontrar al estudiante.");
        return;
    }

    const nuevaUid = prompt(
        "Ingresa la UID de la tarjeta RFID:"
    );

    if (nuevaUid === null) {
        return;
    }

    const uidLimpia = nuevaUid
        .trim()
        .replace(/\s/g, "")
        .toUpperCase();

    if (uidLimpia === "") {
        alert("Debes ingresar una UID.");
        return;
    }

    const respuesta = await fetch(
        "/panel/tarjetas/asignar",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

                body: JSON.stringify({
                    rut: alumnoSeleccionado.rut,
                    uid: uidLimpia
                })
            }
        );

  const datos = await respuesta.json();

    console.log(
        "Respuesta asignación de tarjeta:",
        datos
    );

    if (datos.resultado === "asignada") {

            alert("Tarjeta RFID asignada correctamente.");

            alumnoSeleccionado.uid = datos.uid;
            alumnoSeleccionado.estado_tarjeta = "activa";

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
                        class="boton-bloquear-tarjeta-real"
                        data-id="${alumnoSeleccionado.id}"
                    >
                        Bloquear tarjeta
                    </button>

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

    if (datos.resultado === "uid_repetido") {

        alert("Esa tarjeta RFID ya está asignada a otro estudiante.");

        return;
    }

    if (datos.resultado === "ya_tiene_tarjeta") {

        alert("Este estudiante ya tiene una tarjeta RFID activa.");

        return;
    }

    alert(
        datos.mensaje ?? "No se pudo asignar la tarjeta RFID."
    );

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

    if (evento.target.classList.contains("boton-reemplazar-tarjeta-real")) {

    const idAlumno = Number(evento.target.dataset.id);

    const alumnoSeleccionado = alumnosEncontrados.find(function (alumno) {
        return alumno.id === idAlumno;
    });

    if (!alumnoSeleccionado) {
        alert("No se pudo encontrar al estudiante.");
        return;
    }

    const nuevaUid = prompt(
        "Ingresa la UID de la nueva tarjeta RFID:"
    );

    if (nuevaUid === null) {
        return;
    }

    const uidLimpia = nuevaUid
        .trim()
        .replace(/\s/g, "")
        .toUpperCase();

    if (uidLimpia === "") {
        alert("Debes ingresar una UID.");
        return;
    }

    const respuesta = await fetch(
        "/panel/tarjetas/asignar",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                rut: alumnoSeleccionado.rut,
                uid: uidLimpia
            })
        }
    );

    const datos = await respuesta.json();

    console.log(
        "Respuesta reemplazo de tarjeta:",
        datos
    );

    if (datos.resultado === "asignada") {

        alert("Nueva tarjeta RFID asignada correctamente.");

        alumnoSeleccionado.uid = datos.uid;
        alumnoSeleccionado.estado_tarjeta = "activa";

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
                    class="boton-bloquear-tarjeta-real"
                    data-id="${alumnoSeleccionado.id}"
                >
                    Bloquear tarjeta
                </button>

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

    if (datos.resultado === "uid_repetido") {
        alert("Esa UID ya existe en el sistema.");
        return;
    }

    if (datos.resultado === "ya_tiene_tarjeta") {
        alert("El estudiante ya tiene una tarjeta RFID activa.");
        return;
    }

    alert(
        datos.mensaje ?? "No se pudo reemplazar la tarjeta RFID."
    );

    return;
}

    

            
        
            
        });
