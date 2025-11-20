# ollama_app.py
from flask import Flask
from examples.advanced_agent import AdvancedAgent
from logging_config import configure_logging

import os
import logging

# Configure logging early (writes to responses.log by default)
configure_logging(log_file="responses.log")
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder="app/templates")
agent = AdvancedAgent()

# Register blueprint routes
from app.routes import bp as main_bp
app.register_blueprint(main_bp)
# Register centralized error handlers
from app.errors import register_error_handlers
register_error_handlers(app)

logger.info("Ollama app initialized")

if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    logger.info(f"Starting Flask development server on 0.0.0.0:8000 (debug={debug_mode})")
    app.run(host="0.0.0.0", port=8000, debug=debug_mode)
