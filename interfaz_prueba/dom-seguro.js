/* Constructores dinámicos: los datos nunca se interpretan como HTML. */
(function () {
    "use strict";
    function elemento(tag, texto) {
        const nodo = document.createElement(tag);
        nodo.textContent = String(texto ?? "");
        return nodo;
    }
    window.MPAZDom = {
        celdas(fila, valores) {
            valores.forEach(valor => fila.appendChild(elemento("td", valor)));
        },
        resultadoAlumno(alumno) {
            const contenedor = document.createElement("div");
            const texto = document.createElement("p");
            texto.appendChild(elemento("strong", alumno.nombre));
            texto.appendChild(elemento("span", " - " + alumno.curso));
            const boton = elemento("button", "Ver ficha");
            boton.type = "button";
            boton.className = "boton-ver-alumno";
            boton.dataset.id = String(alumno.id);
            contenedor.appendChild(texto);
            contenedor.appendChild(boton);
            return contenedor;
        },
        resumenCurso(contenedor, nombre, porcentaje, presentes, total, estado) {
            contenedor.appendChild(elemento("h3", nombre));
            const cifra = elemento("p", porcentaje + "%");
            cifra.className = "porcentaje-asistencia";
            contenedor.appendChild(cifra);
            contenedor.appendChild(elemento("p", presentes + " de " + total + " estudiantes con ingreso RFID"));
            contenedor.appendChild(elemento("strong", estado));
        }
    };
})();
