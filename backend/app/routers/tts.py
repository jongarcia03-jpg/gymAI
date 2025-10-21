from fastapi import APIRouter, Depends, Response, HTTPException
from pydantic import BaseModel
from ..deps import get_current_user_id
from ..services.elevenlabs import tts_mp3, tts_generate_with_options
import logging

logger = logging.getLogger("tts.router")

router = APIRouter(prefix="/tts", tags=["tts"])


class TTSIn(BaseModel):
    text: str
    voice_id: str | None = None
    force_spanish: bool = False


@router.post("/speak")
async def speak(data: TTSIn, user_id: int = Depends(get_current_user_id)):
    """Convertir texto en voz (usando tu clon de ElevenLabs)"""
    logger.info(f"/tts/speak called by user_id={user_id} text_len={len(data.text)}")
    try:
        audio = await tts_generate_with_options(data.text, data.voice_id, data.force_spanish)
        return Response(content=audio, media_type="audio/mpeg")
    except Exception as e:
        # Log detallado para depuración de ElevenLabs
        logger.exception("Error generating TTS via ElevenLabs: %s", e)
        raise HTTPException(status_code=502, detail=f"TTS generation failed: {str(e)}")
