import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import App from './pages/App'
import Analytics from './pages/Analytics'

createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <nav style={{display:'flex', gap:12, padding:12, borderBottom:'1px solid #ddd'}}>
      <Link to="/">Recommend</Link>
      <Link to="/analytics">Analytics</Link>
    </nav>
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/analytics" element={<Analytics />} />
    </Routes>
  </BrowserRouter>
)
