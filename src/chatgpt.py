import os

from openai import OpenAI
from dotenv import load_dotenv
from openai.types.chat import ChatCompletionMessage

def _client():
    load_dotenv()
    api_key = os.environ["OPENAI_API_KEY"]
    return OpenAI(api_key=api_key)

client = _client()

def send_message(message: list[dict[str, str | list[dict[str, str]]]]) -> ChatCompletionMessage:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=message,
        response_format={
            "type": "text"
        },
        temperature=1,
        max_completion_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message