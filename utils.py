# utils.py

import time


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
