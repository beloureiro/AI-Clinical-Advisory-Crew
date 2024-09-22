import time  # Adiciona o módulo time para o timer
from config.crew_config import ai_clinical_crew
from utils import log_model_usage, get_patient_feedback, log_all_models

def execute_crew():
    # Marca o tempo de início da execução total
    start_time = time.time()

    # Obtém o feedback inicial do paciente
    patient_feedback = get_patient_feedback()

    # Título e exibição inicial do relatório
    print("############################")
    print("# AI Clinical Advisory Crew Report")
    print("############################\n")

    # Exibe o feedback do paciente no início do relatório
    print(f"Patient Feedback for Analysis:\n{patient_feedback}\n")

    # Ajusta as descrições das tarefas para incluir o feedback
    for task in ai_clinical_crew.tasks:
        if '{feedback}' in task.description:
            task.description = task.description.format(feedback=patient_feedback)

    # Exibe os modelos usados por cada agente uma vez (opcional, se for mantido)
    print("LLM Models Used by Agents:\n")
    agents = [task.agent for task in ai_clinical_crew.tasks]  # Obtém todos os agentes do crew
    log_all_models(agents)

    # Executa o crew com o feedback do paciente como input e mede o tempo de cada agente
    result = ai_clinical_crew.kickoff(inputs={"feedback": patient_feedback})  # Executa a tarefa de todos os agentes

    for task_result in result.tasks_output:
        agent = task_result.agent

        # Se `agent` for uma string (nome), tratamos como tal
        agent_name = agent if isinstance(agent, str) else agent.role

        agent_start_time = time.time()  # Marca o tempo de início do agente

        # Exibe o agente e a resposta final
        print(f"############################")
        print(f"# Agent: {agent_name}")
        
        # Exibe o conteúdo da resposta do agente
        response = task_result.raw if hasattr(task_result, 'raw') else "No response available"
        print(f"## Final Answer:\n{response}\n")

        agent_end_time = time.time()  # Marca o tempo de término do agente
        agent_duration = agent_end_time - agent_start_time  # Calcula a duração do agente
        print(f"Agent {agent_name} took {agent_duration:.2f} seconds.\n")  # Exibe o tempo do agente

    # Marca o tempo de término total
    end_time = time.time()
    total_duration = end_time - start_time  # Calcula o tempo total de execução

    # Converte o tempo total em minutos e segundos
    minutes = int(total_duration // 60)
    seconds = int(total_duration % 60)

    # Relatório final consolidado
    print("############################")
    print("# Consolidated Final Report")
    print("############################\n")

    # Exibe novamente o feedback do paciente no relatório final
    print(f"Patient Feedback: {patient_feedback}\n")

    # Exibe o tempo total de execução em minutos e segundos
    print(f"Total execution time: {minutes} minutes and {seconds} seconds.")

if __name__ == "__main__":
    execute_crew()
