from config.crew_config import ai_clinical_crew

def get_patient_feedback():
    # Read feedback from a text file
    with open("patient_feedback.txt", "r", encoding='utf-8') as file:
        feedback = file.read().strip()
    return feedback

if __name__ == "__main__":
    # Get the initial patient feedback
    patient_feedback = get_patient_feedback()
    print(f"Patient Feedback: {patient_feedback}")  # Log for verification

    # Adjust task descriptions to include the feedback
    for task in ai_clinical_crew.tasks:
        if '{feedback}' in task.description:
            task.description = task.description.format(feedback=patient_feedback)

    # Execute the crew and pass the feedback as input to the tasks
    result = ai_clinical_crew.kickoff(inputs={"feedback": patient_feedback})

    # Print the execution result for debugging (to see the structure)
    print("Execution result:", result)

    # Check if tasks are available in the output
    if hasattr(result, 'tasks_output') and result.tasks_output:
        total_tokens = 0
        for task_result in result.tasks_output:
            # Use vars() to inspect task_result
            print(f"task_result contents: {vars(task_result)}")

            # Get task name and token usage
            task_name = getattr(task_result, 'name', 'Unknown Task')
            # Assuming token usage is stored in task_result.metrics['token_usage']
            metrics = getattr(task_result, 'metrics', {})
            token_usage = metrics.get('token_usage', 0)
            if token_usage:
                print(f"Task '{task_name}' used {token_usage} tokens")
                total_tokens += token_usage
            else:
                print(f"Token usage not available for task '{task_name}'")

        # Print total token usage
        print(f"Total tokens used by the crew: {total_tokens}")
    else:
        print("No tasks output found in the result. Please check the result structure.")
