# agents/base_agent.py
import json
import ollama
import logging
from typing import Dict, List, Callable, Any
from dataclasses import dataclass, field, asdict

logger = logging.getLogger(__name__)

@dataclass
class ResponseMessage:
    role: str
    content: str

class BaseAgent:
    def __init__(self, model_name: str = "qwen3:30b"):
        """
        Initialize the base agent with a specified model
        
        Args:
            model_name: Ollama model to use for responses
        """
        self.model_name = model_name
        self.tools = {}
        self.tool_schemas = []
        
    def register_tool(self, schema: Dict, function: Callable):
        """
        Register a function as an available tool
        
        Args:
            schema: OpenAI-compatible function schema
            function: Python function to execute when tool is called
        """
        tool_name = schema["function"]["name"]
        self.tools[tool_name] = function
        self.tool_schemas.append(schema)
        
    def chat(self, message: str) -> str:
        """
        Send a message to the agent and get a response
        
        Args:
            message: User input message
            
        Returns:
            Agent's response after processing tools if needed
        """
        system_message = ResponseMessage("system", "You are a helpful assistant.")
        user_message = ResponseMessage("user", f"Answer this question: {message}")

        try:
            # Initial response from model
            response = ollama.chat(
                model=self.model_name,
                messages=[system_message.__dict__, 
                          user_message.__dict__],
                #tools=self.tool_schemas
            )
            
            # Check if model wants to call tools
            #if response.get("message", {}).get("tool_calls"):
            #    return self._handle_tool_calls(message, response)
            #else:
            #    return response["message"]["content"]
                
        except Exception as e:
            logger.exception("Error processing request in BaseAgent.chat")
            return f"Error processing request: {str(e)}"
            
    def _handle_tool_calls(self, original_message: str, response: Dict) -> str:
        """
        Execute tool calls and return final response
        
        Args:
            original_message: Original user message
            response: Model response containing tool calls
            
        Returns:
            Final response after executing tools
        """
        messages = [
            {"role": "user", "content": original_message},
            response["message"]
        ]
        
        # Execute each tool call
        for tool_call in response["message"]["tool_calls"]:
            function_name = tool_call["function"]["name"]
            function_args = json.loads(tool_call["function"]["arguments"])
            
            if function_name in self.tools:
                # Execute the function
                try:
                    result = self.tools[function_name](**function_args)
                except Exception:
                    logger.exception("Tool %s failed", function_name)
                    result = f"Error executing tool {function_name}"
                
                # Add tool result to conversation
                messages.append({
                    "role": "tool",
                    "content": str(result),
                    "tool_call_id": tool_call.get("id", "")
                })
        
        # Get final response from model
        final_response = ollama.chat(
            model=self.model_name,
            messages=messages
        )
        
        return final_response["message"]["content"]
