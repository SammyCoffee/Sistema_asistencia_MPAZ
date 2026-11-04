import React, { useState } from 'react';
import { Link } from 'react-router-dom';

export default function Home() {
  // Controla qué sección se muestra ('inicio', 'estudiantes', 'tarjetas', etc.)
  const [vistaActiva, setVistaActiva] = useState('inicio');

  const fechaHoy = new Date().toLocaleDateString('es-CL', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  const cambiarPreferencia = (ajuste, activo) => {
    const html = document.documentElement;
    if (ajuste === 'oscuro') {
      if (activo) html.setAttribute('data-mpaz-tema', 'oscuro');
      else html.removeAttribute('data-mpaz-tema');
    }
    if (ajuste === 'compacto') {
      if (activo) html.setAttribute('data-mpaz-densidad', 'compacta');
      else html.removeAttribute('data-mpaz-densidad');
    }
    if (ajuste === 'letra_grande') {
      if (activo) html.setAttribute('data-mpaz-lectura', 'ampliada');
      else html.removeAttribute('data-mpaz-lectura');
    }
    if (ajuste === 'reducir_movimiento') {
      if (activo) html.setAttribute('data-mpaz-movimiento', 'reducido');
      else html.removeAttribute('data-mpaz-movimiento');
    }
  };

  const restablecerVista = () => {
    const html = document.documentElement;
    html.removeAttribute('data-mpaz-tema');
    html.removeAttribute('data-mpaz-densidad');
    html.removeAttribute('data-mpaz-lectura');
    html.removeAttribute('data-mpaz-movimiento');
  };

  return (
    <div className="pagina">
      {/* ================= BARRA SUPERIOR INSTITUCIONAL (MPAZ-VISTAS-627) ================= */}
      <div className="mpaz-barra">
        <div className="mpaz-barra-identidad">
          <img
            className="mpaz-marca mpaz-escudo"
            src="/escudo-mpaz.webp"
            width="48"
            height="48"
            alt="Escudo de la escuela"
          />
          <div>
            <strong>Escuela Escritora Marcela Paz</strong>
            <small>Sistema de gestión escolar RFID</small>
          </div>
        </div>

        <div className="mpaz-barra-navegacion">
          {vistaActiva !== 'inicio' && (
            <a
              href="#inicio"
              id="mpaz-volver-panel"
              onClick={(e) => {
                e.preventDefault();
                setVistaActiva('inicio');
              }}
            >
              ← Panel principal
            </a>
          )}

          {/* Selector rápido de secciones */}
          <div className="mpaz-selector-contenedor">
            <select
              value={vistaActiva}
              onChange={(e) => setVistaActiva(e.target.value)}
              aria-label="Cambiar sección del panel"
            >
              <option value="inicio">Panel principal</option>
              <option value="estudiantes">Estudiantes</option>
              <option value="tarjetas">Tarjetas RFID</option>
              <option value="vinculacion">Vinculación</option>
              <option value="asistencias">Asistencias</option>
              <option value="inasistencias">Inasistencias</option>
              <option value="atrasos">Atrasos</option>
              <option value="analisis">Análisis de datos</option>
              <option value="calendario">Calendario escolar</option>
              <option value="reportes">Reportes</option>
            </select>
          </div>

          <div id="mpaz-acciones-admin">
            <div className="acciones-cabecera">
              <Link
                to="/"
                className="boton-volver-inicio"
                style={{
                  display: 'inline-block',
                  padding: '10px 16px',
                  borderRadius: '8px',
                  background: '#1677b8',
                  color: '#fff',
                  textDecoration: 'none',
                  fontWeight: 600
                }}
              >
                ← Volver al inicio
              </Link>

              <details className="menu-configuracion">
                <summary
                  aria-label="Abrir preferencias de visualización"
                  title="Preferencias de visualización"
                >
                  ⚙
                </summary>
                <div className="contenido-configuracion mpaz-preferencias">
                  <h2>Preferencias</h2>
                  <p className="mpaz-config-ayuda">
                    Personaliza la apariencia de este dispositivo.
                  </p>
                  <label className="mpaz-ajuste">
                    <span>
                      <strong>Tema oscuro</strong>
                      <small>Usar colores de alto contraste</small>
                    </span>
                    <input
                      type="checkbox"
                      onChange={(e) => cambiarPreferencia('oscuro', e.target.checked)}
                    />
                  </label>
                  <label className="mpaz-ajuste">
                    <span>
                      <strong>Vista compacta</strong>
                      <small>Reducir espacios entre elementos</small>
                    </span>
                    <input
                      type="checkbox"
                      onChange={(e) => cambiarPreferencia('compacto', e.target.checked)}
                    />
                  </label>
                  <label className="mpaz-ajuste">
                    <span>
                      <strong>Texto ampliado</strong>
                      <small>Facilitar la lectura</small>
                    </span>
                    <input
                      type="checkbox"
                      onChange={(e) => cambiarPreferencia('letra_grande', e.target.checked)}
                    />
                  </label>
                  <label className="mpaz-ajuste">
                    <span>
                      <strong>Reducir animaciones</strong>
                      <small>Disminuir movimientos visuales</small>
                    </span>
                    <input
                      type="checkbox"
                      onChange={(e) => cambiarPreferencia('reducir_movimiento', e.target.checked)}
                    />
                  </label>
                  <button
                    type="button"
                    className="mpaz-restablecer"
                    onClick={restablecerVista}
                  >
                    Restablecer vista
                  </button>
                  <Link to="/" className="mpaz-enlace-portales">
                    Ir a selección de portales ↗
                  </Link>
                </div>
              </details>

              <Link to="/login">
                <button type="button" id="boton-cerrar-sesion">
                  Cerrar sesión
                </button>
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* ================= CONTENIDO PRINCIPAL ================= */}
      <main className="contenido">
        {/* VISTA INICIO: BIENVENIDA + ACCESOS + 4 INDICADORES */}
        {vistaActiva === 'inicio' && (
          <>
            <section id="mpaz-bienvenida" className="mpaz-bienvenida">
              <div className="mpaz-bienvenida-texto">
                <span className="mpaz-distintivo">
                  ESCUELA ESCRITORA MARCELA PAZ
                </span>
                <h2>Gestión escolar MPAZ</h2>
                <p>
                  Plataforma de administración de estudiantes, tarjetas RFID y
                  asistencia escolar.
                </p>
                <span id="mpaz-fecha-actual">{fechaHoy}</span>
              </div>

              <div className="mpaz-accesos">
                <a
                  href="#estudiantes"
                  onClick={(e) => { e.preventDefault(); setVistaActiva('estudiantes'); }}
                >
                  <span>👥</span>
                  <strong>Estudiantes</strong>
                  <small>Matrícula y fichas</small>
                </a>

                <a
                  href="#tarjetas"
                  onClick={(e) => { e.preventDefault(); setVistaActiva('tarjetas'); }}
                >
                  <span>🪪</span>
                  <strong>Tarjetas RFID</strong>
                  <small>Inventario y estados</small>
                </a>

                <a
                  href="#vinculacion"
                  onClick={(e) => { e.preventDefault(); setVistaActiva('vinculacion'); }}
                >
                  <span>🔗</span>
                  <strong>Vinculación</strong>
                  <small>Asignar tarjetas</small>
                </a>

                <a
                  href="#asistencias"
                  onClick={(e) => { e.preventDefault(); setVistaActiva('asistencias'); }}
                >
                  <span>📅</span>
                  <strong>Asistencias</strong>
                  <small>Entradas y salidas</small>
                </a>

                <Link to="/seguimiento">
                  <span>📝</span>
                  <strong>Seguimiento Escolar</strong>
                  <small>Casos, observaciones e historial</small>
                </Link>

                <a
                  href="#inasistencias"
                  onClick={(e) => { e.preventDefault(); setVistaActiva('inasistencias'); }}
                >
                  <span>📋</span>
                  <strong>Inasistencias</strong>
                  <small>Seguimiento escolar</small>
                </a>

                <a
                  href="#atrasos"
                  onClick={(e) => { e.preventDefault(); setVistaActiva('atrasos'); }}
                >
                  <span>⏰</span>
                  <strong>Atrasos</strong>
                  <small>Control de llegadas</small>
                </a>

                <a
                  href="#analisis"
                  onClick={(e) => { e.preventDefault(); setVistaActiva('analisis'); }}
                >
                  <span>📊</span>
                  <strong>Análisis</strong>
                  <small>Estadísticas escolares</small>
                </a>

                <a
                  href="#calendario"
                  onClick={(e) => { e.preventDefault(); setVistaActiva('calendario'); }}
                >
                  <span aria-hidden="true">🗓️</span>
                  <strong>Calendario escolar</strong>
                  <small>Jornadas y fechas</small>
                </a>

                <a
                  href="#reportes"
                  onClick={(e) => { e.preventDefault(); setVistaActiva('reportes'); }}
                >
                  <span>📁</span>
                  <strong>Reportes</strong>
                  <small>Exportar información</small>
                </a>
              </div>
            </section>

            {/* TARJETAS DE RESUMEN */}
            <section className="tarjeta-resumen">
              <p className="nombre-indicador">Estudiantes registrados</p>
              <strong className="numero-indicador" id="total-estudiantes">0</strong>
              <span className="detalle-indicador">Matrícula importada al sistema</span>
            </section>

            <section className="tarjeta-resumen">
              <p className="nombre-indicador">Tarjetas RFID asignadas</p>
              <strong className="numero-indicador" id="total-tarjetas-activas">0</strong>
              <span className="detalle-indicador">Pendientes de asignación</span>
            </section>

            <section className="tarjeta-resumen">
              <p className="nombre-indicador">Asistencias registradas hoy</p>
              <strong className="numero-indicador" id="total-asistencias-hoy">0</strong>
              <span className="detalle-indicador">Registros recibidos por los tótems</span>
            </section>

            <section className="tarjeta-resumen">
              <p className="nombre-indicador">Marcaciones por revisar</p>
              <strong className="numero-indicador" id="total-alertas-inasistencia">0</strong>
              <span className="detalle-indicador">Revisión preliminar de registros RFID</span>
            </section>
          </>
        )}

        {/* SECCIÓN ASISTENCIAS */}
        {vistaActiva === 'asistencias' && (
          <section id="asistencias" className="panel-lecturas">
            <h2>Jornadas de asistencia</h2>
            <p>Registro diario de entrada y salida de los estudiantes.</p>

            <div className="mpaz-resumen-asistencias">
              <div className="mpaz-kpi-asistencia">
                <span>Registros de ingreso</span>
                <strong id="mpaz-asis-ingresos">0</strong>
              </div>
              <div className="mpaz-kpi-asistencia">
                <span>Salidas por tótem</span>
                <strong id="mpaz-asis-salidas">0</strong>
              </div>
              <div className="mpaz-kpi-asistencia">
                <span>Cierres automáticos</span>
                <strong id="mpaz-asis-automaticas">0</strong>
              </div>
              <div className="mpaz-kpi-asistencia">
                <span>Salidas pendientes</span>
                <strong id="mpaz-asis-pendientes">0</strong>
              </div>
            </div>

            <div className="mpaz-filtros-asistencias">
              <label>
                Buscar estudiante
                <input
                  type="search"
                  id="mpaz-asis-buscar"
                  placeholder="Nombre del estudiante"
                  autoComplete="off"
                />
              </label>
              <label>
                Fecha
                <input type="date" id="mpaz-asis-fecha" />
              </label>
              <label>
                Curso
                <select id="mpaz-asis-curso">
                  <option value="">Todos los cursos</option>
                </select>
              </label>
            </div>

            <div className="mpaz-ayuda-asistencia">
              <span>Los indicadores corresponden a los registros que cumplen los filtros seleccionados.</span>
              <button type="button" id="mpaz-asis-limpiar">Limpiar filtros</button>
            </div>

            <p className="mpaz-nota-asistencia">
              <strong>Importante:</strong> el cierre automático de una jornada no acredita una salida física registrada mediante el tótem.
            </p>

            <table id="tabla-asistencias" className="tabla-lecturas">
              <thead>
                <tr>
                  <th>Fecha</th>
                  <th>Estudiante</th>
                  <th>Curso</th>
                  <th>Entrada</th>
                  <th>Salida</th>
                  <th>Tipo de salida</th>
                </tr>
              </thead>
              <tbody id="cuerpo-asistencias">
                <tr>
                  <td colSpan="6">No hay asistencias registradas.</td>
                </tr>
              </tbody>
            </table>

            <div className="mpaz-paginacion-asistencias">
              <span id="mpaz-asis-pagina">Página 1 de 1</span>
              <div>
                <button type="button" id="mpaz-asis-anterior">Anterior</button>
                <button type="button" id="mpaz-asis-siguiente">Siguiente</button>
              </div>
            </div>
          </section>
        )}

        {/* SECCIÓN ESTUDIANTES */}
        {vistaActiva === 'estudiantes' && (
          <section id="estudiantes" className="panel-lecturas">
            <h2>Administración de estudiantes</h2>
            <p>Registra nuevos estudiantes, edita sus datos y administra su estado dentro del sistema.</p>

            <details id="mpaz-formulario-plegable" className="mpaz-formulario-plegable">
              <summary>＋ Registrar o editar estudiante</summary>
              <div className="panel-administracion">
                <h3 id="titulo-formulario-estudiante">Nuevo estudiante</h3>
                <form id="formulario-estudiante" onSubmit={(e) => e.preventDefault()}>
                  <input type="hidden" id="estudiante-id" />

                  <label htmlFor="estudiante-rut">RUT</label>
                  <input type="text" id="estudiante-rut" placeholder="Ej: 12.345.678-9" required />

                  <label htmlFor="estudiante-nombre">Nombre completo</label>
                  <input type="text" id="estudiante-nombre" placeholder="Nombre y apellidos" required />

                  <label htmlFor="estudiante-curso">Curso</label>
                  <select id="estudiante-curso" required>
                    <option value="">Seleccione un curso</option>
                    <option value="PK">Pre-Kínder</option>
                    <option value="K">Kínder</option>
                    <option value="1A">1° Básico A</option>
                    <option value="1B">1° Básico B</option>
                    <option value="2A">2° Básico A</option>
                    <option value="2B">2° Básico B</option>
                    <option value="3A">3° Básico A</option>
                    <option value="3B">3° Básico B</option>
                    <option value="4A">4° Básico A</option>
                    <option value="4B">4° Básico B</option>
                    <option value="5A">5° Básico A</option>
                    <option value="5B">5° Básico B</option>
                    <option value="6A">6° Básico A</option>
                    <option value="6B">6° Básico B</option>
                    <option value="7A">7° Básico A</option>
                    <option value="7B">7° Básico B</option>
                    <option value="8A">8° Básico A</option>
                    <option value="8B">8° Básico B</option>
                  </select>

                  <div className="acciones-formulario">
                    <button type="submit" id="boton-guardar-estudiante">Guardar estudiante</button>
                  </div>
                </form>
              </div>
            </details>

            <div className="mpaz-directorio" id="directorio-general">
              <div className="mpaz-directorio-cabecera">
                <div>
                  <span className="mpaz-etiqueta">GESTIÓN ESCOLAR</span>
                  <h3>Directorio de estudiantes</h3>
                  <p>Consulta la matrícula y el estado de vinculación RFID.</p>
                </div>
                <div className="mpaz-contador">
                  <strong id="mpaz-directorio-total">0</strong>
                  <span>Estudiantes encontrados</span>
                </div>
              </div>

              <div className="mpaz-filtros">
                <label>
                  Buscar estudiante
                  <input id="mpaz-directorio-buscar" type="search" placeholder="Nombre o RUT" autoComplete="off" />
                </label>
                <label>
                  Curso
                  <select id="mpaz-directorio-curso">
                    <option value="">Todos</option>
                  </select>
                </label>
                <label>
                  Estado
                  <select id="mpaz-directorio-estado">
                    <option value="">Todos</option>
                    <option value="activo">Activo</option>
                    <option value="inactivo">Inactivo</option>
                  </select>
                </label>
                <label>
                  Tarjeta RFID
                  <select id="mpaz-directorio-rfid">
                    <option value="">Todas</option>
                    <option value="sin">Sin tarjeta</option>
                    <option value="activa">Activa</option>
                    <option value="bloqueada">Bloqueada</option>
                    <option value="extraviada">Extraviada</option>
                    <option value="disponible">Disponible</option>
                  </select>
                </label>
              </div>

              <div className="mpaz-tabla-contenedor">
                <table className="mpaz-tabla-directorio">
                  <thead>
                    <tr>
                      <th>Estudiante</th>
                      <th>Curso</th>
                      <th>Estado</th>
                      <th>Tarjeta RFID</th>
                      <th>Acción</th>
                    </tr>
                  </thead>
                  <tbody id="mpaz-directorio-filas">
                    <tr>
                      <td colSpan="5">Cargando estudiantes...</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <div className="mpaz-paginacion">
                <span id="mpaz-directorio-pagina">Página 1</span>
                <div>
                  <button type="button" id="mpaz-directorio-anterior">Anterior</button>
                  <button type="button" id="mpaz-directorio-siguiente">Siguiente</button>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* SECCIÓN TARJETAS RFID */}
        {vistaActiva === 'tarjetas' && (
          <section id="tarjetas" className="panel-lecturas">
            <h2>Administración de tarjetas RFID</h2>
            <p>Registra tarjetas RFID y consulta su estado dentro del sistema.</p>

            <details className="mpaz-registro-tarjeta">
              <summary>＋ Registrar nueva tarjeta RFID</summary>
              <div className="panel-administracion">
                <h3>Registrar nueva tarjeta</h3>
                <form id="formulario-tarjeta" onSubmit={(e) => e.preventDefault()}>
                  <label htmlFor="tarjeta-uid">UID</label>
                  <input type="text" id="tarjeta-uid" placeholder="Ej: A1B2C3D4" required />
                  <button type="submit">Registrar tarjeta</button>
                </form>
              </div>
            </details>

            <div className="mpaz-resumen-rfid">
              <div className="mpaz-kpi-rfid">
                <span>Total registradas</span>
                <strong id="mpaz-rfid-total">0</strong>
              </div>
              <div className="mpaz-kpi-rfid">
                <span>Activas</span>
                <strong id="mpaz-rfid-activas">0</strong>
              </div>
              <div className="mpaz-kpi-rfid">
                <span>Disponibles</span>
                <strong id="mpaz-rfid-disponibles">0</strong>
              </div>
              <div className="mpaz-kpi-rfid">
                <span>Bloqueadas</span>
                <strong id="mpaz-rfid-bloqueadas">0</strong>
              </div>
              <div className="mpaz-kpi-rfid">
                <span>Extraviadas</span>
                <strong id="mpaz-rfid-extraviadas">0</strong>
              </div>
            </div>

            <div className="mpaz-filtros-rfid">
              <label>
                Buscar tarjeta o estudiante
                <input type="search" id="mpaz-rfid-buscar" placeholder="UID o nombre" />
              </label>
              <label>
                Estado RFID
                <select id="mpaz-rfid-estado">
                  <option value="">Todos</option>
                  <option value="activa">Activa</option>
                  <option value="disponible">Disponible</option>
                  <option value="bloqueada">Bloqueada</option>
                  <option value="extraviada">Extraviada</option>
                </select>
              </label>
              <label>
                Curso
                <select id="mpaz-rfid-curso">
                  <option value="">Todos</option>
                </select>
              </label>
            </div>

            <h3>Tarjetas registradas</h3>
            <table className="tabla-lecturas">
              <thead>
                <tr>
                  <th>UID</th>
                  <th>Estado</th>
                  <th>Estudiante</th>
                  <th>Curso</th>
                  <th>Fecha registro</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody id="tabla-tarjetas">
                <tr>
                  <td colSpan="6">No hay tarjetas RFID registradas.</td>
                </tr>
              </tbody>
            </table>

            <div className="mpaz-paginacion-rfid">
              <span id="mpaz-rfid-pagina">Página 1 de 1</span>
              <div>
                <button type="button" id="mpaz-rfid-anterior">Anterior</button>
                <button type="button" id="mpaz-rfid-siguiente">Siguiente</button>
              </div>
            </div>
          </section>
        )}

        {/* SECCIÓN VINCULACIÓN */}
        {vistaActiva === 'vinculacion' && (
          <section id="vinculacion" className="panel-lecturas">
            <h2>Vinculación de tarjetas RFID</h2>
            <p>Asocia una tarjeta RFID disponible a un estudiante activo.</p>

            <div className="panel-administracion">
              <form id="formulario-vinculacion" onSubmit={(e) => e.preventDefault()}>
                <div className="mpaz-busqueda-vinculacion">
                  <label htmlFor="mpaz-buscar-alumno-vincular">Buscar estudiante por nombre o RUT</label>
                  <input
                    type="search"
                    id="mpaz-buscar-alumno-vincular"
                    placeholder="Escribe al menos 2 caracteres"
                    autoComplete="off"
                  />
                  <small>Selecciona una coincidencia o utiliza la lista de estudiantes.</small>
                </div>

                <label htmlFor="vinculacion-estudiante">Estudiante</label>
                <select id="vinculacion-estudiante" required>
                  <option value="">Selecciona un estudiante</option>
                </select>

                <label htmlFor="vinculacion-tarjeta">Tarjeta RFID disponible</label>
                <select id="vinculacion-tarjeta" required>
                  <option value="">Selecciona una tarjeta</option>
                </select>

                <div id="mpaz-resumen-vinculacion" className="mpaz-resumen-vinculacion" role="status">
                  Selecciona un estudiante y una tarjeta RFID.
                </div>

                <button type="submit">Vincular tarjeta</button>
              </form>
            </div>
          </section>
        )}

        {/* SECCIÓN INASISTENCIAS */}
        {vistaActiva === 'inasistencias' && (
          <section id="inasistencias" className="panel-lecturas">
            <h2>Registro de inasistencias</h2>
            <p>Consulta las inasistencias por día, semana o mes. Vista preliminar basada en fechas con registros RFID.</p>

            <div className="mpaz-aviso-inasistencias">
              <strong>Información preliminar</strong>
              <p>
                Las fechas consideradas se obtienen de las marcaciones existentes. Todavía no se han descontado suspensiones, feriados, justificaciones ni situaciones particulares de cada curso.
              </p>
            </div>

            <div className="filtros-periodo">
              <label htmlFor="periodo-inasistencias">Período:</label>
              <select id="periodo-inasistencias" defaultValue="mensual">
                <option value="diario">Diario</option>
                <option value="semanal">Semanal</option>
                <option value="mensual">Mensual</option>
              </select>

              <label htmlFor="fecha-inasistencias">Fecha de referencia:</label>
              <input type="date" id="fecha-inasistencias" />

              <button type="button" id="boton-filtrar-inasistencias">Consultar</button>
            </div>

            <table className="tabla-lecturas">
              <thead>
                <tr>
                  <th>Estudiante</th>
                  <th>Curso</th>
                  <th>Días sin marcación*</th>
                  <th>Fechas base</th>
                  <th>Revisión</th>
                </tr>
              </thead>
              <tbody id="tabla-inasistencias"></tbody>
            </table>
          </section>
        )}

        {/* SECCIÓN CALENDARIO */}
        {vistaActiva === 'calendario' && (
          <section id="calendario" className="panel-lecturas">
            <div className="mpaz-cal-cabecera">
              <div>
                <small>GESTIÓN ACADÉMICA</small>
                <h2>Calendario escolar</h2>
                <p>Administración de jornadas, suspensiones, feriados y horarios especiales.</p>
              </div>
              <span className="mpaz-cal-etiqueta">Vista preliminar</span>
            </div>

            <div className="mpaz-cal-aviso">
              <strong>Consulta de jornadas activa</strong>
              <p>Este calendario consulta las jornadas y su historial.</p>
            </div>

            <div className="mpaz-cal-layout">
              <div className="mpaz-cal-tarjeta">
                <div className="mpaz-cal-barra">
                  <div>
                    <small>CALENDARIO MENSUAL</small>
                    <h3 id="mpaz-cal-mes">Noviembre 2026</h3>
                  </div>
                  <div className="mpaz-cal-controles">
                    <button type="button" id="mpaz-cal-anterior">‹</button>
                    <button type="button" id="mpaz-cal-hoy">Hoy</button>
                    <button type="button" id="mpaz-cal-siguiente">›</button>
                  </div>
                </div>

                <label className="mpaz-cal-campo">
                  Curso
                  <select id="mpaz-cal-curso">
                    <option value="">Toda la escuela</option>
                  </select>
                </label>

                <div className="mpaz-cal-semana">
                  <span>Lun</span><span>Mar</span><span>Mié</span><span>Jue</span><span>Vie</span><span>Sáb</span><span>Dom</span>
                </div>
                <div className="mpaz-cal-cuadricula" id="mpaz-cal-cuadricula"></div>
              </div>

              <div className="mpaz-cal-tarjeta">
                <small>CONFIGURACIÓN ADMINISTRATIVA</small>
                <h3>Detalle de la jornada</h3>
                <div className="mpaz-cal-fecha-resumen">
                  <span>Fecha seleccionada</span>
                  <strong id="mpaz-cal-fecha-texto">—</strong>
                </div>

                <form id="mpaz-cal-formulario" onSubmit={(e) => e.preventDefault()}>
                  <label className="mpaz-cal-campo">
                    Fecha
                    <input id="mpaz-cal-fecha" type="date" required />
                  </label>
                  <label className="mpaz-cal-campo">
                    Condición
                    <select id="mpaz-cal-condicion">
                      <option value="lectiva">Lectiva</option>
                      <option value="suspendida">Suspensión</option>
                      <option value="feriado">Feriado</option>
                      <option value="reducida">Jornada reducida</option>
                      <option value="horario_especial">Horario especial</option>
                    </select>
                  </label>
                  <div className="mpaz-cal-horarios">
                    <label className="mpaz-cal-campo">
                      Entrada
                      <input id="mpaz-cal-entrada" type="time" />
                    </label>
                    <label className="mpaz-cal-campo">
                      Salida
                      <input id="mpaz-cal-salida" type="time" />
                    </label>
                  </div>
                  <label className="mpaz-cal-campo">
                    Motivo administrativo
                    <textarea id="mpaz-cal-motivo" rows="3" placeholder="Explica el motivo de la jornada"></textarea>
                  </label>
                  <button type="submit" id="mpaz-cal-guardar">Guardar jornada</button>
                </form>
              </div>
            </div>
          </section>
        )}

        {/* SECCIÓN ATRASOS */}
        {vistaActiva === 'atrasos' && (
          <section id="atrasos" className="panel-lecturas">
            <h2>Registro de atrasos</h2>
            <p>Se considera atraso cuando el estudiante registra su entrada después de las 08:20.</p>

            <div className="filtros-periodo">
              <label htmlFor="periodo-atrasos">Período:</label>
              <select id="periodo-atrasos" defaultValue="diario">
                <option value="diario">Diario</option>
                <option value="semanal">Semanal</option>
                <option value="mensual">Mensual</option>
              </select>

              <label htmlFor="fecha-atrasos">Fecha de referencia:</label>
              <input type="date" id="fecha-atrasos" />

              <button type="button" id="boton-filtrar-atrasos">Consultar</button>
            </div>

            <table className="tabla-lecturas">
              <thead>
                <tr>
                  <th>Fecha</th>
                  <th>Estudiante</th>
                  <th>Curso</th>
                  <th>Hora de llegada</th>
                  <th>Minutos de atraso</th>
                </tr>
              </thead>
              <tbody id="tabla-atrasos"></tbody>
            </table>
          </section>
        )}

        {/* SECCIÓN ANÁLISIS */}
        {vistaActiva === 'analisis' && (
          <section id="analisis" className="panel-lecturas">
            <h2>Análisis de datos</h2>
            <p>Resumen del porcentaje de asistencia por curso.</p>

            <div id="resumen-general-asistencia" className="resumen-general-asistencia">
              <div className="dato-resumen">
                <span className="dato-resumen-titulo">Estudiantes activos</span>
                <strong id="analisis-total-estudiantes">0</strong>
              </div>
              <div className="dato-resumen">
                <span className="dato-resumen-titulo">Presentes hoy</span>
                <strong id="analisis-total-presentes">0</strong>
              </div>
              <div className="dato-resumen">
                <span className="dato-resumen-titulo">Asistencia general</span>
                <strong id="analisis-porcentaje-general">0%</strong>
              </div>
            </div>
            <div id="resumen-analisis-asistencia" className="grid-analisis"></div>
          </section>
        )}

        {/* SECCIÓN REPORTES */}
        {vistaActiva === 'reportes' && (
          <section id="reportes" className="panel-lecturas">
            <h2>Reportes de asistencias</h2>
            <p>Desde aquí se pueden generar y descargar reportes de asistencias.</p>

            <label htmlFor="filtro-curso-reporte">Curso: </label>
            <select id="filtro-curso-reporte">
              <option value="">Todos los cursos</option>
            </select>

            <div className="opciones-reportes">
              <button type="button" id="reporte-diario">Reporte diario</button>
              <button type="button" id="reporte-semanal">Reporte semanal</button>
              <button type="button" id="reporte-mensual">Reporte mensual</button>
              <button type="button" id="reporte-anual">Reporte anual</button>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}