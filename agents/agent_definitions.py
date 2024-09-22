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
    llm=quwen_model,  # Ensure this model is properly referenced
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
    llm=llama_model,  # Ensure this model is properly referenced
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
    llm=hermes_model,  # Ensure this model is properly referenced
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
    llm=openhermes_model,  # Ensure this model is properly referenced
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
    goal="Develop a comprehensive report based on expert feedback.",
    backstory="Oversees and integrates inputs from different healthcare experts into actionable recommendations.",
    llm=quwen_model,  # Ensure this model is properly referenced
    inputs=["feedback"],
    system_prompt=(
        "You are a Manager and Advisor. Integrate the expert feedback strictly based on the patient feedback. "
        "Do not include any information that is not present in the feedback. "
        "Do not add any external information, make assumptions, or infer beyond the given input."
    ),
    stop=stop_sequences,
    temperature=0.2
)
log_model_usage(manager_agent)
