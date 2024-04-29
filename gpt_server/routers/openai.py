import asyncio

from fastapi import APIRouter, Request
from sse_starlette import EventSourceResponse
import aiohttp

from gpt_server.schemas.prompt import Prompt
from .._config import APIs

router = APIRouter()

url = "https://api.pumpkinaigc.online/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {APIs['openai']}",
    "Content-Type": "application/json",
}


async def get_content(data):
    async with aiohttp.ClientSession(headers=headers) as sess:
        async with sess.post(url, json=data) as res:
            async for chunk in res.content:
                if chunk:
                    yield chunk.decode("utf-8")[6:]
                else:
                    yield '{"choices":[{"index":0,"delta":{"content":"error from openai"}}]}'
                    yield "[DONE]"
                    break


async def generate_data():
    for i in range(10):
        await asyncio.sleep(.1)  # Simulate some delay
        yield '{"choices":[{"index":0,"delta":{"content":" handle"}}]}'
    yield "[DONE]"


@router.post("/chat", status_code=200)
async def chat(request: Request, prompt: Prompt):

    data = {"model": "gpt-4-turbo", "stream": True}
    less_messages = []
    if len(prompt.messages) > 6:
        less_messages = prompt.messages[-4:]
    else:
        less_messages = prompt.messages[1:]
    data["messages"] = [dict(msg) for msg in less_messages]
    return EventSourceResponse(get_content(data))
