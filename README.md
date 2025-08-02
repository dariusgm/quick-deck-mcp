# quick-deck-mcp
an MCP Server for generating decks / slides.

# Installation
You need python 3.13.
You can use the [uv](https://docs.astral.sh/uv/getting-started/installation/) to manage the virtual environment and dependencies.
And you may need [rust](https://www.rust-lang.org/tools/install) to build some dependencies.
```bash
uv venv --python=3.13 --seed
. .venv/bin/activate
uv sync
```


# Execute via Docker
```bash
docker run -it --rm -v $(pwd):/app -w /app
```

# Running
You can install this server in Claude Desktop and interact with it right away by running:
```bash
uvicorn main:app
```
# Example Usage for agenda generation
Make sure the server is running in sse mode:

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
Example output:
```json
{
  "result": [
    "# Agenda for Git Introduction Presentation\n\n",
    "\n\n## Understanding Git Basics: \n- Introduction to version control systems.\n- What Git is: Definition and key features.\n- The advantages of using Git for project collaboration.\n\n",
    "\n\n## Git History and Evolution:\n- The origin of Git and its creator, Linus Torvalds.\n- Milestones in Git's development.\n- How Git has become a standard in software development.\n\n",
    "\n\n## Core Git Concepts:\n- Repository: What it is and how it works.\n- Commits, branches, and merges: Basic terminology explained.\n- Local vs. remote repositories and their significance.\n\n",
    "\n\n## Setting Up Git:\n- Overview of the installation process for different operating systems.\n- Configuring Git for first-time users.\n- Creating your first repository: A step-by-step guide.\n\n",
    "\n\n## Basic Git Commands:\n- Introduction to essential Git commands: `git init`, `git clone`, `git add`, and `git commit`.\n- Understanding the Git workflow.\n- Practical examples of using commands in a project setting.\n\n",
    "\n\n## Collaboration with Git:\n- Working with branches: How to create and manage them.\n- Pull requests: What they are and how to use them.\n- Resolving merge conflicts: Tips and techniques.\n\n",
    "\n\n## Best Practices and Tips:\n- Writing meaningful commit messages.\n- Regularly pushing changes: Why it’s important.\n- Staying organized with branches and workflows.\n\n",
    "\n\n## Resources for Further Learning:\n- Recommended books, websites, and tutorials for mastering Git.\n- Communities and forums for support and networking.\n- Opportunities for practical, real-world experience with Git. \n\n",
    " \n\n## Q&A Session:\n- Open floor for questions and clarifications.\n- Discuss common challenges and solutions encountered when using Git."
  ]
}
```

# Example Usage for content generation with explicit agenda
You can use the `generate_agenda` endpoint to generate the agenda. 
This can than be passed to the `generate_content` endpoint to generate the content for each agenda item.
When leaving out the agenda, a agenda will be generated based on the topic, audience, style, and language.

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
    }'

```