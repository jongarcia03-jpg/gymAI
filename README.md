# gymAI

Proyecto monorepo que contiene el backend (FastAPI) y el frontend móvil/web (Expo / React Native).

## Estructura
- `backend/` – FastAPI app, dependencias en `backend/requirements.txt`.
- `mobile/` – Expo / React Native app (web + Android/iOS).

## Backend - Quick start
1. Crear un entorno virtual e instalar dependencias:

```powershell
cd backend
python -m venv .venv
. .venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

2. Copiar `.env` y configurar variables (ELEVEN_API_KEY, ELEVEN_VOICE_ID, OPENROUTER_API_KEY, etc.).

3. Ejecutar el servidor:

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Frontend (Expo) - Quick start
1. Abrir la carpeta `mobile` y bajar dependencias:

```powershell
cd mobile
npm install
# o
pnpm install
```

2. Ejecutar Expo en web:

```powershell
npx expo start --web -c
```

3. En Android/iOS sigue las instrucciones de Expo (o usa `npx expo run:android`).

## Notas
- `backend/.env` no está incluido en el repo por seguridad.
- El directorio `mobile/` se incluyó dentro del monorepo.
