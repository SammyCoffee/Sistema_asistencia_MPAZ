/* MPAZ-CALENDARIO-663 */

(function () {
    "use strict";

    const preparar = document.getElementById("mpaz-cal-preparar");
    const cancelar = document.getElementById("mpaz-cal-cancelar");
    const mensaje = document.getElementById("mpaz-cal-operacion");
    const formulario = document.getElementById("mpaz-cal-formulario");
    const guardar = document.getElementById("mpaz-cal-guardar");
    const fecha = document.getElementById("mpaz-cal-fecha");
    const cursoFiltro = document.getElementById("mpaz-cal-curso");
    const alcance = document.getElementById("mpaz-cal-alcance");
    const condicion = document.getElementById("mpaz-cal-condicion");
    const entrada = document.getElementById("mpaz-cal-entrada");
    const salida = document.getElementById("mpaz-cal-salida");
    const motivo = document.getElementById("mpaz-cal-motivo");

    if (![preparar, cancelar, mensaje, formulario, guardar, fecha,
          cursoFiltro, alcance, condicion, entrada, salida, motivo]
         .every(Boolean)) return;

    let operacion = null;
    let secuencia = 0;
    let enviando = false;

    // La edición se habilita únicamente en la vista previa.
    const vistaPrevia = location.hostname === "127.0.0.1" &&
        (location.port === "18765" || location.port === "8765");

    function informar(texto, error = false) {
        mensaje.textContent = texto;
        mensaje.dataset.error = error ? "si" : "no";
    }

    function desactivar() {
        secuencia++;
        operacion = null;
        guardar.disabled = true;
        guardar.textContent = "Guardado pendiente de habilitación";
        cancelar.disabled = true;
        alcance.disabled = false;
    }

    if (!vistaPrevia) {
        preparar.disabled = true;
        informar(
            "Edición bloqueada fuera de la vista previa local."
        );
        return;
    }

    informar(
        "Pulsa «Preparar operación». " +
        "Ninguna jornada se guardará sin confirmación."
    );

    async function consultarMes(curso, dia) {
        const parametros = new URLSearchParams({
            mes: dia.substring(0, 7),
            curso: curso
        });

        const respuesta = await fetch(
            "/panel/calendario/mes?" + parametros,
            {
                credentials: "same-origin",
                cache: "no-store"
            }
        );

        if (!respuesta.ok) {
            throw new Error(
                "Consulta HTTP " + respuesta.status
            );
        }

        const datos = await respuesta.json();

        if (
            datos.resultado !== "ok" ||
            !Array.isArray(datos.jornadas)
        ) {
            throw new Error("Respuesta mensual inválida");
        }

        const efectiva = datos.jornadas.find(
            jornada => jornada.fecha === dia
        );

        // No confundir una jornada general heredada
        // con una excepción propia del curso.
        const exacta = efectiva && (
            curso
                ? efectiva.alcance === "curso"
                : efectiva.alcance === "general"
        );

        return exacta ? efectiva : null;
    }

    function firma(jornada) {
        if (!jornada) return null;

        return JSON.stringify([
            jornada.id,
            jornada.condicion,
            jornada.hora_entrada || null,
            jornada.hora_salida || null,
            jornada.motivo || ""
        ]);
    }

    preparar.addEventListener("click", async function () {
        if (enviando) return;

        desactivar();

        const identificador = secuencia;
        const dia = fecha.value;
        const curso = cursoFiltro.value;

        if (!/^[0-9]{4}-[0-9]{2}-[0-9]{2}$/.test(dia)) {
            informar("Selecciona una fecha válida.", true);
            return;
        }

        preparar.disabled = true;

        informar(
            "Comprobando la configuración exacta " +
            "de la fecha y el curso..."
        );

        try {
            const existente = await consultarMes(curso, dia);

            if (
                identificador !== secuencia ||
                fecha.value !== dia ||
                cursoFiltro.value !== curso
            ) {
                return;
            }

            if (!existente) {
                if (
                    curso &&
                    !window.confirm(
                        "Se preparará una jornada EXCLUSIVA para " +
                        curso + " en " + dia + ". " +
                        "La configuración general no se modificará. " +
                        "¿Continuar?"
                    )
                ) {
                    return;
                }

                condicion.value = "lectiva";
                entrada.value = "";
                salida.value = "";
                motivo.value = "";

            } else {
                condicion.value = existente.condicion;
                entrada.value = existente.hora_entrada || "";
                salida.value = existente.hora_salida || "";
                motivo.value = existente.motivo || "";
            }

            alcance.value = curso;
            alcance.disabled = true;

            operacion = {
                accion: existente ? "editar" : "crear",
                dia: dia,
                curso: curso,
                firma: firma(existente)
            };

            guardar.disabled = false;
            guardar.textContent = existente
                ? "Guardar modificación"
                : "Registrar jornada";

            cancelar.disabled = false;

            informar(
                (existente ? "Edición" : "Registro nuevo") +
                " preparado para " +
                (curso || "toda la escuela") +
                ". Se solicitará confirmación antes de guardar."
            );

        } catch (error) {
            informar(
                "No se pudo verificar el registro. " +
                "El guardado permanece deshabilitado.",
                true
            );

            console.error("MPAZ calendario:", error);

        } finally {
            preparar.disabled = false;
        }
    });

    cancelar.addEventListener("click", function () {
        if (enviando) return;

        desactivar();

        informar(
            "Operación cancelada. No se modificaron jornadas."
        );

        cursoFiltro.dispatchEvent(
            new Event("change", { bubbles: true })
        );
    });

    function invalidarPorNavegacion() {
        if (enviando || !operacion) return;

        desactivar();

        informar(
            "La selección cambió. " +
            "Pulsa «Preparar operación» nuevamente."
        );
    }

    [fecha, cursoFiltro].forEach(function (elemento) {
        elemento.addEventListener(
            "change",
            invalidarPorNavegacion,
            true
        );
    });

    const cuadricula = document.getElementById(
        "mpaz-cal-cuadricula"
    );

    if (cuadricula) {
        cuadricula.addEventListener(
            "click",
            invalidarPorNavegacion,
            true
        );
    }

    [
        "mpaz-cal-anterior",
        "mpaz-cal-siguiente",
        "mpaz-cal-hoy"
    ].forEach(function (id) {
        const boton = document.getElementById(id);

        if (boton) {
            boton.addEventListener(
                "click",
                invalidarPorNavegacion,
                true
            );
        }
    });

    formulario.addEventListener("submit", async function (evento) {
        evento.preventDefault();

        if (enviando || !operacion || guardar.disabled) return;

        const op = operacion;

        if (
            fecha.value !== op.dia ||
            cursoFiltro.value !== op.curso ||
            alcance.value !== op.curso
        ) {
            desactivar();

            informar(
                "Cambió la fecha o el alcance. " +
                "Prepara nuevamente la operación.",
                true
            );
            return;
        }

        const datos = {
            fecha: op.dia,
            curso: op.curso || null,
            condicion: condicion.value,
            motivo: motivo.value.trim(),
            hora_entrada: entrada.value || null,
            hora_salida: salida.value || null
        };

        if (
            datos.motivo.length < 8 ||
            datos.motivo.length > 300
        ) {
            informar(
                "El motivo debe contener entre 8 y 300 caracteres.",
                true
            );
            return;
        }

        if (datos.condicion === "feriado" && datos.curso) {
            informar(
                "Un feriado solo puede registrarse " +
                "para toda la escuela.",
                true
            );
            return;
        }

        const requiereHorario = [
            "reducida",
            "horario_especial"
        ].includes(datos.condicion);

        if (
            requiereHorario &&
            (!datos.hora_entrada || !datos.hora_salida)
        ) {
            informar(
                "La jornada especial requiere " +
                "hora de entrada y salida.",
                true
            );
            return;
        }

        if (
            ["feriado", "suspendida"].includes(datos.condicion) &&
            (datos.hora_entrada || datos.hora_salida)
        ) {
            informar(
                "Suspensiones y feriados no deben incluir horarios.",
                true
            );
            return;
        }

        if (
            Boolean(datos.hora_entrada) !==
                Boolean(datos.hora_salida) ||
            (
                datos.hora_entrada &&
                datos.hora_entrada >= datos.hora_salida
            )
        ) {
            informar(
                "Comprueba que ambas horas estén completas " +
                "y correctamente ordenadas.",
                true
            );
            return;
        }

        const alcanceTexto = op.curso
            ? "CURSO " + op.curso
            : "TODA LA ESCUELA";

        const confirmado = window.confirm(
            "VISTA PREVIA MPAZ\n" +
            "Operación: " + op.accion.toUpperCase() + "\n" +
            "Fecha: " + op.dia + "\n" +
            "Alcance: " + alcanceTexto + "\n" +
            "Condición: " + datos.condicion + "\n" +
            "Motivo: " + datos.motivo + "\n\n" +
            "¿Confirmas esta operación en la base de PRUEBAS?"
        );

        if (!confirmado) return;

        enviando = true;
        guardar.disabled = true;
        preparar.disabled = true;

        informar(
            "Comprobando cambios y enviando operación..."
        );

        try {
            const actual = await consultarMes(op.curso, op.dia);

            if (
                (op.accion === "crear" && actual) ||
                (
                    op.accion === "editar" &&
                    firma(actual) !== op.firma
                )
            ) {
                throw new Error(
                    "El registro cambió. " +
                    "Prepara nuevamente la operación."
                );
            }

            const respuestaToken = await fetch(
                "/panel/calendario/token",
                {
                    credentials: "same-origin",
                    cache: "no-store"
                }
            );

            if (!respuestaToken.ok) {
                throw new Error(
                    "La sesión expiró o el token no está disponible."
                );
            }

            const token = (
                await respuestaToken.json()
            ).csrf_token;

            if (typeof token !== "string" || !token) {
                throw new Error("Token inválido.");
            }

            const ruta = op.accion === "crear"
                ? "/panel/calendario/jornadas/registrar"
                : "/panel/calendario/jornadas/editar";

            const respuesta = await fetch(ruta, {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRF-Token": token
                },
                body: JSON.stringify(datos)
            });

            const resultado = await respuesta.json();

            if (
                !respuesta.ok ||
                ![
                    "creada",
                    "actualizada",
                    "sin_cambios"
                ].includes(resultado.resultado)
            ) {
                throw new Error(
                    "Servidor: " +
                    (resultado.resultado ||
                     "HTTP " + respuesta.status)
                );
            }

            desactivar();

            informar(
                "Operación registrada en la base de PRUEBAS. " +
                "El calendario se está actualizando."
            );

            cursoFiltro.dispatchEvent(
                new Event("change", { bubbles: true })
            );

        } catch (error) {
            desactivar();

            informar(
                "No se confirmó el guardado: " +
                error.message,
                true
            );

            console.error("MPAZ calendario:", error);

        } finally {
            enviando = false;
            preparar.disabled = false;
        }
    });
})();
