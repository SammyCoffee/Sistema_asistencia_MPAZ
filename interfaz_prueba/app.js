const campoBuscar = document.getElementById("buscar-estudiante");

const botonBuscar = document.getElementById("boton-buscar");
botonBuscar.addEventListener("click", function() {

    const textoBuscado = campoBuscar.value.trim();

    if (textoBuscado === "") {
        
        alert("Escribe un nombre, RUT o curso antes de buscar");

        return;
    }

    alert(textoBuscado);
});

