from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..db import get_session
from ..models import WorkoutLog
from ..services.progression import SetLog, recommend_next
from ..deps import get_current_user_id

router = APIRouter(prefix="/suggestions", tags=["suggestions"])

@router.get("/next-weight")
def next_weight(exercise_id: int, rep_min: int = 6, rep_max: int = 10, 
                user_id: int = Depends(get_current_user_id), 
                session: Session = Depends(get_session)):
    """Calcular la siguiente carga de entrenamiento"""
    logs = session.exec(select(WorkoutLog)
        .where(WorkoutLog.user_id == user_id, WorkoutLog.exercise_id == exercise_id)
        .order_by(WorkoutLog.date)
    ).all()
    
    sessions = {}
    for l in logs:
        key = l.date.date().isoformat()
        sessions.setdefault(key, []).append(SetLog(reps=l.reps, weight=l.weight_kg, rir=l.rir, rpe=l.rpe))
    
    history = list(sessions.values())[-8:]
    rec = recommend_next(history, rep_min, rep_max)
    return rec.__dict__
