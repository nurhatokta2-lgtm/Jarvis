class AssistantError(Exception):
    """Base error for assistant domain failures."""


class ProviderUnavailableError(AssistantError):
    """Raised when an AI provider cannot answer."""


class TTSGenerationError(AssistantError):
    """Raised when TTS audio generation fails."""
