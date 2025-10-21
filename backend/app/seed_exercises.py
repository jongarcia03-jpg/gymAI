from sqlmodel import Session
from .db import engine
from .models import Exercise

def seed():
    exercises = [
        Exercise(name="Press banca", muscle_group="Pectoral", description="Ejercicio básico de fuerza para pecho y tríceps.", youtube_url="https://www.youtube.com/watch?v=rT7DgCr-3pg"),
        Exercise(name="Sentadilla", muscle_group="Piernas", description="Ejercicio compuesto para piernas y glúteos.", youtube_url="https://www.youtube.com/watch?v=aclHkVaku9U"),
        Exercise(name="Peso muerto", muscle_group="Espalda", description="Ejercicio de tracción para espalda y cadena posterior.", youtube_url="https://www.youtube.com/watch?v=op9kVnSso6Q"),
        Exercise(name="Press militar", muscle_group="Hombros", description="Ejercicio para deltoides y tríceps.", youtube_url="https://www.youtube.com/watch?v=qEwKCR5JCog"),
        Exercise(name="Dominadas", muscle_group="Espalda", description="Ejercicio con peso corporal para dorsal ancho y bíceps.", youtube_url="https://www.youtube.com/watch?v=eGo4IYlbE5g")
    ]
    with Session(engine) as session:
        for ex in exercises:
            session.add(ex)
        session.commit()
        print("✅ Ejercicios cargados correctamente")

if __name__ == "__main__":
    seed()
