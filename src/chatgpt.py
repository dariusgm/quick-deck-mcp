import os
from typing import AsyncIterator

from openai import AsyncOpenAI
from dotenv import load_dotenv
from openai.types.chat import ChatCompletionMessage

def _client():
    load_dotenv()
    api_key = os.environ["OPENAI_API_KEY"]
    return AsyncOpenAI(api_key=api_key)

client = _client()

async def send_message(message: list[dict[str, str | list[dict[str, str]]]]) -> AsyncIterator[ChatCompletionMessage]:
    stream = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=message,
        response_format={
            "type": "text"
        },
        temperature=1,
        max_completion_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stream=True
    )
    buffer = ""
    async for chunk in stream:
        content = chunk.choices[0].delta.content
        if content is None or content == '':
            continue
        if "\n" in content:
            yield buffer + content
            buffer = ""
        else:
            buffer += content