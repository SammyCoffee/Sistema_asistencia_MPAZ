const estudianteDemo = {

    nombre: "Estudiante Demo",

    rut: "RUT-DEMO-01",

    curso: "2A",

    uid: "B1C2D3E4",

    estadoTarjeta: "Activa",

    inasistenciasSemestre: 2

};

const estudianteDemoDos = {

    nombre: "Estudiante Demo Dos",

    rut: "RUT-DEMO-02",

    curso: "3A",

    uid: "A1B2C3D4",

    estadoTarjeta: "Activa",

    inasistenciasSemestre: 7
};

const estudianteDemoTres = {

    nombre: "Estudiante Demo Tres",

    rut: "RUT-DEMO-03",

    curso: "3A",

    uid: "C1D2E3F4",

    estadoTarjeta: "Activa",

    inasistenciasSemestre: 13

};

const estudiantesDemo = [
    estudianteDemo,
    estudianteDemoDos,
    estudianteDemoTres
];


const campoBuscar = document.getElementById("buscar-estudiante");

const botonBuscar = document.getElementById("boton-buscar");

const resultadoEstudiante = 
    document.getElementById("resultado-estudiante");

const botonReporteDiario = 
    document.getElementById("reporte-diario");

const botonReporteSemanal =
    document.getElementById("reporte-semanal");

const botonReporteMensual =
    document.getElementById("reporte-mensual");
    
botonReporteMensual.addEventListener
("click", function() {

    console.log("Botón reporte mensual detectado");
});

botonReporteSemanal.addEventListener("click", function() {

    console.log("Boton reporte semanal detectado");

    const filasSemanales =
    tablaAsistencias.querySelectorAll("tbody tr");

    console.log(
        "Filas para reporte semanal:",
        filasSemanales.length
    );

    let contenidoCsvSemanal = "Hora,Estudiante,Curso,UID,Resultad\n";

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
                `${horaSemanal},${estudianteSemanal},${cursoSemanal},${uidSemanal},${resultadoSemanal}̣\n`;
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

    console.log("Botón reporte diario detectado");

const filasAsistencias = 
    tablaAsistencias.querySelectorAll("tbody tr");
    
console.log("Filas de asistencia encontradas:", filasAsistencias.length);

let contenidoCsv = "Hora,Estudiante,Curso,UID,Resultado\n";

filasAsistencias.forEach(function(fila) {

    const celdas = fila.querySelectorAll("td");

    console.log(
        celdas[0].textContent,
        celdas[1].textContent,
        celdas[2].textContent,
        celdas[3].textContent,
        celdas[4].textContent
    );

    const hora = celdas[0].textContent.trim();
    const estudiante = celdas[1].textContent.trim();
    const curso = celdas[2].textContent.trim();
    const uid = celdas[3].textContent.trim();
    const resultado = celdas[4].textContent.trim();

    contenidoCsv += `${hora},${estudiante},${curso},${uid},${resultado}\n`;
});

console.log(contenidoCsv);

const archivoCsv = new Blob(
    [contenidoCsv],
    { type: "text/csv;charset=utf-8;"}
);

console.log("Archivo CSV preparado:", archivoCsv);

const urlArchivo = 
    URL.createObjectURL(archivoCsv);

console.log("URL del archivo:", urlArchivo);

const enlaceDescarga = 
    document.createElement("a");

enlaceDescarga.href = urlArchivo;

enlaceDescarga.download = 
"reporte_diario_asistencia.csv";

console.log("Enlace de descarga preparado:", enlaceDescarga);

enlaceDescarga.click();

setTimeout(function(){
    URL.revokeObjectURL(urlArchivo);
}, 1000);


});    

const totalAlertasInasistencia = 
    document.getElementById("total-alertas-inasistencia");

const cantidadAlertas = estudiantesDemo.filter(function(estudiante) {
    return estudiante.inasistenciasSemestre > 5;

}).length;

totalAlertasInasistencia.textContent = cantidadAlertas;


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

function mostrarTablaInasistencias() {

    tablaInasistencias.innerHTML = "";

    estudiantesDemo.forEach(function(estudiante) {

        tablaInasistencias.innerHTML += `
        <tr>
            <td>${estudiante.nombre}</td>

            <td>${estudiante.curso}</td>
            
            <td>
                <span class="${obtenerClaseInasistencias(estudiante.inasistenciasSemestre)}">
                    ${estudiante.inasistenciasSemestre}
                </span>
            </td>

            <td>
                    ${
                        estudiante.inasistenciasSemestre > 12
                        ? "Critica"
                        :estudiante.inasistenciasSemestre > 5
                            ? "Alerta"
                            : "Buena"
                    }
            </td>
        </tr>                
    `;
    });
}  

mostrarTablaInasistencias();


