from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..db import get_session
from ..models import WorkoutLog
from ..deps import get_current_user_id

router = APIRouter(prefix="/workouts", tags=["workouts"])

@router.get("/")
def list_workouts(user_id: int = Depends(get_current_user_id), session: Session = Depends(get_session)):
    """Listar registros de entrenamiento"""
    return session.exec(select(WorkoutLog).where(WorkoutLog.user_id == user_id)).all()

@router.post("/")
def add_workout(log: WorkoutLog, user_id: int = Depends(get_current_user_id), session: Session = Depends(get_session)):
    """Guardar un registro de entrenamiento"""
    log.user_id = user_id
    session.add(log)
    session.commit()
    session.refresh(log)
    return log
