import asyncio

from fastapi import APIRouter, Request
from sse_starlette import EventSourceResponse
import aiohttp

from gpt_server.schemas.prompt import Prompt
from .._config import APIs

router = APIRouter()

url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {APIs['groq']}",
    "Content-Type": "application/json",
}


async def get_content(data):
    async with aiohttp.ClientSession(headers=headers) as sess:
        async with sess.post(url, json=data, proxy=APIs["proxy"]) as res:
            async for chunk in res.content:
                if chunk:
                    yield chunk.decode("utf-8")[6:]


async def generate_data():
    for i in range(10):
        await asyncio.sleep(.1)  # Simulate some delay
        yield '{"choices":[{"index":0,"delta":{"content":" handle"}}]}'
    yield "[DONE]"


@router.post("/chat", status_code=200)
async def chat(request: Request, prompt: Prompt):

    data = {"model": "mixtral-8x7b-32768", "stream": True}
    for message in prompt.messages:
        if message.role == "system":
            message.content = message.content.replace("GitHub Copilot",
                                                      "Groq-mixtral")
    data["messages"] = [dict(msg) for msg in prompt.messages]
    return EventSourceResponse(get_content(data))