function mostrarFichaEstudiante(estudiante) {


    resultadoEstudiante.innerHTML = `
        <h3>Estudiante encontrado</h3>

        <p>
            <strong>Nombre:</strong>
            ${estudiante.nombre}
        </p>

        <p>
            <strong>RUT:</strong>
            ${estudiante.rut}
        </p>

        <p>
            <strong>Curso:</strong>
            ${estudiante.curso}
        </p>

        <p>
            <strong> Inasistencias semestre:</strong>
            
            <span class="${obtenerClaseInasistencias(estudiante.inasistenciasSemestre)}">
                ${estudiante.inasistenciasSemestre}
            </span>    
        </p>    

        <p>
            <strong>UID:</strong>
            ${estudiante.uid}
        </p>

        <p>
            <strong>Estado tarjeta:</strong>

            <span class="estado-tarjeta ${estudiante.estadoTarjeta === "Bloqueada" ? "estado-tarjeta-bloqueada" : ""}">
                ${estudiante.estadoTarjeta}
            </span>
        </p>

        <button  
            type= "button" 
            class="boton-bloquear-tarjeta ${estudiante.estadoTarjeta === "Bloqueada" ? "boton-activar-tarjeta" : ""}"
            data-rut="${estudiante.rut}"
        >
            ${estudiante.estadoTarjeta === "Bloqueada" ? "Activar tarjeta" : "Bloquear tarjeta"}    
        </button>
        
        <button
            type="button"
            class="boton-cambiar-tarjeta"
            data-rut="${estudiante.rut}"
        >
        
            Cambiar tarjeta RFID
        </button>    
    `;

}


botonBuscar.addEventListener("click", function () {

    const textoBuscado = campoBuscar.value.trim();


    if (textoBuscado === "") {

        resultadoEstudiante.innerHTML =
            "Escribe un nombre, RUT o curso antes de buscar";

        return;

    }

    const estudiantesDelCurso = estudiantesDemo.filter(function(estudiante) {

        return (
            textoBuscado.toLowerCase() === estudiante.curso.toLowerCase()

        
        );
    });

    if (estudiantesDelCurso.length > 0) {

        console.log(
            "Estudiantes encontrados en el curso:",
            estudiantesDelCurso.length
        );
    }

    const estudianteEncontrado = estudiantesDemo.find(function (estudiante) {

        return (
            textoBuscado.toLowerCase() === estudiante.nombre.toLowerCase() ||
            textoBuscado.toLowerCase() === estudiante.rut.toLowerCase() ||
            textoBuscado.toLowerCase() === estudiante.curso.toLowerCase() ||
            textoBuscado.toLowerCase() === estudiante.uid.toLowerCase()
        );

    });   
    
    if (estudiantesDelCurso.length > 1) {

        resultadoEstudiante.innerHTML = 
        "<h3>Estudiantes encontrados</h3>";

        estudiantesDelCurso.forEach(function(estudiante) {

            resultadoEstudiante.innerHTML +=
            "<P>" + 
                "<strong>" + estudiante.nombre + "</strong><br>" +
                "RUT: " + estudiante.rut + "<br>" +
                "Curso: " + estudiante.curso + "<br>" +
                "UID: " + estudiante.uid + "<br>" +
                "Estado tarjeta: " + estudiante.estadoTarjeta + "<br>" +
                "<button class='boton-ver-ficha' data-rut= '" + estudiante.rut + "'>Ver ficha</button>" +
            "</p>";    

        });

       
    } else if (estudianteEncontrado) {

        mostrarFichaEstudiante(estudianteEncontrado);
    } else {

        resultadoEstudiante.innerHTML = 
        "Estudiante no encontrado";
    }


    

});

resultadoEstudiante.addEventListener("click", function (evento) {

    if (evento.target.classList.contains("boton-ver-ficha"))  {

        const rutSeleccionado = evento.target.dataset.rut;

        const estudianteSeleccionado = estudiantesDemo.find(function (estudiante) {
            return estudiante.rut === rutSeleccionado;
        });

        mostrarFichaEstudiante(estudianteSeleccionado);
    }
    else if (evento.target.classList.contains("boton-bloquear-tarjeta")) {
      
        const rutSeleccionado = evento.target.dataset.rut;

        const estudianteSeleccionado = estudiantesDemo.find(function(estudiante) {
            return estudiante.rut === rutSeleccionado;    
        });


        estudianteSeleccionado.estadoTarjeta = 
        estudianteSeleccionado.estadoTarjeta === "Bloqueada"
            ? "Activa"
            : "Bloqueada";
        
        mostrarFichaEstudiante(estudianteSeleccionado);    
    }

    else if (evento.target.classList.contains("boton-cambiar-tarjeta")) {

        const rutSeleccionado = evento.target.dataset.rut;

        const estudianteSeleccionado = estudiantesDemo.find(function(estudiante) {
            return estudiante.rut === rutSeleccionado;
        });

        const nuevaUid = prompt("Ingresa la UID de la nueva tarjeta RFID:");
        
            if (nuevaUid === null || nuevaUid.trim() === "") {
                return;
            }

            const uidLimpia = nuevaUid.trim().toUpperCase();

            const uidYaAsignada = estudiantesDemo.some(function(estudiante) {
                return estudiante.uid === uidLimpia &&
                        estudiante.rut !== rutSeleccionado;
            });

            if (uidYaAsignada) {
                alert("Esa UID ya está asignada a otro estudiante.");
                return;
            }

            estudianteSeleccionado.uid = uidLimpia;

            mostrarFichaEstudiante(estudianteSeleccionado);            
        }    
            
        });