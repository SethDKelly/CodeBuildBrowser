# agents/error_handler.py
import logging
import traceback
from functools import wraps
from typing import Callable, Any

class AgentError(Exception):
    """Base exception for agent-related errors"""
    
    pass

class ToolExecutionError(AgentError):
    """Exception raised when tool execution fails"""
    pass

class ModelError(AgentError):
    """Exception raised when model interaction fails"""
    pass

def setup_logging():
    """Configure logging for the agent"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('agent.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('ai_agent')

def error_handler(func: Callable) -> Callable:
    """
    Decorator for handling and logging function errors
    
    Args:
        func: Function to wrap with error handling
        
    Returns:
        Wrapped function with error handling
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        logger = logging.getLogger('ai_agent')
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return f"Error executing {func.__name__}: {str(e)}"
    return wrapper

# Enhanced BaseAgent with error handling
class RobustAgent(BaseAgent):
    def __init__(self, model_name: str = "llama3.1"):
        super().__init__(model_name)
        self.logger = setup_logging()
        
    @error_handler
    def chat(self, message: str) -> str:
        """Chat method with enhanced error handling"""
        self.logger.info(f"Processing message: {message[:50]}...")
        return super().chat(message)
        
    def validate_tool_schema(self, schema: dict) -> bool:
        """
        Validate tool schema before registration
        
        Args:
            schema: Tool schema to validate
            
        Returns:
            True if schema is valid, False otherwise
        """
        required_fields = ["type", "function"]
        function_fields = ["name", "description", "parameters"]
        
        if not all(field in schema for field in required_fields):
            self.logger.error("Tool schema missing required fields")
            return False
            
        if not all(field in schema["function"] for field in function_fields):
            self.logger.error("Function schema missing required fields")
            return False
            
        return True
