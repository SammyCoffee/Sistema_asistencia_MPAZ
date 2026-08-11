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


botonBuscar.addEventListener("click", function () {

    const textoBuscado = campoBuscar.value.trim();


    if (textoBuscado === "") {

        resultadoEstudiante.innerHTML = "Escribe un nombre, RUT o curso antes de buscar";

        return;

    }


    if (textoBuscado.toLowerCase() === estudianteDemo.nombre.toLowerCase()) {

        resultadoEstudiante.innerHTML = `
            <h3>Estudiante encontrado</h3>

            <p><strong>Nombre:</strong> ${estudianteDemo.nombre}</p>

            <p><strong>RUT:</strong> ${estudianteDemo.rut}</p>

            <p><strong>Curso:</strong> ${estudianteDemo.curso}</p>

            <p><strong>UID:</strong> ${estudianteDemo.uid}</p>

            <p><strong>Estado tarjeta:</strong> ${estudianteDemo.estadoTarjeta}</p>

        `;
    
    } else if (textoBuscado.toLowerCase() === estudianteDemo.rut.toLowerCase()) {
        
        resultadoEstudiante.innerHTML = `
            <h3>Estudiante encontrado</h3>

            <p><strong>Nombre:</strong> ${estudianteDemo.nombre}</p>

            <p><strong>RUT:</strong> ${estudianteDemo.rut}</p>

            <p><strong>Curso:</strong> ${estudianteDemo.curso}</p>

            <p><strong>UID:</strong> ${estudianteDemo.uid}</p>

            <p><strong>Estado tarjeta:</strong> ${estudianteDemo.estadoTarjeta}</p>

        `;

    } else if (textoBuscado.toLowerCase() === estudianteDemo.curso.toLowerCase()) {

        resultadoEstudiante.innerHTML = `
            <h3>Estudiante encontrado</h3>

            <p><strong>Nombre:</strong> ${estudianteDemo.nombre}</p>

            <p><strong>RUT:</strong> ${estudianteDemo.rut}</p>

            <p><strong>Curso:</strong> ${estudianteDemo.curso}</p>

            <p><strong>UID:</strong> ${estudianteDemo.uid}</p>

            <p><strong>Estado tarjeta:</strong> ${estudianteDemo.estadoTarjeta}</p>

        `;

    } else {

        resultadoEstudiante.innerHTML = "Estudiante no encotrado";

    }

});