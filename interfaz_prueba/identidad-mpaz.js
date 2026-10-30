/* MPAZ IDENTIDAD V1: preferencias visuales locales. No realiza solicitudes a la API. */
(function () {
    "use strict";

    const KEY = "mpaz:preferencias:visual:v1";
    const raiz = document.documentElement;
    const defaults = {
        oscuro: false,
        compacto: false,
        letra_grande: false,
        reducir_movimiento: false
    };
    let opciones = { ...defaults };

    try {
        const guardadas = JSON.parse(localStorage.getItem(KEY) || "{}");
        opciones.oscuro = guardadas.oscuro === true;
        opciones.compacto = guardadas.compacto === true;
        opciones.letra_grande = guardadas.letra_grande === true;
        opciones.reducir_movimiento =
            guardadas.reducir_movimiento === true;
    } catch (_) {
        // Preferencias del navegador deshabilitadas: usar valores iniciales.
    }

    function guardar() {
        try {
            localStorage.setItem(KEY, JSON.stringify(opciones));
            return true;
        } catch (_) {
            return false;
        }
    }

    function aplicar() {
        raiz.dataset.mpazTema = opciones.oscuro ? "oscuro" : "claro";
        raiz.dataset.mpazDensidad =
            opciones.compacto ? "compacta" : "normal";
        raiz.dataset.mpazLectura =
            opciones.letra_grande ? "ampliada" : "normal";
        raiz.dataset.mpazMovimiento =
            opciones.reducir_movimiento ? "reducido" : "normal";
        raiz.style.colorScheme = opciones.oscuro ? "dark" : "light";

        document.querySelectorAll('[data-mpaz-ajuste="oscuro"]').forEach(function (control) {
            control.checked = opciones.oscuro;
        });
        document.querySelectorAll(
            '[data-mpaz-ajuste="letra_grande"]'
        ).forEach(function (control) {
            control.checked = opciones.letra_grande;
        });
        document.querySelectorAll(
            '[data-mpaz-ajuste="reducir_movimiento"]'
        ).forEach(function (control) {
            control.checked = opciones.reducir_movimiento;
        });
        document.querySelectorAll('[data-mpaz-ajuste="compacto"]').forEach(function (control) {
            control.checked = opciones.compacto;
        });
        document.querySelectorAll("[data-mpaz-tema-toggle]").forEach(function (boton) {
            boton.setAttribute("aria-pressed", String(opciones.oscuro));
            boton.setAttribute("aria-label", opciones.oscuro ? "Activar tema claro" : "Activar tema oscuro");
            boton.innerHTML = opciones.oscuro
                ? '☀ <span>Modo claro</span>'
                : '☾ <span>Modo oscuro</span>';
        });
    }

    function mensaje(texto) {
        document.querySelectorAll(".mpaz-ajustes-estado").forEach(function (elemento) {
            elemento.textContent = texto;
        });
    }

    aplicar();

    document.addEventListener("change", function (evento) {
        const control = evento.target.closest("[data-mpaz-ajuste]");
        if (!control) return;
        const clave = control.dataset.mpazAjuste;
        if (![
            "oscuro", "compacto",
            "letra_grande", "reducir_movimiento"
        ].includes(clave)) return;
        opciones[clave] = control.checked;
        const guardado = guardar();
        aplicar();
        mensaje(guardado ? "Preferencia guardada en este navegador." : "Cambio aplicado para esta visita.");
    });

    document.addEventListener("click", function (evento) {
        const restaurar = evento.target.closest("[data-mpaz-restablecer]");
        if (restaurar) {
            opciones = { ...defaults };
            guardar();
            aplicar();
            mensaje("Vista restablecida.");
            return;
        }
        if (evento.target.closest("[data-mpaz-tema-toggle]")) {
            opciones.oscuro = !opciones.oscuro;
            guardar();
            aplicar();
            return;
        }
        // Cerrar menu de preferencias al hacer clic fuera.
        document.querySelectorAll("details.menu-configuracion[open]").forEach(function (detalle) {
            if (!detalle.contains(evento.target)) detalle.open = false;
        });
    });

    document.addEventListener("keydown", function (evento) {
        if (evento.key !== "Escape") return;
        document.querySelectorAll("details.menu-configuracion[open]").forEach(function (detalle) {
            detalle.open = false;
            const resumen = detalle.querySelector("summary");
            if (resumen) resumen.focus();
        });
    });
})();
