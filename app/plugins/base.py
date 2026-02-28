from __future__ import annotations

from abc import ABC, abstractmethod


class Plugin(ABC):
    name: str

    @abstractmethod
    async def run(self, user_input: str) -> dict:
        raise NotImplementedError
