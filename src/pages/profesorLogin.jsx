import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../css/profesor.css'; // Importa los estilos del profesor

export default function Profesor() {
  const [autenticado, setAutenticado] = useState(false);
  const [cargandoSesion, setCargandoSesion] = useState(true);
  const [nombreProfesor, setNombreProfesor] = useState('Verificando sesión...');
  
  // Estados del Login
  const [usuario, setUsuario] = useState('');
  const [password, setPassword] = useState('');
  const [mensajeLogin, setMensajeLogin] = useState('');

  // Estados del Panel Docente
  const [asignaciones, setAsignaciones] = useState([]);
  const [cursosDisponibles, setCursosDisponibles] = useState([]);
  const [cursoSeleccionado, setCursoSeleccionado] = useState('');
  const [asignaturasFiltradas, setAsignaturasFiltradas] = useState([]);
  const [asignaturaSeleccionada, setAsignaturaSeleccionada] = useState('');
  
  const [mensajePanel, setMensajePanel] = useState('Cargando asignaciones...');
  const [estudiantesCurso, setEstudiantesCurso] = useState([]);
  const [mostrarEstudiantes, setMostrarEstudiantes] = useState(false);

  const navigate = useNavigate();

  // Verificar sesión al cargar
  useEffect(() => {
    async function comprobarSesion() {
      try {
        const res = await fetch('/profesor/sesion', { credentials: 'same-origin' });
        const data = await res.json();
        if (res.ok && data.resultado === 'ok') {
          setAutenticado(true);
          setNombreProfesor(data.profesor?.nombre || 'Profesor autorizado');
          cargarAsignaciones();
        } else {
          setAutenticado(false);
        }
      } catch (err) {
        setAutenticado(false);
      } finally {
        setCargandoSesion(false);
      }
    }
    comprobarSesion();
  }, []);

  // Manejar Login del Profesor
  const handleLogin = async (e) => {
    e.preventDefault();
    setMensajeLogin('Verificando acceso...');
    try {
      const res = await fetch('/profesor/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify({ usuario, password })
      });
      const data = await res.json();
      if (res.ok && data.resultado === 'ok') {
        setAutenticado(true);
        setNombreProfesor(data.profesor?.nombre || 'Profesor autorizado');
        cargarAsignaciones();
      } else {
        setMensajeLogin(res.status === 401 ? 'Usuario o contraseña incorrectos.' : 'No fue posible iniciar sesión.');
      }
    } catch (err) {
      setMensajeLogin('No se pudo conectar con el servidor MPAZ RFID.');
    }
  };

  // Cargar asignaciones del profesor
  const cargarAsignaciones = async () => {
    try {
      const res = await fetch('/profesor/asignaciones', { credentials: 'same-origin' });
      const data = await res.json();
      if (res.ok && data.resultado === 'ok') {
        const lista = data.asignaciones || [];
        setAsignaciones(lista);
        const cursos = [...new Set(lista.map(a => a.curso))];
        setCursosDisponibles(cursos);
        setMensajePanel(cursos.length === 0 ? 'No tiene cursos o asignaturas asignados.' : 'Seleccione un curso y una asignatura para continuar.');
      } else {
        setMensajePanel('No fue posible cargar las asignaciones.');
      }
    } catch (err) {
      setMensajePanel('Error de conexión con el servidor.');
    }
  };

  // Cambio de curso en el selector
  const handleCursoChange = (e) => {
    const curso = e.target.value;
    setCursoSeleccionado(curso);
    setAsignaturaSeleccionada('');
    setMostrarEstudiantes(false);

    const filtradas = asignaciones.filter(a => a.curso === curso);
    setAsignaturasFiltradas(filtradas);
  };

  // Ver estudiantes del curso seleccionado
  const verEstudiantes = async () => {
    if (!cursoSeleccionado) return;
    setMostrarEstudiantes(true);
    setMensajePanel('Cargando estudiantes...');
    try {
      const res = await fetch(`/profesor/cursos/${encodeURIComponent(cursoSeleccionado)}/alumnos`, { credentials: 'same-origin' });
      const data = await res.json();
      if (res.ok && data.resultado === 'ok') {
        setEstudiantesCurso(data.alumnos || []);
      }
    } catch (err) {
      setEstudiantesCurso([]);
    }
  };

  // Cerrar sesión
  const cerrarSesion = async () => {
    try {
      await fetch('/profesor/logout', { method: 'POST', credentials: 'same-origin' });
    } catch (err) {}
    setAutenticado(false);
  };

  if (cargandoSesion) return <div style={{ padding: '40px', textAlign: 'center' }}>Cargando portal docente...</div>;

  // ==========================================
  // VISTA 1: LOGIN DOCENTE
  // ==========================================
  if (!autenticado) {
    return (
      <div className="pagina-login">
        <main className="contenedor-login">
          <section className="tarjeta-login">
            <header className="encabezado-login">
              <div className="identidad">
                <img className="identidad-icono mpaz-escudo" src="/escudo-mpaz.webp" width="70" height="70" alt="Escudo" />
              </div>
              <p className="nombre-escuela">Escuela Escritora Marcela Paz</p>
              <h1>Portal Docente</h1>
              <p className="subtitulo-login">Sistema MPAZ RFID</p>
              <p className="descripcion-login">Gestión de clases y asistencia escolar</p>
            </header>

            <form onSubmit={handleLogin}>
              <div className="grupo-campo">
                <label htmlFor="usuario">Usuario</label>
                <input
                  type="text"
                  id="usuario"
                  value={usuario}
                  onChange={(e) => setUsuario(e.target.value)}
                  placeholder="Ingrese su usuario"
                  required
                />
              </div>

              <div className="grupo-campo">
                <label htmlFor="password">Contraseña</label>
                <input
                  type="password"
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Ingrese su contraseña"
                  required
                />
              </div>

              <button type="submit" className="boton-principal">
                Iniciar sesión
              </button>

              <p className="mensaje-login error">{mensajeLogin}</p>
            </form>

            <nav className="navegacion-login">
              <Link to="/" className="enlace-volver-inicio" style={{ display: 'block', margin: '18px 0', padding: '12px', textAlign: 'center', color: '#1677b8', fontWeight: 600, textDecoration: 'none' }}>
                ← Volver a selección de portales
              </Link>
            </nav>

            <footer className="pie-login">
              <p>Acceso exclusivo para docentes autorizados</p>
              <span>Escuela Escritora Marcela Paz · San Bernardo</span>
            </footer>
          </section>
        </main>
      </div>
    );
  }

  // ==========================================
  // VISTA 2: PANEL DEL DOCENTE
  // ==========================================
  return (
    <div className="pagina-panel">
      <div className="contenedor-panel">
        <header className="cabecera-panel">
          <div className="mpaz-docente-marca">
            <img className="mpaz-sello mpaz-escudo" src="/escudo-mpaz.webp" width="49" height="49" alt="Escudo" />
            <div className="informacion-sistema">
              <p className="nombre-escuela">Escuela Escritora Marcela Paz</p>
              <h1>Portal Docente</h1>
              <p className="subtitulo-login">Sistema MPAZ RFID</p>
            </div>
          </div>

          <div className="acciones-cabecera">
            <Link to="/" className="boton-volver-inicio" style={{ display: 'inline-block', padding: '10px 16px', borderRadius: '8px', background: '#1677b8', color: '#fff', textDecoration: 'none', fontWeight: 600 }}>
              ← Volver al inicio
            </Link>
            <button type="button" onClick={cerrarSesion} className="boton-cerrar">
              Cerrar sesión
            </button>
          </div>
        </header>

        <main>
          <section className="bienvenida-panel">
            <span className="mpaz-etiqueta">ESPACIO DOCENTE</span>
            <h2>Bienvenido/a</h2>
            <p>{nombreProfesor}</p>
          </section>

          <section className="seccion-asignaciones">
            <div className="titulo-seccion">
              <div>
                <h2>Mis cursos y asignaturas</h2>
                <p>Seleccione el curso y la asignatura correspondiente a su clase.</p>
              </div>
            </div>

            <p className="mensaje-panel">{mensajePanel}</p>

            <div className="selector-asignaciones">
              <div className="campo-selector">
                <label htmlFor="selector-curso">Curso</label>
                <select id="selector-curso" value={cursoSeleccionado} onChange={handleCursoChange} disabled={cursosDisponibles.length === 0}>
                  <option value="">Seleccione un curso</option>
                  {cursosDisponibles.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
              </div>

              <div className="campo-selector">
                <label htmlFor="selector-asignatura">Asignatura</label>
                <select id="selector-asignatura" value={asignaturaSeleccionada} onChange={(e) => setAsignaturaSeleccionada(e.target.value)} disabled={!cursoSeleccionado}>
                  <option value="">Seleccione una asignatura</option>
                  {asignaturasFiltradas.map(a => <option key={a.asignacion_id} value={a.asignacion_id}>{a.asignatura}</option>)}
                </select>
              </div>

              <div className="acciones-selector">
                <button type="button" onClick={verEstudiantes} className="boton-asignacion" disabled={!asignaturaSeleccionada}>
                  Ver estudiantes
                </button>
              </div>
            </div>
          </section>

          {mostrarEstudiantes && (
            <section className="seccion-estudiantes">
              <div className="titulo-seccion">
                <h2>Estudiantes del curso</h2>
              </div>
              <div className="lista-estudiantes">
                <ol>
                  {estudiantesCurso.map(alum => (
                    <li key={alum.id || alum.alumno_id}>{alum.nombre}</li>
                  ))}
                </ol>
              </div>
            </section>
          )}
        </main>

        <footer className="pie-panel">
          <p>Sistema MPAZ RFID · Escuela Escritora Marcela Paz</p>
        </footer>
      </div>
    </div>
  );
}