import sys
import os

# Adicionar o diretório principal ao caminho de pesquisa do Python antes das importações
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'agents')))

# Importações necessárias
from crewai import Agent
from config.config_ollama import gemma2_2b_text_q5_K_S, llama3_2_3b_instruct_q5_K_S, llama3_2_1b_instruct_q5_K_S,gemma2_2b_instruct_q4_K_S
from crewai_tools import FileReadTool, FileWriterTool, DirectoryReadTool
from agent_tools.shared_tools import DuplicateFileTool, GenerateProofTool

print(os.getcwd())

# Inicializar as ferramentas padrão
file_read_tool = FileReadTool()
file_write_tool = FileWriterTool()
txt_directory_tool = DirectoryReadTool(directory='D:/OneDrive - InMotion - Consulting/AI Projects/AI-Clinical-Advisory-Crew/data_reports_txt/')
json_directory_tool = DirectoryReadTool(directory='D:/OneDrive - InMotion - Consulting/AI Projects/AI-Clinical-Advisory-Crew/data_reports_json/')

# Função para garantir que o system_template tenha um valor válido
def ensure_system_template(system_template=None):
    if system_template is None or system_template == '':
        # Fornecer um valor padrão se system_template for None ou vazio
        return """
        You are the Output Consistency Agent. Your task is to ensure that the outputs are consistent and well-formatted.

        You have access to the following tools:
        {tools}

        When you need to perform an action, use the following format:

        Thought: Describe what you are thinking.
        Action: The action to take, must be one of {tool_names}.
        Action Input: The input to the action, in JSON format.
        Observation: The result of the action.

        Repeat the Thought/Action/Action Input/Observation cycle as needed until you have enough information to provide the final answer.

        Final Answer: Provide the final answer to the task.

        Remember:
        - Use the tools exactly as specified.
        - Provide clear and concise inputs and outputs.
        - Ensure that you include all required arguments when using a tool.

        Examples:
        - To read a file:
          Thought: I need to read the formatted TXT file.
          Action: Read a file's content
          Action Input: {{ "file_path": "full/path/to/formatted_file.txt" }}

        - To write to a file:
          Thought: I need to save the updated content to the file.
          Action: File Writer Tool
          Action Input: {{
            "filename": "full/path/to/file.txt",
            "content": "The updated content",
            "overwrite": true
          }}

        - To compare file names:
          Thought: I need to compare the TXT and JSON files by their base name (excluding extensions).
          Action: Compare file names
          Action Input: {{
            "txt_file": "report_20240929_113610.txt",
            "json_file": "report_20240929_113610.json"
          }}
          Observation: The base names match, proceeding with further actions.

        - To duplicate a file:
          Thought: I need to duplicate the original TXT file to a formatted version.
          Action: Duplicate File Tool
          Action Input: {{
            "source_path": "full/path/to/original_file.txt",
            "destination_path": "full/path/to/formatted_file.txt"
          }}
        """
    return system_template

# Função para garantir que o prompt_template tenha um valor válido
def ensure_prompt_template(prompt_template=None):
    if prompt_template is None or prompt_template == '':
        # Fornecer um valor padrão se prompt_template for None ou vazio
        return """
        Your task is to maintain consistency in the output.
        Please follow the format provided and ensure clarity and proper formatting.
        """
    return prompt_template

# Função para garantir que o response_template tenha um valor válido
def ensure_response_template(response_template=None):
    if response_template is None or response_template == '':
        # Fornecer um valor padrão se response_template for None ou vazio
        return """
        {{ .Response }}
        """
    return response_template

# Agente: Output Consistency Agent
output_consistency_agent = Agent(
    role="Output Consistency Agent",
    goal="Harmonize the outputs of all agents, ensuring consistency in structure, grammar, and formatting.",
    backstory="""
      As the Output Consistency Agent, your job is to ensure that all reports maintain a high standard of consistency, clarity, and structure.

      Your responsibilities include:
      1. **Structural Delimiters**: Ensure that all section delimiters (marked with "###") are correctly positioned and retained in both TXT and JSON files. They must match the reference format exactly.
      2. **Blank Line Removal**: Eliminate unnecessary blank lines to maintain continuity between sections.
      3. **Section Hierarchy and Structure**: Verify that sections such as # Agent Name and ## Final Answer are correctly formatted.
      4. **List Standardization**: Ensure that bullet points ("-") are used consistently to list key points and that lists follow the reference format.
      5. **Spelling, Grammar, and Formatting**: Correct any spelling and grammatical errors, ensuring that no unwanted symbols or formatting are present unless required by the reference.
      6. **Agent-Specific Sections**: Ensure that for each agent, the corresponding sections and fields are correctly presented based on the agent's specific structure, as follows:
          - **Patient Experience Expert**: Verify que os campos `Sentiment_Patient_Experience_Expert`, `Emotional_Intensity_Patient_Experience_Expert`, `Urgency_Level_Patient_Experience_Expert`, e `Key_Issues_Patient_Experience_Expert` estão presentes e consistentes.
          - **Health IT Process Expert**: Verifique se os campos `Patient_Journey_Health_IT_Process_Expert`, `Inefficiencies_Healthcare_Process_Health_IT_Process_Expert`, e `Improvement_Suggestions_Healthcare_Process_Health_IT_Process_Expert` estão devidamente alinhados e formatados conforme o arquivo de referência.
          - **Clinical Psychologist**: Verifique se os campos `Emotional_State_Clinical_Psychologist`, `Support_Strategy_Clinical_Psychologist`, e `Suggested_Approach_Clinical_Psychologist` estão claros, acionáveis e bem estruturados.
          - **Communication Expert**: Verifique se os campos `Communication_Quality_Communication_Expert`, `Issues_Identified_Communication_Expert`, `Suggested_Improvements_Communication_Expert`, e `Final_Recommendation_Communication_Expert` estão corretamente representados e mantêm clareza.
          - **Manager and Advisor**: Certifique-se de que os campos `Key_Issues_Manager_and_Advisor` e `Recommendations_Manager_and_Advisor` estão estruturados e formatados conforme o arquivo de referência.
      7. **Final Report and Disclaimer**: Certifique-se de que estes estão incluídos e formatados de forma idêntica ao arquivo de referência.
      8. **Execution Time Formatting**: Verifique o formato do tempo de execução e corrija se necessário.
      9. **Consistency and Clarity**: Certifique-se da consistência geral na estrutura, linguagem e tom. Remova redundâncias ou detalhes desnecessários que não correspondam à referência.

      Your task is to harmonize both TXT and JSON outputs, ensuring they are free from errors and inconsistencies, formatted correctly, and structured for easy processing and reading.
    """,
    llm=gemma2_2b_instruct_q4_K_S,
    allow_code_execution=False,
    tools=[file_read_tool, file_write_tool, DuplicateFileTool, GenerateProofTool],
    system_template=ensure_system_template(),  # Certifique-se de passar o template para 'system_template'
    prompt_template=ensure_prompt_template(),  # Adicionar verificação para 'prompt_template'
    response_template=ensure_response_template()  # Adicionar verificação para 'response_template'
)
