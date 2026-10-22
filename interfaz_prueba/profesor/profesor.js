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

        if (
            confirmacionClaseEnCurso
            || asistenciaMasivaEnCurso
            || creacionSesionEnCurso
        ) {
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

            const detalleActualizado = await abrirDetalleSesionClase(
                sesionId
            );

            if (!detalleActualizado) {
                mostrarMensajeGestionClase(
                    "El servidor confirmó la asistencia, "
                    + "pero no fue posible actualizar el detalle. "
                    + "Consulte nuevamente la sesión.",
                    "error"
                );
                return;
            }

            const detalleConfirmado = document.getElementById(
                "detalle-sesion-clase"
            );

            if (
                !detalleConfirmado
                || detalleConfirmado.hidden
                || detalleConfirmado.dataset.estado !== "confirmada"
                || Number(sesionClaseAbiertaId) !== Number(sesionId)
            ) {
                mostrarMensajeGestionClase(
                    "El servidor aceptó la confirmación, "
                    + "pero el estado actualizado de la sesión "
                    + "no coincide con lo esperado. "
                    + "Consulte nuevamente antes de continuar.",
                    "error"
                );
                return;
            }

            const listaActualizada = await consultarSesionesClase();

            if (!listaActualizada) {
                mostrarMensajeGestionClase(
                    "Asistencia confirmada correctamente, "
                    + "pero no fue posible actualizar la lista "
                    + "de sesiones. Consulte nuevamente.",
                    "error"
                );
                return;
            }

            mostrarMensajeGestionClase(
                "Asistencia confirmada correctamente. "
                + "La sesión quedó bloqueada para edición."
            );

        } catch (error) {
            mostrarMensajeGestionClase(
                "No se recibió una respuesta de confirmación. "
                + "Verificando el estado de la sesión...",
                "error"
            );

            const estadoVerificado = await abrirDetalleSesionClase(
                sesionId
            );

            if (!estadoVerificado) {
                mostrarMensajeGestionClase(
                    "No fue posible verificar el estado de la sesión. "
                    + "Consulte nuevamente antes de continuar.",
                    "error"
                );
            } else {
                const detalleVerificado = document.getElementById(
                    "detalle-sesion-clase"
                );

                if (detalleVerificado.dataset.estado === "confirmada") {
                    mostrarMensajeGestionClase(
                        "La sesión figura como confirmada en el servidor. "
                        + "Los registros quedaron bloqueados."
                    );
                } else {
                    mostrarMensajeGestionClase(
                        "Se verificó el estado de la sesión. "
                        + "Revise los registros antes de continuar."
                    );
                }
            }

        } finally {
            confirmacionClaseEnCurso = false;

            const detalleActual = document.getElementById(
                "detalle-sesion-clase"
            );

            if (
                detalleActual
                && !detalleActual.hidden
                && detalleActual.dataset.estado === "borrador"
                && Number(sesionClaseAbiertaId) === Number(sesionId)
            ) {
                recuperarControlesAsistenciaClase();
            }
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
        detalle.dataset.estado = "";
        detalle.dataset.totalAlumnos = "";
        detalle.dataset.pendientes = "";
        lista.replaceChildren();

        mostrarMensajeGestionClase(
            "Cargando asistencia de la clase..."
        );

        try {
            const { respuesta, datos } = await solicitarJSON(
                "/profesor/sesiones/" + encodeURIComponent(sesionId)
            );

            if (numeroConsulta !== consultaDetalleClaseActual) {
                return false;
            }

            if (respuesta.status === 401) {
                redirigirLogin();
                return false;
            }

            if (!respuesta.ok || datos.resultado !== "ok") {
                mostrarMensajeGestionClase(
                    datos.mensaje
                    || "No fue posible consultar la sesión.",
                    "error"
                );
                return false;
            }

            const sesion = datos.sesion;
            const alumnos = datos.alumnos || [];

            sesionClaseAbiertaId = Number(sesion.sesion_id);
            detalle.dataset.estado = sesion.estado;
            detalle.dataset.totalAlumnos = String(
                sesion.total_alumnos
            );
            detalle.dataset.pendientes = String(
                sesion.pendientes
            );

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
                const fila = document.createElement("div");
                fila.className = "fila-asistencia-estudiante";

                const estadoActual = alumno.estado || "sin_verificar";

                const estadosValidos = [
                    "presente",
                    "atrasado",
                    "no_presente"
                ];

                const estadoVisual = estadosValidos.includes(estadoActual)
                    ? estadoActual
                    : "sin_verificar";

                const nombresEstados = {
                    presente: "Presente",
                    atrasado: "Atrasado",
                    no_presente: "No presente",
                    sin_verificar: "Sin verificar"
                };

                const nombre = document.createElement("span");
                nombre.className = "nombre-estudiante-asistencia";
                nombre.textContent = alumno.nombre;

                const estado = document.createElement("span");
                estado.className =
                    "estado-estudiante-asistencia estado-" + estadoVisual;

                estado.textContent = nombresEstados[estadoVisual];

                if (sesion.estado === "borrador") {
                    const etiqueta = document.createElement("label");
                    etiqueta.className = "seleccion-estudiante-fila";

                    const casilla = document.createElement("input");
                    casilla.type = "checkbox";
                    casilla.className = "casilla-asistencia-masiva";
                    casilla.value = String(alumno.alumno_id);

                    casilla.setAttribute(
                        "aria-label",
                        "Seleccionar a " + alumno.nombre
                    );

                    etiqueta.append(casilla, nombre, estado);
                    fila.appendChild(etiqueta);

                    casilla.addEventListener("change", () => {
                        fila.classList.toggle(
                            "fila-seleccionada",
                            casilla.checked
                        );
                    });
                } else {
                    fila.append(nombre, estado);
                    fila.classList.add("fila-solo-lectura");
                }

                lista.appendChild(fila);
            }

            if (alumnos.length === 0) {
                const mensaje = document.createElement("p");
                mensaje.textContent =
                    "No hay estudiantes activos en este curso.";
                lista.appendChild(mensaje);
            }

            const seleccionarTodos = document.getElementById(
                "seleccionar-todos-asistencia"
            );

            const casillas = Array.from(
                lista.querySelectorAll(".casilla-asistencia-masiva")
            );

            const botonesMasivos = [
                document.getElementById("boton-masivo-presentes"),
                document.getElementById("boton-masivo-atrasados"),
                document.getElementById("boton-masivo-no-presentes")
            ];

            const contadorSeleccion = document.getElementById(
                "contador-seleccion-asistencia"
            );

            function actualizarSeleccionAsistencia() {
                const seleccionados = casillas.filter(
                    casilla => casilla.checked
                ).length;

                contadorSeleccion.textContent =
                    seleccionados + " estudiantes seleccionados";

                seleccionarTodos.checked =
                    casillas.length > 0
                    && seleccionados === casillas.length;

                seleccionarTodos.indeterminate =
                    seleccionados > 0
                    && seleccionados < casillas.length;

                const operacionEnCurso =
                    asistenciaMasivaEnCurso
                    || confirmacionClaseEnCurso;

                for (const boton of botonesMasivos) {
                    boton.disabled =
                        seleccionados === 0
                        || sesion.estado !== "borrador"
                        || operacionEnCurso;
                }
            }

            seleccionarTodos.disabled =
                sesion.estado !== "borrador"
                || casillas.length === 0
                || asistenciaMasivaEnCurso
                || confirmacionClaseEnCurso;

            seleccionarTodos.checked = false;
            seleccionarTodos.indeterminate = false;

            seleccionarTodos.onchange = () => {
                for (const casilla of casillas) {
                    casilla.checked = seleccionarTodos.checked;
                }

                actualizarSeleccionAsistencia();
            };

            for (const casilla of casillas) {
                casilla.addEventListener(
                    "change",
                    actualizarSeleccionAsistencia
                );
            }

            actualizarSeleccionAsistencia();

            const accionesMasivas = [
                ["boton-masivo-presentes", "presente"],
                ["boton-masivo-atrasados", "atrasado"],
                ["boton-masivo-no-presentes", "no_presente"]
            ];

            for (const [idBoton, estadoAsistencia] of accionesMasivas) {
                const botonMasivo = document.getElementById(idBoton);

                botonMasivo.onclick = async () => {
                    if (
                        asistenciaMasivaEnCurso
                        || confirmacionClaseEnCurso
                        || sesion.estado !== "borrador"
                    ) {
                        return;
                    }

                    const seleccionados = casillas
                        .filter(casilla => casilla.checked)
                        .map(casilla => Number(casilla.value));

                    if (seleccionados.length === 0) {
                        mostrarMensajeGestionClase(
                            "Seleccione al menos un estudiante.",
                            "error"
                        );
                        return;
                    }

                    await guardarAsistenciaMasivaClase(
                        sesion.sesion_id,
                        seleccionados,
                        estadoAsistencia
                    );
                };
            }

            const botonConfirmar = document.getElementById(
                "boton-confirmar-sesion-clase"
            );

            const puedeConfirmar =
                sesion.estado === "borrador"
                && sesion.total_alumnos > 0
                && sesion.pendientes === 0;

            botonConfirmar.disabled =
                !puedeConfirmar
                || asistenciaMasivaEnCurso
                || confirmacionClaseEnCurso;

            detalle.hidden = false;

            mostrarMensajeGestionClase(
                "Detalle de la sesión cargado correctamente."
            );

            detalle.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

            return true;

        } catch (error) {
            if (numeroConsulta === consultaDetalleClaseActual) {
                mostrarMensajeGestionClase(
                    "No fue posible conectar con el servidor.",
                    "error"
                );
            }

            return false;
        }
    }

    let asistenciaMasivaEnCurso = false;

    function recuperarControlesAsistenciaClase() {
        if (hayOperacionAsistenciaEnCurso()) {
            return;
        }

        if (!sesionClaseAbiertaId) {
            return;
        }

        const detalle = document.getElementById(
            "detalle-sesion-clase"
        );

        if (
            !detalle
            || detalle.hidden
            || detalle.dataset.estado !== "borrador"
        ) {
            return;
        }

        const casillas = Array.from(
            detalle.querySelectorAll(
                ".casilla-asistencia-masiva"
            )
        );

        const seleccionarTodos = document.getElementById(
            "seleccionar-todos-asistencia"
        );

        const botonesMasivos = [
            document.getElementById("boton-masivo-presentes"),
            document.getElementById("boton-masivo-atrasados"),
            document.getElementById("boton-masivo-no-presentes")
        ];

        const seleccionados = casillas.filter(
            casilla => casilla.checked
        ).length;

        for (const casilla of casillas) {
            casilla.disabled = false;
        }

        if (seleccionarTodos) {
            seleccionarTodos.disabled = casillas.length === 0;
        }

        for (const boton of botonesMasivos) {
            if (boton) {
                boton.disabled = seleccionados === 0;
            }
        }

        const botonConfirmar = document.getElementById(
            "boton-confirmar-sesion-clase"
        );

        const totalAlumnos = Number(
            detalle.dataset.totalAlumnos
        );

        const pendientes = Number(
            detalle.dataset.pendientes
        );

        const puedeConfirmar =
            Number.isInteger(totalAlumnos)
            && totalAlumnos > 0
            && Number.isInteger(pendientes)
            && pendientes === 0
            && detalle.dataset.totalAlumnos !== ""
            && detalle.dataset.pendientes !== "";

        if (botonConfirmar) {
            botonConfirmar.disabled = !puedeConfirmar;
        }
    }

    async function guardarAsistenciaMasivaClase(
        sesionId,
        alumnosIds,
        estado
    ) {
        const estadosPermitidos = [
            "presente",
            "atrasado",
            "no_presente"
        ];

        if (
            asistenciaMasivaEnCurso
            || confirmacionClaseEnCurso
            || creacionSesionEnCurso
            || !estadosPermitidos.includes(estado)
            || !tokenCSRFProfesor
            || !Array.isArray(alumnosIds)
            || alumnosIds.length === 0
            || Number(sesionClaseAbiertaId) !== Number(sesionId)
        ) {
            return;
        }

        asistenciaMasivaEnCurso = true;

        const controles = [
            "seleccionar-todos-asistencia",
            "boton-masivo-presentes",
            "boton-masivo-atrasados",
            "boton-masivo-no-presentes",
            "boton-confirmar-sesion-clase"
        ];

        for (const id of controles) {
            document.getElementById(id).disabled = true;
        }

        document.querySelectorAll(
            "#lista-asistencia-clase button, "
            + "#lista-asistencia-clase input"
        ).forEach(elemento => {
            elemento.disabled = true;
        });

        let guardados = 0;
        let fallidos = 0;
        let sesionExpirada = false;

        try {
            for (const alumnoId of alumnosIds) {
                if (Number(sesionClaseAbiertaId) !== Number(sesionId)) {
                    fallidos += alumnosIds.length - guardados - fallidos;
                    break;
                }

                mostrarMensajeGestionClase(
                    "Registrando asistencias: "
                    + (guardados + fallidos + 1)
                    + " de "
                    + alumnosIds.length
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
                        sesionExpirada = true;
                        break;
                    }

                    if (
                        respuesta.ok
                        && datos.resultado === "asistencia_guardada"
                    ) {
                        guardados++;
                    } else {
                        fallidos++;
                    }
                } catch (error) {
                    fallidos++;
                }
            }

            if (sesionExpirada) {
                redirigirLogin();
                return;
            }

            if (Number(sesionClaseAbiertaId) === Number(sesionId)) {
                await abrirDetalleSesionClase(sesionId);

                mostrarMensajeGestionClase(
                    "Registro masivo finalizado. "
                    + "Guardados: " + guardados
                    + ". Fallidos: " + fallidos + ".",
                    fallidos > 0 ? "error" : ""
                );
            }
        } finally {
            asistenciaMasivaEnCurso = false;
            recuperarControlesAsistenciaClase();
        }
    }

    async function consultarSesionesClase() {
        if (!asignacionClaseSeleccionada) {
            mostrarMensajeGestionClase(
                "Seleccione primero una asignatura.",
                "error"
            );
            return false;
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
                return false;
            }

            if (respuesta.status === 401) {
                redirigirLogin();
                return false;
            }

            if (respuesta.status === 403) {
                mostrarMensajeGestionClase(
                    "No tiene autorización para consultar "
                    + "esta asignatura.",
                    "error"
                );
                return false;
            }

            if (!respuesta.ok || datos.resultado !== "ok") {
                mostrarMensajeGestionClase(
                    "No fue posible consultar las sesiones.",
                    "error"
                );
                return false;
            }

            const sesiones = Array.isArray(datos.sesiones)
                ? datos.sesiones
                : [];

            if (sesiones.length === 0) {
                mostrarMensajeGestionClase(
                    "Esta asignatura todavía no tiene "
                    + "sesiones de asistencia registradas."
                );
                return true;
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
                    if (hayOperacionAsistenciaEnCurso()) {
                        mostrarMensajeGestionClase(
                            "Espere a que termine la operación "
                            + "antes de abrir otra sesión.",
                            "error"
                        );
                        return;
                    }

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

            return true;

        } catch (error) {
            if (numeroConsulta !== consultaSesionesActual) {
                return false;
            }

            mostrarMensajeGestionClase(
                "No fue posible conectar con el servidor.",
                "error"
            );

            return false;

        } finally {
            if (numeroConsulta === consultaSesionesActual) {
                botonConsultarSesionesClase.disabled = false;
            }
        }
    }

    let creacionSesionEnCurso = false;

    async function crearSesionClase() {
        if (creacionSesionEnCurso || hayOperacionAsistenciaEnCurso()) {
            mostrarMensajeGestionClase(
                "Espere a que finalice la operación actual.",
                "error"
            );
            return;
        }

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

        creacionSesionEnCurso = true;
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
            creacionSesionEnCurso = false;
            botonCrearSesionClase.disabled =
                !asignacionClaseSeleccionada;
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


    /* ==========================================
       SELECTORES DE CURSO Y ASIGNATURA
       ========================================== */

    const selectorCurso = document.getElementById("selector-curso");
    const selectorAsignatura = document.getElementById("selector-asignatura");

    const botonVerEstudiantesCurso = document.getElementById(
        "boton-ver-estudiantes-curso"
    );

    const botonVerRFIDCurso = document.getElementById(
        "boton-ver-rfid-curso"
    );

    const botonGestionarClase = document.getElementById(
        "boton-gestionar-clase"
    );

    let asignacionesDisponibles = [];

    function obtenerAsignacionSeleccionada() {
        const asignacionId = Number(selectorAsignatura.value);

        return asignacionesDisponibles.find(
            (asignacion) => asignacion.asignacion_id === asignacionId
        ) || null;
    }

    function actualizarBotonesAsignacion() {
        const asignacion = obtenerAsignacionSeleccionada();
        const disponible = asignacion !== null;

        botonVerEstudiantesCurso.disabled = !disponible;
        botonVerRFIDCurso.disabled = !disponible;
        botonGestionarClase.disabled = !disponible;
    }

    function hayOperacionAsistenciaEnCurso() {
        return asistenciaMasivaEnCurso
            || confirmacionClaseEnCurso
            || creacionSesionEnCurso;
    }

    function limpiarSeccionesAsignacion() {
        seccionEstudiantes.hidden = true;
        seccionAsistencia.hidden = true;
        seccionGestionClase.hidden = true;

        // Limpiar la asignación y sesión de clase anteriores.
        asignacionClaseSeleccionada = null;
        sesionClaseAbiertaId = null;

        document.getElementById(
            "detalle-sesion-clase"
        ).hidden = true;

        listaSesionesClase.replaceChildren();
        listaSesionesClase.hidden = true;

        // Invalidar consultas anteriores.
        consultaEstudiantesActual++;
        consultaAsistenciaActual++;
        consultaSesionesActual++;
        consultaDetalleClaseActual++;

        limpiarResultadosAsistencia();
    }

    let cursoSeleccionadoAnterior = "";
    let asignaturaSeleccionadaAnterior = "";

    selectorCurso.addEventListener("change", () => {
        if (hayOperacionAsistenciaEnCurso()) {
            selectorCurso.value = cursoSeleccionadoAnterior;

            mostrarMensajeGestionClase(
                "Espere a que termine el registro de asistencia "
                + "antes de cambiar de curso.",
                "error"
            );
            return;
        }

        const curso = selectorCurso.value;
        cursoSeleccionadoAnterior = curso;
        asignaturaSeleccionadaAnterior = "";

        limpiarSeccionesAsignacion();

        selectorAsignatura.replaceChildren();

        const opcionInicial = document.createElement("option");
        opcionInicial.value = "";
        opcionInicial.textContent = "Seleccione una asignatura";

        selectorAsignatura.appendChild(opcionInicial);

        const asignaturas = asignacionesDisponibles.filter(
            (asignacion) => asignacion.curso === curso
        );

        asignaturas.forEach((asignacion) => {
            const opcion = document.createElement("option");

            opcion.value = String(asignacion.asignacion_id);
            opcion.textContent = asignacion.asignatura;

            selectorAsignatura.appendChild(opcion);
        });

        selectorAsignatura.disabled = asignaturas.length === 0;

        actualizarBotonesAsignacion();
    });

    selectorAsignatura.addEventListener("change", () => {
        if (hayOperacionAsistenciaEnCurso()) {
            selectorAsignatura.value =
                asignaturaSeleccionadaAnterior;

            mostrarMensajeGestionClase(
                "Espere a que termine el registro de asistencia "
                + "antes de cambiar de asignatura.",
                "error"
            );
            return;
        }

        asignaturaSeleccionadaAnterior = selectorAsignatura.value;

        limpiarSeccionesAsignacion();
        actualizarBotonesAsignacion();
    });

    botonVerEstudiantesCurso.addEventListener("click", () => {
        const asignacion = obtenerAsignacionSeleccionada();

        if (!asignacion) return;

        cargarEstudiantesCurso(
            asignacion.curso,
            asignacion.asignatura
        );
    });

    botonVerRFIDCurso.addEventListener("click", () => {
        const asignacion = obtenerAsignacionSeleccionada();

        if (!asignacion) return;

        mostrarSeccionAsistencia(
            asignacion.curso,
            asignacion.asignatura
        );
    });

    botonGestionarClase.addEventListener("click", () => {
        const asignacion = obtenerAsignacionSeleccionada();

        if (!asignacion) return;

        seleccionarGestionClase(asignacion);
    });

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

        asignacionesDisponibles = Array.isArray(datos.asignaciones)
            ? datos.asignaciones
            : [];

        selectorCurso.replaceChildren();
        selectorAsignatura.replaceChildren();

        const opcionCurso = document.createElement("option");
        opcionCurso.value = "";
        opcionCurso.textContent = "Seleccione un curso";
        selectorCurso.appendChild(opcionCurso);

        const opcionAsignatura = document.createElement("option");
        opcionAsignatura.value = "";
        opcionAsignatura.textContent = "Seleccione una asignatura";
        selectorAsignatura.appendChild(opcionAsignatura);

        const cursos = [
            ...new Set(
                asignacionesDisponibles.map(
                    (asignacion) => asignacion.curso
                )
            )
        ];

        cursos.forEach((curso) => {
            const opcion = document.createElement("option");

            opcion.value = curso;
            opcion.textContent = curso;

            selectorCurso.appendChild(opcion);
        });

        selectorCurso.disabled = cursos.length === 0;
        selectorAsignatura.disabled = true;

        actualizarBotonesAsignacion();

        mostrarMensajePanel(
            cursos.length === 0
                ? "No tiene cursos o asignaturas asignados."
                : "Seleccione un curso y una asignatura para continuar."
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
