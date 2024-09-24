import os
import json
import pandas as pd
import logging

class DbIntegration:
    def __init__(self, json_directory, csv_output_path):
        self.json_directory = json_directory
        self.csv_output_path = csv_output_path
        
        # Configurar o logging
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

    def process_json_report(self, file_path):
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

        # Use the file name as Feedback_ID
        feedback_id = os.path.basename(file_path).split('.')[0]
        data["Feedback_ID"] = feedback_id

        # Extract 'Total_execution_time' and 'Patient_Feedback'
        data["Total_execution_time"] = content.get("total_execution_time", "")
        data["Patient_Feedback"] = content.get("patient_feedback", "")

        # Process each agent's response
        for agent in content.get("agents", []):
            agent_name = agent["agent_name"].lower().replace(' ', '_')

            if "patient_experience_expert" in agent_name:
                self.extract_patient_experience_expert(agent["response"], data)
            elif "health_it_process_expert" in agent_name:
                self.extract_health_it_process_expert(agent["response"], data)
            elif "clinical_psychologist" in agent_name:
                self.extract_clinical_psychologist(agent["response"], data)
            elif "communication_expert" in agent_name:
                self.extract_communication_expert(agent["response"], data)
            elif "manager_and_advisor" in agent_name:
                self.extract_manager_and_advisor(agent["response"], data)

        return data

    def extract_patient_experience_expert(self, response, data):
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

    def extract_health_it_process_expert(self, response, data):
        """Extrai informações do agente 'Health & IT Process Expert'."""
        sections = response.split("\n\n")  # Split the response into sections based on double newlines.
        
        # Initialize empty lists to store the steps.
        patient_journey = []
        inefficiencies = []
        improvements = []

        for section in sections:
            if "Patient_Journey_Health_IT_Process_Expert" in section:
                journey_steps = section.split("\n")[1:]  # Skip the first line (label)
                patient_journey = [step.strip("- ").strip() for step in journey_steps if step.strip()]
            
            elif "Inefficiencies_Healthcare_Process_Health_IT_Process_Expert" in section:
                inefficiency_steps = section.split("\n")[1:]
                inefficiencies = [step.strip("- ").strip() for step in inefficiency_steps if step.strip()]
            
            elif "Improvement_Suggestions_Healthcare_Process_Health_IT_Process_Expert" in section:
                improvement_steps = section.split("\n")[1:]
                improvements = [step.strip("- ").strip() for step in improvement_steps if step.strip()]
        
        # Assign data to the respective columns, leaving it empty if no data is present.
        data["Patient_Journey_Health_IT_Process_Expert"] = "; ".join(patient_journey) if patient_journey else ""
        data["Inefficiencies_Healthcare_Process_Health_IT_Process_Expert"] = "; ".join(inefficiencies) if inefficiencies else ""
        data["Improvement_Suggestions_Healthcare_Process_Health_IT_Process_Expert"] = "; ".join(improvements) if improvements else ""

    def extract_clinical_psychologist(self, response, data):
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

    def extract_communication_expert(self, response, data):
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

    def extract_manager_and_advisor(self, response, data):
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

    def process_multiple_jsons(self):
        print("Starting to process JSON files...")
        all_data = []

        if not os.path.exists(self.json_directory):
            logging.error(f"O diretório {self.json_directory} não existe!")
            return

        json_files = [f for f in os.listdir(self.json_directory) if f.endswith(".json")]

        if not json_files:
            logging.error(f"Nenhum arquivo JSON encontrado no diretório {self.json_directory}")
            return

        for file_name in json_files:
            file_path = os.path.join(self.json_directory, file_name)
            logging.info(f"Processando o arquivo: {file_name}")
            report_data = self.process_json_report(file_path)
            if report_data:
                all_data.append(report_data)
                logging.info(f"Adicionado: {file_name}")
                print(f"Processed file: {file_name}")
            else:
                logging.error(f"Falha ao processar: {file_name}")

        if all_data:
            df_new = pd.DataFrame(all_data)

            try:
                # Cria o diretório de saída se não existir
                output_dir = os.path.dirname(self.csv_output_path)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                    logging.debug(f"Criado o diretório de saída: {output_dir}")

                if os.path.exists(self.csv_output_path) and os.path.getsize(self.csv_output_path) > 0:
                    # Lê o CSV existente
                    df_existing = pd.read_csv(self.csv_output_path, encoding='utf-8-sig')

                    # Obter os conjuntos de Feedback_ID
                    existing_ids = set(df_existing["Feedback_ID"].tolist())
                    current_ids = set(df_new["Feedback_ID"].tolist())

                    # Identificar Feedback_IDs para remover (arquivos removidos)
                    ids_to_remove = existing_ids - current_ids
                    if ids_to_remove:
                        df_existing = df_existing[~df_existing["Feedback_ID"].isin(ids_to_remove)]
                        logging.info(f"Removidos os dados de: {', '.join(ids_to_remove)}")

                    # Identificar Feedback_IDs para adicionar (novos arquivos)
                    ids_to_add = current_ids - existing_ids
                    df_to_add = df_new[df_new["Feedback_ID"].isin(ids_to_add)]

                    # Concatenar os novos dados com os existentes
                    df_combined = pd.concat([df_existing, df_to_add], ignore_index=True)
                else:
                    # Caso o CSV não exista ou esteja vazio
                    df_combined = df_new

                # Salva o dataframe combinado no CSV
                df_combined.to_csv(self.csv_output_path, index=False, encoding='utf-8-sig')
                logging.info(f"Dados salvos em {self.csv_output_path}")
            except Exception as e:
                logging.error(f"Erro ao salvar o CSV {self.csv_output_path}: {e}")
        else:
            logging.warning("Nenhum dado novo para processar.")

        print("Finished processing all JSON files.")

if __name__ == "__main__":
    # Caminhos e diretórios
    directory_with_jsons = "D:\\OneDrive - InMotion - Consulting\\AI Projects\\AI-Clinical-Advisory-Crew\\data_reports_json"
    csv_output_path = "D:\\OneDrive - InMotion - Consulting\\AI Projects\\AI-Clinical-Advisory-Crew\\DB\\consolidated_patient_feedback.csv"

    # Criar uma instância da classe DbIntegration
    db_integration = DbIntegration(directory_with_jsons, csv_output_path)

    # Processar os arquivos JSON e salvar no CSV
    db_integration.process_multiple_jsons()

