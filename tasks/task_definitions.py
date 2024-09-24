from crewai import Task
from agents.agent_definitions import (
    patient_experience_agent, process_expert_agent, clinical_psychologist_agent,
    communication_expert_agent, manager_agent
)

# Agent 1 Tasks: Patient Experience Expert
consolidated_patient_experience_task = Task(
    description=(
        "As a Patient Experience Expert, analyze the following patient feedback and provide the information in the specified format:\n\n"
        "'{feedback}'\n\n"
        "**Please provide your output in the exact format below, including the keys and colons. "
        "Do not include any additional text, explanations, or introductory sentences.**\n\n"
        "Sentiment_Patient_Experience_Expert: [Positive/Neutral/Negative]\n"
        "Emotional_Intensity_Patient_Experience_Expert: [Score from -1 to 1, where -1 is highly negative and 1 is highly positive]\n"
        "Urgency_Level_Patient_Experience_Expert: [High/Medium/Low]\n"
        "Key_Issues_Patient_Experience_Expert:\n"
        "- [First key issue directly from feedback]\n"
        "- [Second key issue if applicable]"
    ),
    expected_output=(
        "Sentiment_Patient_Experience_Expert: [Positive/Neutral/Negative]\n"
        "Emotional_Intensity_Patient_Experience_Expert: [Numeric score from -1 to 1]\n"
        "Urgency_Level_Patient_Experience_Expert: [High/Medium/Low]\n"
        "Key_Issues_Patient_Experience_Expert:\n"
        "- [Key issue]\n"
        "- [Another key issue if applicable]"
    ),
    agent=patient_experience_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="text",
    max_tokens=150
)

# Agent 2 Tasks: Health & IT Process Expert
# Revisado: Health & IT Process Expert com BPMN
consolidated_process_task = Task(
    description=(
        "As a Health & IT Process Expert with expertise in Business Process Model and Notation (BPMN), analyze the following patient feedback, map the patient's lifecycle, identify inefficiencies, "
        "and suggest improvements from all stakeholder perspectives, including IT systems:\n\n"
        "'{feedback}'\n\n"
        "**Please provide your output in the exact format below, using bullet points (`-`) for lists. "
        "Do not use numbered lists or include any additional text, explanations, or sections.**\n\n"
        "Patient_Journey_Health_IT_Process_Expert:\n"
        "- [First step in the patient's journey]\n"
        "- [Second step]\n"
        "- [Additional steps if applicable]\n"
        "Inefficiencies_Healthcare_Process_Health_IT_Process_Expert:\n"
        "- [First inefficiency]\n"
        "- [Second inefficiency]\n"
        "- [Additional inefficiencies if applicable]\n"
        "Improvement_Suggestions_Healthcare_Process_Health_IT_Process_Expert:\n"
        "- [First suggestion]\n"
        "- [Second suggestion]\n"
        "- [Additional suggestions if applicable]"
    ),
    expected_output=(
        "Patient_Journey_Health_IT_Process_Expert:\n"
        "- [First step]\n"
        "- [Second step]\n"
        "- [Additional steps if applicable]\n"
        "Inefficiencies_Healthcare_Process_Health_IT_Process_Expert:\n"
        "- [First inefficiency]\n"
        "- [Second inefficiency]\n"
        "- [Additional inefficiencies]\n"
        "Improvement_Suggestions_Healthcare_Process_Health_IT_Process_Expert:\n"
        "- [First improvement]\n"
        "- [Second improvement]\n"
        "- [Additional improvements]"
    ),
    agent=process_expert_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="text",
    max_tokens=300
)

# Agent 3 Tasks: Clinical Psychologist
consolidated_clinical_psychologist_task = Task(
    description=(
        "As a Clinical Psychologist, analyze the patient's emotional state based on the feedback, develop a tailored psychological support strategy, and propose an approach to address the emotional impact:\n\n"
        "'{feedback}'\n\n"
        "**Please provide your output in the exact format below, including the keys and colons. "
        "Do not include any additional text or explanations.**\n\n"
        "Emotional_State_Clinical_Psychologist: [Describe the emotional state]\n"
        "Support_Strategy_Clinical_Psychologist: [Describe the support strategy]\n"
        "Suggested_Approach_Clinical_Psychologist:\n"
        "- [First approach step]\n"
        "- [Second approach step]\n"
        "- [Additional steps if applicable]"
    ),
    expected_output=(
        "Emotional_State_Clinical_Psychologist: [Emotional state]\n"
        "Support_Strategy_Clinical_Psychologist: [Support strategy]\n"
        "Suggested_Approach_Clinical_Psychologist:\n"
        "- [Approach step]\n"
        "- [Another approach step if applicable]"
    ),
    agent=clinical_psychologist_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="text",
    max_tokens=150
)

# Agent 4 Tasks: Communication Expert
consolidated_communication_task = Task(
    description=(
        "As a Communication Expert, evaluate the communication quality based on the patient feedback, identify any issues, and suggest improvements. Provide a final recommendation for improving communication strategies:\n\n"
        "'{feedback}'\n\n"
        "**Please provide your output in the exact format below, including the keys and colons. "
        "Do not include any additional text, explanations, or introductory sentences.**\n\n"
        "Communication_Quality_Communication_Expert: [Excellent/Good/Fair/Poor]\n"
        "Issues_Identified_Communication_Expert:\n"
        "- [First issue identified]\n"
        "- [Second issue if applicable]\n"
        "Suggested_Improvements_Communication_Expert:\n"
        "- [First improvement suggestion]\n"
        "- [Second suggestion if applicable]\n"
        "Final_Recommendation_Communication_Expert: [Overall recommendation]"
    ),
    expected_output=(
        "Communication_Quality_Communication_Expert: [Quality]\n"
        "Issues_Identified_Communication_Expert:\n"
        "- [Issue]\n"
        "- [Another issue if applicable]\n"
        "Suggested_Improvements_Communication_Expert:\n"
        "- [Improvement]\n"
        "- [Another improvement if applicable]\n"
        "Final_Recommendation_Communication_Expert: [Recommendation]"
    ),
    agent=communication_expert_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="text",
    max_tokens=150
)

# Agent 5 Tasks: Manager and Advisor
consolidated_manager_task = Task(
    description=(
        "As a Manager and Advisor, create a concise report by filtering out redundant recommendations from the expert feedback. Summarize the key points in bullet points, with no more than two sentences per item:\n\n"
        "'{feedback}'\n\n"
        "**Please provide your output in the exact format below, including the keys and colons. "
        "Do not include any additional text, explanations, or introductory sentences.**\n\n"
        "Key_Issues_Manager_and_Advisor:\n"
        "- [First key issue from experts]\n"
        "- [Second key issue if applicable]\n"
        "Recommendations_Manager_and_Advisor:\n"
        "- [First recommendation corresponding to key issue]\n"
        "- [Second recommendation if applicable]"
    ),
    expected_output=(
        "Key_Issues_Manager_and_Advisor:\n"
        "- [Issue]\n"
        "- [Another issue if applicable]\n"
        "Recommendations_Manager_and_Advisor:\n"
        "- [Recommendation]\n"
        "- [Another recommendation if applicable]"
    ),
    agent=manager_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="text",
    max_tokens=150
)
