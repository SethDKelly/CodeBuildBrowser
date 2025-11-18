# config/settings.py
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class AgentConfig:
    """Configuration settings for AI agents"""
    
    # Model settings
    model_name: str = "llama3.1"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    
    # Tool settings
    tool_timeout: int = 30
    max_tool_calls: int = 10
    
    # Performance settings
    enable_caching: bool = True
    cache_size: int = 1000
    parallel_tools: bool = False
    
    # Logging settings
    log_level: str = "INFO"
    log_file: str = "agent.log"
    
    @classmethod
    def from_env(cls) -> 'AgentConfig':
        """Load configuration from environment variables"""
        return cls(
            model_name=os.getenv('AGENT_MODEL', 'llama3.1'),
            temperature=float(os.getenv('AGENT_TEMPERATURE', '0.7')),
            tool_timeout=int(os.getenv('TOOL_TIMEOUT', '30')),
            max_tool_calls=int(os.getenv('MAX_TOOL_CALLS', '10')),
            enable_caching=os.getenv('ENABLE_CACHING', 'true').lower() == 'true',
            log_level=os.getenv('LOG_LEVEL', 'INFO')
        )

# Optimized agent with caching
from functools import lru_cache
import hashlib

class OptimizedAgent(RobustAgent):
    def __init__(self, config: AgentConfig):
        super().__init__(config.model_name)
        self.config = config
        
        if config.enable_caching:
            self._setup_caching()
            
    def _setup_caching(self):
        """Setup response caching for repeated queries"""
        self._cached_chat = lru_cache(maxsize=self.config.cache_size)(self._chat_impl)
        
    def _hash_message(self, message: str) -> str:
        """Create hash for message caching"""
        return hashlib.md5(message.encode()).hexdigest()
        
    def chat(self, message: str) -> str:
        """Chat with caching support"""
        if self.config.enable_caching:
            return self._cached_chat(self._hash_message(message), message)
        else:
            return self._chat_impl(message)
            
    def _chat_impl(self, message: str) -> str:
        """Internal chat implementation"""
        return super().chat(message)
