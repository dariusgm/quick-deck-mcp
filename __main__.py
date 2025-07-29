import os
import sys
from string import Template
from typing import List, Literal
from mcp.server.fastmcp import FastMCP, Context
from openai import OpenAI
from dotenv import load_dotenv
from openai.types.chat import ChatCompletionMessage
from pydantic import BaseModel
from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, serialize=True)  # JSON output
logger.info("MCP Booting")

def _client():
    load_dotenv()
    api_key = os.environ["OPENAI_API_KEY"]
    return OpenAI(api_key=api_key)


class InputAgenda(BaseModel):
    topic: str
    audience: str
    style: str
    language: str

class Slide(BaseModel):
    title: str
    content: str


class ExportParameters:
    format: Literal["pdf", "pptx"]


mcp = FastMCP("Quick Deck MCP")
client = _client()

def send_template(developer_prompt: str, user_prompt: str) -> list[dict[str, str | list[dict[str, str]]]]:
    """
    Prepare the message to send to the OpenAI API.
    :param developer_prompt:
    :param user_prompt:
    :return:
    """

    return [{
        "role": "developer",
        "content": [
            {
                "type": "text",
                "text": developer_prompt
            }
        ]
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": user_prompt
            }
        ]
    }]


def send_message(message: list[dict[str, str | list[dict[str, str]]]]) -> ChatCompletionMessage:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=message,
        response_format={
            "type": "text"
        },
        temperature=1,
        max_completion_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message


@mcp.prompt("Generate an agenda for a presentation")
def generate_agenda_prompt(settings: dict) -> list[dict[str, str | list[dict[str, str]]]]:
    developer_template = Template("""
       I want to to act as an expert in presentations for $style. 
       You will receive a topic of my choice and provide slides and speaker notes for me.
       Please use valid Markdown as a response.
       ONLY generate the agenda.
       Separate each Slide with ---
       Here is an example for the topic “git” and the audience is “beginner software engineers”.
       Extend the list of topics as needed.
       Do NOT enumerate the slides. Instead use a summary of the content.
       
       # Agenda for Git Presentation
       
       ---
       
       ## The 4 Ws of Git: 
       - What is git?
       - Why use git?
       - What is the history of git?
       - Who should use git?
       --- 
    """)

    user_template = Template("""
    The topic is about $topic and the audience is $audience. Use $language for the content.
    """)

    developer = developer_template.substitute(style=settings.get('style'))
    user = user_template.substitute(
        topic=settings.get('topic'),
        audience=settings.get('audience'),
        language=settings.get('language')
    )
    logger.info("Agenda Prompt: {} {}", developer, user)
    return send_template(developer, user)

@mcp.prompt("Generate Content for a presentation")
def generate_content_prompt(settings: dict, agenda: str) -> list[
    dict[str, str | list[dict[str, str]]]]:
    developer_template = Template("""
      I want to to act as an expert in presentations for $style. 
       You will receive a topic of my choice and provide slides and speaker notes for me.
       Please use valid Markdown as a response.
       ONLY generate the content for the slide.
       Here is an example for the topic “git” and the audience is “beginner software engineers”.
       Extend the list of topics as needed.
       Do NOT enumerate the slide. Instead use a summary of the content.
       Do NOT translate the Keyword notes for any language.

     
      ## What is git? 
      - Git is a distributed version control system (VCS) 
      - Helps developers to work efficiently.
      ::: notes
      Git is a distributed version control system (VCS) that tracks changes in files, allowing multiple people to collaborate on projects, manage source code, and keep a history of all changes. It helps developers work efficiently on teams, resolve conflicts, and roll back to earlier versions when needed.
      :::
      ---
    """)

    user_template = Template("""
    Topic is "$header" in the Context of "$topic". Use "$language" as language and in the style of "$style" for the "$audience" audience.
    """)


    developer = developer_template.substitute(style=settings.get('style'))
    user = user_template.substitute(
        topic=settings.get('topic'),
        audience=settings.get('audience'),
        language=settings.get('language'),
        style=settings.get('style'),
        header=agenda)
    logger.info("Content Prompt: {} {}", developer, user)
    return send_template(developer, user)


# Basic prompt tools
@mcp.tool("Agenda Generation")
def generate_agenda(settings: dict) -> List[str]:
    logger.info("Generating agenda with this settings: {} ", settings)
    agenda_prompt = generate_agenda_prompt(settings)
    response = send_message(agenda_prompt).content
    if response:
        result = response.split("---")
        return result
    else:
        return []

@mcp.tool("Content Generation")
def generate_content(settings: dict, agenda: List[str]) -> List[Slide]:
    result = []
    for agenda_element in agenda:
        logger.info("Generating Content for agenda element: {} ", agenda_element)
        content_prompt = generate_content_prompt(settings, agenda_element)
        response = send_message(content_prompt).content
        if not response:
            continue
        for paragraph in response.split("---"):
            paragraph = paragraph.strip()
            if paragraph.strip() == "":
                continue

            if paragraph.startswith("-"):
                paragraph = paragraph[1:]

            slide = Slide(content=paragraph, title=agenda_element)
            result.append(slide)
    return result

# Simulated export (pretend long-running)
@mcp.tool()
async def export_pdf(slides: List[str]) -> str:
    return "data:application/pdf;base64,..."  # Fake output

@mcp.tool()
async def export_pptx(slides: List[str]) -> str:
    return "data:application/vnd.openxmlformats-officedocument.presentationml.presentation;base64,..."
