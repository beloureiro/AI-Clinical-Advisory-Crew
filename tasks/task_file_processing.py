import os
from tqdm import tqdm
from crewai import Task
from crewai_tools import DirectoryReadTool, FileReadTool, FileWriterTool, JSONSearchTool  # Incluindo JSONSearchTool
from agents.agent_backend import output_consistency_agent
from agents.agent_tools.shared_tools import DuplicateFileTool, GenerateProofTool
from agents.agent_backend import ensure_system_template

# Inicializar as Ferramentas com Caminhos Completos
txt_directory_tool = DirectoryReadTool(directory='D:/OneDrive - InMotion - Consulting/AI Projects/AI-Clinical-Advisory-Crew/data_reports_txt/')
json_directory_tool = DirectoryReadTool(directory='D:/OneDrive - InMotion - Consulting/AI Projects/AI-Clinical-Advisory-Crew/data_reports_json/')
file_read_tool = FileReadTool()
file_write_tool = FileWriterTool()
json_tool = JSONSearchTool()  # Ferramenta para ler e manipular JSON

# Ferramentas já instanciadas automaticamente pelo sistema CrewAI
duplicate_file_tool = DuplicateFileTool  # Não precisa instanciar, basta referenciar
generate_proof_tool = GenerateProofTool  # Não precisa instanciar, basta referenciar

# Verificar se o agente tem um prompt_template válido
def ensure_agent_template():
    if output_consistency_agent.prompt_template is None:
        print("Warning: system_template is None, assigning default value.")
        output_consistency_agent.prompt_template = ensure_system_template("Default system template")

# Dicionário para rastrear o status de cada etapa
status_dict = {
    "directory_check": "Success",
    "file_processing": {},  # Aqui você adiciona status por arquivo
    "json_processing": {},
    "cache_hits": 0,
    "total_processed": 0,
    "errors": []
}

# Função para listar e processar arquivos TXT e JSON correspondentes
def process_txt_files():
    print("Iniciando o processamento dos arquivos TXT...")

    # Verifique se os arquivos estão sendo encontrados
    txt_files = txt_directory_tool.read_directory()
    json_files = json_directory_tool.read_directory()

    print(f"Número de arquivos TXT encontrados: {len(txt_files)} - {txt_files}")
    print(f"Número de arquivos JSON encontrados: {len(json_files)} - {json_files}")

    if not txt_files or not json_files:
        print("No matching TXT or JSON files found.")
        return "No matching TXT or JSON files found."

    # Barra de progresso para os arquivos TXT
    with tqdm(total=len(txt_files), desc="Processing TXT files", unit="file") as pbar:
        for txt_file in txt_files:
            # Verificar se é um arquivo .txt
            if not txt_file.endswith('.txt'):
                print(f"Arquivo ignorado (não é TXT): {txt_file}")
                continue

            print(f"Processando arquivo TXT: {txt_file}")

            # Extrair o nome base
            txt_base_name = os.path.basename(txt_file).replace('.txt', '')
            # Procurar arquivo JSON correspondente
            json_file = next((jf for jf in json_files if txt_base_name == os.path.basename(jf).replace('.json', '')), None)

            if json_file:
                print(f"Arquivo JSON correspondente encontrado: {json_file}")
                result_txt = process_single_txt_file(txt_file)
                print(f"Resultado do processamento TXT: {result_txt}")
                result_json = process_single_json_file(json_file, txt_file)
                print(f"Resultado do processamento JSON: {result_json}")
                status_dict["file_processing"][txt_file] = "Success"
                status_dict["json_processing"][json_file] = "Success"
            else:
                print(f"Nenhum arquivo JSON correspondente encontrado para {txt_file}")
                status_dict["file_processing"][txt_file] = "Failed"

            status_dict["total_processed"] += 1
            pbar.update(1)

    print("Processamento concluído.")
    return "Processamento completo."


