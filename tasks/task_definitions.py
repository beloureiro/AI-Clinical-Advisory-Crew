from crewai import Task
from agents.agent_definitions import (
    patient_experience_agent, process_expert_agent, clinical_psychologist_agent, 
    communication_expert_agent, manager_agent
)

# Agent 1 Tasks: Patient Experience Expert
collect_feedback_task = Task(
    description="Analyze patient feedback to identify key issues concisely.",
    expected_output="A brief summary categorizing patient feedback by urgency and emotional intensity.",
    agent=patient_experience_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=200  # Reduced to prevent lengthy responses
)

classify_emotional_intensity_task = Task(
    description="Determine the emotional intensity of the patient feedback on a scale of -1 to 1.",
    expected_output="A concise table correlating feedback points with their emotional intensity ratings.",
    agent=patient_experience_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=200  # Further reduced for better focus
)

classify_sentiment_task = Task(
    description="Identify the sentiment of the patient feedback as Positive, Neutral, or Negative.",
    expected_output="A summary of sentiment classifications with relevant feedback examples.",
    agent=patient_experience_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=200  # Further reduced for better focus
)

classify_negative_urgency_task = Task(
    description="Classify negative feedbacks by urgency levels (High/Medium).",
    expected_output="A concise classification of negative feedback points by urgency.",
    agent=patient_experience_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=200  # Further reduced for better focus
)

# Agent 2 Tasks: Health & IT Process Expert
map_patient_journey_task = Task(
    description="Map the patient journey and highlight key process stages based on feedback.",
    expected_output="A brief list outlining the patient journey with identified inefficiencies.",
    agent=process_expert_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=200  # Reduced to avoid excessive details
)

identify_inefficiencies_task = Task(
    description="Identify and list inefficiencies in the healthcare process from patient feedback.",
    expected_output="A concise list of inefficiencies with suggested improvements.",
    agent=process_expert_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=200  # Reduced for better focus
)

process_improvement_report_task = Task(
    description="Create a brief report with process improvement suggestions based on identified inefficiencies.",
    expected_output="A short process improvement report highlighting key recommendations.",
    agent=process_expert_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=200  # Moderate to maintain conciseness
)

# Agent 3 Tasks: Clinical Psychologist
analyze_emotional_state_task = Task(
    description="Analyze the patient's emotional state based on their feedback.",
    expected_output="Targeted psychological insights derived from patient feedback presented concisely.",
    agent=clinical_psychologist_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=200  # Reduced for better focus
)

develop_support_strategies_task = Task(
    description="Develop psychological support strategies tailored to the patient's emotional state.",
    expected_output="Specific and actionable psychological support strategies.",
    agent=clinical_psychologist_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=200  # Reduced for better focus
)

propose_approach_task = Task(
    description="Propose a concise approach to address the emotional impact identified in patient feedback.",
    expected_output="A strategic and succinct approach to mitigate negative emotional impacts.",
    agent=clinical_psychologist_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=200  # Reduced for better focus
)

# Agent 4 Tasks: Communication Expert
analyze_communication_task = Task(
    description="Evaluate the quality of communication based on patient feedback.",
    expected_output="A brief evaluation highlighting key areas for communication improvement.",
    agent=communication_expert_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=200  # Reduced to prevent excessive details
)

identify_communication_issues_task = Task(
    description="Identify communication improvement points from patient feedback.",
    expected_output="A concise list of communication issues with recommended strategies.",
    agent=communication_expert_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=200  # Reduced for better focus
)

communication_report_task = Task(
    description="Develop a communication improvement report based on identified issues.",
    expected_output="A concise report with actionable communication improvement recommendations.",
    agent=communication_expert_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=200  # Moderate to maintain conciseness
)

# Agent 5 Tasks: Manager and Advisor
comprehensive_report_task = Task(
    description="Create a comprehensive report integrating all expert feedback.",
    expected_output="A final concise report with targeted recommendations for process improvements, patient experience enhancements, psychological insights, and communication strategies.",
    agent=manager_agent,
    inputs={"feedback"},
    force_output=True,
    output_format="markdown",
    max_tokens=300  # Reduced to prevent excessive length
)
