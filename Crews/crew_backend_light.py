import os
import time
from tqdm import tqdm  # Progress bar
from crewai import Crew
from tasks.task_file_processing_light import list_json_files_task  # Atualizado para a nova tarefa
from agents.agent_backend_light import file_list_agent

print(os.getcwd())

# Configuração do Crew com o agente de listagem de arquivos JSON
backend_crew = Crew(
    agents=[file_list_agent],
    tasks=[list_json_files_task],  # Atualizado para a nova tarefa de listagem JSON
    process="sequential",  # Execução sequencial de tarefas
    verbose=True  # Logs detalhados
)

# Função para executar o Crew com logging e barra de progresso
def execute_backend_crew():
    start_time = time.time()

    print("############################")
    print("# CrewAI JSON File Listing Execution")
    print("############################\n")

    # Logging dos modelos LLM usados pelos agentes
    print("LLM Models Used by Agents:")
    print(f"Agent: {file_list_agent.role}, Model: {file_list_agent.llm}\n")

    # Iniciar execução da tarefa
    print("Starting task execution...\n")
    
    try:
        # Caminho do diretório para processamento de arquivos JSON
        dir_path = "D:/OneDrive - InMotion - Consulting/AI Projects/AI-Clinical-Advisory-Crew/data_reports_json/"
        print(f"Checking directory '{dir_path}'...")

        if os.path.exists(dir_path):
            print(f"Directory '{dir_path}' found successfully.")
            print("Processing files in directory...\n")

            # Barra de progresso para a execução das tarefas
            tasks = backend_crew.tasks
            with tqdm(total=len(tasks), desc="Executing Crew tasks", unit="task") as pbar:
                result = backend_crew.kickoff()
                if result:
                    pbar.update(1)
                    print("Task execution completed successfully.")
                else:
                    print("No valid outputs found during Crew execution.")
        else:
            print(f"Error: Directory '{dir_path}' does not exist.")
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Calcular tempo total de execução
    end_time = time.time()
    total_duration = end_time - start_time
    print(f"\nTotal Execution Time: {total_duration:.2f} seconds")

    print("\n############################")
    print("# Task Execution Complete")
    print("############################\n")

if __name__ == "__main__":
    execute_backend_crew()
