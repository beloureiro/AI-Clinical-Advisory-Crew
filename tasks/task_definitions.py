from crewai import Task
from agents.agent_definitions import (
    patient_experience_agent, process_expert_agent, clinical_psychologist_agent,
    communication_expert_agent, manager_agent
)

# Agent 1 Tasks: Patient Experience Expert
consolidated_patient_experience_task = Task(
    description=(
        "Analyze the following patient feedback and provide the information in the specified format:\n\n"
        "'{feedback}'\n\n"
        "Output the following, replacing the placeholders with your findings:\n"
        "Sentiment_Patient_Experience_Expert: [Positive/Neutral/Negative]\n"
        "Emotional_Intensity_Patient_Experience_Expert: [Score from -1 to 1, where -1 is highly negative and 1 is highly positive]\n"
        "Urgency_Level_Patient_Experience_Expert: [High/Medium]\n"
        "Key_Issues_Patient_Experience_Expert:\n"
        "- [Key issue directly from feedback]\n"
        "- [Another key issue if applicable]"
    ),
    expected_output=(
        "Sentiment_Patient_Experience_Expert: [Positive/Neutral/Negative]\n"
        "Emotional_Intensity_Patient_Experience_Expert: [Score from -1 to 1, where -1 is highly negative and 1 is highly positive]\n"
        "Urgency_Level_Patient_Experience_Expert: [High/Medium]\n"
        "Key_Issues_Patient_Experience_Expert:\n"
        "- [Key issue directly from feedback]\n"
        "- [Another key issue if applicable]"
    ),
    agent=patient_experience_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="text",
    max_tokens=100
)

# Agent 2 Tasks: Health & IT Process Expert
consolidated_process_task = Task(
    description=(
        "Analyze the following patient feedback, map the patient's journey, identify inefficiencies, and suggest improvements:\n\n"
        "'{feedback}'\n\n"
        "Output the following, replacing the placeholders with your findings:\n"
        "Patient_Journey_Health_IT_Process_Expert: [Describe the patient's journey]\n"
        "Inefficiencies_Healthcare_Process_Health_IT_Process_Expert:\n"
        "- [Inefficiency identified]\n"
        "- [Another inefficiency if applicable]\n"
        "Improvement_Suggestions_Healthcare_Process_Health_IT_Process_Expert:\n"
        "- [Suggestion based on inefficiencies]\n"
        "- [Another suggestion if applicable]"
    ),
    expected_output=(
        "Patient_Journey_Health_IT_Process_Expert: [Patient's journey]\n"
        "Inefficiencies_Healthcare_Process_Health_IT_Process_Expert:\n"
        "- [Inefficiency]\n"
        "Improvement_Suggestions_Healthcare_Process_Health_IT_Process_Expert:\n"
        "- [Suggestion]"
    ),
    agent=process_expert_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="text",
    max_tokens=100
)

# Agent 3 Tasks: Clinical Psychologist
consolidated_clinical_psychologist_task = Task(
    description=(
        "Analyze the patient's emotional state based on the feedback, develop a tailored psychological support strategy, and propose an approach to address the emotional impact:\n\n"
        "'{feedback}'\n\n"
        "Output the following, replacing the placeholders with your findings:\n"
        "Emotional_State_Clinical_Psychologist: [Emotional state]\n"
        "Support_Strategy_Clinical_Psychologist: [Support strategy]\n"
        "Suggested_Approach_Clinical_Psychologist:\n"
        "- [Approach step 1]\n"
        "- [Approach step 2]"
    ),
    expected_output=(
        "Emotional_State_Clinical_Psychologist: [Emotional state]\n"
        "Support_Strategy_Clinical_Psychologist: [Support strategy]\n"
        "Suggested_Approach_Clinical_Psychologist:\n"
        "- [Approach]"
    ),
    agent=clinical_psychologist_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="text",
    max_tokens=100
)

# Agent 4 Tasks: Communication Expert
consolidated_communication_task = Task(
    description=(
        "Evaluate the communication quality based on the patient feedback, identify any issues, and suggest improvements. Provide a final recommendation for improving communication strategies:\n\n"
        "'{feedback}'\n\n"
        "Output the following, replacing the placeholders with your findings:\n"
        "Communication_Quality_Communication_Expert: [Excellent/Good/Fair/Poor]\n"
        "Issues_Identified_Communication_Expert:\n"
        "- [Issue identified]\n"
        "- [Another issue if applicable]\n"
        "Suggested_Improvements_Communication_Expert:\n"
        "- [Improvement suggestion]\n"
        "- [Another suggestion if applicable]\n"
        "Final_Recommendation_Communication_Expert: [Overall recommendation]"
    ),
    expected_output=(
        "Communication_Quality_Communication_Expert: [Quality]\n"
        "Issues_Identified_Communication_Expert:\n"
        "- [Issue]\n"
        "Suggested_Improvements_Communication_Expert:\n"
        "- [Improvement]\n"
        "Final_Recommendation_Communication_Expert: [Recommendation]"
    ),
    agent=communication_expert_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="text",
    max_tokens=100
)

# Agent 5 Tasks: Manager and Advisor
consolidated_manager_task = Task(
    description=(
        "Create a concise report by filtering out redundant recommendations from the expert feedback. Summarize the key points in bullet points, with no more than two sentences per item:\n\n"
        "'{feedback}'\n\n"
        "Output the following, replacing the placeholders with your findings:\n"
        "Key_Issues_Manager_and_Advisor:\n"
        "- [Key issue from experts]\n"
        "Recommendations_Manager_and_Advisor:\n"
        "- [Recommendation corresponding to key issue]"
    ),
    expected_output=(
        "Key_Issues_Manager_and_Advisor:\n"
        "- [Issue]\n"
        "Recommendations_Manager_and_Advisor:\n"
        "- [Recommendation]"
    ),
    agent=manager_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="text",
    max_tokens=100
)