# Função para processar arquivos TXT
def process_single_txt_file(txt_file):
    formatted_file_path = txt_file.replace('data_reports_txt', 'data_processed/txt_formatted').replace('.txt', '_formatted.txt')
    
    print(f"Verificando cache para o arquivo formatado {formatted_file_path}...")
    if os.path.exists(formatted_file_path):
        status_dict["cache_hits"] += 1
        return f"Cache hit: Processed file {formatted_file_path} already exists."

    print(f"Duplicando o arquivo TXT: {txt_file} para {formatted_file_path}")
    duplicate_result = duplicate_file_tool._run(txt_file, formatted_file_path)

    if not os.path.exists(formatted_file_path):
        status_dict["file_processing"][txt_file] = "Failed"
        return f"Error: The formatted TXT file {formatted_file_path} was not found after duplication."

    content = file_read_tool._run(file_path=formatted_file_path)
    ensure_agent_template()

    print("Processando conteúdo do arquivo TXT formatado...")
    processed_content = output_consistency_agent.process(content)

    print(f"Salvando conteúdo processado em {formatted_file_path}")
    file_write_tool._run(filename=formatted_file_path, content=processed_content, overwrite=True)
    
    return f"Processed and saved formatted TXT file: {formatted_file_path}"

# Função para processar arquivos JSON sincronizados
def process_single_json_file(json_file, txt_file):
    synced_json_file = json_file.replace('data_reports_json', 'data_processed/json_synced').replace('.json', '_synced.json')

    print(f"Verificando cache para o arquivo JSON sincronizado {synced_json_file}...")
    if os.path.exists(synced_json_file):
        status_dict["cache_hits"] += 1
        return f"Cache hit: Synced JSON file {synced_json_file} already exists."

    print(f"Duplicando o arquivo JSON: {json_file} para {synced_json_file}")
    duplicate_result = duplicate_file_tool._run(json_file, synced_json_file)

    if not os.path.exists(synced_json_file):
        status_dict["json_processing"][json_file] = "Failed"
        return f"Error: The synced JSON file {synced_json_file} was not found after duplication."

    # Lendo o conteúdo do JSON com a ferramenta JSONSearchTool
    json_content = json_tool._run(file_path=synced_json_file)  # Usando JSONSearchTool para ler o JSON
    txt_content = file_read_tool._run(file_path=txt_file)

    ensure_agent_template()

    combined_content = f"TXT Content:\n{txt_content}\n\nJSON Content:\n{json_content}"
    
    print("Processando conteúdo combinado TXT e JSON...")
    updated_json_content = output_consistency_agent.process(combined_content)

    print(f"Salvando conteúdo JSON sincronizado em {synced_json_file}")
    file_write_tool._run(filename=synced_json_file, content=updated_json_content, overwrite=True)

    proof_file_path = synced_json_file.replace('_synced.json', '_proof.json').replace('json_synced', 'json_proof')
    print(f"Gerando arquivo de prova em {proof_file_path}")
    proof_result = generate_proof_tool._run(txt_content, updated_json_content, proof_file_path)

    return f"Processed and saved synced JSON file: {synced_json_file}\n{proof_result}"

# Task 1: Processar Arquivos TXT
txt_review_task = Task(
    description="Review and correct spelling, grammar, and formatting errors in the TXT reports.",
    agent=output_consistency_agent,
    tools=[file_read_tool, file_write_tool, duplicate_file_tool],
    function=process_txt_files,
    expected_output="A clean and well-formatted TXT report."
)

# Task 2: Atualizar Arquivos JSON com Base nos Arquivos TXT Formatados
json_validation_task = Task(
    description="Update JSON files to ensure they are synchronized with the formatted TXT files.",
    agent=output_consistency_agent,
    tools=[file_read_tool, file_write_tool, duplicate_file_tool, generate_proof_tool, json_tool],  # Adicionando json_tool
    function=process_single_json_file,
    expected_output="An updated and synchronized JSON file matching the formatted TXT."
)

# Função Principal de Execução
def run_file_processing():
    print("Executando tarefa de revisão de arquivos TXT...")
    txt_review_task.run()  # Etapa 1: Processar arquivos TXT

    print("Executando tarefa de validação e sincronização de arquivos JSON...")
    json_validation_task.run()  # Etapa 2: Processar arquivos JSON para consistência

    print("Processamento concluído.")
    print(f"Status final: {status_dict}")


if __name__ == "__main__":
    run_file_processing()
