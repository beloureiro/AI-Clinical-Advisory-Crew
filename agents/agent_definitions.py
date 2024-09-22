from crewai import Agent
from config.config_ollama import llama_model, hermes_model, phi_model, gemma_model, openhermes_model, mistral_model, quwen_model

def log_model_usage(agent):
    model_name = agent.llm if agent.llm else "Unknown Model"
    print(f"Initialized Agent: '{agent.role}', using model: '{model_name}'")

# Common stop sequences for all models
stop_sequences = ["\n# Agent:", "\n# Task:", "<|endoftext|>"]

# Agent 1: Patient Experience Expert
patient_experience_agent = Agent(
    role="Patient Experience Expert",
    goal="Analyze patient feedback and develop reports on patient experience.",
    backstory="Expert in gathering and analyzing patient feedback to improve healthcare services.",
    llm=quwen_model,  # Ensure this model is properly referenced
    inputs=["feedback"],
    system_prompt=(
        "You are a Patient Experience Expert. Analyze the patient's feedback strictly based on the input provided. "
        "Do not include any information that is not present in the feedback. "
        "Do not add any external information, make assumptions, or infer beyond the given input."
    ),
    stop=stop_sequences,
    temperature=0.2
)
log_model_usage(patient_experience_agent)

# Agent 2: Health & IT Process Expert
process_expert_agent = Agent(
    role="Health & IT Process Expert",
    goal="Analyze healthcare processes and suggest improvements.",
    backstory="Expert in identifying inefficiencies and improving healthcare processes.",
    llm=llama_model,  # Ensure this model is properly referenced
    inputs=["feedback"],
    system_prompt=(
        "You are a Health & IT Process Expert. Analyze the patient's feedback strictly based on the input provided. "
        "Do not include any information that is not present in the feedback. "
        "Do not add any external information, make assumptions, or infer beyond the given input."
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
