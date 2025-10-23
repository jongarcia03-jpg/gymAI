import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { getToken, clearToken } from '../services/api'

export default function Navbar(){
  const navigate = useNavigate()
  const token = getToken()

  const logout = () => {
    clearToken()
    navigate('/login')
  }

  if (!token) return null

  return (
    <nav style={{ padding: 10, borderBottom: '1px solid #ddd', display: 'flex', gap: 12, alignItems: 'center' }}>
      <Link to="/">Inicio</Link>
      <Link to="/library">Biblioteca</Link>
      <Link to="/log">Registro</Link>
      <div style={{ marginLeft: 'auto' }}>
        <button onClick={logout}>Cerrar sesión</button>
      </div>
    </nav>
  )
}
