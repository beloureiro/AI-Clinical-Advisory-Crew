import os
from langchain_community.llms import Ollama  # Use the Ollama class


# Set a dummy OpenAI API key (required for initialization, even if not used)
os.environ["OPENAI_API_KEY"] = "sk-proj-111"

# Configure the Ollama local model (Llama 3.1: 8b model)
ollama_model = "ollama/llama3.1:8b"  # Certifique-se de que isso seja uma string


