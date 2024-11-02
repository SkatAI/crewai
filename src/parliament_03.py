from crewai import Agent, Task, Crew, Process
from langchain.tools import tool
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from typing import Dict, List
import json

class ParliamentTools:
    def __init__(self,
                 model_name: str = "gpt-4-1106-preview",  # or "gpt-3.5-turbo-1106"
                 temperature: float = 0.2,
                 max_tokens: int = 4000,
                 top_p: float = 0.9,
                 frequency_penalty: float = 0.0,
                 presence_penalty: float = 0.0):
        """
        Initialize ParliamentTools with configurable LLM parameters

        Args:
            model_name (str): The OpenAI model to use
                Options include:
                - "gpt-4-1106-preview" (recommended for complex analysis)
                - "gpt-3.5-turbo-1106" (faster, good for simpler tasks)
                - "gpt-4" (standard GPT-4)
            temperature (float): Controls randomness (0.0-2.0)
                - Lower values: more focused and deterministic
                - Higher values: more creative and varied
            max_tokens (int): Maximum length of response
            top_p (float): Nucleus sampling parameter
            frequency_penalty (float): Penalize frequent tokens
            presence_penalty (float): Penalize repeated topics
        """
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            request_timeout=120  # Timeout in seconds
        )

        # Rest of the class implementation remains the same...
        self.speaker_extraction_prompt = PromptTemplate(...)
        # ... (other prompts and methods)

# Example usage:
def create_parliament_analysis_crew(
    llm_config: Dict = None
) -> Crew:
    """
    Create a crew with customized LLM configuration

    Args:
        llm_config (Dict): Configuration for the LLM
            Default configuration if None provided
    """
    if llm_config is None:
        llm_config = {
            "model_name": "gpt-4-1106-preview",
            "temperature": 0.2,
            "max_tokens": 4000
        }

    # Initialize tools with custom LLM config
    parliament_tools = ParliamentTools(**llm_config)

    # Create agents with configured tools
    info_extraction_agent = Agent(
        name='Information Extractor',
        goal='Extract and organize key information from parliamentary debates',
        backstory="""You are an expert in analyzing parliamentary proceedings...""",
        tools=[
            parliament_tools.extract_speakers,
            parliament_tools.extract_topic
        ],
        verbose=True
    )

    # ... rest of the crew setup

    return parliament_analysis_crew

# Example of using different configurations:
def analyze_debate_with_config(debate_text: str, config: Dict = None) -> Dict:
    """
    Analyze debate with specific LLM configuration

    Args:
        debate_text (str): The debate text to analyze
        config (Dict): LLM configuration parameters
    """
    crew = create_parliament_analysis_crew(config)
    return crew.kickoff(inputs={'debate_text': debate_text})

# Usage examples:
if __name__ == "__main__":
    # Default configuration (GPT-4 with balanced settings)
    default_analysis = analyze_debate_with_config(debate_text)

    # More creative analysis
    creative_config = {
        "model_name": "gpt-4-1106-preview",
        "temperature": 0.8,
        "max_tokens": 4000,
        "presence_penalty": 0.2
    }
    creative_analysis = analyze_debate_with_config(debate_text, creative_config)

    # Faster, more focused analysis
    fast_config = {
        "model_name": "gpt-3.5-turbo-1106",
        "temperature": 0.1,
        "max_tokens": 2000
    }
    fast_analysis = analyze_debate_with_config(debate_text, fast_config)