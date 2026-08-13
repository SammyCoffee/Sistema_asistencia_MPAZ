const estudianteDemo = {

    nombre: "Estudiante Demo",

    rut: "RUT-DEMO-01",

    curso: "2A",

    uid: "B1C2D3E4",

    estadoTarjeta: "Activa"

};


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


    if (
        textoBuscado.toLowerCase() === estudianteDemo.nombre.toLowerCase()
    ) {

        mostrarFichaEstudiante(estudianteDemo);

    } else if (
        textoBuscado.toLowerCase() === estudianteDemo.rut.toLowerCase()
    ) {

        mostrarFichaEstudiante(estudianteDemo);

    } else if (
        textoBuscado.toLowerCase() === estudianteDemo.curso.toLowerCase()
    ) {

        mostrarFichaEstudiante(estudianteDemo);

    } else {

        resultadoEstudiante.innerHTML =
            "Estudiante no encontrado";

    }

});