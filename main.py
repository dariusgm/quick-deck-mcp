import hashlib
import json
import os

import aiofiles
from fastapi import FastAPI, Request, UploadFile, BackgroundTasks, File
import uvicorn
import asyncio

from generator import agenda_generator, generate_content_generator
from src.app_types import Settings
from fastapi.responses import StreamingResponse, JSONResponse

app = FastAPI()
temp_dir = "tmp"
os.makedirs(temp_dir, exist_ok=True)

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

@app.post("/tools/call/export")
async def export(file: UploadFile = File(...),
                 background_tasks: BackgroundTasks = None) -> JSONResponse:
    """
    Endpoint to trigger a async processing the previously generated agenda in markdown format to a given format.
    :return: A json Object with the a job status.
    :rtype: StreamingResponse
    """

    # Read and hash markdown content
    raw_content = await file.read()
    content = str(raw_content, encoding="utf-8")
    job_id = hashlib.sha256(raw_content).hexdigest()

    # We just store everything in a temporary directory as flat files. Why not?
    status_file = os.path.join(temp_dir, f"{job_id}.json")
    markdown_file = os.path.join(temp_dir, f"{job_id}.md")

    # Early exit if already processed
    if os.path.exists(status_file) and os.path.exists(markdown_file):
        with open(status_file, 'wt') as f:
            status_data = json.load(f)
        return JSONResponse(
            status_code=202,
            content={"job_id": job_id, "status": status_data.get("status", "unknown")}
        )

    # Create job dir and status file
    async with aiofiles.open(markdown_file, "wt") as f:
        await f.write(content)

    # Write initial status
    status = {"status": "processing"}
    async with aiofiles.open(status_file, "wt") as f:
        await f.write(json.dumps(status))

    # Add background task to process export
    background_tasks.add_task(process_export_job, job_id)

    return JSONResponse(
        status_code=202,
        content={"job_id": job_id, "status_url": f"/jobs/{job_id}"}
    )

# Worker inside same process
async def process_export_job(job_id: str):
    status_file = os.path.join(temp_dir, f"{job_id}.json")
    markdown_file = os.path.join(temp_dir, f"{job_id}.md")
    output_file = os.path.join(temp_dir, f"{job_id}.pdf")

    try:
        # Simulate slow export job
        await asyncio.sleep(1)  # replace with real conversion logic

        # Dummy "PDF"
        async with aiofiles.open(output_file, "w") as outfile_handle:
            await outfile_handle.write(f"Exported PDF for job {job_id}")

        # Update status
        async with aiofiles.open(status_file, "wt") as status_handle:
            await status_handle.write(json.dumps({"status": "done"}))
    except Exception as e:
        async with aiofiles.open(status_file, "wt") as status_error_handle:
            await status_error_handle.write(json.dumps({"status": "error", "error": str(e)}))

async def main():
    config = uvicorn.Config("main:app", host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == '__main__':
    asyncio.run(main())