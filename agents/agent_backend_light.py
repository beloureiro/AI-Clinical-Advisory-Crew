from crewai import Agent
from config.config_ollama import gemma2_2b_instruct_q4_K_S
from crewai_tools import DirectoryReadTool

# Initialize directory read tools with paths
json_directory_tool = DirectoryReadTool(directory='D:/OneDrive - InMotion - Consulting/AI Projects/AI-Clinical-Advisory-Crew/data_reports_json/')
txt_directory_tool = DirectoryReadTool(directory='D:/OneDrive - InMotion - Consulting/AI Projects/AI-Clinical-Advisory-Crew/data_reports_txt/')

# JSON File Agent
json_file_agent = Agent(
    role="JSON File List Agent",
    goal="List files in the JSON directory.",
    backstory="An agent to list all files in the JSON directory.",
    llm=gemma2_2b_instruct_q4_K_S,
    tools=[json_directory_tool],
    verbose=True
)

# TXT File Agent
txt_file_agent = Agent(
    role="TXT File List Agent",
    goal="List files in the TXT directory.",
    backstory="An agent to list all files in the TXT directory.",
    llm=gemma2_2b_instruct_q4_K_S,
    tools=[txt_directory_tool],
    verbose=True
)

# File Manager Agent to delegate tasks to JSON and TXT agents
file_manager_agent = Agent(
    role="File Manager Agent",
    goal="Delegate file listing tasks to JSON and TXT agents.",
    backstory="This agent manages the file listing process and delegates tasks to the appropriate agents.",
    llm=gemma2_2b_instruct_q4_K_S,
    tools=[],  # Manager agent does not need directory tools directly
    allow_delegation=True,  # Allow delegation of tasks
    verbose=True
)
