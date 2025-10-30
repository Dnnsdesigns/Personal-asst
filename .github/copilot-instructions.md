# Copilot Instructions for Personal Assistant Project

## Architecture Overview

This is a Python-based AI personal assistant with a modular architecture:

- **`src/core/`** - Core assistant logic, AI models, and conversation handling
- **`src/plugins/`** - Extensible plugin system for adding capabilities (tasks, weather, etc.)
- **`src/ui/`** - Multiple interfaces: CLI (`cli.py`), web (`web_app.py`), and voice
- **`src/utils/`** - Shared utilities for config, logging, and common functions
- **`config/`** - YAML-based configuration with environment-specific overrides

## Key Patterns

### Configuration Management
- Use `config/config.yaml` for settings, with `config.example.yaml` as template
- Environment variables override YAML settings via `python-dotenv`
- Pydantic models validate configuration in `src/core/config.py`

### Plugin Architecture
- Plugins inherit from `BasePlugin` in `src/core/plugin_base.py`
- Auto-discovery via `src/core/plugin_manager.py`
- Each plugin defines capabilities, commands, and dependencies

### AI Integration
- LangChain for AI orchestration with OpenAI models
- Conversation context managed in `src/core/conversation.py`
- Memory and session handling for multi-turn conversations

### Error Handling
- Custom exceptions in `src/core/exceptions.py`
- Rich console output for user-friendly error messages
- Comprehensive logging with structured JSON format

## Development Workflows

### Setup
```bash
pip install -e ".[dev,ui,voice]"  # Editable install with all extras
pre-commit install                # Git hooks for code quality
```

### Testing
```bash
pytest --cov=src                 # Run with coverage
pytest -m "not integration"      # Skip integration tests
```

### Code Quality
- Black (88 char line length), flake8, mypy enforced via CI
- Pre-commit hooks prevent commits without formatting

### Configuration
- Never commit API keys - use `config/config.yaml` (gitignored)
- Copy `config/config.example.yaml` for local development
- Environment-specific configs: `config/local.yaml`, `config/production.yaml`

## Integration Points

### External APIs
- OpenAI GPT models via `langchain-openai`
- Plugin-specific APIs handled in respective plugin modules
- Rate limiting and retry logic in `src/utils/api_client.py`

### Data Flow
1. User input → UI layer (`cli.py`, `web_app.py`)
2. Input processing → Core assistant (`src/core/assistant.py`)
3. Plugin routing → Plugin manager determines appropriate handler
4. AI processing → LangChain chains with context memory
5. Response formatting → Back through UI layer to user

### Voice Interface
- Speech recognition via `Speech recognition` library
- Text-to-speech with `pyttsx3`
- Audio processing utilities in `src/ui/voice.py`

## Common Tasks

### Adding New Plugin
1. Create class inheriting `BasePlugin` in `src/plugins/`
2. Implement required methods: `get_capabilities()`, `execute()`
3. Add plugin config section to `config.example.yaml`
4. Plugin manager auto-discovers on startup

### Extending AI Capabilities
- Modify prompts in `src/core/prompts.py`
- Add new LangChain chains in `src/core/chains/`
- Update conversation context handling as needed

### UI Customization
- Streamlit components in `src/ui/components/`
- CLI commands use Typer with Rich formatting
- Shared UI utilities in `src/ui/common.py`
