from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

# -------------------------------------------------------------
# 👤 USUARIOS
# -------------------------------------------------------------

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relaciones
    routines: List["Routine"] = Relationship(back_populates="user")
    workouts: List["WorkoutLog"] = Relationship(back_populates="user")
    transcripts: List["Transcript"] = Relationship(back_populates="user")

# -------------------------------------------------------------
# 🏋️‍♂️ EJERCICIOS
# -------------------------------------------------------------

class Exercise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    muscle_group: str
    description: str
    youtube_url: Optional[str] = None

    # Relaciones
    routine_links: List["RoutineExercise"] = Relationship(back_populates="exercise")
    workouts: List["WorkoutLog"] = Relationship(back_populates="exercise")

# -------------------------------------------------------------
# 🧩 RUTINAS Y SUS EJERCICIOS
# -------------------------------------------------------------

class Routine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[User] = Relationship(back_populates="routines")
    exercises: List["RoutineExercise"] = Relationship(back_populates="routine")


class RoutineExercise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    routine_id: int = Field(foreign_key="routine.id")
    exercise_id: int = Field(foreign_key="exercise.id")
    sets: int = 3
    reps: int = 10

    routine: Optional[Routine] = Relationship(back_populates="exercises")
    exercise: Optional[Exercise] = Relationship(back_populates="routine_links")

# -------------------------------------------------------------
# 📋 REGISTROS DE ENTRENAMIENTO
# -------------------------------------------------------------

class WorkoutLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    exercise_id: int = Field(foreign_key="exercise.id")

    date: datetime = Field(default_factory=datetime.utcnow)
    set_number: int = 1
    reps: int = 8
    weight_kg: float = 0.0
    rir: Optional[int] = None  # Repeticiones en reserva
    rpe: Optional[float] = None  # Esfuerzo percibido (opcional)

    user: Optional[User] = Relationship(back_populates="workouts")
    exercise: Optional[Exercise] = Relationship(back_populates="workouts")

# -------------------------------------------------------------
# 💬 HISTORIAL DE CHAT / TRANSCRIPCIONES
# -------------------------------------------------------------

class Transcript(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    role: str  # "user" o "assistant"
    text: str
    context: Optional[str] = "fitness"  # fitness | general
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[User] = Relationship(back_populates="transcripts")
