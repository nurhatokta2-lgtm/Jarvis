from __future__ import annotations

import time

from app.models.schemas import ChatRequest, ChatResponse, Message
from app.plugins.registry import PluginRegistry
from app.services.ai_provider import LLMProvider
from app.services.analytics import AnalyticsStore
from app.services.memory import ConversationMemory
from app.services.tts import AdaTTSService


class AssistantEngine:
    def __init__(
        self,
        llm: LLMProvider,
        memory: ConversationMemory,
        analytics: AnalyticsStore,
        plugins: PluginRegistry,
        tts: AdaTTSService,
        model_name: str,
    ) -> None:
        self.llm = llm
        self.memory = memory
        self.analytics = analytics
        self.plugins = plugins
        self.tts = tts
        self.model_name = model_name

    async def chat(self, request: ChatRequest) -> ChatResponse:
        start = time.perf_counter()
        plugin_data = await self.plugins.run_all(request.message)

        history = self.memory.get(request.session_id)
        answer = await self.llm.generate(request.message, history)

        self.memory.add(request.session_id, Message(role="user", content=request.message))
        self.memory.add(request.session_id, Message(role="assistant", content=answer))

        latency_ms = int((time.perf_counter() - start) * 1000)
        self.analytics.log_chat(request.session_id, request.message, answer, latency_ms, self.model_name)

        audio_url = None
        if request.use_voice:
            audio_url = await self.tts.synthesize(answer)

        return ChatResponse(
            session_id=request.session_id,
            answer=answer,
            model=self.model_name,
            latency_ms=latency_ms,
            audio_url=audio_url,
            plugin_data=plugin_data,
        )
