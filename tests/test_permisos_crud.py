"""Permisos por registro y operaciones administrativas con identificadores generados."""
import unittest
import test_auditoria as fixtures


class PermisosCrudTest(unittest.TestCase):
    setUp = fixtures.SistemaTest.setUp
    login = fixtures.SistemaTest.login
    docente = fixtures.SistemaTest.docente

    def test_idor_asignacion_sesion_alumno(self):
        self.con.execute("INSERT INTO sesiones_clase(id,asignacion_id,fecha,hora_inicio) VALUES (2,2,'2026-11-16','08:00')")
        self.con.commit()
        token=self.docente(); cab={'X-CSRF-Token':token}
        for ruta in ['/profesor/asignaciones/2/sesiones', '/profesor/sesiones/2', '/profesor/cursos/2A/alumnos', '/profesor/cursos/2A/asistencia?fecha=2026-11-16']:
            with self.subTest(ruta=ruta):
                self.assertEqual(self.client.get(ruta).status_code,403)
        self.assertEqual(self.client.post('/profesor/sesiones',json={'asignacion_id':2,'fecha':'2026-11-16','hora_inicio':'08:00'},headers=cab).status_code,403)
        self.assertEqual(self.client.post('/profesor/sesiones/2/asistencia',json={'alumno_id':2,'estado':'presente'},headers=cab).status_code,403)
        self.assertEqual(self.client.post('/profesor/sesiones/2/confirmar',headers=cab).status_code,403)
        propia=self.client.post('/profesor/sesiones',json={'asignacion_id':1,'fecha':'2026-11-16','hora_inicio':'08:00'},headers=cab)
        self.assertEqual(propia.status_code,201)
        ident=propia.json['sesion_id']
        self.assertEqual(self.client.post(f'/profesor/sesiones/{ident}/asistencia',json={'alumno_id':2,'estado':'presente'},headers=cab).status_code,403)
        self.assertEqual(self.client.post(f'/profesor/sesiones/{ident}/asistencia',json={'alumno_id':1,'estado':'presente','observacion':'<img src=x onerror=alert(1)>'},headers=cab).status_code,200)
        self.assertEqual(self.client.post(f'/profesor/sesiones/{ident}/confirmar',headers=cab).status_code,200)
        self.assertEqual(self.client.post(f'/profesor/sesiones/{ident}/asistencia',json={'alumno_id':1,'estado':'no_presente'},headers=cab).status_code,409)

    def test_roles_no_modifican_recursos_administrativos(self):
        for rol in ('docente','direccion'):
            with self.subTest(rol=rol):
                self.docente() if rol=='docente' else self.login('direccion')
                for ruta in ['/alumnos','/panel/tarjetas','/panel/totems','/asistencias','/inasistencias','/atrasos','/asistencias/exportar/diario']:
                    self.assertEqual(self.client.get(ruta).status_code,401)
                for ruta,datos in [('/panel/alumnos/estado',{'alumno_id':1,'estado':'inactivo'}),('/panel/tarjetas/vincular',{'alumno_id':1,'uid':'AABBCCDD'}),('/panel/totems/estado',{'codigo':'DEMO','estado':'inactivo'})]:
                    self.assertEqual(self.client.post(ruta,json=datos).status_code,401)
        self.assertEqual(self.con.execute('SELECT estado FROM alumnos WHERE id=1').fetchone()[0],'activo')

    def test_totem_alta_duplicado_estado_y_tarjeta_extraviada(self):
        token=self.login(); cab={'X-CSRF-Token':token}
        datos={'codigo':'DEMO-DOS','nombre':'Totem Ficticio','ubicacion':'Laboratorio'}
        self.assertEqual(self.client.post('/panel/totems/registrar',json=datos,headers=cab).status_code,201)
        self.assertEqual(self.client.post('/panel/totems/registrar',json=datos,headers=cab).status_code,409)
        resultado=fixtures.bd.cambiar_estado_totem('DEMO-DOS','inactivo')
        self.assertEqual(resultado['resultado'],'actualizado')
        self.assertEqual(fixtures.bd.validar_totem('DEMO-DOS')['resultado'],'inactivo')
        self.assertEqual(fixtures.bd.marcar_tarjeta_extraviada('AABBCCDD')['resultado'],'extraviada')
        self.assertEqual(self.con.execute("SELECT estado FROM tarjetas WHERE uid='AABBCCDD'").fetchone()[0],'extraviada')

    def test_crud_estudiante_ficticio(self):
        # Valor generado para el escenario, sin vínculo a personas ni bases escolares.
        cuerpo='99000001'
        suma=sum(int(d)*((i%6)+2) for i,d in enumerate(reversed(cuerpo)))
        digito=11-suma%11; dv='0' if digito==11 else 'K' if digito==10 else str(digito)
        rut=cuerpo+'-'+dv
        token=self.login(); cab={'X-CSRF-Token':token}
        datos={'rut':rut,'nombre':'Estudiante Ficticio','curso':'1A'}
        alta=self.client.post('/panel/alumnos/registrar',json=datos,headers=cab)
        self.assertEqual(alta.status_code,201)
        ident=alta.json['id']
        self.assertEqual(self.client.post('/panel/alumnos/registrar',json=datos,headers=cab).status_code,409)
        datos.update(id=ident,nombre='Estudiante Simulado',curso='2A')
        self.assertEqual(self.client.post('/panel/alumnos/editar',json=datos,headers=cab).status_code,200)
        self.assertEqual(fixtures.bd.cambiar_estado_alumno(ident,'inactivo')['resultado'],'actualizado')
        self.assertIsNotNone(self.con.execute('SELECT fecha_baja FROM alumnos WHERE id=?',(ident,)).fetchone()[0])
        self.assertEqual(fixtures.bd.cambiar_estado_alumno(ident,'activo')['resultado'],'actualizado')
        fila=self.con.execute('SELECT nombre_completo,curso,estado,fecha_baja FROM alumnos WHERE id=?',(ident,)).fetchone()
        self.assertEqual(fila,('Estudiante Simulado','2A','activo',None))

    def test_tokens_unicode_rechazados(self):
        self.assertEqual(self.client.post('/lectura',json={},headers={'X-API-Key':'á'}).status_code,401)
        self.login()
        self.assertEqual(self.client.post('/panel/logout',headers={'X-CSRF-Token':'á'}).status_code,403)
        token=self.docente()
        self.assertEqual(self.client.post('/profesor/logout',headers={'X-CSRF-Token':'á'}).status_code,403)

    def test_json_anidado_en_gestiones(self):
        self.login()
        token=self.client.get('/seguimiento/operador/sesion').json['csrf_token']
        for ruta, datos in [('/panel/seguimiento/casos/1/estado', {'estado': []}), ('/panel/seguimiento/casos/1/contactos', {'canal': [], 'resultado': 'Ficticio'})]:
            with self.subTest(ruta=ruta):
                self.assertEqual(self.client.post(ruta, json=datos, headers={'X-CSRF-Token':token}).status_code,400)
