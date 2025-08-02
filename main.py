from fastapi import FastAPI, Request
import uvicorn
import asyncio
from src.types import Settings
import src.tool
from fastapi.responses import StreamingResponse

app = FastAPI()

async def agenda_generator(input_agenda: Settings):
    """
    Generator function to yield agenda items.
    This simulates a long-running process.
    """
    yield "Generating agenda for topic: {}\n".format(input_agenda.topic)
    yield "Audience: {}\n".format(input_agenda.audience)
    yield "Style: {}\n".format(input_agenda.style)
    yield "Language: {}\n".format(input_agenda.language)
    result = await src.tool.generate_agenda(input_agenda)
    for item in result:
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
    return StreamingResponse(agenda_generator(input_agenda), media_type="text/plain")

async def generate_content_generator(input_agenda: Settings, agenda_elements: list[str]):
    """
    Generator function to yield content for each agenda element.
    This simulates a long-running process.
    """
    if len(agenda_elements) == 0:
        yield "Agenda elements are empty. Generating agenda first...\n"
        agenda_elements = src.tool.generate_agenda(input_agenda)

    for element in agenda_elements:
        yield f"Generating content for agenda element: {element}\n"
        results = await src.tool.generate_content(input_agenda, element)

        for result in results:
            for item in result.split("\n"):
                yield f"{item}\n"
            yield "\n---\n"

@app.post("/tools/call/generate_content")
async def generate_content(request: Request) -> StreamingResponse:
    req = await request.json()
    method = req.get("method")
    params = req.get("params", {})
    arguments = params.get("arguments", {})
    settings = Settings(**arguments)
    agenda = arguments.get("agenda", [])

    return StreamingResponse(generate_content_generator(settings, agenda), media_type="text/plain")

async def main():
    config = uvicorn.Config("main:app", host="0.0.0.0", port=9000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == '__main__':
    asyncio.run(main())