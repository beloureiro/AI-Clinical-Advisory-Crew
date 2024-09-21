from crewai import Crew
from agents.agent_definitions import (
    patient_experience_agent, process_expert_agent, clinical_psychologist_agent, 
    communication_expert_agent, manager_agent
)
from tasks.task_definitions import (
    collect_feedback_task, classify_emotional_intensity_task, classify_sentiment_task, 
    classify_negative_urgency_task, map_patient_journey_task, identify_inefficiencies_task,
    process_improvement_report_task, analyze_emotional_state_task, develop_support_strategies_task, 
    propose_approach_task, analyze_communication_task, identify_communication_issues_task, 
    communication_report_task, comprehensive_report_task
)
from config.config_ollama import ollama_model  # Import ollama_model correctly

# Define the embedder as a dictionary, as expected by the Crew class
embedder = {
    "provider": "ollama",
    "config": {
        "model": "llama3.1:8b"  # Match the model you're using with Ollama
    }
}

# Define the crew for AI-Clinical-Advisory-Crew
ai_clinical_crew = Crew(
    agents=[
        patient_experience_agent,
        process_expert_agent,
        clinical_psychologist_agent,
        communication_expert_agent,
        manager_agent
    ],
    tasks=[
        collect_feedback_task,
        classify_emotional_intensity_task,
        classify_sentiment_task,
        classify_negative_urgency_task,
        map_patient_journey_task,
        identify_inefficiencies_task,
        process_improvement_report_task,
        analyze_emotional_state_task,
        develop_support_strategies_task,
        propose_approach_task,
        analyze_communication_task,
        identify_communication_issues_task,
        communication_report_task,
        comprehensive_report_task
    ],
    process="sequential",
    memory=True,
    embedder=embedder,
    verbose=True
)
