# examples/advanced_agent.py
from agents.base_agent import BaseAgent
from agents.tools.file_manager import FileManager, get_file_tool_schemas
from agents.tools.web_scraper import WebScraper, get_web_tool_schemas

class AdvancedAgent(BaseAgent):
    def __init__(self, model_name: str = "llama3.1"):
        """
        Initialize advanced agent with multiple tool capabilities
        
        Args:
            model_name: Ollama model to use
        """
        super().__init__(model_name)
        
        # Initialize tool instances
        self.file_manager = FileManager()
        self.web_scraper = WebScraper()
        
        # Register all tools
        self._register_all_tools()
        
    def _register_all_tools(self):
        """Register all available tools with the agent"""
        
        # File management tools
        file_schemas = get_file_tool_schemas()
        self.register_tool(file_schemas[0], self.file_manager.read_file)
        self.register_tool(file_schemas[1], self.file_manager.write_file)
        self.register_tool(file_schemas[2], self.file_manager.list_files)
        
        # Web scraping tools
        web_schemas = get_web_tool_schemas()
        self.register_tool(web_schemas[0], self.web_scraper.extract_text)
        self.register_tool(web_schemas[1], self.web_scraper.extract_links)
        
    def get_capabilities(self) -> str:
        """
        Return a description of agent capabilities
        
        Returns:
            Formatted string describing available tools
        """
        capabilities = [
            "File Management:",
            "  - Read files from workspace",
            "  - Write content to files",
            "  - List all workspace files",
            "",
            "Web Scraping:",
            "  - Extract text from webpages",
            "  - Extract links from webpages",
            "  - Support for CSS selectors"
        ]
        return '\n'.join(capabilities)

def main():
    """
    Demonstrate the advanced agent capabilities
    """
    agent = AdvancedAgent()
    
    print("Advanced AI Agent Ready!")
    print("\nCapabilities:")
    print(agent.get_capabilities())
    print("\nExample commands:")
    print("- 'Scrape the latest news from example.com and save it to news.txt'")
    print("- 'Extract all links from https://python.org and show me the first 5'")
    print("- 'Read my todo.txt file and help me prioritize tasks'")
    print("Type 'quit' to exit\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'quit':
            break
            
        response = agent.chat(user_input)
        print(f"Agent: {response}\n")

if __name__ == "__main__":
    main()
