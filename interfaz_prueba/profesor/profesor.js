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

    const seccionEstudiantes = document.getElementById("seccion-estudiantes");
    const tituloEstudiantes = document.getElementById("titulo-estudiantes");
    const descripcionEstudiantes = document.getElementById("descripcion-estudiantes");
    const mensajeEstudiantes = document.getElementById("mensaje-estudiantes");
    const listaEstudiantes = document.getElementById("lista-estudiantes");

    const seccionAsistencia = document.getElementById("seccion-asistencia");
    const tituloAsistencia = document.getElementById("titulo-asistencia");
    const descripcionAsistencia = document.getElementById("descripcion-asistencia");
    const fechaAsistencia = document.getElementById("fecha-asistencia");
    const mensajeAsistencia = document.getElementById("mensaje-asistencia");

    let cursoAsistenciaSeleccionado = null;
    let asignaturaAsistenciaSeleccionada = null;

    function mostrarSeccionAsistencia(curso, asignatura) {
        cursoAsistenciaSeleccionado = curso;
        asignaturaAsistenciaSeleccionada = asignatura;
        consultaAsistenciaActual++;

        const botonConsulta = document.getElementById(
            "boton-consultar-asistencia"
        );

        botonConsulta.disabled = false;

        seccionAsistencia.hidden = false;

        tituloAsistencia.textContent = "Asistencia RFID - Curso " + curso;
        descripcionAsistencia.textContent = "Asignatura: " + asignatura;

        mensajeAsistencia.className = "mensaje-panel";
        mensajeAsistencia.textContent =
            "Seleccione una fecha y presione Consultar.";

        document.getElementById("resumen-asistencia").hidden = true;
        document.getElementById("contenedor-tabla-asistencia").hidden = true;
        document.getElementById("cuerpo-tabla-asistencia").replaceChildren();

        if (!fechaAsistencia.value) {
            fechaAsistencia.value = new Date().toLocaleDateString("en-CA");
        }
    }


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

    let consultaEstudiantesActual = 0;

    async function cargarEstudiantesCurso(curso, asignatura) {
        const numeroConsulta = ++consultaEstudiantesActual;

        seccionEstudiantes.hidden = false;

        tituloEstudiantes.textContent = "Estudiantes del curso " + curso;
        descripcionEstudiantes.textContent = "Asignatura: " + asignatura;

        listaEstudiantes.replaceChildren();

        mensajeEstudiantes.className = "mensaje-panel";
        mensajeEstudiantes.textContent = "Cargando estudiantes...";

        try {

            const ruta = "/profesor/cursos/"
                + encodeURIComponent(curso)
                + "/alumnos";

            const { respuesta, datos } = await solicitarJSON(ruta);

            if (numeroConsulta !== consultaEstudiantesActual) {
                return;
            }

            if (respuesta.status === 401) {
                redirigirLogin();
                return;
            }

            if (respuesta.status === 403) {
                mensajeEstudiantes.className = "mensaje-panel error";
                mensajeEstudiantes.textContent =
                    "No tiene autorización para consultar este curso.";
                return;
            }

            if (!respuesta.ok || datos.resultado !== "ok") {
                mensajeEstudiantes.className = "mensaje-panel error";
                mensajeEstudiantes.textContent =
                    "No fue posible consultar los estudiantes.";
                return;
            }

            const alumnos = Array.isArray(datos.alumnos)
                ? datos.alumnos
                : [];

            if (alumnos.length === 0) {
                mensajeEstudiantes.textContent =
                    "Este curso no tiene estudiantes activos registrados.";
                return;
            }

            const lista = document.createElement("ol");

            alumnos.forEach((alumno) => {
                const elemento = document.createElement("li");
                elemento.textContent = alumno.nombre;
                lista.appendChild(elemento);
            });

            listaEstudiantes.appendChild(lista);

            mensajeEstudiantes.textContent =
                "Estudiantes encontrados: " + alumnos.length;

        } catch (error) {

            if (numeroConsulta !== consultaEstudiantesActual) {
                return;
            }

            mensajeEstudiantes.className = "mensaje-panel error";
            mensajeEstudiantes.textContent =
                "No fue posible conectar con el servidor.";

        }
    }


    /* ==========================================
       CONSULTA DE ASISTENCIA RFID
       ========================================== */

    const botonConsultarAsistencia = document.getElementById(
        "boton-consultar-asistencia"
    );

    const resumenAsistencia = document.getElementById(
        "resumen-asistencia"
    );

    const contenedorTablaAsistencia = document.getElementById(
        "contenedor-tabla-asistencia"
    );

    const cuerpoTablaAsistencia = document.getElementById(
        "cuerpo-tabla-asistencia"
    );

    const totalEstudiantesAsistencia = document.getElementById(
        "total-estudiantes-asistencia"
    );

    const ingresosRegistrados = document.getElementById(
        "ingresos-registrados"
    );

    const sinRegistroAsistencia = document.getElementById(
        "sin-registro-asistencia"
    );

    let consultaAsistenciaActual = 0;

    function limpiarResultadosAsistencia() {
        resumenAsistencia.hidden = true;
        contenedorTablaAsistencia.hidden = true;
        cuerpoTablaAsistencia.replaceChildren();
    }

    async function consultarAsistenciaRFID() {
        const numeroConsulta = ++consultaAsistenciaActual;
        const curso = cursoAsistenciaSeleccionado;
        const fecha = fechaAsistencia.value;

        limpiarResultadosAsistencia();

        mensajeAsistencia.className = "mensaje-panel";

        if (!curso) {
            mensajeAsistencia.className = "mensaje-panel error";
            mensajeAsistencia.textContent =
                "Primero debe seleccionar un curso.";
            return;
        }

        if (!/^\d{4}-\d{2}-\d{2}$/.test(fecha)) {
            mensajeAsistencia.className = "mensaje-panel error";
            mensajeAsistencia.textContent =
                "Seleccione una fecha válida.";
            return;
        }

        mensajeAsistencia.textContent =
            "Consultando registros de asistencia RFID...";

        botonConsultarAsistencia.disabled = true;

        try {
            const ruta = "/profesor/cursos/"
                + encodeURIComponent(curso)
                + "/asistencia?fecha="
                + encodeURIComponent(fecha);

            const { respuesta, datos } = await solicitarJSON(ruta);

            if (numeroConsulta !== consultaAsistenciaActual) {
                return;
            }

            if (respuesta.status === 401) {
                redirigirLogin();
                return;
            }

            if (respuesta.status === 403) {
                mensajeAsistencia.className = "mensaje-panel error";
                mensajeAsistencia.textContent =
                    "No tiene autorización para consultar este curso.";
                return;
            }

            if (!respuesta.ok || !datos || datos.resultado !== "ok") {
                mensajeAsistencia.className = "mensaje-panel error";
                mensajeAsistencia.textContent =
                    "No fue posible consultar la asistencia RFID.";
                return;
            }

            const estudiantes = Array.isArray(datos.estudiantes)
                ? datos.estudiantes
                : [];

            totalEstudiantesAsistencia.textContent =
                String(datos.total_estudiantes);

            ingresosRegistrados.textContent =
                String(datos.ingresos_registrados);

            sinRegistroAsistencia.textContent =
                String(datos.sin_registro);

            estudiantes.forEach((estudiante) => {
                const fila = document.createElement("tr");

                const nombre = document.createElement("td");
                nombre.textContent = estudiante.nombre ?? "Sin nombre";

                const entrada = document.createElement("td");
                entrada.textContent = estudiante.hora_entrada || "—";

                const salida = document.createElement("td");
                salida.textContent = estudiante.hora_salida || "—";

                const estado = document.createElement("td");
                estado.textContent =
                    estudiante.estado === "ingreso_registrado"
                        ? "Ingreso registrado"
                        : "Sin registro de ingreso";

                fila.appendChild(nombre);
                fila.appendChild(entrada);
                fila.appendChild(salida);
                fila.appendChild(estado);

                cuerpoTablaAsistencia.appendChild(fila);
            });

            resumenAsistencia.hidden = false;
            contenedorTablaAsistencia.hidden =
                estudiantes.length === 0;

            mensajeAsistencia.textContent =
                estudiantes.length === 0
                    ? "Este curso no tiene estudiantes activos registrados."
                    : "Consulta completada correctamente.";

        } catch (error) {
            if (numeroConsulta !== consultaAsistenciaActual) {
                return;
            }

            mensajeAsistencia.className = "mensaje-panel error";
            mensajeAsistencia.textContent =
                "No fue posible conectar con el servidor.";

        } finally {
            if (numeroConsulta === consultaAsistenciaActual) {
                botonConsultarAsistencia.disabled = false;
            }
        }
    }

    fechaAsistencia.addEventListener("change", () => {
        // Invalidar respuestas de consultas anteriores.
        consultaAsistenciaActual++;

        // Limpiar los resultados de la fecha anterior.
        limpiarResultadosAsistencia();

        // Permitir consultar nuevamente.
        botonConsultarAsistencia.disabled = false;

        mensajeAsistencia.className = "mensaje-panel";
        mensajeAsistencia.textContent =
            "La fecha cambió. Presione Consultar para actualizar los registros.";
    });

    botonConsultarAsistencia.addEventListener(
        "click",
        consultarAsistenciaRFID
    );

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

        // Botón para consultar estudiantes del curso.
        const botonEstudiantes = document.createElement("button");
        botonEstudiantes.type = "button";
        botonEstudiantes.className = "boton-asignacion";
        botonEstudiantes.textContent = "Ver estudiantes";
        botonEstudiantes.dataset.curso = asignacion.curso;

        botonEstudiantes.addEventListener("click", () => {
            cargarEstudiantesCurso(
                asignacion.curso,
                asignacion.asignatura
            );
        });

        const botonAsistencia = document.createElement("button");
        botonAsistencia.type = "button";
        botonAsistencia.className = "boton-asignacion";
        botonAsistencia.textContent = "Consultar asistencia";

        botonAsistencia.addEventListener("click", () => {
            mostrarSeccionAsistencia(
                asignacion.curso,
                asignacion.asignatura
            );
        });

        tarjeta.appendChild(titulo);
        tarjeta.appendChild(asignatura);
        tarjeta.appendChild(botonEstudiantes);
        tarjeta.appendChild(botonAsistencia);
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
