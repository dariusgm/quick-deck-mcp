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