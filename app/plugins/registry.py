from __future__ import annotations

from app.plugins.base import Plugin


class PluginRegistry:
    def __init__(self) -> None:
        self._plugins: dict[str, Plugin] = {}

    def register(self, plugin: Plugin) -> None:
        self._plugins[plugin.name] = plugin

    async def run_all(self, user_input: str) -> dict:
        result: dict = {}
        for name, plugin in self._plugins.items():
            result[name] = await plugin.run(user_input)
        return result
