const estudianteDemo = {

    nombre: "Estudiante Demo",

    rut: "RUT-DEMO-01",

    curso: "2A",

    uid: "B1C2D3E4",

    estadoTarjeta: "Activa"

};

const estudianteDemoDos = {

    nombre: "Estudiante Demo Dos",

    rut: "RUT-DEMO-02",

    curso: "3A",

    uid: "A1B2C3D4",

    estadoTarjeta: "Activa"
};

const estudianteDemoTres = {

    nombre: "Estudiante Demo Tres",

    rut: "RUT-DEMO-03",

    curso: "3A",

    uid: "C1D2E3F4",

    estadoTarjeta: "Activa"

};

const estudiantesDemo = [
    estudianteDemo,
    estudianteDemoDos,
    estudianteDemoTres
];


const campoBuscar = document.getElementById("buscar-estudiante");

const botonBuscar = document.getElementById("boton-buscar");

const resultadoEstudiante = document.getElementById("resultado-estudiante");


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
            <strong>UID:</strong>
            ${estudiante.uid}
        </p>

        <p>
            <strong>Estado tarjeta:</strong>

            <span class="estado-tarjeta">
                ${estudiante.estadoTarjeta}
            </span>
        </p>
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
                "Estado tarjeta: " + estudiante.estadoTarjeta +
            "</p>";    

        });

       
    } else if (estudianteEncontrado) {

        mostrarFichaEstudiante(estudianteEncontrado);
    } else {

        resultadoEstudiante.innerHTML = 
        "Estudiante no encontrado";
    }


    

});