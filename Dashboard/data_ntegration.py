import os
import pandas as pd
import re
import logging

# Configurar o logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

def normalize_key(key):
    key = key.strip()
    key = re.sub(r'^[-\*\s]+', '', key)  # Remove markers, asterisks, and leading spaces
    key = re.sub(r'[-\*\s]+$', '', key)  # Remove markers, asterisks, and trailing spaces
    key = key.strip()
    key = key.lower()
    key = key.replace('&', 'and')         # Replace '&' with 'and'
    key = re.sub(r'\s+', '_', key)        # Replace spaces with underscores
    key = re.sub(r'[^a-z0-9_]', '', key)  # Remove non-alphanumeric characters except underscores
    return key

def process_txt_report(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        logging.error(f"Erro ao ler o arquivo {file_path}: {e}")
        return None

    # Use the file name as Feedback_ID
    feedback_id = os.path.basename(file_path).split('.')[0]

    # Initialize the data dictionary with empty strings
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
    data["Feedback_ID"] = feedback_id

    # Extract 'Total execution time' from the full content
    match_total_time = re.search(r'Total execution time:\s*(.*)', content)
    if match_total_time:
        total_time = match_total_time.group(1).strip()
        data['Total_execution_time'] = total_time
        logging.debug(f"Extraído 'Total_execution_time': {total_time}")

    # Split the content into sections based on separators
    sections = content.split('############################')

    for section in sections:
        section = section.strip()
        if not section:
            continue

        # Patient Feedback Section
        if 'Patient Feedback:' in section:
            match = re.search(r'Patient Feedback:(.*)', section, re.DOTALL)
            if match:
                patient_feedback = match.group(1).strip()
                data['Patient_Feedback'] = patient_feedback
                logging.debug(f"Extraído 'Patient_Feedback': {patient_feedback}")

        # Agent Sections
        elif 'Agent:' in section:
            agent_match = re.search(r'Agent:\s*(.*)', section)
            if agent_match:
                agent_name = agent_match.group(1).strip()
                # Capture the content after 'Final Answer:'
                answer_match = re.search(r'Final Answer:\s*(.*)', section, re.DOTALL)
                if answer_match:
                    agent_content = answer_match.group(1).strip()
                    logging.debug(f"Processando agente: {agent_name}")
                    # Process the agent's content
                    process_agent_section(agent_name, agent_content, data)
                else:
                    logging.warning(f"'Final Answer:' não encontrado para o agente '{agent_name}'")
            else:
                logging.warning(f"'Agent:' não encontrado na seção.")
        else:
            logging.warning(f"Seção não reconhecida: {section[:30]}...")

    return data

def process_agent_section(agent_name, agent_content, data):
    agent_key_mappings = {
        'patient_experience_expert': {
            'sentiment_patient_experience_expert': 'Sentiment_Patient_Experience_Expert',
            'emotional_intensity_patient_experience_expert': 'Emotional_Intensity_Patient_Experience_Expert',
            'urgency_level_patient_experience_expert': 'Urgency_Level_Patient_Experience_Expert',
            'key_issues_patient_experience_expert': 'Key_Issues_Patient_Experience_Expert',
        },
        'health_and_it_process_expert': {
            'patient_journey_health_it_process_expert': 'Patient_Journey_Health_IT_Process_Expert',
            'inefficiencies_healthcare_process_health_it_process_expert': 'Inefficiencies_Healthcare_Process_Health_IT_Process_Expert',
            'improvement_suggestions_healthcare_process_health_it_process_expert': 'Improvement_Suggestions_Healthcare_Process_Health_IT_Process_Expert',
        },
        'clinical_psychologist': {
            'emotional_state_clinical_psychologist': 'Emotional_State_Clinical_Psychologist',
            'support_strategy_clinical_psychologist': 'Support_Strategy_Clinical_Psychologist',
            'suggested_approach_clinical_psychologist': 'Suggested_Approach_Clinical_Psychologist',
        },
        'communication_expert': {
            'communication_quality_communication_expert': 'Communication_Quality_Communication_Expert',
            'issues_identified_communication_expert': 'Issues_Identified_Communication_Expert',
            'suggested_improvements_communication_expert': 'Suggested_Improvements_Communication_Expert',
            'final_recommendation_communication_expert': 'Final_Recommendation_Communication_Expert',
        },
        'manager_and_advisor': {
            'key_issues_manager_and_advisor': 'Key_Issues_Manager_and_Advisor',
            'recommendations_manager_and_advisor': 'Recommendations_Manager_and_Advisor',
        },
    }

    normalized_agent_name = normalize_key(agent_name)
    key_mapping = agent_key_mappings.get(normalized_agent_name, {})

    if not key_mapping:
        logging.warning(f"Unknown agent or unmapped: '{agent_name}' (normalized: '{normalized_agent_name}')")
        return

    # Prepare a regex pattern to match any key in key_mapping
    key_pattern = re.compile(r'^[-\*\s]*(.+?):\s*(.*)')
    expected_keys = set(key_mapping.keys())

    lines = agent_content.splitlines()
    current_key = None
    value_accumulator = []

    for line in lines:
        line = line.strip()

        if not line or line in ('**', '*'):
            continue

        # Check if line is a key
        match = key_pattern.match(line)
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()

            # Normalize the key
            normalized_key = normalize_key(key)
            mapped_key = key_mapping.get(normalized_key)

            if mapped_key:
                # Save the previous key's value
                if current_key and value_accumulator:
                    data[current_key] = '\n'.join(value_accumulator).strip()
                    value_accumulator = []

                current_key = mapped_key
                value_accumulator = [value] if value else []
            else:
                logging.debug(f"Unrecognized key '{key}' in agent '{agent_name}'")
                current_key = None
        elif line.startswith('-') or line.startswith('*') or re.match(r'^\d+\.', line):
            # It's a list item (bullet or numbered)
            if current_key:
                value_accumulator.append(line.strip())
        else:
            # Continuation of the current key's value
            if current_key:
                value_accumulator.append(line.strip())

    # Save the last accumulated value
    if current_key and value_accumulator:
        data[current_key] = '\n'.join(value_accumulator).strip()

    # Post-processing for specific fields to extract only the required information
    # For 'Sentiment_Patient_Experience_Expert' and 'Urgency_Level_Patient_Experience_Expert', extract only the classification
    if 'Sentiment_Patient_Experience_Expert' in data:
        sentiment_match = re.search(r'\b(Positive|Neutral|Negative)\b', data['Sentiment_Patient_Experience_Expert'], re.IGNORECASE)
        if sentiment_match:
            data['Sentiment_Patient_Experience_Expert'] = sentiment_match.group(1).capitalize()
        else:
            data['Sentiment_Patient_Experience_Expert'] = data['Sentiment_Patient_Experience_Expert'].strip()

    if 'Urgency_Level_Patient_Experience_Expert' in data:
        urgency_match = re.search(r'\b(High|Medium|Low)\b', data['Urgency_Level_Patient_Experience_Expert'], re.IGNORECASE)
        if urgency_match:
            data['Urgency_Level_Patient_Experience_Expert'] = urgency_match.group(1).capitalize()
        else:
            data['Urgency_Level_Patient_Experience_Expert'] = data['Urgency_Level_Patient_Experience_Expert'].strip()

    # For 'Emotional_Intensity_Patient_Experience_Expert', extract the numeric value
    if 'Emotional_Intensity_Patient_Experience_Expert' in data:
        intensity_match = re.search(r'([-+]?\d*\.?\d+)', data['Emotional_Intensity_Patient_Experience_Expert'])
        if intensity_match:
            data['Emotional_Intensity_Patient_Experience_Expert'] = intensity_match.group(1)
        else:
            data['Emotional_Intensity_Patient_Experience_Expert'] = data['Emotional_Intensity_Patient_Experience_Expert'].strip()

    # Post-process the `Recommendations_Manager_and_Advisor` field if necessary.
    if 'Recommendations_Manager_and_Advisor' in data:
        # Ensure all lines are captured properly
        data['Recommendations_Manager_and_Advisor'] = '\n'.join([line.strip() for line in value_accumulator if line]).strip()
        logging.debug(f"Processed 'Recommendations_Manager_and_Advisor': {data['Recommendations_Manager_and_Advisor']}")

def already_processed(feedback_id, existing_csv):
    if os.path.exists(existing_csv) and os.path.getsize(existing_csv) > 0:
        try:
            df_existing = pd.read_csv(existing_csv, encoding='utf-8-sig')
            return feedback_id in df_existing['Feedback_ID'].values
        except Exception as e:
            logging.error(f"Erro ao ler o CSV existente {existing_csv}: {e}")
            return False
    return False

def process_multiple_txts(directory, csv_output_path):
    all_data = []

    for file_name in os.listdir(directory):
        if file_name.endswith(".txt"):
            file_path = os.path.join(directory, file_name)
            feedback_id = os.path.basename(file_path).split('.')[0]

            if not already_processed(feedback_id, csv_output_path):
                report_data = process_txt_report(file_path)
                if report_data:
                    all_data.append(report_data)
                    print(f"Processed and added: {file_name}")
                else:
                    print(f"Failed to process: {file_name}")
            else:
                print(f"Already processed: {file_name}")

    if all_data:
        df_new = pd.DataFrame(all_data)

        try:
            # Create the output directory if it doesn't exist
            output_dir = os.path.dirname(csv_output_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                logging.debug(f"Criado o diretório de saída: {output_dir}")

            if os.path.exists(csv_output_path) and os.path.getsize(csv_output_path) > 0:
                df_existing = pd.read_csv(csv_output_path, encoding='utf-8-sig')
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            else:
                df_combined = df_new

            df_combined.to_csv(csv_output_path, index=False, encoding='utf-8-sig')
            print(f"Data saved to {csv_output_path}")
        except Exception as e:
            logging.error(f"Erro ao salvar o CSV {csv_output_path}: {e}")
    else:
        print("No new data to process.")

# Example usage
directory_with_txts = "D:\\OneDrive - InMotion - Consulting\\AI Projects\\AI-Clinical-Advisory-Crew\\data_reports"
csv_output_path = "D:\\OneDrive - InMotion - Consulting\\AI Projects\\AI-Clinical-Advisory-Crew\\Dashboard\\processed_patient_feedback.csv"

# Process multiple TXT files and save to CSV
process_multiple_txts(directory_with_txts, csv_output_path)
