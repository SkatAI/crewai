import json
from crewai import Agent, Task, Crew
from crewai_tools import tool
import openai

from langchain_openai import ChatOpenAI

from bs4 import BeautifulSoup
import requests
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key = os.getenv("OPENAI_API_KEY")

class DebateAnalyzer:
    def __init__(self,  llm4o, llm_4omini):
        self.llm4o = llm4o
        self.llm_4omini = llm_4omini

    def create_agents(self):
        # NER Agent
        ner_agent = Agent(
            role='Named Entity Recognition Specialist',
            goal='Identify and extract speaker information including name, political group, and role',
            backstory='Specialist in identifying and categorizing named entities in political texts',
            llm=self.llm_4omini,
            max_iter = 5,
            verbose=True
        )

        translator_agent = Agent(
            role = "Translator",
            goal='Translate each intervention in English',
            backstory='Fluent in all european languages, expert in translation of European Parliament debates.',
            llm=self.llm_4omini,
            max_iter = 5,
            verbose=True
        )

        argument_agent= Agent(
            role = "European Union policy analyzer",
            goal='Extract and structure arguments, assessments, and proposals from speeches',
            backstory='Expert in analyzing political discourse and identifying key discussion points',
            llm=self.llm4o,
            max_iter = 10,
            verbose=True
        )

        return [ner_agent, translator_agent, argument_agent]

    def create_tasks(self, agents, raw_text):
        # Task 2: Extract speaker information
        ner_task = Task(
            description= f'''For each intervention in the text :
            1. Extract the speaker's full name
            2. Identify their political group affiliation
            3. Determine their role or position
            4. identify the language.
            Format the output as a list of speaker entries with their associated metadata.
            Verify that no speakers are missed and all affiliations are correctly identified.
            Only return names extracted from the text below. Do not refer to MEPs that are not explicitly mentionned in the text below.

            --- here is the raw_text of the debate:
            {raw_text}
            ''',
            agent=agents[0],
            expected_output="A JSON formatted list of speakers and their group affiliation",
            context=[{
                "raw_text": raw_text,
                "description": "NER task: extract names of speaker and their political affiliation from the raw_text",
                "expected_output": "A JSON formatted list of speakers, their group affiliation"
                }]
        )

        translation_task = Task(
            description= f'''For each speaker intervention translate the text in English:
            - if the text is already in english or in French do not translate the text.
            - Format the output as a valid JSON object with the speaker name, language and political group affiliation obtained from the previous task

            -- verbatim text of the debate:
            {raw_text}
            ''',
            agent=agents[1],
            expected_output="A JSON formatted list of translated text into English per intervention along with each speaker name and metadata",
            context=[{
                "previous_task": ner_task,
                "output_format": "json",
                "description": "Translation task",
                "expected_output": "A JSON formatted list of translated text into English per intervention including the speaker name, political affiliation and original written language"
            }]
        )

        analysis_task = Task(
            description=f'''For each speaker intervention identified in the previous task:
            1. Extract main arguments presented.
            2. Capture the specific context, (laws, regulations, entities, objects or persons) on which the argument is constructed.
            3. Focus on specific details given by the speaker which are related to the topic of the debate. Who, when, what, why, how.
            4. Identify their assessment of the situation
            5. List any specific proposals and recommendations made.
            Format the output as a valid JSON object along with the speaker name and political group affiliation andoriginal text language
            ''',
            agent=agents[2],
            expected_output="A JSON formatted list of main arguments, context, situation assessment, proposals per speaker",
            context=[translation_task]
        )

        return [ner_task, translation_task, analysis_task]

# context=[{
#     "previous_task": translation_task,
#     "output_format": "json",
#     "description": "debate analysis task",
#     "expected_output": "A JSON formatted list of speaker name, language and group affiliation, with main arguments, situation assessment, proposals or recommendations per speaker"
# }]

if __name__ == "__main__":

    llm_4omini = ChatOpenAI( temperature=0, model_name="gpt-4o-mini" )
    llm_4o = ChatOpenAI( temperature=0, model_name="gpt-4o" )

    # get raw text
    # debate_url = "https://www.europarl.europa.eu/doceo/document/CRE-10-2024-09-19-ITM-010_EN.html"
    # response = requests.get(debate_url)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # raw_text = soup.get_text()

    with open('./data/fake_news.txt', 'r') as f:
        raw_text = f.read()

    analyzer = DebateAnalyzer(llm_4o, llm_4omini)

    agents = analyzer.create_agents()
    tasks = analyzer.create_tasks(agents, raw_text)

    # Create and run crew
    debate_crew = Crew(
        agents=agents,
        tasks=tasks,
        verbose=True
    )

    result = debate_crew.kickoff()
    print(result)
