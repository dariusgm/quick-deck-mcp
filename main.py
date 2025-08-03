from fastapi import FastAPI, Request
import uvicorn
import asyncio
from src.app_types import Settings
import src.tool
from fastapi.responses import StreamingResponse
from loguru import logger
app = FastAPI()

async def agenda_generator(input_agenda: Settings):
    """
    Generator function to yield agenda items.
    This simulates a long-running process.
    """
    logger.debug("Generating agenda with settings: {}", input_agenda)
    async for item in src.tool.generate_agenda(input_agenda):
        yield item + "\n"

@app.post("/tools/call/generate_agenda")
async def generate_agenda(request: Request) -> StreamingResponse:
    """
    Endpoint to generate an agenda based on the provided input.
    The request should contain a JSON body with the method, params, and arguments.
    The response will be a streaming response that yields agenda items.
    :param request: The incoming request containing the method and parameters.
    :type request: Request
    :return: A StreamingResponse that yields agenda items.
    :rtype: StreamingResponse
    """
    req = await request.json()
    method = req.get("method")
    params = req.get("params", {})
    arguments = params.get("arguments", {})
    input_agenda = Settings(**arguments)
    id_ = req.get("id")
    return StreamingResponse(agenda_generator(input_agenda), media_type="text/event-stream")

async def generate_content_generator(settings: Settings, agenda_elements: list[str]):
    """
    Generator function to yield content for each agenda element.
    This simulates a long-running process.
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


@app.post("/tools/call/generate_content")
async def generate_content(request: Request) -> StreamingResponse:
    req = await request.json()
    method = req.get("method")
    params = req.get("params", {})
    arguments = params.get("arguments", {})
    settings = Settings(**arguments)
    agenda = arguments.get("agenda", [])
    return StreamingResponse(generate_content_generator(settings, agenda), media_type="text/event-stream")

async def main():
    config = uvicorn.Config("main:app", host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == '__main__':
    asyncio.run(main())