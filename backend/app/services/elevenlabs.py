import httpx
from ..config import settings

# -------------------------------------------------------------
# 🎙️ ElevenLabs API — Text-to-Speech (TTS) y Speech-to-Text (STT)
# -------------------------------------------------------------

async def tts_generate(text: str, voice_id: str | None = None) -> bytes:
    """
    Convierte texto a audio usando ElevenLabs.
    Devuelve los bytes del audio (mp3).
    """
    voice_id = voice_id or settings.ELEVEN_VOICE_ID
    url = f"{settings.ELEVEN_TTS_URL}/{voice_id}"

    headers = {
        "xi-api-key": settings.ELEVEN_API_KEY,
        "Accept": "audio/mpeg",
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "model_id": "eleven_turbo_v2",
        "voice_settings": {
            "stability": 0.6,
            "similarity_boost": 0.8,
            "style": 0.3
        }
    }

    # Llamada a ElevenLabs (loguear solo metadata, no la API key)
    import logging
    logger = logging.getLogger("elevenlabs.service")
    logger.info("Calling ElevenLabs TTS: voice_id=%s text_len=%d", voice_id, len(text))
    logger.debug("TTS payload sample: %s", text[:200])

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(url, headers=headers, json=payload)
        logger.info("ElevenLabs TTS response: status=%s content-type=%s", response.status_code, response.headers.get("content-type"))
        response.raise_for_status()
        return response.content


async def stt_from_audio_bytes(audio_bytes: bytes) -> str:
    """
    Convierte audio (voz) a texto usando ElevenLabs STT.
    Recibe bytes de un archivo .wav o .mp3 y devuelve texto transcrito.
    """
    url = settings.ELEVEN_STT_URL
    headers = {"xi-api-key": settings.ELEVEN_API_KEY}
    files = {"file": ("input.mp3", audio_bytes, "audio/mpeg")}

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(url, headers=headers, files=files)
        response.raise_for_status()
        data = response.json()

    # ElevenLabs devuelve {"text": "Transcripción..."}
    return data.get("text", "")


# -------------------------------------------------------------
# 🎧 Alias de compatibilidad con routers antiguos
# -------------------------------------------------------------

async def tts_mp3(text: str, voice_id: str | None = None) -> bytes:
    """
    Alias de compatibilidad: redirige a tts_generate().
    Esto permite que los routers antiguos (tts.py) funcionen sin cambios.
    """
    return await tts_generate(text, voice_id)


async def tts_generate_with_options(text: str, voice_id: str | None = None, force_spanish: bool = False) -> bytes:
    # Si se pide forzar español, prefijar una instrucción corta para intentar que la voz use español
    if force_spanish:
        text = f"Por favor, habla en español: {text}"
    return await tts_generate(text, voice_id)
