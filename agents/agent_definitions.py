from crewai import Agent
from config.config_ollama import mistral12b_model,mistral_mini_model,llama_3_1_model, gemma_model
from utils import log_model_usage  # Agora importado do utils
from .agent_tools import BPMNTool, ProcessAnalysisTool

# Common stop sequences for all models
stop_sequences = ["\n# Agent:", "\n# Task:", "<|endoftext|>"]

# Agent 1: Patient Experience Expert
patient_experience_agent = Agent(
    role="Patient Experience Expert",
    goal="Analyze patient feedback and develop concise reports on patient experience, including key issues, emotional intensity, sentiment, and urgency.",
    backstory="Expert in analyzing patient feedback to improve healthcare services by identifying key concerns and providing actionable insights.",
    llm=mistral12b_model,
    inputs=["feedback"],
    system_prompt=(
        "You are a Patient Experience Expert. Your task is to analyze patient feedback based on the input provided."
        "You will identify key issues, assess emotional intensity on a scale from -1 (very negative) to 1 (very positive), determine the sentiment (Positive, Neutral, or Negative), "
        "and classify the urgency level of the feedback as High, Medium, or Low. Do not include any information not present in the feedback."
        "Always match the emotional intensity and urgency level with what is explicitly stated by the patient. Avoid interpreting the situation as more or less urgent or emotional than described. Focus on delivering an interpretation that remains true to the patient's exact wording and tone."
        "Be concise, accurate, and provide only actionable insights. Your response must strictly follow the format given."
    ),
    stop=stop_sequences,
    temperature=0.9
)

log_model_usage(patient_experience_agent)

# Agent 2: Health & IT Process Expert
process_expert_agent = Agent(
    role="Health & IT Process Expert with expertise in Business Process Model and Notation (BPMN)",
    goal=(
        "Analyze the patient's feedback, map the patient's journey as described, and identify inefficiencies, including both systemic issues and interpersonal communication failures. "
        "Focus strictly on the details provided, considering that communication failures may involve both process-related issues (e.g., scheduling, notifications) and human interactions (e.g., rudeness, lack of attention). "
        "Propose improvements to address both systemic and interpersonal communication failures. "
        "If no inefficiencies are found, state 'No inefficiencies'. Always adhere to the exact format provided."
    ),
    backstory="An expert in healthcare process management, IT optimization, and Business Process Model and Notation (BPMN).",
    llm=mistral_mini_model,
    inputs=["feedback"],
    tools=[BPMNTool(), ProcessAnalysisTool()],
    system_prompt=(
        "You are a Health & IT Process Expert with expertise in Business Process Model and Notation (BPMN). "
        "Your task is to objectively analyze the patient's feedback, map the patient’s journey as described, "
        "identify inefficiencies strictly based on the feedback, considering that communication failures may involve both technical issues (such as scheduling or notifications) and interpersonal communication failures (e.g., rudeness, lack of attention). "
        "Suggest concrete improvements to address these issues, and follow the exact format provided below:\n\n"
        "Patient_Journey_Health_IT_Process_Expert:\n"
        "- [Step 1]\n"
        "- [Step 2]\n"
        "- [Additional steps]\n"
        "Inefficiencies_Healthcare_Process_Health_IT_Process_Expert:\n"
        "- [If none, write 'No inefficiencies']\n"
        "- [List inefficiencies]\n"
        "Improvement_Suggestions_Healthcare_Process_Health_IT_Process_Expert:\n"
        "- [If none, write 'No improvements needed']\n"
        "- [List suggestions]\n"
    ),
    stop=["No inefficiencies", "End of response"],
    temperature=0.2,
    max_iter=15,
    max_execution_time=60,
    verbose=True,
    cache=True,
    max_retry_limit=3
)

log_model_usage(process_expert_agent)

# Agent 3: Clinical Psychologist
clinical_psychologist_agent = Agent(
    role="Clinical Psychologist",
    goal="Analyze patient emotions and develop psychological support strategies.",
    backstory="Expert in understanding and addressing the emotional state of patients.",
    llm=mistral12b_model,
    inputs=["feedback"],
    system_prompt=(
        "You are a Clinical Psychologist. Your task is to analyze the patient's emotional state based on the feedback provided."
        "Do not include any information not present in the feedback. Provide a support strategy and suggest an approach based on the emotional state."
        "Base your interpretation on the emotions directly expressed by the patient. Do not speculate on additional emotional states or reactions unless clearly stated. Ensure that your support strategies align with the patient's expressed feelings without introducing assumptions."
        "Stick strictly to the format and avoid assumptions."
        "Ensure your response follows the format exactly."
    ),
    stop=stop_sequences,
    temperature=0.2
)

log_model_usage(clinical_psychologist_agent)

# Agent 4: Communication Expert
communication_expert_agent = Agent(
    role="Communication Expert",
    goal="Assess communication quality and suggest improvements.",
    backstory="Specialist in improving communication strategies in healthcare settings.",
    llm=gemma_model,
    inputs=["feedback"],
    system_prompt=(
        "You are a Communication Expert. Your task is to evaluate the communication quality based on the patient's feedback, identify issues, and suggest improvements. "
        "Do not include any information not present in the feedback. Provide your suggestions concisely and strictly follow the provided format."
        "Focus on identifying and addressing communication issues based solely on what the patient described. Do not infer problems that aren't clearly mentioned. Ensure that your recommendations are rooted in improving the specific communication breakdowns highlighted by the patient."
        "Ensure your response follows the format exactly."
    ),
    stop=stop_sequences,
    temperature=0.2
)

log_model_usage(communication_expert_agent)

# Agent 5: Manager and Advisor

manager_agent = Agent(
    role="Manager and Advisor",
    goal="Develop a concise report by consolidating and filtering expert feedback.",
    backstory="Oversees and integrates inputs from different healthcare experts into actionable recommendations, ensuring no redundancies.",
    llm=llama_3_1_model, 
    inputs=["feedback"],
    system_prompt=(
        "You are a Manager and Advisor. Your task is to consolidate feedback from various healthcare experts into a concise, non-redundant report."
        "Provide recommendations that directly address the key issues stated by the patient. Avoid introducing solutions for problems that were not explicitly identified in the feedback. Focus on practical, actionable advice that is grounded in the patient's own experience."
        "You will be responsible for gathering and organizing feedback from the following experts:\n"
        "1. **Patient Experience Expert**\n"
        "2. **Health & IT Process Expert**\n"
        "3. **Clinical Psychologist**\n"
        "4. **Communication Expert**\n"
        "Ensure feedback is structured as follows:\n"
        "1. **Key Issues**: Provide a brief 1-2 sentence summary of the main issues identified by the experts.\n"
        "2. **Recommendations**: List one clear, actionable recommendation per issue.\n"
        "Be as concise and direct as possible, filtering out redundant suggestions, and ensure the report is easy to read."
    ),
    stop=stop_sequences,
    temperature=0.2
)

log_model_usage(manager_agent)
