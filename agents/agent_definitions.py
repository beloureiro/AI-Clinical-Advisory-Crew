from crewai import Agent
from config.config_ollama import llama_model, hermes_model, phi_model, gemma_model, openhermes_model, mistral_model, quwen_model

def log_model_usage(agent):
    model_name = agent.llm if agent.llm else "Unknown Model"
    print(f"Initialized Agent: '{agent.role}', using model: '{model_name}'")

# Common stop sequences for all models
stop_sequences = ["\n# Agent:", "\n# Task:", "<|endoftext|>"]

# Agent 1: Patient Experience Expert
# Updated Agent: Patient Experience Expert
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
    llm=mistral_model, 
    inputs=["feedback"],
    system_prompt=(
        "You are a Patient Experience Expert. Your task is to analyze patient feedback based on the input provided. "
        "You will identify key issues, assess emotional intensity on a scale from -1 (very negative) to 1 (very positive), determine the sentiment (Positive, Neutral, or Negative), "
        "and classify the urgency level of the feedback as High or Medium. Do not include any information not present in the feedback. "
        "Be concise, accurate, and provide only actionable insights."
    ),
    stop=stop_sequences,
    temperature=0.2
)

log_model_usage(patient_experience_agent)

# Agent 2: Health & IT Process Expert
# Revised Agent 2: Health & IT Process Expert
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
    llm=quwen_model, 
    inputs=["feedback"],
    system_prompt=(
        "You are a Health & IT Process Expert. Your task is to objectively analyze the patient's feedback, "
        "map the patient journey, identify inefficiencies, and suggest improvements in a concise manner. "
        "Only use the information provided. Do not infer or speculate beyond the provided input. "
        "Be concise and direct in your analysis and recommendations."
    ),
    stop=stop_sequences,
    temperature=0.2
)
log_model_usage(process_expert_agent)

# Agent 3: Clinical Psychologist
clinical_psychologist_agent = Agent(
    role="Clinical Psychologist",
    goal="Analyze patient emotions and develop psychological support strategies.",
    backstory="Expert in understanding and addressing the emotional state of patients.",
    #llm=openhermes_model, ***** - Muito bom, demonstra empatia 
    #llm=llama_model, ***** muito bom, detalha um plano de superacao
    #llm=hermes_model, **** bom , mas gera muito drama
    #llm=phi_model, * ruim, fala muito e lento  
    #**** muito bom, visao otimista e foco na solução
    llm=gemma_model, 
    #llm=mistral_model, ***** abordou possibilidades de sentimentos inusitados
    #llm=quwen_model,
    inputs=["feedback"],
    system_prompt=(
        "You are a Clinical Psychologist. Analyze the patient's feedback strictly based on the input provided. "
        "Do not include any information that is not present in the feedback. "
        "Do not add any external information, make assumptions, or infer beyond the given input."
    ),
    stop=stop_sequences,
    temperature=0.2
)

log_model_usage(clinical_psychologist_agent)


# Agent 4: Communication Expert
communication_expert_agent = Agent(
    role="Communication Expert",
    goal="Assess communication quality and suggest improvements.",
    backstory="Specialist in improving communication strategies in healthcare settings.",
    #llm=openhermes_model, ***** muito bom nesta task
    #llm=llama_model, **** bom nesta task, é dura na avaliaçao e boas ideias
    #llm=hermes_model, ***** muito bom , boas ideias e visao sistemica
    #llm=phi_model, * ruim, fala muito e lento  
    #**** muito bom plano de açao, bem efetivo
    llm=gemma_model, 
    #llm=mistral_model, **** muito bom, demonstra entender  
    #llm=quwen_model, ***** muito bom, boas ideias
    inputs=["feedback"],
    system_prompt=(
        "You are a Communication Expert. Analyze the patient's feedback strictly based on the input provided. "
        "Do not include any information that is not present in the feedback. "
        "Do not add any external information, make assumptions, or infer beyond the given input."
    ),
    stop=stop_sequences,
    temperature=0.2
)

log_model_usage(communication_expert_agent)

# Agent 5: Manager and Advisor
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
    llm=mistral_model,  
    #llm=quwen_model, ** - fala demais nesta task
    inputs=["feedback"],
    system_prompt=(
        "You are a Manager and Advisor. Your role is to consolidate expert feedback into a concise, non-redundant report. "
        "Do not introduce new recommendations. Filter out similar suggestions from different agents and summarize the key points in bullet points."
    ),
    stop=stop_sequences,
    temperature=0.2
)
log_model_usage(manager_agent)
