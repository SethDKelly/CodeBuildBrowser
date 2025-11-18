# examples/simple_agent.py
from agents.base_agent import BaseAgent
from agents.tools.file_manager import FileManager, get_file_tool_schemas

def create_file_agent():
    """
    Create an AI agent with file management capabilities
    
    Returns:
        Configured BaseAgent instance
    """
    # Initialize components
    agent = BaseAgent(model_name="llama3.1")
    file_manager = FileManager()
    
    # Register file management tools
    schemas = get_file_tool_schemas()
    
    agent.register_tool(schemas[0], file_manager.read_file)
    agent.register_tool(schemas[1], file_manager.write_file)
    agent.register_tool(schemas[2], file_manager.list_files)
    
    return agent

def main():
    """
    Demonstrate the file agent in action
    """
    agent = create_file_agent()
    
    print("File Management Agent Ready!")
    print("Try commands like:")
    print("- 'Create a file called notes.txt with my daily tasks'")
    print("- 'Show me all files in the workspace'")
    print("- 'Read the contents of notes.txt'")
    print("Type 'quit' to exit\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'quit':
            break
            
        response = agent.chat(user_input)
        print(f"Agent: {response}\n")

if __name__ == "__main__":
    main()
