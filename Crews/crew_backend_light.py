import os
import time
from tqdm import tqdm
from crewai import Crew
from agents.agent_backend_light import json_file_agent, txt_file_agent, file_manager_agent
from tasks.task_file_processing_light import list_json_files_task, list_txt_files_task

# Configuração do Crew com os agentes e suas respectivas tarefas
backend_crew = Crew(
    agents=[json_file_agent, txt_file_agent],  # JSON and TXT agents for file listing
    tasks=[list_json_files_task, list_txt_files_task],  # Tasks delegated to agents
    manager_agent=file_manager_agent,  # The file manager agent manages delegation
    process="hierarchical",  # Use hierarchical execution
    verbose=True  # Correção: verbose como booleano
)

# Função para executar o Crew com logging e barra de progresso
def execute_backend_crew():
    start_time = time.time()

    print("############################")
    print("# CrewAI File Listing Execution with Hierarchy")
    print("############################\n")

    # Exibir os modelos LLM usados pelos agentes
    print("LLM Models Used by Agents:")
    print(f"Agent: {json_file_agent.role}, Model: {json_file_agent.llm}")
    print(f"Agent: {txt_file_agent.role}, Model: {txt_file_agent.llm}")
    print(f"Agent: {file_manager_agent.role}, Model: {file_manager_agent.llm}\n")

    # Iniciar execução das tarefas
    print("Starting task execution...\n")
    
    try:
        tasks = backend_crew.tasks
        with tqdm(total=len(tasks), desc="Executing Crew tasks", unit="task") as pbar:
            result = backend_crew.kickoff()
            if result:
                pbar.update(1)
                print("Task execution completed successfully.")
            else:
                print("No valid outputs found during Crew execution.")
    
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
