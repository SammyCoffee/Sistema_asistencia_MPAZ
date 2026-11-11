import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../css/inicio.css';

export default function Contacto() {
  const [temaOscuro, setTemaOscuro] = useState(() => {
    const atributo = document.documentElement.getAttribute('data-mpaz-tema');
    return atributo ? atributo === 'oscuro' : false;
  });

  const toggleTema = () => {
    const nuevoTema = !temaOscuro;
    setTemaOscuro(nuevoTema);
    document.documentElement.setAttribute('data-mpaz-tema', nuevoTema ? 'oscuro' : 'claro');
  };

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
            <Link to="/servicios">Servicios</Link>
            <Link to="/noticias">Noticias</Link>
            <Link to="/contacto" className="activo">Contacto</Link>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="mpaz-ref-main-content">
        <div className="mpaz-ref-container">
          <div className="mpaz-ref-section-header">
            <h2><span className="dot-yellow"></span> Contacto y Atención Institucional</h2>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '2rem', marginBottom: '2.5rem' }}>
            <div style={{ background: 'var(--ref-surface)', padding: '2rem', borderRadius: '12px', border: '1px solid var(--ref-border)', boxShadow: '0 10px 25px -5px rgba(0,0,0,0.04)' }}>
              <h3 style={{ color: 'var(--ref-blue-primary)', marginBottom: '1rem', fontSize: '1.2rem' }}>📍 Ubicación y Dirección</h3>
              <p style={{ color: 'var(--ref-text-muted)', lineHeight: '1.6', marginBottom: '1rem' }}>
                <strong>Dirección:</strong> Ramón Liborio Carvallo 736, 8071614 San Bernardo, Región Metropolitana.
              </p>
              <p style={{ color: 'var(--ref-text-muted)', lineHeight: '1.6' }}>
                <strong>Horario de atención:</strong> Lunes a Viernes de 08:00 a 17:00 hrs.
              </p>
            </div>
            
            <div style={{ background: 'var(--ref-surface)', padding: '2rem', borderRadius: '12px', border: '1px solid var(--ref-border)', boxShadow: '0 10px 25px -5px rgba(0,0,0,0.04)' }}>
              <h3 style={{ color: 'var(--ref-blue-primary)', marginBottom: '1rem', fontSize: '1.2rem' }}>📞 Canales de Comunicación</h3>
              <p style={{ color: 'var(--ref-text-muted)', lineHeight: '1.6', marginBottom: '1rem' }}>
                <strong>Admisión y Matrículas:</strong> admision@escuelamarcelapaz.cl
              </p>
              <p style={{ color: 'var(--ref-text-muted)', lineHeight: '1.6' }}>
                <strong>Soporte Técnico / Sistema MPAZ RFID:</strong> soporte@escuelamarcelapaz.cl
              </p>
            </div>
          </div>

          {/* MAPA ADORNADO E INTEGRADO CON UBICACIÓN REAL */}
          <div style={{ background: 'var(--ref-surface)', padding: '2rem', borderRadius: '16px', border: '1px solid var(--ref-border)', boxShadow: '0 10px 25px -5px rgba(0,0,0,0.04)' }}>
            <h3 style={{ color: 'var(--ref-blue-primary)', marginBottom: '0.75rem', fontSize: '1.3rem' }}>🗺️ Encuéntranos en el Mapa</h3>
            <p style={{ color: 'var(--ref-text-muted)', marginBottom: '1.5rem' }}>
              Puedes planificar tu ruta fácilmente directamente desde Google Maps a través del siguiente mapa interactivo:
            </p>
            <div style={{ width: '100%', height: '420px', borderRadius: '12px', overflow: 'hidden', border: '1px solid var(--ref-border)' }}>
              <iframe 
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3322.963314799056!2d-70.70925072343627!3d-33.60625630550935!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x9662d937dc47cbfb%3A0x812a0859c7319df1!2sRam%C3%B3n%20Liborio%20Carvallo%20736%2C%208071614%20San%20Bernardo%2C%20Regi%C3%B3n%20Metropolitana!5e0!3m2!1ses-419!2scl!4v1794268651708!5m2!1ses-419!2scl" 
                width="100%" 
                height="100%" 
                style={{ border: 0 }} 
                allowFullScreen="" 
                loading="lazy" 
                referrerPolicy="strict-origin-when-cross-origin"
                title="Mapa de Contacto Escuela Marcela Paz"
              ></iframe>
            </div>
          </div>

        </div>
        {/* SECCIÓN BONITA DE REDES SOCIALES EN CONTACTO */}
          <div 
            style={{ 
              backgroundColor: 'var(--ref-surface)', 
              border: '1px solid var(--ref-border)', 
              borderRadius: '16px', 
              padding: '2.5rem', 
              textAlign: 'center', 
              marginBottom: '3.5rem',
              boxShadow: '0 10px 30px rgba(0,0,0,0.03)'
            }}
          >
            <span style={{ fontSize: '0.78rem', fontWeight: '800', color: 'var(--ref-yellow)', textTransform: 'uppercase', letterSpacing: '0.1em' }}>
              CONÉCTATE CON NOSOTROS
            </span>
            <h3 style={{ fontSize: '1.5rem', fontWeight: '800', margin: '0.5rem 0 1rem 0', color: 'var(--ref-text)' }}>
              Visítanos y síguenos en nuestras redes sociales
            </h3>
            <p style={{ color: 'var(--ref-text-muted)', fontSize: '0.95rem', maxWidth: '600px', margin: '0 auto 2rem auto', lineHeight: '1.6' }}>
              Entérate de todas las actividades, galerías fotográficas, avisos importantes y el día a día de nuestra comunidad escolar de manera directa.
            </p>

            <div style={{ display: 'flex', justifyContent: 'center', gap: '1.25rem', flexWrap: 'wrap' }}>
              {/* Botón Instagram */}
              <a 
                href="https://www.instagram.com/escuelampaz/" 
                target="_blank" 
                rel="noopener noreferrer" 
                style={{ 
                  display: 'inline-flex', 
                  alignItems: 'center', 
                  gap: '0.75rem', 
                  background: 'linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%)',
                  color: '#ffffff', 
                  padding: '0.85rem 1.75rem', 
                  borderRadius: '10px', 
                  fontWeight: '700', 
                  fontSize: '0.95rem',
                  textDecoration: 'none',
                  boxShadow: '0 4px 15px rgba(220, 39, 67, 0.25)',
                  transition: 'transform 0.2s ease, opacity 0.2s ease'
                }}
              >
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>
                <span>Síguenos en Instagram</span>
              </a>

              {/* Botón Facebook */}
              <a 
                href="https://www.facebook.com/EscuelaMPaz/?locale=es_LA" 
                target="_blank" 
                rel="noopener noreferrer" 
                style={{ 
                  display: 'inline-flex', 
                  alignItems: 'center', 
                  gap: '0.75rem', 
                  backgroundColor: '#1877F2',
                  color: '#ffffff', 
                  padding: '0.85rem 1.75rem', 
                  borderRadius: '10px', 
                  fontWeight: '700', 
                  fontSize: '0.95rem',
                  textDecoration: 'none',
                  boxShadow: '0 4px 15px rgba(24, 119, 242, 0.25)',
                  transition: 'transform 0.2s ease, opacity 0.2s ease'
                }}
              >
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg>
                <span>Visítanos en Facebook</span>
              </a>
            </div>
          </div>
      </main>

      {/* Footer Unificado con Redes Sociales */}
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
            <p className="mpaz-ref-footer-desc" style={{ marginTop: '0.75rem', fontSize: '0.84rem' }}>
              Síguenos en nuestras redes oficiales para estar al tanto de todas las actividades escolares.
            </p>
            <div style={{ display: 'flex', gap: '0.75rem', marginTop: '1rem' }}>
              <a href="https://www.instagram.com/escuelampaz/" target="_blank" rel="noopener noreferrer" style={{ color: 'var(--ref-yellow)', fontWeight: '700', fontSize: '0.85rem', textDecoration: 'none' }}>
                Instagram ↗
              </a>
              <span style={{ color: '#64748b' }}>•</span>
              <a href="https://www.facebook.com/EscuelaMPaz/?locale=es_LA" target="_blank" rel="noopener noreferrer" style={{ color: 'var(--ref-yellow)', fontWeight: '700', fontSize: '0.85rem', textDecoration: 'none' }}>
                Facebook ↗
              </a>
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