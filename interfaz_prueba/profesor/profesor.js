/*
 * Sistema MPAZ RFID
 * Portal Docente
 * Escuela Escritora Marcela Paz
 */

document.addEventListener("DOMContentLoaded", () => {

    const formulario = document.getElementById("formulario-profesor");

    // Este archivo también se utilizará en el panel docente.
    if (!formulario) {
        return;
    }

    const campoUsuario = document.getElementById("usuario");
    const campoPassword = document.getElementById("password");
    const botonIngresar = document.getElementById("boton-ingresar");
    const mensajeLogin = document.getElementById("mensaje-login");

    function mostrarMensaje(mensaje, tipo = "error") {
        mensajeLogin.textContent = mensaje;
        mensajeLogin.className = "mensaje-login " + tipo;
    }

    formulario.addEventListener("submit", async (event) => {

        event.preventDefault();

        const usuario = campoUsuario.value.trim();
        const password = campoPassword.value;

        if (!usuario || !password) {
            mostrarMensaje("Ingrese su usuario y contraseña.");
            return;
        }

        botonIngresar.disabled = true;
        botonIngresar.textContent = "Verificando acceso...";

        mostrarMensaje("");

        try {

            const respuesta = await fetch("/profesor/login", {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                credentials: "same-origin",

                body: JSON.stringify({
                    usuario: usuario,
                    password: password
                })
            });

            const datos = await respuesta.json();

            if (!respuesta.ok) {

                if (respuesta.status === 401) {
                    mostrarMensaje("Usuario o contraseña incorrectos.");
                } else if (respuesta.status === 403) {
                    mostrarMensaje("No tiene autorización para acceder.");
                } else {
                    mostrarMensaje("No fue posible iniciar sesión.");
                }

                return;
            }

            if (datos.resultado !== "ok") {
                mostrarMensaje("No fue posible validar la sesión.");
                return;
            }

            mostrarMensaje("Acceso autorizado. Ingresando...", "exito");

            campoPassword.value = "";

            window.location.replace("/profesor/panel.html");

        } catch (error) {

            console.error("Error de conexión con el servidor.");

            mostrarMensaje(
                "No se pudo conectar con el servidor MPAZ RFID."
            );

        } finally {

            botonIngresar.disabled = false;
            botonIngresar.textContent = "Iniciar sesión";

        }

    });

});

/* ==========================================
   PANEL PRINCIPAL DEL DOCENTE
   ========================================== */

document.addEventListener("DOMContentLoaded", async () => {

    const listaAsignaciones = document.getElementById("lista-asignaciones");

    // Este bloque solo funciona dentro del panel docente.
    if (!listaAsignaciones) {
        return;
    }

    const nombreProfesor = document.getElementById("nombre-profesor");
    const mensajePanel = document.getElementById("mensaje-panel");
    const botonCerrarSesion = document.getElementById("boton-cerrar-sesion");

    function mostrarMensajePanel(mensaje, tipo = "") {
        mensajePanel.textContent = mensaje;
        mensajePanel.className = "mensaje-panel " + tipo;
    }

    function redirigirLogin() {
        window.location.replace("/profesor/login.html");
    }

    async function solicitarJSON(ruta, opciones = {}) {
        const respuesta = await fetch(ruta, {
            credentials: "same-origin",
            cache: "no-store",
            ...opciones
        });

        const datos = await respuesta.json();

        return { respuesta, datos };
    }

    async function verificarSesion() {

        const { respuesta, datos } = await solicitarJSON(
            "/profesor/sesion"
        );

        if (!respuesta.ok || datos.resultado !== "ok") {
            return null;
        }

        return datos;
    }

    function crearTarjetaAsignacion(asignacion) {

        const tarjeta = document.createElement("article");
        tarjeta.className = "tarjeta-asignacion";

        const titulo = document.createElement("h3");
        titulo.textContent = "Curso " + asignacion.curso;

        const asignatura = document.createElement("p");
        asignatura.textContent = asignacion.asignatura;

        const boton = document.createElement("button");
        boton.type = "button";
        boton.className = "boton-asignacion";
        boton.textContent = "Gestión de clase";

        // Se habilitará al implementar las clases.
        boton.disabled = true;
        boton.title = "Funcionalidad en desarrollo";

        tarjeta.appendChild(titulo);
        tarjeta.appendChild(asignatura);
        tarjeta.appendChild(boton);

        return tarjeta;
    }

    async function cargarAsignaciones() {

        mostrarMensajePanel("Cargando cursos y asignaturas...");

        const { respuesta, datos } = await solicitarJSON(
            "/profesor/asignaciones"
        );

        if (respuesta.status === 401 || respuesta.status === 403) {
            redirigirLogin();
            return;
        }

        if (!respuesta.ok || datos.resultado !== "ok") {
            mostrarMensajePanel(
                "No fue posible cargar las asignaciones.",
                "error"
            );
            return;
        }

        listaAsignaciones.replaceChildren();

        const asignaciones = datos.asignaciones || [];

        if (asignaciones.length === 0) {
            mostrarMensajePanel(
                "No tiene cursos o asignaturas asignados."
            );
            return;
        }

        asignaciones.forEach((asignacion) => {
            const tarjeta = crearTarjetaAsignacion(asignacion);
            listaAsignaciones.appendChild(tarjeta);
        });

        mostrarMensajePanel(
            "Asignaciones disponibles: " + asignaciones.length
        );
    }

    botonCerrarSesion.addEventListener("click", async () => {

        botonCerrarSesion.disabled = true;

        try {
            await solicitarJSON("/profesor/logout", {
                method: "POST"
            });

            redirigirLogin();

        } catch (error) {
            mostrarMensajePanel(
                "No fue posible cerrar la sesión.",
                "error"
            );

            botonCerrarSesion.disabled = false;
        }

    });

    try {

        const sesion = await verificarSesion();

        if (!sesion) {
            redirigirLogin();
            return;
        }

        // La API determina los datos de la sesión.
        nombreProfesor.textContent =
            sesion.profesor?.nombre ||
            "Profesor autorizado";

        await cargarAsignaciones();

    } catch (error) {

        mostrarMensajePanel(
            "No fue posible conectar con el servidor.",
            "error"
        );

    }

});
