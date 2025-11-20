# CodeBuildBrowser — Quick Guide

Overview
- CodeBuildBrowser is a small Flask-based frontend and agent layer that ties into Ollama models to provide an interactive chat UI, health checks, and simple capabilities/endpoints (JSON viewer, health, capabilities).

Key functionality
- Web UI: a simple chat interface that sends messages to the agent and shows responses.
- Health endpoint: `/health` that returns model status for programmatic and UI checks.
- Capabilities/JSON viewer: endpoints to inspect responses and model capabilities.
- Agent layer: `agents/base_agent.py` integrates with the Ollama client to call a local model (default: `qwen3:30b`).

Requirements
- Windows, macOS, or Linux
- Python 3.10+ (recommended)
- Ollama (local model runtime)

Quick setup
1. Clone the repository and open a PowerShell terminal in the repo root.

2. Create and activate a Python virtual environment:

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
```

3. Install Python dependencies (if you have a `requirements.txt`, use it). If not, install the essentials:

```powershell
pip install flask ollama
```

4. Install Ollama
- Follow official instructions at https://ollama.ai for the platform-specific installer. On Windows this typically involves running the installer and ensuring `ollama` is available in your PATH.

5. Download the model used by the app
- The agent defaults to `qwen3:30b` in `agents/base_agent.py`. Use Ollama to pull a model like this:

```powershell
# Example: pull qwen3:30b (replace with the exact model name you need)
ollama pull qwen3:30b
```

6. Run the Flask app
- If the project entrypoint is `ollama-app.py` or a similar file, run it via Python. Example (adjust path if needed):

```powershell
python -m ollama_agents.ollama-app
# or, if running directly:
python ollama-app.py
```

Notes and tips
- If the app cannot connect to a model, check `ollama ls` to confirm the model name and `ollama serve` (if applicable) or that the Ollama service is running.
- For production or frequent development, consider creating a build step to bundle and minify static assets (CSS/JS) and add cache-busting.
- The default model name can be changed in `agents/base_agent.py` constructor.

Troubleshooting
- `ollama` not found: ensure the Ollama binary is on your PATH and restart the terminal.
- Model pull fails: confirm the model name is correct and your Ollama installation supports the model.

License and credits
- See `README.md` for repository credits and links.
