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

    let tokenCSRFProfesor = null;

    async function verificarSesion() {

        const { respuesta, datos } = await solicitarJSON(
            "/profesor/sesion"
        );

        if (!respuesta.ok || datos.resultado !== "ok") {
            tokenCSRFProfesor = null;
            return null;
        }

        tokenCSRFProfesor = datos.csrf_token || null;

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


    /* ==========================================
       GESTIÓN DE ASISTENCIA EN CLASE
       ========================================== */

    const seccionGestionClase = document.getElementById(
        "seccion-gestion-clase"
    );

    const tituloGestionClase = document.getElementById(
        "titulo-gestion-clase"
    );

    const descripcionGestionClase = document.getElementById(
        "descripcion-gestion-clase"
    );

    const mensajeGestionClase = document.getElementById(
        "mensaje-gestion-clase"
    );

    const listaSesionesClase = document.getElementById(
        "lista-sesiones-clase"
    );

    const botonConsultarSesionesClase = document.getElementById(
        "boton-consultar-sesiones-clase"
    );

    const botonCrearSesionClase = document.getElementById(
        "boton-crear-sesion-clase"
    );

    const fechaSesionClase = document.getElementById(
        "fecha-sesion-clase"
    );

    const horaSesionClase = document.getElementById(
        "hora-sesion-clase"
    );

    let asignacionClaseSeleccionada = null;
    let consultaSesionesActual = 0;

    function mostrarMensajeGestionClase(mensaje, tipo = "") {
        mensajeGestionClase.textContent = mensaje;
        mensajeGestionClase.className = "mensaje-panel " + tipo;
    }

    function seleccionarGestionClase(asignacion) {
        consultaSesionesActual++;

        asignacionClaseSeleccionada = asignacion;
        sesionClaseAbiertaId = null;
        consultaDetalleClaseActual++;

        seccionGestionClase.hidden = false;

        tituloGestionClase.textContent =
            "Verificación de asistencia - Curso "
            + asignacion.curso;

        descripcionGestionClase.textContent =
            "Asignatura: " + asignacion.asignatura;

        listaSesionesClase.replaceChildren();
        listaSesionesClase.hidden = true;

        document.getElementById(
            "detalle-sesion-clase"
        ).hidden = true;

        botonConsultarSesionesClase.disabled = false;

        // La creación requiere una asignación docente seleccionada.
        botonCrearSesionClase.disabled = false;

        if (!fechaSesionClase.value) {
            fechaSesionClase.value =
                new Date().toLocaleDateString("en-CA");
        }

        if (!horaSesionClase.value) {
            const ahora = new Date();

            horaSesionClase.value =
                String(ahora.getHours()).padStart(2, "0")
                + ":"
                + String(ahora.getMinutes()).padStart(2, "0");
        }

        mostrarMensajeGestionClase(
            "Asignatura seleccionada. "
            + "Puede consultar sus sesiones anteriores."
        );

        seccionGestionClase.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }

    async function guardarAsistenciaAlumnoClase(
        sesionId,
        alumnoId,
        estado,
        boton
    ) {
        const estadosPermitidos = [
            "presente",
            "atrasado",
            "no_presente"
        ];

        if (!estadosPermitidos.includes(estado)) {
            mostrarMensajeGestionClase(
                "Estado de asistencia no válido.",
                "error"
            );
            return;
        }

        if (!tokenCSRFProfesor) {
            mostrarMensajeGestionClase(
                "No se pudo verificar la sesión docente. "
                + "Vuelva a iniciar sesión.",
                "error"
            );
            return;
        }

        boton.disabled = true;

        mostrarMensajeGestionClase(
            "Guardando asistencia del estudiante..."
        );

        try {
            const { respuesta, datos } = await solicitarJSON(
                "/profesor/sesiones/"
                + encodeURIComponent(sesionId)
                + "/asistencia",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRF-Token": tokenCSRFProfesor
                    },
                    body: JSON.stringify({
                        alumno_id: alumnoId,
                        estado: estado
                    })
                }
            );

            if (respuesta.status === 401) {
                redirigirLogin();
                return;
            }

            if (!respuesta.ok) {
                mostrarMensajeGestionClase(
                    datos.mensaje
                    || "No fue posible guardar la asistencia.",
                    "error"
                );
                return;
            }

            if (datos.resultado !== "asistencia_guardada") {
                mostrarMensajeGestionClase(
                    "El servidor no confirmó el registro.",
                    "error"
                );
                return;
            }

            await abrirDetalleSesionClase(sesionId);

            mostrarMensajeGestionClase(
                "Asistencia guardada correctamente."
            );

        } catch (error) {
            mostrarMensajeGestionClase(
                "Error de conexión al guardar la asistencia.",
                "error"
            );

        } finally {
            boton.disabled = false;
        }
    }

    let sesionClaseAbiertaId = null;
    let confirmacionClaseEnCurso = false;

    document.getElementById(
        "boton-confirmar-sesion-clase"
    ).addEventListener(
        "click",
        confirmarAsistenciaSesionClase
    );

    async function confirmarAsistenciaSesionClase() {
        const sesionId = sesionClaseAbiertaId;

        if (!Number.isInteger(sesionId) || sesionId <= 0) {
            mostrarMensajeGestionClase(
                "Primero debe abrir una sesión de clase.",
                "error"
            );
            return;
        }

        if (confirmacionClaseEnCurso) {
            return;
        }

        if (!tokenCSRFProfesor) {
            mostrarMensajeGestionClase(
                "La sesión docente no tiene un token válido. "
                + "Vuelva a iniciar sesión.",
                "error"
            );
            return;
        }

        const boton = document.getElementById(
            "boton-confirmar-sesion-clase"
        );

        if (boton.disabled) {
            return;
        }

        const aceptado = window.confirm(
            "¿Desea confirmar definitivamente la asistencia? "
            + "Después de confirmar no podrá modificar "
            + "los registros de esta sesión."
        );

        if (!aceptado) {
            return;
        }

        confirmacionClaseEnCurso = true;
        boton.disabled = true;

        mostrarMensajeGestionClase(
            "Confirmando asistencia de la clase..."
        );

        try {
            const { respuesta, datos } = await solicitarJSON(
                "/profesor/sesiones/"
                + encodeURIComponent(sesionId)
                + "/confirmar",
                {
                    method: "POST",
                    headers: {
                        "X-CSRF-Token": tokenCSRFProfesor
                    }
                }
            );

            if (respuesta.status === 401) {
                redirigirLogin();
                return;
            }

            if (
                !respuesta.ok
                || datos.resultado !== "sesion_confirmada"
            ) {
                mostrarMensajeGestionClase(
                    datos.mensaje
                    || "No fue posible confirmar la asistencia.",
                    "error"
                );

                await abrirDetalleSesionClase(sesionId);
                return;
            }

            await abrirDetalleSesionClase(sesionId);

            mostrarMensajeGestionClase(
                "Asistencia confirmada correctamente. "
                + "La sesión quedó bloqueada para edición."
            );

            await consultarSesionesClase();

        } catch (error) {
            mostrarMensajeGestionClase(
                "No se pudo completar la confirmación. "
                + "Consulte nuevamente el estado de la sesión.",
                "error"
            );

        } finally {
            confirmacionClaseEnCurso = false;
        }
    }

    let consultaDetalleClaseActual = 0;

    async function abrirDetalleSesionClase(sesionId) {
        const numeroConsulta = ++consultaDetalleClaseActual;

        const detalle = document.getElementById(
            "detalle-sesion-clase"
        );

        const lista = document.getElementById(
            "lista-asistencia-clase"
        );

        detalle.hidden = true;
        lista.replaceChildren();

        mostrarMensajeGestionClase(
            "Cargando asistencia de la clase..."
        );

        try {
            const { respuesta, datos } = await solicitarJSON(
                "/profesor/sesiones/" + encodeURIComponent(sesionId)
            );

            if (numeroConsulta !== consultaDetalleClaseActual) {
                return;
            }

            if (respuesta.status === 401) {
                redirigirLogin();
                return;
            }

            if (!respuesta.ok || datos.resultado !== "ok") {
                mostrarMensajeGestionClase(
                    datos.mensaje
                    || "No fue posible consultar la sesión.",
                    "error"
                );
                return;
            }

            const sesion = datos.sesion;
            const alumnos = datos.alumnos || [];

            sesionClaseAbiertaId = Number(sesion.sesion_id);

            document.getElementById(
                "titulo-detalle-sesion"
            ).textContent =
                "Asistencia - "
                + sesion.curso
                + " - "
                + sesion.asignatura;

            document.getElementById(
                "estado-sesion-clase"
            ).textContent =
                "Fecha: " + sesion.fecha
                + " | Hora: " + sesion.hora_inicio
                + " | Estado: " + sesion.estado;

            document.getElementById(
                "total-alumnos-clase"
            ).textContent = sesion.total_alumnos;

            document.getElementById(
                "registrados-clase"
            ).textContent = sesion.registrados;

            document.getElementById(
                "pendientes-clase"
            ).textContent = sesion.pendientes;

            for (const alumno of alumnos) {
                const tarjeta = document.createElement("article");
                tarjeta.className = "tarjeta-estudiante";

                const nombre = document.createElement("strong");
                nombre.textContent = alumno.nombre;

                const estado = document.createElement("p");

                estado.textContent =
                    "Estado: "
                    + alumno.estado.replaceAll("_", " ");

                tarjeta.append(nombre, estado);

                if (sesion.estado === "borrador") {
                    const controles = document.createElement("div");
                    controles.className = "controles-asistencia";

                    const opciones = [
                        ["Presente", "presente"],
                        ["Atrasado", "atrasado"],
                        ["No presente", "no_presente"]
                    ];

                    for (const [etiqueta, valor] of opciones) {
                        const boton = document.createElement("button");

                        boton.type = "button";
                        boton.className = "boton-asignacion";
                        boton.textContent = etiqueta;

                        if (alumno.estado === valor) {
                            boton.setAttribute(
                                "aria-pressed",
                                "true"
                            );
                        }

                        boton.addEventListener("click", () => {
                            guardarAsistenciaAlumnoClase(
                                sesion.sesion_id,
                                alumno.alumno_id,
                                valor,
                                boton
                            );
                        });

                        controles.appendChild(boton);
                    }

                    tarjeta.appendChild(controles);
                }

                lista.appendChild(tarjeta);
            }

            if (alumnos.length === 0) {
                const mensaje = document.createElement("p");
                mensaje.textContent =
                    "No hay estudiantes activos en este curso.";
                lista.appendChild(mensaje);
            }

            document.getElementById(
                "boton-todos-presentes"
            ).disabled = true;

            const botonConfirmar = document.getElementById(
                "boton-confirmar-sesion-clase"
            );

            const puedeConfirmar =
                sesion.estado === "borrador"
                && sesion.total_alumnos > 0
                && sesion.pendientes === 0;

            botonConfirmar.disabled = !puedeConfirmar;

            detalle.hidden = false;

            mostrarMensajeGestionClase(
                "Detalle de la sesión cargado correctamente."
            );

            detalle.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        } catch (error) {
            if (numeroConsulta === consultaDetalleClaseActual) {
                mostrarMensajeGestionClase(
                    "No fue posible conectar con el servidor.",
                    "error"
                );
            }
        }
    }

    async function consultarSesionesClase() {
        if (!asignacionClaseSeleccionada) {
            mostrarMensajeGestionClase(
                "Seleccione primero una asignatura.",
                "error"
            );
            return;
        }

        const numeroConsulta = ++consultaSesionesActual;
        const asignacionId = asignacionClaseSeleccionada.asignacion_id;

        listaSesionesClase.replaceChildren();
        listaSesionesClase.hidden = true;

        botonConsultarSesionesClase.disabled = true;

        mostrarMensajeGestionClase(
            "Consultando sesiones de clase..."
        );

        try {
            const ruta = "/profesor/asignaciones/"
                + encodeURIComponent(asignacionId)
                + "/sesiones";

            const { respuesta, datos } = await solicitarJSON(ruta);

            if (numeroConsulta !== consultaSesionesActual) {
                return;
            }

            if (respuesta.status === 401) {
                redirigirLogin();
                return;
            }

            if (respuesta.status === 403) {
                mostrarMensajeGestionClase(
                    "No tiene autorización para consultar "
                    + "esta asignatura.",
                    "error"
                );
                return;
            }

            if (!respuesta.ok || datos.resultado !== "ok") {
                mostrarMensajeGestionClase(
                    "No fue posible consultar las sesiones.",
                    "error"
                );
                return;
            }

            const sesiones = Array.isArray(datos.sesiones)
                ? datos.sesiones
                : [];

            if (sesiones.length === 0) {
                mostrarMensajeGestionClase(
                    "Esta asignatura todavía no tiene "
                    + "sesiones de asistencia registradas."
                );
                return;
            }

            const lista = document.createElement("ol");

            sesiones.forEach((sesion) => {
                const elemento = document.createElement("li");

                const fecha = sesion.fecha || "Sin fecha";
                const hora = sesion.hora_inicio || "--:--";
                const estado = sesion.estado || "desconocido";

                const registrados = Number(
                    sesion.registrados ?? 0
                );

                const pendientes = Number(
                    sesion.pendientes ?? 0
                );

                elemento.textContent =
                    fecha + " · " + hora
                    + " · " + estado
                    + " · Registrados: " + registrados
                    + " · Sin verificar: " + pendientes;

                const botonAbrir = document.createElement("button");
                botonAbrir.type = "button";
                botonAbrir.className = "boton-asignacion";
                botonAbrir.textContent = "Abrir sesión";

                botonAbrir.addEventListener("click", () => {
                    abrirDetalleSesionClase(sesion.sesion_id);
                });

                elemento.appendChild(botonAbrir);

                lista.appendChild(elemento);
            });

            listaSesionesClase.appendChild(lista);
            listaSesionesClase.hidden = false;

            mostrarMensajeGestionClase(
                "Sesiones encontradas: " + sesiones.length
            );

        } catch (error) {
            if (numeroConsulta !== consultaSesionesActual) {
                return;
            }

            mostrarMensajeGestionClase(
                "No fue posible conectar con el servidor.",
                "error"
            );

        } finally {
            if (numeroConsulta === consultaSesionesActual) {
                botonConsultarSesionesClase.disabled = false;
            }
        }
    }

    async function crearSesionClase() {
        if (!asignacionClaseSeleccionada) {
            mostrarMensajeGestionClase(
                "Seleccione primero una asignatura.",
                "error"
            );
            return;
        }

        if (!tokenCSRFProfesor) {
            mostrarMensajeGestionClase(
                "No se pudo verificar la sesión docente. "
                + "Vuelva a iniciar sesión.",
                "error"
            );
            return;
        }

        const asignacionId =
            asignacionClaseSeleccionada.asignacion_id;

        const fecha = fechaSesionClase.value;
        const horaInicio = horaSesionClase.value;

        if (!fecha || !horaInicio) {
            mostrarMensajeGestionClase(
                "Debe indicar la fecha y hora de la clase.",
                "error"
            );
            return;
        }

        botonCrearSesionClase.disabled = true;

        mostrarMensajeGestionClase(
            "Creando sesión de clase..."
        );

        try {
            const { respuesta, datos } = await solicitarJSON(
                "/profesor/sesiones",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRF-Token": tokenCSRFProfesor
                    },
                    body: JSON.stringify({
                        asignacion_id: asignacionId,
                        fecha: fecha,
                        hora_inicio: horaInicio
                    })
                }
            );

            if (respuesta.status === 401) {
                redirigirLogin();
                return;
            }

            if (respuesta.status === 403) {
                mostrarMensajeGestionClase(
                    "No tiene autorización para crear "
                    + "sesiones en esta asignatura.",
                    "error"
                );
                return;
            }

            if (!respuesta.ok) {
                mostrarMensajeGestionClase(
                    datos.mensaje
                    || "No fue posible crear la sesión.",
                    "error"
                );
                return;
            }

            const mensajeCreacion =
                datos.resultado === "sesion_existente"
                    ? "La sesión ya estaba registrada."
                    : "Sesión de clase creada correctamente.";

            await consultarSesionesClase();

            mostrarMensajeGestionClase(mensajeCreacion);

        } catch (error) {
            mostrarMensajeGestionClase(
                "No fue posible conectar con el servidor.",
                "error"
            );
        } finally {
            botonCrearSesionClase.disabled = false;
        }
    }

    botonCrearSesionClase.addEventListener(
        "click",
        crearSesionClase
    );

    botonConsultarSesionesClase.addEventListener(
        "click",
        consultarSesionesClase
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

        boton.disabled = false;
        boton.title = "Verificar asistencia en clase";

        boton.addEventListener("click", () => {
            seleccionarGestionClase(asignacion);
        });

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
