import React, { useState } from 'react';
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
            <span>Ramón Liborio Carvallo 736, 8071614 San Bernardo, Región Metropolitana</span>
            <span></span>
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
            <div className="mpaz-ref-portal-link">
              Portal Interno
            </div>
          </div>
        </div>
      </div>

      {/* 2. NAVBAR PRINCIPAL CON EL LOGO DEL COLEGIO */}
      <header className="mpaz-ref-navbar">
        <div className="mpaz-ref-container mpaz-ref-navbar-inner">
          <div className="mpaz-ref-brand">
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
          </div>

          <nav className="mpaz-ref-nav-links">
            <span className="activo">Inicio</span>
            <span>Nuestra Escuela</span>
            <span>Comunidad</span>
            <span>Servicios</span>
            <span>Noticias</span>
            <span>Contacto</span>
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
            <span className="mpaz-ref-hero-kicker">ESCUELA ESCRITORA MARCELA PAZ</span>
            <h1>Educación integral <br /><span>para grandes historias</span></h1>
            <p>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            </p>
            <div className="mpaz-ref-hero-buttons">
              <div className="mpaz-ref-btn-yellow">
                Matrículas
              </div>
              <div className="mpaz-ref-btn-outline-white">
                Portal Interno
              </div>
            </div>
          </div>
        </section>

        {/* 4. BARRA DE ACCESOS RÁPIDOS */}
        <div className="mpaz-ref-quick-bar">
          <div className="mpaz-ref-container mpaz-ref-quick-grid">
            <div className="mpaz-ref-quick-item">
              <span>Admisión</span> <span className="arrow">›</span>
            </div>
            <div className="mpaz-ref-quick-item">
              <span>Noticias</span> <span className="arrow">›</span>
            </div>
            <div className="mpaz-ref-quick-item">
              <span>Calendario</span> <span className="arrow">›</span>
            </div>
            <div className="mpaz-ref-quick-item">
              <span>PIE</span> <span className="arrow">›</span>
            </div>
            <div className="mpaz-ref-quick-item">
              <span>Contacto</span> <span className="arrow">›</span>
            </div>
          </div>
        </div>

        {/* 5. SECCIÓN DE CONTENIDO PRINCIPAL */}
        <section className="mpaz-ref-main-content" id="noticias">
          <div className="mpaz-ref-container mpaz-ref-grid-layout">
            
            {/* Columna Izquierda: Últimas Noticias */}
            <div className="mpaz-ref-news-column">
              <div className="mpaz-ref-section-header">
                <h2><span className="dot-yellow"></span> Últimas Noticias</h2>
                <span className="mpaz-ref-ver-todas">Ver todas ›</span>
              </div>

              <div className="mpaz-ref-news-grid">
                
                {/* Noticia 1 */}
                <article className="mpaz-ref-news-card">
                  <div className="mpaz-ref-news-img">
                    <img src={imgCarousel1} alt="Instalaciones" />
                    <span className="mpaz-ref-badge-libros">Sede</span>
                  </div>
                  <div className="mpaz-ref-news-body">
                    <span className="mpaz-ref-date">06 de Octubre de 2026</span>
                    <h3>Nuestra sede</h3>
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.</p>
                    <div className="mpaz-ref-leer-mas">Leer más ›</div>
                  </div>
                </article>

                {/* Noticia 2 */}
                <article className="mpaz-ref-news-card">
                  <div className="mpaz-ref-news-img">
                    <img src={imgCarousel2} alt="Huerto Escolar" />
                  </div>
                  <div className="mpaz-ref-news-body">
                    <span className="mpaz-ref-date">15 de abril de 2025</span>
                    <h3>TEXTO</h3>
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore.</p>
                    <div className="mpaz-ref-leer-mas">Leer más ›</div>
                  </div>
                </article>

                {/* Noticia 3 */}
                <article className="mpaz-ref-news-card">
                  <div className="mpaz-ref-news-img">
                    <img src={imgCarousel3} alt="Academias" />
                  </div>
                  <div className="mpaz-ref-news-body">
                    <span className="mpaz-ref-date">10 de abril de 2025</span>
                    <h3>TEXTO</h3>
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia.</p>
                    <div className="mpaz-ref-leer-mas">Leer más ›</div>
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
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Integer vitae justo eget magna fermentum iaculis.
                </p>
                <div className="mpaz-ref-btn-yellow-outline">
                  Conoce más sobre nosotros ›
                </div>
              </div>

              {/* Plataformas y Servicios Destacados */}
              <div className="mpaz-ref-services-box" id="servicios">
                <h2><span className="dot-yellow"></span> Plataformas y Servicios Destacados</h2>
                
                <div className="mpaz-ref-services-grid">
                  <div className="mpaz-ref-service-item">
                    <div className="icon">💻</div>
                    <span>Aula Virtual</span>
                  </div>
                  <div className="mpaz-ref-service-item">
                    <div className="icon">📊</div>
                    <span>Notas y Certificados</span>
                  </div>
                  <div className="mpaz-ref-service-item">
                    <div className="icon">🤝</div>
                    <span>Convivencia Escolar</span>
                  </div>
                  <div className="mpaz-ref-service-item">
                    <div className="icon">📚</div>
                    <span>Biblioteca Digital</span>
                  </div>
                </div>
              </div>

            </div>

          </div>
        </section>

      </main>

      {/* 6. FOOTER INSTITUCIONAL */}
      <footer className="mpaz-ref-footer" id="contacto">
        <div className="mpaz-ref-container mpaz-ref-footer-grid">
          <div>
            <h3>Escuela Escritora Marcela Paz</h3>
            <p>Ramón Liborio Carvallo 736, 8071614 San Bernardo, Región Metropolitana · Sistema MPAZ RFID</p>
          </div>
          <div className="links">
            <div>Portal Administrativo</div>
            <div>Portal Docente</div>
            <div>Soporte Técnico</div>
          </div>
        </div>
        <div className="mpaz-ref-footer-bottom">
          <div className="mpaz-ref-container">
            © {new Date().getFullYear()} Escuela Escritora Marcela Paz. Todos los derechos reservados.
          </div>
        </div>
      </footer>

    </div>
  );
}