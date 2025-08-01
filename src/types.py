from pydantic import BaseModel


class InputAgenda(BaseModel):
    topic: str
    audience: str
    style: str
    language: str
