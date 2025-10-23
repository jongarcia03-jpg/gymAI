from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import init_db
from .seed_data import seed
from .routers import auth, users, exercises, routines, workouts, suggestions, chat, tts, stt

app = FastAPI(title="GymAI API")

# Permitir peticiones desde la app móvil
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ en producción usa dominio específico
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar la base de datos
@app.on_event("startup")
def on_startup():
    init_db()
    try:
        seed()
    except Exception as e:
        print("Seed failed:", e)

# Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(exercises.router)
app.include_router(routines.router)
app.include_router(workouts.router)
app.include_router(suggestions.router)
app.include_router(chat.router)
app.include_router(tts.router)
app.include_router(stt.router)

@app.get("/")
def root():
    return {"message": "Bienvenido a GymAI Backend 🚀"}
