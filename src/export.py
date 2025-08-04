import asyncio
import json
import os
import aiofiles
from global_settings import TEMP_DIR
from loguru import logger
import pypandoc
# Worker inside same process
async def process_export_job(job_id: str, export_format: str):
    try:
        await export(job_id, export_format)
    except Exception as e:
        async with aiofiles.open(os.path.join(TEMP_DIR, f"{job_id}.json"), "wt") as status_error_handle:
            await status_error_handle.write(json.dumps({"status": "error", "error": str(e)}))

async def export(job_id: str, export_format: str):
    # Simulate slow export job
    status_file = os.path.join(TEMP_DIR, f"{job_id}.json")
    markdown_file = os.path.join(TEMP_DIR, f"{job_id}.md")

    # Here we export as reveal.js Slides
    if export_format == "html":
        async with aiofiles.open(os.path.join(TEMP_DIR, f"{job_id}.html"), "w") as outfile_handle:
            await outfile_handle.write(f"<html><body>Exported HTML for job {job_id}</body></html>")
    # For everything else we use pypandoc to convert the markdown file
    else:
        async with aiofiles.open(markdown_file, "rt") as f:
            markdown_content = await f.read()
            markdown_content = markdown_content.replace("---", "\n---\n")

            # ensure we have space before the speaker notes
            markdown_content = markdown_content.replace("::: notes", "\n::: notes")

            # now we need to write a temporary file to convert the markdown to pptx
            async with aiofiles.open(markdown_file, "wt") as outfile_handle:
                await outfile_handle.write(markdown_content)

            target_path = os.path.join(TEMP_DIR, f"{job_id}.{export_format}")

            # convert the markdown to pptx
            logger.debug(f"Converting {markdown_file} to {target_path} with format {export_format}")
            pypandoc.convert_file(source_file=markdown_file, outputfile=target_path, format='md', to=export_format)
            logger.debug(f"Converted {markdown_file} to {target_path}")

    # Update status
    async with aiofiles.open(status_file, "wt") as status_handle:
        await status_handle.write(json.dumps({"status": "done"}))
