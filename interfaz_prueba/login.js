const formularioLogin = document.getElementById("login-form");

const campoUsuario = document.getElementById("usuario");
const campoPassword = document.getElementById("password");

const mensajeLogin = document.getElementById("mensaje-login");


formularioLogin.addEventListener("submit", async function(event) {

    event.preventDefault();
    const usuario = campoUsuario.value.trim();
    const password = campoPassword.value;

    const respuesta = await fetch("/panel/login-individual", {
        method:"POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            "usuario": usuario,
            "password": password
        })
    });

    const datos = await respuesta.json();

    mensajeLogin.textContent = datos.mensaje;

    if (respuesta.ok) {
        if (
            datos.operador &&
            datos.operador.rol === "direccion"
        ) {
            window.location.href = "/seguimiento.html";
        } else {
            window.location.href = "/index.html";
        }
    }
});