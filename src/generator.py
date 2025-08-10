from loguru import logger

import src.tool
from app_types import Settings


async def agenda_generator(input_agenda: Settings):
    """
    Generator function to yield agenda items.
    """
    logger.debug("Generating agenda with settings: {}", input_agenda)
    async for item in src.tool.generate_agenda(input_agenda):
        yield item + "\n"


async def generate_content_generator(settings: Settings, agenda_elements: list[str]):
    """
    """
    if len(agenda_elements) == 0:
        logger.info(f"No agenda elements found for {settings}")

        async for element in src.tool.generate_agenda(settings):
            # remove typical markdown header from the element
            element = element.replace("# ", "").strip()
            # remove "-" from the beginning of the element
            element = element.lstrip("-").strip()

            if element == "":
                continue
            # Check if the element is a separator - we just pass it through
            if element == "---":
                yield "---"
                continue
            async for result in src.tool.generate_content(settings, element):
                for item in result:
                    yield f"{item}"

    else:
        for element in agenda_elements:
            async for result in src.tool.generate_content(settings, element):
                for item in result.split("\n"):
                    yield f"{item}"
