from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import uvicorn
import asyncio
app = FastAPI()

class InputAgenda(BaseModel):
    topic: str
    audience: str
    style: str
    language: str

@app.post("/tools/call/generate_agenda")
async def generate_agenda(request: Request):
    req = await request.json()
    method = req.get("method")
    params = req.get("params", {})
    arguments = params.get("arguments", {})
    input_agenda = InputAgenda(**arguments)
    id_ = req.get("id")
    return {"jsonrpc": "2.0", "result": 200, "id": id_}

async def main():
    config = uvicorn.Config("main:app", host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == '__main__':
    asyncio.run(main())