import os
import sys
from string import Template
from typing import List, Literal
from mcp.server.fastmcp import FastMCP, Context

from pydantic import BaseModel
from loguru import logger
import sys
import src.prompt
import src.tool

logger.remove()
logger.add(sys.stdout, serialize=True)  # JSON output
logger.info("MCP Booting")



class InputAgenda(BaseModel):
    topic: str
    audience: str
    style: str
    language: str

class Slide(BaseModel):
    title: str
    content: str


class ExportParameters:
    format: Literal["pdf", "pptx"]





mcp = FastMCP("Quick Deck MCP")



@mcp.prompt("Generate an agenda for a presentation")
def generate_agenda_prompt(settings: dict) -> list[dict[str, str | list[dict[str, str]]]]:
    return src.prompt.agenda(settings)

@mcp.prompt("Generate Content for a presentation")
def generate_content_prompt(settings: dict, agenda: str) -> list[
    dict[str, str | list[dict[str, str]]]]:
    return src.prompt.content(settings, agenda)


# Basic prompt tools
@mcp.tool("Agenda Generation")
def generate_agenda(settings: dict) -> list[str]:
    logger.info("Generating agenda with this settings: {} ", settings)
    return src.tool.generate_agenda(settings)

@mcp.tool("Content Generation")
def generate_content(settings: dict, agenda: List[str]) -> List[dict]:
    logger.info("Generating content with this settings: {} {}", settings, agenda)
    return src.tool.generate_content(settings, agenda)

# Simulated export (pretend long-running)
@mcp.tool()
async def export_pdf(slides: List[str]) -> str:
    return "data:application/pdf;base64,..."  # Fake output

@mcp.tool()
async def export_pptx(slides: List[str]) -> str:
    return "data:application/vnd.openxmlformats-officedocument.presentationml.presentation;base64,..."
