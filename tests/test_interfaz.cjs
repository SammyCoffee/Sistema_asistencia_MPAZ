// Ejecuta la función real de ficha con un DOM mínimo; no sustituye QA visual.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const fuente = fs.readFileSync('interfaz_prueba/app.js', 'utf8');
const inicio = fuente.indexOf('function mostrarFichaEstudiante(');
const fin = fuente.indexOf('\nresultadoEstudiante.addEventListener', inicio);
const contexto = {resultadoEstudiante: {innerHTML: ''}};
vm.createContext(contexto);
vm.runInContext(fuente.slice(inicio, fin), contexto);
contexto.mostrarFichaEstudiante({id: 1, nombre: 'Nombre Ficticio', curso:'1A', rut:'DEMO-NO-RUT', uid:'<img src=x onerror=alert(1)>', estado_alumno:'activo', estado_tarjeta:'activa'});
assert.ok(!contexto.resultadoEstudiante.innerHTML.includes('<img'), 'UID no debe crear HTML ejecutable');
assert.ok(contexto.resultadoEstudiante.innerHTML.includes('&lt;img'), 'El UID debe mostrarse como texto');
console.log('Ficha: payload HTML escapado correctamente');
