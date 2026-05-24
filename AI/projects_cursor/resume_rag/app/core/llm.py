from app.core.config import settings


def llm_configured() -> bool:
    return bool(settings.GROQ_API_KEY)


def get_chat_llm(*, streaming: bool = False):
    from langchain_groq import ChatGroq

    if not settings.GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not configured")

    return ChatGroq(
        model=settings.GROQ_MODEL,
        api_key=settings.GROQ_API_KEY,
        streaming=streaming,
    )
