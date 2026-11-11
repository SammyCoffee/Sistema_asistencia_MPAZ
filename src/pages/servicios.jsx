import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../css/inicio.css';

export default function Servicios() {
  const [temaOscuro, setTemaOscuro] = useState(() => {
    const atributo = document.documentElement.getAttribute('data-mpaz-tema');
    return atributo ? atributo === 'oscuro' : false;
  });

  const toggleTema = () => {
    const nuevoTema = !temaOscuro;
    setTemaOscuro(nuevoTema);
    document.documentElement.setAttribute('data-mpaz-tema', nuevoTema ? 'oscuro' : 'claro');
  };

  const listaServicios = [
    {
      id: 1,
      titulo: 'Aula Virtual',
      icono: '💻',
      subtitulo: 'Plataforma Académica Online',
      descripcion: 'Acceso directo a clases virtuales, repositorios de guías de aprendizaje, tareas y material de estudio actualizado para estudiantes de todos los niveles.',
      esExterno: true,
      enlace: 'https://classroom.google.com/'
    },
    {
      id: 2,
      titulo: 'Notas y Certificados',
      icono: '📊',
      subtitulo: 'Seguimiento Académico',
      descripcion: 'Consulta de calificaciones en tiempo real, informes de notas parciales y descarga automatizada de certificados oficiales para apoderados y alumnos.',
      esExterno: false,
      enlace: '/login'
    },
    {
      id: 3,
      titulo: 'Convivencia Escolar',
      icono: '🤝',
      subtitulo: 'Apoyo Psicosocial y Orientación',
      descripcion: 'Canales directos de comunicación, orientación escolar, protocolos de buen trato y acompañamiento integral enfocado en el bienestar socioemocional.',
      esExterno: false,
      enlace: '/noticias'
    },
    {
      id: 4,
      titulo: 'Sistema MPAZ RFID',
      icono: '🆔',
      subtitulo: 'Seguridad y Control Institucional',
      descripcion: 'Tecnología avanzada de control de asistencia automatizada mediante credenciales RFID, asegurando un registro transparente y mayor tranquilidad para las familias.',
      esExterno: false,
      enlace: '/login'
    }
  ];

  return (
    <div className={`mpaz-portal-ref ${temaOscuro ? 'oscuro' : 'claro'}`}>
      
      {/* Topbar */}
      <div className="mpaz-ref-topbar">
        <div className="mpaz-ref-container mpaz-ref-topbar-inner">
          <div className="mpaz-ref-topbar-left">
            <span>Ramón Liborio Carvallo 736, San Bernardo, Región Metropolitana</span>
          </div>
          <div className="mpaz-ref-topbar-right">
            <button type="button" className="mpaz-ref-theme-toggle" onClick={toggleTema}>
              {temaOscuro ? 'Modo Claro' : 'Modo Oscuro'}
            </button>
            <Link to="/login" className="mpaz-ref-portal-link">Portal Interno</Link>
          </div>
        </div>
      </div>

      {/* Navbar */}
      <header className="mpaz-ref-navbar">
        <div className="mpaz-ref-container mpaz-ref-navbar-inner">
          <Link to="/" className="mpaz-ref-brand">
            <img src="/escudo-mpaz.webp" width="46" height="46" alt="Escudo" className="mpaz-ref-escudo" />
            <div className="mpaz-ref-brand-text">
              <span className="mpaz-ref-brand-sub">Escuela Escritora</span>
              <strong>Marcela Paz</strong>
            </div>
          </Link>
          <nav className="mpaz-ref-nav-links">
            <Link to="/">Inicio</Link>
            <Link to="/nuestra-escuela">Nuestra Escuela</Link>
            <Link to="/comunidad">Comunidad</Link>
            <Link to="/servicios" className="activo">Servicios</Link>
            <Link to="/noticias">Noticias</Link>
            <Link to="/contacto">Contacto</Link>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="mpaz-ref-main-content">
        <div className="mpaz-ref-container">
          
          <div className="mpaz-ref-section-header">
            <h2><span className="dot-yellow"></span> Plataformas y Servicios Digitales</h2>
          </div>
          <p style={{ fontSize: '1.05rem', color: 'var(--ref-text-muted)', marginBottom: '2.5rem', maxWidth: '850px' }}>
            Facilitamos la conectividad, la transparencia administrativa y el seguimiento académico mediante modernas herramientas tecnológicas diseñadas exclusivamente para nuestra comunidad.
          </p>
          
          {/* Listado en filas institucionales limpias */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', marginBottom: '3rem' }}>
            {listaServicios.map((servicio) => (
              <div 
                key={servicio.id}
                style={{ 
                  backgroundColor: 'var(--ref-surface)', 
                  border: '1px solid var(--ref-border)', 
                  borderRadius: '12px', 
                  padding: '1.75rem',
                  display: 'flex',
                  alignItems: 'flex-start',
                  justifyContent: 'space-between',
                  gap: '1.5rem',
                  flexWrap: 'wrap',
                  boxShadow: '0 4px 15px rgba(0,0,0,0.02)'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1.5rem', flex: 1, minWidth: '280px' }}>
                  <div style={{ fontSize: '2.5rem', background: 'rgba(245, 158, 11, 0.1)', padding: '0.8rem', borderRadius: '10px', lineHeight: 1 }}>
                    {servicio.icono}
                  </div>
                  <div>
                    <span style={{ fontSize: '0.78rem', fontWeight: '700', color: 'var(--ref-yellow)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                      {servicio.subtitulo}
                    </span>
                    <h3 style={{ fontSize: '1.25rem', fontWeight: '800', marginBottom: '0.5rem', color: 'var(--ref-text)' }}>
                      {servicio.titulo}
                    </h3>
                    <p style={{ color: 'var(--ref-text-muted)', fontSize: '0.95rem', lineHeight: '1.6', marginBottom: 0 }}>
                      {servicio.descripcion}
                    </p>
                  </div>
                </div>
                
                <div style={{ alignSelf: 'center' }}>
                  {servicio.esExterno ? (
                    <a 
                      href={servicio.enlace} 
                      target="_blank" 
                      rel="noopener noreferrer" 
                      className="mpaz-ref-btn-yellow" 
                      style={{ padding: '0.6rem 1.2rem', fontSize: '0.88rem', textDecoration: 'none' }}
                    >
                      Acceder al servicio ›
                    </a>
                  ) : (
                    <Link to={servicio.enlace} className="mpaz-ref-btn-yellow" style={{ padding: '0.6rem 1.2rem', fontSize: '0.88rem' }}>
                      Acceder al servicio ›
                    </Link>
                  )}
                </div>
              </div>
            ))}
          </div>

        </div>
      </main>

      {/* Footer */}
      <footer className="mpaz-ref-footer" id="contacto">
        <div className="mpaz-ref-container mpaz-ref-footer-grid-cols">
          <div className="mpaz-ref-footer-col">
            <div className="mpaz-ref-footer-brand">
              <img src="/escudo-mpaz.webp" width="42" height="42" alt="Escudo" className="mpaz-ref-escudo" />
              <div>
                <h3>Escuela Escritora Marcela Paz</h3>
                <span>San Bernardo · Región Metropolitana</span>
              </div>
            </div>
          </div>

          <div className="mpaz-ref-footer-col">
            <h4>Navegación</h4>
            <div className="links-vertical">
              <Link to="/">Inicio</Link>
              <Link to="/nuestra-escuela">Nuestra Escuela</Link>
              <Link to="/comunidad">Comunidad Educativa</Link>
              <Link to="/noticias">Galería de Noticias</Link>
            </div>
          </div>

          <div className="mpaz-ref-footer-col">
            <h4>Plataformas</h4>
            <div className="links-vertical">
              <Link to="/login">Portal Administrativo</Link>
              <Link to="/login">Portal Docente</Link>
              <Link to="/servicios">Certificados y Notas</Link>
              <Link to="/contacto">Soporte Técnico</Link>
            </div>
          </div>

          <div className="mpaz-ref-footer-col">
            <h4>Contacto y Ubicación</h4>
            <ul className="footer-contact-list">
              <li>📍 Ramón Liborio Carvallo 736, San Bernardo</li>
              <li>🕒 Lunes a Viernes: 08:00 – 17:30 hrs</li>
              <li>✉️ Atenciones vía formulario web oficial</li>
            </ul>
          </div>
        </div>

        <div className="mpaz-ref-footer-bottom">
          <div className="mpaz-ref-container mpaz-ref-footer-bottom-inner">
            <span>© {new Date().getFullYear()} Escuela Escritora Marcela Paz. Todos los derechos reservados.</span>
            <span>Sistema Institucional MPAZ RFID</span>
          </div>
        </div>
      </footer>

    </div>
  );
}