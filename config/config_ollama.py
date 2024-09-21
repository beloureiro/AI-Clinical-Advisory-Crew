from config.crew_config import ai_clinical_crew

if __name__ == "__main__":
    # Set patient feedback
    patient_feedback = "Doctor made me wait more than two hours for the appointment. In the end, I gave up due to this neglect."

    # Assign feedback to the first task
    ai_clinical_crew.tasks[0].inputs = {"feedback": patient_feedback}

    # Execute the crew
    result = ai_clinical_crew.kickoff()
    print("Execution result:", result)
