# quick-deck-mcp
an MCP Server for generating decks / slides.

# Quickstart
First, create a .env file in the root directory of the project with the following content:
```env
OPENAI_API_KEY=sk-proj-...
```

Now build the project and install the dependencies:
```bash
uv venv --python=3.13 --seed && . .venv/bin/activate && uv sync
```

Run the server:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000 --workers 4
```


Now you can use the example scripts that are placed in the `doc/` directory to generate agendas and content.


# verbose installation
```bash

# Installation
You need python 3.13.
You can use the [uv](https://docs.astral.sh/uv/getting-started/installation/) to manage the virtual environment and dependencies.
And you may need [rust](https://www.rust-lang.org/tools/install) to build some dependencies.
```bash
uv venv --python=3.13 --seed
. .venv/bin/activate
uv sync
```

# Installation System Dependencies
For the PDF generation, you need to install some system dependencies.
Here are the commands for Debian-based systems (like Ubuntu):
```bash
# Required for pdf generation
sudo apt-get install -y texlive-latex-base texlive-latex-recommended
```

# Doc
This MCP Server is designed to generate decks / slides based on a given topic, audience, style, and language.
We have several endpoints that you can call.

## Generate Agenda
You can generate an agenda for a given topic, audience, style, and language.
You can find the example call in the `doc/generate_agenda.sh` file.

## Generate Content
You can generate content for each agenda item.
When no agenda is provided, the server will generate an agenda based on the topic, audience, style, and language.
You can find the example call in the `doc/generate_content_plain.sh` file when providing no agenda, 
or you checkout the `doc/generate_content_explicit.sh` file when providing an explicit agenda.

The result will be streamed as markdown and can be saved to a file.

## Export
Pass the markdown file to the export tool to generate a PDF.
You can find the example call in the `doc/export.md` file.
It will return you a job ID, which you can use to check the status of the export job.

## Export Status
You can check the status of the export job using the job ID.
You can find the example call in the `doc/export.md` file.

## Download Export
After the job is completed by a json:

```json
{"status": "done"}
```
You can download the PDF file using the job ID. Again, you can find the example call in the `doc/export.md` file.