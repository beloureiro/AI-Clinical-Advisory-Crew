from crewai import Task
from agents.agent_definitions import (
    patient_experience_agent, process_expert_agent, clinical_psychologist_agent,
    communication_expert_agent, manager_agent
)
from utils import post_process_response  # Importa a função post_process_response do utils

# Agent 1 Tasks: Patient Experience Expert

collect_feedback_task = Task(
    description=(
        "Based on the following patient feedback, identify the key issues:\n\n"
        "'{feedback}'\n\n"
        "List the issues using bullet points."
    ),
    expected_output=(
        "### Key Issues Identified:\n"
        "* Issue 1: [Key issue directly from feedback]"
    ),
    agent=patient_experience_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=50,
    post_processing_callback=lambda response, inputs: post_process_response(
        response, max_tokens=50, inputs=inputs, agent=patient_experience_agent
    )
)

classify_emotional_intensity_task = Task(
    description=(
        "Classify the emotional intensity of the following feedback on a scale from -1 to 1:\n\n"
        "'{feedback}'\n\n"
        "Provide the intensity score."
    ),
    expected_output=(
        "### Emotional Intensity\n"
        "* Intensity Score: [Score]"
    ),
    agent=patient_experience_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=20,
    post_processing_callback=lambda response, inputs: post_process_response(
        response, max_tokens=20, inputs=inputs, agent=patient_experience_agent
    )
)

classify_sentiment_task = Task(
    description=(
        "Determine the sentiment of the following feedback (Positive, Neutral, or Negative):\n\n"
        "'{feedback}'"
    ),
    expected_output=(
        "### Sentiment Summary:\n"
        "* Sentiment: [Positive/Negative/Neutral]"
    ),
    agent=patient_experience_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=10,
    post_processing_callback=lambda response, inputs: post_process_response(
        response, max_tokens=10, inputs=inputs, agent=patient_experience_agent
    )
)

classify_negative_urgency_task = Task(
    description=(
        "Classify the urgency level of the negative feedback (High or Medium):\n\n"
        "'{feedback}'"
    ),
    expected_output=(
        "### Negative Feedback Urgency:\n"
        "* Urgency Level: [High/Medium]"
    ),
    agent=patient_experience_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=10,
    post_processing_callback=lambda response, inputs: post_process_response(
        response, max_tokens=10, inputs=inputs, agent=patient_experience_agent
    )
)

# Agent 2 Tasks: Health & IT Process Expert

map_patient_journey_task = Task(
    description=(
        "Outline the patient's journey and identify any inefficiencies based on the feedback:\n\n"
        "'{feedback}'\n\n"
        "Provide your findings."
    ),
    expected_output=(
        "### Patient Journey Map\n"
        "* Stage: [Stage from feedback]\n"
        "* Inefficiency: [Inefficiency from feedback]"
    ),
    agent=process_expert_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=50,
    post_processing_callback=lambda response, inputs: post_process_response(
        response, max_tokens=50, inputs=inputs, agent=process_expert_agent
    )
)

identify_inefficiencies_task = Task(
    description=(
        "Identify inefficiencies in the healthcare process based on the feedback:\n\n"
        "'{feedback}'"
    ),
    expected_output=(
        "### Healthcare Process Inefficiencies:\n"
        "* Inefficiency: [Description from feedback]"
    ),
    agent=process_expert_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=30,
    post_processing_callback=lambda response, inputs: post_process_response(
        response, max_tokens=30, inputs=inputs, agent=process_expert_agent
    )
)

process_improvement_report_task = Task(
    description=(
        "Suggest a process improvement based on the identified inefficiencies:\n\n"
        "'{feedback}'"
    ),
    expected_output=(
        "### Process Improvement Suggestion\n"
        "* Recommendation: [Directly addressing feedback]"
    ),
    agent=process_expert_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=40,
    post_processing_callback=lambda response, inputs: post_process_response(
        response, max_tokens=40, inputs=inputs, agent=process_expert_agent
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
