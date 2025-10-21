import httpx
from ..config import settings

# -------------------------------------------------------------
# 🤖 Servicio de conexión con OpenRouter (IA)
# -------------------------------------------------------------

async def chat_completion(messages: list[dict]) -> str:
    """
    Envía una conversación al modelo configurado en OpenRouter
    y devuelve la respuesta de texto.
    """

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://gym-ai.local",  # identificador opcional
        "X-Title": settings.APP_NAME,
        "Content-Type": "application/json",
    }

    payload = {
        "model": settings.OPENROUTER_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 800,
    }

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

    # OpenRouter devuelve la respuesta en choices[0]["message"]["content"]
    return data["choices"][0]["message"]["content"].strip()
