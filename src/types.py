from pydantic import BaseModel


class Settings(BaseModel):
    topic: str
    audience: str
    style: str
    language: str
