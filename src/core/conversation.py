"""Conversation management for the Personal Assistant."""

from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

from src.core.config import Config
from src.utils.exceptions import AIError

logger = logging.getLogger(__name__)


class ConversationManager:
    """Manages conversation history and AI interactions."""

    def __init__(self, config: Config):
        """Initialize the conversation manager.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.conversation_history: List[Dict[str, Any]] = []
        self._ai_client = None
        self._initialized = False

    def initialize(self) -> None:
        """Initialize the AI client."""
        try:
            # This would initialize the actual AI client (OpenAI, etc.)
            # For now, we'll just mark as initialized
            self._initialized = True
            logger.info("Conversation manager initialized")
        except Exception as e:
            logger.error(f"Failed to initialize conversation manager: {e}")
            raise AIError(f"AI initialization failed: {e}")

    def get_response(self, user_input: str, context: Dict[str, Any]) -> str:
        """Get an AI response to user input.
        
        Args:
            user_input: The user's input
            context: Additional context
            
        Returns:
            AI response string
        """
        if not self._initialized:
            return "I'm not properly initialized yet. Please check the configuration."

        try:
            # For now, return a simple response
            # In a real implementation, this would call the AI model
            response = f"I understand you said: '{user_input}'. I'm still learning how to help you better!"
            
            # Add to conversation history
            self.add_exchange(user_input, response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error getting AI response: {e}")
            return f"I encountered an error: {str(e)}"

    def add_exchange(self, user_input: str, assistant_response: str) -> None:
        """Add a conversation exchange to history.
        
        Args:
            user_input: The user's input
            assistant_response: The assistant's response
        """
        exchange = {
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "assistant": assistant_response
        }
        self.conversation_history.append(exchange)
        
        # Keep only last 50 exchanges to manage memory
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-50:]

    def reset(self) -> None:
        """Reset conversation history."""
        self.conversation_history.clear()

    def get_history(self) -> List[Dict[str, Any]]:
        """Get conversation history.
        
        Returns:
            List of conversation exchanges
        """
        return self.conversation_history.copy()

    def is_available(self) -> bool:
        """Check if conversation manager is available.
        
        Returns:
            True if available, False otherwise
        """
        return self._initialized

    def is_active(self) -> bool:
        """Check if there's an active conversation.
        
        Returns:
            True if there are recent exchanges
        """
        return len(self.conversation_history) > 0

    def get_last_interaction_time(self) -> Optional[str]:
        """Get timestamp of last interaction.
        
        Returns:
            ISO timestamp string or None
        """
        if self.conversation_history:
            return self.conversation_history[-1]["timestamp"]
        return None