from crewai import Task
from agents.agent_backend_light import json_file_agent, txt_file_agent, file_manager_agent

# Delegate JSON task to JSON File List Agent
def delegate_json_task():
    return file_manager_agent.delegate_work_to_coworker(
        coworker="JSON File List Agent",  # Nome do agente
        task="List JSON files",  # Descrição da tarefa como string
        context="List all JSON files in the specified directory"  # Descrição do contexto como string
    )

# Delegate TXT task to TXT File List Agent
def delegate_txt_task():
    return file_manager_agent.delegate_work_to_coworker(
        coworker="TXT File List Agent",  # Nome do agente
        task="List TXT files",  # Descrição da tarefa como string
        context="List all TXT files in the specified directory"  # Descrição do contexto como string
    )

# Definindo as tarefas
list_json_files_task = Task(
    description="Delegate JSON file listing task to the JSON File List Agent.",
    agent=file_manager_agent,
    function=delegate_json_task,  # Chamada correta para a função delegate_json_task
    expected_output="A list of JSON files from the JSON directory."
)

list_txt_files_task = Task(
    description="Delegate TXT file listing task to the TXT File List Agent.",
    agent=file_manager_agent,
    function=delegate_txt_task,  # Chamada correta para a função delegate_txt_task
    expected_output="A list of TXT files from the TXT directory."
)
