from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from .config import settings

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(pw: str):
    return pwd_ctx.hash(pw)

def verify_password(pw: str, pw_hash: str):
    return pwd_ctx.verify(pw, pw_hash)

def create_token(user_id: int):
    exp = datetime.utcnow() + timedelta(days=7)
    payload = {"sub": str(user_id), "exp": exp}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

def decode_token(token: str):
    data = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
    return int(data["sub"])
