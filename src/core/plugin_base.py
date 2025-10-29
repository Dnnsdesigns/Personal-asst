"""Base class for all plugins."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BasePlugin(ABC):
    """Abstract base class for all plugins."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the plugin with configuration.
        
        Args:
            config: Plugin-specific configuration dictionary
        """
        self.config = config
        self.enabled = config.get("enabled", True)

    @abstractmethod
    def get_capabilities(self) -> Dict[str, Any]:
        """Return a description of the plugin's capabilities.
        
        Returns:
            Dictionary describing what the plugin can do
        """
        pass

    @abstractmethod
    def can_handle(self, user_input: str) -> bool:
        """Check if this plugin can handle the given user input.
        
        Args:
            user_input: The user's input text
            
        Returns:
            True if this plugin can handle the input, False otherwise
        """
        pass

    @abstractmethod
    def execute(self, user_input: str, context: Dict[str, Any]) -> str:
        """Execute the plugin's functionality.
        
        Args:
            user_input: The user's input text
            context: Additional context information
            
        Returns:
            The plugin's response
        """
        pass

    def get_commands(self) -> List[str]:
        """Get list of commands this plugin supports.
        
        Returns:
            List of command strings
        """
        return []

    def get_help(self) -> str:
        """Get help text for this plugin.
        
        Returns:
            Help text describing how to use the plugin
        """
        return "No help available for this plugin."

    def is_enabled(self) -> bool:
        """Check if the plugin is enabled.
        
        Returns:
            True if enabled, False otherwise
        """
        return self.enabled