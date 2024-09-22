from crewai import Task
from agents.agent_definitions import (
    patient_experience_agent, process_expert_agent, clinical_psychologist_agent,
    communication_expert_agent, manager_agent
)
from utils import post_process_response  # Importa a função post_process_response do utils

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
    max_tokens=100,  # You may adjust this based on expected output length
    post_processing_callback=lambda response, inputs: post_process_response(
        response, max_tokens=100, inputs=inputs, agent=patient_experience_agent
    )
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
    max_tokens=100,
    post_processing_callback=lambda response, inputs: post_process_response(
        response, max_tokens=100, inputs=inputs, agent=process_expert_agent
    )
)

# Agent 3 Tasks: Clinical Psychologist

analyze_emotional_state_task = Task(
    description=(
        "Analyze the patient's emotional state based on the feedback:\n\n"
        "'{feedback}'"
    ),
    expected_output=(
        "### Emotional State Analysis\n"
        "* Emotional State: [State from feedback]"
    ),
    agent=clinical_psychologist_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=20,
    post_processing_callback=lambda response, inputs: post_process_response(
        response, max_tokens=20, inputs=inputs, agent=clinical_psychologist_agent
    )
)

develop_support_strategies_task = Task(
    description=(
        "Develop a psychological support strategy tailored to the patient's emotional state:\n\n"
        "'{feedback}'"
    ),
    expected_output=(
        "### Support Strategy\n"
        "* Strategy: [Directly addressing feedback]"
    ),
    agent=clinical_psychologist_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=40,
    post_processing_callback=lambda response, inputs: post_process_response(
        response, max_tokens=40, inputs=inputs, agent=clinical_psychologist_agent
    )
)

propose_approach_task = Task(
    description=(
        "Propose an approach to address the emotional impact based on the feedback:\n\n"
        "'{feedback}'"
    ),
    expected_output=(
        "### Emotional Support Approach\n"
        "* Approach: [From feedback]"
    ),
    agent=clinical_psychologist_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=30,
    post_processing_callback=lambda response, inputs: post_process_response(
        response, max_tokens=30, inputs=inputs, agent=clinical_psychologist_agent
    )
)

# Agent 4 Tasks: Communication Expert

analyze_communication_task = Task(
    description=(
        "Evaluate the communication quality based on the patient feedback:\n\n"
        "'{feedback}'"
    ),
    expected_output=(
        "### Communication Evaluation\n"
        "* Issue: [From feedback]"
    ),
    agent=communication_expert_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=30,
    post_processing_callback=lambda response, inputs: post_process_response(
        response, max_tokens=30, inputs=inputs, agent=communication_expert_agent
    )
)

identify_communication_issues_task = Task(
    description=(
        "Identify communication issues and suggest improvements based on the feedback:\n\n"
        "'{feedback}'"
    ),
    expected_output=(
        "### Communication Improvement Points\n"
        "* Issue: [From feedback] -> Improvement: [Suggestion]"
    ),
    agent=communication_expert_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=50,
    post_processing_callback=lambda response, inputs: post_process_response(
        response, max_tokens=50, inputs=inputs, agent=communication_expert_agent
    )
)

communication_report_task = Task(
    description=(
        "Provide a communication improvement recommendation based on the feedback:\n\n"
        "'{feedback}'"
    ),
    expected_output=(
        "### Communication Recommendation\n"
        "* Recommendation: [Directly addressing feedback]"
    ),
    agent=communication_expert_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=40,
    post_processing_callback=lambda response, inputs: post_process_response(
        response, max_tokens=40, inputs=inputs, agent=communication_expert_agent
    )
)

# Agent 5 Tasks: Manager and Advisor

comprehensive_report_task = Task(
    description=(
        "Create a concise report integrating all expert feedback based on the patient feedback:\n\n"
        "'{feedback}'"
    ),
    expected_output=(
        "### Final Report\n"
        "* [Top recommendations from each agent directly addressing feedback]"
    ),
    agent=manager_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=100,
    post_processing_callback=lambda response, inputs: post_process_response(
        response, max_tokens=100, inputs=inputs, agent=manager_agent
    )
)
