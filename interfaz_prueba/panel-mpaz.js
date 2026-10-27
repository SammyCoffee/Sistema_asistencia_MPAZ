
(function () {
    "use strict";

    const menu = document.querySelector(".menu-principal");
    const contenido = document.querySelector("main.contenido");
    const bienvenida = document.getElementById("mpaz-bienvenida");

    if (!menu || !contenido || !bienvenida) {
        return;
    }

    const secciones = [
        "inicio",
        "estudiantes",
        "tarjetas",
        "vinculacion",
        "asistencias",
        "inasistencias",
        "atrasos",
        "analisis",
        "calendario",
        "reportes"
    ];

    const fecha = document.getElementById("mpaz-fecha-actual");

    if (fecha) {
        fecha.textContent = new Intl.DateTimeFormat("es-CL", {
            dateStyle: "full"
        }).format(new Date());
    }

    // Evitar tablas interminables.
    contenido.querySelectorAll(".tabla-lecturas")
        .forEach(function (tabla) {
            if (tabla.parentElement.classList.contains(
                "mpaz-tabla-scroll"
            )) {
                return;
            }

            const contenedor = document.createElement("div");
            contenedor.className = "mpaz-tabla-scroll";

            tabla.parentNode.insertBefore(contenedor, tabla);
            contenedor.appendChild(tabla);
        });

    const tarjetasResumen = contenido.querySelectorAll(
        ":scope > .tarjeta-resumen"
    );

    function mostrarSeccion() {
        let vista = decodeURIComponent(
            window.location.hash.replace("#", "")
        );

        if (!secciones.includes(vista)) {
            vista = "inicio";
        }

        document.body.dataset.mpazVista = vista;

        bienvenida.hidden = vista !== "inicio";

        tarjetasResumen.forEach(function (tarjeta) {
            tarjeta.hidden = vista !== "inicio";
        });

        secciones.forEach(function (nombre) {
            if (nombre === "inicio") {
                return;
            }

            const seccion = document.getElementById(nombre);

            if (seccion) {
                seccion.hidden = nombre !== vista;
            }
        });

        menu.querySelectorAll("a").forEach(function (enlace) {
            const activo = enlace.getAttribute("href") ===
                "#" + vista;

            enlace.classList.toggle("menu-activo", activo);

            if (activo) {
                enlace.setAttribute("aria-current", "page");
            } else {
                enlace.removeAttribute("aria-current");
            }
        });

        window.scrollTo({top: 0, behavior: "instant"});
    }

    // Abrir formulario antes de ejecutar la edición existente.
    document.addEventListener("click", function (evento) {
        if (!evento.target.closest(".boton-editar-estudiante")) {
            return;
        }

        const formulario = document.getElementById(
            "mpaz-formulario-plegable"
        );

        if (formulario) {
            formulario.open = true;
        }
    }, true);

    window.addEventListener("hashchange", mostrarSeccion);

    mostrarSeccion();
})();


/* ==========================================
   MPAZ-VISTAS-627
   BARRA COMPACTA Y SELECTOR DE MÓDULOS
   ========================================== */

(function () {
    "use strict";

    const controlesOriginales = document.querySelector(
        ".encabezado .acciones-cabecera"
    );

    const destino = document.getElementById(
        "mpaz-acciones-admin"
    );

    const selector = document.getElementById(
        "mpaz-selector-vista"
    );

    const volver = document.getElementById(
        "mpaz-volver-panel"
    );

    if (!controlesOriginales || !destino || !selector || !volver) {
        console.error("No se pudo preparar la navegación MPAZ.");
        return;
    }

    // Mover los botones existentes, sin duplicarlos.
    // El cierre de sesión conserva sus eventos originales.
    destino.appendChild(controlesOriginales);

    const enlacePortal = destino.querySelector(
        ".boton-volver-inicio"
    );

    if (enlacePortal) {
        enlacePortal.textContent = "Cambiar portal";
    }

    function sincronizarVista() {
        const solicitada = window.location.hash
            .replace("#", "");

        const opciones = Array.from(selector.options)
            .map(opcion => opcion.value);

        const vista = opciones.includes(solicitada)
            ? solicitada
            : "inicio";

        selector.value = vista;
        volver.hidden = vista === "inicio";
    }

    selector.addEventListener("change", function () {
        window.location.hash = "#" + selector.value;
    });

    window.addEventListener(
        "hashchange",
        sincronizarVista
    );

    sincronizarVista();
})();
