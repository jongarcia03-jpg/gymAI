import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

const instance = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json'
  }
})

function setToken(token){
  if (!token) return
  localStorage.setItem('token', token)
  instance.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

function getToken(){
  return localStorage.getItem('token')
}

function clearToken(){
  localStorage.removeItem('token')
  delete instance.defaults.headers.common['Authorization']
}

// Initialize from storage
const existing = getToken()
if (existing) setToken(existing)

instance.setToken = setToken
instance.getToken = getToken
instance.clearToken = clearToken

export default instance
export { setToken, getToken, clearToken }
