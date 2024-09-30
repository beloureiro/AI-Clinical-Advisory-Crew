import sys
import os
from crewai import Agent
from config.config_ollama import gemma2_2b_instruct_q4_K_S
from crewai_tools import DirectoryReadTool

# Adicionar o diretório principal ao Python path para imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Inicializar a ferramenta de leitura para o diretório JSON
json_directory_tool = DirectoryReadTool(directory='D:/OneDrive - InMotion - Consulting/AI Projects/AI-Clinical-Advisory-Crew/data_reports_json/')

# Agente básico para listagem de arquivos JSON
file_list_agent = Agent(
    role="File List Agent",
    goal="List files in the JSON directory.",
    backstory="A lightweight agent designed to list files in the JSON directory.",
    llm=gemma2_2b_instruct_q4_K_S,  # Usando o LLM correto
    tools=[json_directory_tool],  # Ferramenta de leitura de diretório JSON
    verbose=True  # Logs detalhados
)
