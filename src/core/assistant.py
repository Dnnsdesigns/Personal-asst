"""Core assistant class that orchestrates all functionality."""

from typing import Dict, Any, Optional
import logging
from datetime import datetime

from src.core.config import Config
from src.core.plugin_manager import PluginManager
from src.core.conversation import ConversationManager
from src.utils.exceptions import AssistantError

logger = logging.getLogger(__name__)


class PersonalAssistant:
    """Main assistant class that handles user interactions and coordinates plugins."""

    def __init__(self, config: Config):
        """Initialize the personal assistant.
        
        Args:
            config: Configuration object containing all settings
        """
        self.config = config
        self.plugin_manager = PluginManager(config)
        self.conversation_manager = ConversationManager(config)
        self._initialize()

    def _initialize(self) -> None:
        """Initialize the assistant components."""
        try:
            # Load plugins
            self.plugin_manager.load_plugins()
            logger.info(f"Loaded {len(self.plugin_manager.plugins)} plugins")
            
            # Initialize conversation
            self.conversation_manager.initialize()
            logger.info("Assistant initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize assistant: {e}")
            raise AssistantError(f"Initialization failed: {e}")

    def process_input(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Process user input and return a response.
        
        Args:
            user_input: The user's input text
            context: Optional context information
            
        Returns:
            The assistant's response
        """
        try:
            # Add timestamp and context
            enhanced_context = {
                "timestamp": datetime.now().isoformat(),
                "user_input": user_input,
                **(context or {})
            }
            
            # Check if any plugin can handle this input
            for plugin in self.plugin_manager.plugins.values():
                if plugin.can_handle(user_input):
                    logger.info(f"Routing to plugin: {plugin.__class__.__name__}")
                    response = plugin.execute(user_input, enhanced_context)
                    
                    # Add to conversation history
                    self.conversation_manager.add_exchange(user_input, response)
                    return response
            
            # If no plugin handles it, use general conversation
            response = self.conversation_manager.get_response(user_input, enhanced_context)
            return response
            
        except Exception as e:
            logger.error(f"Error processing input: {e}")
            return f"I'm sorry, I encountered an error: {str(e)}"

    def get_capabilities(self) -> Dict[str, Any]:
        """Get a summary of the assistant's capabilities.
        
        Returns:
            Dictionary describing available capabilities
        """
        capabilities = {
            "plugins": {},
            "conversation": self.conversation_manager.is_available(),
            "timestamp": datetime.now().isoformat()
        }
        
        for name, plugin in self.plugin_manager.plugins.items():
            capabilities["plugins"][name] = plugin.get_capabilities()
            
        return capabilities

    def reset_conversation(self) -> None:
        """Reset the conversation history."""
        self.conversation_manager.reset()
        logger.info("Conversation history reset")

    def get_status(self) -> Dict[str, Any]:
        """Get current status of the assistant.
        
        Returns:
            Status information
        """
        return {
            "plugins_loaded": len(self.plugin_manager.plugins),
            "conversation_active": self.conversation_manager.is_active(),
            "last_interaction": self.conversation_manager.get_last_interaction_time(),
            "capabilities": list(self.plugin_manager.plugins.keys())
        }