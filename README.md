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

# Installation System Dependencies
```bash
# Required for pdf generation
sudo apt-get install -y texlive-latex-base texlive-latex-recommended
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
bash doc/generate_agenda.sh
```
Example output:
```markdown
# Agenda for Git Introduction Presentation
## Understanding Version Control: 
- What is version control and why it matters for developers.
- Benefits of managing code changes in collaborative environments.
## The Basics of Git:  
- Introduction to Git and its core functions.
- Key concepts: repositories, commits, branches, and merges.
## Setting Up Git: 
- Steps to install Git on various platforms.
- Configuring your Git environment: user information and preferences.
## Common Git Commands: 
- Overview of essential commands: `clone`, `add`, `commit`, `push`, and `pull`.
- Practical examples of how to use these commands effectively.
## Branching and Merging: 
- Explanation of branches in Git and their significance in development.
- How to create, switch, and merge branches.
## Collaboration with Git: 
- Working in teams using Git: pull requests and code reviews.
- Integrating Git with platforms like GitHub and GitLab.
## Best Practices and Tips: 
- Recommended practices for commit messages and workflow strategies.
- Common pitfalls to avoid when working with Git.
## Resources for Further Learning: 
- Suggestions for tutorials, books, and online courses to deepen your knowledge.
- Community resources and where to ask for help when needed.
```

# Example Usage for content generation with explicit agenda
You can use the `generate_agenda` endpoint to generate the agenda. 
This can than be passed to the `generate_content` endpoint to generate the content for each agenda item.
When leaving out the agenda, a agenda will be generated based on the topic, audience, style, and language.

```bash
bash doc/generate_content_plain.sh


```