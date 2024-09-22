# AI Clinical Advisory Crew

## Description
This project implements a system for analyzing and improving patient experience in healthcare environments, using a team of specialized AI agents. The system processes patient feedback, analyzes healthcare processes, evaluates emotional states, and proposes improvements in communication and processes.

## Agents
The project utilizes five specialized agents:

1. Patient Experience Expert
2. Health & IT Process Expert
3. Clinical Psychologist
4. Communication Expert
5. Manager and Advisor

Each agent has a specific role in analyzing and improving the patient experience.

## Configuration
The project uses the Ollama models for natural language processing:
- `llama3.1:8b`
- `hermes3:8b`
- `phi3.5:3.8b`
- `gemma2:9b`
- `openhermes:latest`

## Requirements
- Python 3.8+
- Dependencies listed in `requirements.txt`

## Installation
1. Clone the repository
2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
Run the main script:
```
python main.py
```

The script reads patient feedback from `patient_feedback.txt` and performs analysis through the AI agent team.

## Project Structure
- `main.py`: Main script
- `config/`: Project configurations
- `agents/`: Agent definitions
- `tasks/`: Task definitions
- `utils.py`: Utility functions

## Contributing
Contributions are welcome. Please open an issue to discuss proposed changes.

## License
[MIT](https://choosealicense.com/licenses/mit/)
