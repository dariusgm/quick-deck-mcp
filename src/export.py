import json
import os
import time
from string import Template

import aiofiles
from global_settings import TEMP_DIR
from loguru import logger
import pypandoc
import markdown
REVEALJS_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <!-- feuilles de style -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css"
        crossorigin="anonymous" referrerpolicy="no-referrer" />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/black.css"
        crossorigin="anonymous" referrerpolicy="no-referrer" />
</head>
<body>
    <div class="reveal">
        <div class="slides">
            $sections
        </div>
    </div>

    <!-- javascript -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/5.1.0/reveal.js" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/5.1.0/plugin/notes/notes.js" crossorigin="anonymous" referrerpolicy="no-referrer"></script>


    <script>
        Reveal.initialize({
            controls: true,
            progress: true,
            history: true,
            center: true,
            touch: true,
            autoAnimateDuration: 0.5,
            plugins: [ RevealNotes ]
        });

    </script>

</body>

</html>"""

def markdown_to_html(md):
    r = []

    rendered_html = markdown.markdown(md)
    # we only need to replace a <strong> tag when it starts with "Speaker Notes" with  <aside class="notes"> </aside>
    rendered_clean_html = rendered_html.replace("<p>", "").replace("</p>", "")
    multiline_speaker_notes = False
    for line in rendered_clean_html.splitlines():
        if "::: notes" in line:
            multiline_speaker_notes = True
            r.append(line.replace("::: notes", '<aside class="notes">'))
        else:
            # waiting for closing </p> tag
            if multiline_speaker_notes:
                    if line.strip() == "":
                        r.append(f"{line}</aside>")
                        multiline_speaker_notes = False
                    else:
                        r.append(line)
            else:
               r.append(line)

    return "\n".join(r) + "\n"

# Worker inside same process
async def process_export_job(job_id: str, export_format: str):
    try:
        await export(job_id, export_format)
    except Exception as e:
        async with aiofiles.open(os.path.join(TEMP_DIR, f"{job_id}.json"), "wt") as status_error_handle:
            await status_error_handle.write(json.dumps({"status": "error", "error": str(e)}))

async def read_markdown(markdown_file):
    async with aiofiles.open(markdown_file, "rt") as f:
        return await f.read()

async def write_status(status_file, status):
    async with aiofiles.open(status_file, "wt") as status_handle:
        await status_handle.write(json.dumps(status))

async def write_markdown(markdown_file, content):
    async with aiofiles.open(markdown_file, "wt") as outfile_handle:
        await outfile_handle.write(content)

async def export_html(job_id: str):
    sections = []
    markdown_file = os.path.join(TEMP_DIR, f"{job_id}.md")
    async with aiofiles.open(os.path.join(TEMP_DIR, f"{job_id}.html"), "wt") as outfile_html_handle:
        # read the markdown file
        async with aiofiles.open(markdown_file, "rt") as markdown_handle:
            markdown_content = await markdown_handle.read()
            for slide in markdown_content.split("---"):
                reveal_js_content = markdown_to_html(slide)
                sections.append(f"<section>{reveal_js_content}</section>")

            # read the template
            template = Template(REVEALJS_TEMPLATE)

            # create final export
            content = template.substitute(sections="\n".join(sections))
            await outfile_html_handle.write(content)

async def export_rtf(job_id: str, export_format: str = "rtf"):
    """
    Export the markdown file to RTF format.
    This is a synchronous function that uses pypandoc to convert the markdown file.
    """
    markdown_file = os.path.join(TEMP_DIR, f"{job_id}.md")
    markdown_clean_file = os.path.join(TEMP_DIR, f"{job_id}_clean.md")


    target_path = os.path.join(TEMP_DIR, f"{job_id}.{export_format}")

    # Read the markdown content
    markdown_content = await read_markdown(markdown_file)
    markdown_content = markdown_content.replace("---", "\n---\n")
    markdown_content = markdown_content.replace("::: notes", "\n::: notes")

    # Write the cleaned markdown content to a temporary file
    await write_markdown(markdown_clean_file, markdown_content)

    # Convert the cleaned markdown file to RTF format
    pypandoc.convert_file(source_file=markdown_clean_file, outputfile=target_path, format='md', to=export_format)


async def export_pptx(job_id: str):
    markdown_file = os.path.join(TEMP_DIR, f"{job_id}.md")
    markdown_clean_file = os.path.join(TEMP_DIR, f"{job_id}_clean.md")
    export_format = "pptx"
    async with aiofiles.open(markdown_file, "rt") as f:
        markdown_content = await f.read()
        markdown_content = markdown_content.replace("---", "\n---\n")

        # ensure we have space before the speaker notes
        markdown_content = markdown_content.replace("::: notes", "\n::: notes")

        # now we need to write a temporary file to convert the markdown to pptx
        async with aiofiles.open(markdown_clean_file, "wt") as outfile_handle:
            await outfile_handle.write(markdown_content)

        target_path = os.path.join(TEMP_DIR, f"{job_id}.{export_format}")

        # convert the markdown to pptx
        pypandoc.convert_file(source_file=markdown_clean_file, outputfile=target_path, format='md', to=export_format)

async def export_pdf(job_id: str):
    markdown_file = os.path.join(TEMP_DIR, f"{job_id}.md")
    markdown_clean_file = os.path.join(TEMP_DIR, f"{job_id}_clean.md")
    export_format = "pdf"
    async with aiofiles.open(markdown_file, "rt") as f:
        markdown_content = await f.read()
        markdown_content = markdown_content.replace("---", "\n---\n")

        # speaker notes are not supported in pdf, so we remove the tags and just render the content
        markdown_content = markdown_content.replace("::: notes", "").replace(":::", "")

        # now we need to write a temporary file to convert the markdown to pdf
        async with aiofiles.open(markdown_clean_file, "wt") as outfile_handle:
            await outfile_handle.write(markdown_content)

        target_path = os.path.join(TEMP_DIR, f"{job_id}.{export_format}")

        # convert the markdown to pdf
        pypandoc.convert_file(source_file=markdown_clean_file, outputfile=target_path, format='md', to=export_format)

async def export_md(job_id: str):
    """
    Asynchronously export the markdown file to md format.
    As this is the default import format, there is not that much to do here.
    """

    pass

async def export_txt(job_id: str):
    markdown_file = os.path.join(TEMP_DIR, f"{job_id}.md")
    export_format = "txt"
    target_path = os.path.join(TEMP_DIR, f"{job_id}.{export_format}")

    # convert the markdown to txt
    pypandoc.convert_file(source_file=markdown_file, outputfile=target_path, format='md', to='plain')

async def export_tex(job_id: str):
    markdown_file = os.path.join(TEMP_DIR, f"{job_id}.md")
    markdown_clean_file = os.path.join(TEMP_DIR, f"{job_id}_clean.md")
    export_format = "tex"
    target_path = os.path.join(TEMP_DIR, f"{job_id}.{export_format}")

    # Read the markdown content
    async with aiofiles.open(markdown_file, "rt") as f:
        markdown_content = await f.read()
        markdown_content = markdown_content.replace("---", "\n---\n")

        # Write the cleaned markdown content to a temporary file
        async with aiofiles.open(markdown_clean_file, "wt") as outfile_handle:
            await outfile_handle.write(markdown_content)

        # Convert the cleaned markdown file to tex format
        pypandoc.convert_file(source_file=markdown_clean_file, outputfile=target_path, format='md', to='latex')

async def export(job_id: str, export_format: str):
    # Update status
    status_file = os.path.join(TEMP_DIR, f"{job_id}.json")
    start_time = time.time()
    await write_status(status_file, {"status": "running", "start": start_time, "export_format": export_format})

    match export_format:
        case "html":
            await export_html(job_id)
        case "rtf":
            await export_rtf(job_id)
        case "pdf":
            await export_pdf(job_id)
        case "pptx":
            await export_pptx(job_id)
        case "txt":
            await export_txt(job_id)
        case "md":
            await export_md(job_id)
        case "tex":
            await export_tex(job_id)
        case _:
            await write_status(status_file, {"status": "error", "start": start_time, "end": time.time(), "export_format": export_format, "error": f"Unsupported export format."})


    await write_status(status_file, {"status": "done", "start": start_time, "end": time.time(), "export_format": export_format})

