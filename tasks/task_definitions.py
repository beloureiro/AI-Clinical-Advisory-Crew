from crewai import Task
from agents.agent_definitions import (
    patient_experience_agent, process_expert_agent, clinical_psychologist_agent,
    communication_expert_agent, manager_agent
)

# Agent 1 Tasks: Patient Experience Expert
# Consolidated task for Patient Experience Expert
consolidated_patient_experience_task = Task(
    description=(
        "Analyze the following patient feedback, and provide the following information:\n\n"
        "'{feedback}'\n\n"
        "1. Identify the key issues in bullet points.\n"
        "2. Classify the emotional intensity on a scale from -1 (very negative) to 1 (very positive).\n"
        "3. Determine the sentiment (Positive, Neutral, or Negative).\n"
        "4. Classify the urgency level of the negative feedback (High or Medium).\n\n"
        "Provide a concise and clear report covering all of the above points."
    ),
    expected_output=(
        "### Consolidated Patient Feedback Analysis\n"
        "* **Key Issues**: \n"
        "  - Issue 1: [Key issue directly from feedback]\n"
        "  - Issue 2: [Another key issue if applicable]\n"
        "* **Emotional Intensity**: [Score from -1 to 1]\n"
        "* **Sentiment**: [Positive/Neutral/Negative]\n"
        "* **Urgency Level**: [High/Medium]"
    ),
    agent=patient_experience_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=100  # Ajuste conforme necessário
)

# Agent 2 Tasks: Health & IT Process Expert
# Consolidated Task for Health & IT Process Expert
consolidated_process_task = Task(
    description=(
        "Analyze the following patient feedback, map the patient's journey, identify inefficiencies, "
        "and suggest improvements:\n\n"
        "'{feedback}'\n\n"
        "Provide your findings including:\n"
        "1. Key stages in the patient's journey.\n"
        "2. Inefficiencies in the healthcare process.\n"
        "3. Recommendations for process improvements."
    ),
    expected_output=(
        "### Consolidated Healthcare Process Analysis\n"
        "* Patient Journey: [Stage from feedback]\n"
        "* Inefficiencies: [Inefficiency from feedback]\n"
        "* Improvement Suggestions: [Recommendations based on inefficiencies]"
    ),
    agent=process_expert_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=100
)

# Agent 3 Tasks: Clinical Psychologist
# New consolidated task for Clinical Psychologist
consolidated_clinical_psychologist_task = Task(
    description=(
        "Analyze the patient's emotional state based on the feedback, develop a tailored psychological support strategy, "
        "and propose an approach to address the emotional impact:\n\n"
        "'{feedback}'\n\n"
        "Provide your analysis including:\n"
        "1. Emotional State.\n"
        "2. Support Strategy.\n"
        "3. Suggested Approach for emotional support."
    ),
    expected_output=(
        "### Consolidated Psychological Support Analysis\n"
        "* Emotional State: [State from feedback]\n"
        "* Support Strategy: [Directly addressing feedback]\n"
        "* Suggested Approach: [Emotional support approach based on feedback]"
    ),
    agent=clinical_psychologist_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=100
)

# Agent 4 Tasks: Communication Expert
# New consolidated task for Communication Expert
consolidated_communication_task = Task(
    description=(
        "Evaluate the communication quality based on the patient feedback, identify any issues, and suggest improvements. "
        "Provide a final recommendation for improving communication strategies:\n\n"
        "'{feedback}'\n\n"
        "Provide your findings including:\n"
        "1. Communication Quality Evaluation.\n"
        "2. Identified Issues.\n"
        "3. Suggested Improvements."
    ),
    expected_output=(
        "### Consolidated Communication Report\n"
        "* Communication Quality: [From feedback]\n"
        "* Issues Identified: [Issues]\n"
        "* Suggested Improvements: [Suggestions based on feedback]\n"
        "* Final Recommendation: [Recommendations for improvement]"
    ),
    agent=communication_expert_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=100
)

# Agent 5 Tasks: Manager and Advisor
# New task for Manager and Advisor to consolidate and remove redundancy
consolidated_manager_task = Task(
    description=(
        "Create a concise report by filtering out redundant recommendations from the expert feedback. "
        "Summarize the key points in bullet points, with no more than two sentences per item:\n\n"
        "'{feedback}'\n\n"
        "Provide the consolidated recommendations, ensuring no redundant items are repeated."
    ),
    expected_output=(
        "### Final Consolidated Report\n"
        "* [Non-redundant recommendations from all agents]"
    ),
    agent=manager_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=100
)
