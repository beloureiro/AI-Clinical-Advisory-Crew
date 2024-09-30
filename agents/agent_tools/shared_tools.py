from pydantic import BaseModel
from crewai_tools import BaseTool, tool
import os
import shutil
import json

# Definir o schema de argumentos usando Pydantic
class DuplicateFileArgs(BaseModel):
    source_path: str
    destination_path: str

class GenerateProofArgs(BaseModel):
    txt_content: str
    json_content: str
    json_file_path: str  # O caminho para o arquivo JSON, usado para gerar o nome do arquivo de prova automaticamente

# Ferramenta de Duplicação de Arquivos com cache e validação de caminhos
@tool("Duplicate File Tool")
class DuplicateFileTool(BaseTool):
    """
    Tool for duplicating a file from a source path to a destination path.

    This tool ensures that the destination directory exists, checks if the file 
    has already been copied (using caching), and performs the file duplication.
    """
    name: str = "Duplicate File Tool"
    description: str = "Copies files from the source path to the destination path."
    args_schema: type[DuplicateFileArgs]

    def _run(self, source_path, destination_path):
        try:
            # Verificar se o arquivo já foi duplicado (mecanismo de cache)
            if os.path.exists(destination_path):
                return f"Cache hit: File {destination_path} already exists."

            # Verificar se o caminho de origem existe
            if not os.path.exists(source_path):
                return f"Error: Source file {source_path} does not exist."

            # Garantir que o diretório de destino exista
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)

            # Copiar o arquivo
            shutil.copy2(source_path, destination_path)
            return f"File copied from {source_path} to {destination_path}"

        except Exception as e:
            return f"Error copying file from {source_path} to {destination_path}: {str(e)}"

