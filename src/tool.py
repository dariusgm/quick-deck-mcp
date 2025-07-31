# Basic prompt tools
from loguru import logger

from chatgpt import send_message
from prompt import agenda, content
async def generate_agenda(settings: dict) -> list[str]:
    logger.info("Generating agenda with this settings: {} ", settings)
    agenda_prompt = agenda(settings)
    response = send_message(agenda_prompt).content
    if response:
        result = response.split("---")
        return result
    else:
        return []


async def generate_content(settings: dict, agenda_elements: list[str]) -> list[dict]:
    result = []
    for agenda_element in agenda_elements:
        logger.info("Generating Content for agenda element: {} ", agenda_element)
        content_prompt = content(settings, agenda_element)
        response = send_message(content_prompt).content
        if not response:
            continue
        for paragraph in response.split("---"):
            paragraph = paragraph.strip()
            if paragraph.strip() == "":
                continue

            if paragraph.startswith("-"):
                paragraph = paragraph[1:]

            slide = {"content": paragraph, "title": agenda_element }
            result.append(slide)
    return result

async def export_pdf(slides: list[str]) -> str:
    return "data:application/pdf;base64,..."  # Fake output


async def export_pptx(slides: list[str]) -> str:
    return "data:application/vnd.openxmlformats-officedocument.presentationml.presentation;base64,..."