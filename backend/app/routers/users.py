from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select
from ..db import get_session
from ..models import User
from ..auth import hash_password, verify_password, create_token

router = APIRouter(prefix="/users", tags=["users"])

class Register(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
def register(data: Register, session: Session = Depends(get_session)):
    if session.exec(select(User).where(User.email == data.email)).first():
        raise HTTPException(400, "Email ya registrado")
    user = User(email=data.email, password_hash=hash_password(data.password))
    session.add(user)
    session.commit()
    return {"token": create_token(user.id)}
