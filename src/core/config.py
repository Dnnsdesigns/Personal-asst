"""Configuration management for the Personal Assistant."""

from typing import Dict, Any, Optional
from pathlib import Path
import yaml
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


class AIConfig(BaseModel):
    """AI model configuration."""
    provider: str = Field(default="openai", description="AI provider (openai, anthropic, etc.)")
    model: str = Field(default="gpt-3.5-turbo", description="Model name")
    api_key: Optional[str] = Field(default=None, description="API key")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Model temperature")
    max_tokens: int = Field(default=1000, gt=0, description="Maximum tokens per response")


class UIConfig(BaseModel):
    """User interface configuration."""
    default_interface: str = Field(default="cli", description="Default interface (cli, web, voice)")
    voice_enabled: bool = Field(default=False, description="Enable voice interface")
    web_port: int = Field(default=8501, description="Web interface port")


class LoggingConfig(BaseModel):
    """Logging configuration."""
    level: str = Field(default="INFO", description="Logging level")
    format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file: Optional[str] = Field(default=None, description="Log file path")


class Config(BaseModel):
    """Main configuration class."""
    ai: AIConfig = Field(default_factory=AIConfig)
    ui: UIConfig = Field(default_factory=UIConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    plugins: Dict[str, Dict[str, Any]] = Field(default_factory=dict, description="Plugin configurations")

    def __init__(self, **data):
        super().__init__(**data)
        self._apply_env_overrides()

    def _apply_env_overrides(self) -> None:
        """Apply environment variable overrides."""
        # AI configuration overrides
        if os.getenv("OPENAI_API_KEY"):
            self.ai.api_key = os.getenv("OPENAI_API_KEY")
        if os.getenv("AI_MODEL"):
            self.ai.model = os.getenv("AI_MODEL")
        if os.getenv("AI_TEMPERATURE"):
            self.ai.temperature = float(os.getenv("AI_TEMPERATURE"))

        # UI configuration overrides
        if os.getenv("WEB_PORT"):
            self.ui.web_port = int(os.getenv("WEB_PORT"))
        if os.getenv("VOICE_ENABLED"):
            self.ui.voice_enabled = os.getenv("VOICE_ENABLED").lower() == "true"

        # Logging configuration overrides
        if os.getenv("LOG_LEVEL"):
            self.logging.level = os.getenv("LOG_LEVEL")


def load_config(config_path: Optional[str] = None) -> Config:
    """Load configuration from file and environment variables.
    
    Args:
        config_path: Optional path to config file
        
    Returns:
        Loaded configuration object
    """
    config_data = {}
    
    # Determine config file path
    if config_path:
        config_file = Path(config_path)
    else:
        # Look for config files in order of preference
        possible_paths = [
            Path("config/local.yaml"),
            Path("config/config.yaml"),
            Path("config/config.example.yaml"),
        ]
        config_file = None
        for path in possible_paths:
            if path.exists():
                config_file = path
                break
    
    # Load from file if it exists
    if config_file and config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f) or {}
    
    return Config(**config_data)