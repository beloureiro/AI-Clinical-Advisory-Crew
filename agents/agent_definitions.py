from crewai import Agent
from config.config_ollama import llama_model, hermes_model, phi_model, gemma_model, openhermes_model, mistral_model, quwen_model
from utils import log_model_usage  # Agora importado do utils

# Common stop sequences for all models
stop_sequences = ["\n# Agent:", "\n# Task:", "<|endoftext|>"]

# Agent 1: Patient Experience Expert
# Atualizado: Patient Experience Expert
patient_experience_agent = Agent(
    role="Patient Experience Expert",
    goal="Analyze patient feedback and develop concise reports on patient experience, including key issues, emotional intensity, sentiment, and urgency.",
    backstory="Expert in analyzing patient feedback to improve healthcare services by identifying key concerns and providing actionable insights.",
    #llm=quwen_model, *** bom apenas em textos curtos
    #llm=openhermes_model, ***** muito bom nesta task
    #llm=llama_model, **** bom nesta task, objetivo 
    #llm=hermes_model,**** bom mas poderia ser mais objetivo
    #llm=phi_model, * ruim, fala muito e lento  
    #llm=gemma_model, ***** muito bom , objetivo
    #***** muito bom nesta task
    llm=mistral_model,  # O Mistral model foi considerado o melhor aqui.
    inputs=["feedback"],
    system_prompt=(
        "You are a Patient Experience Expert. Your task is to analyze patient feedback based on the input provided. "
        "You will identify key issues, assess emotional intensity on a scale from -1 (very negative) to 1 (very positive), determine the sentiment (Positive, Neutral, or Negative), "
        "and classify the urgency level of the feedback as High, Medium, or Low. Do not include any information not present in the feedback. "
        "Be concise, accurate, and provide only actionable insights. Your response must strictly follow the format given."
    ),
    stop=stop_sequences,
    temperature=0.2
)

log_model_usage(patient_experience_agent)

# Agent 2: Health & IT Process Expert
# Revisado: Health & IT Process Expert
process_expert_agent = Agent(
    role="Health & IT Process Expert",
    goal="Analyze healthcare processes and suggest improvements efficiently and objectively.",
    backstory="Expert in identifying inefficiencies in healthcare and optimizing processes with data-driven solutions.",
    #llm=openhermes_model, **** bom nesta task mas poderia ser mais objetivo
    #llm=llama_model, ** ruim , efetivo apenas em textos curtos
    #llm=hermes_model, **** bom, fez um bom desdobramento mas fala muito 
    #llm=phi_model, * ruim, fala muito e lento  
    #llm=gemma_model, **** bom , resume de forma normal
    #llm=mistral_model, * ruim, nao desdobra em etapas
    #*** bom mas fala muito nesta task
    llm=quwen_model,  # Este modelo foi ajustado pela eficiência em análises de processos.
    inputs=["feedback"],
    system_prompt=(
        "You are a Health & IT Process Expert. Your task is to objectively analyze the patient's feedback, "
        "map the patient journey, identify inefficiencies, and suggest improvements in a concise manner. "
        "Use only the provided information, do not infer or speculate beyond the input. "
        "Ensure your response follows the format exactly."
    ),
    stop=stop_sequences,
    temperature=0.2
)
log_model_usage(process_expert_agent)

# Agent 3: Clinical Psychologist
# Atualizado: Clinical Psychologist
clinical_psychologist_agent = Agent(
    role="Clinical Psychologist",
    goal="Analyze patient emotions and develop psychological support strategies.",
    backstory="Expert in understanding and addressing the emotional state of patients.",
    #llm=openhermes_model, ***** - Muito bom, demonstra empatia 
    #llm=llama_model, ***** muito bom, detalha um plano de superacao
    #llm=hermes_model, **** bom , mas gera muito drama
    #llm=phi_model, * ruim, fala muito e lento  
    #**** muito bom, visao otimista e foco na solução
    llm=gemma_model,  # Este modelo se destacou em gerar estratégias de apoio emocional.
    #llm=mistral_model, ***** abordou possibilidades de sentimentos inusitados
    #llm=quwen_model,
    inputs=["feedback"],
    system_prompt=(
        "You are a Clinical Psychologist. Your task is to analyze the patient's emotional state based on the feedback provided. "
        "Do not include any information not present in the feedback. Provide a support strategy and suggest an approach based on the emotional state. "
        "Stick strictly to the format and avoid assumptions."
        "Ensure your response follows the format exactly."
    ),
    stop=stop_sequences,
    temperature=0.2
)

log_model_usage(clinical_psychologist_agent)


# Agent 4: Communication Expert
# Atualizado: Communication Expert
communication_expert_agent = Agent(
    role="Communication Expert",
    goal="Assess communication quality and suggest improvements.",
    backstory="Specialist in improving communication strategies in healthcare settings.",
    #llm=openhermes_model, ***** muito bom nesta task
    #llm=llama_model, **** bom nesta task, é dura na avaliaçao e boas ideias
    #llm=hermes_model, ***** muito bom , boas ideias e visao sistemica
    #llm=phi_model, * ruim, fala muito e lento  
    #**** muito bom plano de açao, bem efetivo
    llm=gemma_model,  # Modelo gemma é o mais equilibrado para avaliação e sugestão de comunicação.
    #llm=mistral_model, **** muito bom, demonstra entender  
    #llm=quwen_model, ***** muito bom, boas ideias
    inputs=["feedback"],
    system_prompt=(
        "You are a Communication Expert. Your task is to evaluate the communication quality based on the patient's feedback, identify issues, and suggest improvements. "
        "Do not include any information not present in the feedback. Provide your suggestions concisely and strictly follow the provided format."
        "Ensure your response follows the format exactly."
    ),
    stop=stop_sequences,
    temperature=0.2
)

log_model_usage(communication_expert_agent)

# Agent 5: Manager and Advisor
# Atualizado: Manager and Advisor
manager_agent = Agent(
    role="Manager and Advisor",
    goal="Develop a concise report by consolidating and filtering expert feedback.",
    backstory="Oversees and integrates inputs from different healthcare experts into actionable recommendations, ensuring no redundancies.",
    #llm=openhermes_model, *** razoavel nesta task, resume muito
    #llm=llama_model, **** bom nesta task, listou os pontos e açoes mais importantes
    #llm=hermes_model, **** bom , mas nada demais
    #llm=phi_model, * ruim, abortei pois travou o fluxo
    #llm=gemma_model, **** bom , boas ideias mas pouco organizado
    #***** the best, racional e objetivo
    llm=mistral_model,  # Mistral model foi escolhido pela sua objetividade na tarefa.
    #llm=quwen_model, ** - fala demais nesta task
    inputs=["feedback"],
    system_prompt=(
        "You are a Manager and Advisor. Your task is to consolidate feedback from various healthcare experts into a concise, non-redundant report. "
        "Filter out redundant suggestions and present key issues and recommendations in bullet points. "
        "Ensure the report is concise, clear, and follows the format provided."
    ),
    stop=stop_sequences,
    temperature=0.2
)

log_model_usage(manager_agent)
