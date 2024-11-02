import json
from crewai import Agent, Task, Crew
import openai
# from langchain.llms import OpenAI

from langchain_openai import ChatOpenAI

from bs4 import BeautifulSoup
import requests
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

# check OpenAI models list
# models = openai.models.list()
# for model in models.dict()['data']:
#     print(model['id'])

# pricing
# https://openai.com/api/pricing/


from crewai_tools import tool

class ParliamentTools:
    @tool
    def fetch_debate_content(url: str) -> str:
        """The fetch_debate_content tool returns the text extracted from an online page given the page url. It uses BeautifulSoup"""
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract debate text (implementation depends on specific website structure)
        return soup.get_text()

class DebateAnalyzer:
    def __init__(self, prompts, llm, raw_text):
        self.prompts = prompts
        self.llm = llm
        self.raw_text = raw_text
        # self.debate_url = debate_url
        self.agents = { 'ner': None, 'analyzer': None }
        self.tasks = {'ner': None, 'analysis': None }
        # self.agents = {'scraper': None}
        # self.tasks = {'scraping': None}


    def create_agents(self):
        # Web Scraper Agent
        # self.agents['scraper'] = Agent(
        #     role='Web Scraper',
        #     goal='Extract raw text from parliamentary debate webpage',
        #     backstory='Expert at parsing web content and extracting structured debate information',
        #     llm=self.llm,
        #     tools=[ParliamentTools.fetch_debate_content],
        #     verbose=True
        # )

        # NER Agent
        self.agents['ner'] = Agent(
            role='Named Entity Recognition Specialist',
            goal='Identify and extract speaker information including name, political group, and role',
            backstory='Specialist in identifying and categorizing named entities in political texts',
            llm=self.llm,
            verbose=True
        )

        # Content Analyzer Agent
        self.agents['analyzer'] = Agent(
            role='Content Analyzer',
            goal='Extract and structure arguments, assessments, and proposals from speeches',
            backstory='Expert in analyzing political discourse and identifying key discussion points',
            llm=self.llm,
            verbose=True
        )

    def create_tasks(self):
        # Task 1: Fetch and prepare debate content

        # self.tasks['scraping'] = Task(
        #     description=analyzer.prompts['scraping_task'],
        #     agent=analyzer.agents['scraper'],
        #     expected_output="The verbatim text of the debates extracted from the url",
        #     context=[{
        #         "url": analyzer.debate_url,
        #         "description": "URL to scrape debate text from. Has to be from the European Parliament website site: europarl.europa.eu",
        #         "expected_output": "Raw text content from the webpage"
        #     }]
        # )

        # Task 2: Extract speaker information
        self.tasks['ner'] = Task(
            description=self.prompts['ner_task'],
            agent=self.agents['ner'],
            expected_output="A JSON formatted list of speakers, their group affiliation",
            context=[{
                "raw_text": self.raw_text,
                "description": "NER task: extract names of speaker and their political affiliation from the raw_text",
                "expected_output": "A JSON formatted list of speakers, their group affiliation"
                }]
        )

        # Task 3: Analyze speech content
        self.tasks['analysis'] = Task(
            description=self.prompts['analysis_task'],
            agent=self.agents['analyzer'],
            expected_output="A JSON formatted list of main arguments, situation assessment, proposals or recommendations per speaker",
            context=[{
                "previous_task": self.tasks['ner'],
                "output_format": "json",
                "description": "speech analysis task",
                "expected_output": "A JSON formatted list of main arguments, situation assessment, proposals or recommendations per speaker"
            }]
        )


if __name__ == "__main__":


    llm = ChatOpenAI(
        temperature=0.3,
        model_name="gpt-4o-mini"
    )

    # model_name="gpt-3.5-turbo"


    with open('./prompts/prompts_04.json', 'r') as f:
        prompts = json.load(f)

    debate_url = "https://www.europarl.europa.eu/doceo/document/CRE-10-2024-09-19-ITM-010_EN.html"

    def fetch_debate_content(url: str) -> str:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()


    raw_text = fetch_debate_content(debate_url)

    analyzer = DebateAnalyzer(prompts, llm, raw_text)

    analyzer.create_agents()
    analyzer.create_tasks()



    # Create and run crew
    debate_crew = Crew(
        agents=list(analyzer.agents.values()),
        tasks=list(analyzer.tasks.values()),
        verbose=True
    )

    result = debate_crew.kickoff()

    # Parse and verify results
    try:
        parsed_result = json.loads(result)
        # return parsed_result
    except json.JSONDecodeError:
        raise ValueError("Failed to parse results into JSON format")


    # Save results to file
    # with open('debate_analysis.json', 'w') as f:
    #     json.dump(results, f, indent=2)