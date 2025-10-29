# Personal Assistant 🤖

An intelligent AI-powered personal assistant built with Python, designed to help automate daily tasks, answer questions, and provide personalized assistance through multiple interfaces.

## Features

- 🧠 **AI-Powered Conversations** - Natural language processing using OpenAI GPT models
- 🗣️ **Voice Interface** - Speech recognition and text-to-speech capabilities
- 🌐 **Web UI** - Clean Streamlit-based web interface
- 💻 **CLI Interface** - Command-line interface for power users
- 🔌 **Extensible Plugin System** - Easy to add new capabilities
- 📝 **Task Management** - Create, track, and manage personal tasks
- 🔍 **Information Retrieval** - Search and summarize information from various sources
- ⚙️ **Configurable** - Customizable settings and preferences

## Quick Start

### Prerequisites

- Python 3.9 or higher
- OpenAI API key (for AI functionality)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/personal-assistant.git
   cd personal-assistant
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # Or for development
   pip install -e ".[dev,ui,voice]"
   ```

4. **Set up environment variables**
   ```bash
   cp config/config.example.yaml config/config.yaml
   # Edit config/config.yaml with your API keys and preferences
   ```

5. **Run the assistant**
   ```bash
   # CLI interface
   python -m src.main

   # Web interface
   streamlit run src/ui/web_app.py

   # Or using the installed script
   personal-assistant --help
   ```

## Usage

### Command Line Interface
```bash
# Start interactive mode
personal-assistant

# Ask a question directly
personal-assistant ask "What's the weather like today?"

# Manage tasks
personal-assistant task add "Buy groceries"
personal-assistant task list

# Voice mode
personal-assistant --voice
```

### Web Interface
Launch the web UI with `streamlit run src/ui/web_app.py` and navigate to `http://localhost:8501`

## Configuration

Edit `config/config.yaml` to customize:
- AI model settings
- Voice preferences
- Task management options
- Plugin configurations

## Project Structure

```
personal-assistant/
├── src/                    # Main source code
│   ├── core/              # Core assistant logic
│   ├── plugins/           # Extensible plugins
│   ├── ui/                # User interfaces
│   └── utils/             # Utility functions
├── tests/                 # Test suite
├── config/                # Configuration files
├── docs/                  # Documentation
└── .github/               # GitHub workflows and templates
```

## Development

### Setup Development Environment
```bash
pip install -e ".[dev]"
pre-commit install
```

### Running Tests
```bash
pytest
# With coverage
pytest --cov=src
```

### Code Quality
```bash
black src tests
flake8 src tests
mypy src
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for the GPT models
- LangChain for the AI framework
- Streamlit for the web interface
- All contributors and the open-source community