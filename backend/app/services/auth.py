from datetime import datetime, timedelta
from jose import jwt, JWTError
from ..models import User
from ..db import get_session
from sqlmodel import Session, select
from fastapi import Depends, HTTPException, status
from ..config import settings
import hashlib

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 día

def hash_password(password: str):
    """Hash the password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain: str, hashed: str):
    """Verify a password against its hash."""
    return hash_password(plain) == hashed

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
