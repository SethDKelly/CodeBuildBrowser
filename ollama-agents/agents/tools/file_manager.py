# agents/tools/file_manager.py
import os
import json
from pathlib import Path
from typing import List, Dict

class FileManager:
    def __init__(self, base_path: str = "./workspace"):
        """
        Initialize file manager with a base working directory
        
        Args:
            base_path: Base directory for file operations
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        
    def read_file(self, filename: str) -> str:
        """
        Read contents of a file
        
        Args:
            filename: Name of file to read
            
        Returns:
            File contents as string
        """
        try:
            file_path = (self.base_path / filename).resolve()

            # Security checks
            if not str(file_path).startswith(str(self.base_path)):
                # MOVE TO LOGGING
                return f"Error: Access denied - Cannot access files outside working directory"
            
            if not file_path.exists():
                return f"Error: File does not exist: {filename}"
            
            if not file_path.is_file():
                return f"Error: Path is not a file: {filename}"
            
            try:
                file_path = self.base_path / filename
                return file_path.read_text(encoding='utf-8')
            
            except UnicodeDecodeError:
                # Try to read as binary and show info
                size = file_path.stat().st_size
                return f"File {file_path} appears to be binary (size: {size} bytes). Cannot display as text."
            
        except Exception as e:
            return f"Error reading {filename}: {str(e)}"
            
    def write_file(self, filename: str, content: str) -> str:
        """
        Write content to a file
        
        Args:
            filename: Name of file to write
            content: Content to write to file
            
        Returns:
            Success message or error
        """
        try:
            file_path = self.base_path / filename
            file_path.write_text(content, encoding='utf-8')
            return f"Successfully wrote to {filename}"
        except Exception as e:
            return f"Error writing file: {str(e)}"
            
    def list_files(self, directory: str = "") -> str:
        """
        List all files in the workspace
        
        Returns:
            JSON string of file information
        """
        if directory:
            full_path = directory
        else:
            full_path = self.base_path

        try:
            full_path.resolve()

        except Exception as e:
            return f"Error: {str(e)}"
        try:
            files = []
            for file_path in self.base_path.iterdir():
                if file_path.is_file():
                    files.append({
                        "name": file_path.name,
                        "size": file_path.stat().st_size,
                        "modified": file_path.stat().st_mtime
                    })
            return json.dumps(files, indent=2)
        except Exception as e:
            return f"Error listing files: {str(e)}"

# Tool schemas for Ollama
def get_file_tool_schemas():
    """
    Get tool schemas for file management functions
    
    Returns:
        List of tool schemas compatible with Ollama
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "Read the contents of a file from the workspace",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "description": "Name of the file to read"
                        }
                    },
                    "required": ["filename"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "write_file",
                "description": "Write content to a file in the workspace",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "description": "Name of the file to write"
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write to the file"
                        }
                    },
                    "required": ["filename", "content"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_files",
                "description": "List all files in the workspace directory",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
    ]
