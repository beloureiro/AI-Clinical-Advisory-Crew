from config.crew_config import ai_clinical_crew

def get_patient_feedback():
    # Read feedback from a text file
    with open("patient_feedback.txt", "r") as file:
        feedback = file.read().strip()
    return feedback

if __name__ == "__main__":
    # Get the initial patient feedback
    patient_feedback = get_patient_feedback()
    print(f"Patient Feedback: {patient_feedback}")  # Log for verification

    # Execute the crew and pass the feedback as input to the tasks
    result = ai_clinical_crew.kickoff(inputs={"feedback": patient_feedback})

    # Print the execution result for debugging (to see the structure)
    print("Execution result:", result)

    # Check if tasks are available in the output
    if hasattr(result, 'tasks_output'):  # Replace with the correct attribute after checking the structure
        total_tokens = 0
        for task_result in result.tasks_output:
            print(f"Task '{task_result.name}' used {task_result.token_usage} tokens")
            total_tokens += task_result.token_usage

        # Print total token usage
        print(f"Total tokens used by the crew: {total_tokens}")
    else:
        print("No tasks output found in the result. Please check the result structure.")
