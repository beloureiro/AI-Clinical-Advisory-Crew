from config.crew_config import ai_clinical_crew

def get_patient_feedback():
    # Reads the feedback from a text file
    with open("patient_feedback.txt", "r") as file:
        feedback = file.read().strip()
    return feedback

if __name__ == "__main__":
    # Get initial patient feedback from the file
    patient_feedback = get_patient_feedback()

    # Execute the crew and pass the feedback as input to the tasks
    result = ai_clinical_crew.kickoff(inputs={"feedback": patient_feedback})

    # Print the result of the execution
    print("Execution result:", result)
