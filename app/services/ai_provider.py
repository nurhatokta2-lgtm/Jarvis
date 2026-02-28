from __future__ import annotations

import logging
from abc import ABC, abstractmethod

import google.generativeai as genai

from app.core.errors import ProviderUnavailableError
from app.models.schemas import Message

logger = logging.getLogger(__name__)


class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, history: list[Message]) -> str:
        raise NotImplementedError


class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str, model_name: str) -> None:
        self.model_name = model_name
        self.enabled = bool(api_key)
        if self.enabled:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model_name=model_name)
        else:
            self.model = None

    async def generate(self, prompt: str, history: list[Message]) -> str:
        if not self.enabled or not self.model:
            logger.warning("Gemini API key not configured; using local fallback response.")
            return f"[Fallback mode] You said: {prompt}"

        parts = []
        for msg in history[-8:]:
            parts.append(f"{msg.role}: {msg.content}")
        parts.append(f"user: {prompt}")
        final_prompt = "\n".join(parts)

        try:
            response = await self.model.generate_content_async(final_prompt)
            text = (response.text or "").strip()
            if not text:
                raise ProviderUnavailableError("Gemini returned empty text")
            return text
        except Exception as exc:  # noqa: BLE001
            raise ProviderUnavailableError(f"Gemini generation failed: {exc}") from exc
