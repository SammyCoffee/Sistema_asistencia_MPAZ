/* Fechas y horas por defecto en la zona escolar, no la del navegador. */
(function () {
    "use strict";
    window.MPAZTiempo = {
        fecha(instante = new Date()) {
            return new Intl.DateTimeFormat("en-CA", {
                timeZone: "America/Santiago", year: "numeric", month: "2-digit", day: "2-digit"
            }).format(instante);
        },
        hora(instante = new Date()) {
            return new Intl.DateTimeFormat("en-GB", {
                timeZone: "America/Santiago", hour: "2-digit", minute: "2-digit", hourCycle: "h23"
            }).format(instante);
        }
    };
})();
