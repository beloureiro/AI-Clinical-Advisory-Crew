from crewai_tools import BaseTool
import time

class BPMNTool(BaseTool):
    name: str = "BPMN Analysis Tool"
    description: str = "Tool for extracting steps in the patient's journey based on feedback."

    def _run(self, feedback: str) -> str:
        """
        Main function that runs the tool based on the provided feedback.
        It checks if the feedback is a valid string and then processes the journey mapping.
        Includes logic to prevent infinite loops and ensures proper input validation.
        """
        if not isinstance(feedback, str):
            raise TypeError(f"Feedback should be a string, but got {type(feedback).__name__}")
        
        previous_output = None
        max_iterations = 10
        iteration = 0
        start_time = time.time()
        time_limit = 5  # Limit of 5 seconds to prevent infinite loop

        while iteration < max_iterations and (time.time() - start_time < time_limit):
            iteration += 1
            try:
                journey_steps = self.extract_journey_steps(feedback)
                journey_steps = self.remove_redundancies(journey_steps)  # Remove redundant steps
                current_output = self.format_journey(journey_steps)

                # If the output has not changed from the previous iteration, break to avoid looping
                if current_output == previous_output:
                    break
                
                previous_output = current_output
            except Exception as e:
                print(f"Iteration {iteration} failed: {e}")
                continue

        if iteration >= max_iterations:
            raise Exception("Max iterations reached, possible loop detected.")

        return current_output

    def extract_journey_steps(self, feedback: str) -> list:
        """
        Extracts the steps of the patient's journey directly from the feedback.
        Splits the feedback into sentences representing different steps of the journey.
        """
        journey_steps = feedback.split(".")
        return [step.strip() for step in journey_steps if step]

    def remove_redundancies(self, steps: list) -> list:
        """
        Removes redundant steps in the journey. If a step is repeated, it will be filtered out.
        """
        seen = set()
        unique_steps = []
        for step in steps:
            if step not in seen:
                unique_steps.append(step)
                seen.add(step)
        return unique_steps

    def format_journey(self, steps: list) -> str:
        """
        Formats the extracted steps of the journey in the required task format.
        """
        formatted_journey = "Patient_Journey_Health_IT_Process_Expert:\n"
        for step in steps:
            formatted_journey += f"- {step}\n"
        return formatted_journey


class ProcessAnalysisTool(BaseTool):
    name: str = "Process Analysis Tool"
    description: str = "Tool for identifying inefficiencies and improvement suggestions in the patient's journey."

    def _run(self, feedback: str) -> str:
        """
        Main function that runs the tool based on the provided feedback.
        It checks if the feedback is a valid string and processes the analysis for inefficiencies and improvement suggestions.
        Prevents infinite loops using iteration and time limit checks.
        """
        if not isinstance(feedback, str):
            raise TypeError(f"Feedback should be a string, but got {type(feedback).__name__}")

        previous_output = None
        max_iterations = 10
        iteration = 0
        start_time = time.time()
        time_limit = 5  # Limit of 5 seconds to avoid infinite loops

        while iteration < max_iterations and (time.time() - start_time < time_limit):
            iteration += 1
            try:
                inefficiencies, improvements = self.analyze_feedback(feedback)
                current_output = self.format_analysis(inefficiencies, improvements)

                # If the output has not changed from the previous iteration, break to avoid looping
                if current_output == previous_output:
                    break

                previous_output = current_output
            except Exception as e:
                print(f"Iteration {iteration} failed: {e}")
                continue

        if iteration >= max_iterations:
            raise Exception("Max iterations reached, possible loop detected.")
        
        return current_output

    def analyze_feedback(self, feedback: str) -> tuple:
        """
        Analyzes the feedback to identify inefficiencies and suggest improvements.
        Includes both systemic issues and interpersonal communication failures.
        """
        inefficiencies = []
        improvement_suggestions = []

        # Logic to detect inefficiencies based on common healthcare feedback patterns
        if "not" in feedback and "informed" in feedback or "not notified" in feedback:
            inefficiencies.append("Lack of proper communication or notification regarding service details")
        if "wait" in feedback or "delay" in feedback:
            inefficiencies.append("Delay in service")
        if "rude" in feedback or "disrespectful" in feedback:
            inefficiencies.append("Unprofessional behavior from staff")
        if "didn't listen" in feedback or "ignored" in feedback:
            inefficiencies.append("Lack of attention to patient's concerns")

        # Logic to suggest improvements based on feedback
        if "not" in feedback and "informed" in feedback or "not notified" in feedback:
            improvement_suggestions.append("Implement an alert system for notifying patients about service details")
        if "wait" in feedback or "delay" in feedback:
            improvement_suggestions.append("Streamline the scheduling process to minimize wait times")
        if "rude" in feedback or "disrespectful" in feedback:
            improvement_suggestions.append("Provide staff training on professionalism and patient interaction")
        if "didn't listen" in feedback or "ignored" in feedback:
            improvement_suggestions.append("Encourage doctors to engage actively with patients and listen to their concerns")

        return inefficiencies, improvement_suggestions

    def format_analysis(self, inefficiencies: list, improvements: list) -> str:
        """
        Formats the inefficiencies and improvements in the required task format.
        Ensures no duplication of journey mapping.
        """
        formatted_analysis = ""

        # Formatting inefficiencies
        if inefficiencies:
            formatted_analysis += "Inefficiencies_Healthcare_Process_Health_IT_Process_Expert:\n"
            formatted_analysis += "\n".join([f"- {ineff}" for ineff in inefficiencies])
        else:
            formatted_analysis += "Inefficiencies_Healthcare_Process_Health_IT_Process_Expert:\n- No inefficiencies\n"

        # Formatting improvement suggestions
        if improvements:
            formatted_analysis += "\nImprovement_Suggestions_Healthcare_Process_Health_IT_Process_Expert:\n"
            formatted_analysis += "\n".join([f"- {improve}" for improve in improvements])
        else:
            formatted_analysis += "\nImprovement_Suggestions_Healthcare_Process_Health_IT_Process_Expert:\n- No improvements needed\n"

        return formatted_analysis
