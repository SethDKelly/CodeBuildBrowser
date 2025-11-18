# api/server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from examples.advanced_agent import AdvancedAgent
import uvicorn

app = FastAPI(title="AI Agent API", version="1.0.0")

# Global agent instance
agent = AdvancedAgent()

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    session_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Chat with the AI agent
    
    Args:
        request: Chat request containing message and session ID
        
    Returns:
        Agent response
    """
    try:
        response = agent.chat(request.message)
        return ChatResponse(
            response=response,
            session_id=request.session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/capabilities")
async def get_capabilities():
    """
    Get agent capabilities
    
    Returns:
        List of available tools and their descriptions
    """
    return {
        "tools": [schema["function"]["name"] for schema in agent.tool_schemas],
        "capabilities": agent.get_capabilities()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model": agent.model_name}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
