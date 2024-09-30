import os
import time
from tqdm import tqdm  # Biblioteca para a barra de progresso
from crewai import Crew
from tasks.task_file_processing import txt_review_task, json_validation_task
from agents.agent_backend import output_consistency_agent

print(os.getcwd())

# Verificar se a função log_all_models existe e é utilizável
try:
    from utils import log_all_models
except ImportError:
    def log_all_models(agents):
        print("Erro: A função 'log_all_models' não foi encontrada. Certifique-se de que ela está definida corretamente no módulo 'utils'.")

# Configuração opcional do embedder (se necessário para tarefas que usam embeddings)
embedder = {
    "provider": "ollama",
    "config": {
        "model": "nomic-embed-text:latest"
    }
}

# Configuração correta do Crew com o agente único
backend_crew = Crew(
    agents=[output_consistency_agent],  # Inclui o agente utilizado nas tarefas
    tasks=[txt_review_task, json_validation_task],
    process="sequential",  # Execução sequencial das tarefas
    memory=True,
    embedder=embedder,
    verbose=True  # Usa Boolean para verbosidade
)

# Função para verificar se o arquivo ou diretório tem as permissões necessárias
def check_permissions(path):
    status = {
        "directory_check": None,
        "permissions_check": None,
        "processing_status": None
    }

    # Verificar se o diretório existe
    print(f"Verificando se o diretório '{path}' existe...")
    if os.path.exists(path):
        print(f"Diretório '{path}' encontrado com sucesso.")
        status['directory_check'] = 'Success'
    else:
        print(f"Erro: O caminho do diretório não existe: {path}")
        status['directory_check'] = 'Failed'
        return status  # Se o diretório não existe, retorna o status imediatamente

    # Verificar permissões de leitura e escrita
    print(f"Verificando permissões para o caminho: {path}")
    if os.access(path, os.R_OK) and os.access(path, os.W_OK):
        print(f"Permissões de leitura e escrita verificadas com sucesso para o diretório '{path}'.")
        status['permissions_check'] = 'Success'
    else:
        print(f"Erro: Permissões insuficientes para o diretório '{path}'.")
        status['permissions_check'] = 'Failed'
        return status  # Se as permissões falharem, retorna o status imediatamente

    # Se tudo passar até aqui, retorne o status com "Success" para permissões e diretório
    return status

# Função para executar o backend crew com logs detalhados e barra de progresso
def execute_backend_crew():
    start_time = time.time()

    # Imprime logs iniciais para a execução do crew
    print("############################")
    print("# Backend File Processing Crew Execution")
    print("############################\n")

    # Log dos modelos LLM usados pelos agentes
    print("LLM Models Used by Agents:\n")
    agents = [output_consistency_agent]
    log_all_models(agents)

    # Inicia a execução das tarefas no crew
    print("Starting task execution...\n")

    try:
        # Caminho do diretório para processar os arquivos
        dir_path = "D:/OneDrive - InMotion - Consulting/AI Projects/AI-Clinical-Advisory-Crew/data_reports_txt/"
        status = check_permissions(dir_path)  # Verificar diretório e permissões

        # Exibir status de verificação do diretório e permissões
        print(f"Status da verificação do diretório: {status['directory_check']}")
        print(f"Status da verificação das permissões: {status['permissions_check']}")
        
        # Se alguma das verificações falhou, não continuar o processamento
        if status['directory_check'] == 'Failed' or status['permissions_check'] == 'Failed':
            print("Falha nas verificações iniciais. Abortando o processo.")
            return

        if os.path.isdir(dir_path):
            print(f"Processing files in directory: {dir_path}")
            status['processing_status'] = 'In Progress'

            # Executa o crew com barra de progresso
            tasks = backend_crew.tasks  # Lista de tarefas que serão executadas
            num_tasks = len(tasks)

            print(f"Número de tarefas encontradas: {num_tasks}")
            with tqdm(total=num_tasks, desc="Executando tarefas do Crew", unit="tarefa") as pbar:
                result = backend_crew.kickoff()  # Inicia o crew

                if result:
                    print("Execução do crew iniciada com sucesso...")
                    # Verificar os atributos disponíveis no resultado
                    print(f"Atributos disponíveis no resultado: {dir(result)}")

                    # Acessar o atributo correto
                    if hasattr(result, 'tasks_output'):
                        task_outputs = result.tasks_output
                    elif hasattr(result, 'outputs'):
                        task_outputs = result.outputs
                    else:
                        print("Erro: O objeto result não possui os atributos 'tasks_output' ou 'outputs'.")
                        status['processing_status'] = 'Failed'
                        return

                    if not task_outputs:
                        print("Nenhuma tarefa foi executada ou produziu saída.")
                        status['processing_status'] = 'Failed'
                        return

                    # Log dos resultados para a saída de cada tarefa
                    for task_output in task_outputs:
                        pbar.update(1)  # Atualiza a barra de progresso a cada tarefa concluída
                        print(f"\nTask: {task_output.task.description}")
                        print(f"Status: {task_output.status}")

                        # Detalhando o status da tarefa
                        if task_output.status == "completed":
                            print(f"Output: {task_output.output}")
                            status['processing_status'] = 'Success'
                        else:
                            print(f"Error: {task_output.error}")
                            # Detalhando o erro
                            if task_output.error:
                                print(f"Detalhes do erro: {task_output.error}")
                                status['processing_status'] = 'Failed'

                else:
                    print("Erro: Nenhuma saída válida encontrada na execução do crew.")
                    status['processing_status'] = 'Failed'
        else:
            raise NotADirectoryError(f"Esperado um diretório, mas foi encontrado um arquivo: {dir_path}")

    except PermissionError as pe:
        print(f"Erro de permissão: {pe}")
        status['processing_status'] = 'Failed'
    except FileNotFoundError as fnf:
        print(f"Erro de arquivo não encontrado: {fnf}")
        status['processing_status'] = 'Failed'
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante a execução: {e}")
        status['processing_status'] = 'Failed'

    # Calcula o tempo total de execução
    end_time = time.time()
    total_duration = end_time - start_time
    print(f"\nTotal Execution Time: {total_duration:.2f} seconds")

    # Exibir status de processamento final
    print(f"Status final do processamento: {status['processing_status']}")

    # Log de conclusão da tarefa
    print("\n############################")
    print("# Task Execution Complete")
    print("############################\n")


if __name__ == "__main__":
    execute_backend_crew()
