from fastapi import Header, HTTPException
from .auth import decode_token
from .config import settings
import logging

logger = logging.getLogger("deps")


def get_current_user_id(authorization: str = Header(None)):
    # En modo debug, devolver un user_id por defecto para facilitar pruebas locales
    if getattr(settings, "APP_DEBUG", False):
        logger.warning("APP_DEBUG=true: get_current_user_id bypassed, returning user_id=1")
        return 1

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token requerido")
    token = authorization.split(" ")[1]
    try:
        return decode_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")
