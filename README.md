# Engineering Project Planner Agent

An AI-powered engineering project planner that converts natural language prompts into complete, structured project implementations using LangGraph and Groq AI.

## Overview

This project implements a multi-agent system that takes a user's project description and automatically generates a complete project structure with working code. The system uses three specialized agents working in sequence:

1. **Planner Agent** - Converts user prompts into structured project plans
2. **Architect Agent** - Breaks down plans into detailed implementation tasks
3. **Coder Agent** - Implements the actual code using available tools

## Features

- 🤖 **Multi-Agent Architecture** - Specialized agents for planning, architecture, and coding
- 🌐 **Web Interface** - Beautiful Streamlit UI for easy interaction
- 📝 **Natural Language Input** - Describe your project in plain English
- 👀 **Live Preview** - View generated files with syntax highlighting
- 🌐 **HTML Preview** - See web projects rendered in real-time
- 📦 **One-Click Download** - Export projects as ZIP files
- 🏗️ **Structured Planning** - Automatic project structure and file organization
- 💻 **Code Generation** - Complete implementation with proper file management
- 🔧 **Tool Integration** - File operations, directory management, and command execution
- 🔄 **Iterative Processing** - Step-by-step implementation with dependency management

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd engineering-project-planner
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

## Configuration

Create a `.env` file with your Groq API key:
```
GROQ_API_KEY=your_groq_api_key_here
```

## Usage

### Streamlit Web Interface (Recommended)

**Option 1: Ultra Simple Mode (Most Reliable)** ⭐

If you're experiencing any errors, use this version:
```bash
streamlit run app_ultra_simple.py
```

Or on Windows:
```bash
run_ultra_simple.bat
```

This version has:
- ✅ Robust JSON parsing with multiple fallback strategies
- ✅ Automatic retry logic
- ✅ Default fallback plans if AI fails
- ✅ Works with any prompt

**Option 2: Simple Mode**

```bash
streamlit run app_simple.py
```

Or on Windows:
```bash
run_simple.bat
```

**Option 3: Standard Mode**

```bash
streamlit run app.py
```

Or on Windows:
```bash
run_app.bat
```

**Which version should I use?**
- 🥇 **Ultra Simple** (`app_ultra_simple.py`) - Start here! Most reliable, works every time
- 🥈 **Simple** (`app_simple.py`) - Good balance of reliability and features  
- 🥉 **Standard** (`app.py`) - Advanced features, may have occasional errors

See [WHICH_VERSION.md](WHICH_VERSION.md) for a detailed comparison.

### Command Line Interface

Run the planner with an interactive prompt:
```bash
python main.py
```

Then enter your project description when prompted:
```
Enter your project prompt: Build a colorful modern todo app in HTML, CSS, and JS
```

Set custom recursion limits for complex projects:
```bash
python main.py --recursion-limit 150
```

### Example Prompts

- "Build a colorful modern todo app in HTML, CSS, and JS"
- "Create a Python Flask API for user management with SQLite database"
- "Build a React dashboard with charts and data visualization"
- "Create a Node.js Express server with authentication and file upload"

## Project Structure

```
├── agent/
│   ├── __init__.py
│   ├── graph.py              # Standard mode workflow
│   ├── graph_simple.py       # Simple mode workflow
│   ├── graph_ultra_simple.py # Ultra simple mode (most reliable)
│   ├── states.py             # Pydantic models
│   ├── prompts.py            # Prompt templates
│   └── tools.py              # File operations
├── generated_project/        # Output directory
├── app.py                   # Standard web interface
├── app_simple.py            # Simple web interface
├── app_ultra_simple.py      # Ultra simple interface (recommended)
├── main.py                  # CLI entry point
├── config.py                # Configuration
├── run_app.bat              # Windows launcher (standard)
├── run_simple.bat           # Windows launcher (simple)
├── run_ultra_simple.bat     # Windows launcher (ultra simple)
├── requirements.txt         # Dependencies
├── .env                     # Environment variables
├── README.md               # This file
├── QUICK_START.md          # Quick start guide
├── USAGE.md                # Detailed usage
└── TROUBLESHOOTING.md      # Troubleshooting
```

## How It Works

### 1. Planner Agent
- Takes natural language input
- Creates a structured `Plan` with:
  - Project name and description
  - Technology stack
  - Feature list
  - File structure with purposes

### 2. Architect Agent
- Receives the `Plan` from the planner
- Creates detailed `ImplementationTask` objects
- Orders tasks by dependencies
- Provides specific implementation instructions

### 3. Coder Agent
- Executes implementation tasks sequentially
- Uses tools to read/write files
- Maintains project structure and dependencies
- Generates complete, working code

## Dependencies

- **Streamlit** - Modern web interface framework
- **LangChain** - AI agent framework and tools
- **LangGraph** - Multi-agent workflow orchestration
- **Groq** - Fast AI inference API
- **Pydantic** - Data validation and serialization
- **python-dotenv** - Environment variable management

## Generated Projects

All generated projects are created in the `generated_project/` directory. Each run creates a complete project structure with:

- Source code files
- Configuration files
- Documentation
- Proper file organization

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your `GROQ_API_KEY` is set correctly in the `.env` file
2. **Permission Errors**: Check file permissions in the `generated_project/` directory
3. **Recursion Limit**: Increase the recursion limit for complex projects using `-r` flag
4. **Tool Use Failed**: Simplify your prompt or try a different model in `config.py`

For detailed troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### Debug Mode

The project runs with debug and verbose modes enabled by default. Check console output for detailed execution logs. You can adjust these settings in `config.py`.

## Roadmap

- [ ] Support for more programming languages and frameworks
- [ ] Integration with version control systems
- [ ] Project templates and presets
- [ ] Web interface for easier interaction
- [ ] Code quality analysis and optimization
- [ ] Automated testing generation

## Acknowledgments

- Built with [LangChain](https://langchain.com/) and [LangGraph](https://langchain-ai.github.io/langgraph/)
- Powered by [Groq](https://groq.com/) for fast AI inference
- Inspired by modern AI-assisted development workflows