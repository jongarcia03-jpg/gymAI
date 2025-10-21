import re
from typing import Optional

# -------------------------------------------------------------
# 🎥 UTILIDADES DE YOUTUBE
# -------------------------------------------------------------

YOUTUBE_URL_PATTERN = re.compile(
    r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w\-]{11})"
)


def extract_video_id(url: str) -> Optional[str]:
    """
    Extrae el ID del video de YouTube desde un enlace.
    Ejemplo: https://youtu.be/dQw4w9WgXcQ → dQw4w9WgXcQ
    """
    match = YOUTUBE_URL_PATTERN.match(url)
    return match.group(1) if match else None


def get_thumbnail_url(youtube_url: str) -> Optional[str]:
    """
    Devuelve la URL de miniatura del video.
    """
    video_id = extract_video_id(youtube_url)
    if not video_id:
        return None
    return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"


def embed_url(youtube_url: str) -> Optional[str]:
    """
    Devuelve el enlace embebido para mostrar el video dentro de un iframe.
    """
    video_id = extract_video_id(youtube_url)
    if not video_id:
        return None
    return f"https://www.youtube.com/embed/{video_id}"
