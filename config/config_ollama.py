import os

# Set a dummy OpenAI API key (required for initialization, even if not used)
os.environ["OPENAI_API_KEY"] = "sk-proj-111"

# Configure the Ollama local models
#----------------------------------
llama_3_1_model = "ollama/llama3.1:8b"
llama_3_2_model = "ollama/llama3.2:latest"
llama3_8b_model = "ollama/llama3:8b"
hermes_model = "ollama/hermes3:8b"
gemma_model = "ollama/gemma2:9b"
gemma_big_model = "ollama/gemma2:27b-instruct-q2_K "
phi_model = "ollama/phi3.5:3.8b"
openhermes_model = "ollama/openhermes:latest"
mistral_mini_model = "ollama/mistral-nemo:latest"
mistral12b_model = "ollama/mistral-nemo:12b-instruct-2407-q3_K_M"
quwen_model = "ollama/qwen2:7b"
llava_model = "ollama/llava:7b"
zephyr_model = "ollama/zephyr:7b"
nomic_text_model = "ollama/nomic-embed-text:latest"
mxbai_text_model = "ollama/mxbai-embed-large:latest"
#----------------------------------
