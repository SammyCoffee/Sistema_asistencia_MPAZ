import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../css/inicio.css';

// Importación de fotos reales de tu carpeta assets
import imgPiano from '../assets/piano.jpg';
import imgAbp from '../assets/ABP.jpg';

export default function Comunidad() {
  const [temaOscuro, setTemaOscuro] = useState(() => {
    const atributo = document.documentElement.getAttribute('data-mpaz-tema');
    return atributo ? atributo === 'oscuro' : false;
  });

  const toggleTema = () => {
    const nuevoTema = !temaOscuro;
    setTemaOscuro(nuevoTema);
    document.documentElement.setAttribute('data-mpaz-tema', nuevoTema ? 'oscuro' : 'claro');
  };

  // Estamentos presentados en formato de filas institucionales limpias
  const estamentos = [
    {
      id: 1,
      titulo: 'Estudiantes',
      subtitulo: 'Protagonistas del aprendizaje',
      icono: '👥',
      descripcion: 'Niños y jóvenes participativos, creativos y motivados por aprender, liderando iniciativas artísticas, culturales, deportivas y científicas dentro de la escuela.'
    },
    {
      id: 2,
      titulo: 'Cuerpo Docente y Directivo',
      subtitulo: 'Guías vocacionales',
      icono: '👩‍🏫',
      descripcion: 'Profesionales comprometidos con la innovación pedagógica, la enseñanza inclusiva y el acompañamiento académico y socioemocional de cada estudiante.'
    },
    {
      id: 3,
      titulo: 'Familias y Apoderados',
      subtitulo: 'Alianza familia-escuela',
      icono: '👨‍👩‍👧‍👦',
      descripcion: 'Pilares fundamentales en la formación valórica, integrados activamente en las actividades escolares, celebraciones tradicionales y talleres formativos.'
    },
    {
      id: 4,
      titulo: 'Asistentes de la Educación',
      subtitulo: 'Soporte y bienestar diario',
      icono: '🤝',
      descripcion: 'Equipo multidisciplinario, paradocentes, administrativos y auxiliares que garantizan un ambiente seguro, acogedor y propicio para el desarrollo diario.'
    }
  ];

  // Organizaciones y comités internos
  const organizaciones = [
    {
      titulo: 'Centro General de Padres y Apoderados (CGPA)',
      texto: 'Organización que representa a las familias, promoviendo la participación en proyectos comunitarios y apoyando las metas educativas del establecimiento.'
    },
    {
      titulo: 'Centro de Estudiantes (CCAA)',
      texto: 'Espacio de liderazgo juvenil y formación ciudadana donde los alumnos canalizan sus ideas, organizan jornadas recreativas y representan a sus compañeros.'
    },
    {
      titulo: 'Equipo de Convivencia Escolar',
      texto: 'Encargados de fomentar el buen trato, el respeto mutuo, la resolución pacífica de conflictos y el apoyo psicoemocional continuo.'
    },
    {
      titulo: 'Consejo Escolar',
      texto: 'Instancia consultiva e informativa donde convergen representantes de todos los estamentos para trabajar por la mejora continua de la escuela.'
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
            <Link to="/comunidad" className="activo">Comunidad</Link>
            <Link to="/servicios">Servicios</Link>
            <Link to="/noticias">Noticias</Link>
            <Link to="/contacto">Contacto</Link>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="mpaz-ref-main-content">
        <div className="mpaz-ref-container">
          
          {/* Encabezado Principal */}
          <div className="mpaz-ref-section-header">
            <h2><span className="dot-yellow"></span> Nuestra Comunidad Educativa</h2>
          </div>
          <p style={{ fontSize: '1.05rem', color: 'var(--ref-text-muted)', marginBottom: '2.5rem', maxWidth: '850px' }}>
            La fuerza de la Escuela Escritora Marcela Paz reside en la participación activa y armónica de todos sus integrantes. Trabajamos unidos para construir un entorno seguro, inclusivo y de colaboración constante.
          </p>

          {/* 1. Estamentos en formato de filas limpias */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', marginBottom: '3.5rem' }}>
            {estamentos.map((item) => (
              <div 
                key={item.id} 
                style={{ 
                  backgroundColor: 'var(--ref-surface)', 
                  border: '1px solid var(--ref-border)', 
                  borderRadius: '12px', 
                  padding: '1.75rem',
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '1.5rem',
                  boxShadow: '0 4px 15px rgba(0,0,0,0.02)'
                }}
              >
                <div style={{ fontSize: '2.5rem', background: 'rgba(245, 158, 11, 0.1)', padding: '0.8rem', borderRadius: '10px', lineHeight: 1 }}>
                  {item.icono}
                </div>
                <div>
                  <span style={{ fontSize: '0.78rem', fontWeight: '700', color: 'var(--ref-yellow)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                    {item.subtitulo}
                  </span>
                  <h3 style={{ fontSize: '1.25rem', fontWeight: '800', marginBottom: '0.5rem', color: 'var(--ref-text)' }}>
                    {item.titulo}
                  </h3>
                  <p style={{ color: 'var(--ref-text-muted)', fontSize: '0.95rem', lineHeight: '1.6', marginBottom: 0 }}>
                    {item.descripcion}
                  </p>
                </div>
              </div>
            ))}
          </div>

          {/* 2. Organizaciones y Participación */}
          <div className="mpaz-ref-section-header">
            <h2><span className="dot-yellow"></span> Instancias de Participación</h2>
          </div>
          <div 
            style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', 
              gap: '1.5rem', 
              marginBottom: '3.5rem' 
            }}
          >
            {organizaciones.map((org, index) => (
              <div className="mpaz-ref-school-card" key={index} style={{ marginBottom: 0 }}>
                <h3 style={{ fontSize: '1.1rem', fontWeight: '700', marginBottom: '0.6rem', color: 'var(--ref-text)' }}>
                  {org.titulo}
                </h3>
                <p style={{ marginBottom: 0 }}>{org.texto}</p>
              </div>
            ))}
          </div>

          {/* 3. SECCIÓN BONITA DE REDES SOCIALES */}
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

          {/* 4. Bloque Destacado: Vida Escolar y Talleres */}
          <div className="mpaz-ref-school-card" style={{ padding: '2rem' }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '2rem', alignItems: 'center' }}>
              <div>
                <h2><span className="dot-yellow"></span> Vida Escolar, Arte y Cultura</h2>
                <p>
                  Promovemos el desarrollo integral mediante actividades extracurriculares, muestras musicales como el Día del Piano, ferias de Aprendizaje Basado en Proyectos (ABP) y encuentros literarios donde toda la comunidad comparte los logros de nuestros estudiantes.
                </p>
                <Link to="/noticias" className="mpaz-ref-btn-yellow" style={{ marginTop: '0.5rem', display: 'inline-flex' }}>
                  Ver galería de actividades ›
                </Link>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                <img 
                  src={imgPiano} 
                  alt="Día de Piano" 
                  style={{ width: '100%', height: '160px', objectFit: 'cover', borderRadius: '8px' }} 
                />
                <img 
                  src={imgAbp} 
                  alt="Proyectos ABP" 
                  style={{ width: '100%', height: '160px', objectFit: 'cover', borderRadius: '8px' }} 
                />
              </div>
            </div>
          </div>

        </div>
      </main>

      {/* Footer */}
      <footer className="mpaz-ref-footer">
        <div className="mpaz-ref-container mpaz-ref-footer-grid">
          <div>
            <h3>Escuela Escritora Marcela Paz</h3>
            <p>Ramón Liborio Carvallo 736, San Bernardo · Sistema MPAZ RFID</p>
          </div>
          <div className="links">
            <Link to="/login">Portal Administrativo</Link>
            <Link to="/login">Portal Docente</Link>
            <Link to="/contacto">Soporte Técnico</Link>
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