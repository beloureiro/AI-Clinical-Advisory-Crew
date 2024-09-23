import time
from config.crew_config import ai_clinical_crew
from utils import log_model_usage, get_patient_feedback, log_all_models, format_task_descriptions, execute_agents, save_consolidated_report

def execute_crew():
    start_time = time.time()  # Início da execução

    patient_feedback = get_patient_feedback()

    print("############################")
    print("# AI Clinical Advisory Crew Report")
    print("############################\n")
    print(f"Patient Feedback for Analysis:\n{patient_feedback}\n")

    format_task_descriptions(ai_clinical_crew.tasks, patient_feedback)  # Ajusta descrições das tarefas
    print("LLM Models Used by Agents:\n")
    agents = [task.agent for task in ai_clinical_crew.tasks]
    log_all_models(agents)

    result = ai_clinical_crew.kickoff(inputs={"feedback": patient_feedback})  # Executa as tarefas

    execute_agents(result.tasks_output)  # Executa cada agente

    end_time = time.time()  # Fim da execução
    total_duration = end_time - start_time

    print("############################")
    print("# Consolidated Final Report")
    print("############################\n")
    print(f"Patient Feedback: {patient_feedback}\n")

    # Salva o relatório consolidado na pasta 'agents' e obtém o nome do arquivo (ID)
    report_file_name = save_consolidated_report(patient_feedback, result.tasks_output, total_duration)
    print(f"Report saved as: {report_file_name}")  # Exibe o nome do arquivo gerado

if __name__ == "__main__":
    execute_crew()
