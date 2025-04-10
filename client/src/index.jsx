import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './assets/style.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import "@fortawesome/fontawesome-free/css/all.min.css"; 
import "mdb-react-ui-kit/dist/css/mdb.min.css";

import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App/>
  </StrictMode>
)
