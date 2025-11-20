# api/flask_server.py
from flask import Flask, request, jsonify
from pydantic import BaseModel
from examples.advanced_agent import AdvancedAgent

app = Flask(__name__)

# Global agent instance (same as FastAPI server)
agent = AdvancedAgent()

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    session_id: str

@app.route("/chat", methods=["POST"])
def chat_endpoint():
    """
    Chat with the AI agent (Flask version)
    Expects JSON: {"message": "...", "session_id": "..."}
    """
    data = request.get_json(force=True)
    try:
        req = ChatRequest(**data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    try:
        response = agent.chat(req.message)
        resp = ChatResponse(response=response, session_id=req.session_id)
        return jsonify(resp.dict()), 200
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

if __name__ == "__main__":
    # Run Flask dev server. For production use a WSGI server.
    app.run(host="0.0.0.0", port=8000)
