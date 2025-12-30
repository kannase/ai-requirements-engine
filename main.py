import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import FileReadTool

# Load your keys from the .env file
load_dotenv()

# Setup the tool to read your specific file from the data folder
# Replace 'requirements.pdf' with your actual file name
requirement_path = os.path.join('data', 'requirements.pdf')
file_tool = FileReadTool(file_path=requirement_path)

# Define your BA Agent
ba_agent = Agent(
    role='Business Analyst',
    goal='Convert requirements into Jira stories',
    backstory='Expert in agile and domain requirements.',
    tools=[file_tool],
    verbose=True
)

# Define the task to output to your 'output' folder
generate_md = Task(
    description='Read the requirements and write a markdown backlog.',
    expected_output='A structured markdown file.',
    agent=ba_agent,
    output_file='output/backlog.md'
)

# Run the Agent
crew = Crew(agents=[ba_agent], tasks=[generate_md])
crew.kickoff()