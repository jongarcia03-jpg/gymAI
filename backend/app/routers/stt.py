from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from ..deps import get_current_user_id
from ..services.elevenlabs import stt_from_audio_bytes
import logging

logger = logging.getLogger("stt.router")

router = APIRouter(prefix="/stt", tags=["stt"])


@router.post("/")
async def stt(file: UploadFile, user_id: int = Depends(get_current_user_id)):
    """Transcribir audio a texto (voz a texto)"""
    logger.info(f"/stt called by user_id={user_id} filename={file.filename} content_type={file.content_type}")
    try:
        audio_bytes = await file.read()
        text = await stt_from_audio_bytes(audio_bytes)
        return {"text": text}
    except Exception as e:
        logger.exception("Error transcribing audio via ElevenLabs: %s", e)
        raise HTTPException(status_code=502, detail=f"STT failed: {str(e)}")
