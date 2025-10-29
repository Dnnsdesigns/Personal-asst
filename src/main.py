"""Main entry point for the Personal Assistant application."""

import typer
from typing import Optional
from rich.console import Console
from rich.panel import Panel

from src.core.assistant import PersonalAssistant
from src.core.config import load_config
from src.ui.cli import CLIInterface
from src.utils.logging import setup_logging

app = typer.Typer(
    name="personal-assistant",
    help="AI-powered personal assistant",
    add_completion=False,
)
console = Console()


@app.command()
def main(
    config_path: Optional[str] = typer.Option(
        None, "--config", "-c", help="Path to configuration file"
    ),
    voice: bool = typer.Option(False, "--voice", "-v", help="Enable voice interface"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug logging"),
) -> None:
    """Start the personal assistant."""
    try:
        # Setup logging
        setup_logging(debug=debug)
        
        # Load configuration
        config = load_config(config_path)
        
        # Initialize assistant
        assistant = PersonalAssistant(config)
        
        # Create CLI interface
        cli = CLIInterface(assistant, voice_enabled=voice)
        
        # Welcome message
        console.print(
            Panel.fit(
                "🤖 Personal Assistant\nType 'help' for commands or 'quit' to exit",
                style="bold blue",
            )
        )
        
        # Start interactive session
        cli.start()
        
    except KeyboardInterrupt:
        console.print("\n👋 Goodbye!")
    except Exception as e:
        console.print(f"❌ Error: {e}", style="bold red")
        raise typer.Exit(1)


@app.command()
def ask(
    question: str = typer.Argument(..., help="Question to ask the assistant"),
    config_path: Optional[str] = typer.Option(
        None, "--config", "-c", help="Path to configuration file"
    ),
) -> None:
    """Ask the assistant a single question."""
    try:
        config = load_config(config_path)
        assistant = PersonalAssistant(config)
        
        response = assistant.process_input(question)
        console.print(f"🤖 {response}")
        
    except Exception as e:
        console.print(f"❌ Error: {e}", style="bold red")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()