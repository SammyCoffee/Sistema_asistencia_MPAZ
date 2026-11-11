import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../css/inicio.css';

// Importación de fotos desde tu carpeta assets
import imgCarousel1 from '../assets/carousel (1).jpg';
import imgCarousel2 from '../assets/carousel (2).jpg';
import imgCarousel3 from '../assets/carousel (3).jpg';

export default function Inicio() {
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
      
      {/* 1. TOPBAR INSTITUCIONAL SUPERIOR */}
      <div className="mpaz-ref-topbar">
        <div className="mpaz-ref-container mpaz-ref-topbar-inner">
          <div className="mpaz-ref-topbar-left">
            <span>Ramón Liborio Carvallo 736, San Bernardo, Región Metropolitana</span>
          </div>
          <div className="mpaz-ref-topbar-right">
            <button 
              type="button" 
              className="mpaz-ref-theme-toggle" 
              onClick={toggleTema}
              aria-label="Cambiar tema"
            >
              {temaOscuro ? 'Modo Claro' : 'Modo Oscuro'}
            </button>
            <Link to="/login" className="mpaz-ref-portal-link">
              Portal Interno
            </Link>
          </div>
        </div>
      </div>

      {/* 2. NAVBAR PRINCIPAL CON EL LOGO DEL COLEGIO */}
      <header className="mpaz-ref-navbar">
        <div className="mpaz-ref-container mpaz-ref-navbar-inner">
          <Link to="/" className="mpaz-ref-brand">
            <img 
              src="/escudo-mpaz.webp" 
              width="46" 
              height="46" 
              alt="Escudo Escuela Escritora Marcela Paz" 
              className="mpaz-ref-escudo" 
            />
            <div className="mpaz-ref-brand-text">
              <span className="mpaz-ref-brand-sub">Escuela Escritora</span>
              <strong>Marcela Paz</strong>
            </div>
          </Link>

          <nav className="mpaz-ref-nav-links">
            <Link to="/" className="activo">Inicio</Link>
            <Link to="/nuestra-escuela">Nuestra Escuela</Link>
            <Link to="/comunidad">Comunidad</Link>
            <Link to="/servicios">Servicios</Link>
            <Link to="/noticias">Noticias</Link>
            <Link to="/contacto">Contacto</Link>
          </nav>
        </div>
      </header>

      <main id="inicio">
        
        {/* 3. HERO BANNER PRINCIPAL */}
        <section className="mpaz-ref-hero">
          <div className="mpaz-ref-hero-bg">
            <img src={imgCarousel2} alt="Estudiantes Escuela Marcela Paz" />
            <div className="mpaz-ref-hero-gradient"></div>
          </div>

          <div className="mpaz-ref-container mpaz-ref-hero-content">
            <span className="mpaz-ref-hero-kicker">EXCELENCIA Y VALORES • SAN BERNARDO</span>
            <h1>Educación integral y cercana <br /><span>para grandes historias</span></h1>
            <p>
              Un espacio educativo inclusivo y moderno donde promovemos el desarrollo académico, artístico y tecnológico de cada uno de nuestros estudiantes desde sus primeros niveles formativos.
            </p>
            <div className="mpaz-ref-hero-buttons">
              <Link to="/contacto" className="mpaz-ref-btn-yellow">
                Proceso de Admisión
              </Link>
              <Link to="/nuestra-escuela" className="mpaz-ref-btn-outline-white">
                Conoce Nuestra Escuela
              </Link>
            </div>
          </div>
        </section>

        {/* 4. BARRA DE ACCESOS RÁPIDOS */}
        <div className="mpaz-ref-quick-bar">
          <div className="mpaz-ref-container mpaz-ref-quick-grid">
            <Link to="/contacto" className="mpaz-ref-quick-item">
              <span>Admisión</span> <span className="arrow">›</span>
            </Link>
            <Link to="/noticias" className="mpaz-ref-quick-item">
              <span>Noticias</span> <span className="arrow">›</span>
            </Link>
            <Link to="/servicios" className="mpaz-ref-quick-item">
              <span>Calendario</span> <span className="arrow">›</span>
            </Link>
            <Link to="/comunidad" className="mpaz-ref-quick-item">
              <span>PIE</span> <span className="arrow">›</span>
            </Link>
            <Link to="/contacto" className="mpaz-ref-quick-item">
              <span>Contacto</span> <span className="arrow">›</span>
            </Link>
          </div>
        </div>

        {/* 5. SECCIÓN DE CONTENIDO PRINCIPAL */}
        <section className="mpaz-ref-main-content" id="noticias">
          <div className="mpaz-ref-container mpaz-ref-grid-layout">
            
            {/* Columna Izquierda: Últimas Noticias */}
            <div className="mpaz-ref-news-column">
              <div className="mpaz-ref-section-header">
                <h2><span className="dot-yellow"></span> Últimas Noticias y Eventos</h2>
                <Link to="/noticias" className="mpaz-ref-ver-todas">Ver todas ›</Link>
              </div>

              <div className="mpaz-ref-news-grid">
                
                {/* Noticia 1 */}
                <article className="mpaz-ref-news-card">
                  <div className="mpaz-ref-news-img">
                    <img src={imgCarousel1} alt="Infraestructura" />
                    <span className="mpaz-ref-badge-libros">Infraestructura</span>
                  </div>
                  <div className="mpaz-ref-news-body">
                    <span className="mpaz-ref-date">06 de Octubre de 2026</span>
                    <h3>Modernización de nuestra sede escolar</h3>
                    <p>Continuamos mejorando nuestras dependencias para brindar mayor comodidad y seguridad a toda nuestra comunidad durante la jornada escolar.</p>
                  </div>
                </article>

                {/* Noticia 2 */}
                <article className="mpaz-ref-news-card">
                  <div className="mpaz-ref-news-img">
                    <img src={imgCarousel2} alt="Celebración Fiestas Patrias" />
                    <span className="mpaz-ref-badge-libros">Tradición</span>
                  </div>
                  <div className="mpaz-ref-news-body">
                    <span className="mpaz-ref-date">17 de Septiembre de 2026</span>
                    <h3>Gran celebración de Fiestas Patrias</h3>
                    <p>Estudiantes, docentes y apoderados se unieron en una inolvidable jornada llena de bailes típicos, música y muestras de nuestras tradiciones chilenas.</p>
                  </div>
                </article>

                {/* Noticia 3 */}
                <article className="mpaz-ref-news-card">
                  <div className="mpaz-ref-news-img">
                    <img src={imgCarousel3} alt="Día del Alumno" />
                    <span className="mpaz-ref-badge-libros">Comunidad</span>
                  </div>
                  <div className="mpaz-ref-news-body">
                    <span className="mpaz-ref-date">05 de Junio de 2026</span>
                    <h3>Actividades especiales por el Día del Alumno</h3>
                    <p>Una jornada recreativa llena de sorpresas, juegos y momentos de sana convivencia preparados con mucho cariño para reconocer a nuestros estudiantes.</p>
                  </div>
                </article>

              </div>
            </div>

            {/* Columna Derecha: Nuestra Escuela y Servicios */}
            <div className="mpaz-ref-sidebar-column">
              
              {/* Tarjeta Nuestra Escuela */}
              <div className="mpaz-ref-school-card" id="nosotros">
                <h2><span className="dot-yellow"></span> Nuestra Escuela</h2>
                <p>
                  En la Escuela Escritora Marcela Paz fomentamos un ambiente educativo cálido y participativo. Nuestro equipo docente trabaja día a día para entregar herramientas pedagógicas que potencien el pensamiento crítico, la creatividad y los valores ciudadanos de cada alumno.
                </p>
                <Link to="/nuestra-escuela" className="mpaz-ref-btn-yellow-outline">
                  Conoce más sobre nosotros ›
                </Link>
              </div>

              {/* Plataformas y Servicios (Filas limpias institucionales) */}
              <div className="mpaz-ref-services-box" id="servicios">
                <h2><span className="dot-yellow"></span> Plataformas y Servicios</h2>
                
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
                  
                  {/* Item 1: Classroom */}
                  <a 
                    href="https://classroom.google.com/" 
                    target="_blank" 
                    rel="noopener noreferrer" 
                    className="mpaz-ref-service-row"
                  >
                    <div className="mpaz-ref-service-icon">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
                        <line x1="8" y1="21" x2="16" y2="21"></line>
                        <line x1="12" y1="17" x2="12" y2="21"></line>
                      </svg>
                    </div>
                    <div className="mpaz-ref-service-info">
                      <strong>Aula Virtual</strong>
                      <span>Acceso a Google Classroom</span>
                    </div>
                    <span className="mpaz-ref-service-arrow">↗</span>
                  </a>

                  {/* Item 2: Notas */}
                  <Link to="/servicios" className="mpaz-ref-service-row">
                    <div className="mpaz-ref-service-icon">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                        <polyline points="14 2 14 8 20 8"></polyline>
                        <line x1="16" y1="13" x2="8" y2="13"></line>
                        <line x1="16" y1="17" x2="8" y2="17"></line>
                      </svg>
                    </div>
                    <div className="mpaz-ref-service-info">
                      <strong>Notas y Certificados</strong>
                      <span>Informes y documentación</span>
                    </div>
                    <span className="mpaz-ref-service-arrow">›</span>
                  </Link>

                  {/* Item 3: Convivencia */}
                  <Link to="/comunidad" className="mpaz-ref-service-row">
                    <div className="mpaz-ref-service-icon">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                        <circle cx="9" cy="7" r="4"></circle>
                        <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                        <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                      </svg>
                    </div>
                    <div className="mpaz-ref-service-info">
                      <strong>Convivencia Escolar</strong>
                      <span>Orientación y reglamentos</span>
                    </div>
                    <span className="mpaz-ref-service-arrow">›</span>
                  </Link>

                  {/* Item 4: Admisión */}
                  <Link to="/contacto" className="mpaz-ref-service-row">
                    <div className="mpaz-ref-service-icon">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>
                        <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
                      </svg>
                    </div>
                    <div className="mpaz-ref-service-info">
                      <strong>Admisión 2026</strong>
                      <span>Postulaciones y matrículas</span>
                    </div>
                    <span className="mpaz-ref-service-arrow">›</span>
                  </Link>

                </div>
              </div>

            </div>

          </div>
        </section>

      </main>

      {/* 6. FOOTER INSTITUCIONAL MULTI-COLUMNA */}
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
              Síguenos en nuestras redes oficiales para estar al tanto de todas las actividades escolares y eventos comunitarios.
            </p>
            <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
              <a href="https://www.instagram.com/escuelampaz/" target="_blank" rel="noopener noreferrer" style={{ color: 'var(--ref-yellow)', fontWeight: '700', fontSize: '0.85rem', textDecoration: 'none' }}>
                Instagram ↗
              </a>
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