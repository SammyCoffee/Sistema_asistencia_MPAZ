import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../css/inicio.css';

export default function NuestraEscuela() {
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
            <Link to="/nuestra-escuela" className="activo">Nuestra Escuela</Link>
            <Link to="/comunidad">Comunidad</Link>
            <Link to="/servicios">Servicios</Link>
            <Link to="/noticias">Noticias</Link>
            <Link to="/contacto">Contacto</Link>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="mpaz-ref-main-content">
        <div className="mpaz-ref-container">
          <div className="mpaz-ref-section-header">
            <h2><span className="dot-yellow"></span> Conoce Nuestra Escuela</h2>
          </div>
          <p style={{ fontSize: '1.05rem', color: 'var(--ref-text-muted)', marginBottom: '2.5rem' }}>
            Un recorrido por nuestra identidad, el compromiso de nuestra comunidad y el entorno donde día a día fomentamos el aprendizaje.
          </p>

          {/* Misión y Visión */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '2rem', marginBottom: '3rem' }}>
            <div className="mpaz-ref-school-card" style={{ marginBottom: 0 }}>
              <h2>Misión</h2>
              <p>
                Brindar una educación integral, inclusiva y de calidad a todos nuestros estudiantes, potenciando sus habilidades académicas, artísticas y valóricas en un ambiente de sana convivencia y respeto mutuo.
              </p>
            </div>
            <div className="mpaz-ref-school-card" style={{ marginBottom: 0 }}>
              <h2>Visión</h2>
              <p>
                Ser una institución educativa líder en la comuna de San Bernardo, reconocida por su constante innovación pedagógica, su compromiso con el desarrollo de la comunidad y la formación de personas íntegras y preparadas para el futuro.
              </p>
            </div>
          </div>

          {/* Historia y Ubicación */}
          <div className="mpaz-ref-school-card" style={{ marginBottom: '3rem' }}>
            <h2>Nuestra Historia y Ubicación</h2>
            <p>
              La Escuela Escritora Marcela Paz, ubicada en <strong>Ramón Liborio Carvallo 736, San Bernardo</strong>, se enfoca en entregar una formación cercana y de excelencia. Contamos con espacios adaptados para el bienestar, la cultura y el deporte de las nuevas generaciones.
            </p>
          </div>

          {/* Sección del Video de Dron (Sin recortes, controles 100% visibles) */}
          <div style={{ marginBottom: '3rem' }}>
            <h3 style={{ fontSize: '1.25rem', marginBottom: '1rem', fontWeight: '700' }}>Vista Aérea Institucional</h3>
            <div style={{ 
              width: '100%', 
              aspectRatio: '16 / 9',
              maxHeight: '500px',
              borderRadius: '12px', 
              overflow: 'hidden', 
              boxShadow: '0 10px 25px -5px rgba(0,0,0,0.1)',
              backgroundColor: '#000'
            }}>
              <iframe 
                src="https://drive.google.com/file/d/1zhknOnrWk_3AJPrX-cPJtYeRuLazXAbZ/preview" 
                width="100%" 
                height="100%" 
                style={{ border: 0 }} 
                allow="autoplay"
                allowFullScreen
                title="Video Dron Escuela Marcela Paz"
              ></iframe>
            </div>
          </div>

          {/* Mapa de Ubicación Google Maps */}
          <div>
            <h3 style={{ fontSize: '1.25rem', marginBottom: '1rem', fontWeight: '700' }}>Ubicación en el Mapa</h3>
            <div style={{ width: '100%', height: '400px', borderRadius: '12px', overflow: 'hidden', border: '1px solid var(--ref-border)' }}>
              <iframe 
                title="Mapa Escuela Marcela Paz"
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3323.856!2d-70.701!3d-33.592!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMzPCsDM1JzMxLjIiUyA3MMKwNDInMDMuNiJX!5e0!3m2!1ses!2scl!4v1650000000000!5m2!1ses!2scl" 
                width="100%" 
                height="100%" 
                style={{ border: 0 }} 
                allowFullScreen="" 
                loading="lazy">
              </iframe>
            </div>
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