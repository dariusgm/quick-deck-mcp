# quick-deck-mcp
This MCP Server is designed to generate decks / slides based on a given topic, audience, style, and language.
It uses the OpenAI API to generate the content and can export it to PDF or other formats using Pandoc and TeX Live.
It's designed to be used in an educational context, but can be used for any kind of presentation generation.

# Docker Quickstart
This is a minimal setup to get you started with the MCP Server.
You can get the MCP Server running in a few minutes via docker.

    Ensure to create a `.env` file with your OpenAI API key as described below.

```bash
docker build --build-arg PROXY= -t dariusgm/quick-deck-mcp:latest .
```

```bash
docker run -it -p 8000:8000 -v $(pwd)/.env:/app/.env dariusgm/quick-deck-mcp:latest
```

You can find the Image on [Docker Hub](https://example.com).

# Quickstart
Install in the order:
* Pandoc to convert markdown to PDF.
* texlive to generate the PDF from the markdown.
* Something to execute HTTP requests, like `curl` or `wget`.
* Python 3.13 or higher is required.
* [rust](https://www.rust-lang.org/tools/install) to build some dependencies.
* [uv](https://docs.astral.sh/uv/getting-started/installation/) to manage the virtual environment and dependencies.
* [OpenAI API key](https://platform.openai.com/account/api-keys) to use the mcp server. Other LLM providers are not supported yet.


## Quickstart - OpenAI API Key
* Create a .env file in the root directory of the project with the following content:
```env
OPENAI_API_KEY=sk-proj-...
```

This is your OpenAI API key, which is required to use the mcp server. You can get it from your OpenAI account.
All Payments are done via this key, so make sure you have enough credits on your account.
Ensure that the `.env` file is not committed to your version control system, as it contains sensitive information.
And make sure to check the legal implications of using the OpenAI API in your country, your company and for your use case.

## Quickstart - System Dependencies
Besides the python dependencies, you need to install some system dependencies for the PDF generation.
For a debian based system (like ubuntu), you can use the following commands:
```bash
# Required for pdf generation
sudo apt-get install -y texlive-latex-base texlive-latex-recommended
# Required for converting markdown to something else
sudo apt-get install -y pandoc
```


Now build the project and install the dependencies:
```bash
uv venv --python=3.13 --seed && . .venv/bin/activate && uv sync
```
# Server

Run the server:
```bash
uvicorn main:app  --host 127.0.0.1 --port 8000 --workers 4
```
or for more dev-like experience with reloading:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Please note that the server is not designed to be deployed publicly accessible.
Primarily, because no authorization is implemented.
It is intended for local development and closed deployments.

# The MPC Server
We have several endpoints that you can call.
The general flow is as follows:
* Generate Agenda
* Generate Content
* Export

Let's now get into the details of each step.

## Generate Agenda
You can generate an agenda for a given topic, audience, style, and language.
Here is a simple example call using `curl`:

```bash
curl -X POST http://127.0.0.1:8000/tools/call/generate_agenda \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "jsonrpc": "2.0", 
    "params": {
      "arguments":  {
          "topic": "Git Introduction",
          "audience": "Young IT Professionals",
          "style": "Fun educational content",
          "language": "English"
        }
      }
    }'
```

Note that the response is streamed as a server-sent event (SSE) and can be saved to a file.

## Generate Content
After we have the agenda, we can generate the content for each agenda item.
Here is an example call using `curl`:

```bash
curl -X POST http://127.0.0.1:8000/tools/call/generate_content \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "params": {
      "arguments":  {
          "topic": "Git Introduction",
          "audience": "Young IT Professionals",
          "style": "Fun educational content",
          "language": "English"
        }
      }
    }' > git.md
```

Note that this is also streamed as a server-sent event (SSE) and can be saved to a file.
In the provided example, the content is saved to a file named `git.md`.
When no agenda is provided, the server will generate an agenda based on the topic, audience, style, and language.

You can also use an explicit agenda by providing it in the request that the previous got via the `generate_agenda` endpoint.

```bash
curl -X POST http://127.0.0.1:8000/tools/call/generate_content \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "params": {
      "arguments":  {
          "topic": "Git Introduction",
          "audience": "Young IT Professionals",
          "style": "Fun educational content",
          "language": "English",
          "agenda": [
            "Overview of Version Control Systems",
            "Introduction to Git",
            "Key Features of Git",
            "Installing Git",
            "Basic Git Commands",
            "Branching and Merging in Git",
            "Working with Remote Repositories",
            "Best Practices for Using Git",
            "Q&A Session"
          ]
        }
      }
    }' > git.md
```

The result will be streamed as markdown and can be saved to a file. Again we use `git.md` as the file name.

## Export
After we have the content, we can export it to a PDF file or other formats.
As the export takes some time, the processing is done in the background.
You will get a HTTP response with 202, which means that the job is accepted and will be processed in the background.
The response is a JSON object with the job id.
You need to use this job id to check the status of the export job and to download the PDF file once it is completed.
But first, we need to trigger the export tool using the previously generated Markdown file `git.md`.
When providing no "Accept" header, the server will trigger a PDF export by default.
Other formats are implemented by pandoc but not yet fully tested. Feedback is welcome.

| MIME-Type in Accept Header                                                | Format | Supported? |
|---------------------------------------------------------------------------|--------|------------|
| application/pdf (default)                                                 | pdf    | Yes        |
| text/html (reveal_js)                                                     | html   | Yes        |
| application/vnd.openxmlformats-officedocument.wordprocessingml.document   | docx   | No         |
| application/vnd.openxmlformats-officedocument.presentationml.presentation | pptx   | Yes        |
| application/msword                                                        | doc    | No         |
| application/vnd.ms-powerpoint                                             | ppt    | No         |
| text/markdown                                                             | md     | Yes        |
| application/x-latex                                                       | tex    | Yes        |
| application/rtf                                                           | rtf    | Yes        |
| application/vnd.oasis.opendocument.text                                   | odt    | No         |
| application/epub+zip                                                      | epub   | No         |
| text/plain                                                                | txt    | Yes        |

```bash
curl -X POST http://127.0.0.1:8000/tools/call/export -H "Accept: text/html" -F "file=@git.md" | jq '.job_id' > job_id.txt
```


## Export Status
After you have triggered the export, you can check the status of the export job using the job ID.
```bash
curl -X GET http://127.0.0.1:8000/tools/call/export_status?job_id=$(cat job_id.txt | sed 's/"//g') 
```

The response will be a JSON object with the status of the export job. The possible statuses are:
- `running`: The export job is still running. Depending on the size of the Markdown file, this can take some minutes.
- `done`: The export job is completed and the exported file is ready to be downloaded.
- `error`: There was an error during the export job.


    When running the Export job with only one worker (or with `--reload`), you can't fetch the status as the server is blocked.

## Download Export
After the job is completed by a json:

```json
{"status": "done"}
```
You can download the PDF file using the job ID.
```bash
curl -X GET http://127.0.0.1:8000/tools/call/export?job_id=$(cat job_id.txt | sed 's/"//g') -o git.pdf
```

Current Limitations:
- The server is not designed to be publicly accessible.
- No authorization is implemented.
- Only the OpenAI API is supported for generating content.
- The export tool only supports PDF export via Pandoc and TeX Live.
- The export tool only supports Markdown files as input.

Further Improvements:
Please feel free to contribute /suggest features to the project and improve it.