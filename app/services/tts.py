from __future__ import annotations

import uuid
from pathlib import Path

import edge_tts

from app.core.errors import TTSGenerationError


class AdaTTSService:
    def __init__(self, voice_name: str, output_dir: str = "./data/audio") -> None:
        self.voice_name = voice_name
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def synthesize(self, text: str) -> str:
        try:
            file_name = f"{uuid.uuid4().hex}.mp3"
            output_path = self.output_dir / file_name
            communicate = edge_tts.Communicate(text=text, voice=self.voice_name)
            await communicate.save(str(output_path))
            return f"/audio/{file_name}"
        except Exception as exc:  # noqa: BLE001
            raise TTSGenerationError(f"Unable to generate Ada voice output: {exc}") from exc
