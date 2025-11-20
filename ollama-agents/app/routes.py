# All route functions moved from flask_server.py
from flask import request, jsonify, render_template
import json
import dataclasses
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ollama_app import app, agent


@app.route("/")
def index():
	return render_template("index.html")

@app.route("/json")
def json_view():
	sample_data = {"message": "Hello, world!", "status": "success"}
	return render_template("json.html", data=sample_data)

@app.errorhandler(404)
def error_404(e):
	return render_template("error404.html"), 404

@app.errorhandler(410)
def error_410(e):
	return render_template("error410.html"), 410

@app.route("/chat", methods=["POST"])
def chat_endpoint():
	"""
	Chat with the AI agent (Flask version)
	Expects JSON: {"message": "...", "session_id": "..."}
	"""
	data = request.get_json(force=True)
	try:
		# ChatRequest logic in route for simplicity
		message = data.get("message")
		session_id = data.get("session_id", "default")
	except Exception as e:
		return jsonify({"error": str(e)}), 400

	try:
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
		return jsonify({"error": str(e)}), 500

@app.route("/capabilities", methods=["GET"])
def get_capabilities():
	"""
	Get agent capabilities
	"""
	try:
		return jsonify({
			"tools": [schema["function"]["name"] for schema in agent.tool_schemas],
			"capabilities": agent.get_capabilities()
		})
	except Exception as e:
		return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health_check():
	"""Health check endpoint"""
	return jsonify({"status": "healthy", "model": agent.model_name})
