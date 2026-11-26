(() => {
    "use strict";

    const ruta = "/panel/sesiones-docentes";
    const formulario = document.getElementById("filtros-sesiones-docentes");
    const resultados = document.getElementById("resultados-sesiones-docentes");
    const filas = document.getElementById("filas-sesiones-docentes");
    const mensaje = document.getElementById("mensaje-sesiones-docentes");
    const detalle = document.getElementById("detalle-sesion-docente");
    const datosDetalle = document.getElementById("datos-detalle-docente");
    const mensajeDetalle = document.getElementById("mensaje-detalle-docente");
    const paginacion = document.getElementById("paginacion-sesiones-docentes");
    const anterior = document.getElementById("sesiones-docentes-anterior");
    const siguiente = document.getElementById("sesiones-docentes-siguiente");

    const estados = { borrador: "Borrador", confirmada: "Confirmada", anulada: "Anulada" };
    const columnas = [
        ["Fecha", s => s.fecha], ["Hora", s => s.hora_inicio],
        ["Curso", s => s.curso], ["Asignatura", s => s.asignatura],
        ["Docente", s => s.profesor], ["Estado", s => estados[s.estado]],
        ["Presentes", s => s.presentes], ["Atrasados", s => s.atrasados],
        ["No presentes", s => s.no_presentes], ["Pendientes", s => s.pendientes],
    ];

    let pagina = 1;
    let filtros = new URLSearchParams();
    let solicitudLista = 0;
    let solicitudDetalle = 0;

    async function consultar(url) {
        let respuesta;
        try {
            respuesta = await fetch(url, { cache: "no-store", credentials: "same-origin" });
        } catch {
            throw new Error("No hay conexión con el servidor. Vuelva a intentar.");
        }
        const errores = {
            400: "Revise los filtros de búsqueda.",
            401: "La sesión administrativa expiró. Vuelva a iniciar sesión.",
            403: "Su cuenta no tiene permiso para consultar sesiones docentes.",
            404: "La sesión solicitada ya no está disponible.",
        };
        if (!respuesta.ok) {
            throw new Error(errores[respuesta.status] || "El servicio de sesiones docentes no está disponible.");
        }
        try {
            const datos = await respuesta.json();
            if (datos?.resultado !== "ok") throw new Error();
            return datos;
        } catch {
            throw new Error("El servicio devolvió una respuesta inesperada.");
        }
    }

    async function abrirDetalle(id) {
        const solicitud = ++solicitudDetalle;
        detalle.hidden = true;
        datosDetalle.replaceChildren();
        mensajeDetalle.textContent = "Cargando detalle…";
        try {
            const { sesion } = await consultar(ruta + "/" + encodeURIComponent(id));
            if (solicitud !== solicitudDetalle) return;
            for (const [etiqueta, leer] of [
                ...columnas, ["Confirmación (UTC)", s => s.fecha_confirmacion],
            ]) {
                const termino = document.createElement("dt");
                const valor = document.createElement("dd");
                termino.textContent = etiqueta;
                valor.textContent = leer(sesion) ?? "—";
                const campo = document.createElement("div");
                campo.append(termino, valor);
                datosDetalle.appendChild(campo);
            }
            mensajeDetalle.textContent = "";
            detalle.hidden = false;
            document.getElementById("titulo-detalle-docente").focus();
        } catch (error) {
            if (solicitud === solicitudDetalle) mensajeDetalle.textContent = error.message;
        }
    }

    async function listar(nuevaPagina) {
        const solicitud = ++solicitudLista;
        ++solicitudDetalle;
        detalle.hidden = true;
        datosDetalle.replaceChildren();
        mensajeDetalle.textContent = "";
        resultados.hidden = true;
        filas.replaceChildren();
        mensaje.textContent = "Consultando sesiones docentes…";
        const consulta = new URLSearchParams(filtros);
        consulta.set("pagina", nuevaPagina);
        try {
            const datos = await consultar(ruta + "?" + consulta);
            if (solicitud !== solicitudLista) return;
            pagina = datos.pagina;
            for (const sesion of datos.sesiones) {
                const fila = filas.insertRow();
                for (const [, leer] of columnas) {
                    fila.insertCell().textContent = leer(sesion) ?? "—";
                }
                const boton = document.createElement("button");
                boton.type = "button";
                boton.textContent = "Ver detalle";
                boton.setAttribute("aria-label", "Ver detalle de " + sesion.curso + " del " + sesion.fecha + " a las " + sesion.hora_inicio);
                boton.addEventListener("click", () => abrirDetalle(sesion.sesion_id));
                fila.insertCell().appendChild(boton);
            }
            resultados.hidden = !datos.sesiones.length && pagina === 1;
            paginacion.hidden = pagina === 1 && !datos.hay_siguiente;
            anterior.disabled = pagina <= 1;
            siguiente.disabled = !datos.hay_siguiente;
            mensaje.textContent = datos.sesiones.length
                ? "Página " + pagina + ". Pendientes de borrador según la nómina activa."
                : "No hay sesiones docentes para los filtros seleccionados.";
        } catch (error) {
            if (solicitud === solicitudLista) mensaje.textContent = error.message;
        }
    }

    function buscar() {
        filtros = new URLSearchParams(new FormData(formulario));
        listar(1);
    }

    formulario.addEventListener("submit", evento => {
        evento.preventDefault();
        buscar();
    });
    anterior.addEventListener("click", () => listar(pagina - 1));
    siguiente.addEventListener("click", () => listar(pagina + 1));

    function alCambiarVista() {
        if (location.hash === "#sesiones-docentes") buscar();
    }
    window.addEventListener("hashchange", alCambiarVista);
    alCambiarVista();
})();
