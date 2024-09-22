from config.crew_config import ai_clinical_crew
from utils import log_model_usage, process_result, get_patient_feedback  # Importando as funções transferidas

def execute_crew():
    # Obtém o feedback inicial do paciente
    patient_feedback = get_patient_feedback()
    print(f"Patient Feedback: {patient_feedback}")  # Log para verificação

    # Ajusta as descrições das tarefas para incluir o feedback
    for task in ai_clinical_crew.tasks:
        if '{feedback}' in task.description:
            task.description = task.description.format(feedback=patient_feedback)

    # Executa o crew com o feedback do paciente como input
    result = ai_clinical_crew.kickoff(inputs={"feedback": patient_feedback})

    # Processa e imprime o resultado da execução
    process_result(result)

if __name__ == "__main__":
    execute_crew()
