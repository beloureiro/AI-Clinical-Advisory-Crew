# utils.py

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
    # Verifica se o agente possui um atributo `llm`, caso contrário retorna "Unknown Model"
    model_name = getattr(agent, 'llm', "Unknown Model")
    
    # Loga a informação do agente e seu modelo
    print(f"Initialized Agent: '{agent.role}', using model: '{model_name}'")

def get_agent_model(agent):
    """Retorna o nome do modelo LLM utilizado por um agente."""
    # Retorna o nome do modelo ou "Unknown Model" caso não esteja configurado
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
