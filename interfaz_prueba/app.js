


const campoBuscar = document.getElementById("buscar-estudiante");

const botonBuscar = document.getElementById("boton-buscar");

const resultadoEstudiante = 
    document.getElementById("resultado-estudiante");

let alumnosEncontrados = [];    

const botonReporteDiario = 
    document.getElementById("reporte-diario");

const botonReporteSemanal =
    document.getElementById("reporte-semanal");

const botonReporteMensual =
    document.getElementById("reporte-mensual");

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
    
botonReporteMensual.addEventListener
("click", function() {

    console.log("Botón reporte mensual detectado");

    const filasMensuales = 
    tablaAsistencias.querySelectorAll("tbody tr");

    console.log(
        "Filas para reporte mensual:",
        filasMensuales.length
    );

    let contenidoCsvMensual = 
        "Hora,Estudiante,Curso,UID,Resultado\n";
   
        filasMensuales.forEach(function(fila) {

            const celdas = fila.querySelectorAll("td");

            console.log(
                "Celdas mensuales encontradas:",
                celdas.length
            );
            const horaMensual =
                celdas[0].textContent.trim();
            
            const estudianteMensual =
                celdas[1].textContent.trim();
            
            const cursoMensual =
                celdas[2].textContent.trim(); 
            
            const uidMensual = 
                celdas[3].textContent.trim();
            
            const resultadoMensual = 
                celdas[4].textContent.trim();
            
            contenidoCsvMensual +=
                `${horaMensual},${estudianteMensual},${cursoMensual},${uidMensual},${resultadoMensual}\n`;

                
            console.log("Hora mensual:", horaMensual);
            console.log("Estudiante mensual:", estudianteMensual);
            console.log("Curso mensual:", cursoMensual);
            console.log("UID mensual:", uidMensual);
            console.log("Resultado mensual:", resultadoMensual);    
        });

            console.log("Contenido CSV mensual:");
            console.log(contenidoCsvMensual);

            const archivoCsvMensual = new Blob(
                [contenidoCsvMensual],
                { type: "text/csv;charset=utf-8;" }
            );

            const urlArchivoMensual =
                URL.createObjectURL(archivoCsvMensual);

            const enlaceDescargaMensual = 
                document.createElement("a");
            
        
            enlaceDescargaMensual.href   = urlArchivoMensual;
            
            enlaceDescargaMensual.download =
                "reporte_mensual_asistencia.csv";

           enlaceDescargaMensual.click();
           
           URL.revokeObjectURL(urlArchivoMensual);
 });
botonReporteSemanal.addEventListener("click", function() {

    console.log("Boton reporte semanal detectado");

    const filasSemanales =
    tablaAsistencias.querySelectorAll("tbody tr");

    console.log(
        "Filas para reporte semanal:",
        filasSemanales.length
    );

    let contenidoCsvSemanal = "Hora,Estudiante,Curso,UID,Resultado\n";

    filasSemanales.forEach(function(fila) {

        const celdas = fila.querySelectorAll("td");

        console.log("Celdas encontradas:", celdas.length);

        const horaSemanal =
            celdas[0].textContent.trim();
        
        const estudianteSemanal =
            celdas[1].textContent.trim();

        const cursoSemanal =
            celdas[2].textContent.trim();
            
        const uidSemanal =
            celdas[3].textContent.trim();
        
        const resultadoSemanal =
            celdas[4].textContent.trim();        
        
            console.log("Hora semanal:", horaSemanal);
            console.log("Estudiante semanal:", estudianteSemanal);
            console.log("Curso semanal:", cursoSemanal);
            console.log("UID semanal:", uidSemanal);
            console.log("Resultado semanal:", resultadoSemanal);

            contenidoCsvSemanal +=
    `${horaSemanal},${estudianteSemanal},${cursoSemanal},${uidSemanal},${resultadoSemanal}\n`;;
    });

    console.log("Contenido CSV semanal:");
    console.log(contenidoCsvSemanal);

    const archivoCsvSemanal = new Blob(
        [contenidoCsvSemanal],
        { type: "text/csv;charset=utf-8;" }
    );

    const urlArchivoSemanal =
        URL.createObjectURL(archivoCsvSemanal);
    
    const enlaceDescargaSemanal = 
        document.createElement("a");
        
            enlaceDescargaSemanal.href = urlArchivoSemanal;

            enlaceDescargaSemanal.download = 
                "reporte_semanal_asistencia.csv";
            
                enlaceDescargaSemanal.click();

                setTimeout(function() {
                    URL.revokeObjectURL(urlArchivoSemanal);
                }, 1000);
        
});
    

const tablaAsistencias =
    document.getElementById("tabla-asistencias");


botonReporteDiario.addEventListener("click", function() {

    console.log("Descargando reporte desde el servidor");

    window.location.href = "/asistencias/exportar";

});


function obtenerClaseInasistencias(cantidad) {

    if (cantidad > 12) {
        return "inasistencias-rojo";
    }

    if (cantidad > 5) {
        return "inasistencias-amarillo";
    }

    return "inasistencias-verde";
}


const tablaInasistencias =
    document.getElementById("tabla-inasistencias");






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