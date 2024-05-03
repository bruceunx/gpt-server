import os
import json
from typing import Any

from fastapi import APIRouter, Request
from sse_starlette import EventSourceResponse
import aiohttp

from gpt_server.schemas.prompt import Prompt

router = APIRouter()

api_key = os.environ['COHERE_KEY']

url = os.environ['COHERE_URL']

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}


async def get_content(data):
    signal = False
    async with aiohttp.ClientSession(headers=headers) as sess:
        async with sess.post(url, json=data) as res:
            async for chunk in res.content:
                if chunk:
                    tmp = json.loads(chunk.decode("utf-8"))
                    if 'text' not in tmp:
                        continue
                    if tmp["is_finished"]:
                        signal = True
                        yield "[DONE]"
                    else:
                        yield json.dumps({
                            "choices": [{
                                "index": 0,
                                "delta": {
                                    "content": tmp["text"]
                                }
                            }]
                        })
                else:
                    yield '{"choices":[{"index":0,"delta":{"content":"error from claude"}}]}'
                    yield "[DONE]"
                    break
            if not signal:
                yield "[DONE]"


@router.post("/chat", status_code=200)
async def chat_cohere(request: Request, prompt: Prompt):

    data: dict[str, Any] = {"stream": True}
    chat_history = []
    chat_history.append({
        "role": "SYSTEM",
        "message": prompt.messages[0].content
    })
    less_messages = []
    if len(prompt.messages) > 6:
        less_messages = prompt.messages[-4:-1]
    else:
        less_messages = prompt.messages[1:-1]
    for msg in less_messages:
        chat_history.append({"role": msg.role.upper(), "message": msg.content})

    data["chat_history"] = chat_history
    data["message"] = prompt.messages[-1].content

    return EventSourceResponse(get_content(data))
