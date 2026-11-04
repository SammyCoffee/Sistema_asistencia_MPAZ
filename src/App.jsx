import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Inicio from './pages/inicio';
import Login from './pages/login';
import Home from './pages/home';
import ProfesorLogin from './pages/profesorLogin';

function App() {
  return (
    <Router>
      <Routes>
        {/* Ruta principal (Portal de bienvenida) */}
        <Route path="/" element={<Inicio />} />

        {/* Ruta de inicio de sesión administrativo */}
        <Route path="/login" element={<Login />} />

        {/* Ruta del panel principal de gestión RFID */}
        <Route path="/panel" element={<Home />} />

        {/* Ruta del portal docente */}
        <Route path="/profesor/login" element={<ProfesorLogin />} />
      </Routes>
    </Router>
  );
}

export default App;