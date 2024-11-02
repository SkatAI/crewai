import os
import random
import logging
import subprocess
import warnings
from IPython.display import Markdown

import os

from crewai import Agent, Task, Crew

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai_api_key = os.getenv("OPENAI_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")

# TOKEN = os.getenv('DISCORD_TOKEN')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('crewai_agents')

if __name__ == "__main__":

    print("hello world")
    os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

    planner = Agent(
        role="Content Planner",
        goal="Scope content on {topic}",
        backstory="You're working on planning a lesson about the topic: {topic}."
                "You collect information that helps the graduate students learn something. "
                "Your work is the basis for the Content Writer to write a lesson on this topic.",
        allow_delegation=False,
        verbose=True
    )

    writer = Agent(
        role="Content Writer",
        goal="Write a short introduction lesson about the topic: {topic}",
        backstory="You're working on writing a short intro lesson about the topic: {topic}. "
"You base your writing on the work of the Content Planner, who provides an outline and relevant context about the topic. "
"You follow the main objectives and direction of the outline, as provide by the Content Planner. ",
        allow_delegation=False,
        verbose=True
    )

    teacher = Agent(
        role="Teacher",
        goal="Edit and review the content of a lesson to make it engaging with the class",
        backstory="You are a subjject expert and a teacher who receives the content for a short lesson from the Content Writer. "
                "Your goal is to review the content to ensure that it is accurate, concise and straight to the point,"
                "You make sure acronyms are fully explained."
                "You balance abstract concepts and theory with real world uses cases, and highlight pros and cons",
        allow_delegation=False,
        verbose=True
    )


    plan = Task(
        description=(
            "1. Prioritize the main concepts and real world examples on {topic}.\n"
            "2. Take into account the paint points and interests of the target audience which consists of post graduates students, .\n"
            "3. Develop a detailed content outline including an introduction, key points, uses cases, pros and cons and real world examples."
        ),
        expected_output="The outline for an introductory lesson  "
            "with an outline, concepts, uses cases, pros and cons, and real world examples. Include resources.",
        agent=planner,
    )

    write = Task(
        description=(
            "1. Use the content plan to craft a compelling lesson on {topic}.\n"
            "2. Sections/Subtitles are properly named with action verbs.\n"
            "4. Ensure the lesson is structured with an engaging introduction, insightful body, and a summarizing conclusion.\n"
            "5. Proofread for grammatical errors.\n"
        ),
        expected_output="A well-written lesson "
            "in markdown format, ready for class, "
            "each section should have 2 or 3 paragraphs.",
        agent=writer,
    )

    review = Task(
        description=("Proofread the given lesson for grammatical errors and ease of understanding."),
        expected_output="A well-written lesson in markdown format ready for class, "
                        "each section should have 2 or 3 paragraphs.",
        agent=teacher
    )



    crew = Crew(
        agents=[planner, writer, teacher],
        tasks=[plan, write, review],
        verbose=True
    )

    result = crew.kickoff(inputs={"topic": "Neo4j graph in data science"})

    Markdown(result)
