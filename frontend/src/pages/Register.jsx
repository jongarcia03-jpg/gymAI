import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import api from '../services/api'

export default function Register() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  const submit = async (e) => {
    e.preventDefault()
    setError(null)
    if (password !== confirm) return setError('Las contraseñas no coinciden')
    try {
      await api.post('/auth/register', { email, password })
      // Después de registrarse, ir a login
      navigate('/login')
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al registrar')
    }
  }

  return (
    <div style={{maxWidth:400, margin:'40px auto'}}>
      <h2>Registro</h2>
      <form onSubmit={submit}>
        <div>
          <label>Email</label>
          <input value={email} onChange={e=>setEmail(e.target.value)} type="email" required />
        </div>
        <div>
          <label>Contraseña</label>
          <input value={password} onChange={e=>setPassword(e.target.value)} type="password" required />
        </div>
        <div>
          <label>Confirmar contraseña</label>
          <input value={confirm} onChange={e=>setConfirm(e.target.value)} type="password" required />
        </div>
        {error && <div style={{color:'red'}}>{error}</div>}
        <button type="submit">Crear cuenta</button>
      </form>
      <p>¿Ya tienes cuenta? <Link to="/login">Inicia sesión</Link></p>
    </div>
  )
}
