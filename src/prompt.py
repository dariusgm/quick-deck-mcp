from string import Template
from loguru import logger

from src.types import Settings


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


def agenda(settings: Settings) -> list[dict[str, str | list[dict[str, str]]]]:
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

    developer = developer_template.substitute(style=settings.style)
    user = user_template.substitute(
        topic=settings.topic,
        audience=settings.audience,
        language=settings.language
    )
    logger.debug("Agenda Prompt: {} {}", developer, user)
    return send_template(developer, user)


def content(settings: Settings, agenda: str) -> list[
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


    developer = developer_template.substitute(style=settings.style)
    user = user_template.substitute(
        topic=settings.topic,
        audience=settings.audience,
        language=settings.language,
        style=settings.style,
        header=agenda)
    logger.debug("Content Prompt: {} {}", developer, user)
    return send_template(developer, user)