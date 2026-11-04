import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

export default function Login() {
  const [usuario, setUsuario] = useState('');
  const [password, setPassword] = useState('');
  const [mensaje, setMensaje] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensaje('Iniciando sesión...');
    
    try {
      const respuesta = await fetch('/panel/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ usuario, password })
      });
      
      if (respuesta.ok) {
        navigate('/panel'); 
      } else {
        setMensaje('Usuario o contraseña incorrectos.');
      }
    } catch (error) {
      setMensaje('Error de conexión con el servidor.');
    }
  };

  return (
    <div className="mpaz-login-admin">
      <main>
        <img className="mpaz-sello mpaz-escudo" src="/escudo-mpaz.webp" width="60" height="60" alt="Escudo de la escuela" />
        <span className="mpaz-etiqueta">ESCUELA ESCRITORA MARCELA PAZ</span>
        <h1>Acceso administrativo</h1>
        <p>Acceso al sistema de asistencia escolar</p>

        <form onSubmit={handleSubmit}>
          <label htmlFor="usuario">Usuario</label>
          <input
            type="text"
            id="usuario"
            value={usuario}
            onChange={(e) => setUsuario(e.target.value)}
            autoComplete="username"
            maxLength="40"
            required
          />

          <label htmlFor="password">Contraseña</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
            required
          />

          <button type="submit">
            Ingresar
          </button>

          <p id="mensaje-login" style={{ color: '#d32f2f', fontWeight: '600', marginTop: '10px' }}>{mensaje}</p>
        </form>

        <p style={{ marginTop: '20px', textAlign: 'center' }}>
          <Link to="/" className="enlace-volver-inicio">
            ← Volver a selección de portales
          </Link>
        </p>
      </main>
    </div>
  );
}