from datetime import datetime, timedelta
import jwt
from .config import settings
import hashlib

def hash_password(password: str):
    """Hash the password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain: str, hashed: str):
    """Verify a password against its hash."""
    return hash_password(plain) == hashed

def create_token(user_id: int):
    exp = datetime.utcnow() + timedelta(days=7)
    payload = {"sub": str(user_id), "exp": exp}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

def decode_token(token: str):
    data = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
    return int(data["sub"])
