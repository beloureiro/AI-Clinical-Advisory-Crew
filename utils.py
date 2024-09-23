import time
from datetime import datetime
import os

def format_output_with_agent_and_model(agent, model, response):
    """Formata a saída com o nome do agente e o modelo LLM utilizado."""
    return f"# Agent: {agent.role}\n## Model: {model}\n## Final Answer:\n{response}"

def get_patient_feedback():
    """Lê o feedback do paciente de um arquivo de texto."""
    with open("patient_feedback.txt", "r", encoding='utf-8') as file:
        feedback = file.read().strip()
    return feedback

def log_model_usage(agent):
    """Registra e exibe o modelo LLM utilizado pelo agente."""
    model_name = getattr(agent, 'llm', "Unknown Model")
    print(f"Initialized Agent: '{agent.role}', using model: '{model_name}'")

def get_agent_model(agent):
    """Retorna o nome do modelo LLM utilizado por um agente."""
    return getattr(agent, 'llm', "Unknown Model")

def log_all_models(agents):
    """Loga os modelos utilizados por todos os agentes."""
    for agent in agents:
        if isinstance(agent, str):
            print(f"Agent: {agent}, Model: Unknown Model")
        elif hasattr(agent, 'role') and hasattr(agent, 'llm'):
            model_name = agent.llm if agent.llm else "Unknown Model"
            print(f"Agent: {agent.role}, Model: {model_name}")
        else:
            print("Unknown agent type or missing attributes.")

def format_task_descriptions(tasks, feedback):
    """Ajusta as descrições das tarefas para incluir o feedback."""
    for task in tasks:
        if '{feedback}' in task.description:
            task.description = task.description.format(feedback=feedback)

def execute_agents(tasks_output):
    """Executa cada agente e exibe as respostas."""
    for task_result in tasks_output:
        agent = task_result.agent
        agent_name = agent if isinstance(agent, str) else agent.role

        agent_start_time = time.time()

        print(f"############################")
        print(f"# Agent: {agent_name}")
        
        response = task_result.raw if hasattr(task_result, 'raw') else "No response available"
        print(f"## Final Answer:\n{response}\n")

        agent_end_time = time.time()
        agent_duration = agent_end_time - agent_start_time
        print(f"Agent {agent_name} took {agent_duration:.2f} seconds.\n")

def save_consolidated_report(patient_feedback, tasks_output, total_duration):
    """
    Gera um relatório consolidado e o salva em um arquivo de texto na pasta 'agents'
    com o nome baseado na data e hora. O nome do arquivo será usado como ID para uma base de dados.
    """
    # Gera o nome do arquivo com base na data e hora (incluindo segundos)
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"report_{current_time}.txt"

    # Define o diretório onde o arquivo será salvo
    directory = r"D:\OneDrive - InMotion - Consulting\AI Projects\AI-Clinical-Advisory-Crew\data_reports"

    # Cria o caminho completo do arquivo
    file_path = os.path.join(directory, file_name)

    # Converte o tempo total em minutos e segundos
    minutes = int(total_duration // 60)
    seconds = int(total_duration % 60)

    # Abre o arquivo para escrita
    with open(file_path, "w", encoding='utf-8') as report_file:
        report_file.write("############################\n")
        report_file.write("# AI Clinical Advisory Crew Report\n")
        report_file.write("############################\n\n")

        # Feedback do paciente
        report_file.write(f"Patient Feedback: {patient_feedback}\n\n")

        # Informações de cada agente e suas respostas
        for task_result in tasks_output:
            agent = task_result.agent
            agent_name = agent if isinstance(agent, str) else agent.role
            response = task_result.raw if hasattr(task_result, 'raw') else "No response available"
            report_file.write(f"############################\n")
            report_file.write(f"# Agent: {agent_name}\n")
            report_file.write(f"## Final Answer:\n{response}\n\n")
        
        # Adiciona o tempo total de execução ao final do relatório
        report_file.write(f"Total execution time: {minutes} minutes and {seconds} seconds.\n")

        # Adiciona a finalização do relatório
        report_file.write("############################\n")
        report_file.write("# Consolidated Final Report\n")
        report_file.write("############################\n")

    return file_name  # Retorna o nome do arquivo que pode ser usado como ID para a base de dados
