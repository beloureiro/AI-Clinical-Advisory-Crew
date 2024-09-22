import os

# Set a dummy OpenAI API key (required for initialization, even if not used)
os.environ["OPENAI_API_KEY"] = "sk-proj-111"

# Configure the Ollama local models
#----------------------------------
llama_model = "ollama/llama3.1:8b"
hermes_model = "ollama/hermes3:8b"
phi_model = "ollama/phi3.5:3.8b"
gemma_model = "ollama/gemma2:9b"
openhermes_model = "ollama/openhermes:latest"
#----------------------------------
