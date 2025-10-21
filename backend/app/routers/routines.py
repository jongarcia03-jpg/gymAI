from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List
from ..db import get_session
from ..models import Routine, RoutineExercise
from ..deps import get_current_user_id

router = APIRouter(prefix="/routines", tags=["routines"])

@router.get("/")
def list_routines(user_id: int = Depends(get_current_user_id), session: Session = Depends(get_session)):
    """Listar las rutinas del usuario"""
    return session.exec(select(Routine).where(Routine.user_id == user_id)).all()

@router.post("/")
def create_routine(r: Routine, user_id: int = Depends(get_current_user_id), session: Session = Depends(get_session)):
    """Crear una nueva rutina"""
    r.user_id = user_id
    session.add(r)
    session.commit()
    session.refresh(r)
    return r

@router.post("/{routine_id}/exercises")
def add_exercise_to_routine(
    routine_ex: RoutineExercise, 
    routine_id: int, 
    session: Session = Depends(get_session)
):
    """Vincular un ejercicio a una rutina"""
    routine_ex.routine_id = routine_id
    session.add(routine_ex)
    session.commit()
    session.refresh(routine_ex)
    return routine_ex
