const formularioLogin = document.getElementById("login-form");

const campoPassword = document.getElementById("password");

const mensajeLogin = document.getElementById("mensaje-login");


formularioLogin.addEventListener("submit", async function(event) {

    event.preventDefault();
    const password = campoPassword.value;

    const respuesta = await fetch("/panel/login", {
        method:"POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            "password": password
        })
    });

    const datos = await respuesta.json();

    mensajeLogin.textContent = datos.mensaje;

    if (respuesta.ok) {
        window.location.href = "/";
    }
});