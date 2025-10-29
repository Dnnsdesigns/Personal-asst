# Copilot Instructions for Personal Assistant Project

## Architecture Overview

This is a Python-based AI personal assistant with a modular architecture:

- **`src/core/`** - Core assistant logic, AI models, and conversation handling
- **`src/plugins/`** - Extensible plugin system for adding capabilities (tasks, etc.)
- **`src/ui/`** - CLI interface for user interaction
- **`src/utils/`** - Shared utilities for exceptions and logging
- **`config/`** - YAML-based configuration with example templates

## Key Patterns

### Configuration Management
- Use `config/config.yaml` for settings, with `config/config.example.yaml` as template
- Environment variables override YAML settings via `python-dotenv`
- Pydantic models validate configuration in `src/core/config.py`
- Config loader checks for `config/local.yaml`, then `config/config.yaml`, falls back to example

### Plugin Architecture
- Plugins inherit from `BasePlugin` in `src/core/plugin_base.py`
- Auto-discovery via `src/core/plugin_manager.py`
- Each plugin implements: `get_capabilities()`, `can_handle()`, `execute()`
- Plugin config sections stored in main config's `plugins` dictionary
- Example: `TaskPlugin` in `src/plugins/task_plugin.py`

### Conversation Management
- Basic conversation handling in `src/core/conversation.py`
- Maintains conversation history with timestamps
- Currently uses placeholder AI responses (AI integration is planned)
- History limited to last 50 exchanges for memory management

### Error Handling
- Custom exceptions in `src/utils/exceptions.py`:
  - `AssistantError` - Base exception
  - `ConfigurationError`, `PluginError`, `AIError`, `UIError` - Specific errors
- Rich console output for user-friendly messages in CLI

### Logging
- Logging utilities in `src/utils/logging.py`
- Configurable via `setup_logging()` function
- Supports console and optional file logging
- Log level controlled by config or `--debug` flag

## Development Workflows

### Setup
```bash
pip install -e ".[dev,ui,voice]"  # Editable install with all extras
pre-commit install                # Git hooks for code quality (if configured)
```

### Running the Application
```bash
# Interactive CLI mode
python -m src.main

# Or using the installed command
personal-assistant

# Ask a single question
personal-assistant ask "What can you do?"

# Enable debug logging
personal-assistant --debug

# Custom config file
personal-assistant --config path/to/config.yaml
```

### Testing
```bash
pytest                           # Run tests
pytest --cov=src                 # Run with coverage (requires pytest-cov)
pytest tests/test_task_plugin.py # Run specific test file
```

### Code Quality
- Black (88 char line length) for formatting
- flake8, mypy for linting and type checking (configured in pyproject.toml)
- Tools specified in `[project.optional-dependencies]` dev section

### Configuration
- Never commit API keys - use `config/config.yaml` (gitignored)
- Copy `config/config.example.yaml` to `config/config.yaml` for local development
- Environment variables override config values (e.g., `OPENAI_API_KEY`, `AI_MODEL`, `LOG_LEVEL`)

## Current Structure

### Core Components
- **`src/main.py`** - Entry point using Typer for CLI commands
- **`src/core/assistant.py`** - `PersonalAssistant` class that orchestrates plugins and conversation
- **`src/core/config.py`** - Configuration models (AIConfig, UIConfig, LoggingConfig) and loader
- **`src/core/conversation.py`** - `ConversationManager` for conversation history
- **`src/core/plugin_manager.py`** - `PluginManager` for loading and managing plugins
- **`src/core/plugin_base.py`** - `BasePlugin` abstract base class

### UI Layer
- **`src/ui/cli.py`** - `CLIInterface` using Rich for interactive CLI
  - Commands: help, status, capabilities, reset, quit/exit/bye
  - Displays prompts, responses, tables, and panels

### Plugins
- **`src/plugins/task_plugin.py`** - `TaskPlugin` for task management
  - Commands: add task, list tasks, complete task, remove task
  - In-memory task storage (not persistent)

### Utilities
- **`src/utils/exceptions.py`** - Custom exception classes
- **`src/utils/logging.py`** - Logging setup function

## Data Flow

1. User input → CLI (`src/ui/cli.py`)
2. Input processing → Core assistant (`src/core/assistant.py`)
3. Plugin routing → Plugin manager finds capable plugin via `can_handle()`
4. Plugin execution → Plugin's `execute()` method processes input
5. Response formatting → Return to CLI and display with Rich

## Common Tasks

### Adding a New Plugin
1. Create a new file in `src/plugins/` (e.g., `my_plugin.py`)
2. Create a class inheriting from `BasePlugin`
3. Implement required methods:
   - `get_capabilities()` - Return plugin metadata
   - `can_handle(user_input)` - Return True if plugin handles the input
   - `execute(user_input, context)` - Process and return response
4. Optionally implement `get_commands()` and `get_help()`
5. Add plugin config to `config/config.example.yaml` under `plugins:` section
6. Plugin manager auto-discovers on startup from filename

### Modifying Conversation Handling
- Edit `src/core/conversation.py`
- Implement actual AI integration in `get_response()` method
- Update `initialize()` to set up AI client
- History managed via `add_exchange()` method

### Adding CLI Commands
- Edit `src/ui/cli.py` to add new commands to `start()` method
- Or extend `src/main.py` to add new Typer commands
- Use Rich components (Table, Panel, Console) for formatted output