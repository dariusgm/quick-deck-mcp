from fastapi import FastAPI, Request
import uvicorn
import asyncio
from src.types import InputAgenda
import src.tool

app = FastAPI()

@app.post("/tools/call/generate_agenda")
async def generate_agenda(request: Request):
    req = await request.json()
    method = req.get("method")
    params = req.get("params", {})
    arguments = params.get("arguments", {})
    input_agenda = InputAgenda(**arguments)
    id_ = req.get("id")
    result = await src.tool.generate_agenda(input_agenda)
    return {"jsonrpc": "2.0", "result": result, "id": id_}

async def main():
    config = uvicorn.Config("main:app", host="0.0.0.0", port=9000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == '__main__':
    asyncio.run(main())