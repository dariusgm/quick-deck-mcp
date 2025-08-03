# Basic prompt tools
from typing import Any, AsyncGenerator

from loguru import logger

from chatgpt import send_message
from prompt import agenda, content
from src.app_types import Settings
async def generate_agenda(settings: Settings) -> AsyncGenerator[str, None]:
    logger.info("Generating agenda with this settings: {} ", settings)
    agenda_prompt = agenda(settings)
    async for chunk in send_message(agenda_prompt):
        yield chunk



async def generate_content(settings: Settings, agenda_element: str) -> AsyncGenerator[str, None]:
    logger.info("Generating Content for agenda element: {} ", agenda_element)
    content_prompt = content(settings, agenda_element)
    async for chunk in send_message(content_prompt):
        yield chunk




async def export_pdf(slides: list[str]) -> str:
    return "data:application/pdf;base64,..."  # Fake output


async def export_pptx(slides: list[str]) -> str:
    return "data:application/vnd.openxmlformats-officedocument.presentationml.presentation;base64,..."