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
uv run mcp install __main__.py
```
Alternatively, you can test it with the MCP Inspector:

```bash
uv run mcp dev __main__.py
```

Or you can run it as real http server:

```bash
uv run --with mcp mcp run __main__.py -t sse
```



# Example Usage for agenda generation
Make sure the server is running in sse mode:

```bash

curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tools/call",
    "params": {
      "name": "generate_agenda",
      "arguments":  {
          "topic": "Git Introduction",
          "audience": "Young IT Professionals",
          "style": "Fun educational content",
          "language": "German"
        }
      }
    }'
```
