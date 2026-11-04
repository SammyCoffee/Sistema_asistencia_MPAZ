import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import './css/styles.css'
import './css/directorio.css'
import './css/panel-mpaz.css'
import './css/inventario-mpaz.css'
import './css/vinculacion-mpaz.css'
import './css/asistencias-mpaz.css'
import './css/calendario-mpaz.css'
import './css/seguimiento.css'
import './css/identidad-mpaz.css'

import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)