from app.core.config import get_settings
from app.plugins.registry import PluginRegistry
from app.plugins.sentiment import SentimentPlugin
from app.services.ai_provider import GeminiProvider
from app.services.analytics import AnalyticsStore
from app.services.assistant import AssistantEngine
from app.services.memory import ConversationMemory
from app.services.tts import AdaTTSService

_engine: AssistantEngine | None = None


def get_engine() -> AssistantEngine:
    global _engine
    if _engine is None:
        settings = get_settings()
        plugins = PluginRegistry()
        plugins.register(SentimentPlugin())
        _engine = AssistantEngine(
            llm=GeminiProvider(api_key=settings.google_api_key, model_name=settings.gemini_model),
            memory=ConversationMemory(max_messages=settings.max_context_messages),
            analytics=AnalyticsStore(db_path=f"{settings.data_dir}/analytics.db"),
            plugins=plugins,
            tts=AdaTTSService(voice_name=settings.ada_voice_name),
            model_name=settings.gemini_model,
        )
    return _engine
