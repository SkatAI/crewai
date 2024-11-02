# Agents workshop

RAGs is so 2024. Long live AI agents

In this workshop, we build an AI agent to analyze the political discourse of groups and MEPs as expressed in Verbatim report of proceedings from the EU parliament.

This is a no code workshop: all the code will be entirely produced by LLMs.

## Introductory presentation

We will begin with a set of presentations on

- the concepts of AI agents, their roles, and the types of questions they can help answer in political analysis.
- NLP concepts and tasks
  - entity extraction, information extraction, topic extraction
  - identifying underlying sentiments, biases, or recurring themes across debates.
- Guide on prompt engineering, giving participants more control over agent outputs.

- crew.AI: how-to and examples
- Other platforms: Langchain
- hands on google Colab
- tutorials on data visualization tools like Plotly that can be paired with AI agent outputs for deeper insight.
- APIs: OpenAI, Wikipedia, Reddit, ...

## Potential research outcomes

Participants can produce articles on the controversies and respective positions of actors on a given topic (pesticides, workers rights, AI regulation, ...). The nature, style and structure etc of the article or report is up to the participant

The AI agent can also be tailored to produce a database of content (graph database, relational database, ...) that can be used to answer and explore research questions with other means and tools.

- thematic dashboards, interactive timelines of topics, real-time sentiment tracking across different debates or topics.
- different writing formats, including policy briefs, infographics, or multimedia storyboards.

## The data : verbatim report of proceedings

Each parliament session is fully recorded and the verbatim reports are available online

Each proceeding includes the interventions of multiple MEPs on the subject of the day.

Each MEP speaks in his or her native language. The verbatim reports typically have dozens of different languages.

## AI Agents

We want to use crews of AI Agents to perform multiple tasks

- data gathering
- information extraction
- topic, controversies and arguments identification
- writing reports, articles, blog posts
- visually exploring the data
- formatting the extracted information in a database friendly format
- focusing on very specific topics

For instance, an overall task for a group of participants could be

- outline the shift in votes and political discourse in the EU Parliament before and after the EU elections of June 2024
- identify the positions (problem assessment, suggested solution , political agenda, etc ) of the different actors on a given topic
- Map all the topics addressed in the parliament proceedings in 2024 and evaluate the importance (tbd) of the political groups on said topics. Output the data as JSON
- Produce visualization showing the influence of geographic (industrial | economical| cultural etc)  characteristics of the countries on certain topics


Topics can  AI regulation to more specific ones : AI regulation as an impediment to innovation)
In each case, the idea is to decompose the overall task as a set of subtasks that can be given to agents with specific roles.

## Specific activities

- Develop "agent role cards" for each type of AI agent to help participants clearly understand each role and how it fits into the overall task.

- ‘AI Agent Clinic’ where participants share and learn debugging strategies, around common LLM issues.

## Challenges

- leap of faith : LLMs being overly confident, the outcome can be incomplete, or over simplifying.
- finding strategies to handling documents at scale while preserving context
- defining a mix of measurable and insightful quality evaluation of LLMs outcomes
- using external data sources to improve LLMs insights an conclusions (wikipedia for instance)
- how to use LLMs to produce code we don't (or don't want) to understand. What is the right methodology to avoid the endless loop of errors and uncertain fixes ?
- strategies for validating data integrity and mitigating overconfident or misleading outputs by LLMs.

## Tools and data

We can use crew.ai to create series of AI Agents

The dataset of proceedings of the EU parliament can be provided in pdfs, html, text files or other formats.

## Requirements

- We don't assume any familiarity with coding.
- Everything should be specified through prompts and LLMs.
- Code will be run in Google Colab.

Participants are expected

- to have a subscription to OpenAI or equivalent (Anthropic, Huggingface)
- have a Google Colab account (free or paid subscription)
