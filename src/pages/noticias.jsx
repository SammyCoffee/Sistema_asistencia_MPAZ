import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../css/inicio.css';

// -----------------------------------------------------------------
// IMPORTACIONES CON LAS EXTENSIONES EXACTAS (.jpg y .jpeg)
// -----------------------------------------------------------------
import imgAbp from '../assets/ABP.jpg';
import imgChocolate from '../assets/chocolate.jpeg';
import imgPiano from '../assets/piano.jpg';
import imgAlumno from '../assets/alumno.jpeg';
import imgFiestas from '../assets/fiestaspatrias.jpg';
import imgLectura from '../assets/lectura.jpg';
import imgFuturo from '../assets/futuro.jpg';
import imgMujeres from '../assets/mujeres.jpg';

export default function Noticias() {
  const [temaOscuro, setTemaOscuro] = useState(() => {
    const atributo = document.documentElement.getAttribute('data-mpaz-tema');
    return atributo ? atributo === 'oscuro' : false;
  });

  const toggleTema = () => {
    const nuevoTema = !temaOscuro;
    setTemaOscuro(nuevoTema);
    document.documentElement.setAttribute('data-mpaz-tema', nuevoTema ? 'oscuro' : 'claro');
  };

  // Lista de noticias con cada archivo de imagen correspondiente
  const listaNoticias = [
    {
      id: 1,
      titulo: 'Proyectos ABP',
      fecha: '17 de Septiembre',
      categoria: 'Abp',
      imagen: imgAbp,
      descripcion: 'Exposición y trabajos de aprendizaje basado en proyectos desarrollados por los estudiantes.'
    },
    {
      id: 2,
      titulo: 'Chocolate Literario',
      fecha: '05 de Noviembre',
      categoria: 'Chocolate literario',
      imagen: imgChocolate,
      descripcion: 'Jornada de fomento a la lectura compartiendo un cálido chocolate y grandes historias en la biblioteca.'
    },
    {
      id: 3,
      titulo: 'Presentación de Día de Piano',
      fecha: '05 de Junio',
      categoria: 'Día de piano',
      imagen: imgPiano,
      descripcion: 'Demostración de talento musical y sensibilidad artística por parte de los alumnos.'
    },
    {
      id: 4,
      titulo: 'Celebración Día del Alumno',
      fecha: '05 de Junio',
      categoria: 'Día del alumno',
      imagen: imgAlumno,
      descripcion: 'Actividades recreativas, sorpresas y momentos de sana diversión dedicados a nuestros estudiantes.'
    },
    {
      id: 5,
      titulo: 'Festividad de Fiestas Patrias',
      fecha: '18 de Septiembre',
      categoria: 'Fiestas patrias',
      imagen: imgFiestas,
      descripcion: 'Conmemoración de nuestras tradiciones nacionales con bailes típicos, música y alegría.'
    },
    {
      id: 6,
      titulo: 'Actividades de Lectura',
      fecha: '11 de Agosto',
      categoria: 'Lectura',
      imagen: imgLectura,
      descripcion: 'Espacios interactivos dedicados a potenciar el amor por los libros y la comprensión lectora.'
    },
    {
      id: 7,
      titulo: 'Programa Pro Futuro',
      fecha: '03 de Agosto',
      categoria: 'Pro futuro',
      imagen: imgFuturo,
      descripcion: 'Iniciativas tecnológicas y formativas orientadas a potenciar habilidades de innovación en los alumnos.'
    },
    {
      id: 8,
      titulo: 'Remodelación Baño Mujeres',
      fecha: '11 de Agosto',
      categoria: 'Infraestructura',
      imagen: imgMujeres,
      descripcion: 'Mejoras en las dependencias y servicios higiénicos para garantizar el bienestar y comodidad de las alumnas.'
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
            <Link to="/servicios">Servicios</Link>
            <Link to="/noticias" className="activo">Noticias</Link>
            <Link to="/contacto">Contacto</Link>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="mpaz-ref-main-content">
        <div className="mpaz-ref-container">
          <div className="mpaz-ref-section-header">
            <h2><span className="dot-yellow"></span> Galería de Eventos y Noticias</h2>
          </div>
          <p style={{ fontSize: '1.05rem', color: 'var(--ref-text-muted)', marginBottom: '2.5rem' }}>
            Registro fotográfico y actividades oficiales de cada una de nuestras jornadas escolares.
          </p>
          
          <div className="mpaz-ref-news-grid" style={{ rowGap: '2rem' }}>
            {listaNoticias.map((noticia) => (
              <article className="mpaz-ref-news-card" key={noticia.id}>
                <div className="mpaz-ref-news-img">
                  <img src={noticia.imagen} alt={noticia.titulo} />
                  <span className="mpaz-ref-badge-libros">{noticia.categoria}</span>
                </div>
                <div className="mpaz-ref-news-body">
                  <span className="mpaz-ref-date">{noticia.fecha}</span>
                  <h3>{noticia.titulo}</h3>
                  <p>{noticia.descripcion}</p>
                </div>
              </article>
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