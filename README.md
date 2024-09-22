# AI Clinical Advisory Crew

## Description
This project implements a system for analyzing and improving patient experience in healthcare environments, using a team of specialized AI agents. The system processes patient feedback, analyzes healthcare processes, evaluates emotional states, and proposes improvements in communication and processes. 

A key feature of this project is the flexibility to swap out different LLM (Large Language Model) configurations for testing various outputs. Each agent can utilize a different LLM, allowing for the combination of multiple agents with distinct models in the process, enhancing the overall analysis and recommendations.

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

- **llama_model**: Meta's Llama 3.1 8B is a state-of-the-art language model offering a good balance between performance and computational efficiency. It's suitable for various natural language processing tasks, including text generation and question answering, leveraging Meta's advanced AI research.

- **hermes_model**: NousResearch's Hermes 3 8B is an enhanced version of the Hermes model, focusing on advanced agent capabilities and improved performance in reasoning and conversation. It utilizes the ChatML format for prompts, allowing for greater user control and direction in interactions.

- **phi_model**: Microsoft's Phi-3 Mini is a lightweight 3.8B parameter model delivering cutting-edge performance in reasoning and language comprehension tasks. It was trained on synthetic and high-quality datasets, emphasizing dense reasoning properties and showcasing Microsoft's innovative approach to efficient AI models.

- **gemma_model**: Google's Gemma 2 9B is an efficient model part of a series including 2B, 9B, and 27B parameter versions. It offers a good balance between performance and size, suitable for various natural language processing applications, reflecting Google's commitment to accessible AI technology.

- **openhermes_model**: The OpenHermes model, based on the Hermes series by NousResearch, focuses on providing advanced assistant and text generation capabilities. It likely incorporates improvements in context understanding and coherent response generation, building on NousResearch's expertise in AI development.

- **mistral_model**: Mistral AI's Mistral NeMo, developed in collaboration with NVIDIA, is a 12B parameter model offering a context window of up to 128k tokens. It excels in reasoning, general knowledge, and coding accuracy for its size category, showcasing the combined strengths of Mistral AI and NVIDIA's technologies.

- **quwen_model**: Alibaba Group's Qwen2 7B is a multilingual model from the Qwen2 series, supporting 29 languages including English and Chinese. It features an extended context window of 128k tokens, making it versatile for a variety of natural language processing tasks and demonstrating Alibaba's commitment to multilingual AI capabilities.

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
