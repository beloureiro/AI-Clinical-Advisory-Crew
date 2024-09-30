import os
from crewai import Task
from crewai_tools import DirectoryReadTool
from agents.agent_backend_light import file_list_agent

# Inicializar a ferramenta para leitura do diretório JSON
json_directory_tool = DirectoryReadTool(directory='D:/OneDrive - InMotion - Consulting/AI Projects/AI-Clinical-Advisory-Crew/data_reports_json/')

# Função para listar apenas arquivos do diretório JSON
def list_json_files():
    print("Starting JSON file listing task...")

    # Listar arquivos no diretório JSON
    print("Listing JSON files...")
    json_files = json_directory_tool.read_directory()
    json_files = [f for f in json_files if f.endswith('.json')]

    # Log dos arquivos JSON encontrados
    print(f"JSON files found: {len(json_files)}")
    for json_file in json_files:
        print(f"- {json_file}")

    return json_files

# Definir a tarefa para listar os arquivos JSON
list_json_files_task = Task(
    description="List files from the JSON directory.",
    agent=file_list_agent,
    function=list_json_files,
    expected_output="A list of JSON files from the directory."
)
