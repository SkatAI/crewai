from crewai import Agent, Task, Crew, Process
from langchain.tools import tool
from typing import Dict, List
import json

# Custom tools for data processing

class ParliamentTools:
    # [TODO] replace with LLMs and prompts
    @tool
    def extract_speakers(text: str) -> List[Dict]:
        """Extract speakers and their details from parliament text"""
        return []  # Implement extraction logic

    @tool
    def analyze_positions(text: str) -> List[Dict]:
        """Analyze political positions and arguments"""
        return []  # Implement analysis logic

''' Agents '''
# Create the Information Extraction Agent
info_extraction_agent = Agent(
    name='Information Extractor',
    goal='Extract and organize key information from parliamentary debates',
    backstory="""You are an expert in analyzing parliamentary proceedings with deep
    knowledge of EU institutions and political groups. Your expertise lies in identifying
    speakers, their affiliations, and extracting key arguments while filtering out
    general statements.""",
    tools=[ParliamentTools.extract_speakers],
    verbose=True
)

# Create the Political Analyst Agent
political_analyst = Agent(
    name='Political Analyst',
    goal='Analyze political positions and identify key controversies in debates',
    backstory="""You are a seasoned EU political analyst with expertise in
    understanding political dynamics, policy positions, and identifying points of
    contention between different political groups and member states.""",
    tools=[ParliamentTools.analyze_positions],
    verbose=True
)

# Create the Data Organization Agent
data_analyst = Agent(
    name='Data Analyst',
    goal='Structure and organize debate information into standardized JSON format',
    backstory="""You are a data organization expert specializing in converting
    complex political discourse into structured data formats. You ensure consistency
    and clarity in data representation.""",
    verbose=True
)

# Define Tasks
extract_info_task = Task(
    description="""
    1. Read through the debate transcript
    2. Identify the main topic of discussion
    3. Extract all speakers, their political groups, and countries
    4. Summarize specific positions and arguments, excluding general statements
    5. Create a structured summary of the findings
    """,
    agent=info_extraction_agent
)

analyze_politics_task = Task(
    description="""
    1. Review the extracted information
    2. Identify key points of disagreement between speakers
    3. Analyze different approaches to solutions proposed
    4. Highlight significant political divisions
    5. Document contrasting positions on both problem assessment and solutions
    """,
    agent=political_analyst
)

organize_data_task = Task(
    description="""
    1. Take the analyzed information
    2. Structure data into JSON format with required keys:
       - Speakers
        - affiliation
        - country
       - Topic
       - Position
       - Details
    3. Ensure consistency in data representation
    4. Validate the structured output
    """,
    # expected_output = ??,
    # output = ??
    agent=data_analyst
)

# Create the Crew
parliament_analysis_crew = Crew(
    agents=[info_extraction_agent, political_analyst, data_analyst],
    tasks=[extract_info_task, analyze_politics_task, organize_data_task],
    process=Process.sequential,
    verbose=2
)

# main
# Function to run the analysis
def analyze_parliament_debate(debate_text: str) -> Dict:
    """
    Run the full analysis pipeline on a parliament debate

    Args:
        debate_text (str): The raw text of the parliament debate

    Returns:
        Dict: Structured analysis of the debate
    """
    result = parliament_analysis_crew.kickoff(
        inputs={'debate_text': debate_text}
    )
    return result