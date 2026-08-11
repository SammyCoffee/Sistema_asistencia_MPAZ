const estudianteDemo = {

    nombre: "Estudiante Demo",

    rut: "RUT-DEMO-01",

    curso: "2A",

    uid: "B1C2D3E4"

};


const campoBuscar = document.getElementById("buscar-estudiante");

const botonBuscar = document.getElementById("boton-buscar");

const resultadoEstudiante = document.getElementById("resultado-estudiante");


botonBuscar.addEventListener("click", function () {

    const textoBuscado = campoBuscar.value.trim();


    if (textoBuscado === "") {

        resultadoEstudiante.innerHTML = "Escribe un nombre, RUT o curso antes de buscar";

        return;

    }


    if (textoBuscado.toLowerCase() === estudianteDemo.nombre.toLowerCase()) {

        resultadoEstudiante.innerHTML = "Estudiante encontrado: " + estudianteDemo.nombre;
    
    } else if (textoBuscado.toLowerCase() === estudianteDemo.rut.toLowerCase()) {
        
        resultadoEstudiante.innerHTML = "Estudiante encontrado: " + estudianteDemo.nombre;

    } else if (textoBuscado.toLowerCase() === estudianteDemo.curso.toLowerCase()) {

        resultadoEstudiante.innerHTML = "Estudiante encontrado: " + estudianteDemo.nombre;

    } else {

        resultadoEstudiante.innerHTML = "Estudiante no encotrado";

    }

});