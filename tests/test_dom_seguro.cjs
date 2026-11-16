const fs = require('node:fs'), vm = require('node:vm'), assert = require('node:assert/strict');
// DOM mínimo que rechaza HTML: obliga a construir los nodos y campos como texto.
class Nodo {
    constructor(tag) { this.tagName=tag; this.children=[]; this.dataset={}; this.textContent=''; }
    appendChild(n) { this.children.push(n); return n; }
    set innerHTML(_) { throw Error('No se permite interpretar HTML en constructores dinámicos'); }
}
const contexto={document:{createElement: tag=>new Nodo(tag)}, window:{}};
vm.createContext(contexto);
vm.runInContext(fs.readFileSync('interfaz_prueba/dom-seguro.js','utf8'),contexto);
const payload='<img src=x onerror=alert(1)>';
const dom=contexto.window.MPAZDom;
let fila=new Nodo('tr'); dom.celdas(fila,[payload,'1A',null]);
assert.equal(fila.children[0].tagName,'td'); assert.equal(fila.children[0].textContent,payload);
const resultado=dom.resultadoAlumno({id:'" onclick="alert(1)',nombre:payload,curso:payload});
assert.equal(resultado.children[0].children[0].textContent,payload);
assert.equal(resultado.children[1].dataset.id,'" onclick="alert(1)');
let resumen=new Nodo('div'); dom.resumenCurso(resumen,payload,50,1,2,payload);
assert.equal(resumen.children[0].textContent,payload);
assert.equal(resumen.children[3].textContent,payload);
console.log('DOM dinámico: 3 constructores seguros aprobados');
