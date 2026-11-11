import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Inicio from './pages/inicio';
import Login from './pages/login';
import NuestraEscuela from './pages/nuestra-escuela';
import Comunidad from './pages/comunidad';
import Servicios from './pages/servicios';
import Noticias from './pages/noticias';
import Contacto from './pages/contacto';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Inicio />} />
        <Route path="/login" element={<Login />} />
        <Route path="/nuestra-escuela" element={<NuestraEscuela />} />
        <Route path="/comunidad" element={<Comunidad />} />
        <Route path="/servicios" element={<Servicios />} />
        <Route path="/noticias" element={<Noticias />} />
        <Route path="/contacto" element={<Contacto />} />
      </Routes>
    </Router>
  );
}

export default App;