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
    process="sequential",  # Adjust this if you're using a hierarchical process
    memory=True,  # Enable memory to keep context between agents
    verbose=True
)
