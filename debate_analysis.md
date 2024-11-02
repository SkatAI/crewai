# Parliament debate analysis

## Version 02

Your goal is to create AI agents using the platform crew.ai to extract information from the minutes of the European parliament debates.


please create a crew of agents

For each intervention :

- extract speaker name, political group and role (NER)
- extract the specific arguments, situation assessment and proposals for each speaker.
- output the results in a JSON format

Input:

- The input is a URL to the debate online page. not the full text




The code should

- use LLMs for NER and topic / arguments extractions
- instanciate an OpenAI LLM with model name and temperature

Instructions :

- Verify that all speakers and interventions are accounted for
- Keep the number of agents limited
- Keep the code simple
- Write the prompts in an external json file so that the prompt texts are not directly integrated in the code


## version 01

https://claude.ai/chat/949665fb-b0a6-4211-a7ad-560c250afd63


The goal is to create AI agents using the platform crew ai to analyze, extract information and understand the minutes of the european parliament debates on multiple topics.

I want to create a set of crew.ai agents to understand the controversies and arguments from the different countries and political groups

Given a list of documents of the verbatim reports of the european parliament

I attached a pdf version of one of the debate for illustration of the raw content

The **information extraction** agent task is to

- identify the topic of the debate
- identify the speakers, their political affiliation, their country
- summarize the main arguments of the different speakers

focusing on specific positions and do not take into account general statements on the danger of organized crime


The **political analyst** agent is an expert in EU politics
Its task is to
- find the oppositions in terms of assessment of the current situation or problem and suggested solutions ?

The **data analyst** agent will

- organize the data into a JSON format with keys : Topic, Position, Details, list of Speakers


please walk me through creating crew.ai agents leveraging its tools (SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool and others if needed) to carry out the different tasks


https://www.europarl.europa.eu/doceo/document/CRE-10-2024-09-18-ITM-007_EN.html