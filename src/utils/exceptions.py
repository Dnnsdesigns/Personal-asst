"""Custom exceptions for the Personal Assistant."""


class AssistantError(Exception):
    """Base exception for assistant-related errors."""
    pass


class ConfigurationError(AssistantError):
    """Raised when there's a configuration issue."""
    pass


class PluginError(AssistantError):
    """Raised when there's a plugin-related error."""
    pass


class AIError(AssistantError):
    """Raised when there's an AI model-related error."""
    pass


class UIError(AssistantError):
    """Raised when there's a user interface error."""
    pass