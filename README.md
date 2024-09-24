# AI Clinical Advisory Crew

## Description
Welcome to the **AI Clinical Advisory Crew**, an advanced and flexible system designed to transform and elevate the patient experience in healthcare. This project brings together a team of specialized AI agents, each with a unique role in analyzing patient feedback, improving healthcare workflows, assessing emotional states, and delivering actionable recommendations for communication and operational improvements.

At the heart of this system lies its dynamic flexibility: it navigates across a suite of **Large Language Models (LLMs)** to determine the optimal AI configuration for each specific task. By utilizing models like Meta's LLaMA, NousResearch's Hermes, Microsoft's Phi, and others, the system continuously tests and refines outputs to ensure that the best-suited AI crew is selected to address the task at hand. This multi-agent approach allows for the combination of strengths across different models, ensuring comprehensive, data-driven analysis that adapts to the unique needs of your healthcare environment.

**A major benefit** of this system is that it operates using **local LLMs**, ensuring **maximum data security** by processing all information internally, without reliance on third-party APIs. This also delivers **significant cost savings**, as there is no need for external API usage, keeping operational costs low while maintaining full control over data privacy.

## Agents
Our AI team consists of five dedicated agents:
1. **Patient Experience Expert**: Focuses on understanding patient feedback, identifying key concerns, and measuring emotional intensity, ensuring that healthcare providers can address critical issues.
2. **Health & IT Process Expert**: Specializes in mapping the patient journey, identifying inefficiencies in workflows, and recommending improvements from both the healthcare and IT perspectives.
3. **Clinical Psychologist**: Analyzes the emotional state of patients, developing support strategies that address psychological needs and promote overall well-being.
4. **Communication Expert**: Evaluates the quality of interactions between healthcare professionals and patients, identifying where communication can be improved for better clarity, empathy, and problem resolution.
5. **Manager and Advisor**: Consolidates feedback from all experts, eliminating redundancies and providing clear, actionable reports that offer strategic recommendations for process improvement.

These agents are powered by a diverse range of LLMs, which are dynamically tested and swapped across different scenarios to identify the most suitable technology for each specific task:
- **llama_model**: Meta's Llama 3.1 8B is a state-of-the-art language model known for its balance between performance and efficiency. It excels in natural language processing tasks such as text generation and question answering, benefiting from Meta's leading AI research.
- **hermes_model**: NousResearch's Hermes 3 8B is designed for advanced reasoning and conversation. It uses the ChatML format, allowing greater control over interactions, making it a top choice for dialogue-intensive tasks requiring nuanced understanding.
- **phi_model**: Microsoft's Phi-3.5 Mini 3.8B is a lightweight model built for high performance in reasoning and language comprehension tasks. Trained on synthetic and high-quality datasets, it’s optimized for efficiency and excels in complex analytical scenarios.
- **gemma_model**: Google's Gemma 2 9B strikes an excellent balance between size and performance, making it ideal for a wide range of natural language processing tasks. It showcases Google's commitment to scalable and accessible AI solutions.
- **openhermes_model**: OpenHermes by NousResearch is built for superior text generation and assistant capabilities. It improves on context understanding and response coherence, providing robust performance for advanced conversational applications.
- **mistral_model**: Mistral AI's Mistral NeMo 12B, developed with NVIDIA, features a 128k token context window. It excels in reasoning, knowledge retention, and precise coding, offering a powerful solution for tasks requiring deep contextual analysis.
- **quwen_model**: Alibaba's Qwen2 7B is a multilingual model supporting 29 languages with a 128k token context window. It’s highly adaptable for natural language processing tasks, providing reliable performance in multilingual applications.
- **llava_model**: LLaVA (Large Language and Vision Assistant) 7B integrates visual and language understanding. Built on Meta’s LLaMA architecture, it handles tasks like visual question answering and image captioning, making it versatile for multimodal use cases.
- **zephyr_model**: Zephyr 7B from Hugging Face is based on the Mistral-7B-v0.1 architecture and optimized using Direct Preference Optimization (DPO). It excels in following detailed instructions and conversational tasks, outperforming many larger models in benchmarks like MT-Bench and AlpacaEval.

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

