from __future__ import annotations

from langchain_openai import ChatOpenAI

from .config import get_settings


def build_chat_model() -> ChatOpenAI:
    settings = get_settings()
    return ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key)
