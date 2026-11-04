import React, { useState } from 'react';
import { Link } from 'react-router-dom';
// ¡Ya no necesitamos importar la imagen arriba!

export default function Inicio() {
  const [temaOscuro, setTemaOscuro] = useState(false);

  const toggleTema = () => {
    setTemaOscuro(!temaOscuro);
    document.documentElement.setAttribute('data-mpaz-tema', !temaOscuro ? 'oscuro' : 'claro');
  };

  return (
    <div className={`mpaz-portales ${temaOscuro ? 'oscuro' : ''}`}>
      <header className="mpaz-portales-cabecera">
        <Link className="mpaz-identidad-link" to="/" aria-label="Inicio de MPAZ RFID">
          <img className="mpaz-sello mpaz-escudo" src="/escudo-mpaz.webp" width="49" height="49" alt="Escudo de la Escuela" />
          <span className="mpaz-identidad-texto">
            <strong>Escuela Escritora Marcela Paz</strong>
            <small>San Bernardo · Plataforma institucional</small>
          </span>
        </Link>
        <div className="mpaz-portales-herramientas">
          <span className="mpaz-encabezado-distintivo">SISTEMA MPAZ RFID</span>
          <button 
            type="button" 
            className="mpaz-tema-rapido" 
            onClick={toggleTema}
            aria-label="Activar tema oscuro" 
            aria-pressed={temaOscuro}
          >
            ☾ <span>{temaOscuro ? 'Modo claro' : 'Modo oscuro'}</span>
          </button>
        </div>
      </header>

      <main className="mpaz-portales-principal">
        <section className="mpaz-portales-hero" aria-labelledby="mpaz-titulo-hero">
          <div className="mpaz-portales-presentacion">
            <span className="mpaz-etiqueta mpaz-etiqueta-hero">TECNOLOGÍA AL SERVICIO DE LA EDUCACIÓN</span>
            <h1 id="mpaz-titulo-hero">Gestión escolar <span>más conectada.</span></h1>
            <p>Bienvenido a MPAZ RFID, la plataforma de gestión de asistencia de nuestra comunidad educativa. Selecciona tu espacio de trabajo para continuar.</p>
          </div>
          <div className="mpaz-portales-grafico" aria-hidden="true">
            <div className="mpaz-orbita mpaz-orbita-uno"></div>
            <div className="mpaz-orbita mpaz-orbita-dos"></div>
            <div className="mpaz-grafico-tarjeta">
              <span className="mpaz-grafico-mini">ESCUELA ESCRITORA MARCELA PAZ</span>
              <img className="mpaz-grafico-sello mpaz-escudo-grafico" src="/escudo-mpaz.webp" width="82" height="82" alt="" />
              <strong>MPAZ <em>RFID</em></strong>
              <small>Asistencia · Comunidad · Innovación</small>
            </div>
            <span className="mpaz-grafico-punto mpaz-grafico-punto-uno"></span>
            <span className="mpaz-grafico-punto mpaz-grafico-punto-dos"></span>
          </div>
        </section>

        <section id="accesos" className="mpaz-portal-accesos" aria-labelledby="mpaz-titulo-accesos">
          <div className="mpaz-portales-titulos">
            <div>
              <span className="mpaz-etiqueta">ACCESOS INSTITUCIONALES</span>
              <h2 id="mpaz-titulo-accesos">¿A qué portal deseas ingresar?</h2>
              <p>Dos espacios de trabajo, una misma plataforma escolar.</p>
            </div>
          </div>
          <div className="mpaz-portal-tarjetas">
            <article className="mpaz-portal-tarjeta mpaz-portal-tarjeta-admin">
              <div className="mpaz-portal-tarjeta-arriba">
                <span className="mpaz-portal-icono" aria-hidden="true">⚙</span>
                <span className="mpaz-portal-numero">01 / GESTIÓN</span>
              </div>
              <h3>Administración</h3>
              <p>Gestiona estudiantes, tarjetas RFID, asistencias, calendario y reportes del establecimiento.</p>
              <Link className="mpaz-portal-boton" to="/login">Ingresar a administración <span aria-hidden="true">↗</span></Link>
            </article>
            <article className="mpaz-portal-tarjeta mpaz-portal-tarjeta-docente">
              <div className="mpaz-portal-tarjeta-arriba">
                <span className="mpaz-portal-icono" aria-hidden="true">▤</span>
                <span className="mpaz-portal-numero">02 / AULA</span>
              </div>
              <h3>Portal docente</h3>
              <p>Consulta cursos, asignaturas y estudiantes asignados, y gestiona la asistencia de tus clases.</p>
              <Link className="mpaz-portal-boton" to="/login">Ingresar como docente <span aria-hidden="true">↗</span></Link>
            </article>
          </div>
        </section>
      </main>

      <footer className="mpaz-portales-pie">
        <span>Escuela Escritora Marcela Paz · San Bernardo</span>
        <span>MPAZ RFID · Sistema de gestión escolar</span>
      </footer>
    </div>
  );
}