# Ferramenta de Geração de Prova com cache e validação de caminhos
@tool("Generate Proof Tool")
class GenerateProofTool(BaseTool):
    """
    Tool for generating a proof file comparing content from TXT and JSON files.

    This tool generates a proof file that includes detailed comparisons between 
    the sections of the TXT and JSON files, ensuring consistency in the data.
    """
    name: str = "Generate Proof Tool"
    description: str = "Generates a detailed proof file comparing the content of the TXT and JSON files, section by section."
    args_schema: type[GenerateProofArgs]

    def _run(self, txt_content, json_content, json_file_path):
        # Gera o nome do arquivo de prova automaticamente, adicionando o sufixo '_proof.json'
        proof_file_path = json_file_path.replace('.json', '_proof.json').replace('json_synced', 'json_proof')

        # Verificar se o arquivo de prova já foi gerado (mecanismo de cache)
        if os.path.exists(proof_file_path):
            return f"Cache hit: Proof file {proof_file_path} already exists."

        # Estrutura detalhada do arquivo de prova, organizando por seções
        proof_data = {
            "Root": {
                "Patient_Feedback": {
                    "Original": txt_content.get("Patient_Feedback", "N/A"),
                    "JSON": json_content.get("Patient_Feedback", "N/A")
                },
                "Total_Execution_Time": {
                    "Original": txt_content.get("Total_Execution_Time", "N/A"),
                    "JSON": json_content.get("Total_Execution_Time", "N/A")
                },
                "Agents": {
                    "Patient_Experience_Expert": {
                        "Sentiment": {
                            "Original": txt_content.get("Sentiment_Patient_Experience_Expert", "N/A"),
                            "JSON": json_content.get("Sentiment_Patient_Experience_Expert", "N/A")
                        },
                        "Emotional_Intensity": {
                            "Original": txt_content.get("Emotional_Intensity_Patient_Experience_Expert", "N/A"),
                            "JSON": json_content.get("Emotional_Intensity_Patient_Experience_Expert", "N/A")
                        },
                        "Urgency_Level": {
                            "Original": txt_content.get("Urgency_Level_Patient_Experience_Expert", "N/A"),
                            "JSON": json_content.get("Urgency_Level_Patient_Experience_Expert", "N/A")
                        },
                        "Key_Issues": {
                            "Original": txt_content.get("Key_Issues_Patient_Experience_Expert", "N/A"),
                            "JSON": json_content.get("Key_Issues_Patient_Experience_Expert", "N/A")
                        }
                    },
                    "Health_IT_Process_Expert": {
                        "Patient_Journey": {
                            "Original": txt_content.get("Patient_Journey_Health_IT_Process_Expert", []),
                            "JSON": json_content.get("Patient_Journey_Health_IT_Process_Expert", [])
                        },
                        "Inefficiencies": {
                            "Original": txt_content.get("Inefficiencies_Healthcare_Process_Health_IT_Process_Expert", "N/A"),
                            "JSON": json_content.get("Inefficiencies_Healthcare_Process_Health_IT_Process_Expert", "N/A")
                        },
                        "Improvement_Suggestions": {
                            "Original": txt_content.get("Improvement_Suggestions_Healthcare_Process_Health_IT_Process_Expert", []),
                            "JSON": json_content.get("Improvement_Suggestions_Healthcare_Process_Health_IT_Process_Expert", [])
                        }
                    },
                    "Clinical_Psychologist": {
                        "Emotional_State": {
                            "Original": txt_content.get("Emotional_State_Clinical_Psychologist", "N/A"),
                            "JSON": json_content.get("Emotional_State_Clinical_Psychologist", "N/A")
                        },
                        "Support_Strategy": {
                            "Original": txt_content.get("Support_Strategy_Clinical_Psychologist", "N/A"),
                            "JSON": json_content.get("Support_Strategy_Clinical_Psychologist", "N/A")
                        },
                        "Suggested_Approach": {
                            "Original": txt_content.get("Suggested_Approach_Clinical_Psychologist", []),
                            "JSON": json_content.get("Suggested_Approach_Clinical_Psychologist", [])
                        }
                    },
                    "Communication_Expert": {
                        "Communication_Quality": {
                            "Original": txt_content.get("Communication_Quality_Communication_Expert", "N/A"),
                            "JSON": json_content.get("Communication_Quality_Communication_Expert", "N/A")
                        },
                        "Issues_Identified": {
                            "Original": txt_content.get("Issues_Identified_Communication_Expert", "N/A"),
                            "JSON": json_content.get("Issues_Identified_Communication_Expert", "N/A")
                        },
                        "Suggested_Improvements": {
                            "Original": txt_content.get("Suggested_Improvements_Communication_Expert", []),
                            "JSON": json_content.get("Suggested_Improvements_Communication_Expert", [])
                        },
                        "Final_Recommendation": {
                            "Original": txt_content.get("Final_Recommendation_Communication_Expert", "N/A"),
                            "JSON": json_content.get("Final_Recommendation_Communication_Expert", "N/A")
                        }
                    },
                    "Manager_and_Advisor": {
                        "Key_Issues": {
                            "Original": txt_content.get("Key_Issues_Manager_and_Advisor", []),
                            "JSON": json_content.get("Key_Issues_Manager_and_Advisor", [])
                        },
                        "Recommendations": {
                            "Original": txt_content.get("Recommendations_Manager_and_Advisor", []),
                            "JSON": json_content.get("Recommendations_Manager_and_Advisor", [])
                        }
                    }
                },
                "Consolidated_Final_Report": {
                    "Original": txt_content.get("Consolidated_Final_Report", "Present"),
                    "JSON": json_content.get("Consolidated_Final_Report", "Absent")
                },
                "Disclaimer": {
                    "Original": txt_content.get("Disclaimer", "Present"),
                    "JSON": json_content.get("Disclaimer", "Absent")
                }
            }
        }

        try:
            # Garantir que o diretório de destino exista
            os.makedirs(os.path.dirname(proof_file_path), exist_ok=True)

            # Gerar o arquivo de prova
            with open(proof_file_path, 'w', encoding='utf-8') as proof_file:
                json.dump(proof_data, proof_file, indent=4, ensure_ascii=False)

            return f"Proof file generated at {proof_file_path}"

        except Exception as e:
            return f"Error generating proof file at {proof_file_path}: {str(e)}"
