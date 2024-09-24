import os
import json
from datetime import datetime
import time

def save_agent_results_as_json(patient_feedback, tasks_output, total_duration):
    """
    Gera um relatório consolidado em formato JSON e o salva na pasta especificada.
    """
    # Gera o nome do arquivo com base na data e hora (incluindo segundos)
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"report_{current_time}.json"

    # Define o diretório onde o arquivo será salvo
    directory = r"D:\OneDrive - InMotion - Consulting\AI Projects\AI-Clinical-Advisory-Crew\data_reports_json"
    
    # Cria o diretório se não existir
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, file_name)

    # Converte o tempo total em minutos e segundos
    minutes = int(total_duration // 60)
    seconds = int(total_duration % 60)
    
    # Estrutura base do JSON com todos os campos inicializados
    report_data = {
        "patient_feedback": patient_feedback,
        "total_execution_time": f"{minutes} minutes and {seconds} seconds",
        "agents": []
    }
    
    # Definição completa das chaves para cada agente
    agent_fields = {
        "Patient Experience Expert": [
            "Sentiment_Patient_Experience_Expert",
            "Emotional_Intensity_Patient_Experience_Expert",
            "Urgency_Level_Patient_Experience_Expert",
            "Key_Issues_Patient_Experience_Expert"
        ],
        "Health & IT Process Expert with expertise in Business Process Model and Notation (BPMN)": [
            "Patient_Journey_Health_IT_Process_Expert",
            "Inefficiencies_Healthcare_Process_Health_IT_Process_Expert",
            "Improvement_Suggestions_Healthcare_Process_Health_IT_Process_Expert"
        ],
        "Clinical Psychologist": [
            "Emotional_State_Clinical_Psychologist",
            "Support_Strategy_Clinical_Psychologist",
            "Suggested_Approach_Clinical_Psychologist"
        ],
        "Communication Expert": [
            "Communication_Quality_Communication_Expert",
            "Issues_Identified_Communication_Expert",
            "Suggested_Improvements_Communication_Expert",
            "Final_Recommendation_Communication_Expert"
        ],
        "Manager and Advisor": [
            "Key_Issues_Manager_and_Advisor",
            "Recommendations_Manager_and_Advisor"
        ]
    }

    # Função auxiliar para remover ";" extras no final de listas
    def clean_up_field(field):
        if isinstance(field, str):
            return field.rstrip('; ').strip()
        return field

    # Função para correspondência flexível de chaves
    def match_key(agent_name, key_in_response):
        expected_keys = agent_fields.get(agent_name, [])
        key_in_response_clean = key_in_response.strip().replace(' ', '_').replace('-', '_').replace(':', '').lower()
        for expected_key in expected_keys:
            expected_key_clean = expected_key.strip().replace(' ', '_').replace('-', '_').replace(':', '').lower()
            if key_in_response_clean == expected_key_clean:
                return expected_key
        # Tentar correspondência parcial
        for expected_key in expected_keys:
            expected_key_clean = expected_key.strip().replace(' ', '_').replace('-', '_').replace(':', '').lower()
            if key_in_response_clean in expected_key_clean or expected_key_clean in key_in_response_clean:
                return expected_key
        return None

    # Processar cada tarefa do agente
    for task_result in tasks_output:
        agent = task_result.agent
        agent_name = agent if isinstance(agent, str) else agent.role

        # Extrair resposta do agente
        response = task_result.raw if hasattr(task_result, 'raw') else None

        # Inicializa a resposta do agente
        agent_data = {
            "agent_name": agent_name,
            "response": {}
        }

        if response is None or not isinstance(response, str):
            response = "No response available"
        else:
            lines = response.split('\n')
            current_field = None
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if ':' in line:
                    # Para linhas que contêm um campo com valor
                    key, value = map(str.strip, line.split(':', 1))
                    matched_key = match_key(agent_name, key)
                    if matched_key:
                        agent_data["response"][matched_key] = value
                        current_field = matched_key  # Armazena o campo atual
                    else:
                        current_field = None
                elif line.startswith('-') and current_field:
                    # Adiciona itens de lista aos campos correspondentes
                    item = line.strip('- ').strip()
                    if agent_data["response"][current_field]:
                        agent_data["response"][current_field] += f"; {item}"
                    else:
                        agent_data["response"][current_field] = item
                else:
                    # Lógica adicional para Manager and Advisor
                    if agent_name == "Manager and Advisor":
                        if line.startswith("The key issues identified are"):
                            current_field = "Key_Issues_Manager_and_Advisor"
                            value = line[len("The key issues identified are"):].strip()
                            agent_data["response"][current_field] = value
                        elif line.startswith("Recommendations include"):
                            current_field = "Recommendations_Manager_and_Advisor"
                            value = line[len("Recommendations include"):].strip()
                            agent_data["response"][current_field] = value
                        elif current_field:
                            # Continua adicionando ao campo atual
                            if agent_data["response"][current_field]:
                                agent_data["response"][current_field] += f" {line.strip()}"
                            else:
                                agent_data["response"][current_field] = line.strip()
                        else:
                            continue
                    elif current_field:
                        # Lógica existente para anexar ao campo atual
                        if agent_data["response"][current_field]:
                            agent_data["response"][current_field] += f" {line.strip()}"
                        else:
                            agent_data["response"][current_field] = line.strip()
                    else:
                        continue

        # Limpa campos que terminaram com ";" extra
        for field in agent_fields.get(agent_name, []):
            agent_data["response"][field] = clean_up_field(agent_data["response"].get(field, ""))

        report_data["agents"].append(agent_data)

    # Salva o arquivo JSON
    with open(file_path, "w", encoding='utf-8') as json_file:
        json.dump(report_data, json_file, ensure_ascii=False, indent=4)

    print(f"Report saved as JSON: {file_name}")
    return file_name








# Funções auxiliares adicionais
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
