import os
import json
import pandas as pd
import logging

# Configurar o logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

def process_json_report(file_path):
    """
    Processa um arquivo JSON contendo o feedback do paciente e as respostas dos agentes,
    retornando um dicionário organizado para cada agente.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = json.load(file)
    except Exception as e:
        logging.error(f"Erro ao ler o arquivo {file_path}: {e}")
        return None

    logging.debug(f"Arquivo JSON lido com sucesso: {file_path}")

    # Inicializa o dicionário com strings vazias
    data = {key: "" for key in [
        "Feedback_ID",
        "Total_execution_time",
        "Patient_Feedback",
        "Sentiment_Patient_Experience_Expert",
        "Emotional_Intensity_Patient_Experience_Expert",
        "Urgency_Level_Patient_Experience_Expert",
        "Key_Issues_Patient_Experience_Expert",
        "Patient_Journey_Health_IT_Process_Expert",
        "Inefficiencies_Healthcare_Process_Health_IT_Process_Expert",
        "Improvement_Suggestions_Healthcare_Process_Health_IT_Process_Expert",
        "Emotional_State_Clinical_Psychologist",
        "Support_Strategy_Clinical_Psychologist",
        "Suggested_Approach_Clinical_Psychologist",
        "Communication_Quality_Communication_Expert",
        "Issues_Identified_Communication_Expert",
        "Suggested_Improvements_Communication_Expert",
        "Final_Recommendation_Communication_Expert",
        "Key_Issues_Manager_and_Advisor",
        "Recommendations_Manager_and_Advisor"
    ]}

    # Usa o nome do arquivo como Feedback_ID
    feedback_id = os.path.basename(file_path).split('.')[0]
    data["Feedback_ID"] = feedback_id

    # Extrai 'Total_execution_time' e 'Patient_Feedback'
    data["Total_execution_time"] = content.get("total_execution_time", "")
    data["Patient_Feedback"] = content.get("patient_feedback", "")

    # Processa a resposta de cada agente
    for agent in content.get("agents", []):
        agent_name = agent["agent_name"].lower().replace(' ', '_')

        if "patient_experience_expert" in agent_name:
            extract_patient_experience_expert(agent["response"], data)
        elif "health_it_process_expert" in agent_name:
            extract_health_it_process_expert(agent["response"], data)
        elif "clinical_psychologist" in agent_name:
            extract_clinical_psychologist(agent["response"], data)
        elif "communication_expert" in agent_name:
            extract_communication_expert(agent["response"], data)
        elif "manager_and_advisor" in agent_name:
            extract_manager_and_advisor(agent["response"], data)

    return data

def extract_patient_experience_expert(response, data):
    """Extrai informações do agente 'Patient Experience Expert'."""
    lines = response.split('\n')
    key_issues = []
    for line in lines:
        if "Sentiment_Patient_Experience_Expert" in line:
            data["Sentiment_Patient_Experience_Expert"] = line.split(":")[1].strip()
        elif "Emotional_Intensity_Patient_Experience_Expert" in line:
            data["Emotional_Intensity_Patient_Experience_Expert"] = line.split(":")[1].strip()
        elif "Urgency_Level_Patient_Experience_Expert" in line:
            data["Urgency_Level_Patient_Experience_Expert"] = line.split(":")[1].strip()
        elif "Key_Issues_Patient_Experience_Expert" in line or line.startswith("-"):
            key_issues.append(line.strip("- ").strip())
    data["Key_Issues_Patient_Experience_Expert"] = "; ".join(key_issues)

def extract_health_it_process_expert(response, data):
    """Extrai corretamente informações do agente 'Health & IT Process Expert'."""
    patient_journey = []
    inefficiencies = []
    improvement_suggestions = []
    
    section = None  # Controla a seção atual que está sendo processada

    for line in response.split('\n'):
        line = line.strip()
        if "Patient_Journey_Health_IT_Process_Expert" in line:
            section = "Patient_Journey"
            continue
        elif "Inefficiencies_Healthcare_Process_Health_IT_Process_Expert" in line:
            section = "Inefficiencies"
            continue
        elif "Improvement_Suggestions_Healthcare_Process_Health_IT_Process_Expert" in line:
            section = "Improvement_Suggestions"
            continue
        
        # Processar as seções respectivas
        if section == "Patient_Journey" and line:
            patient_journey.append(line)
        elif section == "Inefficiencies" and line:
            inefficiencies.append(line)
        elif section == "Improvement_Suggestions" and line:
            improvement_suggestions.append(line)
    
    # Preencher os dados extraídos nas colunas corretas
    data["Patient_Journey_Health_IT_Process_Expert"] = "; ".join(patient_journey)
    data["Inefficiencies_Healthcare_Process_Health_IT_Process_Expert"] = "; ".join(inefficiencies)
    data["Improvement_Suggestions_Healthcare_Process_Health_IT_Process_Expert"] = "; ".join(improvement_suggestions)

def extract_clinical_psychologist(response, data):
    """Extrai informações do agente 'Clinical Psychologist'."""
    lines = response.split('\n')
    suggested_approach = []
    for line in lines:
        if "Emotional_State_Clinical_Psychologist" in line:
            data["Emotional_State_Clinical_Psychologist"] = line.split(":")[1].strip()
        elif "Support_Strategy_Clinical_Psychologist" in line:
            data["Support_Strategy_Clinical_Psychologist"] = line.split(":")[1].strip()
        elif "Suggested_Approach_Clinical_Psychologist" in line or line.startswith("-"):
            suggested_approach.append(line.strip("- ").strip())
    data["Suggested_Approach_Clinical_Psychologist"] = "; ".join(suggested_approach)

def extract_communication_expert(response, data):
    """Extrai informações do agente 'Communication Expert'."""
    lines = response.split('\n')
    issues_identified = []
    suggested_improvements = []
    for line in lines:
        if "Communication_Quality_Communication_Expert" in line:
            data["Communication_Quality_Communication_Expert"] = line.split(":")[1].strip()
        elif "Issues_Identified_Communication_Expert" in line or line.startswith("-"):
            issues_identified.append(line.strip("- ").strip())
        elif "Suggested_Improvements_Communication_Expert" in line or line.startswith("-"):
            suggested_improvements.append(line.strip("- ").strip())
        elif "Final_Recommendation_Communication_Expert" in line:
            data["Final_Recommendation_Communication_Expert"] = line.split(":")[1].strip()
    data["Issues_Identified_Communication_Expert"] = "; ".join(issues_identified)
    data["Suggested_Improvements_Communication_Expert"] = "; ".join(suggested_improvements)

def extract_manager_and_advisor(response, data):
    """Extrai informações do agente 'Manager and Advisor'."""
    lines = response.split('\n')
    key_issues = []
    recommendations = []
    for line in lines:
        if "Key_Issues_Manager_and_Advisor" in line or line.startswith("-"):
            key_issues.append(line.strip("- ").strip())
        elif "Recommendations_Manager_and_Advisor" in line or line.startswith("-"):
            recommendations.append(line.strip("- ").strip())
    data["Key_Issues_Manager_and_Advisor"] = "; ".join(key_issues)
    data["Recommendations_Manager_and_Advisor"] = "; ".join(recommendations)

def process_multiple_jsons(directory, csv_output_path):
    """Processa múltiplos arquivos JSON e salva em um CSV final."""
    all_data = []

    if not os.path.exists(directory):
        logging.error(f"O diretório {directory} não existe!")
        return

    json_files = [f for f in os.listdir(directory) if f.endswith(".json")]

    if not json_files:
        logging.error(f"Nenhum arquivo JSON encontrado no diretório {directory}")
        return

    for file_name in json_files:
        file_path = os.path.join(directory, file_name)
        logging.info(f"Processando o arquivo: {file_name}")
        report_data = process_json_report(file_path)
        if report_data:
            all_data.append(report_data)
            logging.info(f"Adicionado: {file_name}")
        else:
            logging.error(f"Falha ao processar: {file_name}")

    if all_data:
        df_new = pd.DataFrame(all_data)

        try:
            # Cria o diretório de saída se ele não existir
            output_dir = os.path.dirname(csv_output_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                logging.debug(f"Criado o diretório de saída: {output_dir}")

            if os.path.exists(csv_output_path) and os.path.getsize(csv_output_path) > 0:
                # Concatena os novos dados com o CSV existente
                df_existing = pd.read_csv(csv_output_path, encoding='utf-8-sig')
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            else:
                df_combined = df_new

            # Salva o dataframe combinado no CSV
            df_combined.to_csv(csv_output_path, index=False, encoding='utf-8-sig')
            logging.info(f"Dados salvos em {csv_output_path}")
        except Exception as e:
            logging.error(f"Erro ao salvar o CSV {csv_output_path}: {e}")
    else:
        logging.warning("Nenhum dado novo para processar.")

# Caminhos e diretórios
directory_with_jsons = "D:\\OneDrive - InMotion - Consulting\\AI Projects\\AI-Clinical-Advisory-Crew\\data_reports_json"
csv_output_path = "D:\\OneDrive - InMotion - Consulting\\AI Projects\\AI-Clinical-Advisory-Crew\\DB\\consolidated_patient_feedback.csv"

# Processar os arquivos JSON e salvar no CSV
process_multiple_jsons(directory_with_jsons, csv_output_path)

