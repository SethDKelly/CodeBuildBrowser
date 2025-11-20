
# CodeBuildBrowser

Minimal Flask web UI and agent layer for local Ollama models.

## Features
- Chat with Ollama models via web interface
- Health and capabilities endpoints
- Simple JSON viewer

## Setup
1. Clone the repository and open a terminal in the repo root.
2. Create and activate a Python virtual environment, then install dependencies:

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

## Ollama setup
1. Install Ollama: https://ollama.ai
2. Verify CLI:
	```bash
	ollama --version
	```
3. Pull the default model:
	```bash
	ollama pull qwen3:30b
	```

## Build static assets (optional)
To bundle and (optionally) minify CSS/JS for production, run:

```powershell
./scripts/build_static.ps1           # bundle only
./scripts/build_static.ps1 -Minify   # bundle and minify
```

## Run the app
From the repo root:

```bash
python ollama-agents/ollama-app.py
```

## Troubleshooting
- If the app cannot find the model, run `ollama ls` to list available models and confirm the name.
- If `ollama` is not found, ensure the binary is on your PATH and restart the terminal.

## Credits
See `CodeBuildBrowser.md` for a brief guide and usage tips.
