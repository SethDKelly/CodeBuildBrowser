# ollama_app.py
from flask import Flask
from examples.advanced_agent import AdvancedAgent

app = Flask(__name__)
agent = AdvancedAgent()

# Import routes after app and agent are created
from app.routes import *

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
