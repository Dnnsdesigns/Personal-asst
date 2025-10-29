"""Command-line interface for the Personal Assistant."""

from typing import Optional
import logging
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel

from src.core.assistant import PersonalAssistant

logger = logging.getLogger(__name__)
console = Console()


class CLIInterface:
    """Command-line interface for interacting with the assistant."""

    def __init__(self, assistant: PersonalAssistant, voice_enabled: bool = False):
        """Initialize the CLI interface.
        
        Args:
            assistant: The personal assistant instance
            voice_enabled: Whether voice interface is enabled
        """
        self.assistant = assistant
        self.voice_enabled = voice_enabled
        self.running = False

    def start(self) -> None:
        """Start the interactive CLI session."""
        self.running = True
        console.print("Type 'help' for available commands or 'quit' to exit.\n")

        while self.running:
            try:
                user_input = Prompt.ask("🤖", default="").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    self.running = False
                    console.print("👋 Goodbye!")
                    break
                    
                if user_input.lower() == 'help':
                    self._show_help()
                    continue
                    
                if user_input.lower() == 'status':
                    self._show_status()
                    continue
                    
                if user_input.lower() == 'capabilities':
                    self._show_capabilities()
                    continue
                    
                if user_input.lower() == 'reset':
                    self.assistant.reset_conversation()
                    console.print("🔄 Conversation reset!")
                    continue

                # Process the input
                response = self.assistant.process_input(user_input)
                console.print(f"🤖 {response}\n")
                
            except KeyboardInterrupt:
                self.running = False
                console.print("\n👋 Goodbye!")
            except Exception as e:
                console.print(f"❌ Error: {e}", style="bold red")

    def _show_help(self) -> None:
        """Show help information."""
        help_table = Table(title="Available Commands")
        help_table.add_column("Command", style="cyan")
        help_table.add_column("Description", style="white")
        
        help_table.add_row("help", "Show this help message")
        help_table.add_row("status", "Show assistant status")
        help_table.add_row("capabilities", "Show available capabilities")
        help_table.add_row("reset", "Reset conversation history")
        help_table.add_row("quit/exit/bye", "Exit the assistant")
        
        console.print(help_table)
        console.print()

    def _show_status(self) -> None:
        """Show assistant status."""
        status = self.assistant.get_status()
        
        status_panel = Panel.fit(
            f"Plugins Loaded: {status['plugins_loaded']}\n"
            f"Conversation Active: {status['conversation_active']}\n"
            f"Last Interaction: {status['last_interaction'] or 'None'}\n"
            f"Voice Enabled: {self.voice_enabled}",
            title="Assistant Status",
            style="blue"
        )
        
        console.print(status_panel)
        console.print()

    def _show_capabilities(self) -> None:
        """Show assistant capabilities."""
        capabilities = self.assistant.get_capabilities()
        
        caps_table = Table(title="Assistant Capabilities")
        caps_table.add_column("Plugin", style="cyan")
        caps_table.add_column("Description", style="white")
        
        for plugin_name, plugin_caps in capabilities.get("plugins", {}).items():
            description = plugin_caps.get("description", "No description available")
            caps_table.add_row(plugin_name, description)
        
        if not capabilities.get("plugins"):
            caps_table.add_row("No plugins loaded", "")
            
        console.print(caps_table)
        console.print()