
'use strict';
// MPAZ RFID - Seguimiento Escolar.
(() => {
  const $ = (id) => document.getElementById(id);
  const sesion = {
    operador: null, csrf: null, casos: [], casoId: null,
    soloLectura: false
  };
  const estados = {
    pendiente: 'Pendiente',
    en_gestion: 'En gestión',
    resuelto: 'Resuelto'
  };

  function informar(texto, error = false) {
    $('mensaje-sistema').textContent = texto;
    $('mensaje-sistema').className = error ? 'error' : 'exito';
  }

  async function solicitar(ruta, opciones = {}) {
    const respuesta = await fetch(ruta, {
      credentials: 'same-origin',
      cache: 'no-store',
      ...opciones,
      headers: {
        ...(opciones.body ? {
          'Content-Type': 'application/json'
        } : {}),
        ...(opciones.headers || {})
      }
    });

    const datos = await respuesta.json().catch(() => ({}));

    if (!respuesta.ok) {
      const error = new Error(
        datos.resultado || `Error HTTP ${respuesta.status}`
      );
      error.status = respuesta.status;
      throw error;
    }

    return datos;
  }

  function ejecutar(accion) {
    Promise.resolve().then(accion).catch((error) => {
      if (error.status === 401) {
        window.location.href = '/login.html';
        return;
      }
      informar(`No se pudo completar: ${error.message}`, true);
    });
  }

  function mostrarAcceso() {
    sesion.soloLectura = false;
    sesion.operador = null;
    sesion.csrf = null;
    sesion.casos = [];
    sesion.casoId = null;

    $('panel-seguimiento').hidden = true;
    $('acceso').hidden = false;
    $('cerrar-sesion').hidden = true;
    $('usuario-actual').textContent = '';
    $('gestiones').hidden = true;
    $('detalle-caso').textContent =
      'Seleccione un caso para consultar sus antecedentes.';
  }

  async function comprobarSesion() {

    let panelActivo = false;

    // Comprobar sesión administrativa.
    try {
      await solicitar('/panel/sesion');
      panelActivo = true;
    } catch (error) {
      if (error.status !== 401) throw error;
    }

    // Comprobar identidad individual.
    let identidad = null;

    try {
      const datos = await solicitar(
        '/seguimiento/operador/sesion'
      );

      if (
        datos.operador &&
        ['administracion', 'direccion'].includes(
          datos.operador.rol
        ) &&
        typeof datos.csrf_token === 'string' &&
        datos.csrf_token
      ) {
        identidad = datos;
      }

    } catch (error) {
      if (error.status !== 401) throw error;
    }

    const esDireccion = (
      identidad?.operador?.rol === 'direccion'
    );

    // Exigir una sesión autorizada.
    if (!panelActivo && !esDireccion) {
      window.location.href = '/login.html';
      return;
    }

    sesion.operador = identidad?.operador || null;
    sesion.csrf = identidad?.csrf_token || null;
    sesion.soloLectura = !identidad;

    // Mostrar identidad correspondiente.
    if (identidad) {
      const nombre = identidad.operador.nombre;
      const perfil = esDireccion
        ? 'Dirección'
        : 'Administración';

      $('usuario-actual').textContent =
        `${nombre} · ${perfil}`;

    } else {
      $('usuario-actual').textContent =
        'Administración · Solo consulta';
    }

    $('acceso').hidden = true;
    $('panel-seguimiento').hidden = false;

    // Dirección puede cerrar su sesión aquí.
    $('cerrar-sesion').hidden = !esDireccion;

    // Solo Administración puede regresar al panel.
    const volverPanel = $('volver-panel');

    if (volverPanel) {
      volverPanel.hidden = esDireccion;
      volverPanel.style.display = esDireccion
        ? 'none'
        : '';
    }

    await cargarCasos();
  }

  function elemento(etiqueta, texto, clase = '') {
    const nodo = document.createElement(etiqueta);
    nodo.textContent = texto == null ? '' : String(texto);
    if (clase) nodo.className = clase;
    return nodo;
  }

  async function cargarCasos() {
    const datos = await solicitar('/panel/seguimiento/casos');
    sesion.casos = datos.casos || [];

    const campos = {
      pendiente: 'total-pendientes',
      en_gestion: 'total-gestion',
      resuelto: 'total-resueltos'
    };

    for (const clave of Object.keys(estados)) {
      $(campos[clave]).textContent = sesion.casos.filter(
        (c) => c.estado === clave
      ).length;
    }

    pintarCasos();
  }

  function pintarCasos() {
    const caja = $('lista-casos');
    caja.replaceChildren();

    const filtro = $('filtro-estado').value;
    const casos = sesion.casos.filter(
      (c) => !filtro || c.estado === filtro
    );

    if (!casos.length) {
      caja.append(elemento('p', 'No hay casos para este filtro.'));
    }

    for (const c of casos) {
      const boton = elemento('button', '', 'caso-item');
      boton.type = 'button';

      if (c.id === sesion.casoId) {
        boton.classList.add('activo');
      }

      boton.append(elemento('strong', c.alumno));
      boton.append(elemento(
        'span',
        `${c.curso} · ${c.tipo} · ${c.fecha_evento}`,
        'caso-meta'
      ));
      boton.append(elemento(
        'span',
        estados[c.estado] || c.estado,
        `estado ${c.estado}`
      ));

      boton.addEventListener(
        'click',
        () => ejecutar(() => abrirCaso(c.id))
      );

      caja.append(boton);
    }
  }

  async function abrirCaso(id) {
    const datos = await solicitar(
      `/panel/seguimiento/casos/${id}/historial`
    );

    const c = datos.caso;
    sesion.casoId = c.id;
    pintarCasos();

    $('detalle-caso').replaceChildren(
      elemento('h3', c.alumno),
      elemento('p',
        `Curso ${c.curso} · ${c.tipo} · ${c.fecha_evento}`
      ),
      elemento('p',
        `Estado: ${estados[c.estado] || c.estado}`
      ),
      elemento('strong', 'Observación inicial:'),
      elemento('p', c.descripcion),
      elemento('small',
        `Informado por: ${c.creado_por} · ${c.creado_en}`
      )
    );

    const lista = $('historial-intervenciones');
    lista.replaceChildren();

    const eventos = [
      ...datos.mensajes.map((m) => ({
        fecha: m.fecha,
        actor: m.autor,
        texto: m.mensaje,
        clase: `Mensaje · ${m.autor_rol}`,
        id: m.id
      })),
      ...datos.contactos.map((ct) => ({
        fecha: ct.fecha,
        actor: ct.responsable,
        texto: `${ct.canal}: ${ct.resultado}` +
          (ct.observacion ? ` · ${ct.observacion}` : ''),
        clase: 'Contacto',
        id: ct.id
      }))
    ];

    eventos.sort(
      (a, b) =>
        String(a.fecha).localeCompare(String(b.fecha)) ||
        a.id - b.id
    );

    if (!eventos.length) {
      lista.append(elemento(
        'p', 'Aún no hay intervenciones.'
      ));
    }

    for (const e of eventos) {
      const tarjeta = elemento('article', '', 'intervencion');
      tarjeta.append(elemento(
        'strong', `${e.clase} · ${e.actor}`
      ));
      tarjeta.append(elemento('small', e.fecha));
      tarjeta.append(elemento('p', e.texto));
      lista.append(tarjeta);
    }

    if (datos.historial_parcial) {
      lista.append(elemento(
        'p', 'Se muestran solo las intervenciones más recientes.'
      ));
    }

    $('gestiones').hidden = false;
    $('form-mensaje').hidden =
      sesion.soloLectura || c.estado === 'resuelto';

    $('form-contacto').hidden =
      sesion.soloLectura ||
      c.estado === 'resuelto' ||
      !sesion.operador ||
      sesion.operador.rol !== 'administracion';

    $('form-estado').hidden = sesion.soloLectura;
    $('estado-caso').value = c.estado;
  }

  async function guardar(ruta, datos) {
    if (sesion.soloLectura) {
      throw new Error(
        'Modo consulta: se requiere una cuenta individual.'
      );
    }

    if (sesion.casoId == null) {
      throw new Error('Seleccione un caso.');
    }

    const id = sesion.casoId;

    await solicitar(
      `/panel/seguimiento/casos/${id}/${ruta}`,
      {
        method: 'POST',
        headers: { 'X-CSRF-Token': sesion.csrf },
        body: JSON.stringify(datos)
      }
    );

    await cargarCasos();
    await abrirCaso(id);
    informar('Gestión registrada correctamente.');
  }

  $('form-login').addEventListener('submit', (evento) => {
    evento.preventDefault();

    ejecutar(async () => {
      await solicitar('/seguimiento/operador/login', {
        method: 'POST',
        body: JSON.stringify({
          usuario: $('usuario').value.trim(),
          password: $('password').value
        })
      });

      $('password').value = '';
      await comprobarSesion();
      informar('Sesión iniciada correctamente.');
    });
  });

  $('cerrar-sesion').addEventListener('click', () => {
    ejecutar(async () => {
      await solicitar('/seguimiento/operador/logout', {
        method: 'POST',
        headers: { 'X-CSRF-Token': sesion.csrf }
      });

      window.location.href = '/login.html';
    });
  });

  $('filtro-estado').addEventListener('change', pintarCasos);

  $('actualizar-casos').addEventListener('click', () => {
    ejecutar(async () => {
      await cargarCasos();
      informar('Bandeja actualizada.');
    });
  });

  $('form-mensaje').addEventListener('submit', (evento) => {
    evento.preventDefault();

    ejecutar(async () => {
      await guardar('mensajes', {
        mensaje: $('mensaje').value.trim()
      });

      $('form-mensaje').reset();
    });
  });

  $('form-contacto').addEventListener('submit', (evento) => {
    evento.preventDefault();

    ejecutar(async () => {
      await guardar('contactos', {
        canal: $('canal').value,
        resultado: $('resultado-contacto').value.trim(),
        observacion: $('observacion-contacto').value.trim()
      });

      $('form-contacto').reset();
    });
  });

  $('form-estado').addEventListener('submit', (evento) => {
    evento.preventDefault();

    ejecutar(() => guardar('estado', {
      estado: $('estado-caso').value
    }));
  });

  mostrarAcceso();

  ejecutar(async () => {
    try {
      await comprobarSesion();
    } catch (error) {
      if (error.status !== 401) throw error;
    }
  });
})();
