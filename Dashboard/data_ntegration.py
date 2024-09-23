import os
import pandas as pd
import re

# Função para processar o arquivo de texto e extrair as informações
def process_txt_report(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Usar o nome do arquivo como Feedback_ID
    feedback_id = os.path.basename(file_path).split('.')[0]

    # Inicializar o dicionário de dados
    data = {
        "Feedback_ID": feedback_id,
        "Total_execution_time": "",
        "Patient_Feedback": "",
        "Sentiment_Patient_Experience_Expert": "",
        "Emotional_Intensity_Patient_Experience_Expert": "",
        "Urgency_Level_Patient_Experience_Expert": "",
        "Key_Issues_Patient_Experience_Expert": "",
        "Patient_Journey_Health_IT_Process_Expert": "",
        "Inefficiencies_Healthcare_Process_Health_IT_Process_Expert": "",
        "Improvement_Suggestions_Healthcare_Process_Health_IT_Process_Expert": "",
        "Emotional_State_Clinical_Psychologist": "",
        "Support_Strategy_Clinical_Psychologist": "",
        "Suggested_Approach_Clinical_Psychologist": "",
        "Communication_Quality_Communication_Expert": "",
        "Issues_Identified_Communication_Expert": "",
        "Suggested_Improvements_Communication_Expert": "",
        "Final_Recommendation_Communication_Expert": "",
        "Key_Issues_Manager_and_Advisor": "",
        "Recommendations_Manager_and_Advisor": ""
    }

    # Dividir o conteúdo em seções
    sections = re.split(r'#{10,}', content)

    for section in sections:
        section = section.strip()
        if not section:
            continue

        # Verificar se é a seção de Feedback do Paciente
        if 'Patient Feedback:' in section:
            match = re.search(r'Patient Feedback:(.*?)(?=\n#|$)', section, re.DOTALL)
            if match:
                patient_feedback = match.group(1).strip()
                data['Patient_Feedback'] = patient_feedback

        # Verificar se é a seção de Tempo de Execução Total
        if 'Total execution time:' in section:
            match = re.search(r'Total execution time:\s*(.*)', section)
            if match:
                data['Total_execution_time'] = match.group(1).strip()

        # Verificar se é a seção de um Agente/Especialista
        agent_match = re.search(r'# Agent:\s*(.*)', section)
        if agent_match:
            agent_name = agent_match.group(1).strip()
            if 'Patient Experience Expert' in agent_name:
                process_patient_experience_expert_section(section, data)
            elif 'Health & IT Process Expert' in agent_name:
                process_health_it_process_expert_section(section, data)
            elif 'Clinical Psychologist' in agent_name:
                process_clinical_psychologist_section(section, data)
            elif 'Communication Expert' in agent_name:
                process_communication_expert_section(section, data)
            elif 'Manager and Advisor' in agent_name:
                process_manager_and_advisor_section(section, data)

    return data

# Função para processar a seção do Patient Experience Expert
def process_patient_experience_expert_section(section_text, data):
    # Usar expressões regulares para extrair os dados
    key_issues_match = re.search(r'\*\*Key Issues\*\*:(.*?)(\*\*|$)', section_text, re.DOTALL)
    if key_issues_match:
        key_issues_text = key_issues_match.group(1)
        key_issues_list = re.findall(r'-\s*(.*)', key_issues_text)
        data['Key_Issues_Patient_Experience_Expert'] = ' | '.join(key_issues_list)

    emotional_intensity_match = re.search(r'\*\*Emotional Intensity\*\*:\s*(.*)', section_text)
    if emotional_intensity_match:
        data['Emotional_Intensity_Patient_Experience_Expert'] = emotional_intensity_match.group(1).strip()

    sentiment_match = re.search(r'\*\*Sentiment\*\*:\s*(.*)', section_text)
    if sentiment_match:
        data['Sentiment_Patient_Experience_Expert'] = sentiment_match.group(1).strip()

    urgency_level_match = re.search(r'\*\*Urgency Level\*\*:\s*(.*)', section_text)
    if urgency_level_match:
        data['Urgency_Level_Patient_Experience_Expert'] = urgency_level_match.group(1).strip()

# Função para processar a seção do Health & IT Process Expert
def process_health_it_process_expert_section(section_text, data):
    # Extrair inefficiencies
    inefficiencies_match = re.search(r'key inefficiencies related to (.*?)(\.|$)', section_text, re.IGNORECASE)
    if inefficiencies_match:
        data['Inefficiencies_Healthcare_Process_Health_IT_Process_Expert'] = inefficiencies_match.group(1).strip()

    # Extrair improvement suggestions
    improvement_suggestions_match = re.search(r'To improve (.*?)(\.|$)', section_text, re.DOTALL | re.IGNORECASE)
    if improvement_suggestions_match:
        data['Improvement_Suggestions_Healthcare_Process_Health_IT_Process_Expert'] = improvement_suggestions_match.group(1).strip()

# Função para processar a seção do Clinical Psychologist
def process_clinical_psychologist_section(section_text, data):
    emotional_state_match = re.search(r'\* Emotional State:\s*(.*?)(?=\n\*|$)', section_text, re.DOTALL)
    if emotional_state_match:
        data['Emotional_State_Clinical_Psychologist'] = emotional_state_match.group(1).strip()

    support_strategy_match = re.search(r'\* Support Strategy:\s*(.*?)(?=\n\*|$)', section_text, re.DOTALL)
    if support_strategy_match:
        data['Support_Strategy_Clinical_Psychologist'] = support_strategy_match.group(1).strip()

    suggested_approach_match = re.search(r'\* Suggested Approach:\s*(.*)', section_text, re.DOTALL)
    if suggested_approach_match:
        data['Suggested_Approach_Clinical_Psychologist'] = suggested_approach_match.group(1).strip()

# Função para processar a seção do Communication Expert
def process_communication_expert_section(section_text, data):
    communication_quality_match = re.search(r'\* Communication Quality:\s*\*\*(.*?)\*\*', section_text)
    if communication_quality_match:
        data['Communication_Quality_Communication_Expert'] = communication_quality_match.group(1).strip()

    issues_identified_match = re.search(r'\* Issues Identified:(.*?)(?=\n\*|$)', section_text, re.DOTALL)
    if issues_identified_match:
        issues_text = issues_identified_match.group(1)
        issues_list = re.findall(r'\*\*\*(.*?)\*\*\*', issues_text)
        if not issues_list:
            issues_list = re.findall(r'-\s*(.*)', issues_text)
        data['Issues_Identified_Communication_Expert'] = ' | '.join([issue.strip() for issue in issues_list])

    suggested_improvements_match = re.search(r'\* Suggested Improvements:(.*?)(?=\n\*|$)', section_text, re.DOTALL)
    if suggested_improvements_match:
        improvements_text = suggested_improvements_match.group(1)
        improvements_list = re.findall(r'-\s*(.*)', improvements_text)
        data['Suggested_Improvements_Communication_Expert'] = ' | '.join([imp.strip() for imp in improvements_list])

    final_recommendation_match = re.search(r'\* Final Recommendation:\s*(.*)', section_text, re.DOTALL)
    if final_recommendation_match:
        data['Final_Recommendation_Communication_Expert'] = final_recommendation_match.group(1).strip()

# Função para processar a seção do Manager and Advisor
def process_manager_and_advisor_section(section_text, data):
    key_issues_match = re.search(r'\*\*Key Issues\*\*:(.*?)(?=\*\*Recommendations\*\*|$)', section_text, re.DOTALL)
    if key_issues_match:
        key_issues_text = key_issues_match.group(1)
        key_issues_list = re.findall(r'\*\*\*(.*?)\*\*\*', key_issues_text)
        if not key_issues_list:
            key_issues_list = re.findall(r'-\s*(.*)', key_issues_text)
        data['Key_Issues_Manager_and_Advisor'] = ' | '.join([ki.strip() for ki in key_issues_list])

    recommendations_match = re.search(r'\*\*Recommendations\*\*:(.*?)(?=\*\*Final Recommendation\*\*|$)', section_text, re.DOTALL)
    if recommendations_match:
        recommendations_text = recommendations_match.group(1)
        recommendations_list = re.findall(r'\*\*\*(.*?)\*\*\*', recommendations_text)
        if not recommendations_list:
            recommendations_list = re.findall(r'-\s*(.*)', recommendations_text)
        data['Recommendations_Manager_and_Advisor'] = ' | '.join([rec.strip() for rec in recommendations_list])

# Função para verificar se o arquivo já foi processado
def already_processed(feedback_id, existing_csv):
    # Verificar se o CSV está vazio ou sem colunas
    if os.path.exists(existing_csv) and os.path.getsize(existing_csv) > 0:
        df_existing = pd.read_csv(existing_csv)
        return feedback_id in df_existing['Feedback_ID'].values
    return False

# Função para processar vários arquivos TXT e salvar como CSV
def process_multiple_txts(directory, csv_output_path):
    # Verificar se o CSV já existe, para garantir que novos dados sejam adicionados
    if not os.path.exists(csv_output_path):
        # Se o CSV não existe, cria um CSV novo com o cabeçalho correto
        df = pd.DataFrame(columns=[
            "Feedback_ID", "Total_execution_time", "Patient_Feedback",
            "Sentiment_Patient_Experience_Expert", "Emotional_Intensity_Patient_Experience_Expert", 
            "Urgency_Level_Patient_Experience_Expert", "Key_Issues_Patient_Experience_Expert",
            "Patient_Journey_Health_IT_Process_Expert", "Inefficiencies_Healthcare_Process_Health_IT_Process_Expert",
            "Improvement_Suggestions_Healthcare_Process_Health_IT_Process_Expert", 
            "Emotional_State_Clinical_Psychologist", "Support_Strategy_Clinical_Psychologist", 
            "Suggested_Approach_Clinical_Psychologist", "Communication_Quality_Communication_Expert", 
            "Issues_Identified_Communication_Expert", "Suggested_Improvements_Communication_Expert",
            "Final_Recommendation_Communication_Expert", "Key_Issues_Manager_and_Advisor", 
            "Recommendations_Manager_and_Advisor"
        ])
        df.to_csv(csv_output_path, index=False)

    for file_name in os.listdir(directory):
        if file_name.endswith(".txt"):
            file_path = os.path.join(directory, file_name)
            feedback_id = os.path.basename(file_path).split('.')[0]

            # Verificar se o arquivo já foi processado
            if not already_processed(feedback_id, csv_output_path):
                # Processar o arquivo e salvar os dados no CSV
                report_data = process_txt_report(file_path)
                df = pd.DataFrame([report_data])
                df.to_csv(csv_output_path, mode='a', header=False, index=False)
                print(f"Processed and added: {file_name}")
            else:
                print(f"Already processed: {file_name}")

# Exemplo de uso
directory_with_txts = "D:\\OneDrive - InMotion - Consulting\\AI Projects\\AI-Clinical-Advisory-Crew\\data_reports"
csv_output_path = "D:\\OneDrive - InMotion - Consulting\\AI Projects\\AI-Clinical-Advisory-Crew\\Dashboard\\processed_patient_feedback.csv"

# Processar múltiplos arquivos TXT e salvar no CSV
process_multiple_txts(directory_with_txts, csv_output_path)
