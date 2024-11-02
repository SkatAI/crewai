from crewai import Agent, Task, Crew, Process
from langchain.tools import tool
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from typing import Dict, List
import json

class ParliamentTools:
    def __init__(self):
        # self.llm = ChatOpenAI(temperature=0.2)
        self.llm = ChatOpenAI(
            model_name='gpt-3.5-turbo',
            temperature=0.5,
            # max_tokens=5000,
            # top_p=top_p,
            # frequency_penalty=frequency_penalty,
            # presence_penalty=presence_penalty,
            # request_timeout=120  # Timeout in seconds
        )


        # Speaker extraction prompt
        self.speaker_extraction_prompt = PromptTemplate(
            template="""You are analyzing a European Parliament debate transcript.

            Extract the following information for each speaker:
            - Full name
            - Political group (if mentioned)
            - Country or representation (e.g., "Member of the Commission")
            - Role or position (if mentioned)

            Rules:
            1. Only include speakers who actually make statements
            2. Identify political groups using standard EP abbreviations (EPP, S&D, Renew, etc.)
            3. For Commission members, note their specific portfolio
            4. Include the speaking order in the debate

            Format the output as a JSON list with the following structure:
            {
                "speakers": [
                    {
                        "name": "",
                        "political_group": "",
                        "country": "",
                        "role": "",
                        "speaking_order": 1
                    }
                ]
            }

            Debate transcript:
            {text}

            Extract the speakers information following the above rules:""",
            input_variables=["text"]
        )

        # Position analysis prompt
        self.position_analysis_prompt = PromptTemplate(
            template="""You are analyzing positions and arguments in a European Parliament debate.

            Focus on identifying:
            1. Specific policy positions (not general statements)
            2. Concrete proposals and solutions
            3. Points of disagreement between speakers
            4. National or political group perspectives
            5. Technical or operational suggestions

            Exclude:
            - General statements about the danger/importance of the topic
            - Rhetorical flourishes without substantive content
            - Standard procedural remarks

            Format the output as a JSON with the following structure:
            {
                "policy_positions": [
                    {
                        "speaker": "",
                        "political_group": "",
                        "position": "",
                        "specific_proposals": [],
                        "opposing_views": [],
                        "alignment": [] // other speakers/groups supporting this position
                    }
                ],
                "key_controversies": [
                    {
                        "topic": "",
                        "contrasting_views": [],
                        "groups_involved": []
                    }
                ]
            }

            Debate text:
            {text}

            Analyze the positions following the above rules:""",
            input_variables=["text"]
        )

        # Topic extraction prompt
        self.topic_extraction_prompt = PromptTemplate(
            template="""Analyze this European Parliament debate transcript and extract:

            1. Main topic and subtopics
            2. Context and background
            3. Specific issues being debated

            Format as JSON:
            {
                "main_topic": "",
                "subtopics": [],
                "context": "",
                "key_issues": []
            }

            Debate text:
            {text}

            Extract the topic information:""",
            input_variables=["text"]
        )

    @tool
    def extract_speakers(self, text: str) -> Dict:
        """Extract speakers and their details from parliament text using LLM"""
        response = self.llm.predict(
            self.speaker_extraction_prompt.format(text=text)
        )
        return json.loads(response)

    @tool
    def analyze_positions(self, text: str) -> Dict:
        """Analyze political positions and arguments using LLM"""
        response = self.llm.predict(
            self.position_analysis_prompt.format(text=text)
        )
        return json.loads(response)

    @tool
    def extract_topic(self, text: str) -> Dict:
        """Extract the main topic and context of the debate using LLM"""
        response = self.llm.predict(
            self.topic_extraction_prompt.format(text=text)
        )
        return json.loads(response)

# Enhanced Information Extraction Agent
info_extraction_agent = Agent(
    name='Information Extractor',
    goal='Extract and organize key information from parliamentary debates',
    backstory="""You are an expert in analyzing parliamentary proceedings with deep
    knowledge of EU institutions and political groups. You specialize in identifying
    speakers, their affiliations, and extracting key arguments while filtering out
    general statements. You understand the formal structures of EU debates and can
    identify different types of interventions.""",
    tools=[
        ParliamentTools().extract_speakers,
        ParliamentTools().extract_topic
    ],
    verbose=True
)

# Enhanced Political Analyst Agent
political_analyst = Agent(
    name='Political Analyst',
    goal='Analyze political positions and identify key controversies in debates',
    backstory="""You are a seasoned EU political analyst with expertise in
    understanding political dynamics, policy positions, and identifying points of
    contention between different political groups and member states. You have deep
    knowledge of EU political groups' traditional positions and can identify when
    they deviate from expected stances.""",
    tools=[ParliamentTools().analyze_positions],
    verbose=True
)

# New Context Analyst Agent
context_analyst = Agent(
    name='Context Analyst',
    goal='Provide broader political and policy context to debate positions',
    backstory="""You are an expert in EU policy development and political history.
    You understand how current debates fit into broader policy trajectories and can
    identify relevant historical precedents and related policy initiatives.""",
    verbose=True
)

# Enhanced Data Organization Agent
data_analyst = Agent(
    name='Data Analyst',
    goal='Structure and organize debate information into standardized JSON format',
    backstory="""You are a data organization expert specializing in converting
    complex political discourse into structured data formats. You ensure consistency
    and clarity in data representation while maintaining the nuance of political
    positions.""",
    verbose=True
)

# Define Enhanced Tasks
extract_info_task = Task(
    description="""
    1. Use extract_topic tool to identify the debate subject and context
    2. Use extract_speakers tool to create a comprehensive speaker list
    3. Organize the information chronologically
    4. Note any procedural elements or special debate formats
    5. Create initial structured summary
    """,
    agent=info_extraction_agent
)

analyze_politics_task = Task(
    description="""
    1. Use analyze_positions tool to map political stances
    2. Identify alliance patterns between speakers/groups
    3. Note unusual positions or coalition patterns
    4. Map national vs. political group divisions
    5. Document specific policy proposals and objections
    """,
    agent=political_analyst
)

analyze_context_task = Task(
    description="""
    1. Review the extracted positions
    2. Place arguments in broader EU policy context
    3. Identify related legislative initiatives
    4. Note relevant historical precedents
    5. Highlight potential policy trajectories
    """,
    agent=context_analyst
)

organize_data_task = Task(
    description="""
    1. Collect all analyzed information
    2. Structure into comprehensive JSON format
    3. Ensure cross-referencing between related positions
    4. Validate data completeness and consistency
    5. Generate final structured output
    """,
    agent=data_analyst
)

# Create Enhanced Crew
parliament_analysis_crew = Crew(
    agents=[
        info_extraction_agent,
        political_analyst,
        context_analyst,
        data_analyst
    ],
    tasks=[
        extract_info_task,
        analyze_politics_task,
        analyze_context_task,
        organize_data_task
    ],
    process=Process.sequential,
    verbose=True
)

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