from crewai import Task

# Agent 1 Tasks: Patient Experience Expert
collect_feedback_task = Task(
    description="Collect and analyze patient feedback",
    expected_output="Classified patient feedback with urgency and emotional intensity."
)

classify_emotional_intensity_task = Task(
    description="Classify feedback on a scale of -1 to 1 based on emotional intensity",
    expected_output="Classified feedback with emotional intensity ratings."
)

classify_sentiment_task = Task(
    description="Classify feedback as Positive/Neutral/Negative",
    expected_output="Classified feedback by sentiment."
)

classify_negative_urgency_task = Task(
    description="Classify negative feedbacks with urgency levels (High/Medium)",
    expected_output="Negative feedbacks classified by urgency."
)

# Agent 2 Tasks: Health & IT Process Expert
map_patient_journey_task = Task(
    description="Map patient journey and identify involved process stages",
    expected_output="Identified process stages and inefficiencies."
)

identify_inefficiencies_task = Task(
    description="Identify inefficiencies in healthcare process",
    expected_output="List of inefficiencies and improvement suggestions."
)

process_improvement_report_task = Task(
    description="Develop a report with process improvement suggestions",
    expected_output="Comprehensive process improvement report."
)

# Agent 3 Tasks: Clinical Psychologist
analyze_emotional_state_task = Task(
    description="Analyze patient's emotional state based on feedback",
    expected_output="Detailed analysis of emotional state."
)

develop_support_strategies_task = Task(
    description="Develop psychological support strategies for the patient",
    expected_output="Proposed psychological support strategies."
)

propose_approach_task = Task(
    description="Propose an approach to address the emotional impact",
    expected_output="Psychological approach proposal."
)

# Agent 4 Tasks: Communication Expert
analyze_communication_task = Task(
    description="Analyze the quality of communication in the case",
    expected_output="Communication analysis."
)

identify_communication_issues_task = Task(
    description="Identify communication improvement points",
    expected_output="List of communication improvement suggestions."
)

communication_report_task = Task(
    description="Develop a communication improvement report",
    expected_output="Report with communication enhancement strategies."
)

# Agent 5 Tasks: Manager and Advisor
comprehensive_report_task = Task(
    description="Develop a comprehensive report integrating all expert feedback",
    expected_output="Final comprehensive report with recommendations for process improvements, patient experience enhancements, psychological insights, and communication strategies."
)
