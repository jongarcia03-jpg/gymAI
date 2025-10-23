from pydantic_settings import BaseSettings
from pydantic import Field, model_validator


class Settings(BaseSettings):
    # --- ⚙️ Configuración general ---
    APP_NAME: str = "GymAI"
    APP_DEBUG: bool = Field(default=False, description="Modo debug (True para desarrollo)")

    # Secret / JWT (aceptamos ambos nombres como alias)
    SECRET_KEY: str | None = None
    JWT_SECRET: str | None = None

    # --- 🧠 API Keys ---
    OPENROUTER_API_KEY: str | None = None
    OPENROUTER_MODEL: str | None = None

    ELEVENLABS_API_KEY: str | None = None
    ELEVEN_API_KEY: str | None = None
    ELEVEN_VOICE_ID: str | None = None
    ELEVEN_TTS_URL: str | None = None
    ELEVEN_STT_URL: str | None = None

    # --- 💾 Base de datos ---
    DATABASE_URL: str = Field(default="sqlite:///./gymai.db", description="URL de conexión a la base de datos")

    # --- 🌐 CORS ---
    ALLOWED_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @model_validator(mode="after")
    def coalesce_aliases(self):
        # Si se definió JWT_SECRET en .env, úsalo como SECRET_KEY
        if not self.SECRET_KEY and self.JWT_SECRET:
            object.__setattr__(self, "SECRET_KEY", self.JWT_SECRET)

        # Aceptar ELEVEN_API_KEY como alias de ELEVENLABS_API_KEY
        if not self.ELEVENLABS_API_KEY and self.ELEVEN_API_KEY:
            object.__setattr__(self, "ELEVENLABS_API_KEY", self.ELEVEN_API_KEY)

        # Si hay variables específicas de ElevenLabs en .env, dejar disponibles
        # (ya están en el modelo como ELEVEN_VOICE_ID, ELEVEN_TTS_URL, ELEVEN_STT_URL)

        return self


# Instancia global
settings = Settings()
