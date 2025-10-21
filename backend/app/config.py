from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "GymAI"
    APP_DEBUG: bool = True  # 🆕 añadido
    DATABASE_URL: str = "sqlite:///./gymai.db"

    # 🔐 Seguridad
    JWT_SECRET: str

    # 🤖 OpenRouter (IA)
    OPENROUTER_API_KEY: str
    OPENROUTER_MODEL: str

    # 🗣️ ElevenLabs (voz)
    ELEVEN_API_KEY: str
    ELEVEN_VOICE_ID: str
    ELEVEN_TTS_URL: str | None = None  # 🆕 añadido
    ELEVEN_STT_URL: str | None = None  # 🆕 añadido

    class Config:
        env_file = ".env"

settings = Settings()
