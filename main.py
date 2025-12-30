import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from crewai_tools import PDFSearchTool
# 1. Load your keys from the .env file
load_dotenv()

# 2. Define the Gemini Model
# Ensure your .env has GOOGLE_API_KEY=your_key
gemini_llm = LLM(
    model="gemini/gemini-2.0-flash-lite",
    api_key=os.getenv("GOOGLE_API_KEY")
)

# 3. Setup the tool FIRST (so the agent can find it)
# Ensure 'requirements.pdf' exists in your 'data' folder
requirement_path = os.path.join('data', 'requirements.txt') # Use .txt
file_tool = FileReadTool(file_path=requirement_path)

# 4. Define your BA Agent (Now assigning the tools and LLM correctly)
ba_agent = Agent(
    role='Business Analyst',
    goal='Convert requirements into Jira stories',
    backstory='Expert in agile and domain requirements.',
    tools=[file_tool], # Correctly references the tool defined above
    llm=gemini_llm,    # Uses your Gemini 2.0 Flash thinking power
    verbose=True
)

# 5. Define the task
generate_md = Task(
    description='Read the requirements and write a markdown backlog.',
    expected_output='A structured markdown file.',
    agent=ba_agent,
    output_file='output/backlog.md'
)

# 6. Run the Agent
crew = Crew(agents=[ba_agent], tasks=[generate_md],memory=False)
crew.kickoff()