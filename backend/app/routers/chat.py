from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
from ..db import get_session
from ..models import Transcript
from ..deps import get_current_user_id
from ..services.openrouter import chat_completion
import logging

logger = logging.getLogger("chat.router")

router = APIRouter(prefix="/chat", tags=["chat"])

# -------------------------
# 📩 MODELOS DE ENTRADA
# -------------------------

class ChatIn(BaseModel):
    message: str
    mode: str = "fitness"  # fitness | general

# -------------------------
# 💬 CHAT PRINCIPAL
# -------------------------

@router.post("/")
async def chat(data: ChatIn, user_id: int = Depends(get_current_user_id), session: Session = Depends(get_session)):
    """
    Endpoint principal de conversación con la IA.
    Guarda tanto el mensaje del usuario como la respuesta del asistente.
    """
    # Contexto personalizado según modo
    context = (
        "Eres un entrenador personal profesional. "
        "Ofrece consejos de entrenamiento, técnica y progresión, "
        "pero evita diagnósticos médicos o recomendaciones médicas."
        if data.mode == "fitness"
        else "Eres un asistente general amigable y útil."
    )

    # Estructura del prompt
    messages = [
        {"role": "system", "content": context},
        {"role": "user", "content": data.message},
    ]

    # Llamada al modelo vía OpenRouter
    try:
        reply = await chat_completion(messages)
    except Exception as e:
        logger.exception("Error calling chat_completion: %s", e)
        raise HTTPException(status_code=502, detail=f"Chat generation failed: {str(e)}")

    # Guardar ambos mensajes en la tabla Transcript
    session.add(Transcript(user_id=user_id, role="user", text=data.message, context=data.mode))
    session.add(Transcript(user_id=user_id, role="assistant", text=reply, context=data.mode))
    session.commit()

    return {"text": reply}

# -------------------------
# 🧾 HISTORIAL DE CHAT
# -------------------------

@router.get("/history")
def chat_history(user_id: int = Depends(get_current_user_id), session: Session = Depends(get_session)):
    """
    Devuelve las transcripciones (mensajes usuario/asistente)
    ordenadas por fecha descendente.
    """
    results = session.exec(
        select(Transcript)
        .where(Transcript.user_id == user_id)
        .order_by(Transcript.created_at.desc())
    ).all()

    return [
        {
            "id": t.id,
            "role": t.role,
            "text": t.text,
            "context": t.context,
            "created_at": t.created_at
        } for t in results
    ]

# -------------------------
# 🧹 OPCIONAL: LIMPIAR HISTORIAL
# -------------------------

@router.delete("/clear")
def clear_history(user_id: int = Depends(get_current_user_id), session: Session = Depends(get_session)):
    """
    Elimina todas las transcripciones del usuario actual.
    """
    session.exec(
        Transcript.__table__.delete().where(Transcript.user_id == user_id)
    )
    session.commit()
    return {"message": "Historial eliminado correctamente."}
