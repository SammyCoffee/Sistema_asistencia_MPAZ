const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const contexto={window:{},Intl,Date}; vm.createContext(contexto);
vm.runInContext(fs.readFileSync('interfaz_prueba/tiempo-escolar.js','utf8'),contexto);
const t=contexto.window.MPAZTiempo;
assert.equal(t.fecha(new Date('2026-11-17T01:00:00Z')),'2026-11-16');
assert.equal(t.hora(new Date('2026-11-17T01:00:00Z')),'22:00');
assert.equal(t.hora(new Date('2026-04-05T03:00:00Z')),'23:00');
assert.equal(t.hora(new Date('2026-09-06T04:00:00Z')),'01:00');
console.log('Fecha/hora escolar: medianoche y DST aprobados');
