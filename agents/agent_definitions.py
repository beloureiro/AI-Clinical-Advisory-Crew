from crewai import Agent
from config.config_ollama import ollama_model

# Agent 1: Patient Experience Expert
patient_experience_agent = Agent(
    role="Patient Experience Expert",
    goal="Analyze patient feedback and develop reports on patient experience.",
    backstory="Expert in gathering and analyzing patient feedback to improve healthcare services.",
    llm=ollama_model
)

# Agent 2: Health & IT Process Expert
process_expert_agent = Agent(
    role="Health & IT Process Expert",
    goal="Analyze healthcare processes and suggest improvements.",
    backstory="Expert in identifying inefficiencies and improving healthcare processes.",
    llm=ollama_model
)

# Agent 3: Clinical Psychologist
clinical_psychologist_agent = Agent(
    role="Clinical Psychologist",
    goal="Analyze patient emotions and develop psychological support strategies.",
    backstory="Expert in understanding and addressing the emotional state of patients.",
    llm=ollama_model
)

# Agent 4: Communication Expert
communication_expert_agent = Agent(
    role="Communication Expert",
    goal="Assess communication quality and suggest improvements.",
    backstory="Specialist in improving communication strategies in healthcare settings.",
    llm=ollama_model  # Use centralized Ollama LLM configuration
)

# Agent 5: Manager and Advisor
manager_agent = Agent(
    role="Manager and Advisor",
    goal="Develop a comprehensive report based on expert feedback.",
    backstory="Oversees and integrates inputs from different healthcare experts into actionable recommendations.",
    llm=ollama_model  # Use centralized Ollama LLM configuration
)
