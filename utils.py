# Helper function to monitor and enforce token limits and output structure
def truncate_output(response, max_tokens=50):
    tokens = response.split()
    print(f"Number of tokens before truncation: {len(tokens)}")  # Log para validação
    if len(tokens) > max_tokens:
        # Find the last period before max_tokens
        truncated_response = ' '.join(tokens[:max_tokens])
        last_period = truncated_response.rfind('.')
        if last_period != -1:
            return truncated_response[:last_period+1]  # Trunca até o ponto final
        else:
            return truncated_response + '...'
    return response

def check_for_off_topic(response, feedback):
    feedback_words = set(feedback.lower().split())
    response_words = set(response.lower().split())
    off_topic_words = response_words - feedback_words
    print(f"Off-topic words detected: {off_topic_words}")  # Log para validação
    if off_topic_words:
        print("Off-topic detected in response.")
        return "Content is off-topic based on the input provided."
    return response

def format_output_with_agent_and_model(agent, model, response):
    return f"# Agent: {agent.role}\n## Model: {model}\n## Final Answer:\n{response}"

def post_process_response(response, max_tokens, inputs, agent):
    feedback = inputs.get('feedback', '')
    print(f"Raw response before truncation: {response}")  # Log para validação
    
    # Trunca a resposta
    response = truncate_output(response, max_tokens)
    print(f"Response after truncation: {response}")  # Log para validação
    
    # Verifica conteúdo fora do tópico
    response = check_for_off_topic(response, feedback)
    print(f"Response after off-topic check: {response}")  # Log para validação
    
    # Formata a saída com agente e modelo
    formatted_response = format_output_with_agent_and_model(agent, agent.llm, response)
    print(f"Final formatted response: {formatted_response}")  # Log para validação
    return formatted_response

# Função para consolidar todas as saídas dos agentes em um relatório conciso
def consolidate_agent_output(task_results, agent_role):
    consolidated_output = f"### Consolidated Feedback Report for {agent_role}\n\n"
    key_issues = []
    emotional_intensity = None
    sentiment = None
    urgency = None
    journey_map = ""
    recommendations = ""

    for task_result in task_results:
        task_output = task_result.get('raw', '')
        
        if "Patient Experience Expert" in agent_role:
            if "Key Issues Identified" in task_output:
                key_issues.append(task_output.replace("### Key Issues Identified", "").strip())
            elif "Emotional Intensity" in task_output:
                emotional_intensity = task_output.split(":")[1].strip()
            elif "Sentiment" in task_output:
                sentiment = task_output.split(":")[1].strip()
            elif "Negative Feedback Urgency" in task_output:
                urgency = task_output.split(":")[1].strip()
        elif "Health & IT Process Expert" in agent_role:
            if "Patient Journey Map" in task_output:
                journey_map = task_output.replace("### Patient Journey Map", "").strip()
            elif "Process Improvement Suggestion" in task_output:
                recommendations = task_output.replace("### Process Improvement Suggestion", "").strip()
        elif "Clinical Psychologist" in agent_role:
            if "Emotional State Analysis" in task_output:
                emotional_intensity = task_output.split(":")[1].strip()
            elif "Support Strategy" in task_output:
                recommendations = task_output.replace("### Support Strategy", "").strip()
        elif "Communication Expert" in agent_role:
            if "Communication Recommendation" in task_output:
                recommendations = task_output.replace("### Communication Recommendation", "").strip()
        elif "Manager and Advisor" in agent_role:
            if "Final Report" in task_output:
                consolidated_output += task_output

    if key_issues:
        consolidated_output += "**Key Issues**: " + "; ".join(key_issues) + ".\n"
    if emotional_intensity and sentiment:
        consolidated_output += f"**Emotional Intensity**: {emotional_intensity}, **Sentiment**: {sentiment}.\n"
    if urgency:
        consolidated_output += f"**Urgency Level**: {urgency}.\n"
    if journey_map:
        consolidated_output += f"**Patient Journey Map**:\n{journey_map}\n"
    if recommendations:
        consolidated_output += f"**Recommendations for Improvement**:\n{recommendations}\n"

    return consolidated_output

def get_patient_feedback():
    # Lê o feedback do paciente de um arquivo de texto
    with open("patient_feedback.txt", "r", encoding='utf-8') as file:
        feedback = file.read().strip()
    return feedback

def log_model_usage(agent):
    # Verifica e exibe o modelo utilizado pelo agente
    model_name = agent.llm if agent.llm else "Unknown Model"
    print(f"Initialized Agent: '{agent.role}', using model: '{model_name}'")

def process_result(result):
    # Verifica se existem tarefas disponíveis no output
    if hasattr(result, 'tasks_output') and result.tasks_output:
        total_tokens = 0
        printed_report = False  # Flag para garantir que o relatório final seja impresso apenas uma vez

        for task_result in result.tasks_output:
            # Captura o papel do agente e o modelo, se disponível
            agent_role = getattr(task_result, 'agent', 'Unknown Agent')
            task_name = getattr(task_result, 'name', 'Unknown Task')
            agent_model = getattr(task_result, 'model', 'Unknown Model')

            # Use vars() para inspecionar task_result
            print(f"task_result contents: {vars(task_result)}")

            # Pula a impressão do relatório final se já foi impresso
            if task_name == 'Manager and Advisor' and printed_report:
                continue

            # Imprime a saída normalmente para outras tarefas
            if hasattr(task_result, 'raw') and not printed_report:
                print(f"\n# Agent: {agent_role}\n## Model: {agent_model}\n## Final Answer:\n{task_result.raw}")
                # Marca que o relatório final foi impresso
                if task_name == 'Manager and Advisor':
                    printed_report = True

            # Verifica e exibe o uso de tokens
            metrics = getattr(task_result, 'metrics', {})
            token_usage = metrics.get('token_usage', None)

            if token_usage:
                print(f"Task '{task_name}' used {token_usage} tokens")
                total_tokens += token_usage
            else:
                print(f"Warning: Token usage not available for task '{task_name}'")

        # Exibe o uso total de tokens
        print(f"Total tokens used by the crew: {total_tokens}")
    else:
        print("No tasks output found in the result. Please check the result structure.")
