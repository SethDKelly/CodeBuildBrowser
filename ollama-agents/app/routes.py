# All route functions moved from flask_server.py (now as a Blueprint)
from flask import Blueprint, request, jsonify, render_template
import json
import dataclasses
import logging
from agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
	return render_template("index.html")

@bp.route("/json")
def json_view():
	sample_data = {"message": "Hello, world!", "status": "success"}
	return render_template("json.html", data=sample_data)

# Error handlers are registered centrally in `app.errors.register_error_handlers`

@bp.route("/chat", methods=["POST"])
def chat_endpoint():
	"""
	Chat with the AI agent (Flask version)
	Expects JSON: {"message": "...", "session_id": "..."}
	"""
	data = request.get_json(force=True)
	try:
		message = data.get("message")
		session_id = data.get("session_id", "default")
	except Exception as e:
		return jsonify({"error": str(e)}), 400

	try:
		logger.info("/chat received", extra={"session_id": session_id})
		agent = BaseAgent()
		response = agent.chat(message)
		# Normalize response to a JSON-serializable string in the `response` field
		try:
			if dataclasses.is_dataclass(response):
				response_text = json.dumps(dataclasses.asdict(response))
			elif isinstance(response, dict):
				response_text = json.dumps(response)
			else:
				response_text = str(response)
		except Exception:
			response_text = str(response)

		resp = {"response": response_text, "session_id": session_id}
		return jsonify(resp), 200
	except Exception as e:
		logger.exception("Error in /chat handler")
		return jsonify({"error": str(e)}), 500

@bp.route("/capabilities", methods=["GET"])
def get_capabilities():
	"""
	Get agent capabilities
	"""
	try:
		agent = BaseAgent()
		return jsonify({
			"tools": [schema["function"]["name"] for schema in agent.tool_schemas],
			"capabilities": []  # No get_capabilities method in BaseAgent
		})
	except Exception as e:
		logger.exception("Error getting capabilities")
		return jsonify({"error": str(e)}), 500

@bp.route("/health", methods=["GET"])
def health_check():
	"""Health check endpoint
	Returns JSON for API requests, HTML for browsers.
	"""
	agent = BaseAgent()
	model = agent.model_name
	status = "healthy"
	# Content negotiation: JSON for API, HTML for browser
	if "application/json" in (request.headers.get("Accept") or ""):
		return jsonify({"model": model, "status": status})
	# Otherwise, render HTML using a template that extends base.html
	return render_template("health.html", model=model, status=status)
