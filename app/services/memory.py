from collections import defaultdict, deque

from app.models.schemas import Message


class ConversationMemory:
    def __init__(self, max_messages: int = 12) -> None:
        self.max_messages = max_messages
        self._store: dict[str, deque[Message]] = defaultdict(lambda: deque(maxlen=max_messages))

    def add(self, session_id: str, message: Message) -> None:
        self._store[session_id].append(message)

    def get(self, session_id: str) -> list[Message]:
        return list(self._store[session_id])
