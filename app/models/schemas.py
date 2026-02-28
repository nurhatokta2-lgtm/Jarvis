from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str
    ts: datetime = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    session_id: str = Field(default="default")
    message: str
    use_voice: bool = True


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    model: str
    latency_ms: int
    audio_url: str | None = None
    plugin_data: dict[str, Any] = Field(default_factory=dict)


class HealthResponse(BaseModel):
    status: str
    app: str
    env: str


class AnalyticsSnapshot(BaseModel):
    total_requests: int
    avg_latency_ms: float
    top_sessions: list[dict[str, Any]]
