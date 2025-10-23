import React from 'react'
import { clearToken } from '../services/api'

export default function Home(){
  const logout = ()=>{
    clearToken()
    window.location.href = '/login'
  }

  return (
    <div style={{padding:20}}>
      <h1>Bienvenido a GymAI</h1>
      <p>Interfaz mínima — ya estás autenticado.</p>
      <div style={{ display: 'flex', gap: 10, marginTop: 10 }}>
        <a href="/library">Biblioteca</a>
        <a href="/log">Registro</a>
      </div>
      <div style={{ marginTop: 20 }}>
        <button onClick={logout}>Cerrar sesión</button>
      </div>
    </div>
  )
}
