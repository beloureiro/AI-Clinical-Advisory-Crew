from config.crew_config import ai_clinical_crew

def get_patient_feedback():
    # Reads the feedback from a text file
    with open("patient_feedback.txt", "r") as file:
        feedback = file.read().strip()
    return feedback

if __name__ == "__main__":
    # Get initial patient feedback from the file
    patient_feedback = get_patient_feedback()
    
    # Assign the feedback to the first agent's task as an input (this step can be expanded based on task design)
    ai_clinical_crew.tasks[0].inputs = {"feedback": patient_feedback}  # Assuming task 0 collects feedback
    
    # Execute the crew
    result = ai_clinical_crew.kickoff()
    print("Execution result:", result)
