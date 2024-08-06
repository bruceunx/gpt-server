import os

from fastapi import APIRouter, Request
from sse_starlette import EventSourceResponse
import aiohttp

from gpt_server.schemas.prompt import Prompt

router = APIRouter()

url = os.environ['GROQ_URL']

headers = {
    "Authorization": f"Bearer {os.environ['GROQ_KEY']}",
    "Content-Type": "application/json",
}

PROXY = os.environ['proxy'] if 'proxy' in os.environ else None


async def get_content(data):
    async with aiohttp.ClientSession(headers=headers) as sess:
        async with sess.post(url, json=data, proxy=PROXY) as res:
            async for chunk in res.content:
                if chunk:
                    yield chunk.decode("utf-8")[6:]
                else:
                    yield '{"choices":[{"index":0,"delta":{"content":" handle"}}]}'
                    yield "[DONE]"
                    break


@router.post("/chat", status_code=200)
async def chat(request: Request, prompt: Prompt):

    data = {"model": "llama-3.1-70b-versatile", "stream": True}
    less_messages = []
    if len(prompt.messages) > 4:
        less_messages = [prompt.messages[0]] + prompt.messages[-3:]
    else:
        less_messages = prompt.messages
    for message in less_messages:
        if message.role == "system":
            message.content = message.content.replace("GitHub Copilot",
                                                      "Groq-mixtral")
    data["messages"] = [dict(msg) for msg in less_messages]
    return EventSourceResponse(get_content(data))
