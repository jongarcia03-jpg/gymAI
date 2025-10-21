from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List
from ..db import get_session
from ..models import Exercise

router = APIRouter(prefix="/exercises", tags=["exercises"])

@router.get("/")
def list_exercises(session: Session = Depends(get_session)):
    """Listar todos los ejercicios disponibles"""
    return session.exec(select(Exercise)).all()

@router.post("/")
def create_exercise(ex: Exercise, session: Session = Depends(get_session)):
    """Crear un nuevo ejercicio (usado para añadir los tuyos personalizados)"""
    session.add(ex)
    session.commit()
    session.refresh(ex)
    return ex
