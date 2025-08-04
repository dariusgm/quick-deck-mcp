import hashlib
import json
import os

import aiofiles
from fastapi import FastAPI, Request, UploadFile, BackgroundTasks, File
import uvicorn
import asyncio

import src.export
from generator import agenda_generator, generate_content_generator
from src.app_types import Settings
from fastapi.responses import StreamingResponse, JSONResponse
from src.export import process_export_job
app = FastAPI()
from src.global_settings import TEMP_DIR
from loguru import logger

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

@app.post("/tools/call/generate_content")
async def generate_content(request: Request) -> StreamingResponse:
    req = await request.json()
    method = req.get("method")
    params = req.get("params", {})
    arguments = params.get("arguments", {})
    settings = Settings(**arguments)
    agenda = arguments.get("agenda", [])
    return StreamingResponse(generate_content_generator(settings, agenda), media_type="text/event-stream")

@app.get("/tools/call/export")
async def get_export(request: Request) -> StreamingResponse:
    """
    Endpoint to get the export file.
    This fetches the export file content.
    :return: A bytes object representing the export file.
    :rtype: bytes
    """
    job_id = request.query_params.get("job_id")
    if not job_id:
        return StreamingResponse(status_code=400, content={"error": "job_id is required"})

    for elements in os.listdir(TEMP_DIR):
        if elements.startswith(job_id) and not elements.endswith(".md") and not elements.endswith(".json"):
            async def file_stream():
                async with aiofiles.open(os.path.join(TEMP_DIR, elements), "rb") as f:
                    while True:
                        chunk = await f.read(8192)
                        if not chunk:
                            break
                        yield chunk
            return StreamingResponse(file_stream(), media_type="application/octet-stream")

    return StreamingResponse(status_code=404, content={"error": "job_id not found"})

@app.get("/tools/call/export_status")
async def export_status(request: Request) -> JSONResponse:
    """
    Endpoint to get the export file.
    This fetches the export file content.
    :return: A bytes object representing the export file.
    :rtype: bytes
    """
    job_id = request.query_params.get("job_id")
    if not job_id:
        return JSONResponse(status_code=400, content={"error": "job_id is required"})
    logger.info(f"Fetching status for job_id: {job_id}")
    status_file = os.path.join(TEMP_DIR, f"{job_id}.json")
    if os.path.exists(status_file):
        async with aiofiles.open(status_file, "rt") as f:
            status_content = await f.read()
            return JSONResponse(
                content=json.loads(status_content),
                media_type="application/json"
                )

    return JSONResponse(status_code=404, content={"error": "job_id not found"})




@app.post("/tools/call/export")
async def export(request: Request, background_tasks: BackgroundTasks, file: UploadFile = File(...)) -> JSONResponse:
    """
    Endpoint to trigger a async processing the previously generated agenda in markdown format to a given format.
    :return: A json Object with the a job status.
    :rtype: StreamingResponse
    """

    # Read and hash markdown content
    headers = request.headers
    raw_content = await file.read()
    content = str(raw_content, encoding="utf-8")
    job_id = hashlib.sha256(raw_content).hexdigest()

    # We just store everything in a temporary directory as flat files. Why not?
    status_file = os.path.join(TEMP_DIR, f"{job_id}.json")
    markdown_file = os.path.join(TEMP_DIR, f"{job_id}.md")

    # Detect the export format from the headers
    ACCEPT_TO_EXTENSION = {
        "application/pdf": "pdf",
        "text/html": "html",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation": "pptx",
        "application/msword": "doc",
        "application/vnd.ms-powerpoint": "ppt",
        "text/markdown": "md",
        "application/x-latex": "tex",
        "application/rtf": "rtf",
        "application/vnd.oasis.opendocument.text": "odt",
        "application/epub+zip": "epub",
        "text/plain": "txt"
    }
    accept_header = headers.get("accept", "application/pdf").lower()
    export_format = ACCEPT_TO_EXTENSION.get(accept_header, 'pdf')

    # Early exit if already processed
    # if os.path.exists(status_file) and os.path.exists(markdown_file):
    #     return JSONResponse(
    #         status_code=200,
    #         content={"status_url": f"/jobs/{job_id}"}
    #     )

    # Create markdown source file
    async with aiofiles.open(markdown_file, "wt") as f:
        await f.write(content)

    # Create initial status
    status = {"status": "processing"}
    async with aiofiles.open(status_file, "wt") as f:
        await f.write(json.dumps(status))

    # Add background task to process export
    background_tasks.add_task(process_export_job, job_id, export_format)

    return JSONResponse(
        status_code=202,
        content={"job_id": job_id}
    )


async def main():
    config = uvicorn.Config("main:app", host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == '__main__':
    asyncio.run(main())