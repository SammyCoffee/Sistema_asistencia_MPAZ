const estudianteDemo = {
    nombre: "Estudiante Demo",

    curso: "2A",

    uid: "B1C2D3E4"
};

const campoBuscar = document.getElementById("buscar-estudiante");

const botonBuscar = document.getElementById("boton-buscar");
botonBuscar.addEventListener("click", function() {

    const textoBuscado = campoBuscar.value.trim();

    if (textoBuscado === "") {
        
        alert("Escribe un nombre, RUT o curso antes de buscar");

        return;
    }

    if (textoBuscado.toLowerCase() === estudianteDemo.nombre.toLowerCase()) {

        alert("Estudiante encontrado");

    }
    
    
    {else {
        alert("Estudiante no encontrado");
    } 
    
});

