import pytest

from app.models.schemas import Message
from app.plugins.registry import PluginRegistry
from app.plugins.sentiment import SentimentPlugin
from app.services.memory import ConversationMemory


@pytest.mark.asyncio
async def test_plugin_registry_runs_all():
    registry = PluginRegistry()
    registry.register(SentimentPlugin())
    result = await registry.run_all("I feel great today")
    assert result["sentiment"]["mood"] == "positive"


def test_conversation_memory_keeps_recent_messages():
    memory = ConversationMemory(max_messages=2)
    memory.add("s1", Message(role="user", content="A"))
    memory.add("s1", Message(role="assistant", content="B"))
    memory.add("s1", Message(role="user", content="C"))
    history = memory.get("s1")
    assert len(history) == 2
    assert history[0].content == "B"
