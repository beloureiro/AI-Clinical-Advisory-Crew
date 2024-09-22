from crewai import Task
from agents.agent_definitions import (
    patient_experience_agent, process_expert_agent, clinical_psychologist_agent, 
    communication_expert_agent, manager_agent
)

# Helper function to monitor and enforce token limits and output structure
def truncate_output(response, max_tokens=50):
    words = response.split()
    if len(words) > max_tokens:
        return ' '.join(words[:max_tokens]) + '...'
    return response

def check_for_off_topic(response, feedback):
    # Check if the response contains content not present in the feedback
    feedback_words = set(feedback.lower().split())
    response_words = set(response.lower().split())
    if not response_words.issubset(feedback_words):
        print("Off-topic detected in response.")
    return response

def post_process_response(response, max_tokens, feedback):
    # Truncate the response
    response = truncate_output(response, max_tokens)
    # Check for off-topic content
    response = check_for_off_topic(response, feedback)
    return response

# Agent 1 Tasks: Patient Experience Expert

collect_feedback_task = Task(
    description=(
        "Analyze the patient feedback strictly based on the input provided. "
        "Do not include any information that is not present in the feedback. "
        "List the key issues mentioned using bullet points. Do not exceed 50 tokens."
    ),
    expected_output=(
        "### Key Issues Identified:\n"
        "* Issue 1: [Key issue directly from feedback]\n"
        "* Issue 2: [Another key issue directly from feedback]"
    ),
    agent=patient_experience_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=50,
    post_processing_callback=lambda response: post_process_response(response, max_tokens=50, feedback=feedback)
)

classify_emotional_intensity_task = Task(
    description=(
        "Provide a simple table classifying the emotional intensity of the feedback on a scale from -1 to 1, "
        "strictly based on the input. Do not exceed 50 tokens."
    ),
    expected_output=(
        "### Emotional Intensity\n"
        "| Feedback | Intensity |\n"
        "|---|---|\n"
        "| [Feedback excerpt] | [Intensity score] |"
    ),
    agent=patient_experience_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=50,
    post_processing_callback=lambda response: post_process_response(response, max_tokens=50, feedback=feedback)
)

classify_sentiment_task = Task(
    description=(
        "Classify the sentiment of the patient feedback as Positive, Neutral, or Negative, "
        "strictly based on the input. Use simple language and avoid elaboration."
    ),
    expected_output=(
        "### Sentiment Summary:\n"
        "* Sentiment: [Positive/Negative/Neutral]"
    ),
    agent=patient_experience_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=20,
    post_processing_callback=lambda response: post_process_response(response, max_tokens=20, feedback=feedback)
)

classify_negative_urgency_task = Task(
    description=(
        "Classify the negative feedback by urgency level (High/Medium) based strictly on the input. Be concise."
    ),
    expected_output=(
        "### Negative Feedback Urgency:\n"
        "* Urgency Level: [High/Medium]"
    ),
    agent=patient_experience_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=20,
    post_processing_callback=lambda response: post_process_response(response, max_tokens=20, feedback=feedback)
)

# Agent 2 Tasks: Health & IT Process Expert

map_patient_journey_task = Task(
    description=(
        "Map the patient journey and identify inefficiencies strictly based on the feedback. "
        "Provide concise, structured feedback. Do not include any external information."
    ),
    expected_output=(
        "### Patient Journey Map\n"
        "* Stage 1: [Key stage directly from feedback]\n"
        "* Inefficiency: [Inefficiency directly from feedback]"
    ),
    agent=process_expert_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=70,
    post_processing_callback=lambda response: post_process_response(response, max_tokens=70, feedback=feedback)
)

identify_inefficiencies_task = Task(
    description=(
        "Identify inefficiencies in healthcare processes strictly based on the feedback. Do not exceed 50 tokens."
    ),
    expected_output=(
        "### Healthcare Process Inefficiencies:\n"
        "* Inefficiency 1: [Brief description directly from feedback]"
    ),
    agent=process_expert_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=50,
    post_processing_callback=lambda response: post_process_response(response, max_tokens=50, feedback=feedback)
)

process_improvement_report_task = Task(
    description=(
        "Create a brief process improvement suggestion based on the inefficiencies identified, strictly from the feedback."
    ),
    expected_output=(
        "### Process Improvement Suggestion\n"
        "* Recommendation: [Improvement directly addressing feedback]"
    ),
    agent=process_expert_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=50,
    post_processing_callback=lambda response: post_process_response(response, max_tokens=50, feedback=feedback)
)

# Agent 3 Tasks: Clinical Psychologist

analyze_emotional_state_task = Task(
    description=(
        "Analyze the patient's emotional state strictly from the feedback. Keep it simple and do not infer beyond the input."
    ),
    expected_output=(
        "### Emotional State Analysis\n"
        "* Emotional State: [Emotional state directly from feedback]"
    ),
    agent=clinical_psychologist_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=30,
    post_processing_callback=lambda response: post_process_response(response, max_tokens=30, feedback=feedback)
)

develop_support_strategies_task = Task(
    description=(
        "Develop psychological support strategies tailored to the patient's emotional state, based strictly on the feedback."
    ),
    expected_output=(
        "### Support Strategies\n"
        "* Strategy: [Actionable support directly addressing feedback]"
    ),
    agent=clinical_psychologist_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=50,
    post_processing_callback=lambda response: post_process_response(response, max_tokens=50, feedback=feedback)
)

propose_approach_task = Task(
    description=(
        "Propose a concise approach to address the emotional impact based on the feedback, without adding new information."
    ),
    expected_output=(
        "### Emotional Support Approach\n"
        "* Approach: [Specific approach directly from feedback]"
    ),
    agent=clinical_psychologist_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=40,
    post_processing_callback=lambda response: post_process_response(response, max_tokens=40, feedback=feedback)
)

# Agent 4 Tasks: Communication Expert

analyze_communication_task = Task(
    description=(
        "Evaluate the quality of communication strictly based on patient feedback."
    ),
    expected_output=(
        "### Communication Issues\n"
        "* Issue: [Brief description directly from feedback] -> [Suggested Improvement]"
    ),
    agent=communication_expert_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=60,
    post_processing_callback=lambda response: post_process_response(response, max_tokens=60, feedback=feedback)
)

identify_communication_issues_task = Task(
    description=(
        "Identify communication improvement points from the feedback."
    ),
    expected_output=(
        "### Communication Improvement Points\n"
        "* Issue: [Description directly from feedback] -> [Strategy]"
    ),
    agent=communication_expert_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=60,
    post_processing_callback=lambda response: post_process_response(response, max_tokens=60, feedback=feedback)
)

communication_report_task = Task(
    description=(
        "Develop a communication improvement recommendation based on the feedback."
    ),
    expected_output=(
        "### Communication Recommendation\n"
        "* Recommendation: [Key recommendation directly addressing feedback]"
    ),
    agent=communication_expert_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=50,
    post_processing_callback=lambda response: post_process_response(response, max_tokens=50, feedback=feedback)
)

# Agent 5 Tasks: Manager and Advisor

comprehensive_report_task = Task(
    description=(
        "Create a concise report integrating all expert feedback, strictly based on the patient feedback."
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
    post_processing_callback=lambda response: post_process_response(response, max_tokens=100, feedback=feedback)
)
