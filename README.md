# CodeBuildBrowser

Small Flask-based frontend and agent layer that integrates with Ollama models.

Purpose
- Provide a minimal web UI to chat with a local Ollama model, check model health, and inspect outputs.

Dependencies
- See `requirements.txt` for Python dependencies. Install with `pip install -r requirements.txt`.
- Ollama (local model runtime) is required to run models locally. Follow the official installer at https://ollama.ai.

Quick start
1. Clone the repository and open a terminal in the repo root.
2. Create and activate a virtual environment, then install Python dependencies.

<details>
<summary>Windows (PowerShell)</summary>

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

</details>

<details>
<summary>macOS / Linux (bash/zsh)</summary>

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

</details>

Ollama and model
- Install Ollama following the official instructions: https://ollama.ai
- Verify the `ollama` CLI is available:

```bash
ollama --version
```

- Pull the model used by the app (default in `agents/base_agent.py`):

```bash
ollama pull qwen3:30b
```

Run the app
- From the repository root, run the Flask app:

```bash
python ollama-agents/ollama-app.py
```

Notes and troubleshooting
- If the app cannot find the model, run `ollama ls` to list available models and confirm the model name.
- If `ollama` is not found, ensure the Ollama binary is on your PATH and restart the terminal.
- For production use, add minification and cache-busting for static assets.

Credits
- See `CodeBuildBrowser.md` for a brief project guide and usage tips.
