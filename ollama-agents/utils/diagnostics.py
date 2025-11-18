# utils/diagnostics.py
import ollama
import psutil
import os

def check_system_requirements():
    """Check if system meets minimum requirements"""
    print("System Requirements Check:")
    print(f"  RAM: {psutil.virtual_memory().total / (1024**3):.1f}GB")
    print(f"  Available RAM: {psutil.virtual_memory().available / (1024**3):.1f}GB")
    print(f"  CPU Cores: {psutil.cpu_count()}")
    print(f"  Disk Space: {psutil.disk_usage('/').free / (1024**3):.1f}GB")

def check_ollama_installation():
    """Verify Ollama installation and model availability"""
    try:
        # Check if Ollama is running
        models = ollama.list()
        print(f"\nOllama Status: Running")
        print(f"Available Models:")
        for model in models.get('models', []):
            print(f"  - {model['name']}")
            
        return True
    except Exception as e:
        print(f"\nOllama Status: Error - {str(e)}")
        return False

def test_model_response(model_name: str = "llama3.1"):
    """Test basic model functionality"""
    try:
        response = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": "Hello"}]
        )
        print(f"\nModel Test ({model_name}): ✓ Working")
        return True
    except Exception as e:
        print(f"\nModel Test ({model_name}): ✗ Failed - {str(e)}")
        return False

def full_diagnostic():
    """Run complete system diagnostic"""
    print("=== AI Agent Diagnostic ===")
    
    check_system_requirements()
    ollama_ok = check_ollama_installation()
    
    if ollama_ok:
        test_model_response()
    else:
        print("\nRecommendations:")
        print("1. Install Ollama: curl -fsSL https://ollama.ai/install.sh | sh")
        print("2. Start Ollama service: ollama serve")
        print("3. Pull a model: ollama pull llama3.1")

if __name__ == "__main__":
    full_diagnostic()
