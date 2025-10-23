from sqlmodel import Session, select
from .db import engine
from .models import User, Exercise, Routine, RoutineExercise
from .services.auth import hash_password


def seed():
    with Session(engine) as session:
        # Crear usuario de prueba si no existe
        user = session.exec(select(User).where(User.email == "dev@local" )).first()
        if not user:
            hashed = hash_password("dev")
            user = User(email="dev@local", password_hash=hashed)
            session.add(user)
            session.commit()
            session.refresh(user)

        # Añadir ejercicios si no existen
        exercises = session.exec(select(Exercise)).all()
        if not exercises:
            ex1 = Exercise(name="Press banca", muscle_group="Pectoral", description="Press para pecho.")
            ex2 = Exercise(name="Sentadilla", muscle_group="Piernas", description="Sentadilla profunda.")
            session.add_all([ex1, ex2])
            session.commit()
            session.refresh(ex1)
            session.refresh(ex2)

        # Añadir una rutina para el usuario si no tiene
        routines = session.exec(select(Routine).where(Routine.user_id == user.id)).all()
        if not routines:
            r = Routine(user_id=user.id, name="Rutina full body", description="Descripción de ejemplo")
            session.add(r)
            session.commit()
            session.refresh(r)
            # Vincular ejercicios si existen
            exs = session.exec(select(Exercise)).all()
            for ex in exs:
                re = RoutineExercise(routine_id=r.id, exercise_id=ex.id, sets=3, reps=10)
                session.add(re)
            session.commit()

        print("✅ Seed data asegurada")


if __name__ == "__main__":
    seed()
